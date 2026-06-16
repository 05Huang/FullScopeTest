"""
RBAC 权限体系测试

覆盖：系统角色权限矩阵、自定义角色 CRUD、权限检查服务、
     OrganizationMember 权限方法、API 角色管理端点
"""
import uuid

import pytest


# ── 辅助函数 ─────────────────────────────────────────────────────────────────

def _create_user(db, username=None, email=None, role='member'):
    """创建测试用户（仅数据库层面）"""
    from app.models.user import User
    uid = uuid.uuid4().hex[:6]
    user = User(
        username=username or f"user_{uid}",
        email=email or f"{uid}@test.com",
        password_hash="hashed",
        role=role,
    )
    db.session.add(user)
    db.session.flush()
    return user


def _create_org(db, owner_id, name=None):
    """创建测试组织"""
    from app.models.organization import Organization
    uid = uuid.uuid4().hex[:6]
    org = Organization(
        name=name or f"TestOrg_{uid}",
        slug=f"testorg-{uid}",
        owner_id=owner_id,
    )
    db.session.add(org)
    db.session.flush()
    return org


def _create_membership(db, org_id, user_id, role='tester'):
    """创建组织成员关系"""
    from app.models.organization import OrganizationMember
    member = OrganizationMember(
        organization_id=org_id,
        user_id=user_id,
        role=role,
    )
    db.session.add(member)
    db.session.flush()
    return member


def _register_and_login(client, username=None, password="Passw0rd!"):
    """通过 API 注册并登录用户，返回 (headers, user_id)"""
    uid = uuid.uuid4().hex[:8]
    username = username or f"rbac_{uid}"
    email = f"{username}@example.com"

    # 注册
    client.post("/api/v1/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
    })

    # 登录获取 token
    resp = client.post("/api/v1/auth/login", json={
        "username": username,
        "password": password,
    })
    data = resp.get_json()["data"]
    token = data["access_token"]
    user_id = data.get("user", {}).get("id")
    headers = {"Authorization": f"Bearer {token}"}
    return headers, user_id, username


def _setup_org_with_api_user(client, db_app, member_role='admin'):
    """
    创建一个通过 API 注册的用户，加入组织，并设置指定角色

    Returns:
        (headers, user_id, org_id)
    """
    from app.extensions import db

    headers, user_id, _ = _register_and_login(client)

    # 在 app context 中创建组织和成员关系
    with db_app.app_context():
        org = _create_org(db, user_id)
        _create_membership(db, org.id, user_id, member_role)
        db.session.commit()
        org_id = org.id

    return headers, user_id, org_id


# ══════════════════════════════════════════════════════════════════════════════
# 一、系统角色权限矩阵测试
# ══════════════════════════════════════════════════════════════════════════════

class TestSystemRolePermissions:
    """系统角色权限映射测试"""

    def test_admin_has_all_permissions(self):
        from app.models.role import SYSTEM_ROLE_PERMISSIONS
        admin_perms = SYSTEM_ROLE_PERMISSIONS['admin']
        resources = ['project', 'test_case', 'test_run', 'environment', 'report', 'ai_feature']
        for resource in resources:
            assert resource in admin_perms
            for action in ['create', 'read', 'update', 'delete', 'execute', 'manage']:
                assert action in admin_perms[resource], f"admin 缺少 {resource}:{action}"

    def test_viewer_read_only(self):
        from app.models.role import SYSTEM_ROLE_PERMISSIONS
        viewer_perms = SYSTEM_ROLE_PERMISSIONS['viewer']
        resources = ['project', 'test_case', 'test_run', 'environment', 'report', 'ai_feature']
        for resource in resources:
            assert viewer_perms[resource] == ['read'], f"viewer 在 {resource} 上应仅 read"

    def test_tester_can_manage_tests_but_not_projects(self):
        from app.models.role import SYSTEM_ROLE_PERMISSIONS
        tester_perms = SYSTEM_ROLE_PERMISSIONS['tester']
        # 测试相关资源应有完整权限
        assert 'create' in tester_perms['test_case']
        assert 'delete' in tester_perms['test_case']
        assert 'manage' in tester_perms['test_case']
        assert 'create' in tester_perms['test_run']
        assert 'execute' in tester_perms['test_run']
        # 项目/环境/报告应只读
        assert tester_perms['project'] == ['read']
        assert tester_perms['environment'] == ['read']
        assert tester_perms['report'] == ['read']

    def test_manager_has_more_than_tester_but_less_than_admin(self):
        from app.models.role import SYSTEM_ROLE_PERMISSIONS
        manager_perms = SYSTEM_ROLE_PERMISSIONS['manager']
        admin_perms = SYSTEM_ROLE_PERMISSIONS['admin']
        tester_perms = SYSTEM_ROLE_PERMISSIONS['tester']

        # manager 比 tester 多：project 和 environment 有写权限
        assert 'create' in manager_perms['project']
        assert 'create' in manager_perms['environment']
        # manager 比 admin 少：project 没有 manage
        assert 'manage' not in manager_perms['project']
        assert 'manage' in admin_perms['project']

    def test_legacy_role_mapping(self):
        from app.models.role import LEGACY_ROLE_MAPPING
        assert LEGACY_ROLE_MAPPING['owner'] == 'admin'
        assert LEGACY_ROLE_MAPPING['member'] == 'tester'
        assert LEGACY_ROLE_MAPPING['admin'] == 'admin'
        assert LEGACY_ROLE_MAPPING['viewer'] == 'viewer'

    def test_valid_roles_list(self):
        from app.models.role import VALID_ROLES
        assert set(VALID_ROLES) == {'admin', 'manager', 'tester', 'viewer'}


# ══════════════════════════════════════════════════════════════════════════════
# 二、Role Model 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestRoleModel:
    """Role 模型单元测试"""

    def test_role_has_permission_positive(self):
        from app.models.role import Role
        role = Role(
            name='tester',
            display_name='测试员',
            permissions={'test_case': ['create', 'read', 'update']},
        )
        assert role.has_permission('test_case', 'create') is True
        assert role.has_permission('test_case', 'read') is True

    def test_role_has_permission_negative(self):
        from app.models.role import Role
        role = Role(
            name='tester',
            display_name='测试员',
            permissions={'test_case': ['create', 'read']},
        )
        assert role.has_permission('test_case', 'delete') is False
        assert role.has_permission('project', 'create') is False

    def test_inactive_role_has_no_permissions(self):
        from app.models.role import Role
        role = Role(
            name='tester',
            display_name='测试员',
            permissions={'test_case': ['create', 'read']},
            is_active=False,
        )
        assert role.has_permission('test_case', 'create') is False

    def test_role_to_dict(self):
        from app.models.role import Role
        role = Role(
            name='tester',
            display_name='测试员',
            description='测试角色',
            permissions={'test_case': ['read']},
        )
        d = role.to_dict()
        assert d['name'] == 'tester'
        assert d['display_name'] == '测试员'
        assert d['permissions'] == {'test_case': ['read']}


class TestGetEffectivePermissions:
    """get_effective_permissions 函数测试"""

    def test_system_role_permissions(self):
        from app.models.role import get_effective_permissions
        admin_perms = get_effective_permissions('admin')
        assert 'create' in admin_perms.get('project', [])

    def test_legacy_owner_maps_to_admin(self):
        from app.models.role import get_effective_permissions
        owner_perms = get_effective_permissions('owner')
        admin_perms = get_effective_permissions('admin')
        assert owner_perms == admin_perms

    def test_legacy_member_maps_to_tester(self):
        from app.models.role import get_effective_permissions
        member_perms = get_effective_permissions('member')
        tester_perms = get_effective_permissions('tester')
        assert member_perms == tester_perms

    def test_unknown_role_returns_empty(self):
        from app.models.role import get_effective_permissions
        perms = get_effective_permissions('nonexistent_role')
        assert perms == {}


# ══════════════════════════════════════════════════════════════════════════════
# 三、OrganizationMember 权限方法测试
# ══════════════════════════════════════════════════════════════════════════════

class TestOrganizationMemberRBAC:
    """OrganizationMember 权限相关方法测试"""

    def test_get_effective_role_name_owner(self, app):
        from app.extensions import db
        from app.models.organization import OrganizationMember
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            membership = _create_membership(db, org.id, user.id, 'owner')
            assert membership.get_effective_role_name() == 'admin'
            db.session.rollback()

    def test_get_effective_role_name_member(self, app):
        from app.extensions import db
        from app.models.organization import OrganizationMember
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            membership = _create_membership(db, org.id, user.id, 'member')
            assert membership.get_effective_role_name() == 'tester'
            db.session.rollback()

    def test_has_permission_tester_can_create_test_case(self, app):
        from app.extensions import db
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            membership = _create_membership(db, org.id, user.id, 'tester')
            assert membership.has_permission('test_case', 'create') is True
            db.session.rollback()

    def test_has_permission_tester_cannot_create_project(self, app):
        from app.extensions import db
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            membership = _create_membership(db, org.id, user.id, 'tester')
            assert membership.has_permission('project', 'create') is False
            db.session.rollback()

    def test_has_permission_viewer_cannot_delete(self, app):
        from app.extensions import db
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            membership = _create_membership(db, org.id, user.id, 'viewer')
            assert membership.has_permission('test_case', 'delete') is False
            assert membership.has_permission('project', 'delete') is False
            db.session.rollback()

    def test_get_permissions_returns_full_dict(self, app):
        from app.extensions import db
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            membership = _create_membership(db, org.id, user.id, 'admin')
            perms = membership.get_permissions()
            assert 'project' in perms
            assert 'create' in perms['project']
            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 四、PermissionService 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPermissionService:
    """权限检查服务测试"""

    def test_check_permission_member_in_org(self, app):
        from app.extensions import db
        from app.services.permission_service import check_permission
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            _create_membership(db, org.id, user.id, 'tester')
            assert check_permission(user.id, org.id, 'test_case', 'create') is True
            assert check_permission(user.id, org.id, 'project', 'create') is False
            db.session.rollback()

    def test_check_permission_non_member(self, app):
        from app.extensions import db
        from app.services.permission_service import check_permission
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            # 不创建 membership
            assert check_permission(user.id, org.id, 'test_case', 'create') is False
            db.session.rollback()

    def test_get_user_permissions(self, app):
        from app.extensions import db
        from app.services.permission_service import get_user_permissions
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            _create_membership(db, org.id, user.id, 'admin')
            perms = get_user_permissions(user.id, org.id)
            assert len(perms) > 0
            db.session.rollback()

    def test_get_user_role_name(self, app):
        from app.extensions import db
        from app.services.permission_service import get_user_role_name
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            _create_membership(db, org.id, user.id, 'admin')
            assert get_user_role_name(user.id, org.id) == 'admin'
            db.session.rollback()

    def test_get_user_role_name_non_member(self, app):
        from app.extensions import db
        from app.services.permission_service import get_user_role_name
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            assert get_user_role_name(user.id, org.id) is None
            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 五、自定义角色 CRUD 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCustomRoleCRUD:
    """自定义角色创建、更新、删除测试"""

    def test_create_custom_role(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role
        from app.models.role import Role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            role = create_custom_role(
                organization_id=org.id,
                name='lead_tester',
                display_name='测试主管',
                permissions={
                    'project': ['read'],
                    'test_case': ['create', 'read', 'update', 'delete'],
                },
                description='可管理测试用例',
            )
            assert role.name == 'lead_tester'
            assert role.is_system is False
            assert role.organization_id == org.id
            assert 'delete' in role.permissions['test_case']
            # 清理
            db.session.delete(role)
            db.session.rollback()

    def test_create_custom_role_name_conflict_with_system(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            with pytest.raises(ValueError, match="系统保留"):
                create_custom_role(
                    organization_id=org.id,
                    name='admin',
                    display_name='自定义管理员',
                    permissions={'project': ['read']},
                )
            db.session.rollback()

    def test_create_custom_role_duplicate_name(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            create_custom_role(
                organization_id=org.id,
                name='custom_role',
                display_name='自定义',
                permissions={'project': ['read']},
            )
            with pytest.raises(ValueError, match="已存在"):
                create_custom_role(
                    organization_id=org.id,
                    name='custom_role',
                    display_name='自定义2',
                    permissions={'project': ['read']},
                )
            db.session.rollback()

    def test_create_custom_role_invalid_resource(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            with pytest.raises(ValueError, match="未知资源类型"):
                create_custom_role(
                    organization_id=org.id,
                    name='bad_role',
                    display_name='Bad',
                    permissions={'nonexistent': ['read']},
                )
            db.session.rollback()

    def test_create_custom_role_invalid_action(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            with pytest.raises(ValueError, match="未知操作"):
                create_custom_role(
                    organization_id=org.id,
                    name='bad_role',
                    display_name='Bad',
                    permissions={'project': ['fly']},
                )
            db.session.rollback()

    def test_update_custom_role(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role, update_custom_role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            role = create_custom_role(
                organization_id=org.id,
                name='updatable',
                display_name='可更新',
                permissions={'project': ['read']},
            )
            updated = update_custom_role(
                role_id=role.id,
                organization_id=org.id,
                display_name='已更新',
                permissions={'project': ['read', 'create']},
            )
            assert updated.display_name == '已更新'
            assert 'create' in updated.permissions['project']
            db.session.rollback()

    def test_update_system_role_fails(self, app):
        from app.extensions import db
        from app.models.role import Role
        from app.services.permission_service import update_custom_role
        with app.app_context():
            sys_role = Role(
                name='test_sys', display_name='系统',
                is_system=True, permissions={'project': ['read']},
            )
            db.session.add(sys_role)
            db.session.flush()
            with pytest.raises(ValueError, match="系统角色不可修改"):
                update_custom_role(sys_role.id, organization_id=None, display_name='新名称')
            db.session.rollback()

    def test_delete_custom_role_soft_delete(self, app):
        from app.extensions import db
        from app.services.permission_service import create_custom_role, delete_custom_role
        from app.models.role import Role
        with app.app_context():
            user = _create_user(db)
            org = _create_org(db, user.id)
            role = create_custom_role(
                organization_id=org.id,
                name='deletable',
                display_name='可删除',
                permissions={'project': ['read']},
            )
            delete_custom_role(role.id, org.id)
            # 软删除：记录仍存在但 is_active=False
            refreshed = Role.query.get(role.id)
            assert refreshed.is_active is False
            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 六、系统角色 Seed 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestSeedSystemRoles:
    """系统角色种子数据测试"""

    def test_seed_system_roles_creates_four_roles(self, app):
        from app.extensions import db
        from app.models.role import Role
        from app.services.permission_service import seed_system_roles
        with app.app_context():
            seed_system_roles()
            roles = Role.query.filter_by(is_system=True).all()
            role_names = {r.name for r in roles}
            assert role_names == {'admin', 'manager', 'tester', 'viewer'}
            # 清理
            Role.query.filter_by(is_system=True).delete()
            db.session.commit()

    def test_seed_system_roles_idempotent(self, app):
        from app.extensions import db
        from app.models.role import Role
        from app.services.permission_service import seed_system_roles
        with app.app_context():
            seed_system_roles()
            count_first = Role.query.filter_by(is_system=True).count()
            seed_system_roles()
            count_second = Role.query.filter_by(is_system=True).count()
            assert count_first == count_second == 4
            # 清理
            Role.query.filter_by(is_system=True).delete()
            db.session.commit()


# ══════════════════════════════════════════════════════════════════════════════
# 七、API 角色管理端点测试
# ══════════════════════════════════════════════════════════════════════════════

class TestRoleManagementAPI:
    """角色管理 API 端点测试"""

    def test_list_system_roles(self, app, client, no_rate_limit):
        """GET /roles/system — 无需组织上下文"""
        from app.services.permission_service import seed_system_roles
        from app.extensions import db
        with app.app_context():
            seed_system_roles()
            db.session.commit()

        headers, user_id, _ = _register_and_login(client)

        resp = client.get('/api/v1/roles/system', headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()
        role_names = {r['name'] for r in data['data']}
        assert 'admin' in role_names
        assert 'viewer' in role_names

        # 清理
        from app.models.role import Role
        with app.app_context():
            Role.query.filter_by(is_system=True).delete()
            db.session.commit()

    def test_list_org_roles_includes_system_roles(self, app, client, no_rate_limit):
        """GET /organizations/:id/roles — 包含系统角色"""
        from app.services.permission_service import seed_system_roles
        from app.extensions import db
        with app.app_context():
            seed_system_roles()
            db.session.commit()

        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        resp = client.get(f'/api/v1/organizations/{org_id}/roles', headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()
        role_names = {r['name'] for r in data['data']}
        assert 'admin' in role_names
        assert 'viewer' in role_names

        # 清理
        from app.models.role import Role
        with app.app_context():
            Role.query.filter_by(is_system=True).delete()
            db.session.commit()

    def test_create_custom_role_as_admin(self, app, client, no_rate_limit):
        """POST /organizations/:id/roles — admin 可创建自定义角色"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        resp = client.post(f'/api/v1/organizations/{org_id}/roles', json={
            'name': 'lead',
            'display_name': '测试主管',
            'permissions': {'test_case': ['create', 'read', 'update']},
            'description': '可管理测试用例',
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['data']['name'] == 'lead'

        # 清理
        from app.extensions import db
        from app.models.role import Role
        with app.app_context():
            Role.query.filter_by(name='lead').delete()
            db.session.commit()

    def test_create_custom_role_as_viewer_forbidden(self, app, client, no_rate_limit):
        """viewer 无权创建自定义角色"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'viewer')

        resp = client.post(f'/api/v1/organizations/{org_id}/roles', json={
            'name': 'lead',
            'display_name': '测试主管',
            'permissions': {'test_case': ['read']},
        }, headers=headers)
        assert resp.status_code == 403

    def test_create_custom_role_with_system_name_forbidden(self, app, client, no_rate_limit):
        """不可用系统保留名创建角色"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        resp = client.post(f'/api/v1/organizations/{org_id}/roles', json={
            'name': 'admin',
            'display_name': '自定义管理员',
            'permissions': {'project': ['read']},
        }, headers=headers)
        assert resp.status_code == 400

    def test_update_custom_role(self, app, client, no_rate_limit):
        """PUT /organizations/:id/roles/:role_id — 更新自定义角色"""
        from app.extensions import db
        from app.models.role import Role

        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        # 先在 DB 中创建角色
        with app.app_context():
            role = Role(
                name='custom_edit', display_name='可编辑',
                organization_id=org_id, permissions={'project': ['read']},
            )
            db.session.add(role)
            db.session.commit()
            role_id = role.id

        resp = client.put(f'/api/v1/organizations/{org_id}/roles/{role_id}', json={
            'display_name': '已编辑',
            'permissions': {'project': ['read', 'create']},
        }, headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['display_name'] == '已编辑'

        # 清理
        with app.app_context():
            Role.query.filter_by(id=role_id).delete()
            db.session.commit()

    def test_delete_custom_role(self, app, client, no_rate_limit):
        """DELETE /organizations/:id/roles/:role_id — 软删除自定义角色"""
        from app.extensions import db
        from app.models.role import Role

        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        with app.app_context():
            role = Role(
                name='custom_del', display_name='可删除',
                organization_id=org_id, permissions={'project': ['read']},
            )
            db.session.add(role)
            db.session.commit()
            role_id = role.id

        resp = client.delete(f'/api/v1/organizations/{org_id}/roles/{role_id}', headers=headers)
        assert resp.status_code == 200

        # 验证软删除
        with app.app_context():
            refreshed = db.session.get(Role, role_id)
            assert refreshed.is_active is False
            db.session.rollback()

    def test_get_my_permissions(self, app, client, no_rate_limit):
        """GET /organizations/:id/my-permissions — 获取当前用户权限"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'tester')

        resp = client.get(f'/api/v1/organizations/{org_id}/my-permissions', headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['role'] == 'tester'
        assert 'test_case' in data['data']['permissions']

    def test_get_my_permissions_non_member(self, app, client, no_rate_limit):
        """非组织成员查询权限应返回 403"""
        from app.extensions import db

        # 创建一个组织
        headers_admin, admin_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        # 创建一个不属于该组织的用户
        headers_outsider, outsider_id, _ = _register_and_login(client)

        resp = client.get(f'/api/v1/organizations/{org_id}/my-permissions', headers=headers_outsider)
        assert resp.status_code == 403

    def test_update_member_role(self, app, client, no_rate_limit):
        """PATCH /organizations/:id/members/:uid/role — 修改成员角色"""
        from app.extensions import db

        # 创建 admin 用户和组织
        headers_admin, admin_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        # 创建另一个用户并加入组织（作为 tester）
        headers_member, member_id, _ = _register_and_login(client)
        with app.app_context():
            _create_membership(db, org_id, member_id, 'tester')
            db.session.commit()

        resp = client.patch(
            f'/api/v1/organizations/{org_id}/members/{member_id}/role',
            json={'role': 'manager'},
            headers=headers_admin,
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['role'] == 'manager'

    def test_update_member_role_invalid_role(self, app, client, no_rate_limit):
        """使用无效角色名应返回 400"""
        from app.extensions import db

        headers_admin, admin_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        headers_member, member_id, _ = _register_and_login(client)
        with app.app_context():
            _create_membership(db, org_id, member_id, 'tester')
            db.session.commit()

        resp = client.patch(
            f'/api/v1/organizations/{org_id}/members/{member_id}/role',
            json={'role': 'superadmin'},
            headers=headers_admin,
        )
        assert resp.status_code == 400


# ══════════════════════════════════════════════════════════════════════════════
# 八、@require_permission 装饰器集成测试
# ══════════════════════════════════════════════════════════════════════════════

class TestRequirePermissionDecorator:
    """
    @require_permission 装饰器集成测试

    通过 /my-permissions 端点间接验证权限系统是否正确工作。
    """

    def test_admin_has_project_create_permission(self, app, client, no_rate_limit):
        """admin 角色拥有 project:create 权限"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'admin')

        resp = client.get(f'/api/v1/organizations/{org_id}/my-permissions', headers=headers)
        assert resp.status_code == 200
        perms = resp.get_json()['data']['permissions']
        assert 'create' in perms.get('project', [])

    def test_viewer_lacks_project_create_permission(self, app, client, no_rate_limit):
        """viewer 角色没有 project:create 权限"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'viewer')

        resp = client.get(f'/api/v1/organizations/{org_id}/my-permissions', headers=headers)
        assert resp.status_code == 200
        perms = resp.get_json()['data']['permissions']
        assert 'create' not in perms.get('project', [])

    def test_tester_can_read_test_cases(self, app, client, no_rate_limit):
        """tester 角色拥有 test_case:read 权限"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'tester')

        resp = client.get(f'/api/v1/organizations/{org_id}/my-permissions', headers=headers)
        assert resp.status_code == 200
        perms = resp.get_json()['data']['permissions']
        assert 'read' in perms.get('test_case', [])

    def test_manager_has_project_create_but_not_manage(self, app, client, no_rate_limit):
        """manager 角色有 project:create 但没有 project:manage"""
        headers, user_id, org_id = _setup_org_with_api_user(client, app, 'manager')

        resp = client.get(f'/api/v1/organizations/{org_id}/my-permissions', headers=headers)
        assert resp.status_code == 200
        perms = resp.get_json()['data']['permissions']
        assert 'create' in perms.get('project', [])
        assert 'manage' not in perms.get('project', [])