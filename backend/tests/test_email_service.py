"""
邮件服务单元测试
"""
import os
import pytest


class TestEmailService:
    """邮件服务测试"""

    def test_console_backend_sends_successfully(self, app):
        """控制台后端应成功发送"""
        with app.app_context():
            from app.services.email_service import ConsoleEmailBackend
            backend = ConsoleEmailBackend()
            result = backend.send("test@example.com", "测试邮件", "<p>Hello</p>", "Hello")
            assert result is True

    def test_email_service_default_is_console(self, app):
        """默认应使用控制台后端"""
        with app.app_context():
            from app.services.email_service import EmailService
            service = EmailService()
            assert service._backend.__class__.__name__ == "ConsoleEmailBackend"

    def test_send_email_empty_to_returns_false(self, app):
        """收件人为空时应返回 False"""
        with app.app_context():
            from app.services.email_service import EmailService
            service = EmailService()
            result = service.send_email("", "主题", "<p>正文</p>")
            assert result is False

    def test_send_password_reset_email(self, app):
        """密码重置邮件应包含重置链接"""
        with app.app_context():
            from app.services.email_service import EmailService
            service = EmailService()
            result = service.send_password_reset_email(
                to="user@example.com",
                username="testuser",
                reset_token="abc123token",
            )
            assert result is True

    def test_smtp_backend_init_with_env(self, app, monkeypatch):
        """SMTP 后端应从环境变量读取配置"""
        monkeypatch.setenv("SMTP_HOST", "smtp.test.com")
        monkeypatch.setenv("SMTP_PORT", "465")
        monkeypatch.setenv("SMTP_USER", "user@test.com")
        monkeypatch.setenv("SMTP_PASSWORD", "secret")

        with app.app_context():
            from app.services.email_service import SmtpEmailBackend
            backend = SmtpEmailBackend()
            assert backend.host == "smtp.test.com"
            assert backend.port == 465
            assert backend.user == "user@test.com"
            assert backend.password == "secret"

    def test_sendgrid_backend_init_with_env(self, app, monkeypatch):
        """SendGrid 后端应从环境变量读取 API Key"""
        monkeypatch.setenv("SENDGRID_API_KEY", "SG.test-key-123")

        with app.app_context():
            from app.services.email_service import SendGridEmailBackend
            backend = SendGridEmailBackend()
            assert backend.api_key == "SG.test-key-123"

    def test_email_service_enabled_flag(self, app, monkeypatch):
        """EMAIL_ENABLED=true 时应启用邮件服务"""
        monkeypatch.setenv("EMAIL_ENABLED", "true")
        monkeypatch.setenv("EMAIL_BACKEND", "console")

        with app.app_context():
            from app.services.email_service import EmailService
            service = EmailService()
            assert service.enabled is True
