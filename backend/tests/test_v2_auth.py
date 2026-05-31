"""FastAPI v2 Auth tests"""
import uuid
import pytest
from fastapi.testclient import TestClient
from app.fastapi_app import create_fastapi_app


@pytest.fixture()
def v2_client(app):
    """Create FastAPI test client that shares the same DB as Flask"""
    # Create FastAPI app and share Flask's database session
    fastapi_app = create_fastapi_app("testing", flask_app=app)

    client = TestClient(fastapi_app)
    return client


def test_v2_register_login_me_flow(v2_client):
    """Test v2 register -> login -> me flow"""
    username = f"v2_user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    register_resp = v2_client.post(
        "/api/v2/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert register_resp.status_code == 200
    register_payload = register_resp.json()
    assert register_payload["username"] == username

    login_resp = v2_client.post(
        "/api/v2/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200
    login_payload = login_resp.json()
    access_token = login_payload["access_token"]

    me_resp = v2_client.get(
        "/api/v2/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_resp.status_code == 200
    me_payload = me_resp.json()
    assert me_payload["username"] == username


def test_v2_register_duplicate_username(v2_client):
    """Test v2 register with duplicate username"""
    username = f"dup_user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    v2_client.post(
        "/api/v2/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    resp = v2_client.post(
        "/api/v2/auth/register",
        json={"username": username, "email": "other@example.com", "password": password},
    )
    assert resp.status_code == 400


def test_v2_login_wrong_password(v2_client):
    """Test v2 login with wrong password"""
    username = f"wrongpw_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    v2_client.post(
        "/api/v2/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    resp = v2_client.post(
        "/api/v2/auth/login",
        json={"username": username, "password": "WrongPassword"},
    )
    assert resp.status_code == 401


def test_v2_get_me_unauthorized(v2_client):
    """Test v2 /me without token"""
    resp = v2_client.get("/api/v2/auth/me")
    assert resp.status_code in (401, 403)


def test_v2_refresh_token(v2_client):
    """Test v2 token refresh"""
    username = f"refresh_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    v2_client.post(
        "/api/v2/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    login_resp = v2_client.post(
        "/api/v2/auth/login",
        json={"username": username, "password": password},
    )
    access_token = login_resp.json()["access_token"]

    refresh_resp = v2_client.post(
        "/api/v2/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.json()
