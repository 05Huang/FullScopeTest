"""
Flaky Test 检测服务测试
"""

import pytest


class TestFlakyDetectorService:
    """FlakyDetectorService 测试"""

    def test_detect_empty_project(self, app):
        """无用例时应返回空列表"""
        with app.app_context():
            from app.services.ai.flaky_detector_service import FlakyDetectorService
            svc = FlakyDetectorService()
            result = svc.detect_flaky_tests(project_id=99999)
            assert result == []

    def test_detect_with_cases(self, app, client):
        """有用例时应返回分析结果"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.ai.flaky_detector_service import FlakyDetectorService
            from datetime import datetime

            project = Project(name="Flaky测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            case = ApiTestCase(
                name="flaky case", method="GET", url="/api/flaky",
                project_id=project.id, user_id=1,
                last_status="passed", last_run_at=datetime.utcnow(),
            )
            db.session.add(case)
            db.session.commit()

            svc = FlakyDetectorService()
            result = svc.detect_flaky_tests(project_id=project.id, min_runs=1)
            assert len(result) > 0
            assert "flaky_score" in result[0]

    def test_flaky_report_structure(self, app):
        """报告应包含正确结构"""
        with app.app_context():
            from app.services.ai.flaky_detector_service import FlakyDetectorService
            svc = FlakyDetectorService()
            report = svc.get_flaky_report(project_id=99999)
            assert "total_analyzed" in report
            assert "suspected_flaky" in report
            assert "confirmed_flaky" in report
            assert "top_flaky" in report

    def test_analyze_case_stable(self, app):
        """稳定用例评分应为 0"""
        with app.app_context():
            from app.models.api_test_case import ApiTestCase
            from app.services.ai.flaky_detector_service import FlakyDetectorService
            from unittest.mock import MagicMock

            svc = FlakyDetectorService()
            case = MagicMock()
            case.id = 1
            case.name = "stable"
            case.url = "/api/test"
            case.method = "GET"
            case.last_status = "passed"
            case.last_result = None
            result = svc._analyze_case(case)
            assert result is not None
            assert result["flaky_score"] == 0.0
            assert result["category"] == "stable"

    def test_analyze_case_flaky(self, app):
        """频繁切换状态的用例应标记为 flaky"""
        with app.app_context():
            from app.services.ai.flaky_detector_service import FlakyDetectorService
            from unittest.mock import MagicMock

            svc = FlakyDetectorService()
            case = MagicMock()
            case.id = 2
            case.name = "flaky"
            case.url = "/api/flaky"
            case.method = "GET"
            case.last_status = "passed"
            case.last_result = {"history": ["passed", "failed", "passed", "failed", "passed"]}
            result = svc._analyze_case(case)
            assert result["flaky_score"] > 30
            assert result["category"] in ("suspected", "unstable")

    def test_analyze_case_no_status(self, app):
        """无执行记录的用例应返回 None"""
        with app.app_context():
            from app.services.ai.flaky_detector_service import FlakyDetectorService
            from unittest.mock import MagicMock

            svc = FlakyDetectorService()
            case = MagicMock()
            case.last_status = None
            result = svc._analyze_case(case)
            assert result is None
