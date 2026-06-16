"""
API Token 细粒度权限测试

覆盖：Token 创建（新旧格式）、权限检查、项目范围校验、
     旧格式兼容、validate API 端点
"""
import uuid


def _auth_headers(client, username=None):
    """注册并登录，返回认证头"""
    uid = uuid.uuid4().hex[:8]
    username = username or f"tok_{uid}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={
        "username": username, "email": email, "password": password,
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": username, "password": password,
    })
    token = resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ══════════════════════════════════════════════════════════════════════════════
# 一、Token 创建（新格式）
# ══════════════════════════════════════════════════════════════════════════════

class TestCreateTokenNewFormat:
    """新格式 Token 创建测试"""

    def test_create_token_with_actions(self, client, no_rate_limit):
        """使用 actions 创建 Token"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "CI Token",
            "actions": ["read", "execute"],
            "project_ids": [1, 2],
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["name"] == "CI Token"
        assert set(data["actions"]) == {"read", "execute"}
        assert data["project_ids"] == [1, 2]
        assert "token" in data  # 创建时返回明文

    def test_create_token_default_actions(self, client, no_rate_limit):
        """不指定 actions 默认为 ['read']"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Default Token",
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["actions"] == ["read"]
        assert data["project_ids"] == []

    def test_create_token_unlimited_projects(self, client, no_rate_limit):
        """空 project_ids 表示不限制"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Global Token",
            "actions": ["read"],
            "project_ids": [],
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["project_ids"] == []

    def test_create_token_invalid_actions(self, client, no_rate_limit):
        """无效操作类型应返回 400"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Bad Token",
            "actions": ["read", "fly"],
        }, headers=headers)
        assert resp.status_code == 400

    def test_create_token_invalid_project_ids(self, client, no_rate_limit):
        """project_ids 非数组应返回 400"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Bad Token",
            "actions": ["read"],
            "project_ids": "not-a-list",
        }, headers=headers)
        assert resp.status_code == 400


# ══════════════════════════════════════════════════════════════════════════════
# 二、旧格式兼容
# ══════════════════════════════════════════════════════════════════════════════

class TestCreateTokenOldFormat:
    """旧格式权限兼容测试"""

    def test_create_token_read_only(self, client, no_rate_limit):
        """旧格式 read-only 兼容"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Old Read Token",
            "permissions": ["read-only"],
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert "read" in data["actions"]

    def test_create_token_read_write(self, client, no_rate_limit):
        """旧格式 read-write 兼容"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Old RW Token",
            "permissions": ["read-write"],
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert set(data["actions"]) == {"read", "write", "execute"}

    def test_create_token_invalid_old_format(self, client, no_rate_limit):
        """无效旧格式应返回 400"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/tokens", json={
            "name": "Bad Old Token",
            "permissions": ["super-admin"],
        }, headers=headers)
        assert resp.status_code == 400


# ══════════════════════════════════════════════════════════════════════════════
# 三、Token Model 方法测试
# ══════════════════════════════════════════════════════════════════════════════

class TestApiTokenModel:
    """ApiToken 模型方法测试"""

    def test_get_actions_new_format(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions={'actions': ['read', 'execute']})
        assert token.get_actions() == ['read', 'execute']

    def test_get_actions_old_read_only(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions=['read-only'])
        assert token.get_actions() == ['read']

    def test_get_actions_old_read_write(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions=['read-write'])
        actions = token.get_actions()
        assert 'read' in actions
        assert 'write' in actions
        assert 'execute' in actions

    def test_can_access_project_unscoped(self):
        from app.models.api_token import ApiToken
        token = ApiToken(project_ids=[])
        assert token.can_access_project(1) is True
        assert token.can_access_project(999) is True

    def test_can_access_project_scoped(self):
        from app.models.api_token import ApiToken
        token = ApiToken(project_ids=[1, 2, 5])
        assert token.can_access_project(1) is True
        assert token.can_access_project(5) is True
        assert token.can_access_project(3) is False

    def test_has_action_positive(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions={'actions': ['read', 'write']})
        assert token.has_action('read') is True
        assert token.has_action('write') is True

    def test_has_action_negative(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions={'actions': ['read']})
        assert token.has_action('write') is False
        assert token.has_action('delete') is False

    def test_is_read_only_true(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions=['read-only'])
        assert token.is_read_only() is True

    def test_is_read_only_false(self):
        from app.models.api_token import ApiToken
        token = ApiToken(permissions=['read-write'])
        assert token.is_read_only() is False

    def test_to_dict_includes_project_ids(self):
        from app.models.api_token import ApiToken
        token = ApiToken(
            name='test',
            permissions={'actions': ['read']},
            project_ids=[1, 2],
        )
        d = token.to_dict()
        assert d['project_ids'] == [1, 2]


# ══════════════════════════════════════════════════════════════════════════════
# 四、TokenService 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestTokenService:
    """Token 服务测试"""

    def test_create_token_returns_tuple(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.token_service import create_token
        with app.app_context():
            user = User(username=f"ts_{uuid.uuid4().hex[:6]}", email="ts@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            api_token, raw_token = create_token(
                user_id=user.id,
                name='Test Token',
                actions=['read', 'execute'],
                project_ids=[1, 2],
            )
            assert raw_token is not None
            assert len(raw_token) > 20
            assert api_token.get_actions() == ['read', 'execute']
            assert api_token.project_ids == [1, 2]
            db.session.rollback()

    def test_create_token_invalid_actions(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.token_service import create_token
        with app.app_context():
            user = User(username=f"ts_{uuid.uuid4().hex[:6]}", email="ts2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            import pytest
            with pytest.raises(ValueError, match="无效的操作类型"):
                create_token(user_id=user.id, name='Bad', actions=['fly'])
            db.session.rollback()

    def test_validate_token_success(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.token_service import create_token, validate_token
        with app.app_context():
            user = User(username=f"ts_{uuid.uuid4().hex[:6]}", email="ts3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            _, raw_token = create_token(user_id=user.id, name='Valid Token')
            result = validate_token(raw_token)
            assert result is not None
            assert result.name == 'Valid Token'
            db.session.rollback()

    def test_validate_token_invalid(self, app):
        from app.services.token_service import validate_token
        with app.app_context():
            result = validate_token('invalid-token-12345')
            assert result is None

    def test_check_token_permission_allowed(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.token_service import create_token, check_token_permission
        with app.app_context():
            user = User(username=f"ts_{uuid.uuid4().hex[:6]}", email="ts4@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            api_token, _ = create_token(
                user_id=user.id, name='Scoped',
                actions=['read', 'execute'], project_ids=[1, 2],
            )
            # 项目 1 有权限
            assert check_token_permission(api_token, 'read', 1) is True
            assert check_token_permission(api_token, 'execute', 2) is True
            # 项目 3 无权限
            assert check_token_permission(api_token, 'read', 3) is False
            # write 操作无权限
            assert check_token_permission(api_token, 'write', 1) is False
            db.session.rollback()

    def test_check_token_permission_unscoped(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.token_service import create_token, check_token_permission
        with app.app_context():
            user = User(username=f"ts_{uuid.uuid4().hex[:6]}", email="ts5@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            api_token, _ = create_token(
                user_id=user.id, name='Global',
                actions=['read'], project_ids=[],
            )
            # 无项目限制时，任何项目都可以访问
            assert check_token_permission(api_token, 'read', 1) is True
            assert check_token_permission(api_token, 'read', 999) is True
            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 五、Token 列表和删除 API 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestTokenListAndDelete:
    """Token 列表和删除 API 测试"""

    def test_list_tokens(self, client, no_rate_limit):
        """获取 Token 列表"""
        headers = _auth_headers(client)
        # 创建一个 Token
        client.post("/api/v1/tokens", json={
            "name": "List Test", "actions": ["read"],
        }, headers=headers)
        resp = client.get("/api/v1/tokens", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["pagination"]["total"] >= 1

    def test_delete_token(self, client, no_rate_limit):
        """删除 Token"""
        headers = _auth_headers(client)
        create_resp = client.post("/api/v1/tokens", json={
            "name": "To Delete", "actions": ["read"],
        }, headers=headers)
        token_id = create_resp.get_json()["data"]["id"]
        resp = client.delete(f"/api/v1/tokens/{token_id}", headers=headers)
        assert resp.status_code == 200

    def test_delete_nonexistent_token(self, client, no_rate_limit):
        """删除不存在的 Token 应返回 404"""
        headers = _auth_headers(client)
        resp = client.delete("/api/v1/tokens/99999", headers=headers)
        assert resp.status_code == 404