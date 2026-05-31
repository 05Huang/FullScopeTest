"""
Pydantic v2 Schema - 认证相关
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TokenPayload(BaseModel):
    """JWT Token Payload"""
    sub: str
    exp: Optional[int] = None
    iat: Optional[int] = None
    type: Optional[str] = None


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    email: str
    avatar: Optional[str] = None
    role: str = 'member'
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=100, description='用户名或邮箱')
    password: str = Field(..., min_length=1, max_length=128, description='密码')


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    user: UserResponse


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description='用户名')
    email: str = Field(..., description='邮箱地址')
    password: str = Field(..., min_length=8, max_length=128, description='密码')


class RefreshRequest(BaseModel):
    """刷新 Token 请求"""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)


class ProfileUpdateRequest(BaseModel):
    """修改个人信息请求"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = None
    avatar: Optional[str] = None
