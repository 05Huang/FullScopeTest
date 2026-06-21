"""
管理员 API — 用户管理
仅限 admin 角色访问。
"""
from datetime import datetime, timezone
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from ..extensions import db
from ..models.user import User
from ..utils.response import success_response, error_response

admin_bp = Blueprint('admin', __name__)

def _require_admin():
    """统一权限检查入口"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin():
        return None
    return user

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    admin = _require_admin()
    if not admin:
        return error_response(403, '需要管理员权限')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '').strip()
    query = User.query
    if search:
        query = query.filter(or_(User.username.ilike(f'%{search}%'), User.email.ilike(f'%{search}%')))
    if role_filter:
        query = query.filter(User.role == role_filter)
    query = query.order_by(User.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return success_response(data={
        'items': [u.to_dict(include_sensitive=True) for u in pagination.items],
        'total': pagination.total, 'page': page, 'per_page': per_page, 'pages': pagination.pages,
    })

@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    admin = _require_admin()
    if not admin:
        return error_response(403, '需要管理员权限')
    user = User.query.get(user_id)
    if not user:
        return error_response(404, '用户不存在')
    return success_response(data=user.to_dict(include_sensitive=True))

@admin_bp.route('/admin/users/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
def update_user_role(user_id):
    admin = _require_admin()
    if not admin:
        return error_response(403, '需要管理员权限')
    user = User.query.get(user_id)
    if not user:
        return error_response(404, '用户不存在')
    data = request.get_json() or {}
    new_role = data.get('role', '').strip()
    if new_role not in ('admin', 'member', 'viewer'):
        return error_response(400, '无效的角色，可选: admin, member, viewer')
    if user.id == admin.id:
        return error_response(400, '不能修改自己的角色')
    old_role = user.role
    user.role = new_role
    db.session.commit()
    return success_response(message=f'角色已从 {old_role} 修改为 {new_role}')

@admin_bp.route('/admin/users/<int:user_id>/status', methods=['PATCH'])
@jwt_required()
def update_user_status(user_id):
    admin = _require_admin()
    if not admin:
        return error_response(403, '需要管理员权限')
    user = User.query.get(user_id)
    if not user:
        return error_response(404, '用户不存在')
    data = request.get_json() or {}
    is_active = data.get('is_active')
    if is_active is None:
        return error_response(400, '请提供 is_active 参数')
    if user.id == admin.id:
        return error_response(400, '不能禁用自己的账号')
    user.is_active = bool(is_active)
    db.session.commit()
    return success_response(message=f'用户已{"启用" if user.is_active else "禁用"}')

@admin_bp.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
@jwt_required()
def reset_user_password(user_id):
    admin = _require_admin()
    if not admin:
        return error_response(403, '需要管理员权限')
    user = User.query.get(user_id)
    if not user:
        return error_response(404, '用户不存在')
    data = request.get_json() or {}
    new_password = data.get('password', '').strip()
    from ..utils.validators import validate_password_strength
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        return error_response(400, error_msg)
    from werkzeug.security import generate_password_hash
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return success_response(message='密码已重置')
