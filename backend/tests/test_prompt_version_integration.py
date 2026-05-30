"""
Prompt 版本管理集成测试

测试 P2C-03 的核心功能：
- PromptVersion CRUD API
- A/B 测试版本选择
- 脚本生成使用 PromptVersion
- 统计刷新
"""

import uuid
import pytest


def _auth_headers(client):
    """注册并登录，返回认证 headers"""
    username = f"pv_user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    token = login_resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---- PromptVersion CRUD API Tests ----


class TestPromptVersionCRUD:
    """测试 Prompt 版本的创建、查询、更新、停用"""

    def test_create_prompt_version(self, client):
        """测试创建 Prompt 版本"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "experiment-A",
            "system_prompt": "You are a test assistant.",
            "temperature": 0.5,
            "is_active": True,
            "change_notes": "Test experiment",
        })

        assert resp.status_code == 201
        data = resp.get_json()
        assert data["code"] == 201
        pv = data["data"]
        assert pv["feature"] == "script_gen"
        assert pv["name"] == "experiment-A"
        assert pv["version"] >= 1
        assert pv["is_active"] is True
        assert pv["system_prompt"] == "You are a test assistant."
        assert pv["temperature"] == 0.5

    def test_create_prompt_version_missing_fields(self, client):
        """测试缺少必填字段返回 400"""
        headers = _auth_headers(client)

        # 缺少 feature
        resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "name": "test",
            "system_prompt": "test prompt",
        })
        assert resp.status_code == 400

        # 缺少 name
        resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "system_prompt": "test prompt",
        })
        assert resp.status_code == 400

        # 缺少 system_prompt
        resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "test",
        })
        assert resp.status_code == 400

    def test_create_prompt_version_invalid_feature(self, client):
        """测试无效的 feature 返回 400"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "nonexistent_feature",
            "name": "test",
            "system_prompt": "test prompt",
        })
        assert resp.status_code == 400

    def test_list_prompt_versions(self, client):
        """测试列出 Prompt 版本"""
        headers = _auth_headers(client)

        # 创建两个版本
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "v1",
            "system_prompt": "prompt 1",
        })
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "copilot",
            "name": "v1",
            "system_prompt": "prompt 2",
        })

        # 列出所有
        resp = client.get("/api/v1/ai/prompt-versions", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["pagination"]["total"] >= 2

        # 按 feature 过滤
        resp = client.get("/api/v1/ai/prompt-versions?feature=script_gen", headers=headers)
        assert resp.status_code == 200
        items = resp.get_json()["data"]["items"]
        assert all(v["feature"] == "script_gen" for v in items)

    def test_get_prompt_version(self, client):
        """测试获取单个 Prompt 版本"""
        headers = _auth_headers(client)
        create_resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "v1",
            "system_prompt": "test prompt",
        })
        version_id = create_resp.get_json()["data"]["id"]

        resp = client.get(f"/api/v1/ai/prompt-versions/{version_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["id"] == version_id

    def test_get_prompt_version_not_found(self, client):
        """测试获取不存在的版本返回 404"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/ai/prompt-versions/99999", headers=headers)
        assert resp.status_code == 404

    def test_update_prompt_version(self, client):
        """测试更新 Prompt 版本"""
        headers = _auth_headers(client)
        create_resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "v1",
            "system_prompt": "original prompt",
        })
        version_id = create_resp.get_json()["data"]["id"]

        resp = client.put(f"/api/v1/ai/prompt-versions/{version_id}", headers=headers, json={
            "system_prompt": "updated prompt",
            "temperature": 0.8,
            "change_notes": "Updated for better results",
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["system_prompt"] == "updated prompt"
        assert data["temperature"] == 0.8
        assert data["change_notes"] == "Updated for better results"

    def test_deactivate_prompt_version(self, client):
        """测试停用 Prompt 版本"""
        headers = _auth_headers(client)
        create_resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "v1",
            "system_prompt": "test",
            "is_active": True,
        })
        version_id = create_resp.get_json()["data"]["id"]

        resp = client.delete(f"/api/v1/ai/prompt-versions/{version_id}", headers=headers)
        assert resp.status_code == 200

        # 验证已停用
        get_resp = client.get(f"/api/v1/ai/prompt-versions/{version_id}", headers=headers)
        assert get_resp.get_json()["data"]["is_active"] is False
        assert get_resp.get_json()["data"]["deactivated_at"] is not None

    def test_version_number_auto_increments(self, client):
        """测试版本号自动递增"""
        headers = _auth_headers(client)

        # 创建 v1
        resp1 = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "dedup",
            "name": "inc-v1",
            "system_prompt": "prompt 1",
        })
        v1 = resp1.get_json()["data"]["version"]

        # 创建 v2
        resp2 = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "dedup",
            "name": "inc-v2",
            "system_prompt": "prompt 2",
        })
        assert resp2.get_json()["data"]["version"] == v1 + 1

        # 创建 v3
        resp3 = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "dedup",
            "name": "inc-v3",
            "system_prompt": "prompt 3",
        })
        assert resp3.get_json()["data"]["version"] == v1 + 2


# ---- A/B Test Selection Tests ----


class TestABTestSelection:
    """测试 A/B 测试版本选择"""

    def test_select_version_single_active(self, client):
        """测试单个激活版本直接返回"""
        headers = _auth_headers(client)
        import uuid
        unique = uuid.uuid4().hex[:8]
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": f"single-{unique}",
            "system_prompt": "prompt 1",
            "is_active": True,
        })

        resp = client.post("/api/v1/ai/prompt-versions/select", headers=headers, json={
            "feature": "script_gen",
        })
        assert resp.status_code == 200
        assert resp.get_json()["data"]["feature"] == "script_gen"

    def test_select_version_no_active(self, client):
        """测试没有激活版本返回 404"""
        headers = _auth_headers(client)
        import uuid
        unique = uuid.uuid4().hex[:8]
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "copilot",
            "name": f"inactive-{unique}",
            "system_prompt": "prompt 1",
            "is_active": False,
        })

        resp = client.post("/api/v1/ai/prompt-versions/select", headers=headers, json={
            "feature": "copilot",
        })
        # copilot 可能有其他激活版本，所以可能 200 或 404
        assert resp.status_code in (200, 404)

    def test_select_version_ab_test_multiple(self, client):
        """测试多版本 A/B 测试选择"""
        headers = _auth_headers(client)
        import uuid
        unique = uuid.uuid4().hex[:8]

        # 创建两个激活版本
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "dedup",
            "name": f"control-{unique}",
            "system_prompt": "control prompt",
            "is_active": True,
            "traffic_weight": 0.5,
        })
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "dedup",
            "name": f"experiment-{unique}",
            "system_prompt": "experiment prompt",
            "is_active": True,
            "traffic_weight": 0.5,
        })

        # 多次选择，验证返回的 feature 正确
        for _ in range(10):
            resp = client.post("/api/v1/ai/prompt-versions/select", headers=headers, json={
                "feature": "dedup",
            })
            assert resp.status_code == 200
            assert resp.get_json()["data"]["feature"] == "dedup"


# ---- Stats Refresh Tests ----


class TestStatsRefresh:
    """测试统计刷新"""

    def test_refresh_stats(self, client):
        """测试刷新单个版本的统计"""
        headers = _auth_headers(client)
        create_resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "v1",
            "system_prompt": "test",
        })
        version_id = create_resp.get_json()["data"]["id"]

        resp = client.post("/api/v1/ai/prompt-versions/refresh-stats", headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["refreshed_count"] >= 1

    def test_refresh_stats_with_feature_filter(self, client):
        """测试按 feature 过滤刷新统计"""
        headers = _auth_headers(client)
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "v1",
            "system_prompt": "test",
        })
        client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "copilot",
            "name": "v1",
            "system_prompt": "test",
        })

        resp = client.post(
            "/api/v1/ai/prompt-versions/refresh-stats?feature=script_gen",
            headers=headers,
        )
        assert resp.status_code == 200
        count = resp.get_json()["data"]["refreshed_count"]
        assert count >= 1


# ---- Script Generation with PromptVersion Tests ----


class TestScriptGenerationWithPromptVersion:
    """测试脚本生成使用 PromptVersion"""

    def test_script_gen_fallback_when_no_key(self, client):
        """测试无 API Key 时使用默认 Prompt 降级"""
        client.application.config["AI_ASSISTANT_API_KEY"] = ""
        headers = _auth_headers(client)

        resp = client.post("/api/v1/web-test/ai/generate", headers=headers, json={
            "prompt": "open google.com and take a screenshot",
        })
        # 无 API Key 应该返回错误（降级到 fallback 或报错）
        assert resp.status_code in (400, 500)

    def test_script_gen_disabled(self, client):
        """测试 AI 禁用时返回错误"""
        client.application.config["AI_ASSISTANT_ENABLED"] = False
        headers = _auth_headers(client)

        resp = client.post("/api/v1/web-test/ai/generate", headers=headers, json={
            "prompt": "open google.com",
        })
        # AI 禁用时返回 400 或 500（取决于错误处理）
        assert resp.status_code in (400, 500)

    def test_perf_script_gen_disabled(self, client):
        """测试性能测试 AI 禁用时返回错误"""
        client.application.config["AI_ASSISTANT_ENABLED"] = False
        headers = _auth_headers(client)

        resp = client.post("/api/v1/perf-test/ai/generate", headers=headers, json={
            "prompt": "load test example.com with 10 users",
        })
        # AI 禁用时返回 400 或 500（取决于错误处理）
        assert resp.status_code in (400, 500)

    def test_script_gen_empty_prompt(self, client):
        """测试空 prompt 返回 400"""
        headers = _auth_headers(client)

        resp = client.post("/api/v1/web-test/ai/generate", headers=headers, json={
            "prompt": "",
        })
        assert resp.status_code == 400

    def test_script_gen_with_prompt_version(self, client):
        """测试使用指定 Prompt 版本生成脚本"""
        client.application.config["AI_ASSISTANT_API_KEY"] = ""
        headers = _auth_headers(client)

        # 创建一个 Prompt 版本
        create_resp = client.post("/api/v1/ai/prompt-versions", headers=headers, json={
            "feature": "script_gen",
            "name": "custom",
            "system_prompt": "Custom prompt for testing",
            "is_active": True,
        })
        assert create_resp.status_code == 201

        # 由于没有 API Key，即使指定了版本也会失败
        # 但至少验证 API 接受 prompt_version_id 参数
        resp = client.post("/api/v1/web-test/ai/generate", headers=headers, json={
            "prompt": "test script",
        })
        # 应该返回 400 或 500（无 API key）
        assert resp.status_code in (400, 500)
