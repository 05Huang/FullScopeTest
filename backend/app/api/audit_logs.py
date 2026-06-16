"""
审计日志 API 接口模块

提供审计日志的查询、过滤和统计功能。
审计日志不可修改/删除，仅支持查询。
"""

from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy import func as sa_func

from . import api_bp
from ..extensions import db
from ..models.audit_log import AuditLog
from ..utils.response import success_response, error_response
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

    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()) \
        .offset((page - 1) * per_page) \
        .limit(per_page) \
        .all()

    return success_response(data={
        'items': [log.to_dict() for log in logs],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
    })


@api_bp.route('/audit-logs/<int:log_id>', methods=['GET'])
@jwt_required()
def get_audit_log(log_id):
    """获取单条审计日志详情"""
    log = AuditLog.query.get(log_id)
    if not log:
        return error_response(404, '审计日志不存在')
    return success_response(data=log.to_dict())


@api_bp.route('/audit-logs/stats', methods=['GET'])
@jwt_required()
def get_audit_stats():
    """
    获取审计日志统计

    查询参数:
        days: 统计天数（默认 30）
    """
    days = request.args.get('days', 30, type=int)
    since = datetime.utcnow() - timedelta(days=days)

    # 按操作类型统计
    action_stats = db.session.query(
        AuditLog.action,
        sa_func.count(AuditLog.id).label('count'),
    ).filter(AuditLog.created_at >= since) \
     .group_by(AuditLog.action).all()

    # 按资源类型统计
    resource_stats = db.session.query(
        AuditLog.resource_type,
        sa_func.count(AuditLog.id).label('count'),
    ).filter(AuditLog.created_at >= since) \
     .group_by(AuditLog.resource_type).all()

    # 最近活跃用户
    active_users = db.session.query(
        AuditLog.user_id,
        sa_func.count(AuditLog.id).label('count'),
    ).filter(AuditLog.created_at >= since, AuditLog.user_id.isnot(None)) \
     .group_by(AuditLog.user_id) \
     .order_by(sa_func.count(AuditLog.id).desc()) \
     .limit(10).all()

    return success_response(data={
        'period_days': days,
        'by_action': {row.action: row.count for row in action_stats},
        'by_resource': {row.resource_type: row.count for row in resource_stats},
        'active_users': [{'user_id': row.user_id, 'count': row.count} for row in active_users],
    })
