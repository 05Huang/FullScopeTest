"""
GitHub 集成 API

提供 GitHub App OAuth 授权、回调、绑定管理等接口
"""

from flask import request, redirect, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import api_bp
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/integrations/github/auth', methods=['GET'])
@jwt_required()
def github_auth():
    """
    获取 GitHub OAuth 授权 URL

    用户点击此接口后，会重定向到 GitHub 授权页面。
    授权完成后，GitHub 会回调 /api/v1/integrations/github/callback
    """
    try:
        user_id = get_current_user_id()

        # 生成回调 URL
        base_url = request.host_url.rstrip('/')
        redirect_uri = f'{base_url}/api/v1/integrations/github/callback'

        # 生成授权 URL
        from ..services.github_oauth_service import generate_authorize_url
        authorize_url, state = generate_authorize_url(redirect_uri)

        # 将 state 存储到 session 用于 CSRF 验证
        from flask import session
        session['github_oauth_state'] = state
        session['github_oauth_user_id'] = user_id

        logger.info('GitHub OAuth initiated', user_id=user_id)

        return success_response(data={
            'authorize_url': authorize_url,
            'state': state,
        })

    except Exception as exc:
        logger.error('GitHub OAuth init failed', error=str(exc))
        return error_response(500, f'GitHub OAuth 初始化失败: {str(exc)}')


@api_bp.route('/integrations/github/callback', methods=['GET'])
def github_callback():
    """
    GitHub OAuth 回调接口

    GitHub 授权完成后会重定向到此接口，携带 code 和 state 参数。
    此接口交换 code 为 token，获取用户信息，创建或更新绑定记录。
    """
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    # 检查是否有错误
    if error:
        error_description = request.args.get('error_description', '')
        logger.warning('GitHub OAuth callback error', error=error, description=error_description)
        # 重定向到前端错误页面
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url}/settings?github_error={error}')

    # 验证参数
    if not code or not state:
        logger.warning('GitHub OAuth callback missing parameters')
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url}/settings?github_error=missing_params')

    # 验证 state（CSRF 防护）
    from flask import session
    stored_state = session.get('github_oauth_state')
    user_id = session.get('github_oauth_user_id')

    if not stored_state or stored_state != state:
        logger.warning('GitHub OAuth state mismatch')
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url}/settings?github_error=invalid_state')

    if not user_id:
        logger.warning('GitHub OAuth missing user_id in session')
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url}/settings?github_error=not_logged_in')

    try:
        # 交换 code 为 token
        from ..services.github_oauth_service import (
            exchange_code_for_token,
            get_github_user_info,
            create_or_update_integration,
        )

        token_data = exchange_code_for_token(code)
        github_user_data = get_github_user_info(token_data['access_token'])

        # 创建或更新集成记录
        integration = create_or_update_integration(
            user_id=user_id,
            github_user_data=github_user_data,
            token_data=token_data,
        )

        # 清理 session
        session.pop('github_oauth_state', None)
        session.pop('github_oauth_user_id', None)

        logger.info(
            'GitHub OAuth completed successfully',
            user_id=user_id,
            github_username=integration.github_username,
        )

        # 重定向到前端成功页面
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url}/settings?github_success=true')

    except Exception as exc:
        logger.error('GitHub OAuth callback failed', error=str(exc), user_id=user_id)
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url}/settings?github_error=callback_failed')


@api_bp.route('/integrations/github/status', methods=['GET'])
@jwt_required()
def github_status():
    """获取当前用户的 GitHub 绑定状态"""
    try:
        user_id = get_current_user_id()

        from ..services.github_oauth_service import get_integration_by_user
        integration = get_integration_by_user(user_id)

        if not integration:
            return success_response(data={
                'connected': False,
                'integration': None,
            })

        return success_response(data={
            'connected': True,
            'integration': integration.to_dict(),
        })

    except Exception as exc:
        logger.error('Get GitHub status failed', error=str(exc))
        return error_response(500, f'获取 GitHub 状态失败: {str(exc)}')


@api_bp.route('/integrations/github/unbind', methods=['POST'])
@jwt_required()
def github_unbind():
    """解绑 GitHub 账号"""
    try:
        user_id = get_current_user_id()

        from ..services.github_oauth_service import get_integration_by_user, revoke_integration
        integration = get_integration_by_user(user_id)

        if not integration:
            return error_response(404, '未找到 GitHub 绑定信息')

        success = revoke_integration(integration.id, user_id)
        if not success:
            return error_response(500, '解绑失败')

        logger.info('GitHub unbind successful', user_id=user_id)
        return success_response(message='GitHub 账号已解绑')

    except Exception as exc:
        logger.error('GitHub unbind failed', error=str(exc))
        return error_response(500, f'解绑失败: {str(exc)}')


@api_bp.route('/integrations/github/config', methods=['GET'])
def github_config():
    """获取 GitHub OAuth 配置（公开接口，无需认证）"""
    try:
        from ..services.github_oauth_service import get_github_oauth_config
        config = get_github_oauth_config()

        return success_response(data=config)

    except Exception as exc:
        logger.error('Get GitHub config failed', error=str(exc))
        return error_response(500, f'获取配置失败: {str(exc)}')
