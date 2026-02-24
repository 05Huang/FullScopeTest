import subprocess
import uuid

from app.extensions import db
from app.models.project import Project
from app.models.test_report import TestReport as TestReportModel
from app.models.test_run import TestRun as TestRunModel
from app.models.user import User
from app.models.web_test_script import WebTestScript
from app.tasks import run_web_test_task


def _seed_user_and_script(app, with_project=True):
    with app.app_context():
        suffix = uuid.uuid4().hex[:8]
        user = User(
            username=f'web_case_user_{suffix}',
            email=f'web_case_user_{suffix}@example.com',
            password_hash='hashed-password',
        )
        db.session.add(user)
        db.session.flush()

        project_id = None
        if with_project:
            project = Project(name='Web Project', owner_id=user.id)
            db.session.add(project)
            db.session.flush()
            project_id = project.id

        script = WebTestScript(
            name='web smoke',
            description='smoke case',
            script_content='print("ok")',
            project_id=project_id,
            user_id=user.id,
            browser='chromium',
            timeout=30000,
        )
        db.session.add(script)
        db.session.commit()
        return user.id, script.id


def test_run_web_test_task_creates_run_and_report_on_success(app, monkeypatch):
    user_id, script_id = _seed_user_and_script(app, with_project=True)

    monkeypatch.setattr('app.tasks._get_flask_app', lambda: app)
    monkeypatch.setattr(
        'app.tasks.subprocess.run',
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout='done',
            stderr='',
        ),
    )

    result = run_web_test_task.run(script_id, user_id)

    assert result['success'] is True
    assert result['test_run_id'] is not None
    assert result['report_id'] is not None

    with app.app_context():
        script = db.session.get(WebTestScript, script_id)
        assert script.status == 'passed'
        assert script.last_result['success'] is True

        test_run = TestRunModel.query.filter_by(id=result['test_run_id']).first()
        assert test_run is not None
        assert test_run.test_type == 'web'
        assert test_run.status == 'success'
        assert test_run.total_cases == 1
        assert test_run.passed == 1
        assert test_run.failed == 0

        report = TestReportModel.query.filter_by(id=result['report_id']).first()
        assert report is not None
        assert report.test_type == 'web'
        assert report.test_run_id == test_run.id
        assert report.summary['passed'] == 1


def test_run_web_test_task_creates_failed_report_on_nonzero_exit(app, monkeypatch):
    user_id, script_id = _seed_user_and_script(app, with_project=True)

    monkeypatch.setattr('app.tasks._get_flask_app', lambda: app)
    monkeypatch.setattr(
        'app.tasks.subprocess.run',
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0],
            returncode=1,
            stdout='',
            stderr='boom',
        ),
    )

    result = run_web_test_task.run(script_id, user_id)

    assert result['success'] is False
    assert result['test_run_id'] is not None
    assert result['report_id'] is not None

    with app.app_context():
        script = db.session.get(WebTestScript, script_id)
        assert script.status == 'failed'
        assert script.last_result['success'] is False

        test_run = db.session.get(TestRunModel, result['test_run_id'])
        assert test_run.status == 'failed'
        assert test_run.passed == 0
        assert test_run.failed == 1

        report = db.session.get(TestReportModel, result['report_id'])
        assert report.summary['failed'] == 1


def test_run_web_test_task_without_project_does_not_create_report_records(app, monkeypatch):
    user_id, script_id = _seed_user_and_script(app, with_project=False)
    with app.app_context():
        before_run_count = TestRunModel.query.count()
        before_report_count = TestReportModel.query.count()

    monkeypatch.setattr('app.tasks._get_flask_app', lambda: app)
    monkeypatch.setattr(
        'app.tasks.subprocess.run',
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout='done',
            stderr='',
        ),
    )

    result = run_web_test_task.run(script_id, user_id)

    assert result['success'] is True
    assert result['test_run_id'] is None
    assert result['report_id'] is None

    with app.app_context():
        assert TestRunModel.query.count() == before_run_count
        assert TestReportModel.query.count() == before_report_count
        assert TestRunModel.query.filter_by(test_object_id=script_id, test_type='web').count() == 0
