"""
审计日志 API 接口模块

提供审计日志的查询和过滤功能
"""

from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..extensions import db
from ..models.audit_log import AuditLog
from ..utils.response import success_response, error_response, paginate_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
def get_audit_logs():
    """
    获取审计日志列表

    查询参数:
        page: 页码 (默认 1)
        per_page: 每页数量 (默认 20)
        user_id: 按用户过滤
        action: 按操作类型过滤
        resource_type: 按资源类型过滤
        start_time: 开始时间 (ISO 格式)
        end_time: 结束时间 (ISO 格式)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action', '').strip()
    resource_type = request.args.get('resource_type', '').strip()
    start_time = request.args.get('start_time', '').strip()
    end_time = request.args.get('end_time', '').strip()

    query = AuditLog.query

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    if action:
        query = query.filter(AuditLog.action == action)

    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)

    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(AuditLog.created_at >= start_dt)
        except ValueError:
            return error_response(400, 'start_time 格式无效')

    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(AuditLog.created_at <= end_dt)
        except ValueError:
            return error_response(400, 'end_time 格式无效')

    pagination = query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return paginate_response(
        items=[log.to_dict() for log in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page
    )
