"""
报告模板引擎服务

提供可自定义的报告模板，支持多种输出格式。
"""

import json
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# 内置报告模板
BUILTIN_TEMPLATES = [
    {
        "id": "executive_summary",
        "name": "执行摘要",
        "description": "管理层看的简要报告",
        "sections": ["overview", "pass_rate", "key_metrics", "recommendations"],
    },
    {
        "id": "detailed_report",
        "name": "详细报告",
        "description": "测试团队看的详细报告",
        "sections": ["overview", "pass_rate", "case_details", "failure_analysis", "performance"],
    },
    {
        "id": "trend_analysis",
        "name": "趋势分析报告",
        "description": "质量团队看的趋势报告",
        "sections": ["overview", "trend_chart", "comparison", "recommendations"],
    },
    {
        "id": "cicd_integration",
        "name": "CI/CD 集成报告",
        "description": "研发团队看的集成报告",
        "sections": ["overview", "pass_rate", "failed_cases", "duration", "gate_status"],
    },
]


class ReportTemplateEngine:
    """报告模板引擎"""

    def get_templates(self) -> List[Dict[str, Any]]:
        """获取所有可用模板"""
        return BUILTIN_TEMPLATES

    def render_report(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据模板渲染报告

        Args:
            template_id: 模板 ID
            data: 报告数据

        Returns:
            Dict: 渲染后的报告
        """
        template = next((t for t in BUILTIN_TEMPLATES if t["id"] == template_id), None)
        if not template:
            raise ValueError(f"模板 {template_id} 不存在")

        report = {
            "template_id": template_id,
            "template_name": template["name"],
            "sections": {},
        }

        for section in template["sections"]:
            report["sections"][section] = self._render_section(section, data)

        return report

    def _render_section(self, section: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """渲染报告区块"""
        if section == "overview":
            return {
                "title": "概览",
                "project": data.get("project_name", ""),
                "generated_at": data.get("generated_at", ""),
            }
        elif section == "pass_rate":
            total = data.get("total_cases", 0)
            passed = data.get("passed", 0)
            return {
                "title": "通过率",
                "total": total,
                "passed": passed,
                "failed": data.get("failed", 0),
                "rate": round(passed / max(total, 1) * 100, 1),
            }
        elif section == "key_metrics":
            return {"title": "关键指标", "metrics": data.get("metrics", {})}
        elif section == "failure_analysis":
            return {"title": "失败分析", "failures": data.get("failures", [])}
        elif section == "performance":
            return {"title": "性能指标", "performance": data.get("performance", {})}
        else:
            return {"title": section, "data": data.get(section, {})}


_instance = None


def get_report_template_engine():
    global _instance
    if _instance is None: _instance = ReportTemplateEngine()
    return _instance
