"""
多租户数据隔离服务

提供租户级数据隔离、跨租户访问检测和租户统计。
"""

from typing import Dict, Any, Optional, List
from ..extensions import db
from ..models.organization import Organization, OrganizationMember
from ..models.project import Project
from ..models.api_test_case import ApiTestCase
from ..core.logging import get_logger

logger = get_logger(__name__)


class TenantIsolationService:
    """多租户数据隔离服务"""

    def check_access(self, user_id: int, resource_org_id: Optional[int], action: str = "read") -> bool:
        """
        检查用户是否有权访问指定组织的资源

        Args:
            user_id: 用户 ID
            resource_org_id: 资源所属组织 ID
            action: 操作类型

        Returns:
            bool: 是否允许访问
        """
        if resource_org_id is None:
            return True  # 无组织限制的资源

        # 检查用户是否是该组织成员
        membership = OrganizationMember.query.filter_by(
            user_id=user_id,
            organization_id=resource_org_id,
            is_active=True,
        ).first()

        if not membership:
            logger.warning("跨租户访问尝试", user_id=user_id, target_org=resource_org_id, action=action)
            return False

        return True

    def get_user_organizations(self, user_id: int) -> List[Dict[str, Any]]:
        """获取用户所属的所有组织"""
        memberships = OrganizationMember.query.filter_by(
            user_id=user_id, is_active=True,
        ).all()

        orgs = []
        for m in memberships:
            org = Organization.query.get(m.organization_id)
            if org:
                orgs.append({"id": org.id, "name": org.name, "role": m.role})
        return orgs

    def get_tenant_stats(self, org_id: int) -> Dict[str, Any]:
        """获取租户数据统计"""
        org = Organization.query.get(org_id)
        if not org:
            return {"error": "Organization not found"}

        # 成员数
        member_count = OrganizationMember.query.filter_by(
            organization_id=org_id, is_active=True,
        ).count()

        # 项目数
        project_count = Project.query.filter_by(organization_id=org_id).count()

        return {
            "organization_id": org_id,
            "name": org.name,
            "member_count": member_count,
            "project_count": project_count,
        }

    def cleanup_tenant_data(self, org_id: int) -> Dict[str, Any]:
        """清理租户所有关联数据（删除组织时调用）"""
        # 删除组织的所有项目关联数据
        projects = Project.query.filter_by(organization_id=org_id).all()
        project_ids = [p.id for p in projects]

        deleted_cases = 0
        if project_ids:
            deleted_cases = ApiTestCase.query.filter(
                ApiTestCase.project_id.in_(project_ids)
            ).delete(synchronize_session=False)

        # 删除项目
        deleted_projects = Project.query.filter_by(organization_id=org_id).delete()

        # 删除成员关系
        deleted_members = OrganizationMember.query.filter_by(organization_id=org_id).delete()

        db.session.commit()

        logger.info("租户数据清理完成", org_id=org_id, projects=deleted_projects, cases=deleted_cases)
        return {
            "deleted_projects": deleted_projects,
            "deleted_cases": deleted_cases,
            "deleted_members": deleted_members,
        }


_instance = None


def get_tenant_isolation_service():
    global _instance
    if _instance is None: _instance = TenantIsolationService()
    return _instance
