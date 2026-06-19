"""
FastAPI 认证模块

将 JWT 验证逻辑重写为 FastAPI Depends
实现 get_current_user、get_current_organization 依赖
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from ...extensions import db
from ...models.user import User
from ...core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["auth"])
security = HTTPBearer()


class TokenPayload(BaseModel):
    """JWT Token Payload"""
    sub: str
    exp: Optional[int] = None
    iat: Optional[int] = None
    type: Optional[str] = None


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=100, description='用户名或邮箱')
    password: str = Field(..., min_length=1, max_length=128, description='密码')


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    user_id: int
    username: str


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description='用户名')
    email: str = Field(..., description='邮箱地址')
    password: str = Field(..., min_length=8, max_length=128, description='密码')


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """获取当前用户 - FastAPI Depends"""
    from flask_jwt_extended import decode_token

    try:
        token = credentials.credentials
        decoded = decode_token(token)
        user_id = decoded.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail='Invalid token')

        user = User.query.get(int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail='User not found')
        if not user.is_active:
            raise HTTPException(status_code=403, detail='Account disabled')

        return user
    except Exception as exc:
        logger.error('Failed to authenticate user', error=str(exc))
        raise HTTPException(status_code=401, detail='Authentication failed')


def get_current_organization(user: User = Depends(get_current_user)) -> Optional[int]:
    """获取当前组织 - FastAPI Depends"""
    from flask import g
    return getattr(g, 'organization_id', None)


@router.post("/login", response_model=LoginResponse)
async def login_v2(request_data: LoginRequest):
    """用户登录 - v2 API"""
    from werkzeug.security import check_password_hash
    from flask_jwt_extended import create_access_token, create_refresh_token

    user = User.query.filter(
        (User.username == request_data.username) | (User.email == request_data.username.lower())
    ).first()

    if not user or not check_password_hash(user.password_hash, request_data.password):
        raise HTTPException(status_code=401, detail='用户名或密码错误')

    if not user.is_active:
        raise HTTPException(status_code=403, detail='账号已被禁用')

    user.update_last_login()
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        username=user.username,
    )


@router.post("/register")
async def register_v2(request_data: RegisterRequest):
    """用户注册 - v2 API"""
    from werkzeug.security import generate_password_hash

    # 检查用户名是否已存在
    if User.query.filter_by(username=request_data.username).first():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail='用户名已被使用')

    # 检查邮箱是否已存在
    if User.query.filter_by(email=request_data.email).first():
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail='邮箱已被注册')

    user = User(
        username=request_data.username,
        email=request_data.email,
        password_hash=generate_password_hash(request_data.password)
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "注册成功", "user_id": user.id, "username": user.username}


@router.get("/me")
async def get_current_user_v2(user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return user.to_dict()


@router.put("/me")
async def update_profile_v2(user: User = Depends(get_current_user)):
    """修改个人信息"""
    from ..utils.validators import is_valid_email

    data = request.json

    if 'username' in data:
        username = data['username'].strip()
        if len(username) < 3 or len(username) > 50:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail='用户名长度应为 3-50 个字符')
        if User.query.filter(User.username == username, User.id != user.id).first():
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail='用户名已被使用')
        user.username = username

    if 'email' in data:
        email = data['email'].strip().lower()
        if not is_valid_email(email):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail='邮箱格式不正确')
        if User.query.filter(User.email == email, User.id != user.id).first():
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail='邮箱已被注册')
        user.email = email

    if 'avatar' in data:
        user.avatar = data['avatar']

    db.session.commit()
    return user.to_dict()


@router.post("/refresh")
async def refresh_token_v2(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """刷新 Access Token"""
    from flask_jwt_extended import create_access_token, decode_token

    try:
        token = credentials.credentials
        decoded = decode_token(token)
        user_id = decoded.get('sub')
        access_token = create_access_token(identity=str(user_id))
        return {"access_token": access_token}
    except Exception as exc:
        raise HTTPException(status_code=401, detail='Token refresh failed')
