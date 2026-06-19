"""
Webhook 调试器 API

提供 Webhook URL 创建、请求记录、日志查询功能。
"""

from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..utils.response import success_response, error_response
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/webhook-debugger', methods=['GET'])
@jwt_required()
def list_debug_webhooks():
    """列出所有调试 Webhook"""
    from ..services.webhook_debugger_service import get_webhook_debugger_service
    service = get_webhook_debugger_service()
    webhooks = service.list_webhooks()
    return success_response(data=webhooks)


@api_bp.route('/webhook-debugger', methods=['POST'])
@jwt_required()
def create_debug_webhook():
    """创建调试 Webhook"""
    from ..services.webhook_debugger_service import get_webhook_debugger_service
    data = request.get_json() or {}
    name = data.get('name', '')
    service = get_webhook_debugger_service()
    result = service.create_webhook(name=name)
    return success_response(data=result, message='Webhook 已创建', code=201)


@api_bp.route('/webhook-debugger/<token>/requests', methods=['GET'])
@jwt_required()
def get_debug_webhook_requests(token):
    """获取 Webhook 请求日志"""
    from ..services.webhook_debugger_service import get_webhook_debugger_service
    limit = request.args.get('limit', 100, type=int)
    service = get_webhook_debugger_service()
    result = service.get_requests(token, limit=limit)
    if 'error' in result:
        return error_response(404, result['error'])
    return success_response(data=result)


@api_bp.route('/webhook-debugger/<token>/requests', methods=['DELETE'])
@jwt_required()
def clear_debug_webhook_requests(token):
    """清空 Webhook 请求日志"""
    from ..services.webhook_debugger_service import get_webhook_debugger_service
    service = get_webhook_debugger_service()
    service.clear_requests(token)
    return success_response(message='日志已清空')


@api_bp.route('/webhook/<token>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def receive_webhook(token):
    """接收 Webhook 请求（无需认证）"""
    from ..services.webhook_debugger_service import get_webhook_debugger_service
    service = get_webhook_debugger_service()
    result = service.record_request(
        token=token,
        method=request.method,
        path=request.path,
        headers={k: v for k, v in request.headers},
        body=request.get_data(as_text=True),
        query_params=dict(request.args),
    )
    if 'error' in result:
        return error_response(404, result['error'])

    resp = make_response('{"ok": true}')
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp