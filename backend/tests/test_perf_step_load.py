import uuid

from app.tasks import _build_locust_command, _build_step_stages


def _auth_headers(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
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
    access_token = login_resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def _create_scenario(client, headers, payload=None):
    body = {
        "name": "step-load-scenario",
        "target_url": "http://localhost:8080/api/v1/ping",
        "user_count": 20,
        "spawn_rate": 2,
        "duration": 60,
    }
    if payload:
        body.update(payload)

    return client.post(
        "/api/v1/perf-test/scenarios",
        json=body,
        headers=headers,
    )


def test_create_scenario_step_load_missing_required_field_returns_400(client):
    headers = _auth_headers(client)
    response = _create_scenario(
        client,
        headers,
        payload={
            "step_load_enabled": True,
            "step_duration": 30,
        },
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert "step_users" in payload["message"]


def test_update_scenario_step_load_missing_fields_returns_400(client):
    headers = _auth_headers(client)
    create_response = _create_scenario(client, headers)
    assert create_response.status_code == 200
    scenario_id = create_response.get_json()["data"]["id"]

    update_response = client.put(
        f"/api/v1/perf-test/scenarios/{scenario_id}",
        json={"step_load_enabled": True},
        headers=headers,
    )

    assert update_response.status_code == 400
    payload = update_response.get_json()
    assert "step_users and step_duration" in payload["message"]


def test_run_scenario_step_load_missing_fields_returns_400(client):
    headers = _auth_headers(client)
    create_response = _create_scenario(client, headers)
    assert create_response.status_code == 200
    scenario_id = create_response.get_json()["data"]["id"]

    run_response = client.post(
        f"/api/v1/perf-test/scenarios/{scenario_id}/run",
        json={"step_load_enabled": True},
        headers=headers,
    )

    assert run_response.status_code == 400
    payload = run_response.get_json()
    assert "step_users and step_duration" in payload["message"]


def test_build_step_stages_incremental_users():
    stages = _build_step_stages(
        user_count=35,
        step_users=10,
        step_duration=30,
        run_time=95,
    )

    assert stages == [
        {"start": 0, "end": 30, "users": 10, "spawn_rate": 1},
        {"start": 30, "end": 60, "users": 20, "spawn_rate": 1},
        {"start": 60, "end": 90, "users": 30, "spawn_rate": 1},
        {"start": 90, "end": 95, "users": 35, "spawn_rate": 1},
    ]


def test_build_step_stages_keeps_target_users_until_run_time_end():
    stages = _build_step_stages(
        user_count=10,
        step_users=10,
        step_duration=30,
        run_time=90,
    )

    assert stages == [
        {"start": 0, "end": 30, "users": 10, "spawn_rate": 1},
        {"start": 30, "end": 60, "users": 10, "spawn_rate": 1},
        {"start": 60, "end": 90, "users": 10, "spawn_rate": 1},
    ]


def test_build_locust_command_switches_between_fixed_and_step_mode():
    normal_cmd = _build_locust_command(
        locustfile="locustfile.py",
        base_host="http://localhost:8080",
        csv_prefix="rt",
        run_time=120,
        user_count=50,
        spawn_rate=5,
        step_load_enabled=False,
    )
    assert "--users" in normal_cmd
    assert "--spawn-rate" in normal_cmd

    step_cmd = _build_locust_command(
        locustfile="locustfile.py",
        base_host="http://localhost:8080",
        csv_prefix="rt",
        run_time=120,
        user_count=50,
        spawn_rate=5,
        step_load_enabled=True,
    )
    assert "--users" not in step_cmd
    assert "--spawn-rate" not in step_cmd
