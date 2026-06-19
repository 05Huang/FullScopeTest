"""
组织级数据隔离中间件

所有查询自动注入 organization_id 过滤条件，防止越权访问
"""

from functools import wraps
from typing import Optional
from flask import g, request
from ..extensions import db
from ..models.organization import Organization, OrganizationMember
from ..core.logging import get_logger

logger = get_logger(__name__)


def get_current_organization_id() -> Optional[int]:
    """获取当前请求上下文中的组织 ID"""
    return getattr(g, 'organization_id', None)


def set_current_organization_id(org_id: Optional[int]):
    """设置当前请求上下文中的组织 ID"""
    g.organization_id = org_id


def get_current_user_organization_ids() -> list:
    """获取当前用户所属的所有组织 ID"""
    return getattr(g, 'user_organization_ids', [])


def require_organization(f):
    """装饰器：要求请求必须关联到一个组织"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        org_id = get_current_organization_id()
        if not org_id:
            return {'error': 'Organization context required'}, 403
        return f(*args, **kwargs)
    return decorated_function


def check_organization_access(user_id: int, organization_id: int) -> bool:
    """检查用户是否有权访问指定组织"""
    membership = OrganizationMember.query.filter_by(
        user_id=user_id,
        organization_id=organization_id,
        is_active=True,
    ).first()
    return membership is not None


def get_user_organizations(user_id: int) -> list:
    """获取用户所属的所有组织 ID 列表"""
    memberships = OrganizationMember.query.filter_by(
        user_id=user_id,
        is_active=True,
    ).all()
    return [m.organization_id for m in memberships]


def ensure_user_has_organization(user_id: int):
    """确保用户至少有一个组织，没有则自动创建个人空间"""
    memberships = OrganizationMember.query.filter_by(
        user_id=user_id, is_active=True
    ).count()

    if memberships > 0:
        return

    from ..models.user import User
    user = User.query.get(user_id)
    if not user:
        return

    # 创建个人空间组织
    slug = f"personal-{user.username}-{user.id}"
    org = Organization(
        name=f"{user.username} 的个人空间",
        slug=slug,
        description="系统自动创建的个人空间",
        owner_id=user.id,
        is_active=True,
    )
    db.session.add(org)
    db.session.flush()

    # 添加为所有者
    member = OrganizationMember(
        organization_id=org.id,
        user_id=user.id,
        role='owner',
        invited_by=user.id,
        is_active=True,
    )
    db.session.add(member)
    db.session.commit()

    logger.info(f'Auto-created personal org for user {user.username}', org_id=org.id)


def setup_tenant_hooks(app):
    """在应用初始化时设置租户钩子"""
    @app.before_request
    def set_tenant_context():
        """在每个请求开始时设置租户上下文"""
        from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                org_ids = get_user_organizations(user_id)
                g.user_organization_ids = org_ids
                if len(org_ids) == 1:
                    g.organization_id = org_ids[0]
                elif len(org_ids) > 1:
                    g.organization_id = request.headers.get('X-Organization-ID') or request.args.get('organization_id')
                    if g.organization_id:
                        g.organization_id = int(g.organization_id)
                        # 校验用户是否属于该组织，防止越权访问
                        if g.organization_id not in org_ids:
                            logger.warning("用户尝试访问非所属组织", user_id=user_id, org_id=g.organization_id)
                            g.organization_id = None
                else:
                    g.organization_id = None
        except Exception:
            g.user_organization_ids = []
            g.organization_id = None

    logger.info('Tenant middleware initialized')
