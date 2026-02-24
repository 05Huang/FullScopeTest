import uuid


def _auth_headers(client):
    username = f"ai_user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    register_resp = client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert register_resp.status_code == 201

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200
    token = login_resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_ai_plan_generates_fallback_operations(client):
    client.application.config["AI_ASSISTANT_API_KEY"] = ""
    headers = _auth_headers(client)

    response = client.post(
        "/api/v1/api-test/ai/plan",
        headers=headers,
        json={"prompt": "create environment and run collection"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["code"] == 200
    assert payload["data"]["source"] == "fallback"
    assert isinstance(payload["data"]["operations"], list)
    assert len(payload["data"]["operations"]) >= 1
    assert any(op["type"] == "create_case" for op in payload["data"]["operations"])


def test_ai_plan_returns_400_when_disabled(client):
    client.application.config["AI_ASSISTANT_ENABLED"] = False
    headers = _auth_headers(client)

    response = client.post(
        "/api/v1/api-test/ai/plan",
        headers=headers,
        json={"prompt": "create some cases"},
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["code"] == 400
    assert "disabled" in payload["message"].lower()

