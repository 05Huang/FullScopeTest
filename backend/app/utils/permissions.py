"""
权限控制模块

提供角色和权限检查的装饰器和工具函数
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..models.user import User, ROLE_PERMISSIONS
from .response import error_response


def get_current_user() -> User:
    """获取当前用户对象"""
    identity = get_jwt_identity()
    if not identity:
        return None
    return User.query.get(int(identity))


def require_role(*roles):
    """
    角色检查装饰器

    用法:
        @require_role('admin', 'member')
        def my_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()

            if not user:
                return error_response(401, '未认证')

            if not user.is_active:
                return error_response(403, '账号已被禁用')

            if user.role not in roles:
                return error_response(403, f'需要角色: {", ".join(roles)}')

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_permission(*permissions):
    """
    权限检查装饰器

    用法:
        @require_permission('write', 'delete')
        def my_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()

            if not user:
                return error_response(401, '未认证')

            if not user.is_active:
                return error_response(403, '账号已被禁用')

            user_permissions = ROLE_PERMISSIONS.get(user.role, [])
            for perm in permissions:
                if perm not in user_permissions:
                    return error_response(403, f'缺少权限: {perm}')

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_admin(f):
    """
    管理员检查装饰器

    用法:
        @require_admin
        def my_endpoint():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()

        if not user:
            return error_response(401, '未认证')

        if not user.is_active:
            return error_response(403, '账号已被禁用')

        if not user.is_admin():
            return error_response(403, '需要管理员权限')

        return f(*args, **kwargs)
    return decorated_function


def check_project_permission(user_id: int, project_id: int) -> bool:
    """
    检查用户是否有项目访问权限

    Args:
        user_id: 用户 ID
        project_id: 项目 ID

    Returns:
        bool: 是否有权限
    """
    from ..models.project import Project

    # 管理员可以访问所有项目
    user = User.query.get(user_id)
    if user and user.is_admin():
        return True

    # 检查项目所有权
    project = Project.query.get(project_id)
    if not project:
        return False

    return project.user_id == user_id
