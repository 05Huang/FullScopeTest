"""
统一响应格式工具

提供标准化的 API 响应格式
"""

from flask import jsonify
from datetime import datetime


def success_response(data=None, message='success', code=200):
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: HTTP 状态码
    
    Returns:
        tuple: (响应体, 状态码)
    """
    response = {
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    return jsonify(response), code


def error_response(code, message, errors=None):
    """
    错误响应
    
    Args:
        code: HTTP 状态码
        message: 错误消息
        errors: 详细错误信息
    
    Returns:
        tuple: (响应体, 状态码)
    """
    response = {
        'code': code,
        'message': message,
        'errors': errors,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    return jsonify(response), code


def paginate_response(items, total, page, per_page, message='success'):
    """
    分页响应
    
    Args:
        items: 数据列表
        total: 总数量
        page: 当前页码
        per_page: 每页数量
        message: 响应消息
    
    Returns:
        tuple: (响应体, 状态码)
    """
    response = {
        'code': 200,
        'message': message,
        'data': {
            'items': items,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        },
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    return jsonify(response), 200
