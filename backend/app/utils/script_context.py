"""
脚本上下文构建器

为前置脚本和后置断言准备执行上下文
"""

import json
from typing import Dict, Any, Optional


def build_pre_script_context(
    environment_vars: Dict[str, Any],
    request_data: Dict[str, Any],
    variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    构建前置脚本的执行上下文

    Args:
        environment_vars: 环境变量字典
        request_data: 请求数据 { method, url, headers, params, body }
        variables: 临时变量字典

    Returns:
        执行上下文字典
    """
    return {
        'environment': environment_vars or {},
        'variables': variables or {},
        'request': {
            'method': request_data.get('method', 'GET'),
            'url': request_data.get('url', ''),
            'headers': request_data.get('headers', {}) or {},
            'params': request_data.get('params', {}) or {},
            'body': request_data.get('body')
        }
    }


def build_post_script_context(
    environment_vars: Dict[str, Any],
    response_data: Dict[str, Any],
    variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    构建后置断言的执行上下文

    Args:
        environment_vars: 环境变量字典
        response_data: 响应数据 { status, headers, body, responseTime, responseSize }
        variables: 临时变量字典

    Returns:
        执行上下文字典
    """
    # 解析响应体
    body = response_data.get('body')
    body_json = None
    if isinstance(body, dict):
        body_json = body
    elif isinstance(body, str):
        try:
            body_json = json.loads(body)
        except:
            pass

    return {
        'environment': environment_vars or {},
        'variables': variables or {},
        'response': {
            'status': response_data.get('status_code'),
            'code': response_data.get('status_code'),  # 别名，与 Postman 一致
            'headers': response_data.get('headers', {}) or {},
            'body': body_json if body_json is not None else body,
            'responseTime': response_data.get('response_time', 0),
            'size': response_data.get('response_size', 0)
        }
    }


def apply_pre_script_changes(
    request_data: Dict[str, Any],
    script_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    应用前置脚本的修改到请求数据

    Args:
        request_data: 原始请求数据
        script_result: 脚本执行结果（包含 request_changes）

    Returns:
        修改后的请求数据
    """
    if not script_result.get('passed'):
        return request_data

    request_changes = script_result.get('request_changes', {})

    # 应用 URL 修改
    if 'url' in request_changes:
        request_data['url'] = request_changes['url']

    # 应用 Headers 修改（追加）
    if 'headers' in request_changes:
        new_headers = request_changes['headers']
        existing_headers = request_data.get('headers', {}) or {}
        # 合并 headers
        request_data['headers'] = {**existing_headers, **new_headers}

    # 应用 Body 修改
    if 'body' in request_changes:
        request_data['body'] = request_changes['body']

    return request_data


def apply_env_changes(
    environment_vars: Dict[str, Any],
    script_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    应用脚本的环境变量修改

    Args:
        environment_vars: 原始环境变量
        script_result: 脚本执行结果（包含 env_changes）

    Returns:
        更新后的环境变量
    """
    if not script_result.get('passed'):
        return environment_vars

    env_changes = script_result.get('env_changes', {})
    if env_changes:
        environment_vars.update(env_changes)

    return environment_vars


def calculate_case_passed(
    script_result: Dict[str, Any],
    http_status: Optional[int] = None,
    has_script: bool = False
) -> bool:
    """
    计算用例最终是否通过

    判定规则：
    1. 有前置脚本且失败 → 用例失败
    2. 有后置断言且失败 → 用例失败
    3. 无脚本但 HTTP 错误 → 用例失败
    4. HTTP 成功 → 用例通过

    Args:
        script_result: 脚本执行结果（包含 pre_script 和 post_script）
        http_status: HTTP 状态码
        has_script: 是否有脚本执行

    Returns:
        是否通过
    """
    # 检查前置脚本结果
    pre_script = script_result.get('pre_script', {})
    if pre_script.get('executed') and not pre_script.get('passed', True):
        return False

    # 检查后置断言结果
    post_script = script_result.get('post_script', {})
    if post_script.get('executed') and not post_script.get('passed', True):
        return False

    # 有脚本的情况，脚本通过则用例通过
    if has_script:
        return True

    # 没有脚本的情况，按 HTTP 状态码判断
    if http_status is not None:
        return http_status < 400

    return True
