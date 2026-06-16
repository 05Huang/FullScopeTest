"""
P16 企业安全服务测试（GDPR/Token轮换/IP白名单/数据脱敏）
"""

import pytest


class TestGDPRService:
    """GDPR 服务测试"""

    def test_request_deletion(self, app, client):
        """删除请求应返回正确结构"""
        with app.app_context():
            from app.extensions import db
            from app.models.user import User
            from werkzeug.security import generate_password_hash
            user = User(username="gdpr_test", email="gdpr@test.com", role="user",
                       password_hash=generate_password_hash("Test123456"))
            db.session.add(user)
            db.session.commit()
            from app.services.gdpr_service import GDPRService
            svc = GDPRService()
            result = svc.request_account_deletion(user_id=user.id)
            assert result["status"] == "pending"
            assert result["cooling_period_days"] == 30


class TestTokenRotationService:
    """Token 轮换服务测试"""

    def test_generate_token(self, app):
        """生成的 Token 应以 fst_ 开头"""
        with app.app_context():
            from app.services.token_rotation_service import TokenRotationService
            svc = TokenRotationService()
            token = svc.generate_token()
            assert token.startswith("fst_")
            assert len(token) > 40

    def test_hash_token(self, app):
        """Token 哈希应为 64 位十六进制"""
        with app.app_context():
            from app.services.token_rotation_service import TokenRotationService
            svc = TokenRotationService()
            h = svc.hash_token("test_token")
            assert len(h) == 64

    def test_calculate_expiry(self, app):
        """过期时间计算应正确"""
        with app.app_context():
            from app.services.token_rotation_service import TokenRotationService
            svc = TokenRotationService()
            exp_30 = svc.calculate_expiry("30d")
            exp_never = svc.calculate_expiry("never")
            assert exp_30 is not None
            assert exp_never is None

    def test_is_expiring_soon(self, app):
        """即将过期检查应正确"""
        with app.app_context():
            from app.services.token_rotation_service import TokenRotationService
            from datetime import datetime, timedelta
            svc = TokenRotationService()
            soon = datetime.utcnow() + timedelta(days=3)
            assert svc.is_expiring_soon(soon) is True
            not_soon = datetime.utcnow() + timedelta(days=30)
            assert svc.is_expiring_soon(not_soon) is False

    def test_rotate_token(self, app):
        """Token 轮换应返回新 Token"""
        with app.app_context():
            from app.services.token_rotation_service import TokenRotationService
            svc = TokenRotationService()
            result = svc.rotate_token()
            assert "token" in result
            assert "token_hash" in result
            assert result["token"].startswith("fst_")


class TestIPFilterService:
    """IP 白名单服务测试"""

    def test_empty_whitelist_allows_all(self, app):
        """空白名单应允许所有 IP"""
        with app.app_context():
            from app.services.ip_filter_service import IPFilterService
            svc = IPFilterService()
            assert svc.is_ip_allowed("192.168.1.1", []) is True

    def test_ip_in_whitelist(self, app):
        """白名单中的 IP 应被允许"""
        with app.app_context():
            from app.services.ip_filter_service import IPFilterService
            svc = IPFilterService()
            assert svc.is_ip_allowed("10.0.0.1", ["10.0.0.1", "10.0.0.2"]) is True

    def test_ip_not_in_whitelist(self, app):
        """不在白名单中的 IP 应被拒绝"""
        with app.app_context():
            from app.services.ip_filter_service import IPFilterService
            svc = IPFilterService()
            assert svc.is_ip_allowed("10.0.0.5", ["10.0.0.1", "10.0.0.2"]) is False

    def test_cidr_whitelist(self, app):
        """CIDR 白名单应匹配子网"""
        with app.app_context():
            from app.services.ip_filter_service import IPFilterService
            svc = IPFilterService()
            assert svc.is_ip_allowed("10.0.0.5", ["10.0.0.0/24"]) is True
            assert svc.is_ip_allowed("10.0.1.5", ["10.0.0.0/24"]) is False

    def test_validate_whitelist(self, app):
        """验证白名单应检测无效条目"""
        with app.app_context():
            from app.services.ip_filter_service import IPFilterService
            svc = IPFilterService()
            invalid = svc.validate_whitelist(["10.0.0.1", "not_an_ip", "10.0.0.0/24"])
            assert "not_an_ip" in invalid
            assert len(invalid) == 1


class TestDataMaskingService:
    """数据脱敏服务测试"""

    def test_mask_email(self, app):
        """邮箱应被脱敏"""
        with app.app_context():
            from app.services.data_masking_service import DataMaskingService
            svc = DataMaskingService()
            result = svc.mask_string("user@example.com")
            assert "***" in result
            assert "example.com" in result

    def test_mask_phone(self, app):
        """手机号应被脱敏"""
        with app.app_context():
            from app.services.data_masking_service import DataMaskingService
            svc = DataMaskingService()
            result = svc.mask_string("13812345678")
            assert "****" in result
            assert result.startswith("138")
            assert result.endswith("5678")

    def test_mask_dict_password(self, app):
        """字典中的密码字段应被脱敏"""
        with app.app_context():
            from app.services.data_masking_service import DataMaskingService
            svc = DataMaskingService()
            data = {"username": "test", "password": "secret123", "token": "abc"}
            result = svc.mask_dict(data)
            assert result["username"] == "test"
            assert result["password"] == "***"
            assert result["token"] == "***"

    def test_mask_dict_nested(self, app):
        """嵌套字典应递归脱敏"""
        with app.app_context():
            from app.services.data_masking_service import DataMaskingService
            svc = DataMaskingService()
            data = {"user": {"name": "test", "api_key": "secret"}}
            result = svc.mask_dict(data)
            assert result["user"]["api_key"] == "***"

    def test_mask_disabled(self, app):
        """禁用脱敏时应返回原文"""
        with app.app_context():
            import app.services.data_masking_service as dms
            original = dms.MASKING_ENABLED
            dms.MASKING_ENABLED = False
            svc = dms.DataMaskingService()
            assert svc.mask_string("test@example.com") == "test@example.com"
            dms.MASKING_ENABLED = original
