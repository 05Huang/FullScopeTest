"""
API 健康监控 API

提供 API 端点的健康检查配置、执行和统计查询。
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..utils.response import success_response, error_response
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/health-monitor', methods=['GET'])
@jwt_required()
def list_monitors():
    """列出所有监控规则"""
    from ..services.health_monitor_service import get_health_monitor_service
    service = get_health_monitor_service()
    monitors = service.list_monitors()
    return success_response(data=monitors)


@api_bp.route('/health-monitor', methods=['POST'])
@jwt_required()
def create_monitor():
    """创建监控规则"""
    from ..services.health_monitor_service import get_health_monitor_service
    data = request.get_json() or {}
    if not data.get('url'):
        return error_response(400, '缺少监控 URL')
    if not data.get('name'):
        return error_response(400, '缺少监控名称')

    service = get_health_monitor_service()
    result = service.create_monitor(data)
    return success_response(data=result, message='监控规则已创建', code=201)


@api_bp.route('/health-monitor/<int:monitor_id>', methods=['GET'])
@jwt_required()
def get_monitor(monitor_id):
    """获取监控详情"""
    from ..services.health_monitor_service import get_health_monitor_service
    service = get_health_monitor_service()
    result = service.get_monitor(monitor_id)
    if not result:
        return error_response(404, '监控规则不存在')
    return success_response(data=result)


@api_bp.route('/health-monitor/<int:monitor_id>', methods=['DELETE'])
@jwt_required()
def delete_monitor(monitor_id):
    """删除监控规则"""
    from ..services.health_monitor_service import get_health_monitor_service
    service = get_health_monitor_service()
    if service.delete_monitor(monitor_id):
        return success_response(message='监控规则已删除')
    return error_response(404, '监控规则不存在')


@api_bp.route('/health-monitor/<int:monitor_id>/check', methods=['POST'])
@jwt_required()
def run_health_check(monitor_id):
    """执行一次健康检查"""
    from ..services.health_monitor_service import get_health_monitor_service
    service = get_health_monitor_service()
    result = service.run_check(monitor_id)
    if 'error' in result:
        return error_response(400, result['error'])
    return success_response(data=result, message='检查完成')


@api_bp.route('/health-monitor/<int:monitor_id>/stats', methods=['GET'])
@jwt_required()
def get_uptime_stats(monitor_id):
    """获取可用率统计"""
    from ..services.health_monitor_service import get_health_monitor_service
    days = request.args.get('days', 7, type=int)
    service = get_health_monitor_service()
    result = service.get_uptime_stats(monitor_id, days=days)
    if 'error' in result:
        return error_response(404, result['error'])
    return success_response(data=result)