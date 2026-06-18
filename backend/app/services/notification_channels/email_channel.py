"""邮件通知渠道"""
from ...core.logging import get_logger

logger = get_logger(__name__)


class EmailChannel:
    """邮件通知渠道 — 依赖 P24-1 的 EmailService"""

    def __init__(self, config=None):
        self.config = config or {}

    def send(self, to, subject, content, **kwargs):
        from ..email_service import email_service
        return email_service.send_email(to=to, subject=subject, html_body=content, text_body=content)
