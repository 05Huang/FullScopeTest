"""
邮件发送服务

支持多种邮件后端：
- SMTP（通用，通过 SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASSWORD 配置）
- SendGrid API（通过 SENDGRID_API_KEY 配置）
- 控制台输出（开发环境，EMAIL_BACKEND=console）
"""

import os
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..core.logging import get_logger

logger = get_logger(__name__)


class EmailBackend(ABC):
    """邮件后端抽象基类"""

    @abstractmethod
    def send(self, to, subject, html_body, text_body=""):
        ...


class ConsoleEmailBackend(EmailBackend):
    """控制台输出邮件后端（开发环境）"""

    def send(self, to, subject, html_body, text_body=""):
        logger.info("[console] 模拟发送邮件", to=to, subject=subject)
        return True


class SmtpEmailBackend(EmailBackend):
    """SMTP 邮件后端"""

    def __init__(self):
        self.host = os.environ.get("SMTP_HOST", "")
        self.port = int(os.environ.get("SMTP_PORT", "587"))
        self.user = os.environ.get("SMTP_USER", "")
        self.password = os.environ.get("SMTP_PASSWORD", "")
        self.use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"

    def send(self, to, subject, html_body, text_body=""):
        try:
            from_name = os.environ.get("EMAIL_FROM_NAME", "FullScopeTest")
            from_addr = os.environ.get("EMAIL_FROM", "noreply@example.com")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_addr}>"
            msg["To"] = to

            if text_body:
                msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            if self.use_tls:
                server = smtplib.SMTP(self.host, self.port, timeout=30)
                server.starttls()
            else:
                server = smtplib.SMTP(self.host, self.port, timeout=30)

            try:
                if self.user:
                    server.login(self.user, self.password)

                server.sendmail(from_addr, [to], msg.as_string())
            finally:
                # 确保连接始终关闭，防止连接泄漏
                try:
                    server.quit()
                except Exception:
                    pass

            logger.info("SMTP 邮件发送成功", to=to, subject=subject)
            return True
        except Exception as exc:
            logger.error("SMTP 邮件发送失败", to=to, error=str(exc))
            return False


class SendGridEmailBackend(EmailBackend):
    """SendGrid API 邮件后端"""

    def __init__(self):
        self.api_key = os.environ.get("SENDGRID_API_KEY", "")
        self.from_email = os.environ.get("EMAIL_FROM", "noreply@example.com")
        self.from_name = os.environ.get("EMAIL_FROM_NAME", "FullScopeTest")

    def send(self, to, subject, html_body, text_body=""):
        try:
            import requests as http_requests

            response = http_requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": to}]}],
                    "from": {"email": self.from_email, "name": self.from_name},
                    "subject": subject,
                    "content": [
                        {"type": "text/plain", "value": text_body or ""},
                        {"type": "text/html", "value": html_body},
                    ],
                },
                timeout=30,
            )

            if response.status_code in (200, 201, 202):
                logger.info("SendGrid 邮件发送成功", to=to, subject=subject)
                return True
            else:
                logger.error("SendGrid 邮件发送失败", to=to, status=response.status_code)
                return False
        except Exception as exc:
            logger.error("SendGrid 邮件发送失败", to=to, error=str(exc))
            return False


class EmailService:
    """统一邮件发送服务"""

    def __init__(self):
        self.enabled = os.environ.get("EMAIL_ENABLED", "false").lower() == "true"
        backend_type = os.environ.get("EMAIL_BACKEND", "console").lower()

        if not self.enabled:
            self._backend = ConsoleEmailBackend()
            logger.info("邮件服务未启用，使用控制台输出模式")
        elif backend_type == "smtp":
            self._backend = SmtpEmailBackend()
            logger.info("邮件服务已启用，后端: SMTP")
        elif backend_type == "sendgrid":
            self._backend = SendGridEmailBackend()
            logger.info("邮件服务已启用，后端: SendGrid")
        else:
            self._backend = ConsoleEmailBackend()
            logger.info("邮件服务使用控制台输出模式")

    def send_email(self, to, subject, html_body, text_body=""):
        """发送邮件"""
        if not to:
            logger.warning("邮件发送跳过：收件人为空")
            return False
        return self._backend.send(to, subject, html_body, text_body)

    def send_password_reset_email(self, to, username, reset_token):
        """发送密码重置邮件"""
        frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
        reset_url = f"{frontend_url}/reset-password?token={reset_token}"

        subject = "[FullScopeTest] 密码重置"
        html_body = _render_reset_email_html(username, reset_url)
        text_body = (
            f"您好 {username}，\n\n"
            f"您请求了密码重置。请点击以下链接重置密码：\n"
            f"{reset_url}\n\n"
            f"此链接 1 小时内有效。如果您没有请求重置密码，请忽略此邮件。\n\n"
            f"—— FullScopeTest 团队"
        )

        return self.send_email(to, subject, html_body, text_body)


def _render_reset_email_html(username, reset_url):
    """渲染密码重置邮件 HTML 模板"""
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8"></head>'
        '<body style="font-family:-apple-system,sans-serif;background:#f5f5f5;padding:40px 0;">'
        '<div style="max-width:480px;margin:0 auto;background:#fff;border-radius:12px;'
        'box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">'
        '<div style="background:linear-gradient(135deg,#5FA59B,#3D6E66);padding:24px;text-align:center;">'
        '<h1 style="color:#fff;margin:0;font-size:20px;">FullScopeTest</h1>'
        '</div>'
        '<div style="padding:32px 24px;">'
        f'<p>您好 <strong>{username}</strong>，</p>'
        '<p>您请求了密码重置。请点击下方按钮重置密码，链接 <strong>1 小时</strong>内有效。</p>'
        '<div style="text-align:center;margin:28px 0;">'
        f'<a href="{reset_url}" style="display:inline-block;background:#5FA59B;color:#fff;'
        'padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:600;">重置密码</a>'
        '</div>'
        f'<p style="color:#999;font-size:12px;">链接: {reset_url}</p>'
        '<hr style="border:none;border-top:1px solid #eee;margin:24px 0;"/>'
        '<p style="color:#aaa;font-size:11px;">如果您没有请求重置密码，请忽略此邮件。</p>'
        '</div></div></body></html>'
    )


# 全局单例
email_service = EmailService()
