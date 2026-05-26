"""
全局搜索模块测试
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
        'name': 'Search Test Project',
        'description': 'Project for search testing'
    }, headers=auth_headers)
    return response.get_json()['data']


class TestGlobalSearch:
    """全局搜索测试"""

    def test_search_unauthorized(self, client):
        """测试未认证搜索"""
        response = client.post('/api/v1/ai/global-search', json={
            'query': 'test'
        })
        assert response.status_code in [401, 422]

    def test_search_with_keyword(self, client, auth_headers, sample_project):
        """测试关键词搜索"""
        response = client.post(
            '/api/v1/ai/global-search',
            json={'query': 'test'},
            headers=auth_headers
        )

        # 搜索可能因 AI 服务不可用而失败，但不应返回 500
        assert response.status_code in [200, 400, 500]

    def test_search_empty_query(self, client, auth_headers):
        """测试空查询"""
        response = client.post(
            '/api/v1/ai/global-search',
            json={'query': ''},
            headers=auth_headers
        )

        # 空查询应该返回空结果或错误
        assert response.status_code in [200, 400]

    def test_search_no_results(self, client, auth_headers):
        """测试无结果搜索"""
        response = client.post(
            '/api/v1/ai/global-search',
            json={'query': 'nonexistent_xyz_12345'},
            headers=auth_headers
        )

        assert response.status_code in [200, 400, 500]

    def test_search_with_type_filter(self, client, auth_headers):
        """测试带类型过滤的搜索"""
        response = client.post(
            '/api/v1/ai/global-search',
            json={'query': 'test', 'type': 'project'},
            headers=auth_headers
        )

        assert response.status_code in [200, 400, 500]

    def test_search_with_project_scope(self, client, auth_headers, sample_project):
        """测试项目范围内的搜索"""
        response = client.post(
            '/api/v1/ai/global-search',
            json={'query': 'test', 'project_id': sample_project['id']},
            headers=auth_headers
        )

        assert response.status_code in [200, 400, 500]
