"""
用户模型

存储用户账号信息
"""

from datetime import datetime
from ..extensions import db


# 角色常量
ROLE_ADMIN = 'admin'
ROLE_MEMBER = 'member'
ROLE_VIEWER = 'viewer'

ROLE_PERMISSIONS = {
    ROLE_ADMIN: ['read', 'write', 'delete', 'manage_users', 'manage_settings'],
    ROLE_MEMBER: ['read', 'write'],
    ROLE_VIEWER: ['read'],
}


class User(db.Model):
    """用户表"""

    __tablename__ = 'users'
    __table_args__ = (
        db.Index('idx_users_role', 'role'),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(120), unique=True, nullable=False, comment='邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    avatar = db.Column(db.String(255), comment='头像 URL')
    role = db.Column(db.String(20), default=ROLE_MEMBER, comment='角色: admin/member/viewer')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    reset_token = db.Column(db.String(255), nullable=True, comment='密码重置 Token')
    reset_token_expires = db.Column(db.DateTime, nullable=True, comment='重置 Token 过期时间')
    password_changed_at = db.Column(db.DateTime, nullable=True, comment='最后一次修改密码时间')

    # SSO 单点登录字段
    sso_provider = db.Column(db.String(50), nullable=True, comment='SSO 提供商: oidc/ldap/local')
    sso_id = db.Column(db.String(255), nullable=True, comment='SSO 提供商中的用户标识')
    sso_metadata = db.Column(db.JSON, nullable=True, comment='SSO 提供商返回的额外元数据')

    # 关联
    projects = db.relationship('Project', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'sso_provider': self.sso_provider,
        }

    def has_permission(self, permission: str) -> bool:
        """检查用户是否有指定权限"""
        permissions = ROLE_PERMISSIONS.get(self.role, [])
        return permission in permissions

    def is_admin(self) -> bool:
        """检查是否为管理员"""
        return self.role == ROLE_ADMIN

    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'
