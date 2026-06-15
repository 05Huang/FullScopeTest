"""
通知配置模型

存储用户/组织的通知渠道配置。
"""
from datetime import datetime
from ..extensions import db


class NotificationConfig(db.Model):
    """通知配置表"""

    __tablename__ = 'notification_configs'
    __table_args__ = (
        db.Index('idx_notif_config_user_id', 'user_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户 ID')
    name = db.Column(db.String(100), nullable=False, comment='配置名称')
    channel = db.Column(db.String(20), nullable=False, comment='渠道: webhook/dingtalk/feishu/slack')
    webhook_url = db.Column(db.String(500), nullable=False, comment='Webhook URL')
    token = db.Column(db.String(500), comment='认证 Token（可选）')
    events = db.Column(db.JSON, default=list, comment='订阅事件列表')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    user = db.relationship('User', backref='notification_configs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'channel': self.channel,
            'webhook_url': self.webhook_url,
            'has_token': bool(self.token),
            'events': self.events or [],
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<NotificationConfig {self.name} [{self.channel}]>'
