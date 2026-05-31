"""FastAPI v2 Performance test module tests"""

import uuid
import pytest
from fastapi.testclient import TestClient
from app.fastapi_app import create_fastapi_app


@pytest.fixture()
def v2_client(app):
    fastapi_app = create_fastapi_app("testing", flask_app=app)
    with app.app_context():
        from app.extensions import db as flask_db
        flask_db.create_all()
        client = TestClient(fastapi_app)
        client.flask_app = app
        yield client


def _rl(client, username=None):
    if username is None:
        username = f"v2perf_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    client.post("/api/v2/auth/register", json={"username": username, "email": email, "password": "Str0ng!Pass"})
    resp = client.post("/api/v2/auth/login", json={"username": username, "password": "Str0ng!Pass"})
    return {"username": username, "access_token": resp.json()["access_token"]}


def _h(token):
    return {"Authorization": f"Bearer {token}"}


class TestV2PerfScenarios:
    def test_unauth(self, v2_client):
        assert v2_client.get("/api/v2/perf-tests/scenarios").status_code in (401, 403)

    def test_empty(self, v2_client):
        u = _rl(v2_client)
        r = v2_client.get("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]))
        assert r.status_code == 200 and r.json() == []

    def test_create(self, v2_client):
        u = _rl(v2_client)
        r = v2_client.post("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]),
            json={"name": "TS", "target_url": "https://httpbin.org/get", "user_count": 5, "spawn_rate": 1, "duration": 10})
        assert r.status_code == 201 and r.json()["name"] == "TS"

    def test_invalid_url(self, v2_client):
        u = _rl(v2_client)
        r = v2_client.post("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]),
            json={"name": "X", "target_url": "not-a-url"})
        assert r.status_code == 400

    def test_invalid_numbers(self, v2_client):
        u = _rl(v2_client)
        r = v2_client.post("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]),
            json={"name": "X", "user_count": 5000, "spawn_rate": 1, "duration": 10})
        assert r.status_code in (400, 422)

    def test_get_one(self, v2_client):
        u = _rl(v2_client)
        c = v2_client.post("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]),
            json={"name": "GM", "target_url": "https://httpbin.org/get"})
        sid = c.json()["id"]
        r = v2_client.get(f"/api/v2/perf-tests/scenarios/{sid}", headers=_h(u["access_token"]))
        assert r.status_code == 200 and r.json()["name"] == "GM"

    def test_not_found(self, v2_client):
        u = _rl(v2_client)
        assert v2_client.get("/api/v2/perf-tests/scenarios/99999", headers=_h(u["access_token"])).status_code == 404

    def test_update(self, v2_client):
        u = _rl(v2_client)
        c = v2_client.post("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]),
            json={"name": "Orig", "target_url": "https://httpbin.org/get"})
        sid = c.json()["id"]
        r = v2_client.put(f"/api/v2/perf-tests/scenarios/{sid}", headers=_h(u["access_token"]), json={"name": "Upd"})
        assert r.status_code == 200 and r.json()["name"] == "Upd"

    def test_delete(self, v2_client):
        u = _rl(v2_client)
        c = v2_client.post("/api/v2/perf-tests/scenarios", headers=_h(u["access_token"]),
            json={"name": "Del", "target_url": "https://httpbin.org/get"})
        sid = c.json()["id"]
        v2_client.delete(f"/api/v2/perf-tests/scenarios/{sid}", headers=_h(u["access_token"]))
        assert v2_client.get(f"/api/v2/perf-tests/scenarios/{sid}", headers=_h(u["access_token"])).status_code == 404


class TestV2PerfAlertRules:
    def test_unauth(self, v2_client):
        assert v2_client.get("/api/v2/perf-tests/alert-rules").status_code in (401, 403)

    def test_create(self, v2_client):
        u = _rl(v2_client)
        r = v2_client.post("/api/v2/perf-tests/alert-rules", headers=_h(u["access_token"]),
            json={"name": "P95", "condition_type": "absolute", "metric_name": "p95_response_time",
                  "operator": ">", "threshold_value": 2000})
        assert r.status_code == 201 and r.json()["name"] == "P95"

    def test_list(self, v2_client):
        u = _rl(v2_client)
        v2_client.post("/api/v2/perf-tests/alert-rules", headers=_h(u["access_token"]),
            json={"name": "R1", "condition_type": "absolute", "metric_name": "rps",
                  "operator": "<", "threshold_value": 10})
        r = v2_client.get("/api/v2/perf-tests/alert-rules", headers=_h(u["access_token"]))
        assert r.status_code == 200 and len(r.json()) >= 1

    def test_delete(self, v2_client):
        u = _rl(v2_client)
        c = v2_client.post("/api/v2/perf-tests/alert-rules", headers=_h(u["access_token"]),
            json={"name": "D", "condition_type": "absolute", "metric_name": "rps",
                  "operator": "<", "threshold_value": 10})
        rid = c.json()["id"]
        assert v2_client.delete(f"/api/v2/perf-tests/alert-rules/{rid}", headers=_h(u["access_token"])).status_code == 200


class TestV2PerfResults:
    def test_unauth(self, v2_client):
        assert v2_client.get("/api/v2/perf-tests/results").status_code in (401, 403)

    def test_empty(self, v2_client):
        u = _rl(v2_client)
        r = v2_client.get("/api/v2/perf-tests/results", headers=_h(u["access_token"]))
        assert r.status_code == 200 and r.json()["total"] == 0

    def test_compare_needs_2(self, v2_client):
        u = _rl(v2_client)
        assert v2_client.get("/api/v2/perf-tests/compare?run_ids=1", headers=_h(u["access_token"])).status_code == 400


class TestV2PerfRunning:
    def test_unauth(self, v2_client):
        assert v2_client.get("/api/v2/perf-tests/running").status_code in (401, 403)

    def test_empty(self, v2_client):
        u = _rl(v2_client)
        assert v2_client.get("/api/v2/perf-tests/running", headers=_h(u["access_token"])).json() == []


class TestV2PerfAI:
    def test_unauth(self, v2_client):
        assert v2_client.post("/api/v2/perf-tests/ai/generate", json={"prompt": "x"}).status_code in (401, 403)

    def test_no_prompt(self, v2_client):
        u = _rl(v2_client)
        assert v2_client.post("/api/v2/perf-tests/ai/generate", headers=_h(u["access_token"]), json={}).status_code == 400
