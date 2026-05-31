"""
API Token 管理接口

提供 Token 的创建、查询、删除功能
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import api_bp
from ..extensions import db
from ..models.api_token import ApiToken
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json
from .. import limiter


def _hash_token(token: str) -> str:
    """生成 token 的 SHA-256 哈希值"""
    return hashlib.sha256(token.encode()).hexdigest()


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

    query = ApiToken.query.filter_by(user_id=user_id)
    pagination = query.order_by(ApiToken.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return success_response(data={
        'items': [t.to_dict() for t in pagination.items],
        'pagination': {
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
        }
    })


@api_bp.route('/tokens', methods=['POST'])
@jwt_required()
@validate_json('name')
def create_token():
    """
    创建新的 API Token

    请求体:
        name: Token 名称 (必填)
        permissions: 权限范围 (可选, 默认 ['read-only'])
        expires_in_days: 有效期天数 (可选, 默认 null 表示不过期)
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    name = data['name'].strip()
    permissions = data.get('permissions', ['read-only'])
    expires_in_days = data.get('expires_in_days')

    # 验证权限范围
    valid_permissions = {'read-only', 'read-write'}
    if not all(p in valid_permissions for p in permissions):
        return error_response(400, '权限范围无效，可选值: read-only, read-write')

    # 生成 Token
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)

    # 计算过期时间
    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

    api_token = ApiToken(
        user_id=user_id,
        name=name,
        token_hash=token_hash,
        permissions=permissions,
        expires_at=expires_at,
    )

    db.session.add(api_token)
    db.session.commit()

    return success_response(
        data={
            'id': api_token.id,
            'token': token,  # 仅在创建时返回
            'name': api_token.name,
            'permissions': api_token.permissions,
            'expires_at': api_token.expires_at.isoformat() if api_token.expires_at else None,
        },
        message='Token 创建成功',
        code=201
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
