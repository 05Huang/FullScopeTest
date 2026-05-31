"""
API Token 模型

存储用户 API Token 信息，用于 CI/CD 集成
"""

from datetime import datetime
from ..extensions import db


class ApiToken(db.Model):
    """API Token 表"""

    __tablename__ = 'api_tokens'
    __table_args__ = (
        db.Index('idx_api_tokens_user_id', 'user_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户 ID')
    name = db.Column(db.String(100), nullable=False, comment='Token 名称')
    token_hash = db.Column(db.String(256), nullable=False, comment='Token 哈希值')
    permissions = db.Column(db.JSON, default=list, comment='权限范围: read-only/read-write')
    expires_at = db.Column(db.DateTime, comment='过期时间（可为 null 表示不过期）')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    last_used_at = db.Column(db.DateTime, comment='最后使用时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 关联关系
    user = db.relationship('User', backref='api_tokens')

    def to_dict(self):
        """转换为字典（不包含 token 明文）"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'permissions': self.permissions,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<ApiToken {self.name}>'
