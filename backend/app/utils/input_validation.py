"""
输入验证与安全加固工具模块

提供统一的输入验证、XSS 防护、文件上传验证、脚本内容沙箱化等功能。
"""

import re
import os
from typing import Dict, Any, Optional, List
from functools import wraps
from flask import request, current_app
from ..utils.response import error_response
from ..core.logging import get_logger

logger = get_logger(__name__)

# 文件上传白名单（MIME 类型）
ALLOWED_UPLOAD_TYPES = {
    'image/png', 'image/jpeg', 'image/gif', 'image/webp',
    'application/pdf', 'text/plain', 'text/csv',
    'application/json', 'application/xml', 'application/yaml',
    'application/x-yaml', 'text/yaml', 'text/xml',
    'application/octet-stream',
}

# 脚本内容黑名单（可执行代码模式）
SCRIPT_BLOCKED_PATTERNS = [
    re.compile(r'import\s+subprocess', re.IGNORECASE),
    re.compile(r'from\s+subprocess\s+import', re.IGNORECASE),
    re.compile(r'os\.system\s*\(', re.IGNORECASE),
    re.compile(r'os\.popen\s*\(', re.IGNORECASE),
    re.compile(r'exec\s*\(', re.IGNORECASE),
    re.compile(r'eval\s*\(', re.IGNORECASE),
    re.compile(r'__import__\s*\(', re.IGNORECASE),
    re.compile(r'compile\s*\(', re.IGNORECASE),
    re.compile(r'open\s*\(.+,\s*["\']w["\']', re.IGNORECASE),
    re.compile(r'rm\s+-rf\s+/', re.IGNORECASE),
    re.compile(r'shutil\.rmtree', re.IGNORECASE),
]

# XSS 防护：HTML 转义映射
HTML_ESCAPE_MAP = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
}


def sanitize_html(text: str) -> str:
    """HTML 转义防护 XSS 攻击"""
    if not text:
        return text
    for char, replacement in HTML_ESCAPE_MAP.items():
        text = text.replace(char, replacement)
    return text


def validate_string_length(value: str, min_len: int = 1, max_len: int = 10000, field_name: str = 'input') -> Optional[str]:
    """验证字符串长度，返回错误消息或 None"""
    if value is None:
        return f'{field_name} 不能为空' if min_len > 0 else None
    if len(value) < min_len:
        return f'{field_name} 长度至少 {min_len} 个字符'
    if len(value) > max_len:
        return f'{field_name} 长度不能超过 {max_len} 个字符'
    return None


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validate_url(url: str) -> bool:
    """验证 URL 格式"""
    return bool(re.match(r'^https?://[^\s/$.?#].[^\s]*$', url, re.IGNORECASE))


def sanitize_script_content(content: str) -> str:
    """沙箱化处理脚本内容，禁止存储可执行的服务端代码"""
    if not content:
        return content
    sanitized = content
    for pattern in SCRIPT_BLOCKED_PATTERNS:
        sanitized = pattern.sub('# [BLOCKED]', sanitized)
    sanitized = re.sub(r'^#!.*\n', '', sanitized)
    return sanitized


def detect_script_danger(content: str) -> List[Dict[str, Any]]:
    """检测脚本中的危险代码模式"""
    threats = []
    for i, pattern in enumerate(SCRIPT_BLOCKED_PATTERNS):
        matches = pattern.findall(content)
        if matches:
            threats.append({'pattern_index': i, 'matches': matches[:5], 'count': len(matches)})
    return threats


def validate_file_upload(file) -> Dict[str, Any]:
    """验证文件上传"""
    if not file or not file.filename:
        return {'valid': False, 'error': '未选择文件'}
    if len(file.filename) > 255:
        return {'valid': False, 'error': '文件名过长'}

    ext = os.path.splitext(file.filename)[1].lower()
    blocked_extensions = ['.exe', '.bat', '.cmd', '.sh', '.bash', '.ps1',
                          '.php', '.jsp', '.asp', '.aspx', '.py', '.rb', '.pl']
    if ext in blocked_extensions:
        return {'valid': False, 'error': f'不允许上传 {ext} 类型的文件'}

    if file.content_type and file.content_type not in ALLOWED_UPLOAD_TYPES:
        return {'valid': False, 'error': f'不支持的文件类型: {file.content_type}'}

    max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    if file_size > max_size:
        return {'valid': False, 'error': f'文件大小超过限制 ({max_size // (1024 * 1024)}MB)'}
    if file_size == 0:
        return {'valid': False, 'error': '文件为空'}

    return {'valid': True, 'error': None}


def validate_json_body(*required_fields):
    """验证 JSON 请求体装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return error_response(400, '请求必须是 JSON 格式')
            data = request.get_json()
            if not data:
                return error_response(400, '请求体不能为空')
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return error_response(400, f'缺少必需字段: {", ".join(missing_fields)}')
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_query_params(*required_params):
    """验证查询参数装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            missing = [param for param in required_params if not request.args.get(param)]
            if missing:
                return error_response(400, f'缺少必需参数: {", ".join(missing)}')
            return f(*args, **kwargs)
        return wrapper
    return decorator
