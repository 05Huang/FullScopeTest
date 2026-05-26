"""
环境变量模块测试
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


@pytest.fixture
def sample_environment(client, auth_headers, sample_project):
    """创建示例环境"""
    response = client.post('/api/v1/environments', json={
        'name': 'Development',
        'project_id': sample_project['id'],
        'base_url': 'http://localhost:8080',
        'variables': {
            'api_key': 'test-key-123'
        },
        'headers': {
            'X-Environment': 'dev'
        }
    }, headers=auth_headers)
    return response.get_json()['data']


class TestEnvironmentCRUD:
    """环境 CRUD 测试"""

    def test_create_environment(self, client, auth_headers, sample_project):
        """测试创建环境"""
        response = client.post('/api/v1/environments', json={
            'name': 'Production',
            'project_id': sample_project['id'],
            'base_url': 'https://api.example.com',
            'variables': {
                'api_key': 'prod-key'
            },
            'headers': {
                'X-Environment': 'prod'
            }
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 201
        assert data['data']['name'] == 'Production'

    def test_get_environments(self, client, auth_headers, sample_project, sample_environment):
        """测试获取环境列表"""
        response = client.get(
            f'/api/v1/environments?project_id={sample_project["id"]}',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200
        assert isinstance(data['data'], list)
        assert len(data['data']) > 0

    def test_get_environment_by_id(self, client, auth_headers, sample_environment):
        """测试通过 ID 获取环境"""
        env_id = sample_environment['id']
        response = client.get(f'/api/v1/environments/{env_id}', headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['id'] == env_id

    def test_update_environment(self, client, auth_headers, sample_environment):
        """测试更新环境"""
        env_id = sample_environment['id']
        response = client.put(f'/api/v1/environments/{env_id}', json={
            'name': 'Updated Dev',
            'variables': {
                'api_key': 'new-key'
            }
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'Updated Dev'

    def test_delete_environment(self, client, auth_headers, sample_environment):
        """测试删除环境"""
        env_id = sample_environment['id']
        response = client.delete(f'/api/v1/environments/{env_id}', headers=auth_headers)

        assert response.status_code == 200

        # 验证已删除
        response = client.get(f'/api/v1/environments/{env_id}', headers=auth_headers)
        assert response.status_code == 404


class TestEnvironmentVariables:
    """环境变量测试"""

    def test_variables_json_format(self, client, auth_headers, sample_project):
        """测试变量 JSON 格式"""
        variables = {
            'string_var': 'hello',
            'number_var': 123,
            'bool_var': True,
            'nested': {'key': 'value'}
        }

        response = client.post('/api/v1/environments', json={
            'name': 'JSON Test',
            'project_id': sample_project['id'],
            'variables': variables
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 201
        assert data['data']['variables']['string_var'] == 'hello'
        assert data['data']['variables']['number_var'] == 123

    def test_empty_variables(self, client, auth_headers, sample_project):
        """测试空变量"""
        response = client.post('/api/v1/environments', json={
            'name': 'Empty Vars',
            'project_id': sample_project['id'],
            'variables': {}
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 201
        assert data['data']['variables'] == {}
