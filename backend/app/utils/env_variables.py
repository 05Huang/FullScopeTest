"""
环境变量处理工具

支持在测试用例中使用环境变量 {{variable_name}}
内置变量：{{$timestamp}}、{{$random_int}}、{{$uuid}}
"""

import re
import uuid
import time
import random
from typing import Dict, Any, Optional


# 内置动态变量（每次调用生成新值）
BUILTIN_VARIABLES = {
    "$timestamp": lambda: str(int(time.time())),
    "$random_int": lambda: str(random.randint(100000, 999999)),
    "$uuid": lambda: str(uuid.uuid4()),
}


def replace_variables(text: str, variables: Dict[str, Any]) -> str:
    """
    替换文本中的变量 (支持 {{variable_name}} 格式，与 Postman 一致)
    支持内置变量：{{$timestamp}}、{{$random_int}}、{{$uuid}}
    支持变量嵌套：{{api_url}}/users/{{user_id}}

    Args:
        text: 原始文本，包含 {{variable_name}} 格式的变量
        variables: 变量字典

    Returns:
        替换后的文本
    """
    if not text or not isinstance(text, str):
        return text

    # 合并内置变量和用户变量
    all_vars = {}
    for key, gen_fn in BUILTIN_VARIABLES.items():
        all_vars[key] = gen_fn()
    if variables:
        all_vars.update(variables)

    if not all_vars:
        return text

    # 查找所有 {{variable_name}} 格式的变量
    pattern = r'\{\{([^}]+)\}\}'

    def replacer(match):
        var_name = match.group(1).strip()
        # 先检查内置变量（带 $ 前缀）
        if var_name in BUILTIN_VARIABLES:
            return BUILTIN_VARIABLES[var_name]()
        # 再检查用户变量
        return str(all_vars.get(var_name, match.group(0)))

    # 支持多轮替换（处理嵌套变量）
    max_rounds = 3
    for _ in range(max_rounds):
        new_text = re.sub(pattern, replacer, text)
        if new_text == text:
            break
        text = new_text

    return text


def replace_variables_in_dict(data: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归替换字典中的变量
    
    Args:
        data: 包含变量的字典
        variables: 变量字典
        
    Returns:
        替换后的字典
    """
    if not data or not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = replace_variables(value, variables)
        elif isinstance(value, dict):
            result[key] = replace_variables_in_dict(value, variables)
        elif isinstance(value, list):
            result[key] = [
                replace_variables(item, variables) if isinstance(item, str)
                else replace_variables_in_dict(item, variables) if isinstance(item, dict)
                else item
                for item in value
            ]
        else:
            result[key] = value
    
    return result


def extract_variables(text: str) -> list:
    """
    从文本中提取所有变量名 (支持 {{variable_name}} 格式)

    Args:
        text: 包含 {{variable_name}} 格式变量的文本

    Returns:
        变量名列表

    Example:
        >>> extract_variables("http://api.com/{{version}}/user/{{id}}")
        ['version', 'id']
    """
    if not text or not isinstance(text, str):
        return []

    pattern = r'\{\{([^}]+)\}\}'
    return re.findall(pattern, text)


def get_environment_variables(environment_id: int, db) -> Optional[Dict[str, Any]]:
    """
    获取环境的变量字典

    Args:
        environment_id: 环境 ID
        db: 数据库实例

    Returns:
        环境变量字典，如果环境不存在则返回 None
    """
    from ..models.environment import Environment

    env = db.session.get(Environment, environment_id)
    if not env:
        return None

    return env.variables or {}


def merge_headers_with_env(headers: Dict[str, str], environment_id: int, db) -> Dict[str, str]:
    """
    合并请求头和环境的公共请求头

    Args:
        headers: 用例的请求头
        environment_id: 环境 ID
        db: 数据库实例

    Returns:
        合并后的请求头
    """
    from ..models.environment import Environment

    env = db.session.get(Environment, environment_id)
    if not env:
        return headers or {}

    # 环境的公共请求头
    env_headers = env.headers or {}

    # 合并（用例的请求头优先级更高）
    result = {}
    result.update(env_headers)
    if headers:
        result.update(headers)

    return result
