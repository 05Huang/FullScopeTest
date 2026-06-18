"""钉钉 Webhook 通知渠道"""
import os
import hashlib
import hmac
import time
import base64
import urllib.parse
import requests as http_requests

from ...core.logging import get_logger

logger = get_logger(__name__)


class DingtalkChannel:
    """钉钉通知 — Webhook URL + 加签"""

    def __init__(self, config=None):
        self.config = config or {}
        self.webhook_url = self.config.get("webhook_url", os.environ.get("DINGTALK_WEBHOOK_URL", ""))
        self.secret = self.config.get("secret", os.environ.get("DINGTALK_WEBHOOK_SECRET", ""))

    def _sign(self, timestamp):
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(self.secret.encode("utf-8"), string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return urllib.parse.quote_plus(base64.b64encode(hmac_code).decode("utf-8"))

    def send(self, title, content, **kwargs):
        if not self.webhook_url:
            logger.warning("钉钉 Webhook URL 未配置")
            return False
        try:
            url = self.webhook_url
            if self.secret:
                timestamp = str(round(time.time() * 1000))
                url = f"{url}&timestamp={timestamp}&sign={self._sign(timestamp)}"
            payload = {"msgtype": "markdown", "markdown": {"title": title, "text": f"### {title}\n\n{content}"}}
            resp = http_requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200 and resp.json().get("errcode") == 0:
                logger.info("钉钉消息发送成功", title=title)
                return True
            logger.error("钉钉消息发送失败", status=resp.status_code)
            return False
        except Exception as exc:
            logger.error("钉钉消息发送异常", error=str(exc))
            return False
