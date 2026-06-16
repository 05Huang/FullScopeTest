"""
配置热更新服务

支持运行时修改配置，无需重启服务。
"""

import os
import json
import time
from typing import Dict, Any, Optional, List
from ..core.logging import get_logger

logger = get_logger(__name__)

# 可热更新的配置项
HOT_RELOADABLE = {
    "AI_ASSISTANT_MODEL", "AI_ASSISTANT_TIMEOUT",
    "RATELIMIT_DEFAULT", "PARALLEL_WORKERS",
    "SESSION_TIMEOUT", "DATA_MASKING_ENABLED",
    "COMPRESSION_ENABLED", "TRACING_ENABLED",
}

# 不可热更新的配置项（需重启）
REQUIRES_RESTART = {
    "DATABASE_URL", "REDIS_URL", "SECRET_KEY", "JWT_SECRET_KEY",
}


class ConfigService:
    """配置热更新服务"""

    def __init__(self):
        self._overrides: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（优先使用覆盖值）"""
        if key in self._overrides:
            return self._overrides[key]
        return os.environ.get(key, default)

    def set(self, key: str, value: Any, user_id: int = None) -> Dict[str, Any]:
        """
        设置配置覆盖值

        Args:
            key: 配置键
            value: 配置值
            user_id: 操作者 ID

        Returns:
            Dict: 操作结果
        """
        if key in REQUIRES_RESTART:
            return {"success": False, "message": f"{key} 需要重启服务才能生效"}

        old_value = self._overrides.get(key)
        self._overrides[key] = value

        # 记录变更历史
        self._history.append({
            "key": key, "old_value": old_value, "new_value": value,
            "user_id": user_id, "timestamp": time.time(),
        })

        # 同步到环境变量
        os.environ[key] = str(value)

        logger.info("配置已更新", key=key, value=str(value)[:100])
        return {"success": True, "message": f"{key} 已更新"}

    def list_overrides(self) -> Dict[str, Any]:
        """列出所有配置覆盖"""
        return dict(self._overrides)

    def get_history(self) -> List[Dict[str, Any]]:
        """获取变更历史"""
        return list(self._history)

    def rollback(self, key: str) -> bool:
        """回滚配置到上一个值"""
        for entry in reversed(self._history):
            if entry["key"] == key:
                old = entry["old_value"]
                if old is not None:
                    self._overrides[key] = old
                    os.environ[key] = str(old)
                else:
                    self._overrides.pop(key, None)
                    os.environ.pop(key, None)
                logger.info("配置已回滚", key=key)
                return True
        return False

    def is_reloadable(self, key: str) -> bool:
        """检查配置是否可热更新"""
        return key in HOT_RELOADABLE


_instance = None


def get_config_service() -> ConfigService:
    global _instance
    if _instance is None: _instance = ConfigService()
    return _instance
