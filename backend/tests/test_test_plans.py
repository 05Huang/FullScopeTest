"""
测试计划模块测试

覆盖：计划 CRUD、执行轮次、用例结果更新、通过率趋势、
     边界条件和错误处理
"""
import uuid


def _auth_headers(client, username=None):
    """注册并登录用户，返回认证头"""
    uid = uuid.uuid4().hex[:8]
    username = username or f"tp_{uid}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={
        "username": username, "email": email, "password": password,
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": username, "password": password,
    })
    token = resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_project(client, headers, name=None):
    """创建测试项目"""
    name = name or f"Proj_{uuid.uuid4().hex[:8]}"
    resp = client.post("/api/v1/projects", headers=headers, json={"name": name})
    return resp.get_json()["data"]


def _create_api_case(client, headers, project_id, name=None):
    """创建一个 API 测试用例"""
    name = name or f"Case_{uuid.uuid4().hex[:8]}"
    resp = client.post("/api/v1/api-tests/cases", headers=headers, json={
        "project_id": project_id,
        "name": name,
        "method": "GET",
        "url": "https://httpbin.org/get",
    })
    data = resp.get_json()
    if data.get("data"):
        return data["data"]
    # 某些环境可能不存在该端点，返回模拟数据
    return {"id": 1, "name": name}


# ══════════════════════════════════════════════════════════════════════════════
# 一、计划 CRUD 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPlanCRUD:
    """测试计划 CRUD 测试"""

    def test_create_plan(self, client, no_rate_limit):
        """创建测试计划"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "回归测试计划",
            "project_id": project["id"],
            "description": "V2.0 回归测试",
            "tags": ["regression", "v2.0"],
        })
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["name"] == "回归测试计划"
        assert data["project_id"] == project["id"]
        assert data["status"] == "draft"
        assert "regression" in data["tags"]

    def test_create_plan_missing_name(self, client, no_rate_limit):
        """缺少名称应返回 400"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        resp = client.post("/api/v1/test-plans", headers=headers, json={
            "project_id": project["id"],
        })
        assert resp.status_code == 400

    def test_create_plan_missing_project(self, client, no_rate_limit):
        """缺少 project_id 应返回 400"""
        headers = _auth_headers(client)

        resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Test Plan",
        })
        assert resp.status_code == 400

    def test_list_plans(self, client, no_rate_limit):
        """获取计划列表"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        # 创建 2 个计划
        for i in range(2):
            client.post("/api/v1/test-plans", headers=headers, json={
                "name": f"Plan {i}",
                "project_id": project["id"],
            })

        resp = client.get(f"/api/v1/test-plans?project_id={project['id']}", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] >= 2

    def test_list_plans_missing_project_id(self, client, no_rate_limit):
        """缺少 project_id 查询参数应返回 400"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/test-plans", headers=headers)
        assert resp.status_code == 400

    def test_get_plan_detail(self, client, no_rate_limit):
        """获取计划详情"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        create_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Detail Plan",
            "project_id": project["id"],
            "include_cases": [{"case_type": "api", "case_id": 1}],
        })
        plan_id = create_resp.get_json()["data"]["id"]

        resp = client.get(f"/api/v1/test-plans/{plan_id}", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["name"] == "Detail Plan"
        assert len(data["include_cases"]) == 1

    def test_get_plan_not_found(self, client, no_rate_limit):
        """获取不存在的计划应返回 404"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/test-plans/99999", headers=headers)
        assert resp.status_code == 404

    def test_update_plan(self, client, no_rate_limit):
        """更新计划"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        create_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Old Name",
            "project_id": project["id"],
        })
        plan_id = create_resp.get_json()["data"]["id"]

        resp = client.put(f"/api/v1/test-plans/{plan_id}", headers=headers, json={
            "name": "New Name",
            "description": "Updated description",
            "status": "active",
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["name"] == "New Name"
        assert data["status"] == "active"

    def test_update_plan_not_found(self, client, no_rate_limit):
        """更新不存在的计划应返回 404"""
        headers = _auth_headers(client)
        resp = client.put("/api/v1/test-plans/99999", headers=headers, json={
            "name": "New",
        })
        assert resp.status_code == 404

    def test_delete_plan(self, client, no_rate_limit):
        """删除计划"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        create_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "To Delete",
            "project_id": project["id"],
        })
        plan_id = create_resp.get_json()["data"]["id"]

        resp = client.delete(f"/api/v1/test-plans/{plan_id}", headers=headers)
        assert resp.status_code == 200

        # 确认已删除
        resp = client.get(f"/api/v1/test-plans/{plan_id}", headers=headers)
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 二、执行轮次测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPlanRuns:
    """执行轮次测试"""

    def _create_plan_with_cases(self, client, headers):
        """创建包含用例的计划"""
        project = _create_project(client, headers)
        resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Run Test Plan",
            "project_id": project["id"],
            "include_cases": [
                {"case_type": "api", "case_id": 1},
                {"case_type": "api", "case_id": 2},
                {"case_type": "web", "case_id": 10},
            ],
        })
        return resp.get_json()["data"]

    def test_create_run(self, client, no_rate_limit):
        """创建执行轮次"""
        headers = _auth_headers(client)
        plan = self._create_plan_with_cases(client, headers)

        resp = client.post(f"/api/v1/test-plans/{plan['id']}/runs", headers=headers, json={
            "environment_name": "staging",
            "notes": "V2.0 回归",
        })
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["status"] == "pending"
        assert data["total_cases"] == 3
        assert len(data["case_results"]) == 3
        assert data["environment_name"] == "staging"

    def test_create_run_no_cases(self, client, no_rate_limit):
        """没有用例的计划不能创建轮次"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        plan_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Empty Plan",
            "project_id": project["id"],
        })
        plan_id = plan_resp.get_json()["data"]["id"]

        resp = client.post(f"/api/v1/test-plans/{plan_id}/runs", headers=headers, json={})
        assert resp.status_code == 400

    def test_list_runs(self, client, no_rate_limit):
        """获取轮次列表"""
        headers = _auth_headers(client)
        plan = self._create_plan_with_cases(client, headers)

        # 创建 2 个轮次
        for _ in range(2):
            client.post(f"/api/v1/test-plans/{plan['id']}/runs", headers=headers, json={})

        resp = client.get(f"/api/v1/test-plans/{plan['id']}/runs", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] >= 2

    def test_get_run_detail(self, client, no_rate_limit):
        """获取轮次详情"""
        headers = _auth_headers(client)
        plan = self._create_plan_with_cases(client, headers)

        run_resp = client.post(f"/api/v1/test-plans/{plan['id']}/runs", headers=headers, json={})
        run_id = run_resp.get_json()["data"]["id"]

        resp = client.get(f"/api/v1/test-plan-runs/{run_id}", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total_cases"] == 3
        assert len(data["case_results"]) == 3

    def test_get_run_not_found(self, client, no_rate_limit):
        """获取不存在的轮次应返回 404"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/test-plan-runs/99999", headers=headers)
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 三、用例结果更新测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCaseResults:
    """用例结果更新测试"""

    def _setup_run(self, client, headers):
        """创建一个轮次"""
        project = _create_project(client, headers)
        plan_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Result Plan",
            "project_id": project["id"],
            "include_cases": [
                {"case_type": "api", "case_id": 1},
                {"case_type": "api", "case_id": 2},
            ],
        })
        plan_id = plan_resp.get_json()["data"]["id"]

        run_resp = client.post(f"/api/v1/test-plans/{plan_id}/runs", headers=headers, json={})
        return run_resp.get_json()["data"]

    def test_update_case_result_passed(self, client, no_rate_limit):
        """更新用例结果为 passed"""
        headers = _auth_headers(client)
        run = self._setup_run(client, headers)

        resp = client.patch(f"/api/v1/test-plan-runs/{run['id']}/case-results", headers=headers, json={
            "case_type": "api",
            "case_id": 1,
            "status": "passed",
            "duration": 1.5,
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["status"] == "passed"
        assert data["duration"] == 1.5

    def test_update_case_result_failed(self, client, no_rate_limit):
        """更新用例结果为 failed"""
        headers = _auth_headers(client)
        run = self._setup_run(client, headers)

        resp = client.patch(f"/api/v1/test-plan-runs/{run['id']}/case-results", headers=headers, json={
            "case_type": "api",
            "case_id": 1,
            "status": "failed",
            "error_message": "AssertionError: expected 200 got 500",
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["status"] == "failed"

    def test_update_case_result_missing_fields(self, client, no_rate_limit):
        """缺少必填字段应返回 400"""
        headers = _auth_headers(client)
        run = self._setup_run(client, headers)

        resp = client.patch(f"/api/v1/test-plan-runs/{run['id']}/case-results", headers=headers, json={
            "case_type": "api",
            # 缺少 case_id 和 status
        })
        assert resp.status_code == 400

    def test_update_case_result_not_found(self, client, no_rate_limit):
        """更新不存在的用例结果应返回 404"""
        headers = _auth_headers(client)
        run = self._setup_run(client, headers)

        resp = client.patch(f"/api/v1/test-plan-runs/{run['id']}/case-results", headers=headers, json={
            "case_type": "api",
            "case_id": 99999,
            "status": "passed",
        })
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 四、轮次完成与通过率测试
# ══════════════════════════════════════════════════════════════════════════════

class TestRunCompletion:
    """轮次完成与通过率测试"""

    def _setup_run_with_results(self, client, headers, passed_count=1, failed_count=1):
        """创建轮次并更新所有用例结果"""
        project = _create_project(client, headers)
        cases = []
        for i in range(passed_count):
            cases.append({"case_type": "api", "case_id": i + 1})
        for i in range(failed_count):
            cases.append({"case_type": "api", "case_id": passed_count + i + 1})

        plan_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Complete Plan",
            "project_id": project["id"],
            "include_cases": cases,
        })
        plan_id = plan_resp.get_json()["data"]["id"]

        run_resp = client.post(f"/api/v1/test-plans/{plan_id}/runs", headers=headers, json={})
        run_id = run_resp.get_json()["data"]["id"]

        # 更新结果
        for i in range(passed_count):
            client.patch(f"/api/v1/test-plan-runs/{run_id}/case-results", headers=headers, json={
                "case_type": "api", "case_id": i + 1, "status": "passed", "duration": 0.5,
            })
        for i in range(failed_count):
            client.patch(f"/api/v1/test-plan-runs/{run_id}/case-results", headers=headers, json={
                "case_type": "api", "case_id": passed_count + i + 1,
                "status": "failed", "error_message": "Fail",
            })

        return run_id, plan_id

    def test_complete_run_calculates_pass_rate(self, client, no_rate_limit):
        """完成轮次后正确计算通过率"""
        headers = _auth_headers(client)
        run_id, _ = self._setup_run_with_results(client, headers, passed_count=3, failed_count=1)

        resp = client.post(f"/api/v1/test-plan-runs/{run_id}/complete", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["status"] == "completed"
        assert data["passed"] == 3
        assert data["failed"] == 1
        assert data["pass_rate"] == 75.0

    def test_complete_run_updates_plan_stats(self, client, no_rate_limit):
        """完成轮次后更新计划的最后执行信息"""
        headers = _auth_headers(client)
        run_id, plan_id = self._setup_run_with_results(client, headers, passed_count=2, failed_count=0)

        client.post(f"/api/v1/test-plan-runs/{run_id}/complete", headers=headers)

        # 获取计划详情
        resp = client.get(f"/api/v1/test-plans/{plan_id}", headers=headers)
        data = resp.get_json()["data"]
        assert data["last_pass_rate"] == 100.0
        assert data["last_run_at"] is not None

    def test_complete_run_not_found(self, client, no_rate_limit):
        """完成不存在的轮次应返回 404"""
        headers = _auth_headers(client)
        resp = client.post("/api/v1/test-plan-runs/99999/complete", headers=headers)
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 五、通过率趋势测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPassRateTrend:
    """通过率趋势测试"""

    def test_get_trend_empty(self, client, no_rate_limit):
        """没有轮次时趋势为空"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        plan_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Trend Plan",
            "project_id": project["id"],
            "include_cases": [{"case_type": "api", "case_id": 1}],
        })
        plan_id = plan_resp.get_json()["data"]["id"]

        resp = client.get(f"/api/v1/test-plans/{plan_id}/trend", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data == []

    def test_get_trend_with_runs(self, client, no_rate_limit):
        """有多次轮次后返回趋势数据"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        plan_resp = client.post("/api/v1/test-plans", headers=headers, json={
            "name": "Trend Plan 2",
            "project_id": project["id"],
            "include_cases": [
                {"case_type": "api", "case_id": 1},
                {"case_type": "api", "case_id": 2},
            ],
        })
        plan_id = plan_resp.get_json()["data"]["id"]

        # 创建并完成 2 个轮次
        for _ in range(2):
            run_resp = client.post(f"/api/v1/test-plans/{plan_id}/runs", headers=headers, json={})
            run_id = run_resp.get_json()["data"]["id"]
            # 标记所有用例通过
            for cid in [1, 2]:
                client.patch(f"/api/v1/test-plan-runs/{run_id}/case-results", headers=headers, json={
                    "case_type": "api", "case_id": cid, "status": "passed",
                })
            client.post(f"/api/v1/test-plan-runs/{run_id}/complete", headers=headers)

        resp = client.get(f"/api/v1/test-plans/{plan_id}/trend", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) == 2
        assert data[0]["pass_rate"] == 100.0


# ══════════════════════════════════════════════════════════════════════════════
# 六、Service 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPlanServiceUnit:
    """PlanService 单元测试"""

    def test_create_plan_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.services.plan_service import PlanService
        svc = PlanService()
        with app.app_context():
            user = User(username=f"svc_{uuid.uuid4().hex[:6]}", email="svc@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="SvcProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()

            result = svc.create_plan(
                user_id=user.id,
                project_id=proj.id,
                name="Service Plan",
                description="Created by service",
                include_cases=[{"case_type": "api", "case_id": 1}],
                tags=["test"],
            )
            assert result["name"] == "Service Plan"
            assert len(result["include_cases"]) == 1
            db.session.rollback()

    def test_create_plan_empty_name_raises(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.services.plan_service import PlanService
        from app.utils.exceptions import ValidationError
        svc = PlanService()
        with app.app_context():
            user = User(username=f"svc_{uuid.uuid4().hex[:6]}", email="svc2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="SvcProj2", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()

            import pytest
            with pytest.raises(ValidationError):
                svc.create_plan(user_id=user.id, project_id=proj.id, name="")
            db.session.rollback()

    def test_update_case_result_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_plan import TestPlan, TestPlanRun, TestPlanCaseResult
        from app.services.plan_service import PlanService
        svc = PlanService()
        with app.app_context():
            user = User(username=f"svc_{uuid.uuid4().hex[:6]}", email="svc3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="SvcProj3", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()

            plan = svc.create_plan(
                user_id=user.id, project_id=proj.id, name="P",
                include_cases=[{"case_type": "api", "case_id": 1}],
            )
            run = svc.create_run(plan_id=plan['id'], user_id=user.id)
            run_id = run['id']

            result = svc.update_case_result(run_id, 'api', 1, 'passed', duration=0.5)
            assert result['status'] == 'passed'

            completed = svc.complete_run(run_id)
            assert completed['pass_rate'] == 100.0
            db.session.rollback()

    def test_get_pass_rate_trend_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.services.plan_service import PlanService
        svc = PlanService()
        with app.app_context():
            user = User(username=f"svc_{uuid.uuid4().hex[:6]}", email="svc4@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="SvcProj4", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()

            plan = svc.create_plan(
                user_id=user.id, project_id=proj.id, name="T",
                include_cases=[{"case_type": "api", "case_id": 1}],
            )

            # 创建并完成一个轮次
            run = svc.create_run(plan_id=plan['id'], user_id=user.id)
            svc.update_case_result(run['id'], 'api', 1, 'passed')
            svc.complete_run(run['id'])

            trend = svc.get_pass_rate_trend(plan['id'])
            assert len(trend) == 1
            assert trend[0]['pass_rate'] == 100.0
            db.session.rollback()