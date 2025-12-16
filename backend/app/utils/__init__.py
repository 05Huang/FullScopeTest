"""
工具函数模块
"""

from flask_jwt_extended import get_jwt_identity


def get_current_user_id():
    """
    获取当前用户 ID
    
    Returns:
        int: 用户 ID
    """
    identity = get_jwt_identity()
    return int(identity) if identity else None
