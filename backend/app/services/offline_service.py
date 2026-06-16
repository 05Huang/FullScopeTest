"""
离线支持服务

提供请求队列管理和乐观更新支持。
"""

import time
from typing import Dict, Any, List, Callable
from ..core.logging import get_logger

logger = get_logger(__name__)


class OfflineQueue:
    """离线请求队列"""

    def __init__(self):
        self._queue: List[Dict[str, Any]] = []
        self._is_online: bool = True

    def enqueue(self, request: Dict[str, Any]):
        """将请求加入队列"""
        request["queued_at"] = time.time()
        self._queue.append(request)
        logger.info("请求已入队", method=request.get("method"), path=request.get("path"))

    def dequeue_all(self) -> List[Dict[str, Any]]:
        """取出所有队列中的请求"""
        requests = list(self._queue)
        self._queue.clear()
        return requests

    def set_online(self, online: bool):
        """设置在线状态"""
        self._is_online = online
        if online:
            logger.info("网络已恢复", pending_requests=len(self._queue))
        else:
            logger.info("网络已断开")

    @property
    def is_online(self) -> bool:
        return self._is_online

    @property
    def pending_count(self) -> int:
        return len(self._queue)


_instance = None


def get_offline_queue():
    global _instance
    if _instance is None: _instance = OfflineQueue()
    return _instance
