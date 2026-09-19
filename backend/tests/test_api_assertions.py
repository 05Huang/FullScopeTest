"""
API Testing 断言验证测试

测试断言功能的正确性：状态码断言、JSON 路径断言、Header 断言、响应时间断言
"""

import uuid

import pytest

from tests.conftest import *  # noqa: F401, F403


def _get_auth_headers(client):
    """创建测试用户并返回认证头"""
    username = f"at_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    return {"Authorization": f"Bearer {resp.get_json()['data']['access_token']}"}


class TestStatusCodeAssertion:
    """状态码断言测试"""

    def test_assertion_status_code_equals_pass(self, client):
        """状态码等于断言通过"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Status Code Test",
                "method": "GET",
                "url": "https://httpbin.org/status/200",
                "assertions": [{"type": "status_code", "operator": "equals", "expected": 200}],
            },
        )
        assert resp.status_code == 200
        case_id = resp.get_json()["data"]["id"]

        # 执行用例
        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.status_code == 200
        data = result.get_json()["data"]
        assert data["passed"] is True

    def test_assertion_status_code_equals_fail(self, client):
        """状态码等于断言失败"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Status Code Fail Test",
                "method": "GET",
                "url": "https://httpbin.org/status/200",
                "assertions": [{"type": "status_code", "operator": "equals", "expected": 201}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        data = result.get_json()["data"]
        assert data["passed"] is False

    def test_assertion_status_code_contains(self, client):
        """状态码包含断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Status Code Contains",
                "method": "GET",
                "url": "https://httpbin.org/status/200",
                "assertions": [{"type": "status_code", "operator": "contains", "expected": "2"}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_status_code_range(self, client):
        """状态码范围断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Status Code Range",
                "method": "GET",
                "url": "https://httpbin.org/status/200",
                "assertions": [{"type": "status_code", "operator": "between", "expected": [200, 299]}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True


class TestJsonPathAssertion:
    """JSON 路径断言测试"""

    def test_assertion_json_path_simple(self, client):
        """简单 JSON 路径断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "JSON Path Test",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {
                        "type": "json_path",
                        "path": "$.slideshow.author",
                        "operator": "equals",
                        "expected": "Yours Truly",
                    }
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_json_path_nested(self, client):
        """嵌套 JSON 路径断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Nested JSON Path",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {
                        "type": "json_path",
                        "path": "$.slideshow.slides[0].title",
                        "operator": "equals",
                        "expected": "Wake up to WonderWidgets!",
                    }
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_json_path_contains(self, client):
        """JSON 路径包含断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "JSON Path Contains",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {
                        "type": "json_path",
                        "path": "$.slideshow.author",
                        "operator": "contains",
                        "expected": "Truly",
                    }
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_json_path_not_equals(self, client):
        """JSON 路径不等于断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "JSON Path Not Equals",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {
                        "type": "json_path",
                        "path": "$.slideshow.author",
                        "operator": "not_equals",
                        "expected": "Wrong Author",
                    }
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True


class TestHeaderAssertion:
    """响应头断言测试"""

    def test_assertion_header_exists(self, client):
        """响应头存在断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Header Exists",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "assertions": [{"type": "header", "path": "content-type", "operator": "exists"}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_header_contains(self, client):
        """响应头包含断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Header Contains",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "assertions": [
                    {"type": "header", "path": "content-type", "operator": "contains", "expected": "json"}
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True


class TestResponseTimeAssertion:
    """响应时间断言测试"""

    def test_assertion_response_time_less_than(self, client):
        """响应时间小于断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Response Time Test",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "assertions": [{"type": "response_time", "operator": "less_than", "expected": 10000}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_response_time_greater_than(self, client):
        """响应时间大于断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Response Time Greater",
                "method": "GET",
                "url": "https://httpbin.org/delay/1",
                "assertions": [{"type": "response_time", "operator": "greater_than", "expected": 500}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True


class TestBodyAssertion:
    """响应体断言测试"""

    def test_assertion_body_contains(self, client):
        """响应体包含断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Body Contains",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "assertions": [{"type": "body", "operator": "contains", "expected": "origin"}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_assertion_body_equals(self, client):
        """响应体等于断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Body Equals",
                "method": "POST",
                "url": "https://httpbin.org/anything",
                "body": '{"key": "value"}',
                "body_type": "json",
                "assertions": [{"type": "body", "operator": "contains", "expected": "value"}],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True


class TestMultipleAssertions:
    """多个断言组合测试"""

    def test_multiple_assertions_all_pass(self, client):
        """多个断言全部通过"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Multiple Assertions",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {"type": "status_code", "operator": "equals", "expected": 200},
                    {"type": "header", "path": "content-type", "operator": "contains", "expected": "json"},
                    {"type": "response_time", "operator": "less_than", "expected": 10000},
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        assert result.get_json()["data"]["passed"] is True

    def test_multiple_assertions_one_fails(self, client):
        """多个断言中一个失败"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Multiple Assertions One Fail",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {"type": "status_code", "operator": "equals", "expected": 200},
                    {"type": "status_code", "operator": "equals", "expected": 404},  # 会失败
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        data = result.get_json()["data"]
        assert data["passed"] is False
        # 应该有失败详情
        assert "assertion_results" in data


class TestAssertionWithVariables:
    """变量提取与断言结合测试"""

    def test_variable_extraction_and_assertion(self, client):
        """变量提取后在断言中使用"""
        headers = _get_auth_headers(client)

        # 创建用例集
        cid = client.post(
            "/api/v1/api-test/collections",
            headers=headers,
            json={"name": "Variable Test Collection"},
        ).get_json()["data"]["id"]

        # 创建第一个用例：提取变量
        client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Get Token",
                "method": "POST",
                "url": "https://httpbin.org/post",
                "body": '{"token": "test123"}',
                "body_type": "json",
                "extract_variables": [{"name": "extracted_token", "path": "$.json.token"}],
                "collection_id": cid,
            },
        )

        # 创建第二个用例：使用提取的变量
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Use Token",
                "method": "POST",
                "url": "https://httpbin.org/post",
                "body": '{"token": "{{extracted_token}}"}',
                "body_type": "json",
                "collection_id": cid,
            },
        )
        case_id = resp.get_json()["data"]["id"]

        # 执行用例
        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        # 应该能正确替换变量并执行
        assert result.status_code == 200


class TestAssertionEdgeCases:
    """断言边界情况测试"""

    def test_empty_assertions(self, client):
        """空断言列表（总是通过）"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "No Assertions",
                "method": "GET",
                "url": "https://httpbin.org/get",
                "assertions": [],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        # 无断言应该视为通过
        assert result.get_json()["data"]["passed"] is True

    def test_invalid_json_path(self, client):
        """无效的 JSON 路径"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Invalid JSON Path",
                "method": "GET",
                "url": "https://httpbin.org/json",
                "assertions": [
                    {"type": "json_path", "path": "$.nonexistent.path", "operator": "equals", "expected": "value"}
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        # 无效路径应该导致断言失败
        assert result.get_json()["data"]["passed"] is False

    def test_response_not_json(self, client):
        """响应不是 JSON 时的 JSON 路径断言"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/api-test/cases",
            headers=headers,
            json={
                "name": "Plain Text Response",
                "method": "GET",
                "url": "https://httpbin.org/robots.txt",
                "assertions": [
                    {"type": "json_path", "path": "$.key", "operator": "equals", "expected": "value"}
                ],
            },
        )
        case_id = resp.get_json()["data"]["id"]

        result = client.post(
            f"/api/v1/api-test/cases/{case_id}/run",
            headers=headers,
        )
        # 非 JSON 响应的 JSON 路径断言应该失败
        assert result.get_json()["data"]["passed"] is False
