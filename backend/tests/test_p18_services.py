"""
P18 报告与分析增强测试
"""

import pytest


class TestReportTemplateEngine:
    """报告模板引擎测试"""

    def test_get_templates(self, app):
        """应返回内置模板列表"""
        with app.app_context():
            from app.services.report_template_engine import ReportTemplateEngine
            engine = ReportTemplateEngine()
            templates = engine.get_templates()
            assert len(templates) >= 4
            assert all("id" in t and "name" in t for t in templates)

    def test_render_executive_summary(self, app):
        """渲染执行摘要模板"""
        with app.app_context():
            from app.services.report_template_engine import ReportTemplateEngine
            engine = ReportTemplateEngine()
            data = {"project_name": "Test", "total_cases": 100, "passed": 95, "failed": 5}
            report = engine.render_report("executive_summary", data)
            assert report["template_id"] == "executive_summary"
            assert "overview" in report["sections"]
            assert "pass_rate" in report["sections"]

    def test_render_pass_rate_section(self, app):
        """通过率区块应正确计算"""
        with app.app_context():
            from app.services.report_template_engine import ReportTemplateEngine
            engine = ReportTemplateEngine()
            data = {"total_cases": 200, "passed": 180, "failed": 20}
            report = engine.render_report("executive_summary", data)
            pass_rate = report["sections"]["pass_rate"]
            assert pass_rate["rate"] == 90.0
            assert pass_rate["total"] == 200

    def test_render_unknown_template(self, app):
        """未知模板应抛出异常"""
        with app.app_context():
            from app.services.report_template_engine import ReportTemplateEngine
            engine = ReportTemplateEngine()
            with pytest.raises(ValueError):
                engine.render_report("nonexistent", {})


class TestSLAService:
    """SLA 服务测试"""

    def test_sla_all_pass(self, app):
        """全部达标应返回 ok"""
        with app.app_context():
            from app.services.sla_service import SLAService
            svc = SLAService()
            metrics = {"api_pass_rate": 96.0, "web_pass_rate": 92.0, "perf_p95_ms": 1500, "availability": 99.95}
            result = svc.evaluate_sla(metrics)
            assert result["overall_status"] == "ok"

    def test_sla_violation(self, app):
        """未达标应返回 violation"""
        with app.app_context():
            from app.services.sla_service import SLAService
            svc = SLAService()
            metrics = {"api_pass_rate": 80.0, "web_pass_rate": 92.0, "perf_p95_ms": 1500, "availability": 99.95}
            result = svc.evaluate_sla(metrics)
            assert result["overall_status"] == "violation"
            assert result["checks"]["api_pass_rate"]["passed"] is False

    def test_sla_warning(self, app):
        """接近阈值应标记为 warning"""
        with app.app_context():
            from app.services.sla_service import SLAService
            svc = SLAService()
            metrics = {"api_pass_rate": 93.0, "web_pass_rate": 92.0, "perf_p95_ms": 1500, "availability": 99.95}
            result = svc.evaluate_sla(metrics)
            assert result["checks"]["api_pass_rate"]["status"] == "warning"


class TestCostAnalysisService:
    """成本分析服务测试"""

    def test_analyze_empty(self, app):
        """无数据时应返回零成本"""
        with app.app_context():
            from app.services.cost_analysis_service import CostAnalysisService
            svc = CostAnalysisService()
            result = svc.analyze_costs(project_id=99999)
            assert result["total_cost"] == 0
            assert result["test_runs"] == 0

    def test_analyze_structure(self, app):
        """结果应包含所有字段"""
        with app.app_context():
            from app.services.cost_analysis_service import CostAnalysisService
            svc = CostAnalysisService()
            result = svc.analyze_costs()
            assert "total_cost" in result
            assert "execution_cost" in result
            assert "ai_cost" in result
            assert "hourly_rate" in result
