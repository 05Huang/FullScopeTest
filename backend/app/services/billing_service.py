"""
计费服务

提供订阅管理、用量计量、账单生成功能。
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from ..extensions import db
from ..models.billing_plan import BillingPlan
from ..models.subscription import Subscription, UsageRecord
from ..core.logging import get_logger

logger = get_logger(__name__)


class BillingService:
    """计费服务"""

    def get_plans(self):
        """获取所有可用套餐"""
        return BillingPlan.query.filter_by(is_active=True).order_by(BillingPlan.sort_order).all()

    def get_plan_by_name(self, name: str) -> Optional[BillingPlan]:
        """按名称获取套餐"""
        return BillingPlan.query.filter_by(name=name, is_active=True).first()

    def get_subscription(self, organization_id: int) -> Optional[Subscription]:
        """获取组织的当前订阅"""
        return Subscription.query.filter_by(
            organization_id=organization_id,
            status='active',
        ).first()

    def get_or_create_free_subscription(self, organization_id: int) -> Subscription:
        """获取或创建免费订阅"""
        sub = self.get_subscription(organization_id)
        if sub:
            return sub

        free_plan = self.get_plan_by_name('free')
        if not free_plan:
            logger.error("Free plan not found, seeding default plans")
            from ..models.billing_plan import seed_default_plans
            seed_default_plans()
            free_plan = self.get_plan_by_name('free')

        sub = Subscription(
            organization_id=organization_id,
            plan_id=free_plan.id,
            status='active',
            billing_cycle='monthly',
            current_period_start=datetime.now(timezone.utc),
        )
        db.session.add(sub)
        db.session.commit()
        logger.info("Created free subscription", org_id=organization_id)
        return sub

    def upgrade_plan(self, organization_id: int, plan_name: str, billing_cycle: str = 'monthly') -> Subscription:
        """升级/变更套餐"""
        plan = self.get_plan_by_name(plan_name)
        if not plan:
            raise ValueError(f"Plan '{plan_name}' not found")

        sub = self.get_subscription(organization_id)
        if sub:
            sub.plan_id = plan.id
            sub.billing_cycle = billing_cycle
            sub.updated_at = datetime.now(timezone.utc)
        else:
            sub = Subscription(
                organization_id=organization_id,
                plan_id=plan.id,
                status='active',
                billing_cycle=billing_cycle,
                current_period_start=datetime.now(timezone.utc),
            )
            db.session.add(sub)

        db.session.commit()
        logger.info("Plan upgraded", org_id=organization_id, plan=plan_name)
        return sub

    def cancel_subscription(self, organization_id: int) -> Subscription:
        """取消订阅（降级到 Free）"""
        sub = self.get_subscription(organization_id)
        if not sub:
            raise ValueError("No active subscription found")

        sub.status = 'cancelled'
        sub.cancelled_at = datetime.now(timezone.utc)

        # 自动降级到 Free
        free_plan = self.get_plan_by_name('free')
        if free_plan:
            new_sub = Subscription(
                organization_id=organization_id,
                plan_id=free_plan.id,
                status='active',
                billing_cycle='monthly',
                current_period_start=datetime.now(timezone.utc),
            )
            db.session.add(new_sub)

        db.session.commit()
        logger.info("Subscription cancelled", org_id=organization_id)
        return sub

    def check_quota(self, organization_id: int, resource: str) -> Dict[str, Any]:
        """
        检查配额

        返回：
            allowed: 是否允许
            current: 当前使用量
            limit: 限额（-1 表示不限）
            plan_name: 当前套餐名
        """
        sub = self.get_subscription(organization_id)
        if not sub:
            sub = self.get_or_create_free_subscription(organization_id)

        plan = sub.plan
        now = datetime.now(timezone.utc)
        usage = UsageRecord.query.filter_by(
            organization_id=organization_id,
            year=now.year,
            month=now.month,
        ).first()

        resource_map = {
            'projects': ('projects_count', plan.max_projects),
            'test_cases': ('test_cases_count', plan.max_test_cases),
            'ai_calls': ('ai_calls_count', plan.max_ai_calls_monthly),
            'members': ('members_count', plan.max_members),
            'storage': ('storage_used_mb', plan.max_storage_mb),
        }

        if resource not in resource_map:
            return {'allowed': True, 'current': 0, 'limit': -1, 'plan_name': plan.name}

        attr, limit = resource_map[resource]
        current = getattr(usage, attr, 0) if usage else 0
        allowed = limit == -1 or current < limit

        return {
            'allowed': allowed,
            'current': current,
            'limit': limit,
            'plan_name': plan.name,
        }

    def record_usage(self, organization_id: int, resource: str, count: int = 1):
        """记录用量"""
        now = datetime.now(timezone.utc)
        usage = UsageRecord.query.filter_by(
            organization_id=organization_id,
            year=now.year,
            month=now.month,
        ).first()

        if not usage:
            usage = UsageRecord(
                organization_id=organization_id,
                year=now.year,
                month=now.month,
            )
            db.session.add(usage)

        attr_map = {
            'projects': 'projects_count',
            'test_cases': 'test_cases_count',
            'ai_calls': 'ai_calls_count',
            'members': 'members_count',
            'storage': 'storage_used_mb',
        }

        attr = attr_map.get(resource)
        if attr:
            current = getattr(usage, attr, 0)
            setattr(usage, attr, current + count)

        db.session.commit()


# 全局单例
billing_service = BillingService()
