"""
用例版本历史测试

覆盖：版本快照自动保存、版本列表查询、版本详情、
     diff 对比、最大版本数清理、边界条件
"""
import uuid


def _auth_headers(client, username=None):
    uid = uuid.uuid4().hex[:8]
    username = username or f"cv_{uid}"
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


def _create_case(client, headers, project_id, name=None, url=None):
    name = name or f"Case_{uuid.uuid4().hex[:8]}"
    url = url or "https://httpbin.org/get"
    resp = client.post("/api/v1/api-test/cases", headers=headers, json={
        "project_id": project_id,
        "name": name,
        "method": "GET",
        "url": url,
    })
    data = resp.get_json()
    if "data" not in data:
        raise RuntimeError(f"Create case failed: {data}")
    return data["data"]


# ══════════════════════════════════════════════════════════════════════════════
# 一、版本快照自动保存测试
# ══════════════════════════════════════════════════════════════════════════════

class TestVersionAutoSave:
    """更新用例时自动保存版本快照"""

    def test_update_creates_version(self, client, no_rate_limit):
        """更新用例后应自动创建版本快照"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        case = _create_case(client, headers, project["id"], name="Original")

        # 更新用例
        client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={
            "name": "Updated Name",
            "method": "POST",
        })

        # 查询版本历史
        resp = client.get(f"/api/v1/api-test/cases/{case['id']}/versions", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] >= 1
        # 版本快照保存的是更新前的内容
        assert data["items"][0]["content"]["name"] == "Original"

    def test_no_version_on_no_change(self, client, no_rate_limit):
        """没有实际变更时不创建版本"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        case = _create_case(client, headers, project["id"])

        # 用相同数据更新
        client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={
            "name": case["name"],
            "method": case["method"],
            "url": case["url"],
        })

        resp = client.get(f"/api/v1/api-test/cases/{case['id']}/versions", headers=headers)
        data = resp.get_json()["data"]
        # 没有变更时不应创建版本
        assert data["total"] == 0

    def test_multiple_updates_create_multiple_versions(self, client, no_rate_limit):
        """多次更新应创建多个版本"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        case = _create_case(client, headers, project["id"], name="V0")

        # 更新 3 次
        for i in range(1, 4):
            client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={
                "name": f"V{i}",
            })

        resp = client.get(f"/api/v1/api-test/cases/{case['id']}/versions", headers=headers)
        data = resp.get_json()["data"]
        assert data["total"] == 3

    def test_version_records_changed_fields(self, client, no_rate_limit):
        """版本应记录变更的字段列表"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        case = _create_case(client, headers, project["id"])

        client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={
            "name": "New Name",
            "url": "https://httpbin.org/post",
        })

        resp = client.get(f"/api/v1/api-test/cases/{case['id']}/versions", headers=headers)
        data = resp.get_json()["data"]
        assert data["total"] >= 1
        changed = data["items"][0]["changed_fields"]
        assert "name" in changed
        assert "url" in changed


# ══════════════════════════════════════════════════════════════════════════════
# 二、版本查询 API 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestVersionQuery:
    """版本查询 API 测试"""

    def test_get_version_detail(self, client, no_rate_limit):
        """获取指定版本详情"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        case = _create_case(client, headers, project["id"], name="Before")

        client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={"name": "After"})

        resp = client.get(f"/api/v1/api-test/cases/{case['id']}/versions", headers=headers)
        version_id = resp.get_json()["data"]["items"][0]["id"]

        resp = client.get(f"/api/v1/api-test/versions/{version_id}", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["content"]["name"] == "Before"

    def test_get_version_not_found(self, client, no_rate_limit):
        """获取不存在的版本应返回 404"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/api-test/versions/99999", headers=headers)
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 三、版本 diff 对比测试
# ══════════════════════════════════════════════════════════════════════════════

class TestVersionDiff:
    """版本 diff 对比测试"""

    def test_diff_two_versions(self, client, no_rate_limit):
        """对比两个版本的差异"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        case = _create_case(client, headers, project["id"], name="V1")

        # 第一次更新
        client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={"name": "V2"})
        # 第二次更新
        client.put(f"/api/v1/api-test/cases/{case['id']}", headers=headers, json={"method": "POST"})

        resp = client.get(f"/api/v1/api-test/cases/{case['id']}/versions", headers=headers)
        versions = resp.get_json()["data"]["items"]
        assert len(versions) == 2

        v1_id = versions[1]["id"]  # 旧版本
        v2_id = versions[0]["id"]  # 新版本

        resp = client.get(f"/api/v1/api-test/versions/diff?v1={v1_id}&v2={v2_id}", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert "diff" in data
        assert "name" in data["diff"]["changed_fields"] or "method" in data["diff"]["changed_fields"]

    def test_diff_missing_params(self, client, no_rate_limit):
        """缺少参数应返回 400"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/api-test/versions/diff", headers=headers)
        assert resp.status_code == 400

    def test_diff_version_not_found(self, client, no_rate_limit):
        """对比不存在的版本应返回 404"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/api-test/versions/diff?v1=99999&v2=99998", headers=headers)
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 四、Model 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestVersionModel:
    """TestCaseVersion Model 测试"""

    def test_to_dict(self):
        from app.models.test_case_version import TestCaseVersion
        v = TestCaseVersion(
            case_type='api', case_id=1, version=1,
            content={'name': 'Test'}, change_summary='修改了 name',
            changed_fields=['name'],
        )
        d = v.to_dict()
        assert d['case_type'] == 'api'
        assert d['version'] == 1
        assert d['content'] == {'name': 'Test'}
        assert 'name' in d['changed_fields']

    def test_diff_versions(self):
        from app.models.test_case_version import diff_versions
        old = {'name': 'Old', 'method': 'GET', 'url': 'https://a.com'}
        new = {'name': 'New', 'method': 'GET', 'url': 'https://b.com'}
        result = diff_versions(old, new)
        assert 'name' in result['changed_fields']
        assert 'url' in result['changed_fields']
        assert 'method' not in result['changed_fields']
        assert result['diffs']['name']['old'] == 'Old'
        assert result['diffs']['name']['new'] == 'New'

    def test_diff_ignores_timestamps(self):
        from app.models.test_case_version import diff_versions
        old = {'name': 'Test', 'created_at': '2026-01-01'}
        new = {'name': 'Test', 'created_at': '2026-06-01'}
        result = diff_versions(old, new)
        assert len(result['changed_fields']) == 0


# ══════════════════════════════════════════════════════════════════════════════
# 五、Service 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestVersionService:
    """ApiCaseService 版本方法测试"""

    def test_update_case_saves_version(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.api_test_case import ApiTestCase
        from app.services.api_case_service import ApiCaseService
        svc = ApiCaseService()
        with app.app_context():
            user = User(username=f"cv_{uuid.uuid4().hex[:6]}", email="cv@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="CVProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            case = ApiTestCase(
                user_id=user.id, project_id=proj.id,
                name="Original", method="GET", url="https://example.com",
            )
            db.session.add(case)
            db.session.flush()

            svc.update_case(case.id, user.id, {'name': 'Updated'})
            versions = svc.get_versions(case.id)
            assert versions['total'] == 1
            assert versions['items'][0]['content']['name'] == 'Original'
            db.session.rollback()

    def test_update_no_change_no_version(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.api_test_case import ApiTestCase
        from app.services.api_case_service import ApiCaseService
        svc = ApiCaseService()
        with app.app_context():
            user = User(username=f"cv_{uuid.uuid4().hex[:6]}", email="cv2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="CVProj2", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            case = ApiTestCase(
                user_id=user.id, project_id=proj.id,
                name="Same", method="GET", url="https://example.com",
            )
            db.session.add(case)
            db.session.flush()

            svc.update_case(case.id, user.id, {'name': 'Same'})
            versions = svc.get_versions(case.id)
            assert versions['total'] == 0
            db.session.rollback()

    def test_diff_two_versions_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.api_test_case import ApiTestCase
        from app.services.api_case_service import ApiCaseService
        svc = ApiCaseService()
        with app.app_context():
            user = User(username=f"cv_{uuid.uuid4().hex[:6]}", email="cv3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="CVProj3", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            case = ApiTestCase(
                user_id=user.id, project_id=proj.id,
                name="V1", method="GET", url="https://example.com",
            )
            db.session.add(case)
            db.session.flush()

            svc.update_case(case.id, user.id, {'name': 'V2'})
            svc.update_case(case.id, user.id, {'method': 'POST'})
            versions = svc.get_versions(case.id)
            v1_id = versions['items'][1]['id']
            v2_id = versions['items'][0]['id']

            diff = svc.diff_two_versions(v1_id, v2_id)
            assert 'diff' in diff
            assert 'name' in diff['diff']['changed_fields'] or 'method' in diff['diff']['changed_fields']
            db.session.rollback()