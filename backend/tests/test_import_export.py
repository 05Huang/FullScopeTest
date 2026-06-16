"""
导入导出测试

覆盖：Postman JSON 导入、CSV 导入/导出、Excel 导出、模板生成、
     错误处理、去重逻辑
"""
import csv
import io
import json
import uuid


def _auth_headers(client, username=None):
    uid = uuid.uuid4().hex[:8]
    username = username or f"ie_{uid}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    token = resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_project(client, headers, name=None):
    name = name or f"Proj_{uuid.uuid4().hex[:8]}"
    resp = client.post("/api/v1/projects", headers=headers, json={"name": name})
    return resp.get_json()["data"]


# ══════════════════════════════════════════════════════════════════════════════
# 一、Postman JSON 导入测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPostmanImport:
    """Postman Collection JSON 导入测试"""

    SAMPLE_POSTMAN = {
        "info": {"name": "Test Collection"},
        "item": [
            {
                "name": "Get Users",
                "request": {
                    "method": "GET",
                    "url": {"raw": "https://api.example.com/users"},
                },
            },
            {
                "name": "Create User",
                "request": {
                    "method": "POST",
                    "url": {"raw": "https://api.example.com/users"},
                    "header": [
                        {"key": "Content-Type", "value": "application/json"},
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": '{"name": "test"}',
                    },
                },
            },
            {
                "name": "Folder",
                "item": [
                    {
                        "name": "Nested Request",
                        "request": {
                            "method": "GET",
                            "url": {"raw": "https://api.example.com/items"},
                        },
                    },
                ],
            },
        ],
    }

    def test_import_postman_success(self, client, no_rate_limit):
        """正常导入 Postman Collection"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        resp = client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "project_id": project["id"],
            "content": json.dumps(self.SAMPLE_POSTMAN),
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] == 3
        assert data["imported"] == 3
        assert data["skipped"] == 0

    def test_import_postman_dedup(self, client, no_rate_limit):
        """重复导入应跳过"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        content = json.dumps(self.SAMPLE_POSTMAN)
        client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "project_id": project["id"], "content": content,
        })
        # 第二次导入
        resp = client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "project_id": project["id"], "content": content,
        })
        data = resp.get_json()["data"]
        assert data["imported"] == 0
        assert data["skipped"] == 3

    def test_import_postman_invalid_json(self, client, no_rate_limit):
        """无效 JSON 应返回 400"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        resp = client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "project_id": project["id"], "content": "not-json",
        })
        assert resp.status_code == 400

    def test_import_postman_empty_items(self, client, no_rate_limit):
        """空 Collection 应返回 400"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        resp = client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "project_id": project["id"],
            "content": json.dumps({"item": []}),
        })
        assert resp.status_code == 400

    def test_import_postman_missing_project(self, client, no_rate_limit):
        """缺少 project_id 应返回 400"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "content": json.dumps(self.SAMPLE_POSTMAN),
        })
        assert resp.status_code == 400

    def test_import_postman_missing_content(self, client, no_rate_limit):
        """缺少 content 应返回 400"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        resp = client.post("/api/v1/api-test/import/postman", headers=headers, json={
            "project_id": project["id"],
        })
        assert resp.status_code == 400


# ══════════════════════════════════════════════════════════════════════════════
# 二、CSV 导入测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCSVImport:
    """CSV 导入测试"""

    SAMPLE_CSV = "name,method,url,headers,body,expected_status\n"
    SAMPLE_CSV += 'Login,POST,https://api.example.com/login,"{""Content-Type"": ""application/json""}","{""user"": ""test""}",200\n'
    SAMPLE_CSV += "Get Users,GET,https://api.example.com/users,,,\n"

    def test_import_csv_success(self, client, no_rate_limit):
        """正常导入 CSV"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        resp = client.post("/api/v1/api-test/import/csv", headers=headers, json={
            "project_id": project["id"],
            "content": self.SAMPLE_CSV,
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] == 2
        assert data["imported"] == 2

    def test_import_csv_dedup(self, client, no_rate_limit):
        """重复 CSV 导入应跳过"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        client.post("/api/v1/api-test/import/csv", headers=headers, json={
            "project_id": project["id"], "content": self.SAMPLE_CSV,
        })
        resp = client.post("/api/v1/api-test/import/csv", headers=headers, json={
            "project_id": project["id"], "content": self.SAMPLE_CSV,
        })
        data = resp.get_json()["data"]
        assert data["imported"] == 0
        assert data["skipped"] == 2

    def test_import_csv_empty_rows(self, client, no_rate_limit):
        """name/url 为空的行应跳过"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        csv_content = "name,method,url\n,GET,\nValid,GET,https://example.com\n"
        resp = client.post("/api/v1/api-test/import/csv", headers=headers, json={
            "project_id": project["id"], "content": csv_content,
        })
        data = resp.get_json()["data"]
        assert data["total"] == 2
        assert data["imported"] == 1
        assert data["skipped"] == 1

    def test_import_csv_missing_required_columns(self, client, no_rate_limit):
        """缺少必需列应返回 400"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        csv_content = "title,endpoint\nTest,https://example.com\n"
        resp = client.post("/api/v1/api-test/import/csv", headers=headers, json={
            "project_id": project["id"], "content": csv_content,
        })
        assert resp.status_code == 400

    def test_import_csv_invalid_headers_json(self, client, no_rate_limit):
        """headers 列 JSON 格式错误应跳过"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        csv_content = "name,method,url,headers\nTest,GET,https://example.com,not-json\n"
        resp = client.post("/api/v1/api-test/import/csv", headers=headers, json={
            "project_id": project["id"], "content": csv_content,
        })
        data = resp.get_json()["data"]
        assert data["skipped"] == 1


# ══════════════════════════════════════════════════════════════════════════════
# 三、CSV 模板测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCSVTemplate:
    """CSV 模板测试"""

    def test_get_csv_template(self, client, no_rate_limit):
        """获取 CSV 模板"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/api-test/import/template", headers=headers)
        assert resp.status_code == 200
        template = resp.get_json()["data"]["template"]
        assert "name" in template
        assert "method" in template
        assert "url" in template


# ══════════════════════════════════════════════════════════════════════════════
# 四、Service 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestImportServiceUnit:
    """导入 Service 单元测试"""

    def test_import_postman_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.services.import_export_service import import_from_postman_json
        with app.app_context():
            user = User(username=f"ie_{uuid.uuid4().hex[:6]}", email="ie@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="IEProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()

            content = json.dumps({
                "item": [{
                    "name": "Test",
                    "request": {"method": "GET", "url": {"raw": "https://example.com"}},
                }]
            })
            result = import_from_postman_json(user.id, proj.id, content)
            assert result['imported'] == 1
            db.session.rollback()

    def test_import_csv_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.services.import_export_service import import_from_csv
        with app.app_context():
            user = User(username=f"ie_{uuid.uuid4().hex[:6]}", email="ie2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="IEProj2", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()

            csv_content = "name,method,url\nTest,GET,https://example.com\n"
            result = import_from_csv(user.id, proj.id, csv_content)
            assert result['imported'] == 1
            db.session.rollback()

    def test_generate_csv_template_service(self):
        from app.services.import_export_service import generate_csv_template
        template = generate_csv_template()
        assert 'name' in template
        assert 'method' in template
        assert 'https://' in template


class TestExportServiceUnit:
    """导出 Service 单元测试"""

    def test_export_csv_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.import_export_service import export_test_report_csv
        with app.app_context():
            user = User(username=f"ie_{uuid.uuid4().hex[:6]}", email="ie3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="IEProj3", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api', status='success',
                total_cases=5, passed=4, failed=1,
                results=[{'name': 'Test1', 'status': 'passed'}, {'name': 'Test2', 'status': 'failed'}],
            )
            db.session.add(run)
            db.session.flush()

            csv_content = export_test_report_csv(run.id)
            assert '执行 ID' in csv_content
            assert 'Test1' in csv_content
            assert 'Test2' in csv_content
            db.session.rollback()

    def test_export_excel_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.import_export_service import export_test_report_excel
        with app.app_context():
            user = User(username=f"ie_{uuid.uuid4().hex[:6]}", email="ie4@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="IEProj4", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api', status='success',
                total_cases=3, passed=3, failed=0,
            )
            db.session.add(run)
            db.session.flush()

            excel_bytes = export_test_report_excel(run.id)
            if excel_bytes is not None:
                # openpyxl 已安装
                assert len(excel_bytes) > 0
                assert b'PK' in excel_bytes[:4]  # Excel 是 ZIP 格式
            db.session.rollback()