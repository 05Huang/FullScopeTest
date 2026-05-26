"""
项目模块测试
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


class TestProjectCRUD:
    """项目 CRUD 测试"""

    def test_create_project(self, client, auth_headers):
        """测试创建项目"""
        response = client.post('/api/v1/projects', json={
            'name': 'My Project',
            'description': 'Project Description'
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 201
        assert data['code'] == 201
        assert data['data']['name'] == 'My Project'
        assert data['data']['description'] == 'Project Description'

    def test_create_project_missing_name(self, client, auth_headers):
        """测试创建项目缺少名称"""
        response = client.post('/api/v1/projects', json={
            'description': 'No Name'
        }, headers=auth_headers)

        assert response.status_code == 400

    def test_get_projects(self, client, auth_headers, sample_project):
        """测试获取项目列表"""
        response = client.get('/api/v1/projects', headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert isinstance(data['data']['items'], list)
        assert len(data['data']['items']) > 0

    def test_get_project_by_id(self, client, auth_headers, sample_project):
        """测试通过 ID 获取项目"""
        project_id = sample_project['id']
        response = client.get(f'/api/v1/projects/{project_id}', headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['id'] == project_id

    def test_update_project(self, client, auth_headers, sample_project):
        """测试更新项目"""
        project_id = sample_project['id']
        response = client.put(f'/api/v1/projects/{project_id}', json={
            'name': 'Updated Project',
            'description': 'Updated Description'
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'Updated Project'
        assert data['data']['description'] == 'Updated Description'

    def test_delete_project(self, client, auth_headers, sample_project):
        """测试删除项目"""
        project_id = sample_project['id']
        response = client.delete(f'/api/v1/projects/{project_id}', headers=auth_headers)

        assert response.status_code == 200

        # 验证已删除
        response = client.get(f'/api/v1/projects/{project_id}', headers=auth_headers)
        assert response.status_code == 404


class TestProjectAuthorization:
    """项目权限测试"""

    def test_unauthorized_access(self, client):
        """测试未认证访问"""
        response = client.get('/api/v1/projects')
        assert response.status_code == 401

    def test_other_user_project_not_visible(self, client, auth_headers, sample_project):
        """测试其他用户项目不可见"""
        # 创建另一个用户
        other_username = f'other_{uuid.uuid4().hex[:8]}'
        client.post('/api/v1/auth/register', json={
            'username': other_username,
            'password': 'TestPass123!',
            'email': f'{other_username}@test.com'
        })
        response = client.post('/api/v1/auth/login', json={
            'username': other_username,
            'password': 'TestPass123!'
        })
        other_token = response.get_json()['data']['access_token']
        other_headers = {'Authorization': f'Bearer {other_token}'}

        # 获取项目列表应该为空
        response = client.get('/api/v1/projects', headers=other_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert len(data['data']['items']) == 0
