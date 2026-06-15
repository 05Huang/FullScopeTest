"""
多级缓存服务

高频读取接口（项目列表、环境列表、Dashboard 统计）的缓存抽象层。

- 生产环境：Redis（通过 REDIS_URL 配置）
- 开发/测试环境：内存 dict + TTL（复用 SessionStore 模式）
- 通过 CACHE_ENABLED 环境变量控制开关（默认 true）

用法：
    cache = get_cache_service()
    if cache:
        data = cache.get("projects:user:1")
        if data is None:
            data = fetch_from_db()
            cache.set("projects:user:1", data, ttl=300)
"""

import json
import os
import time
import threading
from typing import Any, Optional

from ..core.logging import get_logger

logger = get_logger(__name__)


class CacheService:
    """缓存服务接口"""

    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError

    def invalidate_pattern(self, pattern: str) -> int:
        """按模式批量失效缓存，返回删除数量"""
        raise NotImplementedError

    @property
    def backend(self) -> str:
        raise NotImplementedError


class RedisCacheService(CacheService):
    """基于 Redis 的缓存实现"""

    def __init__(self, redis_url: str):
        import redis as redis_lib
        self._redis = redis_lib.from_url(
            redis_url,
            decode_responses=True,
            socket_timeout=2,
            socket_connect_timeout=2,
        )
        try:
            self._redis.ping()
        except Exception as exc:
            logger.error("Redis CacheService 连接失败", error=str(exc))
            raise

    def get(self, key: str) -> Optional[Any]:
        raw = self._redis.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        data = json.dumps(value, ensure_ascii=False, default=str)
        if ttl > 0:
            self._redis.setex(key, ttl, data)
        else:
            self._redis.set(key, data)

    def delete(self, key: str) -> None:
        self._redis.delete(key)

    def invalidate_pattern(self, pattern: str) -> int:
        """使用 SCAN 按模式删除键（避免阻塞 Redis）"""
        count = 0
        for key in self._redis.scan_iter(match=pattern, count=100):
            self._redis.delete(key)
            count += 1
        return count

    @property
    def backend(self) -> str:
        return "redis"


class MemoryCacheService(CacheService):
    """基于内存 dict 的缓存实现（开发/测试环境）"""

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, exp = entry
            if time.time() >= exp:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        exp = time.time() + ttl if ttl > 0 else float('inf')
        with self._lock:
            self._store[key] = (value, exp)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def invalidate_pattern(self, pattern: str) -> int:
        prefix = pattern.rstrip("*")
        with self._lock:
            keys_to_delete = [k for k in self._store if k.startswith(prefix)]
            for key in keys_to_delete:
                del self._store[key]
            return len(keys_to_delete)

    @property
    def backend(self) -> str:
        return "memory"


# ==================== 工厂函数 ====================

_cache_instance: Optional[CacheService] = None
_cache_lock = threading.Lock()


def get_cache_service() -> Optional[CacheService]:
    """
    获取全局缓存服务实例

    返回 None 表示缓存禁用（CACHE_ENABLED=false）。
    """
    enabled = os.environ.get("CACHE_ENABLED", "true").strip().lower() == "true"
    if not enabled:
        return None

    global _cache_instance
    if _cache_instance is not None:
        return _cache_instance

    with _cache_lock:
        if _cache_instance is not None:
            return _cache_instance

        redis_url = os.environ.get("REDIS_URL", "").strip()
        if redis_url:
            try:
                _cache_instance = RedisCacheService(redis_url)
                logger.info("CacheService 使用 Redis 后端")
                return _cache_instance
            except Exception as exc:
                logger.warning("Redis CacheService 初始化失败，回退到内存", error=str(exc))

        _cache_instance = MemoryCacheService()
        logger.info("CacheService 使用内存后端")
        return _cache_instance


def reset_cache_service():
    """重置全局缓存实例（仅用于测试）"""
    global _cache_instance
    with _cache_lock:
        _cache_instance = None


# ==================== 缓存键与 TTL 常量 ====================

PROJECTS_TTL = 300       # 项目列表 5 分钟
ENVIRONMENTS_TTL = 120   # 环境列表 2 分钟
DASHBOARD_TTL = 60       # Dashboard 统计 1 分钟


def projects_key(user_id: int) -> str:
    return f"projects:user:{user_id}"


def environments_key(user_id: int, project_id: Optional[int] = None) -> str:
    if project_id:
        return f"envs:user:{user_id}:proj:{project_id}"
    return f"envs:user:{user_id}"


def dashboard_key(user_id: int) -> str:
    return f"dashboard:user:{user_id}"
