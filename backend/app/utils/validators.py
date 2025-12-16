"""
数据验证工具

提供常用的数据验证函数
"""

import re
from functools import wraps
from flask import request
from .response import error_response


def validate_json(*required_fields):
    """
    验证 JSON 请求体装饰器
    
    Args:
        required_fields: 必需的字段名列表
    
    Usage:
        @validate_json('name', 'email')
        def create_user():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 检查 Content-Type
            if not request.is_json:
                return error_response(400, '请求必须是 JSON 格式')
            
            data = request.get_json()
            if not data:
                return error_response(400, '请求体不能为空')
            
            # 检查必需字段
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return error_response(400, f'缺少必需字段: {", ".join(missing_fields)}')
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def is_valid_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_required(data, required_fields):
    """
    验证必需字段
    
    Args:
        data: 要验证的字典数据
        required_fields: 必需的字段名列表
    
    Returns:
        str: 错误信息，如果验证通过则返回 None
    """
    if not data:
        return '请求数据不能为空'
    
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return f'缺少必需字段: {", ".join(missing_fields)}'
    
    return None


def is_valid_url(url):
    """验证 URL 格式"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url, re.IGNORECASE))


def is_valid_http_method(method):
    """验证 HTTP 方法"""
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    return method.upper() in valid_methods
