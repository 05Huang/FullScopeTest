"""
会话状态存储抽象层

将运行时状态（录制进程、Live View 会话等）从进程内存迁移到 Redis，
支持多实例部署共享状态，进程重启后状态可恢复。

Redis 不可用时自动回退到内存 dict（开发/测试场景）。
"""

import json
import os
import time
import threading
from typing import Any, Optional

from ..core.logging import get_logger

logger = get_logger(__name__)


class SessionStore:
    """会话状态存储接口"""

    def get(self, key: str) -> Optional[dict]:
        """获取键值，不存在返回 None"""
        raise NotImplementedError

    def set(self, key: str, value: dict, ttl: Optional[int] = None) -> None:
        """
        设置键值

        Args:
            key: 存储键
            value: 字典值（必须可 JSON 序列化）
            ttl: 过期时间（秒），None 表示不过期
        """
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """删除键"""
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        raise NotImplementedError

    def expire(self, key: str, ttl: int) -> None:
        """设置过期时间（秒）"""
        raise NotImplementedError

    def keys(self, pattern: str) -> list:
        """按模式匹配获取所有键"""
        raise NotImplementedError

    @property
    def backend(self) -> str:
        """返回存储后端名称，用于日志和诊断"""
        raise NotImplementedError


class RedisSessionStore(SessionStore):
    """
    基于 Redis 的会话状态存储

    数据以 JSON 字符串存储在 Redis STRING 类型中，
    通过 key 前缀区分不同类型会话。
    """

    def __init__(self, redis_url: str):
        import redis as redis_lib
        self._redis = redis_lib.from_url(
            redis_url,
            decode_responses=True,
            socket_timeout=2,
            socket_connect_timeout=2,
        )
        # 验证连接
        try:
            self._redis.ping()
        except Exception as exc:
            logger.error("Redis SessionStore 连接失败", error=str(exc))
            raise

    def get(self, key: str) -> Optional[dict]:
        raw = self._redis.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            logger.warning("SessionStore JSON 解析失败", key=key)
            return None

    def set(self, key: str, value: dict, ttl: Optional[int] = None) -> None:
        data = json.dumps(value, ensure_ascii=False)
        if ttl is not None and ttl > 0:
            self._redis.setex(key, ttl, data)
        else:
            self._redis.set(key, data)

    def delete(self, key: str) -> None:
        self._redis.delete(key)

    def exists(self, key: str) -> bool:
        return self._redis.exists(key) > 0

    def expire(self, key: str, ttl: int) -> None:
        self._redis.expire(key, ttl)

    def keys(self, pattern: str) -> list:
        return self._redis.keys(pattern)

    @property
    def backend(self) -> str:
        return "redis"


class MemorySessionStore(SessionStore):
    """
    基于内存 dict 的会话状态存储

    开发和测试环境的回退方案。支持 TTL，通过后台清理线程实现。
    多次 get 返回副本，防止调用方意外修改内部状态。
    """

    def __init__(self):
        self._store: dict[str, tuple[dict, Optional[float]]] = {}
        self._lock = threading.Lock()

        # 后台清理过期键（每 60 秒一次）
        self._cleanup_stop = threading.Event()
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True, name="session-store-cleanup"
        )
        self._cleanup_thread.start()

    def _cleanup_loop(self):
        while not self._cleanup_stop.wait(timeout=60):
            self._purge_expired()

    def _purge_expired(self):
        now = time.time()
        with self._lock:
            expired_keys = [
                key for key, (_, exp) in self._store.items()
                if exp is not None and now >= exp
            ]
            for key in expired_keys:
                del self._store[key]

    def get(self, key: str) -> Optional[dict]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, exp = entry
            if exp is not None and time.time() >= exp:
                del self._store[key]
                return None
            return dict(value)

    def set(self, key: str, value: dict, ttl: Optional[int] = None) -> None:
        exp = (time.time() + ttl) if ttl is not None and ttl > 0 else None
        with self._lock:
            self._store[key] = (dict(value), exp)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def exists(self, key: str) -> bool:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return False
            _, exp = entry
            if exp is not None and time.time() >= exp:
                del self._store[key]
                return False
            return True

    def expire(self, key: str, ttl: int) -> None:
        with self._lock:
            entry = self._store.get(key)
            if entry is not None:
                value, _ = entry
                self._store[key] = (value, time.time() + ttl)

    def keys(self, pattern: str) -> list:
        """简单模式匹配（仅支持 '*' 通配符后缀）"""
        prefix = pattern.rstrip("*")
        suffix = pattern[len(prefix):]  # 通常为 '*'
        with self._lock:
            if suffix == "*":
                return [k for k in self._store if k.startswith(prefix)]
            # 精确匹配
            return [k for k in self._store if k == pattern]

    @property
    def backend(self) -> str:
        return "memory"

    def shutdown(self):
        """停止后台清理线程"""
        self._cleanup_stop.set()


# ==================== 工厂函数 ====================

_store_instance: Optional[SessionStore] = None
_store_lock = threading.Lock()


def get_session_store() -> SessionStore:
    """
    获取全局 SessionStore 实例（懒初始化、线程安全）

    优先使用 Redis（通过 REDIS_URL 环境变量），不可用时回退到内存存储。
    """
    global _store_instance
    if _store_instance is not None:
        return _store_instance

    with _store_lock:
        if _store_instance is not None:
            return _store_instance

        redis_url = os.environ.get("REDIS_URL", "").strip()
        if redis_url:
            try:
                _store_instance = RedisSessionStore(redis_url)
                logger.info("SessionStore 使用 Redis 后端", redis_url=redis_url.split("@")[-1])
                return _store_instance
            except Exception as exc:
                logger.warning(
                    "Redis SessionStore 初始化失败，回退到内存存储",
                    error=str(exc),
                )

        _store_instance = MemorySessionStore()
        logger.info("SessionStore 使用内存后端（开发/测试模式）")
        return _store_instance


def reset_session_store():
    """重置全局实例（仅用于测试）"""
    global _store_instance
    with _store_lock:
        if isinstance(_store_instance, MemorySessionStore):
            _store_instance.shutdown()
        _store_instance = None


# ==================== 常量 ====================

# 录制会话 TTL（1 小时）
RECORDING_TTL = 3600

# Live View 会话 TTL（30 分钟）
LIVE_VIEW_TTL = 1800

# 键前缀
RECORDING_KEY_PREFIX = "recording:"
LIVE_VIEW_KEY_PREFIX = "live_view:"
