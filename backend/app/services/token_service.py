"""
API Token 服务

提供 Token 的校验、权限检查和项目范围验证。
供中间件和 API 层使用。

Token 权限格式（新）：
    {"actions": ["read", "execute"], "project_ids": [1, 2]}

旧格式兼容：
    ['read-only'] → actions: ['read']
    ['read-write'] → actions: ['read', 'write', 'execute']
"""
import hashlib
from datetime import datetime, timezone
from typing import Optional
from ..extensions import db
from ..models.api_token import ApiToken, VALID_TOKEN_ACTIONS
from ..core.logging import get_logger

logger = get_logger(__name__)


def hash_token(token: str) -> str:
    """生成 token 的 SHA-256 哈希值"""
    return hashlib.sha256(token.encode()).hexdigest()


def validate_token(token: str) -> Optional[ApiToken]:
    """
    验证 API Token 并返回对应的 ApiToken 对象

    校验逻辑：
    1. 哈希匹配
    2. Token 激活状态
    3. 未过期

    Args:
        token: 原始 Token 字符串

    Returns:
        ApiToken 对象，None 表示验证失败
    """
    token_hash = hash_token(token)
    api_token = ApiToken.query.filter_by(token_hash=token_hash).first()

    if not api_token:
        return None

    if not api_token.is_active:
        logger.warning("Token 已禁用", token_id=api_token.id)
        return None

    if api_token.expires_at and api_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        logger.warning("Token 已过期", token_id=api_token.id, expires_at=api_token.expires_at)
        return None

    # 更新最后使用时间
    api_token.last_used_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.session.commit()

    return api_token


def check_token_permission(api_token: ApiToken, action: str, project_id: int = None) -> bool:
    """
    检查 Token 是否有权执行指定操作

    Args:
        api_token: ApiToken 对象
        action: 操作类型（read/write/execute/delete）
        project_id: 项目 ID（可选，为 None 时仅检查操作权限）

    Returns:
        True 表示有权限
    """
    # 检查操作权限
    if not api_token.has_action(action):
        logger.warning("Token 操作权限不足",
                       token_id=api_token.id, action=action,
                       allowed=api_token.get_actions())
        return False

    # 检查项目范围
    if project_id is not None and not api_token.can_access_project(project_id):
        logger.warning("Token 项目权限不足",
                       token_id=api_token.id, project_id=project_id,
                       allowed_projects=api_token.project_ids)
        return False

    return True


def create_token(
    user_id: int,
    name: str,
    actions: list = None,
    project_ids: list = None,
    expires_in_days: int = None,
) -> tuple:
    """
    创建 API Token

    Args:
        user_id: 用户 ID
        name: Token 名称
        actions: 允许的操作列表（默认 ['read']）
        project_ids: 项目 ID 白名单（默认 [] 表示不限制）
        expires_in_days: 有效期天数（默认不过期）

    Returns:
        (ApiToken 对象, 原始 Token 字符串)
    """
    import secrets

    if actions is None:
        actions = ['read']

    # 校验操作类型
    invalid_actions = set(actions) - VALID_TOKEN_ACTIONS
    if invalid_actions:
        raise ValueError(f"无效的操作类型: {invalid_actions}，合法值: {VALID_TOKEN_ACTIONS}")

    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)

    expires_at = None
    if expires_in_days:
        from datetime import timedelta
        expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=expires_in_days)

    api_token = ApiToken(
        user_id=user_id,
        name=name,
        token_hash=token_hash,
        permissions={'actions': actions, 'project_ids': project_ids or []},
        project_ids=project_ids or [],
        expires_at=expires_at,
    )

    db.session.add(api_token)
    db.session.commit()

    logger.info("API Token 已创建",
                token_id=api_token.id, user_id=user_id,
                actions=actions, project_ids=project_ids)

    return api_token, token
