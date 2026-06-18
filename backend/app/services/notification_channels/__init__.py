"""
通知渠道包

支持多渠道消息推送：
- email: 邮件通知（依赖 EmailService）
- feishu: 飞书 Webhook 通知
- dingtalk: 钉钉 Webhook 通知
- slack: Slack Incoming Webhook
"""
from .email_channel import EmailChannel
from .feishu_channel import FeishuChannel
from .dingtalk_channel import DingtalkChannel
from .slack_channel import SlackChannel

__all__ = ['EmailChannel', 'FeishuChannel', 'DingtalkChannel', 'SlackChannel']
