"""
RBAC 角色与权限模型

定义系统角色和自定义角色，每个角色包含一组权限。
权限格式：{resource}:{action}，如 project:create、test_case:delete

系统角色（不可删除/修改）：
- admin: 全权限
- manager: 除组织管理外的全部权限
- tester: 测试相关全权限，项目/环境/报告只读
- viewer: 仅查看

自定义角色可由组织管理员创建，权限范围不超过创建者自身。
"""
from datetime import datetime
from ..extensions import db

# ── 权限常量 ──────────────────────────────────────────────────────────────────

# 权限资源
RESOURCE_PROJECT = 'project'
RESOURCE_TEST_CASE = 'test_case'
RESOURCE_TEST_RUN = 'test_run'
RESOURCE_ENVIRONMENT = 'environment'
RESOURCE_REPORT = 'report'
RESOURCE_AI_FEATURE = 'ai_feature'

RESOURCES = [
    RESOURCE_PROJECT,
    RESOURCE_TEST_CASE,
    RESOURCE_TEST_RUN,
    RESOURCE_ENVIRONMENT,
    RESOURCE_REPORT,
    RESOURCE_AI_FEATURE,
]

# 权限操作
ACTION_CREATE = 'create'
ACTION_READ = 'read'
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'
ACTION_EXECUTE = 'execute'
ACTION_MANAGE = 'manage'

ACTIONS = [
    ACTION_CREATE,
    ACTION_READ,
    ACTION_UPDATE,
    ACTION_DELETE,
    ACTION_EXECUTE,
    ACTION_MANAGE,
]

# ── 系统角色-权限映射表 ──────────────────────────────────────────────────────
# key = role name, value = {resource: [actions]}
#
# admin    — 全权限
# manager  — 除 manage 外的全部权限（不能管理组织设置/用户）
# tester   — 测试全权限，项目/环境/报告只读
# viewer   — 只读

SYSTEM_ROLE_PERMISSIONS = {
    'admin': {
        RESOURCE_PROJECT: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_TEST_CASE: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_TEST_RUN: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_ENVIRONMENT: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_REPORT: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_AI_FEATURE: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
    },
    'manager': {
        RESOURCE_PROJECT: ['create', 'read', 'update', 'delete', 'execute'],
        RESOURCE_TEST_CASE: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_TEST_RUN: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_ENVIRONMENT: ['create', 'read', 'update', 'delete', 'execute'],
        RESOURCE_REPORT: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_AI_FEATURE: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
    },
    'tester': {
        RESOURCE_PROJECT: ['read'],
        RESOURCE_TEST_CASE: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_TEST_RUN: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
        RESOURCE_ENVIRONMENT: ['read'],
        RESOURCE_REPORT: ['read'],
        RESOURCE_AI_FEATURE: ['create', 'read', 'update', 'delete', 'execute', 'manage'],
    },
    'viewer': {
        RESOURCE_PROJECT: ['read'],
        RESOURCE_TEST_CASE: ['read'],
        RESOURCE_TEST_RUN: ['read'],
        RESOURCE_ENVIRONMENT: ['read'],
        RESOURCE_REPORT: ['read'],
        RESOURCE_AI_FEATURE: ['read'],
    },
}

# 向后兼容：旧角色名 → 新角色名映射
LEGACY_ROLE_MAPPING = {
    'owner': 'admin',
    'admin': 'admin',
    'member': 'tester',
    'manager': 'manager',
    'tester': 'tester',
    'viewer': 'viewer',
}

# 允许在 API 中设置的角色名
VALID_ROLES = ['admin', 'manager', 'tester', 'viewer']


class Role(db.Model):
    """
    角色表

    系统角色（is_system=True）在所有组织共享，不可修改/删除。
    自定义角色（is_system=False）属于特定组织，可由管理员创建。
    """

    __tablename__ = 'roles'
    __table_args__ = (
        db.UniqueConstraint('name', 'organization_id', name='uq_role_name_org'),
        db.Index('idx_roles_org_id', 'organization_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, comment='角色标识（英文）')
    display_name = db.Column(db.String(100), nullable=False, comment='角色显示名称')
    description = db.Column(db.Text, comment='角色描述')
    organization_id = db.Column(
        db.Integer, db.ForeignKey('organizations.id'),
        nullable=True, comment='所属组织（null 表示系统角色）',
    )
    is_system = db.Column(db.Boolean, nullable=False, server_default='0', comment='是否为系统内置角色')
    is_active = db.Column(db.Boolean, nullable=False, server_default='1', comment='是否激活')
    permissions = db.Column(db.JSON, nullable=False, server_default='{}', comment='权限配置 {resource: [actions]}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    organization = db.relationship('Organization', backref='roles')

    def __init__(self, **kwargs):
        # 设置 Python 层面的默认值（db.Column 的 default 仅在 INSERT 时生效）
        kwargs.setdefault('is_system', False)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('permissions', {})
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'organization_id': self.organization_id,
            'is_system': self.is_system,
            'is_active': self.is_active,
            'permissions': self.permissions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def has_permission(self, resource: str, action: str) -> bool:
        """检查角色是否拥有指定权限"""
        if not self.is_active:
            return False
        allowed_actions = self.permissions.get(resource, [])
        return action in allowed_actions

    def __repr__(self):
        return f'<Role {self.name} system={self.is_system} org={self.organization_id}>'


def get_effective_permissions(role_name: str) -> dict:
    """
    根据角色名获取有效权限配置

    优先查询数据库自定义角色，未找到则回退到系统角色映射。
    旧角色名（owner/member）通过 LEGACY_ROLE_MAPPING 转换。
    """
    # 旧角色名兼容
    mapped_name = LEGACY_ROLE_MAPPING.get(role_name, role_name)

    # 先尝试从数据库查找（管理员创建的自定义角色）
    # 注意：数据库查询需要在 app context 中调用
    try:
        role = Role.query.filter_by(name=mapped_name, is_system=True, is_active=True).first()
        if role:
            return role.permissions
    except Exception:
        pass

    # 回退到常量映射
    return SYSTEM_ROLE_PERMISSIONS.get(mapped_name, {})
