"""
配额执行服务

在所有写操作前检查配额，确保不超过订阅限制。
"""

import os
from typing import Dict, Any, Optional
from ..extensions import db
from ..models.quota import Quota
from ..core.logging import get_logger

logger = get_logger(__name__)

# 默认配额计划
DEFAULT_PLANS = {
    "free": {"projects": 5, "test_cases": 100, "parallel_executions": 1, "ai_calls_monthly": 100, "storage_mb": 500},
    "pro": {"projects": 50, "test_cases": 1000, "parallel_executions": 5, "ai_calls_monthly": 5000, "storage_mb": 5120},
    "enterprise": {"projects": -1, "test_cases": -1, "parallel_executions": 20, "ai_calls_monthly": -1, "storage_mb": -1},
}

# 配额预警阈值
WARNING_THRESHOLD = 0.8  # 80%


class QuotaExceededError(Exception):
    """配额超限异常"""

    def __init__(self, resource_type: str, current: int, limit: int):
        self.resource_type = resource_type
        self.current = current
        self.limit = limit
        super().__init__(f"配额不足: {resource_type} 已使用 {current}/{limit}")


class QuotaService:
    """配额执行服务"""

    def check_quota(self, org_id: int, resource_type: str, amount: int = 1) -> bool:
        """
        检查配额是否足够

        Args:
            org_id: 组织 ID
            resource_type: 资源类型
            amount: 请求的数量

        Returns:
            bool: 配额是否足够

        Raises:
            QuotaExceededError: 配额不足时抛出
        """
        quota = Quota.query.filter_by(
            organization_id=org_id, resource_type=resource_type,
        ).first()

        if quota is None:
            # 无配额记录，使用默认计划
            return True

        limit = quota.limit
        used = quota.used

        # -1 表示无限制
        if limit == -1:
            return True

        if used + amount > limit:
            raise QuotaExceededError(resource_type, used, limit)

        # 配额预警
        if (used + amount) / limit >= WARNING_THRESHOLD:
            logger.warning("配额预警", org_id=org_id, resource=resource_type, used=used, limit=limit)

        return True

    def consume_quota(self, org_id: int, resource_type: str, amount: int = 1) -> Dict[str, Any]:
        """
        消耗配额（原子操作）

        Args:
            org_id: 组织 ID
            resource_type: 资源类型
            amount: 消耗数量

        Returns:
            Dict: 配额使用情况
        """
        # 先检查
        self.check_quota(org_id, resource_type, amount)

        # 更新配额
        quota = Quota.query.filter_by(
            organization_id=org_id, resource_type=resource_type,
        ).first()

        if quota:
            quota.used += amount
            db.session.commit()
            return {"used": quota.used, "limit": quota.limit, "remaining": max(quota.limit - quota.used, 0)}

        return {"used": amount, "limit": -1, "remaining": -1}

    def get_quota_usage(self, org_id: int) -> Dict[str, Any]:
        """获取组织的所有配额使用情况"""
        quotas = Quota.query.filter_by(organization_id=org_id).all()
        result = {}
        for q in quotas:
            result[q.resource_type] = {
                "used": q.used,
                "limit": q.limit,
                "remaining": max(q.limit - q.used, 0) if q.limit != -1 else -1,
                "percentage": round(q.used / q.limit * 100, 1) if q.limit > 0 else 0,
            }
        return result

    def reset_monthly_quota(self, org_id: int, resource_type: str):
        """重置月度配额"""
        quota = Quota.query.filter_by(
            organization_id=org_id, resource_type=resource_type,
        ).first()
        if quota:
            quota.used = 0
            db.session.commit()
            logger.info("月度配额已重置", org_id=org_id, resource=resource_type)


_instance = None


def get_quota_service():
    global _instance
    if _instance is None: _instance = QuotaService()
    return _instance
