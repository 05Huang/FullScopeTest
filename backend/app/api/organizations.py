"""
组织管理 API 接口模块
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
    
    member = OrganizationMember(
        organization_id=org.id,
        user_id=user_id,
        role='owner',
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


@api_bp.route('/organizations/<int:org_id>/members', methods=['POST'])
@jwt_required()
def invite_member(org_id):
    """邀请成员"""
    user_id = get_current_user_id()
    org = Organization.query.get(org_id)
    if not org:
        return error_response(404, '组织不存在')
    
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id
    ).first()
    if not membership or membership.role not in ('owner', 'admin'):
        return error_response(403, '无权限')
    
    data = request.get_json()
    target_user_id = data.get('user_id')
    role = data.get('role', 'member')
    
    if not target_user_id:
        return error_response(400, '缺少 user_id')
    
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
    """删除成员"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id
    ).first()
    if not membership or membership.role not in ('owner', 'admin'):
        return error_response(403, '无权限')
    
    target = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=target_user_id
    ).first()
    if not target:
        return error_response(404, '成员不存在')
    
    if target.role == 'owner':
        return error_response(400, '不能删除组织所有者')
    
    db.session.delete(target)
    db.session.commit()
    
    return success_response(message='成员已移除')


@api_bp.route('/organizations/<int:org_id>/members/<int:target_user_id>/role', methods=['PATCH'])
@jwt_required()
def update_member_role(org_id, target_user_id):
    """修改成员角色"""
    user_id = get_current_user_id()
    membership = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=user_id
    ).first()
    if not membership or membership.role != 'owner':
        return error_response(403, '仅组织所有者可修改角色')
    
    target = OrganizationMember.query.filter_by(
        organization_id=org_id, user_id=target_user_id
    ).first()
    if not target:
        return error_response(404, '成员不存在')
    
    data = request.get_json()
    new_role = data.get('role')
    if new_role not in ('admin', 'member', 'viewer'):
        return error_response(400, '无效的角色')
    
    target.role = new_role
    db.session.commit()
    
    return success_response(data=target.to_dict(), message='角色修改成功')
