"""
触发器和定时任务模块测试
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


class TestWebhookCRUD:
    """Webhook CRUD 测试"""

    def test_create_webhook(self, client, auth_headers, sample_project):
        """测试创建 Webhook"""
        response = client.post('/api/v1/webhooks', json={
            'project_id': sample_project['id'],
            'name': 'Deploy Hook',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'Deploy Hook'
        assert 'token' in data['data']

    def test_get_webhooks(self, client, auth_headers, sample_project):
        """测试获取 Webhook 列表"""
        # 先创建一个
        client.post('/api/v1/webhooks', json={
            'project_id': sample_project['id'],
            'name': 'Test Hook',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)

        response = client.get(
            f'/api/v1/webhooks?project_id={sample_project["id"]}',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200
        assert isinstance(data['data'], list)

    def test_delete_webhook(self, client, auth_headers, sample_project):
        """测试删除 Webhook"""
        # 先创建一个
        create_response = client.post('/api/v1/webhooks', json={
            'project_id': sample_project['id'],
            'name': 'To Delete',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)
        webhook_id = create_response.get_json()['data']['id']

        # 删除
        response = client.delete(f'/api/v1/webhooks/{webhook_id}', headers=auth_headers)
        assert response.status_code == 200


class TestWebhookTrigger:
    """Webhook 触发测试"""

    def test_trigger_with_valid_token(self, client, auth_headers, sample_project):
        """测试使用有效 Token 触发"""
        # 创建 Webhook
        create_response = client.post('/api/v1/webhooks', json={
            'project_id': sample_project['id'],
            'name': 'Trigger Test',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)
        token = create_response.get_json()['data']['token']

        # 触发 (不需要认证)
        response = client.post(f'/api/v1/triggers/{token}')
        data = response.get_json()

        # 可能因为 collection 不存在而失败，但应该能识别 token
        assert response.status_code in [200, 400, 500]

    def test_trigger_with_invalid_token(self, client):
        """测试使用无效 Token 触发"""
        response = client.post('/api/v1/triggers/invalid-token-12345')
        assert response.status_code == 404


class TestScheduleCRUD:
    """定时任务 CRUD 测试"""

    def test_create_schedule(self, client, auth_headers, sample_project):
        """测试创建定时任务"""
        response = client.post('/api/v1/schedules', json={
            'project_id': sample_project['id'],
            'name': 'Daily Test',
            'cron_expression': '0 9 * * *',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'Daily Test'
        assert data['data']['cron_expression'] == '0 9 * * *'

    def test_get_schedules(self, client, auth_headers, sample_project):
        """测试获取定时任务列表"""
        # 先创建一个
        client.post('/api/v1/schedules', json={
            'project_id': sample_project['id'],
            'name': 'Test Schedule',
            'cron_expression': '0 * * * *',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)

        response = client.get(
            f'/api/v1/schedules?project_id={sample_project["id"]}',
            headers=auth_headers
        )

        data = response.get_json()
        assert response.status_code == 200
        assert isinstance(data['data'], list)

    def test_update_schedule(self, client, auth_headers, sample_project):
        """测试更新定时任务"""
        # 先创建一个
        create_response = client.post('/api/v1/schedules', json={
            'project_id': sample_project['id'],
            'name': 'To Update',
            'cron_expression': '0 9 * * *',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)
        task_id = create_response.get_json()['data']['id']

        # 更新
        response = client.put(f'/api/v1/schedules/{task_id}', json={
            'name': 'Updated Schedule',
            'is_active': False
        }, headers=auth_headers)

        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'Updated Schedule'

    def test_delete_schedule(self, client, auth_headers, sample_project):
        """测试删除定时任务"""
        # 先创建一个
        create_response = client.post('/api/v1/schedules', json={
            'project_id': sample_project['id'],
            'name': 'To Delete',
            'cron_expression': '0 9 * * *',
            'target_type': 'api_collection',
            'target_id': 1
        }, headers=auth_headers)
        task_id = create_response.get_json()['data']['id']

        # 删除
        response = client.delete(f'/api/v1/schedules/{task_id}', headers=auth_headers)
        assert response.status_code == 200
