"""FastAPI v2 接口测试执行模块测试"""

import uuid
import pytest
from fastapi.testclient import TestClient
from app.fastapi_app import create_fastapi_app


@pytest.fixture()
def v2_client(app):
    """Create FastAPI test client that shares the same DB as Flask"""
    fastapi_app = create_fastapi_app("testing")
    with app.app_context():
        from app.extensions import db as flask_db
        flask_db.create_all()
        client = TestClient(fastapi_app)
        client.flask_app = app
        yield client


def _register_and_login_v2(client, username=None, password="Str0ng!Pass"):
    """辅助函数：通过 v2 注册并登录"""
    if username is None:
        username = f"v2api_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    client.post(
        "/api/v2/auth/register",
        json={"username": username, "email": email, "password": password},
    )

    login_resp = client.post(
        "/api/v2/auth/login",
        json={"username": username, "password": password},
    )
    data = login_resp.json()
    return {
        "username": username,
        "access_token": data["access_token"],
        "user_id": data.get("user_id", 1),
    }


def _create_collection_v2(client, user_id, name=None):
    """辅助函数：直接在数据库创建集合"""
    from app.extensions import db
    from app.models.api_test_case import ApiTestCollection

    with client.flask_app.app_context():
        collection = ApiTestCollection(
            name=name or f"Coll_{uuid.uuid4().hex[:8]}",
            description="Test collection",
            user_id=user_id,
        )
        db.session.add(collection)
        db.session.commit()
        return {"id": collection.id, "name": collection.name}


def _create_case_v2(client, user_id, collection_id=None, name=None):
    """辅助函数：直接在数据库创建用例"""
    from app.extensions import db
    from app.models.api_test_case import ApiTestCase

    with client.flask_app.app_context():
        case = ApiTestCase(
            name=name or f"Case_{uuid.uuid4().hex[:8]}",
            method="GET",
            url="https://httpbin.org/get",
            description="Test case",
            collection_id=collection_id,
            user_id=user_id,
        )
        db.session.add(case)
        db.session.commit()
        return {"id": case.id, "name": case.name}


class TestV2ExecuteRequest:
    """v2 快速执行请求测试"""

    def test_execute_request_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.post(
            "/api/v2/api-tests/execute",
            json={"method": "GET", "url": "https://httpbin.org/get"},
        )
        assert resp.status_code in (401, 403)

    def test_execute_mock_request(self, v2_client):
        """Mock 模式应返回预设响应"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/api-tests/execute",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={
                "method": "GET",
                "url": "https://example.com",
                "mock_enabled": True,
                "mock_response_code": 200,
                "mock_response_body": '{"mocked": true}',
                "mock_response_headers": {"X-Mock": "yes"},
                "mock_delay_ms": 0,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["is_mock"] is True
        assert data["status_code"] == 200

    def test_execute_mock_with_delay(self, v2_client):
        """Mock 模式支持延迟"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/api-tests/execute",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={
                "method": "GET",
                "url": "https://example.com",
                "mock_enabled": True,
                "mock_response_code": 201,
                "mock_response_body": "{}",
                "mock_delay_ms": 10,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["status_code"] == 201

    def test_execute_missing_method(self, v2_client):
        """缺少 method 字段应返回 422"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/api-tests/execute",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"url": "https://example.com"},
        )
        assert resp.status_code == 422


class TestV2RunCase:
    """v2 单用例执行测试"""

    def test_run_case_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.post("/api/v2/api-tests/cases/1/run")
        assert resp.status_code in (401, 403)

    def test_run_case_not_found(self, v2_client):
        """不存在的用例应返回 404"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/api-tests/cases/99999/run",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404

    def test_run_case_mock(self, v2_client):
        """Mock 用例应直接返回 Mock 数据"""
        from app.extensions import db as flask_db
        from app.models.api_test_case import ApiTestCase as ATC
        import flask_jwt_extended

        user = _register_and_login_v2(v2_client)

        # Decode token to get actual user_id
        decoded = flask_jwt_extended.decode_token(user["access_token"])
        actual_user_id = int(decoded["sub"])

        with v2_client.flask_app.app_context():
            case = ATC(
                name="MockCase",
                method="GET",
                url="https://httpbin.org/get",
                user_id=actual_user_id,
                mock_enabled=True,
                mock_response_code=201,
                mock_response_body='{"mocked": true}',
            )
            flask_db.session.add(case)
            flask_db.session.commit()
            case_id = case.id

        resp = v2_client.post(
            f"/api/v2/api-tests/cases/{case_id}/run",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["is_mock"] is True
        assert data["passed"] is True


class TestV2RunCollection:
    """v2 集合批量执行测试"""

    def test_run_collection_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.post("/api/v2/api-tests/collections/1/run")
        assert resp.status_code in (401, 403)

    def test_run_collection_not_found(self, v2_client):
        """不存在的集合应返回 404"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/api-tests/collections/99999/run",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404

    def test_run_collection_empty(self, v2_client):
        """空集合应返回 400"""
        from app.extensions import db as flask_db
        from app.models.api_test_case import ApiTestCollection
        import flask_jwt_extended

        user = _register_and_login_v2(v2_client)

        decoded = flask_jwt_extended.decode_token(user["access_token"])
        actual_user_id = int(decoded["sub"])

        with v2_client.flask_app.app_context():
            collection = ApiTestCollection(
                name="Empty_Coll",
                user_id=actual_user_id,
            )
            flask_db.session.add(collection)
            flask_db.session.commit()
            coll_id = collection.id

        resp = v2_client.post(
            f"/api/v2/api-tests/collections/{coll_id}/run",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={},
        )
        assert resp.status_code == 400


class TestV2GetResults:
    """v2 测试结果查询测试"""

    def test_get_results_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.get("/api/v2/api-tests/results/1")
        assert resp.status_code in (401, 403)

    def test_get_results_not_found(self, v2_client):
        """不存在的结果应返回 404"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.get(
            "/api/v2/api-tests/results/99999",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404
