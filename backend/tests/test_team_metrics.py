"""
团队效能度量测试

覆盖：团队指标计算、按成员分组、API 端点、边界条件
"""
import uuid


def _auth_headers(client, username=None):
    uid = uuid.uuid4().hex[:8]
    username = username or f"tm_{uid}"
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
# 一、Service 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestTeamMetricsService:
    """团队效能 Service 测试"""

    def test_get_team_metrics_empty(self, app):
        from app.services.team_metrics_service import get_team_metrics
        with app.app_context():
            result = get_team_metrics(project_id=999999, days=30)
            assert result['period_days'] == 30
            assert result['summary']['total_members'] == 0
            assert result['summary']['total_cases'] == 0
            assert result['members'] == []

    def test_get_team_metrics_with_cases(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.api_test_case import ApiTestCase
        from app.services.team_metrics_service import get_team_metrics
        with app.app_context():
            user = User(username=f"tm_{uuid.uuid4().hex[:6]}", email="tm@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="TMProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            for i in range(5):
                case = ApiTestCase(
                    user_id=user.id, project_id=proj.id,
                    name=f"Case {i}", method="GET", url="https://example.com",
                )
                db.session.add(case)
            db.session.commit()

            result = get_team_metrics(proj.id, 30)
            assert result['summary']['total_members'] >= 1
            assert result['summary']['total_cases'] >= 5
            assert len(result['members']) >= 1
            assert result['members'][0]['cases_created'] >= 5

            # 清理
            ApiTestCase.query.filter_by(project_id=proj.id).delete()
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()

    def test_get_team_metrics_with_runs(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.team_metrics_service import get_team_metrics
        with app.app_context():
            user = User(username=f"tm_{uuid.uuid4().hex[:6]}", email="tm2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="TMProj2", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api', status='success',
                total_cases=10, passed=8, failed=2,
                triggered_user_id=user.id,
            )
            db.session.add(run)
            db.session.commit()

            result = get_team_metrics(proj.id, 30)
            assert len(result['members']) >= 1
            member = result['members'][0]
            assert member['runs_executed'] >= 1
            assert member['defect_rate'] > 0
            assert member['regression_pass_rate'] > 0

            TestRun.query.filter_by(project_id=proj.id).delete()
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()

    def test_get_team_metrics_member_structure(self, app):
        from app.services.team_metrics_service import _empty_member_data
        with app.app_context():
            data = _empty_member_data(1)
            assert data['user_id'] == 1
            assert data['cases_created'] == 0
            assert data['defect_rate'] == 0.0
            assert data['regression_pass_rate'] == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 二、API 端点测试
# ══════════════════════════════════════════════════════════════════════════════

class TestTeamMetricsAPI:
    """团队效能 API 测试"""

    def test_get_team_metrics_empty(self, client, no_rate_limit):
        """没有数据时返回空成员列表"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/team-metrics?days=7", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert "summary" in data
        assert "members" in data
        assert data["summary"]["total_members"] == 0

    def test_get_team_metrics_with_project(self, client, no_rate_limit):
        """按项目查询团队效能"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        resp = client.get(
            f"/api/v1/reports/team-metrics?project_id={project['id']}&days=30",
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["period_days"] == 30

    def test_get_team_metrics_structure(self, client, no_rate_limit):
        """验证返回结构"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/team-metrics", headers=headers)
        data = resp.get_json()["data"]
        assert "summary" in data
        assert "members" in data
        assert "period_days" in data
        assert "project_id" in data
        summary = data["summary"]
        assert "total_members" in summary
        assert "total_cases" in summary
        assert "total_runs" in summary
        assert "avg_cases_per_member" in summary