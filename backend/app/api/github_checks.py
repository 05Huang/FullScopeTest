"""
GitHub Check Run API 路由

提供 Check Run 创建、更新、完成等接口
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..models.test_run import TestRun
from ..models.project import Project
from ..models.github_integration import GitHubIntegration
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..extensions import db
from ..core.logging import get_logger
from ..services.github_check_service import create_check_service

logger = get_logger(__name__)


def _get_test_run_owned_by_user(test_run_id, user_id):
    """获取 TestRun 并验证项目所有者"""
    test_run = TestRun.query.filter_by(id=test_run_id).first()
    if not test_run:
        return None, error_response(404, '测试运行记录不存在')
    project = Project.query.get(test_run.project_id)
    if not project or project.owner_id != user_id:
        logger.warning('IDOR attempt blocked on github_checks',
                       user_id=user_id, test_run_id=test_run_id)
        return None, error_response(404, '测试运行记录不存在')
    return test_run, None


@api_bp.route('/github-checks/<int:test_run_id>/create', methods=['POST'])
@jwt_required()
def create_check_run(test_run_id):
    """
    为测试运行创建 GitHub Check Run

    请求体:
        repo_full_name: 仓库全名 (owner/repo)
        head_sha: 提交 SHA
    """
    user_id = get_current_user_id()
    data = request.get_json() or {}

    repo_full_name = data.get('repo_full_name')
    head_sha = data.get('head_sha')

    if not repo_full_name or not head_sha:
        return error_response(400, '缺少 repo_full_name 或 head_sha 参数')

    # 获取测试运行记录（验证所有权）
    test_run, err = _get_test_run_owned_by_user(test_run_id, user_id)
    if err:
        return err

    # 获取 GitHub 集成信息
    integration = GitHubIntegration.query.filter_by(
        user_id=user_id,
        is_active=True,
    ).first()
    if not integration:
        return error_response(404, '未找到 GitHub 集成信息')

    # 创建 Check Run
    service = create_check_service(integration)
    result = service.start_test_check_run(test_run, repo_full_name, head_sha)

    if not result:
        return error_response(500, '创建 Check Run 失败')

    # 更新测试运行记录
    test_run.check_run_id = result.get('id')
    test_run.check_run_repo = repo_full_name
    db.session.commit()

    return success_response(data=result, message='Check Run 创建成功')


@api_bp.route('/github-checks/<int:test_run_id>/update', methods=['POST'])
@jwt_required()
def update_check_run(test_run_id):
    """
    更新 Check Run 进度

    请求体:
        current_step: 当前步骤描述
    """
    user_id = get_current_user_id()
    data = request.get_json() or {}

    test_run, err = _get_test_run_owned_by_user(test_run_id, user_id)
    if err:
        return err

    if not test_run.check_run_id or not test_run.check_run_repo:
        return error_response(400, '此测试运行没有关联的 Check Run')

    integration = GitHubIntegration.query.filter_by(
        user_id=user_id,
        is_active=True,
    ).first()
    if not integration:
        return error_response(404, '未找到 GitHub 集成信息')

    service = create_check_service(integration)
    result = service.update_test_progress(
        test_run.check_run_repo,
        test_run.check_run_id,
        test_run,
        current_step=data.get('current_step'),
    )

    if not result:
        return error_response(500, '更新 Check Run 失败')

    return success_response(data=result, message='Check Run 更新成功')


@api_bp.route('/github-checks/<int:test_run_id>/complete', methods=['POST'])
@jwt_required()
def complete_check_run(test_run_id):
    """
    完成 Check Run

    请求体:
        report_url: 报告链接（可选）
    """
    user_id = get_current_user_id()
    data = request.get_json() or {}

    test_run, err = _get_test_run_owned_by_user(test_run_id, user_id)
    if err:
        return err

    if not test_run.check_run_id or not test_run.check_run_repo:
        return error_response(400, '此测试运行没有关联的 Check Run')

    integration = GitHubIntegration.query.filter_by(
        user_id=user_id,
        is_active=True,
    ).first()
    if not integration:
        return error_response(404, '未找到 GitHub 集成信息')

    service = create_check_service(integration)
    result = service.complete_test_check_run(
        test_run.check_run_repo,
        test_run.check_run_id,
        test_run,
        report_url=data.get('report_url'),
    )

    if not result:
        return error_response(500, '完成 Check Run 失败')

    return success_response(data=result, message='Check Run 已完成')
