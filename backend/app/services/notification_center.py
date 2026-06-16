"""
通知中心服务

提供统一的通知管理，支持多种通知类型和实时推送。
"""

import time
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)


class Notification:
    """通知对象"""

    def __init__(self, user_id: int, notification_type: str, title: str,
                 content: str = "", data: Dict = None, is_read: bool = False):
        self.id = int(time.time() * 1000)  # 简单 ID 生成
        self.user_id = user_id
        self.notification_type = notification_type
        self.title = title
        self.content = content
        self.data = data or {}
        self.is_read = is_read
        self.created_at = time.time()

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "type": self.notification_type,
                "title": self.title, "content": self.content, "data": self.data,
                "is_read": self.is_read, "created_at": self.created_at}


class NotificationCenter:
    """通知中心管理器"""

    def __init__(self):
        self._notifications: Dict[int, List[Notification]] = {}  # user_id -> notifications

    def send(self, user_id: int, notification_type: str, title: str,
             content: str = "", data: Dict = None) -> Notification:
        """发送通知"""
        if user_id not in self._notifications:
            self._notifications[user_id] = []

        notification = Notification(
            user_id=user_id, notification_type=notification_type,
            title=title, content=content, data=data,
        )
        self._notifications[user_id].append(notification)

        # 防止内存溢出
        if len(self._notifications[user_id]) > 500:
            self._notifications[user_id] = self._notifications[user_id][-250:]

        logger.info("通知已发送", user_id=user_id, type=notification_type, title=title)
        return notification

    def get_notifications(self, user_id: int, unread_only: bool = False,
                         limit: int = 50) -> List[Dict[str, Any]]:
        """获取用户通知列表"""
        notifications = self._notifications.get(user_id, [])
        if unread_only:
            notifications = [n for n in notifications if not n.is_read]
        # 按时间倒序
        notifications = sorted(notifications, key=lambda n: n.created_at, reverse=True)
        return [n.to_dict() for n in notifications[:limit]]

    def get_unread_count(self, user_id: int) -> int:
        """获取未读通知数"""
        return len([n for n in self._notifications.get(user_id, []) if not n.is_read])

    def mark_read(self, user_id: int, notification_id: int) -> bool:
        """标记单条通知为已读"""
        for n in self._notifications.get(user_id, []):
            if n.id == notification_id:
                n.is_read = True
                return True
        return False

    def mark_all_read(self, user_id: int) -> int:
        """标记所有通知为已读"""
        count = 0
        for n in self._notifications.get(user_id, []):
            if not n.is_read:
                n.is_read = True
                count += 1
        return count


_instance = None


def get_notification_center():
    global _instance
    if _instance is None: _instance = NotificationCenter()
    return _instance
