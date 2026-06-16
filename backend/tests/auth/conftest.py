"""
认证模块测试 fixtures

提供已认证的测试客户端和用户数据。
"""
import pytest


@pytest.fixture()
def registered_user(client):
    """注册并返回用户信息"""
    user_data = {
        "username": "testauthuser",
        "email": "testauth@example.com",
        "password": "Test@123456",
    }
    resp = client.post("/api/v1/auth/register", json=user_data)
    assert resp.status_code in (200, 201), resp.get_data(as_text=True)
    return user_data


@pytest.fixture()
def auth_token(client, registered_user):
    """登录并返回 JWT Token"""
    resp = client.post("/api/v1/auth/login", json={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    assert resp.status_code == 200
    data = resp.get_json()
    return data.get("data", {}).get("access_token", "")


@pytest.fixture()
def auth_headers(auth_token):
    """返回包含 JWT Token 的请求头"""
    return {"Authorization": f"Bearer {auth_token}"}
