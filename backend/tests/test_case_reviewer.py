"""
AI 用例质量审查服务测试
"""

import pytest


class TestCaseReviewerService:
    """CaseReviewerService 测试"""

    def test_review_case_not_found(self, app):
        """用例不存在应抛出异常"""
        with app.app_context():
            from app.services.ai.case_reviewer_service import CaseReviewerService
            from app.utils.exceptions import NotFoundError
            svc = CaseReviewerService()
            with pytest.raises(NotFoundError):
                svc.review_case(99999)

    def test_fallback_review_with_assertions(self, app):
        """有断言的用例降级评分应较高"""
        with app.app_context():
            from app.services.ai.case_reviewer_service import CaseReviewerService
            from unittest.mock import MagicMock

            svc = CaseReviewerService()
            case = MagicMock()
            case.id = 1
            case.name = "测试用户登录接口验证"
            case.assertions = [
                {"type": "status_code", "expected": 200},
                {"type": "json_path", "path": "$.token"},
                {"type": "response_time", "max": 1000},
            ]
            case.body = {"username": "test"}
            case.description = "测试登录"
            case.method = "POST"
            case.url = "/api/login"
            case.headers = None
            result = svc._fallback_review(case)
            assert result["score"] > 50
            assert "assertions" in result["dimensions"]

    def test_fallback_review_no_assertions(self, app):
        """无断言的用例降级评分应较低"""
        with app.app_context():
            from app.services.ai.case_reviewer_service import CaseReviewerService
            from unittest.mock import MagicMock

            svc = CaseReviewerService()
            case = MagicMock()
            case.id = 2
            case.name = "test"
            case.assertions = None
            case.body = None
            case.description = None
            case.method = "GET"
            case.url = "/api/test"
            case.headers = None
            result = svc._fallback_review(case)
            assert result["score"] <= 60

    def test_case_to_text(self, app):
        """用例转文本应包含关键信息"""
        with app.app_context():
            from app.services.ai.case_reviewer_service import CaseReviewerService
            from unittest.mock import MagicMock

            svc = CaseReviewerService()
            case = MagicMock()
            case.name = "登录测试"
            case.method = "POST"
            case.url = "/api/login"
            case.description = "测试登录功能"
            case.headers = None
            case.body = None
            case.assertions = [{"type": "status_code"}]
            text = svc._case_to_text(case)
            assert "登录测试" in text
            assert "POST" in text

    def test_review_collection_not_found(self, app):
        """用例集不存在应抛出异常"""
        with app.app_context():
            from app.services.ai.case_reviewer_service import CaseReviewerService
            from app.utils.exceptions import NotFoundError
            svc = CaseReviewerService()
            with pytest.raises(NotFoundError):
                svc.review_collection(99999)
