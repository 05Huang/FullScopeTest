"""
GitHub OAuth 服务

处理 GitHub App OAuth 流程：授权 URL 生成、Token 交换、用户信息获取
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

from ..extensions import db
from ..models.github_integration import GitHubIntegration
from ..models.user import User
from ..core.logging import get_logger

logger = get_logger(__name__)

# GitHub OAuth 配置
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
GITHUB_OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_OAUTH_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_USER_URL = 'https://api.github.com/user'
GITHUB_API_USER_EMAILS_URL = 'https://api.github.com/user/emails'

# Token 加密密钥（从环境变量读取，默认使用 Flask SECRET_KEY）
TOKEN_ENCRYPTION_KEY = os.environ.get('GITHUB_TOKEN_ENCRYPTION_KEY', '')


def get_github_oauth_config() -> Dict[str, Any]:
    """获取 GitHub OAuth 配置"""
    return {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'authorize_url': GITHUB_OAUTH_AUTHORIZE_URL,
        'token_url': GITHUB_OAUTH_TOKEN_URL,
        'is_configured': bool(GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET),
    }


def generate_authorize_url(redirect_uri: str, state: Optional[str] = None) -> Tuple[str, str]:
    """
    生成 GitHub OAuth 授权 URL

    Args:
        redirect_uri: OAuth 回调地址
        state: 可选的 state 参数（用于 CSRF 防护）

    Returns:
        (authorize_url, state)
    """
    if not state:
        state = secrets.token_urlsafe(32)

    params = {
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scope': 'read:user user:email read:org',
        'state': state,
        'allow_signup': 'true',
    }

    query_string = '&'.join(f'{k}={v}' for k, v in params.items())
    authorize_url = f'{GITHUB_OAUTH_AUTHORIZE_URL}?{query_string}'

    return authorize_url, state


def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """
    用授权码换取 Access Token

    Args:
        code: OAuth 授权码

    Returns:
        dict: {access_token: ..., token_type: ..., scope: ..., expires_in: ...}

    Raises:
        ValueError: 交换失败
    """
    import requests

    resp = requests.post(
        GITHUB_OAUTH_TOKEN_URL,
        json={
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code,
        },
        headers={'Accept': 'application/json'},
        timeout=10,
    )

    if resp.status_code != 200:
        raise ValueError(f'GitHub token exchange failed: HTTP {resp.status_code}')

    data = resp.json()

    if 'error' in data:
        raise ValueError(f'GitHub OAuth error: {data["error"]} - {data.get("error_description", "")}')

    return data


def get_github_user_info(access_token: str) -> Dict[str, Any]:
    """
    获取 GitHub 用户信息

    Args:
        access_token: GitHub Access Token

    Returns:
        dict: {id: ..., login: ..., email: ..., avatar_url: ...}
    """
    import requests

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }

    # 获取用户基本信息
    user_resp = requests.get(GITHUB_API_USER_URL, headers=headers, timeout=10)
    if user_resp.status_code != 200:
        raise ValueError(f'Failed to fetch GitHub user: HTTP {user_resp.status_code}')

    user_data = user_resp.json()

    # 获取用户邮箱
    email = user_data.get('email')
    if not email:
        emails_resp = requests.get(GITHUB_API_USER_EMAILS_URL, headers=headers, timeout=10)
        if emails_resp.status_code == 200:
            emails = emails_resp.json()
            # 优先使用 primary 邮箱
            for e in emails:
                if e.get('primary') and e.get('verified'):
                    email = e['email']
                    break
            # 如果没有 primary，使用第一个 verified 的
            if not email:
                for e in emails:
                    if e.get('verified'):
                        email = e['email']
                        break

    return {
        'id': str(user_data.get('id', '')),
        'login': user_data.get('login', ''),
        'email': email or '',
        'avatar_url': user_data.get('avatar_url', ''),
        'name': user_data.get('name', ''),
        'html_url': user_data.get('html_url', ''),
    }


def encrypt_token(token: str) -> str:
    """
    加密 Token（使用简单的 XOR 加密 + base64 编码）

    生产环境建议使用 Fernet 加密（cryptography 库）
    """
    import base64

    key = TOKEN_ENCRYPTION_KEY or 'default-dev-key-change-in-production'
    # 确保 key 足够长
    key_bytes = key.encode('utf-8')

    token_bytes = token.encode('utf-8')
    encrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(token_bytes))
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_token(encrypted_token: str) -> str:
    """
    解密 Token
    """
    import base64

    key = TOKEN_ENCRYPTION_KEY or 'default-dev-key-change-in-production'
    key_bytes = key.encode('utf-8')

    encrypted_bytes = base64.b64decode(encrypted_token)
    decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(encrypted_bytes))
    return decrypted.decode('utf-8')


def create_or_update_integration(
    user_id: int,
    github_user_data: Dict[str, Any],
    token_data: Dict[str, Any],
) -> GitHubIntegration:
    """
    创建或更新 GitHub 集成记录

    Args:
        user_id: 本地用户 ID
        github_user_data: GitHub 用户信息
        token_data: Token 数据

    Returns:
        GitHubIntegration 实例
    """
    github_user_id = github_user_data['id']

    # 查找现有集成
    integration = GitHubIntegration.query.filter_by(
        user_id=user_id,
        github_user_id=github_user_id,
    ).first()

    # 计算 token 过期时间
    token_expires_at = None
    expires_in = token_data.get('expires_in')
    if expires_in:
        token_expires_at = datetime.utcnow() + timedelta(seconds=int(expires_in))

    encrypted_access_token = encrypt_token(token_data['access_token'])

    if integration:
        # 更新现有集成
        integration.access_token_encrypted = encrypted_access_token
        integration.token_type = token_data.get('token_type', 'bearer')
        integration.scope = token_data.get('scope', '')
        integration.token_expires_at = token_expires_at
        integration.github_username = github_user_data['login']
        integration.github_email = github_user_data.get('email', '')
        integration.github_avatar = github_user_data.get('avatar_url', '')
        integration.is_active = True
        integration.last_used_at = datetime.utcnow()

        # 处理 refresh token
        refresh_token = token_data.get('refresh_token')
        if refresh_token:
            integration.refresh_token_encrypted = encrypt_token(refresh_token)
            refresh_expires_in = token_data.get('refresh_token_expires_in')
            if refresh_expires_in:
                integration.refresh_token_expires_at = datetime.utcnow() + timedelta(seconds=int(refresh_expires_in))

        logger.info('GitHub integration updated', user_id=user_id, github_username=integration.github_username)
    else:
        # 创建新集成
        refresh_token_encrypted = None
        refresh_token_expires_at = None
        refresh_token = token_data.get('refresh_token')
        if refresh_token:
            refresh_token_encrypted = encrypt_token(refresh_token)
            refresh_expires_in = token_data.get('refresh_token_expires_in')
            if refresh_expires_in:
                refresh_token_expires_at = datetime.utcnow() + timedelta(seconds=int(refresh_expires_in))

        integration = GitHubIntegration(
            user_id=user_id,
            github_user_id=github_user_id,
            github_username=github_user_data['login'],
            github_email=github_user_data.get('email', ''),
            github_avatar=github_user_data.get('avatar_url', ''),
            access_token_encrypted=encrypted_access_token,
            token_type=token_data.get('token_type', 'bearer'),
            scope=token_data.get('scope', ''),
            token_expires_at=token_expires_at,
            refresh_token_encrypted=refresh_token_encrypted,
            refresh_token_expires_at=refresh_token_expires_at,
            is_active=True,
            last_used_at=datetime.utcnow(),
        )
        db.session.add(integration)
        logger.info('GitHub integration created', user_id=user_id, github_username=integration.github_username)

    db.session.commit()
    return integration


def get_integration_by_user(user_id: int) -> Optional[GitHubIntegration]:
    """获取用户的 GitHub 集成信息"""
    return GitHubIntegration.query.filter_by(user_id=user_id, is_active=True).first()


def get_access_token(integration: GitHubIntegration) -> Optional[str]:
    """获取解密后的 Access Token"""
    if not integration or not integration.access_token_encrypted:
        return None
    try:
        return decrypt_token(integration.access_token_encrypted)
    except Exception as exc:
        logger.error('Failed to decrypt GitHub token', error=str(exc))
        return None


def revoke_integration(integration_id: int, user_id: int) -> bool:
    """
    撤销 GitHub 集成（软删除）

    Args:
        integration_id: 集成记录 ID
        user_id: 用户 ID（安全验证）

    Returns:
        是否成功
    """
    integration = GitHubIntegration.query.filter_by(
        id=integration_id,
        user_id=user_id,
    ).first()

    if not integration:
        return False

    integration.is_active = False
    db.session.commit()

    logger.info('GitHub integration revoked', user_id=user_id, github_username=integration.github_username)
    return True
