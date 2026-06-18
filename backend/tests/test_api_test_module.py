"""
API 测试模块测试

覆盖：集合 CRUD、用例 CRUD、Mock 功能
"""

import uuid


def _register_and_login(client, username=None, password="Str0ng!Pass"):
    """辅助函数：注册并登录"""
    if username is None:
        username = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    data = login_resp.get_json()["data"]
    return {
        "username": username,
        "access_token": data["access_token"],
    }


def _create_collection(client, token, name=None):
    """辅助函数：创建集合"""
    if name is None:
        name = f"Collection_{uuid.uuid4().hex[:8]}"

    resp = client.post(
        "/api/v1/api-test/collections",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name, "description": "Test collection"},
    )
    return resp.get_json()["data"]


def _create_case(client, token, collection_id=None, name=None):
    """辅助函数：创建用例"""
    if name is None:
        name = f"Case_{uuid.uuid4().hex[:8]}"

    payload = {
        "name": name,
        "method": "GET",
        "url": "https://httpbin.org/get",
        "description": "Test case",
    }
    if collection_id:
        payload["collection_id"] = collection_id

    resp = client.post(
        "/api/v1/api-test/cases",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    return resp.get_json()["data"]


class TestCollectionCRUD:
    """集合 CRUD 测试"""

    def test_create_collection(self, client):
        """创建集合"""
        user = _register_and_login(client)
        collection = _create_collection(client, user["access_token"])

        assert collection["id"] is not None
        assert collection["name"].startswith("Collection_")

    def test_get_collections(self, client):
        """获取集合列表"""
        user = _register_and_login(client)
        _create_collection(client, user["access_token"])
        _create_collection(client, user["access_token"])

        resp = client.get(
            "/api/v1/api-test/collections",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) >= 2

    def test_update_collection(self, client):
        """更新集合"""
        user = _register_and_login(client)
        collection = _create_collection(client, user["access_token"])

        resp = client.put(
            f"/api/v1/api-test/collections/{collection['id']}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"name": "Updated Name", "description": "Updated desc"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["data"]["name"] == "Updated Name"

    def test_delete_collection(self, client):
        """删除集合"""
        user = _register_and_login(client)
        collection = _create_collection(client, user["access_token"])

        resp = client.delete(
            f"/api/v1/api-test/collections/{collection['id']}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200

        # 验证已删除
        resp = client.get(
            "/api/v1/api-test/collections",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        ids = [c["id"] for c in resp.get_json()["data"]]
        assert collection["id"] not in ids

    def test_update_nonexistent_collection(self, client):
        """更新不存在的集合应该返回 404"""
        user = _register_and_login(client)

        resp = client.put(
            "/api/v1/api-test/collections/99999",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"name": "Test"},
        )
        assert resp.status_code == 404

    def test_delete_nonexistent_collection(self, client):
        """删除不存在的集合应该返回 404"""
        user = _register_and_login(client)

        resp = client.delete(
            "/api/v1/api-test/collections/99999",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404


class TestCaseCRUD:
    """用例 CRUD 测试"""

    def test_create_case(self, client):
        """创建用例"""
        user = _register_and_login(client)
        case = _create_case(client, user["access_token"])

        assert case["id"] is not None
        assert case["method"] == "GET"
        assert case["url"] == "https://httpbin.org/get"

    def test_create_case_in_collection(self, client):
        """在集合中创建用例"""
        user = _register_and_login(client)
        collection = _create_collection(client, user["access_token"])
        case = _create_case(client, user["access_token"], collection["id"])

        assert case["collection_id"] == collection["id"]

    def test_get_cases(self, client):
        """获取用例列表"""
        user = _register_and_login(client)
        _create_case(client, user["access_token"])
        _create_case(client, user["access_token"])

        resp = client.get(
            "/api/v1/api-test/cases",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) >= 2

    def test_get_case_detail(self, client):
        """获取用例详情"""
        user = _register_and_login(client)
        case = _create_case(client, user["access_token"])

        resp = client.get(
            f"/api/v1/api-test/cases/{case['id']}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["data"]["id"] == case["id"]

    def test_update_case(self, client):
        """更新用例"""
        user = _register_and_login(client)
        case = _create_case(client, user["access_token"])

        resp = client.put(
            f"/api/v1/api-test/cases/{case['id']}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={
                "name": "Updated Case",
                "method": "POST",
                "url": "https://httpbin.org/post",
                "body": {"key": "value"},
            },
        )
        assert resp.status_code == 200
        updated = resp.get_json()["data"]
        assert updated["name"] == "Updated Case"
        assert updated["method"] == "POST"

    def test_delete_case(self, client):
        """删除用例"""
        user = _register_and_login(client)
        case = _create_case(client, user["access_token"])

        resp = client.delete(
            f"/api/v1/api-test/cases/{case['id']}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200

    def test_get_nonexistent_case(self, client):
        """获取不存在的用例应该返回 404"""
        user = _register_and_login(client)

        resp = client.get(
            "/api/v1/api-test/cases/99999",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404

    def test_create_case_missing_fields(self, client):
        """缺少必需字段应该失败"""
        user = _register_and_login(client)

        resp = client.post(
            "/api/v1/api-test/cases",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"name": "Test"},  # 缺少 method 和 url
        )
        assert resp.status_code in [400, 422]


class TestMockServer:
    """Mock Server 测试"""

    def test_mock_endpoint_enabled(self, client):
        """启用 Mock 的用例应该返回预设响应"""
        user = _register_and_login(client)

        # 创建用例
        case = _create_case(client, user["access_token"])

        # 启用 Mock
        client.put(
            f"/api/v1/api-test/cases/{case['id']}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={
                "mock_enabled": True,
                "mock_response_code": 201,
                "mock_response_body": '{"mock": true}',
                "mock_response_headers": {"X-Custom": "test"},
            },
        )

        # 访问 Mock 端点
        resp = client.get(f"/api/v1/api-test/mock/{case['id']}")
        assert resp.status_code == 201
        assert resp.get_data(as_text=True) == '{"mock": true}'
        assert resp.headers.get("X-Custom") == "test"

    def test_mock_endpoint_disabled(self, client):
        """未启用 Mock 的用例应该返回 400"""
        user = _register_and_login(client)
        case = _create_case(client, user["access_token"])

        resp = client.get(f"/api/v1/api-test/mock/{case['id']}")
        assert resp.status_code == 400

    def test_mock_endpoint_nonexistent(self, client):
        """不存在的用例 Mock 应该返回 404"""
        resp = client.get("/api/v1/api-test/mock/99999")
        assert resp.status_code == 404


class TestCurlParser:
    """cURL 解析器测试"""

    def test_parse_simple_get(self):
        """解析简单 GET 请求"""
        from app.api.api_test import parse_curl
        result = parse_curl("curl https://example.com/api")
        assert result['method'] == 'GET'
        assert result['url'] == 'https://example.com/api'

    def test_parse_post_with_data(self):
        """解析 POST 请求带 data"""
        from app.api.api_test import parse_curl
        result = parse_curl('curl -X POST https://example.com/api -d \'{"key": "value"}\'')
        assert result['method'] == 'POST'
        assert result['url'] == 'https://example.com/api'
        assert result['body'] == '{"key": "value"}'

    def test_parse_multiline_curl(self):
        """解析多行 cURL（\\ 换行）"""
        from app.api.api_test import parse_curl
        curl_cmd = """curl -X POST \\
  https://example.com/api \\
  -H 'Content-Type: application/json' \\
  -d '{"name": "test"}'"""
        result = parse_curl(curl_cmd)
        assert result['method'] == 'POST'
        assert result['url'] == 'https://example.com/api'
        assert result['headers']['Content-Type'] == 'application/json'
        assert result['body'] == '{"name": "test"}'

    def test_parse_data_raw(self):
        """解析 --data-raw 参数"""
        from app.api.api_test import parse_curl
        result = parse_curl('curl https://example.com --data-raw "test=1&foo=2"')
        assert result['method'] == 'POST'
        assert result['body'] == 'test=1&foo=2'

    def test_parse_compressed_ignored(self):
        """--compressed 参数应被忽略"""
        from app.api.api_test import parse_curl
        result = parse_curl('curl --compressed https://example.com')
        assert result['url'] == 'https://example.com'

    def test_parse_empty_raises(self):
        """空命令应抛出 ValueError"""
        from app.api.api_test import parse_curl
        import pytest
        with pytest.raises(ValueError, match="为空"):
            parse_curl("")

    def test_parse_no_url_raises(self):
        """无 URL 应抛出 ValueError"""
        from app.api.api_test import parse_curl
        import pytest
        with pytest.raises(ValueError, match="未找到 URL"):
            parse_curl("curl -X GET")

    def test_import_curl_endpoint(self, client):
        """测试导入 cURL 端点"""
        user = _register_and_login(client)
        headers = {"Authorization": f"Bearer {user['access_token']}"}

        resp = client.post(
            "/api/v1/api-test/import-curl",
            json={"curl": 'curl -X POST https://example.com -H "Content-Type: application/json" -d \'{"a":1}\''},
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["method"] == "POST"
        assert data["url"] == "https://example.com"
        assert data["headers"]["Content-Type"] == "application/json"

    def test_import_curl_multiline_endpoint(self, client):
        """测试导入多行 cURL 端点"""
        user = _register_and_login(client)
        headers = {"Authorization": f"Bearer {user['access_token']}"}

        curl_cmd = """curl -X PUT \\
  https://api.example.com/users/1 \\
  -H 'Authorization: Bearer token123' \\
  -H 'Content-Type: application/json' \\
  -d '{"name": "updated"}'"""

        resp = client.post(
            "/api/v1/api-test/import-curl",
            json={"curl": curl_cmd},
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["method"] == "PUT"
        assert "users/1" in data["url"]
        assert data["headers"]["Authorization"] == "Bearer token123"


class TestHealthCheck:
    """健康检查测试"""

    def test_api_test_health(self, client):
        """API 测试模块健康检查"""
        resp = client.get("/api/v1/api-test/health")
        assert resp.status_code == 200
