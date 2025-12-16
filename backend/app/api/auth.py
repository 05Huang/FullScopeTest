"""
认证接口模块

提供用户注册、登录、登出等功能
"""

from flask import request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required
)
from werkzeug.security import generate_password_hash, check_password_hash

from . import api_bp
from ..extensions import db
from ..models.user import User
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json, is_valid_email
from ..utils import get_current_user_id


@api_bp.route('/auth/register', methods=['POST'])
@validate_json('username', 'email', 'password')
def register():
    """
    用户注册
    
    请求体:
        username: 用户名 (3-50字符)
        email: 邮箱地址
        password: 密码 (至少6位)
    """
    data = request.get_json()
    
    username = data['username'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    
    # 验证用户名长度
    if len(username) < 3 or len(username) > 50:
        return error_response(400, '用户名长度应为 3-50 个字符')
    
    # 验证邮箱格式
    if not is_valid_email(email):
        return error_response(400, '邮箱格式不正确')
    
    # 验证密码长度
    if len(password) < 6:
        return error_response(400, '密码长度至少 6 位')
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return error_response(400, '用户名已被使用')
    
    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        return error_response(400, '邮箱已被注册')
    
    # 创建用户
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    
    db.session.add(user)
    db.session.commit()
    
    return success_response(
        data={'user_id': user.id, 'username': user.username},
        message='注册成功',
        code=201
    )


@api_bp.route('/auth/login', methods=['POST'])
@validate_json('username', 'password')
def login():
    """
    用户登录
    
    请求体:
        username: 用户名或邮箱
        password: 密码
    """
    data = request.get_json()
    
    username = data['username'].strip()
    password = data['password']
    
    # 支持用户名或邮箱登录
    user = User.query.filter(
        (User.username == username) | (User.email == username.lower())
    ).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return error_response(401, '用户名或密码错误')
    
    if not user.is_active:
        return error_response(403, '账号已被禁用')
    
    # 更新最后登录时间
    user.update_last_login()
    
    # 生成 Token (identity 需要是字符串)
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return success_response(
        data={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        },
        message='登录成功'
    )


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return error_response(404, '用户不存在')
    
    return success_response(data=user.to_dict())


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """刷新 Access Token"""
    user_id = get_current_user_id()
    access_token = create_access_token(identity=str(user_id))
    
    return success_response(
        data={'access_token': access_token},
        message='Token 刷新成功'
    )


@api_bp.route('/auth/password', methods=['PUT'])
@jwt_required()
@validate_json('old_password', 'new_password')
def change_password():
    """修改密码"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']
    
    # 验证旧密码
    if not check_password_hash(user.password_hash, old_password):
        return error_response(400, '原密码错误')
    
    # 验证新密码长度
    if len(new_password) < 6:
        return error_response(400, '新密码长度至少 6 位')
    
    # 更新密码
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return success_response(message='密码修改成功')
