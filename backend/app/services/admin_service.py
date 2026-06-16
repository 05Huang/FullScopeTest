"""
管理员后台服务

提供平台运营视角，监控整体使用情况。
仅 super_admin 角色可访问。
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..extensions import db
from ..models.user import User
from ..models.organization import Organization, OrganizationMember
from ..models.project import Project
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)


class AdminService:
    """管理员后台服务"""

    def get_platform_overview(self) -> Dict[str, Any]:
        """获取平台概览"""
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_orgs = Organization.query.count()
        total_projects = Project.query.count()

        # 最近 24 小时的执行量
        since = datetime.utcnow() - timedelta(hours=24)
        daily_runs = TestRun.query.filter(TestRun.created_at >= since).count()

        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_organizations": total_orgs,
            "total_projects": total_projects,
            "daily_test_runs": daily_runs,
        }

    def get_tenant_list(self) -> list:
        """获取租户列表"""
        orgs = Organization.query.all()
        result = []
        for org in orgs:
            member_count = OrganizationMember.query.filter_by(
                organization_id=org.id, is_active=True,
            ).count()
            project_count = Project.query.filter_by(organization_id=org.id).count()
            result.append({
                "id": org.id, "name": org.name,
                "member_count": member_count,
                "project_count": project_count,
                "created_at": org.created_at.isoformat() if org.created_at else None,
            })
        return result

    def get_system_health(self) -> Dict[str, Any]:
        """获取系统健康状态"""
        from ..core.health import _check_database, _check_redis
        return {
            "database": _check_database(),
            "redis": _check_redis(),
        }


_instance = None


def get_admin_service():
    global _instance
    if _instance is None: _instance = AdminService()
    return _instance
