"""
APP Testing 模块 API 集成测试

测试用例集 CRUD、脚本 CRUD、设备配置、执行功能
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
    data = resp.get_json()
    token = data["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestAppTestHealth:
    """健康检查测试"""

    def test_health_returns_ok(self, client):
        """健康检查接口正常返回"""
        resp = client.get("/api/v1/app-test/health")
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["code"] == 200
        assert data["data"]["status"] == "ok"


class TestAppCollectionCRUD:
    """用例集 CRUD 测试"""

    def test_create_collection(self, client):
        """创建用例集"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "APP Tests"},
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["code"] == 201
        assert data["data"]["name"] == "APP Tests"
        assert "id" in data["data"]

    def test_create_collection_with_description(self, client):
        """创建带描述的用例集"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "Test Collection", "description": "Test description"},
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["data"]["description"] == "Test description"

    def test_create_collection_without_name(self, client):
        """创建用例集缺少名称字段"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"description": "No name"},
        )
        assert resp.status_code == 400

    def test_get_collections(self, client):
        """获取用例集列表"""
        headers = _get_auth_headers(client)
        # 创建两个用例集
        client.post(
            "/api/v1/app-test/collections", headers=headers, json={"name": "Collection A"}
        )
        client.post(
            "/api/v1/app-test/collections", headers=headers, json={"name": "Collection B"}
        )

        resp = client.get("/api/v1/app-test/collections", headers=headers)
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["code"] == 200
        # 至少有刚创建的两个
        names = [c["name"] for c in data["data"]]
        assert "Collection A" in names
        assert "Collection B" in names

    def test_get_collections_filter_by_project(self, client):
        """按项目筛选用例集"""
        headers = _get_auth_headers(client)

        # 创建项目
        resp = client.post(
            "/api/v1/projects", headers=headers, json={"name": "Test Project"}
        )
        project_id = resp.get_json()["data"]["id"]

        # 在项目中创建用例集
        client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "In Project", "project_id": project_id},
        )
        # 创建不在项目中的用例集
        client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "No Project"},
        )

        resp = client.get(
            f"/api/v1/app-test/collections?project_id={project_id}",
            headers=headers,
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        names = [c["name"] for c in data["data"]]
        assert "In Project" in names
        assert "No Project" not in names

    def test_update_collection(self, client):
        """更新用例集"""
        headers = _get_auth_headers(client)
        cid = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "Old Name"},
        ).get_json()["data"]["id"]

        resp = client.put(
            f"/api/v1/app-test/collections/{cid}",
            headers=headers,
            json={"name": "New Name", "description": "New desc"},
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["data"]["name"] == "New Name"
        assert data["data"]["description"] == "New desc"

    def test_update_collection_not_found(self, client):
        """更新不存在的用例集"""
        headers = _get_auth_headers(client)
        resp = client.put(
            "/api/v1/app-test/collections/99999",
            headers=headers,
            json={"name": "Test"},
        )
        assert resp.status_code == 404

    def test_delete_collection(self, client):
        """删除用例集"""
        headers = _get_auth_headers(client)
        cid = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "To Delete"},
        ).get_json()["data"]["id"]

        resp = client.delete(f"/api/v1/app-test/collections/{cid}", headers=headers)
        assert resp.status_code in [200, 201]

        # 确认删除
        resp = client.get(
            "/api/v1/app-test/collections",
            headers=headers,
        )
        names = [c["name"] for c in resp.get_json()["data"]]
        assert "To Delete" not in names

    def test_delete_collection_not_found(self, client):
        """删除不存在的用例集"""
        headers = _get_auth_headers(client)
        resp = client.delete("/api/v1/app-test/collections/99999", headers=headers)
        assert resp.status_code == 404

    def test_user_isolation(self, client):
        """用户间数据隔离"""
        headers1 = _get_auth_headers(client)
        headers2 = _get_auth_headers(client)

        # 用户1创建用例集
        client.post(
            "/api/v1/app-test/collections",
            headers=headers1,
            json={"name": "User1 Collection"},
        )

        # 用户2获取列表（应该看不到用户1的）
        resp = client.get("/api/v1/app-test/collections", headers=headers2)
        names = [c["name"] for c in resp.get_json()["data"]]
        assert "User1 Collection" not in names


class TestAppScriptCRUD:
    """脚本 CRUD 测试"""

    def test_create_script_android(self, client):
        """创建 Android 脚本"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={
                "name": "Android Test",
                "platform": "android",
                "app_package": "com.example.app",
                "app_activity": ".MainActivity",
            },
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["data"]["name"] == "Android Test"
        assert data["data"]["platform"] == "android"
        assert data["data"]["app_package"] == "com.example.app"

    def test_create_script_ios(self, client):
        """创建 iOS 脚本"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={
                "name": "iOS Test",
                "platform": "ios",
                "bundle_id": "com.example.app",
                "device_name": "iPhone 15",
            },
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["data"]["platform"] == "ios"
        assert data["data"]["bundle_id"] == "com.example.app"

    def test_create_script_with_defaults(self, client):
        """创建脚本使用默认值"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Minimal Script"},
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        # 默认平台是 android
        assert data["data"]["platform"] == "android"
        # 默认 automation_name
        assert data["data"]["automation_name"] == "UiAutomator2"
        # 默认 appium_server
        assert data["data"]["appium_server"] == "http://localhost:4723"

    def test_create_script_with_collection(self, client):
        """创建脚本并关联用例集"""
        headers = _get_auth_headers(client)

        # 先创建用例集
        cid = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "Test Collection"},
        ).get_json()["data"]["id"]

        # 创建脚本并关联
        resp = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "In Collection", "collection_id": cid},
        )
        assert resp.status_code in [200, 201]
        assert resp.get_json()["data"]["collection_id"] == cid

    def test_create_script_with_full_config(self, client):
        """创建完整配置的脚本"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={
                "name": "Full Config Script",
                "platform": "android",
                "app_path": "/path/to/app.apk",
                "app_package": "com.example.app",
                "app_activity": ".MainActivity",
                "device_name": "Pixel 5",
                "platform_version": "12.0",
                "automation_name": "UiAutomator2",
                "appium_server": "http://192.168.1.100:4723",
                "script_content": "from appium import webdriver\n\ncaps = {}\ndriver = webdriver.Remote('http://localhost:4723', caps)\n",
            },
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()["data"]
        assert data["app_path"] == "/path/to/app.apk"
        assert data["device_name"] == "Pixel 5"
        assert data["platform_version"] == "12.0"

    def test_create_script_without_name(self, client):
        """创建脚本缺少名称"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"platform": "android"},
        )
        assert resp.status_code == 400

    def test_get_scripts(self, client):
        """获取脚本列表"""
        headers = _get_auth_headers(client)
        client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Script A"},
        )
        client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Script B"},
        )

        resp = client.get("/api/v1/app-test/scripts", headers=headers)
        assert resp.status_code in [200, 201]
        names = [s["name"] for s in resp.get_json()["data"]]
        assert "Script A" in names
        assert "Script B" in names

    def test_get_scripts_filter_by_collection(self, client):
        """按用例集筛选脚本"""
        headers = _get_auth_headers(client)

        cid = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "Collection"},
        ).get_json()["data"]["id"]

        client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "In Collection", "collection_id": cid},
        )
        client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "No Collection"},
        )

        resp = client.get(
            f"/api/v1/app-test/scripts?collection_id={cid}",
            headers=headers,
        )
        names = [s["name"] for s in resp.get_json()["data"]]
        assert "In Collection" in names
        assert "No Collection" not in names

    def test_get_script_detail(self, client):
        """获取脚本详情"""
        headers = _get_auth_headers(client)
        sid = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Detail Test"},
        ).get_json()["data"]["id"]

        resp = client.get(f"/api/v1/app-test/scripts/{sid}", headers=headers)
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["data"]["name"] == "Detail Test"
        assert "script_content" in data["data"]

    def test_get_script_not_found(self, client):
        """获取不存在的脚本"""
        headers = _get_auth_headers(client)
        resp = client.get("/api/v1/app-test/scripts/99999", headers=headers)
        assert resp.status_code == 404

    def test_update_script(self, client):
        """更新脚本"""
        headers = _get_auth_headers(client)
        sid = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Old Name"},
        ).get_json()["data"]["id"]

        resp = client.put(
            f"/api/v1/app-test/scripts/{sid}",
            headers=headers,
            json={
                "name": "New Name",
                "device_name": "Updated Device",
                "platform_version": "13.0",
            },
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()["data"]
        assert data["name"] == "New Name"
        assert data["device_name"] == "Updated Device"
        assert data["platform_version"] == "13.0"

    def test_update_script_not_found(self, client):
        """更新不存在的脚本"""
        headers = _get_auth_headers(client)
        resp = client.put(
            "/api/v1/app-test/scripts/99999",
            headers=headers,
            json={"name": "Test"},
        )
        assert resp.status_code == 404

    def test_delete_script(self, client):
        """删除脚本"""
        headers = _get_auth_headers(client)
        sid = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "To Delete"},
        ).get_json()["data"]["id"]

        resp = client.delete(f"/api/v1/app-test/scripts/{sid}", headers=headers)
        assert resp.status_code in [200, 201]

        # 确认删除
        resp = client.get("/api/v1/app-test/scripts", headers=headers)
        names = [s["name"] for s in resp.get_json()["data"]]
        assert "To Delete" not in names

    def test_delete_script_not_found(self, client):
        """删除不存在的脚本"""
        headers = _get_auth_headers(client)
        resp = client.delete("/api/v1/app-test/scripts/99999", headers=headers)
        assert resp.status_code == 404

    def test_script_user_isolation(self, client):
        """脚本用户隔离"""
        headers1 = _get_auth_headers(client)
        headers2 = _get_auth_headers(client)

        client.post(
            "/api/v1/app-test/scripts",
            headers=headers1,
            json={"name": "User1 Script"},
        )

        resp = client.get("/api/v1/app-test/scripts", headers=headers2)
        names = [s["name"] for s in resp.get_json()["data"]]
        assert "User1 Script" not in names

    def test_collection_delete_cascades_to_scripts(self, client):
        """删除用例集时级联删除关联脚本"""
        headers = _get_auth_headers(client)

        cid = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "Parent Collection"},
        ).get_json()["data"]["id"]

        client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Child Script", "collection_id": cid},
        )

        # 删除用例集
        client.delete(f"/api/v1/app-test/collections/{cid}", headers=headers)

        # 脚本应该也被删除
        resp = client.get("/api/v1/app-test/scripts", headers=headers)
        names = [s["name"] for s in resp.get_json()["data"]]
        assert "Child Script" not in names


class TestAppScriptExecution:
    """脚本执行测试"""

    def test_run_script_empty_content(self, client):
        """执行空脚本内容（应返回成功但无输出）"""
        headers = _get_auth_headers(client)
        sid = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Empty Script"},
        ).get_json()["data"]["id"]

        resp = client.post(
            f"/api/v1/app-test/scripts/{sid}/run",
            headers=headers,
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["code"] == 200
        # 空脚本执行可能成功（返回码0）或失败
        assert data["data"]["status"] in ["passed", "failed", "running"]

    def test_run_script_not_found(self, client):
        """执行不存在的脚本"""
        headers = _get_auth_headers(client)
        resp = client.post(
            "/api/v1/app-test/scripts/99999/run",
            headers=headers,
        )
        assert resp.status_code == 404

    def test_run_script_no_auth(self, client):
        """未认证执行脚本"""
        resp = client.post("/api/v1/app-test/scripts/1/run")
        assert resp.status_code == 401

    def test_script_execution_updates_status(self, client):
        """脚本执行后更新状态"""
        headers = _get_auth_headers(client)
        sid = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={"name": "Status Test"},
        ).get_json()["data"]["id"]

        # 执行脚本
        client.post(f"/api/v1/app-test/scripts/{sid}/run", headers=headers)

        # 获取脚本详情
        resp = client.get(f"/api/v1/app-test/scripts/{sid}", headers=headers)
        data = resp.get_json()["data"]
        # 状态应该已更新
        assert data["status"] in ["passed", "failed", "running"]
        # 应该有时间戳
        assert data["last_run_at"] is not None


class TestAppDevices:
    """设备管理测试"""

    def test_get_devices_no_appium(self, client):
        """获取设备列表（Appium 未运行）"""
        headers = _get_auth_headers(client)
        resp = client.get("/api/v1/app-test/devices", headers=headers)
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["code"] == 200
        # 即使 Appium 未运行，也应返回空列表而非错误
        assert data["data"]["server_status"]["connected"] is False
        assert data["data"]["devices"] == []

    def test_get_devices_with_custom_server(self, client):
        """获取自定义 Appium Server 的设备列表"""
        headers = _get_auth_headers(client)
        resp = client.get(
            "/api/v1/app-test/devices?server_url=http://localhost:9999",
            headers=headers,
        )
        assert resp.status_code in [200, 201]
        data = resp.get_json()
        assert data["data"]["server_status"]["url"] == "http://localhost:9999"

    def test_get_devices_no_auth(self, client):
        """未认证获取设备列表"""
        resp = client.get("/api/v1/app-test/devices")
        assert resp.status_code == 401


class TestAppTestIntegration:
    """集成测试"""

    def test_full_workflow(self, client):
        """完整的 APP 测试工作流"""
        headers = _get_auth_headers(client)

        # 1. 创建用例集
        cid = client.post(
            "/api/v1/app-test/collections",
            headers=headers,
            json={"name": "My Tests", "description": "Integration test collection"},
        ).get_json()["data"]["id"]

        # 2. 创建脚本
        sid = client.post(
            "/api/v1/app-test/scripts",
            headers=headers,
            json={
                "name": "My Android Test",
                "collection_id": cid,
                "platform": "android",
                "app_package": "com.example.app",
                "script_content": "print('Hello from App Test')",
            },
        ).get_json()["data"]["id"]

        # 3. 验证脚本在用例集中
        resp = client.get(
            f"/api/v1/app-test/scripts?collection_id={cid}",
            headers=headers,
        )
        assert len(resp.get_json()["data"]) == 1
        assert resp.get_json()["data"][0]["name"] == "My Android Test"

        # 4. 更新脚本
        client.put(
            f"/api/v1/app-test/scripts/{sid}",
            headers=headers,
            json={"description": "Updated description"},
        )

        # 5. 执行脚本
        resp = client.post(
            f"/api/v1/app-test/scripts/{sid}/run",
            headers=headers,
        )
        assert resp.status_code in [200, 201]

        # 6. 清理 - 删除用例集
        client.delete(f"/api/v1/app-test/collections/{cid}", headers=headers)

        # 7. 确认脚本也被删除
        resp = client.get("/api/v1/app-test/scripts", headers=headers)
        names = [s["name"] for s in resp.get_json()["data"]]
        assert "My Android Test" not in names
