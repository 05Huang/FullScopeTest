"""
RBAC 权限校验中间件

提供装饰器用于在 API 端点上声明所需的资源权限。

用法：
    @require_permission('project', 'create')
    def create_project():
        ...

    @require_permission('test_case', 'delete')
    def delete_test_case(case_id):
        ...

装饰器自动：
1. 验证 JWT
2. 从请求上下文获取当前组织 ID（由 tenant 中间件注入）
3. 检查用户在该组织中的角色是否拥有指定权限
4. 权限不足时返回 403 错误
"""
from functools import wraps
from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..utils.response import error_response
from ..services.permission_service import check_permission, get_user_role_name, get_user_permissions
from ..core.logging import get_logger

logger = get_logger(__name__)


def require_permission(resource: str, action: str):
    """
    权限校验装饰器

    检查当前用户在当前组织上下文中是否拥有指定的资源操作权限。

    Args:
        resource: 权限资源名（project/test_case/test_run/environment/report/ai_feature）
        action: 权限操作名（create/read/update/delete/execute/manage）

    Usage:
        @api_bp.route('/projects', methods=['POST'])
        @jwt_required()
        @require_permission('project', 'create')
        def create_project():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 验证 JWT
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            if not user_id:
                return error_response(401, '未认证')

            user_id = int(user_id)

            # 获取当前组织上下文（由 tenant 中间件注入）
            org_id = getattr(g, 'organization_id', None)
            if not org_id:
                return error_response(403, '需要组织上下文')

            # 检查权限
            has_perm = check_permission(user_id, org_id, resource, action)
            if not has_perm:
                role_name = get_user_role_name(user_id, org_id)
                logger.warning("权限不足",
                               user_id=user_id,
                               organization_id=org_id,
                               role=role_name,
                               required_resource=resource,
                               required_action=action)
                return error_response(
                    403,
                    f'权限不足：需要 {resource}:{action} 权限',
                    errors={
                        'required': f'{resource}:{action}',
                        'role': role_name,
                    },
                )

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def inject_user_permissions(app):
    """
    在请求上下文中注入当前用户的权限信息

    应在 tenant 中间件之后调用。
    可在 API 中通过 g.user_permissions 和 g.user_role 访问。

    Args:
        app: Flask 应用实例
    """
    @app.before_request
    def _inject_permissions():
        """在每个请求中注入用户权限（仅已认证请求）"""
        from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            org_id = getattr(g, 'organization_id', None)

            if user_id and org_id:
                user_id = int(user_id)
                g.user_role = get_user_role_name(user_id, org_id)
                g.user_permissions = get_user_permissions(user_id, org_id)
            else:
                g.user_role = None
                g.user_permissions = {}
        except Exception:
            g.user_role = None
            g.user_permissions = {}
