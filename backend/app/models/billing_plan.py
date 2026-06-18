"""
套餐模型

定义 SaaS 定价计划：
- Free：5 项目、100 用例、1 并行、100 AI 调用/月
- Pro（¥299/月）：50 项目、1000 用例、5 并行、5000 AI 调用/月
- Enterprise（定制）：不限
"""
from datetime import datetime
from ..extensions import db


class BillingPlan(db.Model):
    """套餐表"""
    __tablename__ = 'billing_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, comment='套餐名称：free/pro/enterprise')
    display_name = db.Column(db.String(100), nullable=False, comment='显示名称')
    description = db.Column(db.Text, comment='套餐描述')
    price_monthly = db.Column(db.Float, default=0, comment='月价格（元）')
    price_yearly = db.Column(db.Float, default=0, comment='年价格（元）')
    currency = db.Column(db.String(10), default='CNY', comment='货币单位')

    # 配额限制
    max_projects = db.Column(db.Integer, default=5, comment='最大项目数')
    max_test_cases = db.Column(db.Integer, default=100, comment='最大用例数')
    max_parallel_executions = db.Column(db.Integer, default=1, comment='最大并行执行数')
    max_ai_calls_monthly = db.Column(db.Integer, default=100, comment='每月 AI 调用次数')
    max_members = db.Column(db.Integer, default=5, comment='最大成员数')
    max_storage_mb = db.Column(db.Integer, default=1024, comment='最大存储空间（MB）')

    # 功能开关
    features = db.Column(db.JSON, default=dict, comment='功能开关 {feature: enabled}')

    is_active = db.Column(db.Boolean, default=True, comment='是否可用')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'price_monthly': self.price_monthly,
            'price_yearly': self.price_yearly,
            'currency': self.currency,
            'max_projects': self.max_projects,
            'max_test_cases': self.max_test_cases,
            'max_parallel_executions': self.max_parallel_executions,
            'max_ai_calls_monthly': self.max_ai_calls_monthly,
            'max_members': self.max_members,
            'max_storage_mb': self.max_storage_mb,
            'features': self.features,
            'is_active': self.is_active,
        }


def seed_default_plans():
    """种子默认套餐"""
    plans = [
        BillingPlan(
            name='free',
            display_name='Free',
            description='适合个人或小团队试用',
            price_monthly=0,
            price_yearly=0,
            max_projects=5,
            max_test_cases=100,
            max_parallel_executions=1,
            max_ai_calls_monthly=100,
            max_members=5,
            max_storage_mb=1024,
            sort_order=0,
        ),
        BillingPlan(
            name='pro',
            display_name='Pro',
            description='适合中型团队，解锁全部功能',
            price_monthly=299,
            price_yearly=2990,
            max_projects=50,
            max_test_cases=1000,
            max_parallel_executions=5,
            max_ai_calls_monthly=5000,
            max_members=50,
            max_storage_mb=10240,
            features={'advanced_reports': True, 'api_tokens': True, 'webhooks': True},
            sort_order=1,
        ),
        BillingPlan(
            name='enterprise',
            display_name='Enterprise',
            description='适合大型企业，不限用量',
            price_monthly=0,
            price_yearly=0,
            max_projects=-1,
            max_test_cases=-1,
            max_parallel_executions=-1,
            max_ai_calls_monthly=-1,
            max_members=-1,
            max_storage_mb=-1,
            features={'advanced_reports': True, 'api_tokens': True, 'webhooks': True,
                      'sso': True, 'audit_logs': True, 'custom_branding': True},
            sort_order=2,
        ),
    ]

    for plan in plans:
        existing = BillingPlan.query.filter_by(name=plan.name).first()
        if not existing:
            db.session.add(plan)
    db.session.commit()
