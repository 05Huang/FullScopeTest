"""
多租户资源配额服务

管理组织级别的资源配额：初始化、查询、消耗、释放。

默认配额计划：
- free:       5 项目，100 用例，1 并行，100 AI/月，500MB 存储
- pro:       50 项目，1000 用例，5 并行，5000 AI/月，5GB 存储
- enterprise: 不限（limit=-1）
"""
import os
from typing import Optional
from ..extensions import db
from ..models.quota import Quota
from ..core.logging import get_logger

logger = get_logger(__name__)

# 默认配额计划
DEFAULT_PLANS = {
    'free': {
        'projects': 5,
        'test_cases': 100,
        'parallel_executions': 1,
        'ai_calls_monthly': 100,
        'storage_mb': 500,
    },
    'pro': {
        'projects': 50,
        'test_cases': 1000,
        'parallel_executions': 5,
        'ai_calls_monthly': 5000,
        'storage_mb': 5120,
    },
    'enterprise': {
        'projects': -1,
        'test_cases': -1,
        'parallel_executions': -1,
        'ai_calls_monthly': -1,
        'storage_mb': -1,
    },
}


def init_quota_for_organization(organization_id: int, plan: str = 'free'):
    """
    为组织初始化默认配额

    Args:
        organization_id: 组织 ID
        plan: 计划类型（free/pro/enterprise）
    """
    plan_config = DEFAULT_PLANS.get(plan, DEFAULT_PLANS['free'])

    for resource_type, limit in plan_config.items():
        existing = Quota.query.filter_by(
            organization_id=organization_id,
            resource_type=resource_type,
        ).first()
        if not existing:
            quota = Quota(
                organization_id=organization_id,
                resource_type=resource_type,
                limit=limit,
                used=0,
                plan=plan,
            )
            db.session.add(quota)

    db.session.commit()
    logger.info("组织配额已初始化", organization_id=organization_id, plan=plan)


def get_quota(organization_id: int, resource_type: str) -> Optional[Quota]:
    """获取指定组织的资源配额"""
    return Quota.query.filter_by(
        organization_id=organization_id,
        resource_type=resource_type,
    ).first()


def get_all_quotas(organization_id: int) -> list:
    """获取组织的所有配额"""
    quotas = Quota.query.filter_by(organization_id=organization_id).all()
    return [q.to_dict() for q in quotas]


def check_quota(organization_id: int, resource_type: str, amount: int = 1) -> bool:
    """
    检查配额是否足够

    Args:
        organization_id: 组织 ID
        resource_type: 资源类型
        amount: 请求量

    Returns:
        True 表示配额充足
    """
    quota = get_quota(organization_id, resource_type)
    if not quota:
        # 未配置配额时默认允许（向后兼容）
        return True
    if quota.limit == -1:
        return True  # 不限量
    return (quota.used + amount) <= quota.limit


def consume_quota(organization_id: int, resource_type: str, amount: int = 1) -> bool:
    """
    消耗配额

    Args:
        organization_id: 组织 ID
        resource_type: 资源类型
        amount: 消耗量

    Returns:
        True 表示消耗成功，False 表示配额不足
    """
    quota = get_quota(organization_id, resource_type)
    if not quota:
        return True  # 未配置配额时允许
    if quota.limit == -1:
        quota.used += amount
        db.session.commit()
        return True
    if (quota.used + amount) > quota.limit:
        logger.warning("配额不足",
                       organization_id=organization_id,
                       resource_type=resource_type,
                       used=quota.used, limit=quota.limit, requested=amount)
        return False
    quota.used += amount
    db.session.commit()
    return True


def release_quota(organization_id: int, resource_type: str, amount: int = 1):
    """
    释放配额（删除资源时调用）

    Args:
        organization_id: 组织 ID
        resource_type: 资源类型
        amount: 释放量
    """
    quota = get_quota(organization_id, resource_type)
    if quota:
        quota.used = max(0, quota.used - amount)
        db.session.commit()


def update_quota(organization_id: int, resource_type: str, limit: int, plan: str = None):
    """
    管理员修改配额

    Args:
        organization_id: 组织 ID
        resource_type: 资源类型
        limit: 新上限（-1 表示不限）
        plan: 计划类型（可选）
    """
    quota = get_quota(organization_id, resource_type)
    if quota:
        quota.limit = limit
        if plan:
            quota.plan = plan
    else:
        quota = Quota(
            organization_id=organization_id,
            resource_type=resource_type,
            limit=limit,
            used=0,
            plan=plan or 'custom',
        )
        db.session.add(quota)
    db.session.commit()
    logger.info("配额已更新", organization_id=organization_id,
                resource_type=resource_type, limit=limit)
