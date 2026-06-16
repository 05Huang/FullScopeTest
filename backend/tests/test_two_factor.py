"""
双因素认证（2FA/TOTP）服务测试
"""

import pytest
import time


class TestTwoFactorService:
    """TwoFactorService 测试"""

    def test_generate_secret(self, app):
        """生成密钥应为 Base32 编码"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            secret = svc.generate_secret()
            assert isinstance(secret, str)
            assert len(secret) >= 20

    def test_generate_totp(self, app):
        """生成的 TOTP 应为 6 位数字"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            secret = svc.generate_secret()
            code = svc.generate_totp(secret)
            assert len(code) == 6
            assert code.isdigit()

    def test_verify_totp_valid(self, app):
        """验证正确的 TOTP 应通过"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            secret = svc.generate_secret()
            code = svc.generate_totp(secret)
            assert svc.verify_totp(secret, code) is True

    def test_verify_totp_invalid(self, app):
        """验证错误的 TOTP 应失败"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            secret = svc.generate_secret()
            assert svc.verify_totp(secret, "000000") is False

    def test_verify_totp_with_window(self, app):
        """时间窗口内的验证码应通过"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService, TOTP_PERIOD
            svc = TwoFactorService()
            secret = svc.generate_secret()
            # 前一个时间窗口的验证码',
            code = svc.generate_totp(secret, int(time.time()) - TOTP_PERIOD)
            assert svc.verify_totp(secret, code, window=1) is True

    def test_generate_recovery_codes(self, app):
        """应生成 8 个恢复码"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            codes = svc.generate_recovery_codes()
            assert len(codes) == 8
            for code in codes:
                assert len(code) == 9  # XXXX-XXXX
                assert code[4] == "-"

    def test_provisioning_uri(self, app):
        """配置 URI 应包含正确格式"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            secret = svc.generate_secret()
            uri = svc.generate_provisioning_uri(secret, "test@example.com")
            assert uri.startswith("otpauth://totp/")
            assert "test@example.com" in uri
            assert secret in uri

    def test_setup_2fa(self, app):
        """2FA 设置应返回密钥和恢复码"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            result = svc.setup_2fa("test@example.com")
            assert "secret" in result
            assert "provisioning_uri" in result
            assert "recovery_codes" in result
            assert len(result["recovery_codes"]) == 8

    def test_verify_and_activate(self, app):
        """激活验证应正确工作"""
        with app.app_context():
            from app.services.two_factor_service import TwoFactorService
            svc = TwoFactorService()
            secret = svc.generate_secret()
            code = svc.generate_totp(secret)
            assert svc.verify_and_activate(secret, code) is True
