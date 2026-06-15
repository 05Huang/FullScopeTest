"""
多租户资源配额模型

定义组织级别的资源配额限制，支持按计划（免费/专业/企业）配置不同的配额。
"""
from datetime import datetime
from ..extensions import db


class Quota(db.Model):
    """组织资源配额表"""

    __tablename__ = 'quotas'
    __table_args__ = (
        db.UniqueConstraint('organization_id', 'resource_type', name='uq_org_resource_quota'),
        db.Index('idx_quotas_org_id', 'organization_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False, comment='组织 ID')
    resource_type = db.Column(db.String(50), nullable=False, comment='资源类型')
    limit = db.Column(db.Integer, nullable=False, default=0, comment='配额上限（-1 表示不限）')
    used = db.Column(db.Integer, nullable=False, default=0, comment='已使用量')
    plan = db.Column(db.String(20), default='free', comment='计划类型: free/pro/enterprise')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    organization = db.relationship('Organization', backref='quotas')

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'resource_type': self.resource_type,
            'limit': self.limit,
            'used': self.used,
            'remaining': self.remaining,
            'plan': self.plan,
            'is_exhausted': self.is_exhausted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @property
    def remaining(self):
        """剩余配额（-1 表示不限）"""
        if self.limit == -1:
            return -1
        return max(0, self.limit - self.used)

    @property
    def is_exhausted(self):
        """配额是否已耗尽"""
        if self.limit == -1:
            return False
        return self.used >= self.limit

    def __repr__(self):
        return f'<Quota org={self.organization_id} {self.resource_type} {self.used}/{self.limit}>'
