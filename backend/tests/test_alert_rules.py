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
        "condition_type": "absolute",
        "metric_name": "p99_response_time",
        "operator": ">",
        "threshold_value": 2000,
    }, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert data["name"] == "P99 Alert"
    assert data["condition_type"] == "absolute"
    assert data["metric_name"] == "p99_response_time"


def test_create_alert_rule_missing_name_returns_400(client):
    headers = _auth_headers(client)
    resp = client.post("/api/v1/perf-test/alert-rules", json={
        "condition_type": "absolute",
    }, headers=headers)
    assert resp.status_code == 400


def test_get_alert_rules(client):
    headers = _auth_headers(client)
    client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Test Rule",
        "condition_type": "absolute",
        "metric_name": "p95_response_time",
        "operator": ">",
        "threshold_value": 1000,
    }, headers=headers)
    resp = client.get("/api/v1/perf-test/alert-rules", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert len(data) >= 1


def test_update_alert_rule(client):
    headers = _auth_headers(client)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Old Name",
        "condition_type": "absolute",
        "metric_name": "rps",
        "operator": "<",
        "threshold_value": 10,
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
        "condition_type": "absolute",
        "metric_name": "rps",
        "operator": ">",
        "threshold_value": 10,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    resp = client.delete(f"/api/v1/perf-test/alert-rules/{rule_id}", headers=headers)
    assert resp.status_code == 200


def test_get_alert_rules_by_scenario(client):
    headers = _auth_headers(client)
    client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Scenario Alert",
        "scenario_id": 999,
        "condition_type": "absolute",
        "metric_name": "p95_response_time",
        "operator": ">",
        "threshold_value": 1000,
    }, headers=headers)
    resp = client.get("/api/v1/perf-test/alert-rules?scenario_id=999", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert len(data) >= 1
    assert all(r["scenario_id"] == 999 for r in data)


def test_create_relative_alert_rule(client):
    headers = _auth_headers(client)
    resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "P95 Degradation Alert",
        "condition_type": "relative",
        "relative_metric": "p95_response_time",
        "degradation_percentage": 20,
    }, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert data["condition_type"] == "relative"
    assert data["degradation_percentage"] == 20


def test_get_alert_rule_detail(client):
    headers = _auth_headers(client)
    create_resp = client.post("/api/v1/perf-test/alert-rules", json={
        "name": "Detail Test",
        "condition_type": "absolute",
        "metric_name": "error_rate",
        "operator": ">",
        "threshold_value": 5.0,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    resp = client.get(f"/api/v1/perf-test/alert-rules/{rule_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()["data"]
    assert data["name"] == "Detail Test"
    assert data["threshold_value"] == 5.0


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
        "condition_type": "absolute",
        "metric_name": "rps",
        "operator": ">",
        "threshold_value": 100,
        "notify_webhook": "https://example.com/hook",
        "is_enabled": True,
    }, headers=headers)
    rule_id = create_resp.get_json()["data"]["id"]
    with app.app_context():
        from app.models.perf_test_alert import PerformanceAlertRule
        rule = PerformanceAlertRule.query.get(rule_id)
        d = rule.to_dict()
        assert d["name"] == "Model Test"
        assert d["metric_name"] == "rps"
        assert d["notify_webhook"] == "https://example.com/hook"
        assert d["is_enabled"] is True
