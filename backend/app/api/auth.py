"""
认证接口模块

提供用户注册、登录、登出、密码重置等功能
"""

import secrets
from datetime import datetime, timedelta

from flask import request, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from werkzeug.security import generate_password_hash, check_password_hash

from . import api_bp
from ..extensions import db
from ..models.user import User
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json, is_valid_email, validate_password_strength
from .. import limiter
from ..utils import get_current_user_id
from ..utils.oss_upload import upload_to_oss
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/auth/register', methods=['POST'])
@limiter.limit("5/minute")
@validate_json('username', 'email', 'password')
def register():
    """
    用户注册

    请求体:
        username: 用户名 (3-50字符)
        email: 邮箱地址
        password: 密码 (至少8位，包含大小写字母、数字、特殊字符)
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

    # 验证密码强度
    is_valid, error_msg = validate_password_strength(password)
    if not is_valid:
        return error_response(400, error_msg)
    
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
@limiter.limit("5/minute")
@validate_json('username', 'password')
def login():
    """
    用户登录

    请求体:
        username: 用户名或邮箱
        password: 密码

    安全机制：
        - 连续 5 次登录失败后锁定账户 15 分钟
        - 锁定状态下返回 HTTP 423
        - 成功登录后重置失败计数
    """
    from ..services.password_policy import (
        is_account_locked, record_login_failure, reset_login_failures, get_login_failures,
    )

    data = request.get_json()

    username = data['username'].strip()
    password = data['password']
    ip_address = request.remote_addr

    # 支持用户名或邮箱登录
    user = User.query.filter(
        (User.username == username) | (User.email == username.lower())
    ).first()

    # 用户不存在时也记录（但不锁定，因为没有 user_id）
    if not user:
        logger.warning("登录失败：用户不存在", username=username, ip=ip_address)
        return error_response(401, '用户名或密码错误')

    # 检查账户锁定状态
    locked, remaining = is_account_locked(user.id)
    if locked:
        logger.warning("登录尝试：账户已锁定",
                       user_id=user.id, username=username,
                       remaining_seconds=remaining, ip=ip_address)
        return error_response(
            423,
            f'账户已锁定，请在 {remaining // 60} 分 {remaining % 60} 秒后重试',
            errors={
                'locked': True,
                'remaining_seconds': remaining,
                'max_failures': 5,
            },
        )

    # 验证密码
    if not check_password_hash(user.password_hash, password):
        record_login_failure(user.id, ip_address=ip_address, username=username)
        failures = get_login_failures(user.id)
        return error_response(
            401,
            '用户名或密码错误',
            errors={'failures': failures, 'max_failures': 5},
        )

    # 检查账户是否激活
    if not user.is_active:
        return error_response(403, '账号已被禁用')

    # 登录成功：重置失败计数
    reset_login_failures(user.id)

    # 更新最后登录时间
    user.update_last_login()

    # 生成 Token (identity 需要是字符串)
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    # 构建响应
    # Token 同时在 body 中返回（兼容 API 客户端和测试）和 httpOnly Cookie 中设置（前端安全使用）
    from flask import make_response
    response = make_response(success_response(
        data={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        },
        message='登录成功'
    ))

    # 设置 httpOnly Cookie（XSS 无法窃取，前端优先使用 Cookie 认证）
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前登录用户信息"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return error_response(404, '用户不存在')
    
    return success_response(data=user.to_dict())


@api_bp.route('/auth/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """修改个人信息"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return error_response(404, '用户不存在')
        
    data = request.get_json()
    
    if 'username' in data:
        username = data['username'].strip()
        if len(username) < 3 or len(username) > 50:
            return error_response(400, '用户名长度应为 3-50 个字符')
        if User.query.filter(User.username == username, User.id != user_id).first():
            return error_response(400, '用户名已被使用')
        user.username = username
        
    if 'email' in data:
        email = data['email'].strip().lower()
        if not is_valid_email(email):
            return error_response(400, '邮箱格式不正确')
        if User.query.filter(User.email == email, User.id != user_id).first():
            return error_response(400, '邮箱已被注册')
        user.email = email
        
    if 'avatar' in data:
        user.avatar = data['avatar']
        
    db.session.commit()
    
    return success_response(data=user.to_dict(), message='个人信息修改成功')


@api_bp.route('/auth/me/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传个人头像到 OSS"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return error_response(404, '用户不存在')
        
    if 'file' not in request.files:
        return error_response(400, '未找到文件')
        
    file = request.files['file']
    if file.filename == '':
        return error_response(400, '未选择文件')
        
    success, result = upload_to_oss(file, folder='avatars')
    if not success:
        return error_response(500, result)
        
    user.avatar = result
    db.session.commit()
    
    return success_response(data={'avatar': result}, message='头像上传成功')


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """刷新 Access Token"""
    user_id = get_current_user_id()
    access_token = create_access_token(identity=str(user_id))

    # 通过 httpOnly Cookie 设置新的 access_token，同时在 body 中返回（兼容性）
    from flask import make_response
    response = make_response(success_response(
        data={'access_token': access_token},
        message='Token 刷新成功'
    ))
    set_access_cookies(response, access_token)

    return response


@api_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    登出 - 注销当前 Token

    将当前 Access Token 加入黑名单，使其立即失效。
    清除 httpOnly Cookie。
    """
    from flask_jwt_extended import get_jwt
    from ..services.token_blacklist import blacklist_token

    jwt_data = get_jwt()
    jti = jwt_data.get('jti')
    exp_timestamp = jwt_data.get('exp')

    if jti and exp_timestamp:
        from datetime import datetime
        expires_at = datetime.utcfromtimestamp(exp_timestamp)
        blacklist_token(jti, expires_at)

    logger.info('User logged out', user_id=get_current_user_id())

    # 清除 httpOnly Cookie
    from flask import make_response
    response = make_response(success_response(message='已成功登出'))
    unset_jwt_cookies(response)

    return response


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
    
    # 验证新密码强度
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        return error_response(400, error_msg)
    
    # 更新密码
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return success_response(message='密码修改成功')


@api_bp.route('/auth/forgot-password', methods=['POST'])
@limiter.limit("3/minute")
@validate_json('email')
def forgot_password():
    """
    忘记密码 - 发送重置链接

    请求体:
        email: 注册邮箱地址

    注意: 当前实现直接返回 token（适用于无邮件服务的场景）。
    生产环境建议集成邮件服务发送重置链接。
    """
    data = request.get_json()
    email = data['email'].strip().lower()

    user = User.query.filter_by(email=email).first()

    # 不论用户是否存在，都返回相同消息（防止邮箱枚举攻击）
    if not user or not user.is_active:
        return success_response(message='如果该邮箱已注册，重置链接已发送')

    # 生成重置 Token（有效期 30 分钟）
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = generate_password_hash(reset_token)
    user.reset_token_expires = datetime.utcnow() + timedelta(minutes=30)
    db.session.commit()

    logger.info('Password reset requested', user_id=user.id, email=email)

    # TODO: 生产环境应通过邮件发送重置链接，而非直接返回 token
    # reset_url = f"{FRONTEND_URL}/reset-password?token={reset_token}"
    # send_reset_email(user.email, reset_url)

    response_data = {}
    # 仅在开发环境返回 token，生产环境不应暴露
    from flask import current_app
    if current_app.config.get('DEBUG'):
        response_data['reset_token'] = reset_token

    return success_response(
        data=response_data,
        message='如果该邮箱已注册，重置链接已发送'
    )


@api_bp.route('/auth/reset-password', methods=['POST'])
@limiter.limit("5/minute")
@validate_json('token', 'new_password')
def reset_password():
    """
    重置密码

    请求体:
        token: 重置 Token（从 forgot-password 接口获取）
        new_password: 新密码（至少8位，包含大小写字母、数字、特殊字符）
    """
    data = request.get_json()
    token = data['token']
    new_password = data['new_password']

    # 验证新密码强度
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        return error_response(400, error_msg)

    # 查找所有有待重置 token 的活跃用户（不能直接通过 token 查找，因为存的是 hash）
    users = User.query.filter(
        User.reset_token.isnot(None),
        User.reset_token_expires.isnot(None),
        User.is_active == True
    ).all()

    matched_user = None
    for user in users:
        if user.reset_token_expires < datetime.utcnow():
            continue
        if check_password_hash(user.reset_token, token):
            matched_user = user
            break

    if not matched_user:
        return error_response(400, '重置 Token 无效或已过期')

    # 更新密码，清除重置 token
    matched_user.password_hash = generate_password_hash(new_password)
    matched_user.reset_token = None
    matched_user.reset_token_expires = None
    db.session.commit()

    logger.info('Password reset completed', user_id=matched_user.id)

    return success_response(message='密码重置成功，请使用新密码登录')
