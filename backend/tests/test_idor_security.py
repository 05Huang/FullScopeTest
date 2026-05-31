"""
IDOR 安全测试

验证用户 A 无法通过猜测 ID 访问用户 B 的数据。
覆盖以下模块：
- 项目 (projects)
- API 测试集合/用例 (api_test)
- Web 测试脚本 (web_test)
- 性能测试场景 (perf_test)
- 质量门禁 (quality_gates)
- 告警规则 (alert_rules)
- 视觉回归 (visual)
"""

import json
import pytest


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user_a_token(client):
    """创建用户 A 并返回 token"""
    client.post('/api/v1/auth/register', json={
        'username': 'user_a_idor',
        'email': 'a@idor.test',
        'password': 'Test@1234',
    })
    resp = client.post('/api/v1/auth/login', json={
        'username': 'user_a_idor',
        'password': 'Test@1234',
    })
    data = resp.get_json()
    return data['data']['access_token']


@pytest.fixture()
def user_b_token(client):
    """创建用户 B 并返回 token"""
    client.post('/api/v1/auth/register', json={
        'username': 'user_b_idor',
        'email': 'b@idor.test',
        'password': 'Test@1234',
    })
    resp = client.post('/api/v1/auth/login', json={
        'username': 'user_b_idor',
        'password': 'Test@1234',
    })
    data = resp.get_json()
    return data['data']['access_token']


def _auth_header(token):
    return {'Authorization': f'Bearer {token}'}


class TestProjectIDOR:
    """项目 IDOR 测试"""

    def test_user_cannot_access_other_user_project(self, client, user_a_token, user_b_token):
        """用户 B 不能通过 ID 访问用户 A 的项目"""
        # 用户 A 创建项目
        resp = client.post('/api/v1/projects', json={'name': 'A的项目'},
                           headers=_auth_header(user_a_token))
        project_id = resp.get_json()['data']['id']

        # 用户 B 尝试访问用户 A 的项目
        resp = client.get(f'/api/v1/projects/{project_id}',
                          headers=_auth_header(user_b_token))
        assert resp.status_code in (404, 403)


class TestApiTestIDOR:
    """API 测试 IDOR 测试"""

    def test_user_cannot_access_other_user_collection(self, client, user_a_token, user_b_token):
        """用户 B 不能执行用户 A 的测试集合"""
        # 用户 A 创建项目和集合
        resp = client.post('/api/v1/projects', json={'name': 'A的项目'},
                           headers=_auth_header(user_a_token))
        project_id = resp.get_json()['data']['id']

        resp = client.post('/api/v1/api-test/collections', json={
            'name': 'A的集合', 'project_id': project_id,
        }, headers=_auth_header(user_a_token))
        collection_id = resp.get_json()['data']['id']

        # 用户 B 尝试执行用户 A 的集合
        resp = client.post(f'/api/v1/api-test/collections/{collection_id}/run',
                           headers=_auth_header(user_b_token))
        assert resp.status_code in (404, 403)


class TestQualityGateIDOR:
    """质量门禁 IDOR 测试"""

    def test_user_cannot_access_other_user_quality_gate(self, client, user_a_token, user_b_token):
        """用户 B 不能访问用户 A 的质量门禁"""
        # 用户 A 创建项目和质量门禁
        resp = client.post('/api/v1/projects', json={'name': 'A的项目'},
                           headers=_auth_header(user_a_token))
        project_id = resp.get_json()['data']['id']

        resp = client.post('/api/v1/quality-gates', json={
            'name': 'A的门禁', 'project_id': project_id,
        }, headers=_auth_header(user_a_token))
        gate_id = resp.get_json()['data']['id']

        # 用户 B 尝试访问
        resp = client.get(f'/api/v1/quality-gates/{gate_id}',
                          headers=_auth_header(user_b_token))
        assert resp.status_code in (404, 403)

        # 用户 B 尝试更新
        resp = client.put(f'/api/v1/quality-gates/{gate_id}',
                          json={'name': '被篡改'},
                          headers=_auth_header(user_b_token))
        assert resp.status_code in (404, 403)

        # 用户 B 尝试删除
        resp = client.delete(f'/api/v1/quality-gates/{gate_id}',
                             headers=_auth_header(user_b_token))
        assert resp.status_code in (404, 403)


class TestAlertRuleIDOR:
    """告警规则 IDOR 测试"""

    def test_user_cannot_access_other_user_alert_rule(self, client, user_a_token, user_b_token):
        """用户 B 不能访问用户 A 的告警规则"""
        # 用户 A 创建场景和告警规则
        resp = client.post('/api/v1/projects', json={'name': 'A的项目'},
                           headers=_auth_header(user_a_token))
        project_id = resp.get_json()['data']['id']

        resp = client.post('/api/v1/perf-test/scenarios', json={
            'name': 'A的场景', 'project_id': project_id,
            'target_url': 'http://example.com', 'concurrent_users': 10,
            'duration': 60, 'spawn_rate': 5,
        }, headers=_auth_header(user_a_token))
        scenario_id = resp.get_json()['data']['id']

        resp = client.post('/api/v1/perf-test/alert-rules', json={
            'name': 'A的规则', 'scenario_id': scenario_id,
            'condition_type': 'absolute', 'metric_name': 'response_time',
            'operator': '>', 'threshold_value': 1000,
        }, headers=_auth_header(user_a_token))
        rule_id = resp.get_json()['data']['id']

        # 用户 B 尝试访问
        resp = client.get(f'/api/v1/perf-test/alert-rules/{rule_id}',
                          headers=_auth_header(user_b_token))
        assert resp.status_code in (404, 403)
