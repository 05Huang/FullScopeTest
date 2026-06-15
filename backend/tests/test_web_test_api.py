"""
Web 测试模块 API 集成测试

覆盖：集合 CRUD、脚本 CRUD、健康检查、录制状态、权限校验、边界条件
"""

import uuid


def _auth_headers(client):
    username = f"wt_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    token = resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ====================================================================
# 健康检查
# ====================================================================

class TestWebTestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/api/v1/web-test/health")
        assert resp.status_code == 200
        assert resp.get_json()["code"] == 200


# ====================================================================
# 集合 CRUD
# ====================================================================

class TestWebCollectionCRUD:
    def test_create_collection(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/collections", headers=headers, json={"name": "Smoke"})
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["id"] is not None
        assert data["name"] == "Smoke"

    def test_get_collection_list(self, client):
        headers = _auth_headers(client)
        client.post("/api/v1/web-test/collections", headers=headers, json={"name": "A"})
        client.post("/api/v1/web-test/collections", headers=headers, json={"name": "B"})
        resp = client.get("/api/v1/web-test/collections", headers=headers)
        assert resp.status_code == 200
        items = resp.get_json()["data"]
        assert len(items) >= 2

    def test_update_collection(self, client):
        headers = _auth_headers(client)
        cid = client.post("/api/v1/web-test/collections", headers=headers, json={"name": "Old"}).get_json()["data"]["id"]
        resp = client.put(f"/api/v1/web-test/collections/{cid}", headers=headers, json={"name": "New"})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["name"] == "New"

    def test_delete_collection(self, client):
        headers = _auth_headers(client)
        cid = client.post("/api/v1/web-test/collections", headers=headers, json={"name": "ToDel"}).get_json()["data"]["id"]
        resp = client.delete(f"/api/v1/web-test/collections/{cid}", headers=headers)
        assert resp.status_code == 200

    def test_update_nonexistent_collection_returns_404(self, client):
        headers = _auth_headers(client)
        resp = client.put("/api/v1/web-test/collections/99999", headers=headers, json={"name": "X"})
        assert resp.status_code == 404

    def test_delete_nonexistent_collection_returns_404(self, client):
        headers = _auth_headers(client)
        resp = client.delete("/api/v1/web-test/collections/99999", headers=headers)
        assert resp.status_code == 404

    def test_create_collection_unauthorized(self, client):
        resp = client.post("/api/v1/web-test/collections", json={"name": "NoAuth"})
        assert resp.status_code == 401

    def test_create_collection_empty_body(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/collections", headers=headers, json={})
        # 空 name 允许通过（无严格必填）
        assert resp.status_code in (200, 400)


# ====================================================================
# 脚本 CRUD
# ====================================================================

class TestWebScriptCRUD:
    def test_create_script(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "S1"})
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["name"] == "S1"
        assert data["id"] is not None

    def test_create_script_missing_name_returns_400(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/scripts", headers=headers, json={"description": "no name"})
        assert resp.status_code == 400

    def test_get_script_detail(self, client):
        headers = _auth_headers(client)
        sid = client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "D"}).get_json()["data"]["id"]
        resp = client.get(f"/api/v1/web-test/scripts/{sid}", headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["name"] == "D"

    def test_update_script(self, client):
        headers = _auth_headers(client)
        sid = client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "Old"}).get_json()["data"]["id"]
        resp = client.put(f"/api/v1/web-test/scripts/{sid}", headers=headers, json={"name": "New"})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["name"] == "New"

    def test_delete_script(self, client):
        headers = _auth_headers(client)
        sid = client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "Del"}).get_json()["data"]["id"]
        resp = client.delete(f"/api/v1/web-test/scripts/{sid}", headers=headers)
        assert resp.status_code == 200

    def test_get_nonexistent_script_returns_404(self, client):
        headers = _auth_headers(client)
        resp = client.get("/api/v1/web-test/scripts/99999", headers=headers)
        assert resp.status_code == 404

    def test_update_nonexistent_script_returns_404(self, client):
        headers = _auth_headers(client)
        resp = client.put("/api/v1/web-test/scripts/99999", headers=headers, json={"name": "X"})
        assert resp.status_code == 404

    def test_delete_nonexistent_script_returns_404(self, client):
        headers = _auth_headers(client)
        resp = client.delete("/api/v1/web-test/scripts/99999", headers=headers)
        assert resp.status_code == 404

    def test_create_script_with_custom_content(self, client):
        headers = _auth_headers(client)
        custom = "print('custom')"
        resp = client.post("/api/v1/web-test/scripts", headers=headers,
                           json={"name": "Custom", "script_content": custom})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["script_content"] == custom

    def test_create_script_with_collection(self, client):
        headers = _auth_headers(client)
        cid = client.post("/api/v1/web-test/collections", headers=headers, json={"name": "C"}).get_json()["data"]["id"]
        resp = client.post("/api/v1/web-test/scripts", headers=headers,
                           json={"name": "InCol", "collection_id": cid})
        assert resp.status_code == 200
        assert resp.get_json()["data"]["collection_id"] == cid

    def test_create_script_collection_not_found(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/scripts", headers=headers,
                           json={"name": "BadCol", "collection_id": 99999})
        assert resp.status_code == 404

    def test_create_script_default_has_template(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "Tpl"})
        content = resp.get_json()["data"]["script_content"]
        assert "playwright" in content.lower() or "playwright" in content

    def test_scripts_filter_by_collection(self, client):
        headers = _auth_headers(client)
        cid = client.post("/api/v1/web-test/collections", headers=headers, json={"name": "F"}).get_json()["data"]["id"]
        client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "A", "collection_id": cid})
        client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "B"})
        resp = client.get(f"/api/v1/web-test/scripts?collection_id={cid}", headers=headers)
        items = resp.get_json()["data"]
        assert len(items) == 1


# ====================================================================
# 脚本运行
# ====================================================================

class TestWebScriptRun:
    def test_run_script(self, client, monkeypatch):
        from types import SimpleNamespace
        headers = _auth_headers(client)
        sid = client.post("/api/v1/web-test/scripts", headers=headers, json={"name": "R"}).get_json()["data"]["id"]

        def _fake_apply_async(*a, **k):
            return SimpleNamespace(id="fake-task-001")
        monkeypatch.setattr("app.api.web_test.run_web_test_task.apply_async", _fake_apply_async)

        resp = client.post(f"/api/v1/web-test/scripts/{sid}/run", headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["task_id"] == "fake-task-001"

    def test_run_nonexistent_script_returns_404(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/scripts/99999/run", headers=headers)
        assert resp.status_code == 404


# ====================================================================
# 录制状态
# ====================================================================

class TestRecordingStatus:
    def test_status_when_no_recording(self, client):
        headers = _auth_headers(client)
        resp = client.get("/api/v1/web-test/record/status", headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["is_recording"] is False

    def test_stop_when_no_recording_returns_400(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/record/stop", headers=headers)
        assert resp.status_code == 400


# ====================================================================
# SSRF 防护集成
# ====================================================================

class TestWebTestSSRF:
    def test_explore_rejects_localhost(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/ai/explore", headers=headers,
                           json={"start_url": "http://127.0.0.1/admin"})
        assert resp.status_code == 400
        assert "内网" in resp.get_json()["message"]

    def test_record_rejects_localhost(self, client):
        headers = _auth_headers(client)
        resp = client.post("/api/v1/web-test/record/start", headers=headers,
                           json={"url": "http://192.168.1.1/admin"})
        assert resp.status_code == 400
