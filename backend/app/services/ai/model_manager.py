"""
AI 模型管理与成本控制服务

统一管理 AI 模型调用，提供：
- 模型路由：按功能选择最优模型
- 模型降级链：主模型不可用时自动切换备用模型
- Token 用量统计：按用户/功能/天统计
- 成本预算：月度 Token 预算控制
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from ...extensions import db
from ...models.ai_invocation_log import AIInvocationLog
from ...core.logging import get_logger

logger = get_logger(__name__)

# 模型配置：功能 -> 模型映射
MODEL_ROUTING = {
    "copilot": "gpt-4o-mini",
    "script_gen": "gpt-4o-mini",
    "swagger_gen": "gpt-4o-mini",
    "dedup": "gpt-4o-mini",
    "nl_test_creation": "gpt-4o-mini",
    "case_healing": "gpt-4o-mini",
    "root_cause_analysis": "gpt-4o-mini",
    "general": "gpt-4o-mini",
}

# 模型降级链
FALLBACK_CHAIN = [
    "gpt-4o-mini",
    "gpt-4o",
    "deepseek-chat",
]

# 模型定价（美元/1M tokens）
MODEL_PRICING = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "deepseek-chat": {"input": 0.14, "output": 0.28},
}


class ModelManager:
    """AI 模型管理器"""

    def __init__(self):
        self.monthly_budget = float(os.environ.get("AI_MONTHLY_BUDGET", "100.0"))
        self.budget_warning_threshold = float(os.environ.get("AI_BUDGET_WARNING", "0.8"))

    def get_model_for_feature(self, feature: str) -> str:
        """获取功能对应的模型"""
        return MODEL_ROUTING.get(feature, MODEL_ROUTING["general"])

    def check_budget(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        检查月度预算使用情况

        Returns:
            Dict: {used, budget, remaining, percentage, exceeded}
        """
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        from sqlalchemy import func as sa_func
        query = db.session.query(
            sa_func.sum(AIInvocationLog.cost_estimate)
        ).filter(
            AIInvocationLog.created_at >= month_start,
        )
        if user_id:
            query = query.filter_by(user_id=user_id)

        used = query.scalar() or 0.0
        remaining = max(self.monthly_budget - used, 0)
        percentage = (used / self.monthly_budget * 100) if self.monthly_budget > 0 else 0

        return {
            "used": round(used, 4),
            "budget": self.monthly_budget,
            "remaining": round(remaining, 4),
            "percentage": round(percentage, 1),
            "exceeded": used >= self.monthly_budget,
            "warning": percentage >= self.budget_warning_threshold * 100,
        }

    def get_usage_stats(
        self,
        days: int = 30,
        user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        获取 Token 用量统计

        Args:
            days: 统计天数
            user_id: 限定用户

        Returns:
            Dict: 统计信息
        """
        since = datetime.utcnow() - timedelta(days=days)

        query = AIInvocationLog.query.filter(AIInvocationLog.created_at >= since)
        if user_id:
            query = query.filter_by(user_id=user_id)

        logs = query.all()

        total_tokens = sum(l.total_tokens or 0 for l in logs)
        total_cost = sum(l.cost_estimate or 0 for l in logs)
        total_calls = len(logs)
        success_calls = sum(1 for l in logs if l.success)

        # 按功能分组
        by_feature = {}
        for l in logs:
            f = l.feature or "unknown"
            if f not in by_feature:
                by_feature[f] = {"calls": 0, "tokens": 0, "cost": 0.0, "errors": 0}
            by_feature[f]["calls"] += 1
            by_feature[f]["tokens"] += l.total_tokens or 0
            by_feature[f]["cost"] += l.cost_estimate or 0
            if not l.success:
                by_feature[f]["errors"] += 1

        # 按天分组
        by_day = {}
        for l in logs:
            day = l.created_at.strftime("%Y-%m-%d") if l.created_at else "unknown"
            if day not in by_day:
                by_day[day] = {"calls": 0, "tokens": 0, "cost": 0.0}
            by_day[day]["calls"] += 1
            by_day[day]["tokens"] += l.total_tokens or 0
            by_day[day]["cost"] += l.cost_estimate or 0

        return {
            "period_days": days,
            "total_calls": total_calls,
            "success_calls": success_calls,
            "error_calls": total_calls - success_calls,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 4),
            "avg_tokens_per_call": round(total_tokens / max(total_calls, 1)),
            "by_feature": by_feature,
            "by_day": dict(sorted(by_day.items())),
        }

    def get_model_status(self) -> List[Dict[str, Any]]:
        """获取所有模型状态"""
        models = []
        for name, pricing in MODEL_PRICING.items():
            models.append({
                "name": name,
                "pricing": pricing,
                "is_primary": name == MODEL_ROUTING.get("general"),
            })
        return models


_instance = None


def get_model_manager() -> ModelManager:
    global _instance
    if _instance is None:
        _instance = ModelManager()
    return _instance
