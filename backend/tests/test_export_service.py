"""
报告导出服务测试

覆盖：PDF 生成、增强 Excel 生成、多 Sheet 结构、按范围查询、
     边界条件、API 端点
"""
import uuid


def _auth_headers(client, username=None):
    uid = uuid.uuid4().hex[:8]
    username = username or f"exp_{uid}"
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
# 一、PDF 生成测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPDFExport:
    """PDF 报告生成测试"""

    def test_generate_pdf_report(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import generate_pdf_report
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api', status='success',
                total_cases=10, passed=8, failed=2,
                results=[
                    {'name': 'Test1', 'status': 'passed'},
                    {'name': 'Test2', 'status': 'failed', 'error': 'AssertionError'},
                ],
            )
            db.session.add(run)
            db.session.flush()

            pdf_bytes = generate_pdf_report(run.id)
            if pdf_bytes is not None:
                assert len(pdf_bytes) > 0
                assert pdf_bytes[:4] == b'%PDF'  # PDF magic bytes
            db.session.rollback()

    def test_generate_pdf_not_found(self, app):
        from app.services.export_service import generate_pdf_report
        from app.utils.exceptions import NotFoundError
        import pytest
        with app.app_context():
            with pytest.raises(NotFoundError):
                generate_pdf_report(99999)

    def test_generate_pdf_no_results(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import generate_pdf_report
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj2", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(project_id=proj.id, test_type='api', status='success', total_cases=0)
            db.session.add(run)
            db.session.flush()

            pdf_bytes = generate_pdf_report(run.id)
            if pdf_bytes is not None:
                assert len(pdf_bytes) > 0
            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 二、增强 Excel 生成测试
# ══════════════════════════════════════════════════════════════════════════════

class TestEnhancedExcel:
    """增强版 Excel 报告测试"""

    def test_generate_enhanced_excel_by_run(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import generate_enhanced_excel
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj3", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api', status='success',
                total_cases=5, passed=5, failed=0,
                results=[{'name': 'C1', 'status': 'passed'}],
            )
            db.session.add(run)
            db.session.flush()

            excel_bytes = generate_enhanced_excel(test_run_id=run.id)
            assert excel_bytes is not None
            assert len(excel_bytes) > 0
            assert b'PK' in excel_bytes[:4]  # Excel is ZIP format
            db.session.rollback()

    def test_generate_enhanced_excel_by_project(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import generate_enhanced_excel
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp4@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj4", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            for i in range(3):
                run = TestRun(project_id=proj.id, test_type='api', status='success', total_cases=1)
                db.session.add(run)
            db.session.commit()

            excel_bytes = generate_enhanced_excel(project_id=proj.id)
            assert excel_bytes is not None
            TestRun.query.filter_by(project_id=proj.id).delete()
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()

    def test_generate_enhanced_excel_with_filters(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import generate_enhanced_excel
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp5@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj5", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(project_id=proj.id, test_type='api', status='success', total_cases=1)
            db.session.add(run)
            db.session.commit()

            excel_bytes = generate_enhanced_excel(project_id=proj.id, days=30, test_type='api')
            assert excel_bytes is not None
            TestRun.query.filter_by(project_id=proj.id).delete()
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()

    def test_generate_enhanced_excel_performance_sheet(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import generate_enhanced_excel
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp6@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj6", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='performance', status='success',
                total_cases=1, results=[{'total_requests': 1000, 'avg_response_time': 50}],
            )
            db.session.add(run)
            db.session.flush()

            excel_bytes = generate_enhanced_excel(test_run_id=run.id)
            assert excel_bytes is not None
            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 三、API 端点测试
# ══════════════════════════════════════════════════════════════════════════════

class TestExportAPI:
    """导出 API 端点测试"""

    def test_export_excel_range_endpoint(self, client, no_rate_limit):
        """按范围导出 Excel 端点"""
        headers = _auth_headers(client)
        resp = client.get("/api/v1/reports/export/excel", headers=headers)
        assert resp.status_code == 200

    def test_export_excel_range_with_filters(self, client, no_rate_limit):
        """带过滤参数的 Excel 导出"""
        headers = _auth_headers(client)
        project = _create_project(client, headers)
        resp = client.get(
            f"/api/v1/reports/export/excel?project_id={project['id']}&days=30&test_type=api",
            headers=headers,
        )
        assert resp.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# 四、内部工具测试
# ══════════════════════════════════════════════════════════════════════════════

class TestExportHelpers:
    """内部工具函数测试"""

    def test_query_runs_by_id(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.export_service import _query_runs
        with app.app_context():
            user = User(username=f"exp_{uuid.uuid4().hex[:6]}", email="exp7@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ExpProj7", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(project_id=proj.id, test_type='api', status='success', total_cases=1)
            db.session.add(run)
            db.session.flush()

            result = _query_runs(test_run_id=run.id, project_id=None, days=None, test_type=None)
            assert len(result) == 1
            assert result[0].id == run.id
            db.session.rollback()

    def test_query_runs_empty(self, app):
        from app.services.export_service import _query_runs
        with app.app_context():
            result = _query_runs(test_run_id=99999, project_id=None, days=None, test_type=None)
            assert len(result) == 0

    def test_try_register_chinese_font(self):
        from app.services.export_service import _try_register_chinese_font
        # 不应抛异常
        _try_register_chinese_font()