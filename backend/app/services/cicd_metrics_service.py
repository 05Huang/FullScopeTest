"""
CI/CD 指标服务

提供 CI/CD 集成的统计和度量能力。
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..extensions import db
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)


class CICDMetricsService:
    """CI/CD 指标服务"""

    def get_metrics(self, project_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
        """
        获取 CI/CD 指标

        Args:
            project_id: 限定项目
            days: 统计天数

        Returns:
            Dict: CI/CD 指标
        """
        since = datetime.utcnow() - timedelta(days=days)
        query = TestRun.query.filter(TestRun.created_at >= since)
        if project_id:
            query = query.filter_by(project_id=project_id)

        runs = query.all()
        total_runs = len(runs)
        if total_runs == 0:
            return self._empty_metrics(days)

        # CI/CD 触发的执行
        ci_runs = [r for r in runs if r.triggered_by in ("github_actions", "webhook", "schedule")]
        ci_total = len(ci_runs)
        ci_passed = sum(1 for r in ci_runs if r.status == "success")
        ci_failed = sum(1 for r in ci_runs if r.status == "failed")

        # 手动触发的执行
        manual_runs = [r for r in runs if r.triggered_by == "manual"]

        # 平均执行时长
        durations = [r.duration for r in runs if r.duration and r.duration > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # 按天分组
        by_day = {}
        for r in runs:
            day = r.created_at.strftime("%Y-%m-%d") if r.created_at else "unknown"
            if day not in by_day:
                by_day[day] = {"runs": 0, "passed": 0, "failed": 0}
            by_day[day]["runs"] += 1
            if r.status == "success":
                by_day[day]["passed"] += 1
            elif r.status == "failed":
                by_day[day]["failed"] += 1

        return {
            "period_days": days,
            "total_runs": total_runs,
            "ci_runs": ci_total,
            "ci_passed": ci_passed,
            "ci_failed": ci_failed,
            "ci_pass_rate": round(ci_passed / max(ci_total, 1) * 100, 1),
            "manual_runs": len(manual_runs),
            "avg_duration_seconds": round(avg_duration, 1),
            "by_day": dict(sorted(by_day.items())),
        }

    def _empty_metrics(self, days):
        return {"period_days": days, "total_runs": 0, "ci_runs": 0, "ci_pass_rate": 0, "manual_runs": 0, "avg_duration_seconds": 0, "by_day": {}}


_instance = None


def get_cicd_metrics_service():
    global _instance
    if _instance is None: _instance = CICDMetricsService()
    return _instance
