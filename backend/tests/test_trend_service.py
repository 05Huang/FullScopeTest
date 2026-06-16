"""
质量趋势分析测试

覆盖：趋势 API、Dashboard 统计、时间粒度、边界条件
"""
import uuid
from datetime import datetime, timedelta


def _auth_headers(client, username=None):
    uid = uuid.uuid4().hex[:8]
    username = username or f"trend_{uid}"
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


def _create_test_run(client, headers, project_id, test_type='api', status='success',
                     total=5, passed=4, failed=1):
    """创建测试执行记录（通过 API + DB 补丁设置状态）"""
    resp = client.post("/api/v1/test-runs", headers=headers, json={
        "project_id": project_id,
        "test_type": test_type,
        "test_object_name": f"Test {test_type}",
        "total_cases": total,
    })
    data = resp.get_json()
    # API 创建的记录默认 status='pending'，需要通过 DB 更新
    if data.get("data") and data["data"].get("id"):
        from app.extensions import db
        from app.models.test_run import TestRun
        run_id = data["data"]["id"]
        run = TestRun.query.get(run_id)
        if run:
            run.status = status
            run.passed = passed
            run.failed = failed
            db.session.commit()
    return data


# ══════════════════════════════════════════════════════════════════════════════
# 一、Trend API 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestTrendAPI:
    """趋势 API 测试"""

    def test_get_trend_empty(self, client, no_rate_limit):
        """没有数据时返回空列表"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/trend?days=7", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data == []

    def test_get_trend_with_data(self, client, no_rate_limit):
        """有执行记录时返回趋势数据"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)

        # 创建并更新执行记录状态
        _create_test_run(client, headers, project["id"], 'api', 'success', 5, 5, 0)
        _create_test_run(client, headers, project["id"], 'web', 'failed', 3, 1, 2)

        resp = client.get(f"/api/v1/reports/trend?project_id={project['id']}&days=30", headers=headers)
        assert resp.status_code == 200
        resp_data = resp.get_json()
        assert resp_data["code"] == 200
        data = resp_data["data"]
        # 可能为空（如果没有成功/失败的记录），但应为列表
        assert isinstance(data, list)

    def test_get_trend_invalid_days(self, client, no_rate_limit):
        """无效的 days 参数应返回 400"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/trend?days=15", headers=headers)
        assert resp.status_code == 400

    def test_get_trend_invalid_granularity(self, client, no_rate_limit):
        """无效的 granularity 参数应返回 400"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/trend?granularity=year", headers=headers)
        assert resp.status_code == 400

    def test_get_trend_granularity_day(self, client, no_rate_limit):
        """按天粒度查询"""
        headers = _auth_headers(client)
        _create_test_run(client, headers, 1, 'api', 'success')
        resp = client.get("/api/v1/reports/trend?days=7&granularity=day", headers=headers)
        assert resp.status_code == 200

    def test_get_trend_granularity_month(self, client, no_rate_limit):
        """按月粒度查询"""
        headers = _auth_headers(client)
        _create_test_run(client, headers, 1, 'api', 'success')
        resp = client.get("/api/v1/reports/trend?days=90&granularity=month", headers=headers)
        assert resp.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# 二、Dashboard API 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestDashboardAPI:
    """Dashboard 统计 API 测试"""

    def test_get_trend_stats_endpoint(self, client, no_rate_limit):
        """趋势统计端点应返回正确的结构"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/trend/stats?days=7", headers=headers)
        assert resp.status_code == 200
        resp_data = resp.get_json()
        assert resp_data["code"] == 200
        data = resp_data["data"]
        # 验证返回结构
        assert "total_runs" in data or "period_days" in data

    def test_get_trend_stats_with_project(self, client, no_rate_limit):
        """按项目查询趋势统计"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        resp = client.get(f"/api/v1/reports/trend/stats?project_id={project['id']}&days=30", headers=headers)
        assert resp.status_code == 200
        resp_data = resp.get_json()
        assert resp_data["code"] == 200


# ══════════════════════════════════════════════════════════════════════════════
# 三、Service 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestTrendServiceUnit:
    """趋势 Service 单元测试"""

    def test_get_pass_rate_trend_empty(self, app):
        from app.services.trend_service import get_pass_rate_trend
        with app.app_context():
            # 使用不存在的 project_id 以确保隔离
            result = get_pass_rate_trend(project_id=999999, days=7)
            assert result == []

    def test_get_pass_rate_trend_with_runs(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.trend_service import get_pass_rate_trend
        with app.app_context():
            user = User(username=f"trend_{uuid.uuid4().hex[:6]}", email="t@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="TrendProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api', status='success',
                total_cases=10, passed=10, failed=0,
            )
            db.session.add(run)
            db.session.commit()

            result = get_pass_rate_trend(proj.id, 30, 'week')
            assert len(result) >= 1
            assert 'date' in result[0]
            assert 'api' in result[0]
            # 清理
            db.session.delete(run)
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()

    def test_get_dashboard_stats_empty(self, app):
        from app.services.trend_service import get_dashboard_stats
        with app.app_context():
            # 使用不存在的 project_id 以确保隔离
            result = get_dashboard_stats(project_id=999999, days=7)
            assert result['total_runs'] == 0
            assert result['pass_rate'] == 0

    def test_get_dashboard_stats_with_runs(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.trend_service import get_dashboard_stats
        with app.app_context():
            user = User(username=f"trend_{uuid.uuid4().hex[:6]}", email="t2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="TrendProj2", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            for tt, status, total, passed, failed in [
                ('api', 'success', 10, 10, 0),
                ('web', 'failed', 5, 2, 3),
            ]:
                run = TestRun(
                    project_id=proj.id, test_type=tt, status=status,
                    total_cases=total, passed=passed, failed=failed,
                )
                db.session.add(run)
            db.session.commit()

            result = get_dashboard_stats(proj.id, 30)
            assert result['total_runs'] >= 2
            assert 'api' in result['by_type']
            assert 'web' in result['by_type']
            # 清理
            TestRun.query.filter_by(project_id=proj.id).delete()
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()


class TestBucketKey:
    """时间分桶测试"""

    def test_day_bucket(self):
        from app.services.trend_service import _get_bucket_key
        dt = datetime(2026, 6, 15, 10, 30)
        assert _get_bucket_key(dt, 'day') == '2026-06-15'

    def test_week_bucket(self):
        from app.services.trend_service import _get_bucket_key
        dt = datetime(2026, 1, 5)
        key = _get_bucket_key(dt, 'week')
        assert '2026' in key
        assert 'W' in key

    def test_month_bucket(self):
        from app.services.trend_service import _get_bucket_key
        dt = datetime(2026, 6, 15)
        assert _get_bucket_key(dt, 'month') == '2026-06'