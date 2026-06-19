"""
Token 黑名单服务

使用 Redis 存储已注销的 JWT Token，支持：
- 登出时注销当前 Token
- 修改密码后注销所有 Token
- Token 过期后自动清理
"""

import redis
from datetime import datetime, timezone, timedelta
from ..core.logging import get_logger

logger = get_logger(__name__)

# Redis 连接（延迟初始化）
_redis_client = None


def _get_redis():
    """获取 Redis 连接"""
    global _redis_client
    if _redis_client is None:
        import os
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        try:
            _redis_client = redis.from_url(redis_url, decode_responses=True)
            _redis_client.ping()
        except Exception as e:
            logger.warning('Redis not available for token blacklist', error=str(e))
            return None
    return _redis_client


def blacklist_token(jti: str, expires_at: datetime) -> bool:
    """
    将 Token 加入黑名单

    Args:
        jti: Token 的 JWT ID
        expires_at: Token 过期时间

    Returns:
        bool: 是否成功
    """
    r = _get_redis()
    if not r:
        logger.warning('Cannot blacklist token: Redis unavailable', jti=jti)
        return False

    try:
        # 计算剩余存活时间
        ttl = expires_at - datetime.now(timezone.utc).replace(tzinfo=None)
        if ttl.total_seconds() <= 0:
            return False  # Token 已过期，无需黑名单

        key = f'token_blacklist:{jti}'
        r.setex(key, int(ttl.total_seconds()), '1')
        logger.info('Token blacklisted', jti=jti, ttl_seconds=int(ttl.total_seconds()))
        return True
    except Exception as e:
        logger.error('Failed to blacklist token', jti=jti, error=str(e))
        return False


def is_token_blacklisted(jti: str) -> bool:
    """
    检查 Token 是否在黑名单中

    Args:
        jti: Token 的 JWT ID

    Returns:
        bool: 是否已黑名单
    """
    r = _get_redis()
    if not r:
        return False  # Redis 不可用时放行（降级策略）

    try:
        key = f'token_blacklist:{jti}'
        return r.exists(key) > 0
    except Exception as e:
        logger.error('Failed to check token blacklist', jti=jti, error=str(e))
        return False


def blacklist_all_user_tokens(user_id: int) -> bool:
    """
    注销用户的所有 Token（用于修改密码等场景）

    通过递增 token_version 计数器实现：
    - JWT 中嵌入 token_version claim
    - 验证时比对 JWT 中的 version 与 Redis 存储的 version
    - version 不匹配则拒绝 Token
    """
    r = _get_redis()
    if not r:
        logger.warning('Cannot blacklist all tokens: Redis unavailable', user_id=user_id)
        return False

    try:
        key = f'user:{user_id}:token_version'
        new_version = r.incr(key)
        # 设置过期时间 30 天，避免无限增长
        r.expire(key, 30 * 24 * 3600)
        logger.info('All user tokens blacklisted via version increment', user_id=user_id, new_version=new_version)
        return True
    except Exception as e:
        logger.error('Failed to blacklist all user tokens', user_id=user_id, error=str(e))
        return False


def get_user_token_version(user_id: int) -> int:
    """
    获取用户当前 token 版本号

    新 Token 创建时嵌入此版本号，验证时比对。
    """
    r = _get_redis()
    if not r:
        return 0  # Redis 不可用时默认版本 0

    try:
        key = f'user:{user_id}:token_version'
        version = r.get(key)
        return int(version) if version else 0
    except Exception:
        return 0


def is_token_version_valid(user_id: int, token_version: int) -> bool:
    """
    校验 Token 的版本号是否有效

    Token 中的 version 小于当前版本则已失效。
    """
    current_version = get_user_token_version(user_id)
    return token_version >= current_version
