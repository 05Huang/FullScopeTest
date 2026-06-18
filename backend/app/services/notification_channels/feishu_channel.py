"""飞书 Webhook 通知渠道"""
import os
import hashlib
import hmac
import time
import base64
import requests as http_requests

from ...core.logging import get_logger

logger = get_logger(__name__)


class FeishuChannel:
    """飞书通知 — Webhook URL + 签名验证"""

    def __init__(self, config=None):
        self.config = config or {}
        self.webhook_url = self.config.get("webhook_url", os.environ.get("FEISHU_WEBHOOK_URL", ""))
        self.secret = self.config.get("secret", os.environ.get("FEISHU_WEBHOOK_SECRET", ""))

    def _sign(self, timestamp):
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(hmac_code).decode("utf-8")

    def send(self, title, content, **kwargs):
        if not self.webhook_url:
            logger.warning("飞书 Webhook URL 未配置")
            return False
        try:
            timestamp = str(int(time.time()))
            payload = {
                "msg_type": "interactive",
                "card": {
                    "header": {"title": {"tag": "plain_text", "content": title}, "template": "blue"},
                    "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": content}}],
                },
            }
            if self.secret:
                payload["timestamp"] = timestamp
                payload["sign"] = self._sign(timestamp)
            resp = http_requests.post(self.webhook_url, json=payload, timeout=10)
            if resp.status_code == 200 and resp.json().get("code") == 0:
                logger.info("飞书消息发送成功", title=title)
                return True
            logger.error("飞书消息发送失败", status=resp.status_code)
            return False
        except Exception as exc:
            logger.error("飞书消息发送异常", error=str(exc))
            return False
