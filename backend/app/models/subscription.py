"""
订阅模型

记录组织的订阅信息
"""
from datetime import datetime
from ..extensions import db


class Subscription(db.Model):
    """订阅表"""
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, comment='组织 ID')
    plan_id = db.Column(db.Integer, db.ForeignKey('billing_plans.id'), nullable=False, comment='套餐 ID')
    status = db.Column(db.String(20), default='active', comment='状态：active/cancelled/expired/paused')
    billing_cycle = db.Column(db.String(10), default='monthly', comment='计费周期：monthly/yearly')

    # 订阅时间
    started_at = db.Column(db.DateTime, default=datetime.utcnow, comment='开始时间')
    current_period_start = db.Column(db.DateTime, comment='当前计费周期开始')
    current_period_end = db.Column(db.DateTime, comment='当前计费周期结束')
    cancelled_at = db.Column(db.DateTime, comment='取消时间')

    # 支付信息
    payment_method = db.Column(db.String(50), comment='支付方式：stripe/alipay/wechat')
    external_subscription_id = db.Column(db.String(255), comment='外部订阅 ID（Stripe 等）')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    organization = db.relationship('Organization', backref='subscription')
    plan = db.relationship('BillingPlan', backref='subscriptions')

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'plan_id': self.plan_id,
            'plan_name': self.plan.name if self.plan else None,
            'plan_display_name': self.plan.display_name if self.plan else None,
            'status': self.status,
            'billing_cycle': self.billing_cycle,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'payment_method': self.payment_method,
        }


class UsageRecord(db.Model):
    """用量记录表 — 按月统计各项资源使用量"""
    __tablename__ = 'usage_records'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False, comment='年份')
    month = db.Column(db.Integer, nullable=False, comment='月份')

    projects_count = db.Column(db.Integer, default=0, comment='项目数')
    test_cases_count = db.Column(db.Integer, default=0, comment='用例数')
    ai_calls_count = db.Column(db.Integer, default=0, comment='AI 调用次数')
    storage_used_mb = db.Column(db.Float, default=0, comment='已用存储（MB）')
    members_count = db.Column(db.Integer, default=0, comment='成员数')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('organization_id', 'year', 'month', name='uq_usage_org_period'),
    )

    def to_dict(self):
        return {
            'organization_id': self.organization_id,
            'year': self.year,
            'month': self.month,
            'projects_count': self.projects_count,
            'test_cases_count': self.test_cases_count,
            'ai_calls_count': self.ai_calls_count,
            'storage_used_mb': self.storage_used_mb,
            'members_count': self.members_count,
        }
