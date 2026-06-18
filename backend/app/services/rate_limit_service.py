"""
Redis 滑动窗口限流服务

支持：
- 基于 Redis 的滑动窗口算法
- 按用户类型配置不同限额（普通用户 100/min, API token 1000/min）
- 按组织配置限额
- Prometheus 指标记录
"""

import time
import os
from typing import Optional, Dict, Any
import redis

from ..core.logging import get_logger

logger = get_logger(__name__)

# 默认限流规则
DEFAULT_RATE_LIMITS = {
    'user': 100,        # 普通用户 100 req/min
    'api_token': 1000,  # API token 1000 req/min
}

# Redis 连接
_redis = None


def _get_redis():
    """获取 Redis 连接（惰性初始化）"""
    global _redis
    if _redis is None:
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        _redis = redis.from_url(redis_url, decode_responses=True, socket_timeout=2, socket_connect_timeout=2)
    # 验证连接有效，失效则重建
    try:
        _redis.ping()
    except Exception:
        _redis = None
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        _redis = redis.from_url(redis_url, decode_responses=True, socket_timeout=2, socket_connect_timeout=2)
    return _redis


def sliding_window_rate_limit(
    key: str,
    limit: int,
    window: int = 60,
    redis_client=None,
) -> bool:
    """
    滑动窗口限流算法

    Args:
        key: 限流键（如 user_id 或 org_id:ip）
        limit: 时间窗口内的最大请求数
        window: 时间窗口大小（秒）
        redis_client: Redis 连接

    Returns:
        bool: True 表示允许，False 表示被限流
    """
    if redis_client is None:
        try:
            redis_client = _get_redis()
        except Exception as exc:
            logger.warning('Redis unavailable for rate limiting, allowing request', error=str(exc))
            return True

    now = time.time()
    window_start = now - window

    try:
        # 使用 Redis sorted set 实现滑动窗口
        pipe = redis_client.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window)
        results = pipe.execute()

        current_count = results[2]
        return current_count <= limit
    except Exception as exc:
        logger.warning('Redis rate limit check failed, allowing request', error=str(exc))
        return True


def get_rate_limit_headers(key: str, limit: int, window: int = 60, redis_client=None) -> Dict[str, str]:
    """获取限流响应头"""
    if redis_client is None:
        try:
            redis_client = _get_redis()
        except Exception:
            redis_client = None

    now = time.time()

    if redis_client:
        try:
            window_start = now - window
            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zcard(key)
            results = pipe.execute()
            remaining = max(0, limit - results[1])
        except Exception:
            remaining = 0
    else:
        remaining = 0

    reset_time = int(now + window)

    return {
        'X-RateLimit-Limit': str(limit),
        'X-RateLimit-Remaining': str(remaining),
        'X-RateLimit-Reset': str(reset_time),
        'Retry-After': str(window),
    }


def get_user_rate_limit(user_id: int, is_api_token: bool = False, org_id: int = None) -> int:
    """
    获取用户限流配置

    优先使用组织自定义限额，回退到全局默认值。
    组织限额缓存到 Redis（TTL 5 分钟），避免每次请求查数据库。
    """
    base_limit = DEFAULT_RATE_LIMITS['api_token' if is_api_token else 'user']

    if org_id is None:
        # 尝试通过用户获取组织 ID
        try:
            from ..models.organization import OrganizationMember
            membership = OrganizationMember.query.filter_by(user_id=user_id).first()
            if membership:
                org_id = membership.organization_id
        except Exception:
            pass

    if org_id is not None:
        org_limit = get_org_rate_limit(org_id)
        if org_limit is not None:
            return org_limit

    return base_limit


def get_org_rate_limit(org_id: int) -> Optional[int]:
    """
    获取组织自定义限流配置

    从 Quota 模型查询 api_rate_limit 资源类型的配额。
    缓存到 Redis（TTL 5 分钟），避免每次请求查数据库。
    返回 None 表示使用全局默认值。
    """
    cache_key = f"rate_limit:org:{org_id}"

    # 尝试从 Redis 缓存读取
    try:
        r = _get_redis()
        cached = r.get(cache_key)
        if cached is not None:
            if cached == 'null':
                return None
            return int(cached)
    except Exception:
        pass

    # 从数据库查询
    try:
        from ..models.quota import Quota
        quota = Quota.query.filter_by(
            organization_id=org_id,
            resource_type='api_rate_limit'
        ).first()

        result = quota.limit if quota and quota.limit > 0 else None

        # 缓存到 Redis（TTL 5 分钟）
        try:
            r = _get_redis()
            r.setex(cache_key, 300, str(result) if result is not None else 'null')
        except Exception:
            pass

        return result
    except Exception as exc:
        logger.warning('获取组织限流配置失败', org_id=org_id, error=str(exc))
        return None


def reset_rate_limit(key: str, redis_client=None) -> bool:
    """重置指定键的限流计数"""
    if redis_client is None:
        redis_client = _get_redis()

    try:
        redis_client.delete(key)
        return True
    except Exception as exc:
        logger.error('Failed to reset rate limit', key=key, error=str(exc))
        return False
