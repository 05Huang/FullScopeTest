"""Slack Incoming Webhook 通知渠道"""
import os
import requests as http_requests

from ...core.logging import get_logger

logger = get_logger(__name__)


class SlackChannel:
    """Slack 通知 — Incoming Webhook + Block Kit"""

    def __init__(self, config=None):
        self.config = config or {}
        self.webhook_url = self.config.get("webhook_url", os.environ.get("SLACK_WEBHOOK_URL", ""))

    def send(self, title, content, **kwargs):
        if not self.webhook_url:
            logger.warning("Slack Webhook URL 未配置")
            return False
        try:
            payload = {
                "blocks": [
                    {"type": "header", "text": {"type": "plain_text", "text": title}},
                    {"type": "section", "text": {"type": "mrkdwn", "text": content}},
                    {"type": "divider"},
                ],
            }
            resp = http_requests.post(self.webhook_url, json=payload, timeout=10)
            if resp.status_code == 200 and resp.text == "ok":
                logger.info("Slack 消息发送成功", title=title)
                return True
            logger.error("Slack 消息发送失败", status=resp.status_code)
            return False
        except Exception as exc:
            logger.error("Slack 消息发送异常", error=str(exc))
            return False
