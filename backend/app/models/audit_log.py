"""
审计日志模型

记录所有写操作的审计日志
"""

from datetime import datetime
from ..extensions import db


class AuditLog(db.Model):
    """审计日志表 - 记录所有写操作"""

    __tablename__ = 'audit_logs'
    __table_args__ = (
        db.Index('idx_audit_logs_user_id', 'user_id'),
        db.Index('idx_audit_logs_action', 'action'),
        db.Index('idx_audit_logs_resource_type', 'resource_type'),
        db.Index('idx_audit_logs_created_at', 'created_at'),
        db.Index('idx_audit_logs_organization_id', 'organization_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # 用户信息
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, comment='操作用户 ID')

    # 组织信息
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, comment='组织 ID')

    # 操作信息
    action = db.Column(db.String(50), nullable=False, comment='操作类型: create/update/delete/login/logout')
    resource_type = db.Column(db.String(50), nullable=False, comment='资源类型: project/test_case/test_run/organization/user')
    resource_id = db.Column(db.Integer, comment='资源 ID')

    # 变更详情
    changes = db.Column(db.JSON, comment='变更内容 (JSON diff)')
    old_values = db.Column(db.JSON, comment='旧值')
    new_values = db.Column(db.JSON, comment='新值')

    # 请求信息
    ip_address = db.Column(db.String(45), comment='客户端 IP 地址')
    user_agent = db.Column(db.String(500), comment='客户端 User-Agent')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='操作时间')

    # 关联关系
    user = db.relationship('User', backref='audit_logs')
    organization = db.relationship('Organization', backref='audit_logs')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'changes': self.changes,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<AuditLog {self.action} {self.resource_type} #{self.resource_id}>'
