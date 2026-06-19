"""
密码策略与登录锁定服务

功能：
- 密码复杂度校验
- 登录失败计数与账户锁定
- 登录失败审计日志

锁定策略：
- 连续 5 次登录失败后锁定账户 15 分钟
- 锁定状态返回 HTTP 423 (Locked) 和剩余时间
- 成功登录后重置失败计数
"""
import os
import time
from datetime import datetime, timezone, timedelta
from ..core.logging import get_logger

logger = get_logger(__name__)

# ── 配置 ──────────────────────────────────────────────────────────────────────

# 最大失败次数
MAX_LOGIN_FAILURES = int(os.environ.get('MAX_LOGIN_FAILURES', '5'))

# 锁定时间（秒）
LOCKOUT_DURATION = int(os.environ.get('LOCKOUT_DURATION_SECONDS', str(15 * 60)))

# ── 内存存储（开发/测试环境）──────────────────────────────────────────────────
# 生产环境应使用 Redis，格式：{user_id: {"failures": int, "locked_until": float}}

_login_failure_store: dict = {}

# Redis 连接缓存（模块级单例，避免每次调用创建新连接）
_redis_client = None


def _get_store_key(user_id: int) -> str:
    """获取存储键"""
    return f"login_failures:{user_id}"


def _get_redis():
    """获取 Redis 连接（带缓存，失败时自动重建）"""
    global _redis_client
    if _redis_client is not None:
        try:
            _redis_client.ping()
            return _redis_client
        except Exception:
            _redis_client = None

    try:
        import redis as redis_lib
        redis_url = os.environ.get('REDIS_URL')
        if redis_url:
            _redis_client = redis_lib.from_url(redis_url, decode_responses=True)
            _redis_client.ping()
            return _redis_client
    except Exception:
        _redis_client = None
    return None


# ── 失败计数 ──────────────────────────────────────────────────────────────────

def record_login_failure(user_id: int, ip_address: str = None, username: str = None):
    """
    记录一次登录失败

    Args:
        user_id: 用户 ID
        ip_address: 客户端 IP
        username: 尝试登录的用户名（用于审计）
    """
    r = _get_redis()
    key = _get_store_key(user_id)

    if r:
        try:
            pipe = r.pipeline()
            pipe.hincrby(key, 'failures', 1)
            pipe.hset(key, 'last_attempt', datetime.now(timezone.utc).replace(tzinfo=None).isoformat())
            pipe.expire(key, LOCKOUT_DURATION * 2)
            result = pipe.execute()
            failures = int(result[0])
        except Exception as e:
            logger.error("Redis 记录登录失败出错", error=str(e))
            failures = _record_failure_memory(user_id)
    else:
        failures = _record_failure_memory(user_id)

    logger.warning("登录失败",
                   user_id=user_id,
                   username=username,
                   ip=ip_address,
                   failures=failures,
                   max_failures=MAX_LOGIN_FAILURES)


def _record_failure_memory(user_id: int) -> int:
    """内存方式记录失败"""
    key = _get_store_key(user_id)
    now = time.time()
    entry = _login_failure_store.get(key, {'failures': 0, 'locked_until': 0})

    # 如果已锁定且锁定时间已过，重置
    if entry.get('locked_until', 0) and now > entry['locked_until']:
        entry = {'failures': 0, 'locked_until': 0}

    entry['failures'] = entry.get('failures', 0) + 1
    entry['last_attempt'] = now

    # 达到阈值时设置锁定
    if entry['failures'] >= MAX_LOGIN_FAILURES:
        entry['locked_until'] = now + LOCKOUT_DURATION

    _login_failure_store[key] = entry
    return entry['failures']


def get_login_failures(user_id: int) -> int:
    """获取当前连续失败次数"""
    r = _get_redis()
    key = _get_store_key(user_id)

    if r:
        try:
            failures = r.hget(key, 'failures')
            return int(failures) if failures else 0
        except Exception:
            pass

    entry = _login_failure_store.get(key, {'failures': 0})
    now = time.time()
    if entry.get('locked_until', 0) and now > entry['locked_until']:
        return 0
    return entry.get('failures', 0)


def is_account_locked(user_id: int) -> tuple:
    """
    检查账户是否被锁定

    Returns:
        (is_locked: bool, remaining_seconds: int)
    """
    r = _get_redis()
    key = _get_store_key(user_id)

    if r:
        try:
            failures = r.hget(key, 'failures')
            if not failures or int(failures) < MAX_LOGIN_FAILURES:
                return False, 0
            # 使用 TTL 判断剩余锁定时间
            ttl = r.ttl(key)
            if ttl > 0:
                return True, ttl
            return False, 0
        except Exception:
            pass

    entry = _login_failure_store.get(key, {'failures': 0, 'locked_until': 0})
    now = time.time()
    locked_until = entry.get('locked_until', 0)

    if locked_until and now < locked_until:
        remaining = int(locked_until - now)
        return True, remaining

    return False, 0


def reset_login_failures(user_id: int):
    """
    重置登录失败计数（成功登录后调用）
    """
    r = _get_redis()
    key = _get_store_key(user_id)

    if r:
        try:
            r.delete(key)
        except Exception:
            pass

    _login_failure_store.pop(key, None)

    logger.info("登录失败计数已重置", user_id=user_id)
