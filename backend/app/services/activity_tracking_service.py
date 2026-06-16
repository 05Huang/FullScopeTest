"""
用户行为分析服务

追踪用户操作行为，提供使用分析。
"""

import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from ..core.logging import get_logger

logger = get_logger(__name__)


class ActivityTracker:
    """用户行为追踪器"""

    def __init__(self):
        # 内存存储（生产环境应使用独立表或 Redis）
        self._events: List[Dict[str, Any]] = []

    def track(self, user_id: int, event_type: str, event_name: str,
              properties: Dict[str, Any] = None):
        """
        记录用户行为

        Args:
            user_id: 用户 ID
            event_type: 事件类型（page_view/feature_use/ai_use/error）
            event_name: 事件名称
            properties: 附加属性
        """
        event = {
            "user_id": user_id,
            "event_type": event_type,
            "event_name": event_name,
            "properties": properties or {},
            "timestamp": time.time(),
        }
        self._events.append(event)

        # 防止内存溢出
        if len(self._events) > 10000:
            self._events = self._events[-5000:]

    def get_events(self, user_id: int = None, event_type: str = None,
                   hours: int = 24) -> List[Dict[str, Any]]:
        """获取事件列表"""
        since = time.time() - hours * 3600
        filtered = [e for e in self._events if e["timestamp"] >= since]
        if user_id:
            filtered = [e for e in filtered if e["user_id"] == user_id]
        if event_type:
            filtered = [e for e in filtered if e["event_type"] == event_type]
        return filtered

    def get_dau(self, hours: int = 24) -> int:
        """获取日活跃用户数"""
        events = self.get_events(hours=hours)
        return len(set(e["user_id"] for e in events))

    def get_feature_usage(self, hours: int = 24) -> Dict[str, int]:
        """获取功能使用频率"""
        events = self.get_events(event_type="feature_use", hours=hours)
        usage = {}
        for e in events:
            name = e["event_name"]
            usage[name] = usage.get(name, 0) + 1
        return dict(sorted(usage.items(), key=lambda x: -x[1]))


_instance = None


def get_activity_tracker():
    global _instance
    if _instance is None: _instance = ActivityTracker()
    return _instance
