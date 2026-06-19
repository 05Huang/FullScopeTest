"""
Webhook 调试器服务

提供 Webhook URL 自动生成、请求接收、日志查询功能。
"""

import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# 内存存储：token -> {requests: [...], created_at, expires_at}
_webhook_store: Dict[str, Dict[str, Any]] = {}

# 请求日志过期时间（秒）
EXPIRY_SECONDS = 86400  # 24 小时


class WebhookDebuggerService:
    """Webhook 调试器服务"""

    def create_webhook(self, name: str = '') -> Dict[str, Any]:
        """
        创建一个调试用 Webhook

        Returns:
            Dict: {token, url, created_at, expires_at}
        """
        token = str(uuid.uuid4()).replace('-', '')[:16]
        now = datetime.now(timezone.utc)
        _webhook_store[token] = {
            'name': name or f'webhook-{token[:8]}',
            'requests': [],
            'created_at': now.isoformat(),
            'expires_at': now.timestamp() + EXPIRY_SECONDS,
        }
        logger.info('Webhook 已创建', token=token)
        return {
            'token': token,
            'name': _webhook_store[token]['name'],
            'created_at': _webhook_store[token]['created_at'],
            'expires_in': EXPIRY_SECONDS,
        }

    def record_request(
        self,
        token: str,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: str,
        query_params: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        记录一个 Webhook 请求

        Returns:
            记录的请求信息
        """
        self._cleanup_expired()

        webhook = _webhook_store.get(token)
        if not webhook:
            return {'error': 'Webhook 不存在或已过期'}

        req = {
            'id': len(webhook['requests']) + 1,
            'method': method,
            'path': path,
            'headers': {k: v for k, v in headers.items() if k.lower() not in ('host', 'connection')},
            'body': body[:5000] if body else '',
            'query_params': query_params,
            'received_at': datetime.now(timezone.utc).isoformat(),
        }
        webhook['requests'].append(req)

        logger.info('Webhook 请求已记录', token=token, method=method, total=len(webhook['requests']))
        return req

    def get_requests(self, token: str, limit: int = 100) -> Dict[str, Any]:
        """获取 Webhook 的请求日志"""
        self._cleanup_expired()

        webhook = _webhook_store.get(token)
        if not webhook:
            return {'error': 'Webhook 不存在或已过期', 'requests': []}

        requests = webhook['requests'][-limit:]
        return {
            'token': token,
            'name': webhook['name'],
            'total': len(webhook['requests']),
            'requests': list(reversed(requests)),
        }

    def clear_requests(self, token: str) -> Dict[str, Any]:
        """清空 Webhook 请求日志"""
        webhook = _webhook_store.get(token)
        if webhook:
            webhook['requests'] = []
        return {'cleared': True}

    def list_webhooks(self) -> List[Dict[str, Any]]:
        """列出所有活跃的 Webhook"""
        self._cleanup_expired()
        result = []
        for token, webhook in _webhook_store.items():
            result.append({
                'token': token,
                'name': webhook['name'],
                'request_count': len(webhook['requests']),
                'created_at': webhook['created_at'],
            })
        return result

    def _cleanup_expired(self):
        """清理过期的 Webhook"""
        now = time.time()
        expired = [t for t, w in _webhook_store.items() if now > w.get('expires_at', 0)]
        for t in expired:
            del _webhook_store[t]
        if expired:
            logger.info('清理过期 Webhook', count=len(expired))


_instance = None


def get_webhook_debugger_service() -> WebhookDebuggerService:
    global _instance
    if _instance is None:
        _instance = WebhookDebuggerService()
    return _instance
