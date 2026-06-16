"""
Feature Flag 服务

提供功能开关管理，支持灰度发布和 A/B 测试。
"""

import os
import hashlib
from typing import Dict, Any, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)


class FeatureFlag:
    """功能开关"""

    def __init__(self, name: str, enabled: bool = False, flag_type: str = "boolean",
                 percentage: float = 0, user_list: list = None, description: str = ""):
        self.name = name
        self.enabled = enabled
        self.flag_type = flag_type  # boolean/percentage/user_list
        self.percentage = percentage  # 0-100
        self.user_list = user_list or []
        self.description = description

    def evaluate(self, user_id: int = None) -> bool:
        """评估功能开关是否对用户启用"""
        if not self.enabled:
            return False
        if self.flag_type == "boolean":
            return True
        elif self.flag_type == "percentage":
            if user_id is None:
                return False
            # 基于用户 ID 的确定性哈希，保证同一用户始终得到相同结果
            hash_val = int(hashlib.md5(f"{self.name}:{user_id}".encode()).hexdigest(), 16)
            return (hash_val % 100) < self.percentage
        elif self.flag_type == "user_list":
            return user_id in self.user_list
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "enabled": self.enabled, "flag_type": self.flag_type,
                "percentage": self.percentage, "user_list": self.user_list, "description": self.description}


class FeatureFlagService:
    """Feature Flag 管理服务"""

    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}

    def register_flag(self, name: str, enabled: bool = False, flag_type: str = "boolean",
                      percentage: float = 0, user_list: list = None, description: str = "") -> FeatureFlag:
        """注册功能开关"""
        flag = FeatureFlag(name=name, enabled=enabled, flag_type=flag_type,
                          percentage=percentage, user_list=user_list, description=description)
        self._flags[name] = flag
        logger.info("Feature flag registered", name=name, enabled=enabled)
        return flag

    def is_enabled(self, name: str, user_id: int = None) -> bool:
        """检查功能开关是否启用"""
        flag = self._flags.get(name)
        if flag is None:
            # 环境变量覆盖
            env_val = os.environ.get(f"FEATURE_{name.upper()}", "").lower()
            if env_val in ("true", "1", "yes"):
                return True
            return False  # 默认行为：Flag 关闭
        return flag.evaluate(user_id)

    def get_flag(self, name: str) -> Optional[FeatureFlag]:
        """获取功能开关"""
        return self._flags.get(name)

    def list_flags(self):
        """列出所有功能开关"""
        return [f.to_dict() for f in self._flags.values()]

    def toggle_flag(self, name: str, enabled: bool) -> bool:
        """切换功能开关状态"""
        flag = self._flags.get(name)
        if flag:
            flag.enabled = enabled
            logger.info("Feature flag toggled", name=name, enabled=enabled)
            return True
        return False


_instance = None


def get_feature_flag_service() -> FeatureFlagService:
    global _instance
    if _instance is None: _instance = FeatureFlagService()
    return _instance
