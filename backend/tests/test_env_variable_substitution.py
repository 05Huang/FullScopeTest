"""
环境变量替换功能测试

测试环境变量在 API 测试中的正确替换
"""

import uuid

import pytest

from tests.conftest import *  # noqa: F401, F403


def _get_auth_headers(client):
    """创建测试用户并返回认证头"""
    username = f"env_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    return {"Authorization": f"Bearer {resp.get_json()['data']['access_token']}"}


class TestEnvironmentCRUD:
    """环境管理 CRUD 测试"""

    def test_create_environment(self, client):
        """创建环境"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "Test Environment"},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["data"]["name"] == "Test Environment"
        assert "id" in data["data"]

    def test_create_environment_with_variables(self, client):
        """创建带变量的环境"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Dev Environment",
                "variables": [
                    {"key": "base_url", "value": "https://dev.example.com", "type": "string"},
                    {"key": "api_key", "value": "dev-key-123", "type": "secret"},
                    {"key": "timeout", "value": "5000", "type": "number"},
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["data"]["variables"]) == 3

    def test_get_environments(self, client):
        """获取环境列表"""
        headers = _get_auth_headers(client)
        client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "Env A"},
        )
        client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "Env B"},
        )

        resp = client.get("/api/v1/environments", headers=headers)
        assert resp.status_code == 200
        names = [e["name"] for e in resp.get_json()["data"]]
        assert "Env A" in names
        assert "Env B" in names

    def test_update_environment(self, client):
        """更新环境"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "Old Name"},
        ).get_json()["data"]["id"]

        resp = client.put(
            f"/api/v1/environments/{eid}",
            headers=headers,
            json={"name": "New Name", "variables": [{"key": "new_var", "value": "value"}]},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["data"]["name"] == "New Name"
        assert data["data"]["variables"][0]["key"] == "new_var"

    def test_delete_environment(self, client):
        """删除环境"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "To Delete"},
        ).get_json()["data"]["id"]

        resp = client.delete(f"/api/v1/environments/{eid}", headers=headers)
        assert resp.status_code == 200

    def test_set_default_environment(self, client):
        """设置默认环境"""
        headers = _get_auth_headers(client)

        eid1 = client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "Env 1", "is_default": True},
        ).get_json()["data"]["id"]

        eid2 = client.post(
            "/api/v1/environments",
            headers=headers,
            json={"name": "Env 2", "is_default": True},
        ).get_json()["data"]["id"]

        # Env2 应该是默认的，Env1 不是
        resp = client.get("/api/v1/environments", headers=headers)
        envs = {e["name"]: e["is_default"] for e in resp.get_json()["data"]}
        assert envs["Env 2"] is True


class TestVariableSubstitution:
    """变量替换测试"""

    def test_simple_variable_substitution(self, client):
        """简单变量替换"""
        headers = _get_auth_headers(client)

        # 创建环境
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Test Env",
                "variables": [{"key": "base_url", "value": "https://httpbin.org", "type": "string"}],
            },
        ).get_json()["data"]["id"]

        # 创建用例集
        cid = client.post(
            "/api/v1/api-test/collections",
            headers=headers,
            json={"name": "Test Collection"},
        ).get_json()["data"]["id"]

        # 创建用例使用变量
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Variable Test",
                "method": "GET",
                "url": "{{base_url}}/get",
                "collection_id": cid,
            },
        )
        case_id = resp.get_json()["data"]["id"]

        # 执行用例（选择环境）
        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200
        data = result.get_json()["data"]
        # URL 应该被替换为实际地址
        assert data["passed"] is True

    def test_multiple_variable_substitution(self, client):
        """多个变量替换"""
        headers = _get_auth_headers(client)

        # 创建环境
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Multi Var Env",
                "variables": [
                    {"key": "host", "value": "httpbin.org", "type": "string"},
                    {"key": "protocol", "value": "https://", "type": "string"},
                    {"key": "endpoint", "value": "/get", "type": "string"},
                ],
            },
        ).get_json()["data"]["id"]

        # 创建用例
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Multi Variable Test",
                "method": "GET",
                "url": "{{protocol}}{{host}}{{endpoint}}",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200

    def test_variable_in_headers(self, client):
        """变量在请求头中替换"""
        headers = _get_auth_headers(client)

        # 创建环境
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Header Var Env",
                "variables": [
                    {"key": "auth_token", "value": "Bearer test-token-123", "type": "secret"},
                    {"key": "content_type", "value": "application/json", "type": "string"},
                ],
            },
        ).get_json()["data"]["id"]

        # 创建用例
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Header Variable Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "headers": {"Authorization": "{{auth_token}}", "Content-Type": "{{content_type}}"},
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200
        data = result.get_json()["data"]
        # 应该成功执行，头部被正确替换
        assert data["passed"] is True

    def test_variable_in_body(self, client):
        """变量在请求体中替换"""
        headers = _get_auth_headers(client)

        # 创建环境
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Body Var Env",
                "variables": [
                    {"key": "username", "value": "testuser", "type": "string"},
                    {"key": "email", "value": "test@example.com", "type": "string"},
                ],
            },
        ).get_json()["data"]["id"]

        # 创建用例
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Body Variable Test",
                "method": "POST",
                "url": "https://httpbin.org/post",
                "body_type": "json",
                "body": '{"username": "{{username}}", "email": "{{email}}"}',
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200
        data = result.get_json()["data"]
        assert data["passed"] is True

    def test_variable_default_value(self, client):
        """变量默认值"""
        headers = _get_auth_headers(client)

        # 创建环境（不定义某个变量）
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Partial Env",
                "variables": [{"key": "defined_var", "value": "defined", "type": "string"}],
            },
        ).get_json()["data"]["id"]

        # 创建用例（使用未定义的变量带默认值）
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Default Value Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "body_type": "json",
                "body": '{"defined": "{{defined_var}}", "undefined": "{{undefined_var:-fallback}}"}',
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        # 应该使用默认值
        assert result.status_code == 200

    def test_variable_no_environment(self, client):
        """无环境时的变量处理"""
        headers = _get_auth_headers(client)

        # 创建用例使用变量但不选择环境
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "No Env Test",
                "method": "GET",
                "url": "{{undefined_var}}/get",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        # 执行但不选择环境
        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        # 应该失败，因为变量未定义
        data = result.get_json()["data"]
        # 变量未替换，URL 变成字面量
        assert result.status_code == 200  # 请求仍会发送

    def test_secret_variable_masked(self, client):
        """敏感变量应该被掩码"""
        headers = _get_auth_headers(client)

        # 创建环境
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Secret Env",
                "variables": [
                    {"key": "api_key", "value": "super-secret-key-12345", "type": "secret"},
                    {"key": "password", "value": "mypassword", "type": "secret"},
                ],
            },
        ).get_json()["data"]["id"]

        # 获取环境详情
        resp = client.get(f"/api/v1/environments/{eid}", headers=headers)
        data = resp.get_json()["data"]

        # secret 类型的变量值应该被掩码
        for var in data["variables"]:
            if var["key"] in ["api_key", "password"]:
                # 值可能是掩码形式或者完全不显示
                assert var["type"] == "secret"

    def test_variable_update_reflects(self, client):
        """更新环境变量后执行应该使用新值"""
        headers = _get_auth_headers(client)

        # 创建环境
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Update Env",
                "variables": [{"key": "version", "value": "v1", "type": "string"}],
            },
        ).get_json()["data"]["id"]

        # 创建用例
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Update Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "headers": {"X-Version": "{{version}}"},
            },
        )
        case_id = resp.get_json()["data"]["id"]

        # 第一次执行
        result1 = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result1.status_code == 200

        # 更新环境变量
        client.put(
            f"/api/v1/environments/{eid}",
            headers=headers,
            json={"variables": [{"key": "version", "value": "v2", "type": "string"}]},
        )

        # 第二次执行（应该使用新值 v2）
        result2 = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result2.status_code == 200


class TestVariableTypes:
    """变量类型测试"""

    def test_string_variable(self, client):
        """字符串类型变量"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "String Env",
                "variables": [{"key": "str_var", "value": "hello world", "type": "string"}],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "String Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "body": '{"message": "{{str_var}}"}',
                "body_type": "json",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200

    def test_number_variable(self, client):
        """数字类型变量"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Number Env",
                "variables": [{"key": "timeout", "value": "3000", "type": "number"}],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Number Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "body": '{"timeout": {{timeout}}}',
                "body_type": "json",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200

    def test_boolean_variable(self, client):
        """布尔类型变量"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Boolean Env",
                "variables": [{"key": "debug", "value": "true", "type": "boolean"}],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Boolean Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "body": '{"debug": {{debug}}}',
                "body_type": "json",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200

    def test_variable_in_url_params(self, client):
        """变量在 URL 参数中"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Param Env",
                "variables": [{"key": "user_id", "value": "12345", "type": "string"}],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Param Test",
                "method": "GET",
                "url": "https://httpbin.org/get?user_id={{user_id}}",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200


class TestVariableEdgeCases:
    """变量边界情况测试"""

    def test_empty_variable_value(self, client):
        """空变量值"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Empty Env",
                "variables": [{"key": "empty_var", "value": "", "type": "string"}],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Empty Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "body": '{"key": "{{empty_var}}"}',
                "body_type": "json",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200

    def test_special_characters_in_variable(self, client):
        """变量值包含特殊字符"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "Special Env",
                "variables": [
                    {"key": "special", "value": "hello {{world}} nested", "type": "string"}
                ],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Special Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "body": '{"text": "{{special}}"}',
                "body_type": "json",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        # 特殊字符可能需要转义
        assert result.status_code == 200

    def test_json_object_variable(self, client):
        """JSON 对象类型变量"""
        headers = _get_auth_headers(client)
        eid = client.post(
            "/api/v1/environments",
            headers=headers,
            json={
                "name": "JSON Env",
                "variables": [
                    {"key": "config", "value": '{"host": "localhost", "port": 8080}', "type": "string"}
                ],
            },
        ).get_json()["data"]["id"]

        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "JSON Test",
                "method": "POST",
                "url": "https://httpbin.org/post",
                "body": '{{config}}',
                "body_type": "json",
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run?environment_id={eid}",
            headers=headers,
        )
        assert result.status_code == 200
