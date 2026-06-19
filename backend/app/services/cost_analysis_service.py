"""
测试成本分析服务

量化测试执行的时间、资源和 AI Token 成本。
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from ..extensions import db
from ..models.test_run import TestRun
from ..models.ai_invocation_log import AIInvocationLog
from ..core.logging import get_logger

logger = get_logger(__name__)

# 默认人力单价（美元/小时）
DEFAULT_HOURLY_RATE = float(__import__("os").environ.get("TEST_HOURLY_RATE", "50"))


class CostAnalysisService:
    """测试成本分析服务"""

    def analyze_costs(self, project_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
        """
        分析测试执行成本

        Args:
            project_id: 限定项目
            days: 分析天数

        Returns:
            Dict: 成本分析结果
        """
        since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days)

        # 测试执行成本
        run_query = TestRun.query.filter(TestRun.created_at >= since)
        if project_id:
            run_query = run_query.filter_by(project_id=project_id)
        runs = run_query.all()

        total_duration_hours = sum((r.duration or 0) for r in runs) / 3600
        execution_cost = total_duration_hours * DEFAULT_HOURLY_RATE

        # AI Token 成本
        ai_query = AIInvocationLog.query.filter(AIInvocationLog.created_at >= since)
        ai_logs = ai_query.all()
        ai_cost = sum((l.cost_estimate or 0) for l in ai_logs)
        ai_tokens = sum((l.total_tokens or 0) for l in ai_logs)

        # 总成本
        total_cost = execution_cost + ai_cost

        return {
            "period_days": days,
            "total_cost": round(total_cost, 4),
            "execution_cost": round(execution_cost, 4),
            "ai_cost": round(ai_cost, 4),
            "test_runs": len(runs),
            "total_duration_hours": round(total_duration_hours, 2),
            "ai_calls": len(ai_logs),
            "ai_tokens": ai_tokens,
            "hourly_rate": DEFAULT_HOURLY_RATE,
        }


_instance = None


def get_cost_analysis_service():
    global _instance
    if _instance is None: _instance = CostAnalysisService()
    return _instance
