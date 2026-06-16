"""
审计日志装饰器

提供 @audit_action 装饰器，用于在 API 端点上声明审计记录。
装饰器在请求成功完成后自动记录审计日志。

用法：
    @api_bp.route('/projects', methods=['POST'])
    @jwt_required()
    @audit_action('create', 'project')
    def create_project():
        ...

    @api_bp.route('/projects/<int:project_id>', methods=['PUT'])
    @jwt_required()
    @audit_action('update', 'project', resource_id_param='project_id')
    def update_project(project_id):
        ...
"""
from functools import wraps
from flask import request, g
from ..services.audit_log_service import log_action
from ..core.logging import get_logger

logger = get_logger(__name__)


def audit_action(action: str, resource_type: str, resource_id_param: str = None):
    """
    审计日志装饰器

    在 API 端点成功执行后记录审计日志。
    仅在响应状态码 < 400 时记录（成功操作）。

    Args:
        action: 操作类型（create/update/delete/execute/login/logout）
        resource_type: 资源类型（project/test_case/test_run/...）
        resource_id_param: URL 参数中的资源 ID 参数名（可选）
            如 'project_id' → 从 kwargs 中获取
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 执行原始函数
            result = f(*args, **kwargs)

            # 仅在成功时记录（Flask 返回 tuple (response, status_code) 或 Response 对象）
            try:
                status_code = _get_status_code(result)
                if status_code and status_code < 400:
                    # 获取资源 ID
                    resource_id = None
                    if resource_id_param and resource_id_param in kwargs:
                        resource_id = kwargs[resource_id_param]

                    # 尝试从响应体中提取 resource_id
                    if resource_id is None:
                        resource_id = _extract_resource_id(result)

                    # 获取变更信息
                    changes = _extract_changes(result, action)

                    log_action(
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        new_values=changes,
                    )
            except Exception as exc:
                logger.warning("审计日志记录失败", error=str(exc))

            return result
        return decorated_function
    return decorator


def _get_status_code(result) -> int:
    """从 Flask 响应中提取状态码"""
    if isinstance(result, tuple):
        # (response, status_code) 或 (response, status_code, headers)
        if len(result) >= 2 and isinstance(result[1], int):
            return result[1]
    # Response 对象
    if hasattr(result, 'status_code'):
        return result.status_code
    return None


def _extract_resource_id(result) -> int:
    """尝试从响应体中提取资源 ID"""
    try:
        if isinstance(result, tuple):
            resp = result[0]
        else:
            resp = result
        if hasattr(resp, 'get_json'):
            data = resp.get_json()
            if isinstance(data, dict):
                # 尝试从 data.data.id 中获取
                inner = data.get('data', {})
                if isinstance(inner, dict):
                    return inner.get('id')
    except Exception:
        pass
    return None


def _extract_changes(result, action: str) -> dict:
    """从响应中提取变更信息"""
    try:
        if isinstance(result, tuple):
            resp = result[0]
        else:
            resp = result
        if hasattr(resp, 'get_json'):
            data = resp.get_json()
            if isinstance(data, dict):
                inner = data.get('data', {})
                if isinstance(inner, dict):
                    # 对于 create/update，记录关键字段
                    return {
                        'message': data.get('message', ''),
                        'fields': list(inner.keys())[:10],
                    }
    except Exception:
        pass
    return {'action': action}