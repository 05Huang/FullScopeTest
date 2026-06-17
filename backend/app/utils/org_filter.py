"""
组织级数据过滤工具

提供按组织 ID 过滤查询的辅助函数
"""
from typing import Optional, List
from ..middleware.tenant import get_current_organization_id, get_current_user_organization_ids


def get_org_filter():
    """获取当前组织过滤条件，返回 organization_id 或 None"""
    return get_current_organization_id()


def filter_by_org(query, model):
    """给 SQLAlchemy 查询添加组织过滤条件"""
    org_id = get_current_organization_id()
    if org_id and hasattr(model, 'organization_id'):
        query = query.filter(model.organization_id == org_id)
    return query


def filter_by_owner_or_org(query, model, user_id):
    """
    按 owner_id 或 organization_id 过滤
    优先使用 organization_id，回退到 owner_id
    """
    org_id = get_current_organization_id()
    if org_id and hasattr(model, 'organization_id'):
        return query.filter(model.organization_id == org_id)
    return query.filter(model.owner_id == user_id)


def get_org_id_for_create() -> Optional[int]:
    """创建资源时获取组织 ID"""
    return get_current_organization_id()


def get_org_project_ids() -> List[int]:
    """获取当前组织下所有项目 ID 列表"""
    from ..models.project import Project
    org_id = get_current_organization_id()
    if org_id:
        return [p.id for p in Project.query.filter_by(organization_id=org_id).all()]
    return []


def filter_by_org_projects(query, model, project_id_field='project_id'):
    """
    按组织下的项目过滤
    用于测试用例、测试运行等关联到项目的资源
    """
    org_id = get_current_organization_id()
    if org_id:
        project_ids = get_org_project_ids()
        if project_ids:
            return query.filter(getattr(model, project_id_field).in_(project_ids))
        else:
            return query.filter(model.id == -1)
    return query
