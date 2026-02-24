import uuid
from types import SimpleNamespace

from app.extensions import db
from app.models.web_test_script import WebTestScript


def _auth_headers(client):
    username = f"web_user_{uuid.uuid4().hex[:8]}"
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


def test_web_collection_crud_and_script_filter(client):
    headers = _auth_headers(client)

    create_collection_resp = client.post(
        "/api/v1/web-test/collections",
        headers=headers,
        json={"name": "smoke", "description": "smoke tests"},
    )
    assert create_collection_resp.status_code == 200
    collection_payload = create_collection_resp.get_json()
    collection_id = collection_payload["data"]["id"]

    script_1_resp = client.post(
        "/api/v1/web-test/scripts",
        headers=headers,
        json={
            "name": "login case",
            "collection_id": collection_id,
            "script_content": "print('ok')",
        },
    )
    assert script_1_resp.status_code == 200
    script_1_id = script_1_resp.get_json()["data"]["id"]

    script_2_resp = client.post(
        "/api/v1/web-test/scripts",
        headers=headers,
        json={
            "name": "profile case",
            "script_content": "print('ok')",
        },
    )
    assert script_2_resp.status_code == 200
    script_2_id = script_2_resp.get_json()["data"]["id"]

    filter_resp = client.get(
        f"/api/v1/web-test/scripts?collection_id={collection_id}",
        headers=headers,
    )
    assert filter_resp.status_code == 200
    filter_data = filter_resp.get_json()["data"]
    assert len(filter_data) == 1
    assert filter_data[0]["id"] == script_1_id

    bind_resp = client.put(
        f"/api/v1/web-test/scripts/{script_2_id}",
        headers=headers,
        json={"collection_id": collection_id},
    )
    assert bind_resp.status_code == 200

    filter_resp_after_bind = client.get(
        f"/api/v1/web-test/scripts?collection_id={collection_id}",
        headers=headers,
    )
    assert filter_resp_after_bind.status_code == 200
    ids = {item["id"] for item in filter_resp_after_bind.get_json()["data"]}
    assert ids == {script_1_id, script_2_id}

    delete_collection_resp = client.delete(
        f"/api/v1/web-test/collections/{collection_id}",
        headers=headers,
    )
    assert delete_collection_resp.status_code == 200

    script_2_detail_resp = client.get(
        f"/api/v1/web-test/scripts/{script_2_id}",
        headers=headers,
    )
    assert script_2_detail_resp.status_code == 200
    assert script_2_detail_resp.get_json()["data"]["collection_id"] is None


def test_run_web_collection_submit_and_skip_running(client, monkeypatch):
    headers = _auth_headers(client)

    collection_resp = client.post(
        "/api/v1/web-test/collections",
        headers=headers,
        json={"name": "batch"},
    )
    collection_id = collection_resp.get_json()["data"]["id"]

    script_1 = client.post(
        "/api/v1/web-test/scripts",
        headers=headers,
        json={"name": "case1", "collection_id": collection_id, "script_content": "print('ok')"},
    ).get_json()["data"]
    script_2 = client.post(
        "/api/v1/web-test/scripts",
        headers=headers,
        json={"name": "case2", "collection_id": collection_id, "script_content": "print('ok')"},
    ).get_json()["data"]

    with client.application.app_context():
        s2 = db.session.get(WebTestScript, script_2["id"])
        s2.status = "running"
        db.session.commit()

    task_counter = {"count": 0}

    def _fake_apply_async(*args, **kwargs):
        task_counter["count"] += 1
        return SimpleNamespace(id=f"fake-task-{task_counter['count']}")

    monkeypatch.setattr("app.api.web_test.run_web_test_task.apply_async", _fake_apply_async)

    run_resp = client.post(
        f"/api/v1/web-test/collections/{collection_id}/run",
        headers=headers,
    )
    assert run_resp.status_code == 200
    payload = run_resp.get_json()["data"]
    assert payload["submitted_count"] == 1
    assert len(payload["submitted"]) == 1
    assert payload["submitted"][0]["script_id"] == script_1["id"]
    assert len(payload["skipped"]) == 1
    assert payload["skipped"][0]["script_id"] == script_2["id"]
