import uuid


def test_register_login_me_flow(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    register_resp = client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert register_resp.status_code == 201
    register_payload = register_resp.get_json()
    assert register_payload["code"] == 201

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200
    login_payload = login_resp.get_json()
    access_token = login_payload["data"]["access_token"]

    me_resp = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_resp.status_code == 200
    me_payload = me_resp.get_json()
    assert me_payload["data"]["username"] == username


def test_login_sets_httponly_cookie(client):
    """验证登录成功后同时设置 httpOnly Cookie"""
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200

    # 验证同时返回 access_token（兼容性）和 httpOnly Cookie
    login_payload = login_resp.get_json()
    assert "access_token" in login_payload["data"]

    cookies = login_resp.headers.getlist('Set-Cookie')
    cookie_names = [c.split('=')[0] for c in cookies]
    assert 'access_token_cookie' in cookie_names
    assert 'refresh_token_cookie' in cookie_names


def test_logout_clears_cookie(client):
    """验证登出后 Cookie 被清除"""
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )

    logout_resp = client.post("/api/v1/auth/logout")
    assert logout_resp.status_code == 200
