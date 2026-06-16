"""
AI 失败根因分析服务测试
"""

import pytest


class TestRootCauseService:
    """RootCauseService 测试"""

    def test_analyze_empty_failures(self, app):
        """空失败列表应返回空报告"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            result = svc.analyze_failures([])
            assert result["summary"]["total_failed"] == 0
            assert result["categories"] == []

    def test_fallback_classify_404(self, app):
        """404 应归类为 api_changed"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            failures = [
                {"case_name": "test1", "status_code": 404, "url": "/api/test", "method": "GET"},
            ]
            result = svc._fallback_classify(failures)
            assert result["summary"]["total_failed"] == 1
            assert result["categories"][0]["reason"] == "api_changed"

    def test_fallback_classify_401(self, app):
        """401 应归类为 auth_expired"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            failures = [
                {"case_name": "test2", "status_code": 401, "url": "/api/auth", "method": "POST"},
            ]
            result = svc._fallback_classify(failures)
            assert result["categories"][0]["reason"] == "auth_expired"

    def test_fallback_classify_500(self, app):
        """500 应归类为 bug"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            failures = [
                {"case_name": "test3", "status_code": 500, "url": "/api/crash", "method": "GET"},
            ]
            result = svc._fallback_classify(failures)
            assert result["categories"][0]["reason"] == "bug"

    def test_fallback_classify_timeout(self, app):
        """超时应归类为 timeout"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            failures = [
                {"case_name": "test4", "status_code": 0, "error_message": "Request timeout", "url": "/api/slow", "method": "GET"},
            ]
            result = svc._fallback_classify(failures)
            assert result["categories"][0]["reason"] == "timeout"

    def test_fallback_classify_multiple(self, app):
        """多个失败应正确分类和聚合"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            failures = [
                {"case_name": "t1", "status_code": 404, "url": "/a", "method": "GET"},
                {"case_name": "t2", "status_code": 404, "url": "/b", "method": "GET"},
                {"case_name": "t3", "status_code": 500, "url": "/c", "method": "GET"},
            ]
            result = svc._fallback_classify(failures)
            assert result["summary"]["total_failed"] == 3
            assert len(result["categories"]) == 2

    def test_build_failure_text(self, app):
        """构建的文本应包含关键信息"""
        with app.app_context():
            from app.services.ai.root_cause_service import RootCauseService
            svc = RootCauseService()
            failures = [
                {"case_name": "login", "status_code": 401, "url": "/api/login", "method": "POST", "error_message": "Unauthorized"},
            ]
            text = svc._build_failure_text(failures)
            assert "login" in text
            assert "401" in text
