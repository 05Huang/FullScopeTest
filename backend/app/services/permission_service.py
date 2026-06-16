"""
RBAC 权限检查服务

提供基于组织角色的权限检查，供 API 层和 Service 层使用。

核心功能：
- 根据用户 ID + 组织 ID 查询成员角色并检查权限
- 获取用户在指定组织中的权限列表
- 管理角色（系统角色只读，自定义角色 CRUD）
"""
from typing import Optional
from ..extensions import db
from ..models.organization import Organization, OrganizationMember
from ..models.role import (
    Role,
    RESOURCES,
    ACTIONS,
    VALID_ROLES,
    SYSTEM_ROLE_PERMISSIONS,
    LEGACY_ROLE_MAPPING,
    get_effective_permissions,
)
from ..core.logging import get_logger

logger = get_logger(__name__)


# ── 权限查询 ──────────────────────────────────────────────────────────────────

def get_user_role_in_org(user_id: int, organization_id: int) -> Optional[OrganizationMember]:
    """
    获取用户在指定组织中的成员记录

    Returns:
        OrganizationMember 对象，None 表示用户不在该组织中
    """
    return OrganizationMember.query.filter_by(
        user_id=user_id,
        organization_id=organization_id,
        is_active=True,
    ).first()


def check_permission(user_id: int, organization_id: int, resource: str, action: str) -> bool:
    """
    检查用户在指定组织中是否拥有指定权限

    Args:
        user_id: 用户 ID
        organization_id: 组织 ID
        resource: 权限资源（project/test_case/test_run/environment/report/ai_feature）
        action: 权限操作（create/read/update/delete/execute/manage）

    Returns:
        True 表示有权限
    """
    membership = get_user_role_in_org(user_id, organization_id)
    if not membership:
        return False
    return membership.has_permission(resource, action)


def get_user_permissions(user_id: int, organization_id: int) -> dict:
    """
    获取用户在指定组织中的完整权限配置

    Returns:
        {resource: [actions]} 字典，空字典表示无权限
    """
    membership = get_user_role_in_org(user_id, organization_id)
    if not membership:
        return {}
    return membership.get_permissions()


def get_user_role_name(user_id: int, organization_id: int) -> Optional[str]:
    """
    获取用户在指定组织中的有效角色名

    Returns:
        角色名字符串（已映射到新 RBAC 角色名），None 表示不属于该组织
    """
    membership = get_user_role_in_org(user_id, organization_id)
    if not membership:
        return None
    return membership.get_effective_role_name()


# ── 角色管理 ──────────────────────────────────────────────────────────────────

def get_system_roles() -> list[dict]:
    """获取所有系统角色列表"""
    roles = Role.query.filter_by(is_system=True, is_active=True).all()
    if not roles:
        # 数据库中尚无系统角色，返回常量
        return _build_system_role_dicts()
    return [r.to_dict() for r in roles]


def get_organization_roles(organization_id: int) -> list[dict]:
    """
    获取组织可用的角色列表（系统角色 + 组织自定义角色）
    """
    system_roles = Role.query.filter_by(is_system=True, is_active=True).all()
    custom_roles = Role.query.filter_by(
        organization_id=organization_id,
        is_system=False,
        is_active=True,
    ).all()

    if not system_roles:
        # 系统角色尚未初始化到数据库，使用常量
        result = _build_system_role_dicts()
    else:
        result = [r.to_dict() for r in system_roles]

    result.extend(r.to_dict() for r in custom_roles)
    return result


def create_custom_role(
    organization_id: int,
    name: str,
    display_name: str,
    permissions: dict,
    description: str = '',
) -> Role:
    """
    创建组织自定义角色

    Args:
        organization_id: 组织 ID
        name: 角色标识（英文，不可与系统角色重名）
        display_name: 角色显示名称
        permissions: 权限配置 {resource: [actions]}
        description: 角色描述

    Returns:
        创建的 Role 对象

    Raises:
        ValueError: 角色名冲突或权限配置无效
    """
    # 系统角色名不可使用
    if name in SYSTEM_ROLE_PERMISSIONS:
        raise ValueError(f"角色名 '{name}' 为系统保留，不可使用")

    # 检查组织内是否重名
    existing = Role.query.filter_by(
        name=name,
        organization_id=organization_id,
    ).first()
    if existing:
        raise ValueError(f"角色名 '{name}' 已存在")

    # 校验权限格式
    _validate_permissions(permissions)

    role = Role(
        name=name,
        display_name=display_name,
        description=description,
        organization_id=organization_id,
        is_system=False,
        permissions=permissions,
    )
    db.session.add(role)
    db.session.commit()
    logger.info("自定义角色已创建",
                organization_id=organization_id, role_name=name)
    return role


def update_custom_role(
    role_id: int,
    organization_id: int,
    display_name: str = None,
    permissions: dict = None,
    description: str = None,
) -> Role:
    """
    更新组织自定义角色

    系统角色不可修改。
    """
    role = Role.query.get(role_id)
    if not role:
        raise ValueError("角色不存在")
    if role.is_system:
        raise ValueError("系统角色不可修改")
    if role.organization_id != organization_id:
        raise ValueError("无权修改该角色")

    if display_name is not None:
        role.display_name = display_name
    if permissions is not None:
        _validate_permissions(permissions)
        role.permissions = permissions
    if description is not None:
        role.description = description

    db.session.commit()
    logger.info("自定义角色已更新", role_id=role_id, role_name=role.name)
    return role


def delete_custom_role(role_id: int, organization_id: int):
    """
    删除组织自定义角色（软删除）

    系统角色不可删除。
    """
    role = Role.query.get(role_id)
    if not role:
        raise ValueError("角色不存在")
    if role.is_system:
        raise ValueError("系统角色不可删除")
    if role.organization_id != organization_id:
        raise ValueError("无权删除该角色")

    role.is_active = False
    db.session.commit()
    logger.info("自定义角色已删除", role_id=role_id, role_name=role.name)


def seed_system_roles():
    """
    将系统角色写入数据库（幂等操作）

    应在应用启动或首次部署时调用。
    """
    role_names = {
        'admin': ('管理员', '拥有所有权限，可管理组织和成员'),
        'manager': ('经理', '可管理测试资源，不能管理组织设置'),
        'tester': ('测试员', '可执行和管理测试，项目/环境/报告只读'),
        'viewer': ('观察者', '仅查看权限'),
    }

    for name, perms in SYSTEM_ROLE_PERMISSIONS.items():
        existing = Role.query.filter_by(name=name, is_system=True).first()
        if not existing:
            display_name, desc = role_names.get(name, (name, ''))
            role = Role(
                name=name,
                display_name=display_name,
                description=desc,
                organization_id=None,
                is_system=True,
                permissions=perms,
            )
            db.session.add(role)
            logger.info("系统角色已创建", role_name=name)

    db.session.commit()


# ── 内部工具 ──────────────────────────────────────────────────────────────────

def _validate_permissions(permissions: dict):
    """
    校验权限配置格式

    - key 必须是合法的 resource 名
    - value 必须是合法的 action 列表
    """
    if not isinstance(permissions, dict):
        raise ValueError("权限配置必须为字典格式")

    for resource, actions in permissions.items():
        if resource not in RESOURCES:
            raise ValueError(f"未知资源类型: {resource}，合法值: {RESOURCES}")
        if not isinstance(actions, list):
            raise ValueError(f"资源 {resource} 的权限操作必须为列表")
        for action in actions:
            if action not in ACTIONS:
                raise ValueError(f"未知操作: {action}，合法值: {ACTIONS}")


def _build_system_role_dicts() -> list[dict]:
    """从常量构建系统角色字典列表（用于数据库尚未初始化时）"""
    names = {
        'admin': ('管理员', '拥有所有权限，可管理组织和成员'),
        'manager': ('经理', '可管理测试资源，不能管理组织设置'),
        'tester': ('测试员', '可执行和管理测试，项目/环境/报告只读'),
        'viewer': ('观察者', '仅查看权限'),
    }
    result = []
    for name, perms in SYSTEM_ROLE_PERMISSIONS.items():
        display_name, desc = names.get(name, (name, ''))
        result.append({
            'id': None,
            'name': name,
            'display_name': display_name,
            'description': desc,
            'organization_id': None,
            'is_system': True,
            'is_active': True,
            'permissions': perms,
            'created_at': None,
            'updated_at': None,
        })
    return result
