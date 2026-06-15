"""
SessionStore 单元测试

覆盖：
- MemorySessionStore 全部接口
- TTL 过期行为
- RedisSessionStore（mock Redis）
- 工厂函数回退逻辑
"""

import os
import time
import threading
from unittest.mock import patch, MagicMock

import pytest


# ====================================================================
# MemorySessionStore 测试
# ====================================================================

class TestMemorySessionStore:
    """内存 SessionStore 测试"""

    def setup_method(self):
        from app.services.session_store import MemorySessionStore
        self.store = MemorySessionStore()

    def teardown_method(self):
        self.store.shutdown()

    # ---- 基础读写 ----

    def test_set_get_returns_dict(self):
        self.store.set("k1", {"name": "test"})
        result = self.store.get("k1")
        assert result == {"name": "test"}

    def test_get_nonexistent_returns_none(self):
        assert self.store.get("no_such_key") is None

    def test_set_overwrites_existing(self):
        self.store.set("k1", {"v": 1})
        self.store.set("k1", {"v": 2})
        assert self.store.get("k1") == {"v": 2}

    def test_get_returns_copy(self):
        """返回副本，修改不影响内部状态"""
        self.store.set("k1", {"v": 1})
        result = self.store.get("k1")
        result["v"] = 999
        assert self.store.get("k1") == {"v": 1}

    # ---- delete ----

    def test_delete_existing_key(self):
        self.store.set("k1", {"v": 1})
        self.store.delete("k1")
        assert self.store.get("k1") is None

    def test_delete_nonexistent_key_no_error(self):
        self.store.delete("no_such_key")

    # ---- exists ----

    def test_exists_returns_true(self):
        self.store.set("k1", {"v": 1})
        assert self.store.exists("k1") is True

    def test_exists_returns_false(self):
        assert self.store.exists("no_such_key") is False

    # ---- TTL ----

    def test_set_with_ttl_key_still_exists(self):
        self.store.set("k1", {"v": 1}, ttl=60)
        assert self.store.exists("k1") is True
        assert self.store.get("k1") == {"v": 1}

    def test_set_with_ttl_zero_no_expiry(self):
        self.store.set("k1", {"v": 1}, ttl=0)
        assert self.store.get("k1") == {"v": 1}

    def test_set_with_ttl_negative_no_expiry(self):
        self.store.set("k1", {"v": 1}, ttl=-5)
        assert self.store.get("k1") == {"v": 1}

    def test_key_expires_after_ttl(self):
        self.store.set("k1", {"v": 1}, ttl=1)
        time.sleep(1.1)
        assert self.store.get("k1") is None

    def test_expire_sets_ttl(self):
        self.store.set("k1", {"v": 1})
        self.store.expire("k1", 1)
        assert self.store.get("k1") == {"v": 1}
        time.sleep(1.1)
        assert self.store.get("k1") is None

    def test_expire_nonexistent_key_no_error(self):
        self.store.expire("no_such_key", 60)

    # ---- keys ----

    def test_keys_wildcard_match(self):
        self.store.set("recording:1", {"pid": 100})
        self.store.set("recording:2", {"pid": 200})
        self.store.set("live_view:abc", {"sid": "abc"})

        result = self.store.keys("recording:*")
        assert sorted(result) == ["recording:1", "recording:2"]

    def test_keys_exact_match(self):
        self.store.set("exact_key", {"v": 1})
        result = self.store.keys("exact_key")
        assert result == ["exact_key"]

    def test_keys_empty_result(self):
        result = self.store.keys("nonexistent:*")
        assert result == []

    # ---- TTL 清理线程 ----

    def test_cleanup_removes_expired_keys(self):
        self.store.set("k1", {"v": 1}, ttl=1)
        time.sleep(1.1)
        # 手动触发清理
        self.store._purge_expired()
        assert self.store.exists("k1") is False

    # ---- backend ----

    def test_backend_returns_memory(self):
        assert self.store.backend == "memory"


# ====================================================================
# RedisSessionStore 测试（Mock Redis）
# ====================================================================

class TestRedisSessionStore:
    """Redis SessionStore 测试（通过 mock 隔离真实 Redis）"""

    def _make_store(self):
        """构造带 mock redis 的 RedisSessionStore"""
        with patch("redis.from_url") as mock_from_url:
            mock_redis = MagicMock()
            mock_from_url.return_value = mock_redis
            from app.services.session_store import RedisSessionStore
            store = RedisSessionStore("redis://fake:6379/0")
        store._redis = mock_redis
        return store, mock_redis

    def test_set_calls_setex_with_ttl(self):
        store, mock_redis = self._make_store()
        store.set("k1", {"v": 1}, ttl=300)
        mock_redis.setex.assert_called_once()
        args = mock_redis.setex.call_args[0]
        assert args[0] == "k1"
        assert args[1] == 300

    def test_set_without_ttl_calls_set(self):
        store, mock_redis = self._make_store()
        store.set("k1", {"v": 1})
        mock_redis.set.assert_called_once()

    def test_get_returns_parsed_json(self):
        store, mock_redis = self._make_store()
        mock_redis.get.return_value = '{"v": 1}'
        result = store.get("k1")
        assert result == {"v": 1}

    def test_get_returns_none_when_missing(self):
        store, mock_redis = self._make_store()
        mock_redis.get.return_value = None
        result = store.get("k1")
        assert result is None

    def test_get_handles_invalid_json(self):
        store, mock_redis = self._make_store()
        mock_redis.get.return_value = "NOT_JSON"
        result = store.get("k1")
        assert result is None

    def test_delete_calls_redis_delete(self):
        store, mock_redis = self._make_store()
        store.delete("k1")
        mock_redis.delete.assert_called_once_with("k1")

    def test_exists_true(self):
        store, mock_redis = self._make_store()
        mock_redis.exists.return_value = 1
        assert store.exists("k1") is True

    def test_exists_false(self):
        store, mock_redis = self._make_store()
        mock_redis.exists.return_value = 0
        assert store.exists("k1") is False

    def test_expire_calls_redis(self):
        store, mock_redis = self._make_store()
        store.expire("k1", 60)
        mock_redis.expire.assert_called_once_with("k1", 60)

    def test_keys_calls_redis(self):
        store, mock_redis = self._make_store()
        mock_redis.keys.return_value = ["recording:1", "recording:2"]
        result = store.keys("recording:*")
        mock_redis.keys.assert_called_once_with("recording:*")
        assert result == ["recording:1", "recording:2"]

    def test_backend_returns_redis(self):
        store, _ = self._make_store()
        assert store.backend == "redis"


# ====================================================================
# 工厂函数测试
# ====================================================================

class TestGetSessionStore:
    """工厂函数 get_session_store 测试"""

    def setup_method(self):
        from app.services.session_store import reset_session_store
        reset_session_store()

    def teardown_method(self):
        from app.services.session_store import reset_session_store
        reset_session_store()

    def test_fallback_to_memory_when_no_redis_url(self):
        with patch.dict(os.environ, {"REDIS_URL": ""}, clear=False):
            from app.services.session_store import get_session_store
            store = get_session_store()
            assert store.backend == "memory"

    def test_fallback_to_memory_when_redis_unavailable(self):
        with patch.dict(os.environ, {"REDIS_URL": "redis://fakehost:9999/0"}, clear=False):
            from app.services.session_store import get_session_store
            store = get_session_store()
            # 连接失败应回退到内存
            assert store.backend == "memory"

    def test_returns_same_instance_on_repeated_calls(self):
        from app.services.session_store import get_session_store
        s1 = get_session_store()
        s2 = get_session_store()
        assert s1 is s2


# ====================================================================
# 模块级常量测试
# ====================================================================

def test_ttl_constants():
    from app.services.session_store import RECORDING_TTL, LIVE_VIEW_TTL
    assert RECORDING_TTL == 3600   # 1 小时
    assert LIVE_VIEW_TTL == 1800   # 30 分钟


def test_key_prefixes():
    from app.services.session_store import RECORDING_KEY_PREFIX, LIVE_VIEW_KEY_PREFIX
    assert RECORDING_KEY_PREFIX == "recording:"
    assert LIVE_VIEW_KEY_PREFIX == "live_view:"
