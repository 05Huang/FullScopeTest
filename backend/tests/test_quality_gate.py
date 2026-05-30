"""Quality Gate tests"""

import pytest
from app.models.quality_gate import QualityGate
from app.models.test_run import TestRun
from app.services.quality_gate_service import quality_gate_service


def _register_and_login(client, username=None, password="Str0ng!Pass"):
    if username is None:
        username = f"test_user_{__import__('random').randint(1000, 9999)}"
    client.post('/api/v1/auth/register', json={'username': username, 'email': f'{username}@test.com', 'password': password})
    resp = client.post('/api/v1/auth/login', json={'username': username, 'password': password})
    return resp.get_json()['data']['access_token']


class TestQualityGateService:

    def test_evaluate_pass_rate_below_threshold(self, client):
        with client.application.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.user import User
            from werkzeug.security import generate_password_hash
            user = User(username='eval_qg_1', email='eval_qg_1@test.com', password_hash=generate_password_hash('test'))
            db.session.add(user); db.session.commit()
            project = Project(name='Test', owner_id=user.id); db.session.add(project); db.session.commit()
            gate = QualityGate(project_id=project.id, name='Test Gate', min_pass_rate=95.0, created_by=user.id)
            db.session.add(gate); db.session.commit()
            test_run = TestRun(project_id=project.id, test_type='api', status='success', total_cases=100, passed=80, failed=15, skipped=5)
            db.session.add(test_run); db.session.commit()
            result = quality_gate_service.evaluate(gate, test_run)
            assert result['passed'] is False
            assert len(result['violations']) == 1
            assert result['violations'][0]['metric'] == 'pass_rate'

    def test_evaluate_pass_rate_above_threshold(self, client):
        with client.application.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.user import User
            from werkzeug.security import generate_password_hash
            user = User(username='eval_qg_2', email='eval_qg_2@test.com', password_hash=generate_password_hash('test'))
            db.session.add(user); db.session.commit()
            project = Project(name='Test', owner_id=user.id); db.session.add(project); db.session.commit()
            gate = QualityGate(project_id=project.id, name='Test Gate', min_pass_rate=95.0, created_by=user.id)
            db.session.add(gate); db.session.commit()
            test_run = TestRun(project_id=project.id, test_type='api', status='success', total_cases=100, passed=98, failed=2)
            db.session.add(test_run); db.session.commit()
            result = quality_gate_service.evaluate(gate, test_run)
            assert result['passed'] is True
            assert len(result['violations']) == 0

    def test_evaluate_no_threshold(self, client):
        with client.application.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.user import User
            from werkzeug.security import generate_password_hash
            user = User(username='eval_qg_3', email='eval_qg_3@test.com', password_hash=generate_password_hash('test'))
            db.session.add(user); db.session.commit()
            project = Project(name='Test', owner_id=user.id); db.session.add(project); db.session.commit()
            gate = QualityGate(project_id=project.id, name='Empty Gate', created_by=user.id, min_pass_rate=100.0, max_p95_response_time=None, max_visual_diff_percentage=None)
            db.session.add(gate); db.session.commit()
            test_run = TestRun(project_id=project.id, test_type='api', status='success', total_cases=100, passed=100)
            db.session.add(test_run); db.session.commit()
            result = quality_gate_service.evaluate(gate, test_run)
            assert result['passed'] is True
            assert len(result['violations']) == 0


class TestQualityGateAPI:

    def test_create_and_evaluate(self, client):
        token = _register_and_login(client)
        headers = {'Authorization': f'Bearer {token}'}
        with client.application.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.user import User
            from werkzeug.security import generate_password_hash
            user = User(username='qg_api_user', email='qg_api@test.com', password_hash=generate_password_hash('test'))
            db.session.add(user); db.session.commit()
            project = Project(name='Test', owner_id=user.id); db.session.add(project); db.session.commit()
            test_run = TestRun(project_id=project.id, test_type='api', status='success', total_cases=100, passed=100)
            db.session.add(test_run); db.session.commit()
            project_id = project.id
            test_run_id = test_run.id
        resp = client.post('/api/v1/quality-gates', json={'project_id': project_id, 'name': 'Gate', 'pass_rate_threshold': 95.0}, headers=headers)
        gate_id = resp.get_json()['data']['id']
        resp = client.post(f'/api/v1/quality-gates/{gate_id}/evaluate', json={'test_run_id': test_run_id}, headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['passed'] is True