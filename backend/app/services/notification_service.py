"""
Webhook 通知服务

支持多种通知渠道，测试执行完成后自动触发通知。

支持渠道：
- webhook: 通用 Webhook URL（POST JSON）
- dingtalk: 钉钉机器人
- feishu: 飞书机器人
- slack: Slack Incoming Webhook

通知事件：
- test_completed: 测试执行完成
- test_failed: 测试执行失败
- alert_triggered: 告警触发
"""
import json
import time
import os
import requests
from typing import Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# 最大重试次数
MAX_RETRIES = 3
# 初始重试间隔（秒）
INITIAL_RETRY_DELAY = 2


def send_notification(
    channel: str,
    webhook_url: str,
    event: str,
    title: str,
    content: str,
    extra: dict = None,
    token: str = None,
) -> dict:
    """
    发送通知

    Args:
        channel: 渠道类型（webhook/dingtalk/feishu/slack）
        webhook_url: Webhook URL
        event: 事件类型
        title: 通知标题
        content: 通知内容
        extra: 附加数据
        token: 认证 Token（Slack Bearer Token 等）

    Returns:
        dict: {success: bool, status_code: int, error: str}
    """
    payload = _build_payload(channel, event, title, content, extra)
    headers = {'Content-Type': 'application/json'}
    if token and channel == 'slack':
        headers['Authorization'] = f'Bearer {token}'

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10,
            )
            if resp.status_code < 400:
                logger.info("通知发送成功", channel=channel, notify_event=event,
                           status=resp.status_code, attempt=attempt + 1)
                return {'success': True, 'status_code': resp.status_code}

            logger.warning("通知发送失败", channel=channel, notify_event=event,
                          status=resp.status_code, attempt=attempt + 1)
        except requests.RequestException as exc:
            logger.warning("通知发送异常", channel=channel, notify_event=event,
                          error=str(exc), attempt=attempt + 1)

        # 指数退避
        if attempt < MAX_RETRIES - 1:
            delay = INITIAL_RETRY_DELAY * (2 ** attempt)
            time.sleep(delay)

    logger.error("通知发送最终失败", channel=channel, notify_event=event, url=webhook_url)
    return {'success': False, 'status_code': 0, 'error': 'max retries exceeded'}


def _build_payload(channel: str, event: str, title: str, content: str, extra: dict = None) -> dict:
    """根据渠道构建通知 payload"""
    if channel == 'dingtalk':
        return {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': f'### {title}\n\n{content}',
            },
        }
    elif channel == 'feishu':
        return {
            'msg_type': 'interactive',
            'card': {
                'header': {'title': {'tag': 'plain_text', 'content': title}},
                'elements': [
                    {'tag': 'div', 'text': {'tag': 'plain_text', 'content': content}},
                ],
            },
        }
    elif channel == 'slack':
        return {
            'text': f'*{title}*\n{content}',
            'blocks': [
                {'type': 'header', 'text': {'type': 'plain_text', 'text': title}},
                {'type': 'section', 'text': {'type': 'mrkdwn', 'text': content}},
            ],
        }
    else:
        # 通用 Webhook
        return {
            'event': event,
            'title': title,
            'content': content,
            'data': extra or {},
            'source': 'fullscopetest',
        }


def notify_test_result(
    webhook_url: str,
    channel: str,
    test_name: str,
    status: str,
    duration: float = 0,
    details: str = '',
):
    """
    通知测试执行结果（便捷方法）

    Args:
        webhook_url: Webhook URL
        channel: 渠道类型
        test_name: 测试名称
        status: 状态（completed/failed）
        duration: 执行时长（秒）
        details: 详细信息
    """
    event = 'test_completed' if status == 'completed' else 'test_failed'
    emoji = '✅' if status == 'completed' else '❌'
    title = f'{emoji} 测试{status}: {test_name}'
    content = f'**测试名称:** {test_name}\n**状态:** {status}\n**耗时:** {duration:.1f}s'
    if details:
        content += f'\n**详情:** {details}'

    return send_notification(
        channel=channel,
        webhook_url=webhook_url,
        event=event,
        title=title,
        content=content,
        extra={'test_name': test_name, 'status': status, 'duration': duration},
    )
