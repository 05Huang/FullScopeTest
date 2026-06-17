"""
性能告警规则测试
"""
import uuid

from app.extensions import db
from app.models.perf_test_alert import PerformanceAlertRule, PerformanceAlertLog


def _auth_headers(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})
    login_resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    access_token = login_resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_create_alert_rule(client):
    headers = _auth_headers(client)
    resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "P99 Alert",
        "p99_threshold": 2000,
        "error_rate_threshold": 5.0,
    }, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert data["name"] == "P99 Alert"
    assert data["p99_threshold"] == 2000
    assert data["error_rate_threshold"] == 5.0


def test_create_alert_rule_missing_name_returns_400(client):
    headers = _auth_headers(client)
    resp = client.post("/api/v1/perf-test/alert-rules", json={
        "p95_threshold": 1000,
    }, headers=headers)
    assert resp.status_code == 400


def test_get_alert_rules(client):
    headers = _auth_headers(client)
    client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Test Rule",
        "p95_threshold": 1000,
    }, headers=headers)
    resp = client.get("/api/v1/perf-test/alert-rules", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert len(data) >= 1


def test_update_alert_rule(client):
    headers = _auth_headers(client)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Old Name",
        "p95_threshold": 500,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    resp = client.put(f"/api/v1/perf-test/alert-rules/{rule_id}", json={
        "name": "New Name",
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.get_json()["data"]["name"] == "New Name"


def test_delete_alert_rule(client):
    headers = _auth_headers(client)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "To Delete",
        "p95_threshold": 500,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    resp = client.delete(f"/api/v1/perf-test/alert-rules/{rule_id}", headers=headers)
    assert resp.status_code == 200


def test_get_alert_rules_by_scenario(client):
    headers = _auth_headers(client)
    # Create a rule with scenario_id (scenario may not exist, but rule should still be created)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Scenario Alert",
        "scenario_id": 1,
        "p95_threshold": 1000,
    }, headers=headers)
    assert create_resp.status_code == 200
    # Query by scenario_id - should return rules for that scenario
    resp = client.get("/api/v1/perf-test/alert-rules?scenario_id=1", headers=headers)
    assert resp.status_code == 200


def test_create_relative_alert_rule(client):
    headers = _auth_headers(client)
    resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "P95 Degradation Alert",
        "relative_p95_degradation": 20,
        "relative_rps_degradation": 15,
    }, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert data["relative_p95_degradation"] == 20
    assert data["relative_rps_degradation"] == 15


def test_get_alert_rule_detail(client):
    headers = _auth_headers(client)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Detail Test",
        "error_rate_threshold": 5.0,
        "p95_threshold": 2000,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    resp = client.get(f"/api/v1/perf-test/alert-rules/{rule_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert data["name"] == "Detail Test"
    assert data["error_rate_threshold"] == 5.0


def test_get_alert_rule_not_found(client):
    headers = _auth_headers(client)
    resp = client.get("/api/v1/perf-test/alert-rules/999999", headers=headers)
    assert resp.status_code == 404


def test_delete_alert_rule_not_found(client):
    headers = _auth_headers(client)
    resp = client.delete("/api/v1/perf-test/alert-rules/999999", headers=headers)
    assert resp.status_code == 404


def test_alert_rule_model_to_dict(client, app):
    headers = _auth_headers(client)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Model Test",
        "p95_threshold": 100,
        "rps_min_threshold": 50,
        "notify_webhook": "https://example.com/hook",
        "enabled": True,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    with app.app_context():
        from app.models.perf_test_alert import PerformanceAlertRule
        rule = PerformanceAlertRule.query.get(rule_id)
        d = rule.to_dict()
        assert d["name"] == "Model Test"
        assert d["p95_threshold"] == 100
        assert d["notify_webhook"] == "https://example.com/hook"
        assert d["enabled"] is True
