"""
API Token 模型

存储用户 API Token 信息，用于 CI/CD 集成。

支持两种权限格式：
1. 旧格式（向后兼容）：['read-only'] 或 ['read-write']
2. 新格式（细粒度）：{"actions": ["read", "execute"], "project_ids": [1, 2]}
   - actions: 允许的操作（read/write/execute/delete）
   - project_ids: 允许访问的项目 ID 列表，空列表表示不限制项目
"""

from datetime import datetime
from ..extensions import db

# 合法的 Token 操作
VALID_TOKEN_ACTIONS = {'read', 'write', 'execute', 'delete'}


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
    permissions = db.Column(db.JSON, default=list, comment='权限范围')
    project_ids = db.Column(db.JSON, default=list, comment='项目 ID 白名单（空=不限制）')
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
            'project_ids': self.project_ids or [],
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def get_actions(self) -> list:
        """
        获取允许的操作列表

        兼容旧格式（['read-only']）和新格式（{"actions": [...]}）。
        """
        if isinstance(self.permissions, dict):
            return self.permissions.get('actions', [])
        # 旧格式兼容
        if isinstance(self.permissions, list):
            actions = []
            for p in self.permissions:
                if p == 'read-only':
                    actions.append('read')
                elif p == 'read-write':
                    actions.extend(['read', 'write', 'execute'])
            return actions
        return []

    def is_read_only(self) -> bool:
        """是否为只读 Token"""
        actions = self.get_actions()
        return actions == ['read'] or self.permissions == ['read-only']

    def can_access_project(self, project_id: int) -> bool:
        """
        检查 Token 是否有权访问指定项目

        空 project_ids 表示不限制（可访问所有项目）。
        """
        scoped_ids = self.project_ids or []
        if not scoped_ids:
            return True
        return project_id in scoped_ids

    def has_action(self, action: str) -> bool:
        """检查 Token 是否允许指定操作"""
        return action in self.get_actions()

    def __repr__(self):
        return f'<ApiToken {self.name}>'
