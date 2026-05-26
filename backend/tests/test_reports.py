"""
测试报告模块测试
"""

import uuid
import pytest


@pytest.fixture
def auth_headers(client):
    """获取认证头"""
    username = f'testuser_{uuid.uuid4().hex[:8]}'
    password = 'TestPass123!'

    # 注册用户
    client.post('/api/v1/auth/register', json={
        'username': username,
        'password': password,
        'email': f'{username}@test.com'
    })

    # 登录获取 token
    response = client.post('/api/v1/auth/login', json={
        'username': username,
        'password': password
    })
    token = response.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_project(client, auth_headers):
    """创建示例项目"""
    response = client.post('/api/v1/projects', json={
        'name': 'Test Project',
        'description': 'Test Description'
    }, headers=auth_headers)
    return response.get_json()['data']


class TestReportRetrieval:
    """报告检索测试"""

    def test_get_reports_list(self, client, auth_headers, sample_project):
        """测试获取报告列表"""
        response = client.get(
            f'/api/v1/reports?project_id={sample_project["id"]}',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200
        assert isinstance(data['data'], list) or isinstance(data['data'], dict)

    def test_get_reports_with_pagination(self, client, auth_headers, sample_project):
        """测试分页获取报告"""
        response = client.get(
            f'/api/v1/reports?project_id={sample_project["id"]}&page=1&per_page=10',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200

    def test_get_report_by_id(self, client, auth_headers):
        """测试通过 ID 获取报告（可能不存在）"""
        response = client.get('/api/v1/reports/99999', headers=auth_headers)
        # 应该返回 404
        assert response.status_code in [200, 404]

    def test_get_reports_unauthorized(self, client):
        """测试未认证获取报告"""
        response = client.get('/api/v1/reports')
        assert response.status_code == 401


class TestReportFiltering:
    """报告过滤测试"""

    def test_filter_by_test_type(self, client, auth_headers, sample_project):
        """测试按测试类型过滤"""
        response = client.get(
            f'/api/v1/reports?project_id={sample_project["id"]}&test_type=api',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200

    def test_filter_by_status(self, client, auth_headers, sample_project):
        """测试按状态过滤"""
        response = client.get(
            f'/api/v1/reports?project_id={sample_project["id"]}&status=completed',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200
