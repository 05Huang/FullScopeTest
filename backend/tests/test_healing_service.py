"""
AI 用例自愈服务测试
"""

import pytest
from unittest.mock import patch, MagicMock


class TestHealingService:
    """HealingService 测试"""

    def test_heal_case_not_found(self, app):
        """用例不存在应抛出 NotFoundError"""
        with app.app_context():
            from app.services.ai.healing_service import HealingService
            from app.utils.exceptions import NotFoundError
            svc = HealingService()
            with pytest.raises(NotFoundError):
                svc.heal_case(99999, {"status_code": 404})

    def test_heal_case_with_mock_ai(self, app, client):
        """自愈应返回包含修复建议的结构"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.ai.healing_service import HealingService

            project = Project(name="Heal测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            case = ApiTestCase(
                name="登录测试", method="POST", url="/api/login",
                project_id=project.id, user_id=1,
                assertions=[{"type": "status_code", "expected": 200}],
            )
            db.session.add(case)
            db.session.commit()

            svc = HealingService()
            # Mock AI 返回
            mock_response = {
                "role": "assistant",
                "content": '{"failure_reason": "path_changed", "analysis": "URL 变更", "fixes": [{"field": "url", "current": "/api/login", "suggested": "/api/v2/login", "reason": "路径升级"}], "confidence": 0.85}',
            }
            with patch.object(svc, 'simple_chat', return_value=mock_response):
                result = svc.heal_case(
                    case.id,
                    {"status_code": 404, "error_message": "Not Found"},
                    user_id=1,
                )
            assert "case_id" in result
            assert result["case_id"] == case.id
            assert result["failure_reason"] == "path_changed"

    def test_apply_fix(self, app, client):
        """应用修复应更新用例字段"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.ai.healing_service import HealingService

            project = Project(name="Fix测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            case = ApiTestCase(
                name="旧用例", method="GET", url="/api/old",
                project_id=project.id, user_id=1,
            )
            db.session.add(case)
            db.session.commit()
            case_id = case.id

            svc = HealingService()
            result = svc.apply_fix(
                case_id,
                [{"field": "url", "suggested": "/api/new", "reason": "路径变更"}],
                user_id=1,
            )
            assert result.get("case_id") == case_id
            assert "/api/new" in str(result.get("updated_case", {}))

    def test_parse_suggestion_json(self, app):
        """解析 AI 返回的 JSON 建议"""
        with app.app_context():
            from app.services.ai.healing_service import HealingService
            svc = HealingService()
            content = '{"failure_reason": "path_changed", "analysis": "URL 变更", "fixes": [], "confidence": 0.9}'
            result = svc._parse_suggestion(content, 1)
            assert result["failure_reason"] == "path_changed"
            assert result["case_id"] == 1

    def test_parse_suggestion_with_codeblock(self, app):
        """解析带代码块的 AI 返回"""
        with app.app_context():
            from app.services.ai.healing_service import HealingService
            svc = HealingService()
            content = '分析如下:\n```json\n{"failure_reason": "status_changed", "analysis": "状态码变更", "fixes": [], "confidence": 0.8}\n```'
            result = svc._parse_suggestion(content, 2)
            assert result["failure_reason"] == "status_changed"

    def test_parse_suggestion_invalid_json(self, app):
        """无效 JSON 应返回降级结果"""
        with app.app_context():
            from app.services.ai.healing_service import HealingService
            svc = HealingService()
            result = svc._parse_suggestion("这不是 JSON", 3)
            assert result["failure_reason"] == "unknown"
            assert result["confidence"] == 0.3

    def test_heal_collection_not_found(self, app):
        """用例集不存在应抛出异常"""
        with app.app_context():
            from app.services.ai.healing_service import HealingService
            from app.utils.exceptions import NotFoundError
            svc = HealingService()
            with pytest.raises(NotFoundError):
                svc.heal_collection(99999, [{"case_id": 1, "failure_info": {}}])

    def test_case_to_text(self, app):
        """用例转文本应包含关键信息"""
        with app.app_context():
            from app.models.api_test_case import ApiTestCase
            from app.services.ai.healing_service import HealingService
            svc = HealingService()
            case = MagicMock()
            case.name = "测试"
            case.method = "GET"
            case.url = "/api/test"
            case.assertions = None
            text = svc._case_to_text(case)
            assert "GET" in text
            assert "/api/test" in text
