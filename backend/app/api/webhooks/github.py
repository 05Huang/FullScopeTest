# GitHub Webhook Receiver

import hashlib
import hmac
from typing import Optional
from flask import request, current_app
from .. import api_bp
from ...extensions import db
from ...models.github_integration import GitHubIntegration
from ...models.test_run import TestRun
from ...models.project import Project
from ...utils.response import success_response, error_response
from ...core.logging import get_logger
from ...services.trigger_rule_service import evaluate_push_event, evaluate_pr_event

logger = get_logger(__name__)

def _verify_github_signature(payload, signature, secret):
    if not signature or not secret:
        return False
    if signature.startswith('sha256='):
        signature = signature[7:]
    expected = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)

def _find_integration_for_repo(full_name):
    integrations = GitHubIntegration.query.filter_by(is_active=True).all()
    for integration in integrations:
        if integration._is_token_valid():
            return integration
    return None

@api_bp.route('/webhooks/github', methods=['POST'])
def github_webhook():
    webhook_secret = current_app.config.get('GITHUB_WEBHOOK_SECRET', '')
    if webhook_secret:
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature:
            logger.warning('GitHub webhook missing signature')
            return error_response(401, 'Missing signature')
        payload = request.get_data()
        if not _verify_github_signature(payload, signature, webhook_secret):
            logger.warning('GitHub webhook signature verification failed')
            return error_response(401, 'Signature verification failed')
    event_type = request.headers.get('X-GitHub-Event', '')
    delivery_id = request.headers.get('X-GitHub-Delivery', '')
    payload = request.get_json() or {}
    logger.info('GitHub webhook received', event_type=event_type, delivery_id=delivery_id, action=payload.get('action'))
    try:
        if event_type == 'push':
            return _handle_push_event(payload)
        elif event_type == 'pull_request':
            return _handle_pull_request_event(payload)
        elif event_type == 'ping':
            return success_response(message='pong')
        else:
            return success_response(message=f'Event {event_type} ignored')
    except Exception as exc:
        logger.error('Failed to handle GitHub webhook', error=str(exc))
        return error_response(500, str(exc))


def _handle_push_event(payload):
    """Handle push event"""
    repo = payload.get('repository', {})
    ref = payload.get('ref', '')
    commits = payload.get('commits', [])
    head_commit = payload.get('head_commit', {})

    changed_files = []
    for commit in commits:
        changed_files.extend(commit.get('added', []))
        changed_files.extend(commit.get('modified', []))
        changed_files.extend(commit.get('removed', []))

    integration = _find_integration_for_repo(repo.get('full_name', ''))
    if not integration:
        return success_response(message='No integration found')

    trigger_result = evaluate_push_event(
        ref=ref,
        changed_files=changed_files,
        commit_message=head_commit.get('message', ''),
        repository=repo.get('full_name', ''),
    )
    if not trigger_result.get('should_trigger'):
        return success_response(message='No trigger matched')

    test_plan = _create_test_plan_from_push(payload, trigger_result, integration)
    return success_response(data={'test_plan_id': test_plan.id if test_plan else None, 'triggered_by': 'push'})


def _handle_pull_request_event(payload):
    """Handle pull_request event"""
    action = payload.get('action', '')
    pr = payload.get('pull_request', {})
    repo = payload.get('repository', {})

    if action not in ('opened', 'synchronize', 'reopened'):
        return success_response(message=f'Ignored action: {action}')

    integration = _find_integration_for_repo(repo.get('full_name', ''))
    if not integration:
        return success_response(message='No integration found')

    trigger_result = evaluate_pr_event(
        action=action,
        head_branch=pr.get('head', {}).get('ref', ''),
        base_branch=pr.get('base', {}).get('ref', ''),
        pr_number=pr.get('number'),
        pr_title=pr.get('title', ''),
        repository=repo.get('full_name', ''),
        changed_files=[],
    )
    if not trigger_result.get('should_trigger'):
        return success_response(message='No trigger matched')

    test_plan = _create_test_plan_from_pr(payload, trigger_result, integration)
    return success_response(data={'test_plan_id': test_plan.id if test_plan else None, 'triggered_by': 'pull_request'})


def _create_test_plan_from_push(payload, trigger_result, integration):
    """Create test plan from push event"""
    repo = payload.get('repository', {})
    head_commit = payload.get('head_commit', {})

    project = _find_or_create_project(repo.get('full_name', ''), integration)
    if not project:
        return None

    test_run = TestRun(
        project_id=project.id,
        name=f'Push Test - {repo.get("full_name", "")}',
        test_type=trigger_result.get('test_type', 'api'),
        status='pending',
        trigger_source='github_push',
        trigger_metadata={
            'repository': repo.get('full_name'),
            'ref': payload.get('ref'),
            'commit_sha': head_commit.get('id'),
            'commit_message': head_commit.get('message'),
        },
        created_by_user_id=integration.user_id,
    )

    db.session.add(test_run)
    db.session.commit()
    _schedule_test_execution(test_run, trigger_result)
    return test_run


def _create_test_plan_from_pr(payload, trigger_result, integration):
    """Create test plan from pull_request event"""
    pr = payload.get('pull_request', {})
    repo = payload.get('repository', {})

    project = _find_or_create_project(repo.get('full_name', ''), integration)
    if not project:
        return None

    test_run = TestRun(
        project_id=project.id,
        name=f'PR #{pr.get("number")} Test',
        test_type=trigger_result.get('test_type', 'api'),
        status='pending',
        trigger_source='github_pr',
        trigger_metadata={
            'repository': repo.get('full_name'),
            'pr_number': pr.get('number'),
            'pr_title': pr.get('title'),
            'head_branch': pr.get('head', {}).get('ref'),
            'base_branch': pr.get('base', {}).get('ref'),
        },
        created_by_user_id=integration.user_id,
    )

    db.session.add(test_run)
    db.session.commit()
    _schedule_test_execution(test_run, trigger_result)
    return test_run


def _find_or_create_project(repo_name, integration):
    """Find or create project by repository name"""
    project = Project.query.filter_by(
        github_repository=repo_name,
        owner_id=integration.user_id,
    ).first()

    if project:
        return project

    repo_parts = repo_name.split('/')
    project_name = repo_parts[-1] if len(repo_parts) > 1 else repo_name

    project = Project(
        name=project_name,
        description=f'Auto-created from {repo_name}',
        owner_id=integration.user_id,
        github_repository=repo_name,
    )

    db.session.add(project)
    db.session.commit()
    return project


def _schedule_test_execution(test_run, trigger_result):
    """Schedule test execution"""
    try:
        from ...tasks import run_api_collection_task

        test_type = trigger_result.get('test_type', 'api')
        target_id = trigger_result.get('target_id')

        if test_type == 'api' and target_id:
            task = run_api_collection_task.delay(
                collection_id=target_id,
                environment_id=None,
                test_run_id=test_run.id,
            )
            test_run.celery_task_id = task.id
            db.session.commit()
            logger.info('Scheduled API test', test_run_id=test_run.id, task_id=task.id)
    except Exception as exc:
        logger.error('Failed to schedule test', error=str(exc))

