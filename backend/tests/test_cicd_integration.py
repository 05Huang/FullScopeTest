"""
CI/CD 深度集成测试（PR 评论 + CI/CD 指标）
"""

import pytest


class TestPRCommentService:
    """PR 评论服务测试"""

    def test_format_results_comment(self, app):
        """格式化测试结果评论"""
        with app.app_context():
            from app.services.pr_comment_service import PRCommentService
            svc = PRCommentService()
            results = {"total": 20, "passed": 18, "failed": 2, "pass_rate": 90.0, "duration": 125.5}
            comment = svc.format_test_results_comment(results)
            assert "90.0%" in comment
            assert "20" in comment
            assert "2" in comment
            assert "125.5s" in comment

    def test_format_all_passed(self, app):
        """全部通过时应显示绿色图标"""
        with app.app_context():
            from app.services.pr_comment_service import PRCommentService
            svc = PRCommentService()
            results = {"total": 10, "passed": 10, "failed": 0, "pass_rate": 100.0, "duration": 50.0}
            comment = svc.format_test_results_comment(results)
            assert "✅" in comment  # green checkmark

    def test_format_with_failures(self, app):
        """有失败时应显示红色图标"""
        with app.app_context():
            from app.services.pr_comment_service import PRCommentService
            svc = PRCommentService()
            results = {"total": 10, "passed": 8, "failed": 2, "pass_rate": 80.0, "duration": 60.0}
            comment = svc.format_test_results_comment(results)
            assert "❌" in comment  # red X

    def test_no_token_returns_false(self, app):
        """无 Token 时应返回 False"""
        with app.app_context():
            from app.services.pr_comment_service import PRCommentService
            svc = PRCommentService(token="")
            assert svc.add_comment("owner/repo", 1, "test") is False

    def test_format_with_report_url(self, app):
        """包含报告链接"""
        with app.app_context():
            from app.services.pr_comment_service import PRCommentService
            svc = PRCommentService()
            results = {"total": 5, "passed": 5, "failed": 0, "pass_rate": 100.0, "duration": 30.0, "report_url": "https://example.com/report/1"}
            comment = svc.format_test_results_comment(results)
            assert "https://example.com/report/1" in comment


class TestCICDMetricsService:
    """CI/CD 指标服务测试"""

    def test_get_metrics_empty(self, app):
        """无数据时应返回空指标"""
        with app.app_context():
            from app.services.cicd_metrics_service import CICDMetricsService
            svc = CICDMetricsService()
            metrics = svc.get_metrics(project_id=99999)
            assert metrics["total_runs"] == 0
            assert metrics["ci_runs"] == 0

    def test_get_metrics_structure(self, app):
        """指标应包含所有字段"""
        with app.app_context():
            from app.services.cicd_metrics_service import CICDMetricsService
            svc = CICDMetricsService()
            metrics = svc.get_metrics()
            assert "total_runs" in metrics
            assert "ci_runs" in metrics
            assert "ci_pass_rate" in metrics
            assert "avg_duration_seconds" in metrics
            assert "by_day" in metrics
