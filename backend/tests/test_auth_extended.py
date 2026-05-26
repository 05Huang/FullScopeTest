"""
认证模块扩展测试

覆盖：Token 刷新、密码修改、密码强度验证、限流、错误场景
"""

import uuid
import time


def _register_and_login(client, username=None, password="Str0ng!Pass"):
    """辅助函数：注册并登录，返回 token"""
    if username is None:
        username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    data = login_resp.get_json()["data"]
    return {
        "username": username,
        "email": email,
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
    }


class TestTokenRefresh:
    """Token 刷新测试"""

    def test_refresh_token_success(self, client):
        """使用 refresh token 获取新的 access token"""
        user = _register_and_login(client)

        resp = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {user['refresh_token']}"},
        )
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload["code"] == 200
        assert "access_token" in payload["data"]

    def test_refresh_with_access_token_fails(self, client):
        """使用 access token 刷新应该失败"""
        user = _register_and_login(client)

        resp = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 422

    def test_refresh_without_token_fails(self, client):
        """不带 token 刷新应该失败"""
        resp = client.post("/api/v1/auth/refresh")
        assert resp.status_code == 401


class TestPasswordChange:
    """密码修改测试"""

    def test_change_password_success(self, client):
        """成功修改密码"""
        user = _register_and_login(client)

        resp = client.put(
            "/api/v1/auth/password",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"old_password": "Str0ng!Pass", "new_password": "N3w!Passw0rd"},
        )
        assert resp.status_code == 200

        # 用新密码登录
        login_resp = client.post(
            "/api/v1/auth/login",
            json={"username": user["username"], "password": "N3w!Passw0rd"},
        )
        assert login_resp.status_code == 200

    def test_change_password_wrong_old_password(self, client):
        """旧密码错误应该失败"""
        user = _register_and_login(client)

        resp = client.put(
            "/api/v1/auth/password",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"old_password": "Wrong!Pass1", "new_password": "N3w!Passw0rd"},
        )
        assert resp.status_code == 400

    def test_change_password_weak_new_password(self, client):
        """新密码强度不足应该失败"""
        user = _register_and_login(client)

        resp = client.put(
            "/api/v1/auth/password",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"old_password": "Str0ng!Pass", "new_password": "weak"},
        )
        assert resp.status_code == 400


class TestPasswordStrength:
    """密码强度验证测试"""

    def test_register_weak_password_no_uppercase(self, client):
        """缺少大写字母应该失败"""
        resp = client.post(
            "/api/v1/auth/register",
            json={
                "username": f"test_{uuid.uuid4().hex[:8]}",
                "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
                "password": "nouppercase1!",
            },
        )
        assert resp.status_code == 400

    def test_register_weak_password_no_digit(self, client):
        """缺少数字应该失败"""
        resp = client.post(
            "/api/v1/auth/register",
            json={
                "username": f"test_{uuid.uuid4().hex[:8]}",
                "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
                "password": "NoDigit!Pass",
            },
        )
        assert resp.status_code == 400

    def test_register_weak_password_no_special(self, client):
        """缺少特殊字符应该失败"""
        resp = client.post(
            "/api/v1/auth/register",
            json={
                "username": f"test_{uuid.uuid4().hex[:8]}",
                "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
                "password": "NoSpecial1Pass",
            },
        )
        assert resp.status_code == 400

    def test_register_weak_password_too_short(self, client):
        """密码太短应该失败"""
        resp = client.post(
            "/api/v1/auth/register",
            json={
                "username": f"test_{uuid.uuid4().hex[:8]}",
                "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
                "password": "Sh0!",
            },
        )
        assert resp.status_code == 400

    def test_register_strong_password_success(self, client):
        """强密码应该成功"""
        username = f"test_{uuid.uuid4().hex[:8]}"
        resp = client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": "Str0ng!Pass",
            },
        )
        assert resp.status_code == 201


class TestLoginErrors:
    """登录错误场景测试"""

    def test_login_wrong_password(self, client):
        """密码错误应该返回 401"""
        user = _register_and_login(client)

        resp = client.post(
            "/api/v1/auth/login",
            json={"username": user["username"], "password": "Wrong!Pass1"},
        )
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        """不存在的用户应该返回 401"""
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent_user", "password": "Some!Pass1"},
        )
        assert resp.status_code == 401

    def test_login_with_email(self, client):
        """使用邮箱登录应该成功"""
        user = _register_and_login(client)

        resp = client.post(
            "/api/v1/auth/login",
            json={"username": user["email"], "password": "Str0ng!Pass"},
        )
        assert resp.status_code == 200


class TestUserProfile:
    """用户信息测试"""

    def test_get_me_unauthorized(self, client):
        """未登录获取用户信息应该失败"""
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_update_username(self, client):
        """修改用户名"""
        user = _register_and_login(client)
        new_username = f"new_{uuid.uuid4().hex[:8]}"

        resp = client.put(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"username": new_username},
        )
        assert resp.status_code == 200
        assert resp.get_json()["data"]["username"] == new_username

    def test_update_email(self, client):
        """修改邮箱"""
        user = _register_and_login(client)
        new_email = f"new_{uuid.uuid4().hex[:8]}@example.com"

        resp = client.put(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"email": new_email},
        )
        assert resp.status_code == 200
        assert resp.get_json()["data"]["email"] == new_email

    def test_update_duplicate_username(self, client):
        """使用已存在的用户名应该失败"""
        user1 = _register_and_login(client)
        user2 = _register_and_login(client)

        resp = client.put(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {user2['access_token']}"},
            json={"username": user1["username"]},
        )
        assert resp.status_code == 400
