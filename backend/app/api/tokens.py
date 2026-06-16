"""
API Token 管理接口

提供 Token 的创建、查询、删除功能。
支持细粒度权限：操作类型 + 项目范围。
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import api_bp
from ..extensions import db
from ..models.api_token import ApiToken, VALID_TOKEN_ACTIONS
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json
from ..services.token_service import create_token, validate_token, check_token_permission
from .. import limiter


@api_bp.route('/tokens', methods=['GET'])
@jwt_required()
def get_tokens():
    """
    获取当前用户的所有 API Token

    查询参数:
        page: 页码 (默认 1)
        per_page: 每页数量 (默认 20)
    """
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = ApiToken.query.filter_by(user_id=user_id).order_by(ApiToken.created_at.desc())

    # Flask-SQLAlchemy 3.x 兼容分页
    try:
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = pagination.items
        total = pagination.total
        pages = pagination.pages
    except AttributeError:
        # 回退到手动分页
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        pages = (total + per_page - 1) // per_page

    return success_response(data={
        'items': [t.to_dict() for t in items],
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': pages,
        }
    })


@api_bp.route('/tokens', methods=['POST'])
@jwt_required()
@validate_json('name')
def create_token_api():
    """
    创建新的 API Token

    请求体:
        name: Token 名称 (必填)
        actions: 允许的操作列表 (可选, 默认 ['read'])
            合法值: read, write, execute, delete
        project_ids: 项目 ID 白名单 (可选, 空列表表示不限制)
        permissions: 旧格式权限 (可选, 向后兼容)
            可选值: read-only, read-write
        expires_in_days: 有效期天数 (可选, 默认 null 表示不过期)

    示例（新格式）:
        {
            "name": "CI Token",
            "actions": ["read", "execute"],
            "project_ids": [1, 2, 5]
        }

    示例（旧格式兼容）:
        {
            "name": "Read Token",
            "permissions": ["read-only"]
        }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    name = data['name'].strip()
    actions = data.get('actions')
    project_ids = data.get('project_ids', [])
    old_permissions = data.get('permissions')
    expires_in_days = data.get('expires_in_days')

    # 支持旧格式 → 新格式转换
    if actions is None and old_permissions:
        actions = _convert_old_permissions(old_permissions)
        if actions is None:
            return error_response(400, '权限格式无效，可选值: read-only, read-write')
    elif actions is None:
        actions = ['read']

    # 校验操作类型
    invalid_actions = set(actions) - VALID_TOKEN_ACTIONS
    if invalid_actions:
        return error_response(
            400,
            f'无效的操作类型: {invalid_actions}',
            errors={'valid_actions': list(VALID_TOKEN_ACTIONS)},
        )

    # 校验 project_ids 格式
    if not isinstance(project_ids, list):
        return error_response(400, 'project_ids 必须为数组')
    for pid in project_ids:
        if not isinstance(pid, int):
            return error_response(400, f'project_ids 中的值必须为整数: {pid}')

    try:
        api_token, token = create_token(
            user_id=user_id,
            name=name,
            actions=actions,
            project_ids=project_ids,
            expires_in_days=expires_in_days,
        )
    except ValueError as e:
        return error_response(400, str(e))

    return success_response(
        data={
            'id': api_token.id,
            'token': token,  # 仅在创建时返回明文
            'name': api_token.name,
            'actions': actions,
            'project_ids': project_ids,
            'permissions': api_token.permissions,
            'expires_at': api_token.expires_at.isoformat() if api_token.expires_at else None,
        },
        message='Token 创建成功',
        code=201,
    )


@api_bp.route('/tokens/<int:token_id>', methods=['DELETE'])
@jwt_required()
def delete_token(token_id):
    """删除 API Token"""
    user_id = get_jwt_identity()

    api_token = ApiToken.query.filter_by(id=token_id, user_id=user_id).first()
    if not api_token:
        return error_response(404, 'Token 不存在')

    db.session.delete(api_token)
    db.session.commit()

    return success_response(message='Token 已删除')


@api_bp.route('/tokens/validate', methods=['POST'])
@jwt_required()
def validate_token_api():
    """
    验证当前请求中 API Token 的权限

    请求体:
        action: 要检查的操作
        project_id: 要检查的项目 ID（可选）

    返回:
        Token 是否有权限执行指定操作
    """
    data = request.get_json()
    action = data.get('action', 'read')
    project_id = data.get('project_id')

    # 获取当前 Token（通过 Authorization header）
    from flask import request as req
    auth_header = req.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return error_response(400, '缺少 Token')

    token = auth_header[7:]
    api_token = validate_token(token)
    if not api_token:
        return error_response(401, 'Token 无效')

    has_perm = check_token_permission(api_token, action, project_id)
    return success_response(data={
        'has_permission': has_perm,
        'token_name': api_token.name,
        'actions': api_token.get_actions(),
        'project_ids': api_token.project_ids or [],
    })


def _convert_old_permissions(permissions: list) -> list:
    """将旧格式权限转换为新的 actions 列表"""
    if not isinstance(permissions, list):
        return None
    actions = []
    for p in permissions:
        if p == 'read-only':
            actions.append('read')
        elif p == 'read-write':
            actions.extend(['read', 'write', 'execute'])
        else:
            return None
    return list(set(actions)) if actions else None
