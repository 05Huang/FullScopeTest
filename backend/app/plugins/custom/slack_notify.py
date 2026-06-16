"""
Slack 通知示例插件

在测试执行完成/失败时发送 Slack 通知。
通过环境变量 SLACK_WEBHOOK_URL 配置 Webhook 地址。

用法：
    1. 设置环境变量 SLACK_WEBHOOK_URL
    2. 插件会自动加载并在测试事件时发送通知
"""
import os
from ..base import PluginBase
from ...core.logging import get_logger

logger = get_logger(__name__)


class SlackNotifyPlugin(PluginBase):
    """Slack 通知插件"""

    name = 'slack_notify'
    version = '1.0.0'
    description = '测试执行完成/失败时发送 Slack 通知'

    def on_init(self, app):
        """初始化时检查配置"""
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL', '')
        if not webhook_url:
            self.log('warning', 'SLACK_WEBHOOK_URL 未配置，Slack 通知将不可用')

    def on_event(self, event_name: str, data: dict):
        """处理事件"""
        if event_name == 'test_completed':
            self._send_notification(data, success=True)
        elif event_name == 'test_failed':
            self._send_notification(data, success=False)

    def _send_notification(self, data: dict, success: bool):
        """发送 Slack 通知"""
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL', '')
        if not webhook_url:
            return

        try:
            import requests
            emoji = '✅' if success else '❌'
            status = '通过' if success else '失败'
            run_id = data.get('run_id', 'N/A')
            test_name = data.get('test_name', data.get('test_object_name', 'N/A'))

            payload = {
                'text': f'{emoji} 测试{status}: {test_name} (Run #{run_id})',
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'{emoji} *测试{status}*\n'
                                    f'- *测试名称:* {test_name}\n'
                                    f'- *Run ID:* {run_id}\n'
                                    f'- *状态:* {status}',
                        },
                    },
                ],
            }

            resp = requests.post(webhook_url, json=payload, timeout=10)
            if resp.status_code < 400:
                self.log('info', 'Slack 通知已发送', status=resp.status_code)
            else:
                self.log('warning', 'Slack 通知发送失败', status=resp.status_code)
        except Exception as exc:
            self.log('error', 'Slack 通知异常', error=str(exc))