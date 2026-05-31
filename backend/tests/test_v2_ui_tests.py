"""FastAPI v2 Web 自动化测试模块测试"""

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
        username = f"v2ui_{uuid.uuid4().hex[:8]}"
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


class TestV2RunWebTest:
    """v2 Web 测试触发测试"""

    def test_run_web_test_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.post(
            "/api/v2/ui-tests/run",
            json={"script_id": 1},
        )
        assert resp.status_code in (401, 403)

    def test_run_web_test_not_found(self, v2_client):
        """不存在的脚本应返回 404"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/ui-tests/run",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={"script_id": 99999},
        )
        assert resp.status_code == 404

    def test_run_web_test_missing_script_id(self, v2_client):
        """缺少 script_id 应返回 422"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.post(
            "/api/v2/ui-tests/run",
            headers={"Authorization": f"Bearer {user['access_token']}"},
            json={},
        )
        assert resp.status_code == 422


class TestV2GetWebTestResults:
    """v2 Web 测试结果查询测试"""

    def test_get_results_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.get("/api/v2/ui-tests/results/1")
        assert resp.status_code in (401, 403)

    def test_get_results_not_found(self, v2_client):
        """不存在的结果应返回 404"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.get(
            "/api/v2/ui-tests/results/99999",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404


class TestV2GetVisualDiffs:
    """v2 视觉差异查询测试"""

    def test_get_visual_diffs_unauthorized(self, v2_client):
        """未认证应返回 401/403"""
        resp = v2_client.get("/api/v2/ui-tests/visual-diffs/1")
        assert resp.status_code in (401, 403)

    def test_get_visual_diffs_not_found(self, v2_client):
        """不存在的运行应返回 404"""
        user = _register_and_login_v2(v2_client)
        resp = v2_client.get(
            "/api/v2/ui-tests/visual-diffs/99999",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 404

    def test_get_visual_diffs_empty(self, v2_client):
        """有权限但无数据时应返回空列表"""
        from app.extensions import db as flask_db
        from app.models.test_run import TestRun as TR
        import flask_jwt_extended

        user = _register_and_login_v2(v2_client)
        decoded = flask_jwt_extended.decode_token(user["access_token"])
        actual_user_id = int(decoded["sub"])

        with v2_client.flask_app.app_context():
            tr = TR(
                project_id=1,
                test_type="web",
                status="success",
                total_cases=1,
                passed=1,
                triggered_user_id=actual_user_id,
            )
            flask_db.session.add(tr)
            flask_db.session.commit()
            run_id = tr.id

        resp = v2_client.get(
            f"/api/v2/ui-tests/visual-diffs/{run_id}",
            headers={"Authorization": f"Bearer {user['access_token']}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 0
