"""
智能选测服务测试
"""

import pytest


class TestTestSelectorService:
    """TestSelectorService 测试"""

    def test_select_empty_files(self, app):
        """无变更文件应返回空结果"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            result = svc.select_tests([])
            assert result["cases"] == []
            assert result["total_estimated_time"] == 0

    def test_map_api_files(self, app):
        """API 文件应映射到对应路径"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            paths = svc._map_files_to_paths(["app/api/auth.py", "app/api/projects.py"])
            assert "/api/v1/auth" in paths
            assert "/api/v1/projects" in paths

    def test_map_model_files(self, app):
        """模型文件变更应标记为 __all__"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            paths = svc._map_files_to_paths(["app/models/user.py"])
            assert "__all__" in paths

    def test_map_unknown_files(self, app):
        """未知文件应提取关键词"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            paths = svc._map_files_to_paths(["src/utils/helper.py"])
            assert "helper" in paths

    def test_select_with_cases(self, app, client):
        """有用例时应返回匹配结果"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.ai.test_selector_service import TestSelectorService

            project = Project(name="Selector测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            case = ApiTestCase(
                name="auth login", method="POST", url="/api/v1/auth/login",
                project_id=project.id, user_id=1, priority="P0",
            )
            db.session.add(case)
            db.session.commit()

            svc = TestSelectorService()
            result = svc.select_tests(
                ["app/api/auth.py"],
                project_id=project.id,
            )
            assert len(result["cases"]) > 0
            assert "match_reason" in result["cases"][0]

    def test_score_priority(self, app):
        """高优先级用例应获得更高分数"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            cases = [
                {"case": {"priority": "P0", "last_status": "failed"}, "score": 1.0, "estimated_time": 5},
                {"case": {"priority": "P3", "last_status": "passed"}, "score": 1.0, "estimated_time": 5},
            ]
            scored = svc._apply_scores(cases)
            assert scored[0]["score"] > scored[1]["score"]

    def test_reasoning_output(self, app):
        """选测理由应包含关键信息"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            reasoning = svc._build_reasoning(
                ["a.py", "b.py"],
                {"/api/v1/test"},
                [{"case": {}}],
            )
            assert "2" in reasoning
            assert "1" in reasoning

    def test_max_cases_limit(self, app, client):
        """max_cases 应限制返回数量"""
        with app.app_context():
            from app.services.ai.test_selector_service import TestSelectorService
            svc = TestSelectorService()
            result = svc.select_tests(["app/api/auth.py"], max_cases=1)
            assert len(result["cases"]) <= 1
