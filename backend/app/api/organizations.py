"""
组织管理 API 接口模块

包含组织 CRUD、成员管理和 RBAC 角色管理端点。
"""
from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..extensions import db
from ..models.organization import Organization, OrganizationMember
from ..models.user import User
from ..utils.response import success_response, error_response, paginate_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id
from ..middleware.tenant import get_current_organization_id
from ..services import permission_service
from ..models.role import VALID_ROLES


# ── 组织 CRUD ────────────────────────────────────────────────────────────────

@api_bp.route('/organizations', methods=['POST'])
@jwt_required()
@validate_json('name')
def create_organization():
    """创建组织"""
    user_id = get_current_user_id()
    data = request.get_json()

    name = data['name'].strip()
    slug = data.get('slug', '').strip()
    description = data.get('description', '').strip()

    if len(name) < 1 or len(name) > 100:
        return error_response(400, '组织名称长度应为 1-100 个字符')

    if not slug:
        slug = name.lower().replace(' ', '-')

    existing = Organization.query.filter_by(slug=slug).first()
    if existing:
        return error_response(400, '组织 slug 已存在')

    org = Organization(
        name=name,
        slug=slug,
        description=description,
        owner_id=user_id,
    )
    db.session.add(org)
    db.session.flush()

    # 创建者默认为 admin 角色（RBAC 兼容）
    member = OrganizationMember(
        organization_id=org.id,
        user_id=user_id,
        role='admin',
    )
    db.session.add(member)
    db.session.commit()

    return success_response(data=org.to_dict(), message='组织创建成功', code=201)


@api_bp.route('/organizations/me', methods=['GET'])
@jwt_required()
def get_my_organizations():
    """获取当前用户的组织列表"""
    user_id = get_current_user_id()
    memberships = OrganizationMember.query.filter_by(user_id=user_id).all()
    org_ids = [m.organization_id for m in memberships]
    orgs = Organization.query.filter(Organization.id.in_(org_ids)).all()
    return success_response(data=[o.to_dict() for o in orgs])


# ── 成员管理 ──────────────────────────────────────────────────────────────────

@api_bp.route('/organizations/<int:org_id>/members', methods=['POST'])
@jwt_required()
def invite_member(org_id):
    """邀请成员（需要 project:manage 权限）"""
    user_id = get_current_user_id()
    org = Organization.query.get(org_id)
    if not org:
        return error_response(404, '组织不存在')

    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership:
        return error_response(403, '无权限')

    # 检查邀请者是否有 manage 权限（admin 或 manager 角色）
    inviter_role = membership.get_effective_role_name()
    if inviter_role not in ('admin', 'manager', 'owner'):
        return error_response(403, '无权限邀请成员')

    data = request.get_json()
    target_user_id = data.get('user_id')
    role = data.get('role', 'tester')

    if not target_user_id:
        return error_response(400, '缺少 user_id')

    # 验证角色是否合法
    if role not in VALID_ROLES and role not in ('owner', 'member'):
        return error_response(400, '无效的角色', errors={'valid_roles': VALID_ROLES})

    existing = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=target_user_id
    ).first()
    if existing:
        return error_response(400, '用户已在组织中')

    member = OrganizationMember(
        organization_id=org_id,
        user_id=target_user_id,
        role=role,
        invited_by=user_id,
    )
    db.session.add(member)
    db.session.commit()

    return success_response(data=member.to_dict(), message='成员邀请成功', code=201)


@api_bp.route('/organizations/<int:org_id>/members/<int:target_user_id>', methods=['DELETE'])
@jwt_required()
def remove_member(org_id, target_user_id):
    """删除成员（需要 manage 权限或为组织所有者）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership:
        return error_response(403, '无权限')

    # admin 角色或 owner 可移除成员
    inviter_role = membership.get_effective_role_name()
    if inviter_role not in ('admin', 'owner'):
        return error_response(403, '无权限')

    target = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=target_user_id
    ).first()
    if not target:
        return error_response(404, '成员不存在')

    if target.role == 'owner' or target.get_effective_role_name() == 'admin':
        # 不能删除最后一个 admin
        admin_count = OrganizationMember.query.filter_by(
            organization_id=org_id, is_active=True,
        ).filter(OrganizationMember.role.in_(['owner', 'admin'])).count()
        if admin_count <= 1:
            return error_response(400, '不能删除组织唯一的管理员')

    db.session.delete(target)
    db.session.commit()

    return success_response(message='成员已移除')


@api_bp.route('/organizations/<int:org_id>/members/<int:target_user_id>/role', methods=['PATCH'])
@jwt_required()
def update_member_role(org_id, target_user_id):
    """修改成员角色（仅 admin 可操作）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership:
        return error_response(403, '无权限')

    inviter_role = membership.get_effective_role_name()
    if inviter_role != 'admin':
        return error_response(403, '仅管理员可修改角色')

    target = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=target_user_id
    ).first()
    if not target:
        return error_response(404, '成员不存在')

    data = request.get_json()
    new_role = data.get('role')
    if new_role not in VALID_ROLES:
        return error_response(400, '无效的角色', errors={'valid_roles': VALID_ROLES})

    # 不允许降级最后一个 admin
    if target.role in ('owner', 'admin') and new_role != 'admin':
        admin_count = OrganizationMember.query.filter_by(
            organization_id=org_id, is_active=True,
        ).filter(OrganizationMember.role.in_(['owner', 'admin'])).count()
        if admin_count <= 1:
            return error_response(400, '不能降级组织唯一的管理员')

    target.role = new_role
    db.session.commit()

    return success_response(data=target.to_dict(), message='角色修改成功')


# ── 成员权限查询 ─────────────────────────────────────────────────────────────

@api_bp.route('/organizations/<int:org_id>/my-permissions', methods=['GET'])
@jwt_required()
def get_my_permissions(org_id):
    """获取当前用户在指定组织中的权限信息"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership:
        return error_response(403, '不属于该组织')

    permissions = permission_service.get_user_permissions(user_id, org_id)
    role_name = permission_service.get_user_role_name(user_id, org_id)

    return success_response(data={
        'role': role_name,
        'original_role': membership.role,
        'permissions': permissions,
    })


@api_bp.route('/organizations/<int:org_id>/members/<int:target_user_id>/permissions', methods=['GET'])
@jwt_required()
def get_member_permissions(org_id, target_user_id):
    """获取指定成员在组织中的权限信息（需要 manage 权限）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership:
        return error_response(403, '无权限')

    inviter_role = membership.get_effective_role_name()
    if inviter_role not in ('admin', 'manager', 'owner'):
        return error_response(403, '需要管理员或经理权限')

    target = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=target_user_id, is_active=True,
    ).first()
    if not target:
        return error_response(404, '成员不存在')

    permissions = target.get_permissions()
    return success_response(data={
        'user_id': target_user_id,
        'role': target.get_effective_role_name(),
        'original_role': target.role,
        'permissions': permissions,
    })


# ── 角色管理 ──────────────────────────────────────────────────────────────────

@api_bp.route('/organizations/<int:org_id>/roles', methods=['GET'])
@jwt_required()
def list_roles(org_id):
    """获取组织可用的角色列表（系统角色 + 自定义角色）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership:
        return error_response(403, '不属于该组织')

    roles = permission_service.get_organization_roles(org_id)
    return success_response(data=roles)


@api_bp.route('/organizations/<int:org_id>/roles', methods=['POST'])
@jwt_required()
def create_role(org_id):
    """创建自定义角色（仅 admin）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership or membership.get_effective_role_name() != 'admin':
        return error_response(403, '仅管理员可创建角色')

    data = request.get_json()
    name = data.get('name', '').strip()
    display_name = data.get('display_name', '').strip()
    permissions = data.get('permissions', {})
    description = data.get('description', '')

    if not name:
        return error_response(400, '缺少角色标识')
    if not display_name:
        return error_response(400, '缺少角色显示名称')

    try:
        role = permission_service.create_custom_role(
            organization_id=org_id,
            name=name,
            display_name=display_name,
            permissions=permissions,
            description=description,
        )
    except ValueError as e:
        return error_response(400, str(e))

    return success_response(data=role.to_dict(), message='角色创建成功', code=201)


@api_bp.route('/organizations/<int:org_id>/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(org_id, role_id):
    """更新自定义角色（仅 admin）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership or membership.get_effective_role_name() != 'admin':
        return error_response(403, '仅管理员可修改角色')

    data = request.get_json()

    try:
        role = permission_service.update_custom_role(
            role_id=role_id,
            organization_id=org_id,
            display_name=data.get('display_name'),
            permissions=data.get('permissions'),
            description=data.get('description'),
        )
    except ValueError as e:
        return error_response(400, str(e))

    return success_response(data=role.to_dict(), message='角色更新成功')


@api_bp.route('/organizations/<int:org_id>/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(org_id, role_id):
    """删除自定义角色（仅 admin，软删除）"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id, is_active=True,
    ).first()
    if not membership or membership.get_effective_role_name() != 'admin':
        return error_response(403, '仅管理员可删除角色')

    try:
        permission_service.delete_custom_role(role_id=role_id, organization_id=org_id)
    except ValueError as e:
        return error_response(400, str(e))

    return success_response(message='角色已删除')


@api_bp.route('/roles/system', methods=['GET'])
@jwt_required()
def list_system_roles():
    """获取所有系统角色定义"""
    roles = permission_service.get_system_roles()
    return success_response(data=roles)
