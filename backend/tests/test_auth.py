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
