"""
GitLab Webhook Receiver

处理 GitLab merge request 和 push webhook，
逻辑与 GitHub 一致，生成 GitLab Pipeline 状态回写。
"""

import hashlib
import hmac
from flask import request, current_app
from .. import api_bp
from ...extensions import db
from ...models.test_run import TestRun
from ...models.project import Project
from ...utils.response import success_response, error_response
from ...core.logging import get_logger
from ...services.trigger_rule_service import evaluate_push_event, evaluate_pr_event

logger = get_logger(__name__)


def _verify_gitlab_signature(payload, signature, secret):
    if not signature or not secret:
        return False
    if signature.startswith('sha256='):
        signature = signature[7:]
    expected = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


@api_bp.route('/webhooks/gitlab', methods=['POST'])
def gitlab_webhook():
    webhook_secret = current_app.config.get('GITLAB_WEBHOOK_SECRET', '')
    if webhook_secret:
        signature = request.headers.get('X-Gitlab-Token', '')
        if not signature:
            return error_response(401, 'Missing signature')
        payload = request.get_data()
        if not _verify_gitlab_signature(payload, signature, webhook_secret):
            return error_response(401, 'Signature verification failed')

    event_type = request.headers.get('X-Gitlab-Event', '')
    payload = request.get_json() or {}

    try:
        if event_type == 'Push Hook':
            return _handle_push_event(payload)
        elif event_type == 'Merge Request Hook':
            return _handle_merge_request_event(payload)
        else:
            return success_response(message=f'Event {event_type} ignored')
    except Exception as exc:
        logger.error('Failed to handle GitLab webhook', error=str(exc))
        return error_response(500, str(exc))


def _handle_push_event(payload):
    project = payload.get('project', {})
    ref = payload.get('ref', '')
    commits = payload.get('commits', [])
    changed_files = []
    for commit in commits:
        changed_files.extend(commit.get('added', []))
        changed_files.extend(commit.get('modified', []))
        changed_files.extend(commit.get('removed', []))

    repo_name = project.get('path_with_namespace', '')
    project_obj = _find_or_create_project(repo_name)
    if not project_obj:
        return error_response(500, 'Failed to find or create project')

    trigger_result = evaluate_push_event(ref=ref, changed_files=changed_files, commit_message=commits[0].get('message', '') if commits else '', repository=repo_name, project_id=project_obj.id)
    if not trigger_result.get('should_trigger'):
        return success_response(message='No trigger matched')

    head_commit = commits[-1] if commits else {}
    test_run = TestRun(project_id=project_obj.id, name='Push Test - ' + repo_name, test_type=trigger_result.get('test_type', 'api'), status='pending', trigger_source='gitlab_push', trigger_metadata={'repository': repo_name, 'ref': ref, 'commit_sha': head_commit.get('id'), 'commit_message': head_commit.get('message')}, created_by_user_id=project_obj.owner_id)
    db.session.add(test_run)
    db.session.commit()
    _schedule_test_execution(test_run, trigger_result)
    return success_response(data={'test_run_id': test_run.id, 'triggered_by': 'push'})


def _handle_merge_request_event(payload):
    attrs = payload.get('object_attributes', {})
    action = attrs.get('action', '')
    project = payload.get('project', {})
    if action not in ('open', 'update', 'reopen'):
        return success_response(message=f'Ignored action: {action}')

    repo_name = project.get('path_with_namespace', '')
    project_obj = _find_or_create_project(repo_name)
    if not project_obj:
        return error_response(500, 'Failed to find or create project')

    trigger_result = evaluate_pr_event(action=action, head_branch=attrs.get('source_branch', ''), base_branch=attrs.get('target_branch', ''), pr_number=attrs.get('iid', 0), pr_title=attrs.get('title', ''), repository=repo_name, changed_files=[])
    if not trigger_result.get('should_trigger'):
        return success_response(message='No trigger matched')

    mr_iid = attrs.get('iid', 0)
    mr_title = attrs.get('title', '')
    test_run = TestRun(project_id=project_obj.id, name='MR !' + str(mr_iid) + ' Test - ' + mr_title, test_type=trigger_result.get('test_type', 'api'), status='pending', trigger_source='gitlab_mr', trigger_metadata={'repository': repo_name, 'mr_iid': mr_iid, 'mr_title': mr_title, 'source_branch': attrs.get('source_branch'), 'target_branch': attrs.get('target_branch')}, created_by_user_id=project_obj.owner_id)
    db.session.add(test_run)
    db.session.commit()
    _schedule_test_execution(test_run, trigger_result)
    return success_response(data={'test_run_id': test_run.id, 'triggered_by': 'merge_request'})


def _find_or_create_project(repo_name):
    project = Project.query.filter_by(name=repo_name.split('/')[-1] if '/' in repo_name else repo_name, owner_id=1).first()
    if project:
        return project
    project = Project(name=repo_name.split('/')[-1] if '/' in repo_name else repo_name, description=f'Auto-created from GitLab: {repo_name}', owner_id=1)
    db.session.add(project)
    db.session.commit()
    return project


def _schedule_test_execution(test_run, trigger_result):
    try:
        from ...tasks import run_api_collection_task
        test_type = trigger_result.get('test_type', 'api')
        target_id = trigger_result.get('target_id')
        if test_type == 'api' and target_id:
            task = run_api_collection_task.delay(collection_id=target_id, environment_id=None, test_run_id=test_run.id)
            test_run.celery_task_id = task.id
            db.session.commit()
            logger.info('Scheduled API test', test_run_id=test_run.id, task_id=task.id)
    except Exception as exc:
        logger.error('Failed to schedule test', error=str(exc))
