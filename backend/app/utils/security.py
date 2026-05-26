"""
安全工具模块

提供 HMAC 签名验证、日志脱敏等安全功能
"""

import hashlib
import hmac
import re
from functools import wraps
from flask import request, current_app


def verify_hmac_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    验证 HMAC-SHA256 签名

    Args:
        payload: 请求体字节
        signature: 请求头中的签名 (格式: sha256=xxxx)
        secret: Webhook 密钥

    Returns:
        bool: 签名是否有效
    """
    if not signature or not secret:
        return False

    # 支持 GitHub 风格的签名格式: sha256=xxxx
    if signature.startswith('sha256='):
        signature = signature[7:]

    expected = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


def generate_hmac_signature(payload: bytes, secret: str) -> str:
    """
    生成 HMAC-SHA256 签名

    Args:
        payload: 请求体字节
        secret: Webhook 密钥

    Returns:
        str: 签名 (格式: sha256=xxxx)
    """
    signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return f'sha256={signature}'


# 敏感字段模式
SENSITIVE_PATTERNS = [
    (re.compile(r'(password|passwd|pwd)\s*[=:]\s*\S+', re.IGNORECASE), r'\1=***'),
    (re.compile(r'(secret|token|key|api_key|apikey|access_key)\s*[=:]\s*\S+', re.IGNORECASE), r'\1=***'),
    (re.compile(r'(authorization)\s*:\s*\S+', re.IGNORECASE), r'\1: ***'),
    (re.compile(r'Bearer\s+\S+', re.IGNORECASE), 'Bearer ***'),
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '***@***.***'),
    (re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'), '****-****-****-****'),
]


def sanitize_log_message(message: str) -> str:
    """
    脱敏日志消息中的敏感信息

    Args:
        message: 原始日志消息

    Returns:
        str: 脱敏后的日志消息
    """
    result = message
    for pattern, replacement in SENSITIVE_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def sanitize_dict(data: dict, sensitive_keys: list = None) -> dict:
    """
    脱敏字典中的敏感字段

    Args:
        data: 原始字典
        sensitive_keys: 需要脱敏的键列表，默认为常见敏感字段

    Returns:
        dict: 脱敏后的字典
    """
    if sensitive_keys is None:
        sensitive_keys = [
            'password', 'passwd', 'pwd',
            'secret', 'token', 'key', 'api_key', 'apikey',
            'access_key_id', 'access_key_secret',
            'authorization', 'jwt', 'refresh_token',
        ]

    result = {}
    for k, v in data.items():
        if any(sensitive in k.lower() for sensitive in sensitive_keys):
            if isinstance(v, str) and len(v) > 4:
                result[k] = v[:2] + '*' * (len(v) - 4) + v[-2:]
            else:
                result[k] = '***'
        elif isinstance(v, dict):
            result[k] = sanitize_dict(v, sensitive_keys)
        elif isinstance(v, list):
            result[k] = [sanitize_dict(item, sensitive_keys) if isinstance(item, dict) else item for item in v]
        else:
            result[k] = v
    return result
