"""
审计日志服务

提供记录审计日志的便捷方法
"""

from flask import request
from ..extensions import db
from ..models.audit_log import AuditLog
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


def log_action(action, resource_type, resource_id=None, changes=None, old_values=None, new_values=None):
    """
    记录审计日志

    Args:
        action: 操作类型 (create/update/delete/login/logout)
        resource_type: 资源类型 (project/test_case/test_run/organization/user)
        resource_id: 资源 ID
        changes: 变更内容
        old_values: 旧值
        new_values: 新值
    """
    try:
        user_id = None
        try:
            user_id = get_current_user_id()
        except Exception:
            pass

        organization_id = None
        try:
            from flask import g
            organization_id = getattr(g, 'organization_id', None)
        except Exception:
            pass

        ip_address = None
        try:
            ip_address = request.remote_addr
        except Exception:
            pass

        user_agent = None
        try:
            user_agent = request.headers.get('User-Agent')
        except Exception:
            pass

        audit_log = AuditLog(
            user_id=user_id,
            organization_id=organization_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.session.add(audit_log)
        db.session.commit()

        logger.info(
            'Audit log recorded',
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
        )
    except Exception as exc:
        logger.error('Failed to record audit log', error=str(exc))
