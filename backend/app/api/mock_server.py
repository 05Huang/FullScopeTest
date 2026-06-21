"""
独立 Mock Server API

提供 Mock Server 的 CRUD、规则管理、请求处理和日志查询。
"""

from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..utils.response import success_response, error_response
from ..core.logging import get_logger
from ..utils.exceptions import NotFoundError, ValidationError

logger = get_logger(__name__)


# ==================== Mock Server CRUD ====================

@api_bp.route('/mock-servers', methods=['GET'])
@jwt_required()
def get_mock_servers():
    """获取项目下的 Mock 服务器列表"""
    from ..services.mock_server_service import get_mock_server_service

    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return error_response(400, '缺少 project_id 参数')

    try:
        service = get_mock_server_service()
        servers = service.get_servers(project_id)
        return success_response(data=servers)
    except Exception as exc:
        logger.error('获取 Mock 服务器列表失败', error=str(exc))
        return error_response(500, f'获取失败: {str(exc)}')


@api_bp.route('/mock-servers', methods=['POST'])
@jwt_required()
def create_mock_server():
    """创建 Mock 服务器"""
    from ..services.mock_server_service import get_mock_server_service

    data = request.get_json() or {}
    if not data.get('name'):
        return error_response(400, '缺少服务器名称')
    if not data.get('project_id'):
        return error_response(400, '缺少 project_id')

    try:
        user_id = get_jwt_identity()
        service = get_mock_server_service()
        server = service.create_server(data, user_id=user_id)
        return success_response(data=server, message='Mock 服务器已创建', code=201)
    except Exception as exc:
        logger.error('创建 Mock 服务器失败', error=str(exc))
        return error_response(500, f'创建失败: {str(exc)}')


@api_bp.route('/mock-servers/<int:server_id>', methods=['GET'])
@jwt_required()
def get_mock_server(server_id):
    """获取 Mock 服务器详情（含规则）"""
    from ..services.mock_server_service import get_mock_server_service

    try:
        service = get_mock_server_service()
        server = service.get_server(server_id)
        return success_response(data=server)
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error('获取 Mock 服务器详情失败', error=str(exc))
        return error_response(500, f'获取失败: {str(exc)}')


@api_bp.route('/mock-servers/<int:server_id>', methods=['PUT'])
@jwt_required()
def update_mock_server(server_id):
    """更新 Mock 服务器"""
    from ..services.mock_server_service import get_mock_server_service

    data = request.get_json() or {}

    try:
        service = get_mock_server_service()
        server = service.update_server(server_id, data)
        return success_response(data=server, message='Mock 服务器已更新')
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error('更新 Mock 服务器失败', error=str(exc))
        return error_response(500, f'更新失败: {str(exc)}')


@api_bp.route('/mock-servers/<int:server_id>', methods=['DELETE'])
@jwt_required()
def delete_mock_server(server_id):
    """删除 Mock 服务器"""
    from ..services.mock_server_service import get_mock_server_service

    try:
        service = get_mock_server_service()
        service.delete_server(server_id)
        return success_response(message='Mock 服务器已删除')
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error('删除 Mock 服务器失败', error=str(exc))
        return error_response(500, f'删除失败: {str(exc)}')


# ==================== Mock Rule 管理 ====================

@api_bp.route('/mock-servers/<int:server_id>/rules', methods=['POST'])
@jwt_required()
def create_mock_rule(server_id):
    """创建 Mock 规则"""
    from ..services.mock_server_service import get_mock_server_service

    data = request.get_json() or {}
    if not data.get('name'):
        return error_response(400, '缺少规则名称')
    if not data.get('match_path'):
        return error_response(400, '缺少匹配路径')

    try:
        service = get_mock_server_service()
        rule = service.create_rule(server_id, data)
        return success_response(data=rule, message='规则已创建', code=201)
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error('创建 Mock 规则失败', error=str(exc))
        return error_response(500, f'创建失败: {str(exc)}')


@api_bp.route('/mock-rules/<int:rule_id>', methods=['PUT'])
@jwt_required()
def update_mock_rule(rule_id):
    """更新 Mock 规则"""
    from ..services.mock_server_service import get_mock_server_service

    data = request.get_json() or {}

    try:
        service = get_mock_server_service()
        rule = service.update_rule(rule_id, data)
        return success_response(data=rule, message='规则已更新')
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error('更新 Mock 规则失败', error=str(exc))
        return error_response(500, f'更新失败: {str(exc)}')


@api_bp.route('/mock-rules/<int:rule_id>', methods=['DELETE'])
@jwt_required()
def delete_mock_rule(rule_id):
    """删除 Mock 规则"""
    from ..services.mock_server_service import get_mock_server_service

    try:
        service = get_mock_server_service()
        service.delete_rule(rule_id)
        return success_response(message='规则已删除')
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error('删除 Mock 规则失败', error=str(exc))
        return error_response(500, f'删除失败: {str(exc)}')


# ==================== Mock 请求处理 ====================

@api_bp.route('/mock/<int:server_id>/<path:subpath>', methods=[
    'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'
])
def mock_server_proxy(server_id, subpath):
    """
    Mock Server 代理端点

    接收请求，匹配规则，返回 Mock 响应。
    不需要 JWT 认证（方便前端开发直接调用）。
    """
    from ..services.mock_server_service import get_mock_server_service

    # 处理 OPTIONS
    if request.method == 'OPTIONS':
        resp = make_response()
        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '')
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp

    try:
        service = get_mock_server_service()
        body = request.get_data(as_text=True)
        result = service.handle_request(
            server_id=server_id,
            method=request.method,
            path='/' + subpath,
            query_params=dict(request.args),
            headers={k: v for k, v in request.headers},
            body=body,
        )

        resp = make_response(result.get('body', ''))
        resp.status_code = result.get('code', 200)
        for k, v in (result.get('headers') or {}).items():
            resp.headers[k] = v
        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '')
        if 'Content-Type' not in result.get('headers', {}):
            resp.headers['Content-Type'] = 'application/json'

        # 添加 Mock 标识
        if result.get('rule_name'):
            resp.headers['X-Mock-Rule'] = result['rule_name']
        resp.headers['X-Mock-Server-ID'] = str(server_id)

        return resp

    except NotFoundError:
        return error_response(404, 'Mock 服务器不存在')
    except Exception as exc:
        logger.error('Mock 请求处理失败', server_id=server_id, error=str(exc))
        return error_response(500, f'Mock 请求处理失败: {str(exc)}')


# ==================== 请求日志 ====================

@api_bp.route('/mock-servers/<int:server_id>/logs', methods=['GET'])
@jwt_required()
def get_mock_request_logs(server_id):
    """获取 Mock 请求日志"""
    from ..services.mock_server_service import get_mock_server_service

    limit = request.args.get('limit', 100, type=int)

    try:
        service = get_mock_server_service()
        logs = service.get_request_logs(server_id, limit=limit)
        return success_response(data=logs)
    except Exception as exc:
        logger.error('获取请求日志失败', error=str(exc))
        return error_response(500, f'获取失败: {str(exc)}')


@api_bp.route('/mock-servers/<int:server_id>/logs', methods=['DELETE'])
@jwt_required()
def clear_mock_request_logs(server_id):
    """清空 Mock 请求日志"""
    from ..services.mock_server_service import get_mock_server_service

    try:
        service = get_mock_server_service()
        count = service.clear_request_logs(server_id)
        return success_response(data={'deleted': count}, message='日志已清空')
    except Exception as exc:
        logger.error('清空日志失败', error=str(exc))
        return error_response(500, f'清空失败: {str(exc)}')
