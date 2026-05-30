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


# ==================== 触发规则测试 ====================


class TestTriggerRuleCRUD:
    """触发规则 CRUD 测试"""

    def test_create_trigger_rule(self, client, auth_headers, sample_project):
        """测试创建触发规则"""
        response = client.post('/api/v1/trigger-rules', json={
            'project_id': sample_project['id'],
            'name': 'PR to Main',
            'trigger_event': 'pull_request',
            'target_type': 'api_collection',
            'target_branches': ['main', 'master'],
            'description': 'Run tests when PR targets main'
        }, headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'PR to Main'
        assert data['data']['trigger_event'] == 'pull_request'
        assert data['data']['target_branches'] == ['main', 'master']

    def test_create_trigger_rule_missing_fields(self, client, auth_headers, sample_project):
        """测试创建触发规则缺少必填字段"""
        response = client.post('/api/v1/trigger-rules', json={
            'project_id': sample_project['id'],
            'name': 'Incomplete Rule'
        }, headers=auth_headers)
        assert response.status_code == 400

    def test_get_trigger_rules(self, client, auth_headers, sample_project):
        """测试获取触发规则列表"""
        client.post('/api/v1/trigger-rules', json={
            'project_id': sample_project['id'],
            'name': 'Rule 1',
            'trigger_event': 'push',
            'target_type': 'api_collection'
        }, headers=auth_headers)
        client.post('/api/v1/trigger-rules', json={
            'project_id': sample_project['id'],
            'name': 'Rule 2',
            'trigger_event': 'pull_request',
            'target_type': 'web_collection'
        }, headers=auth_headers)

        response = client.get(
            f'/api/v1/trigger-rules?project_id={sample_project["id"]}',
            headers=auth_headers
        )
        data = response.get_json()
        assert response.status_code == 200
        assert len(data['data']) == 2

    def test_update_trigger_rule(self, client, auth_headers, sample_project):
        """测试更新触发规则"""
        create_response = client.post('/api/v1/trigger-rules', json={
            'project_id': sample_project['id'],
            'name': 'To Update',
            'trigger_event': 'push',
            'target_type': 'api_collection'
        }, headers=auth_headers)
        rule_id = create_response.get_json()['data']['id']

        response = client.put(f'/api/v1/trigger-rules/{rule_id}', json={
            'name': 'Updated Rule',
            'target_branches': ['develop']
        }, headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert data['data']['name'] == 'Updated Rule'

    def test_delete_trigger_rule(self, client, auth_headers, sample_project):
        """测试删除触发规则"""
        create_response = client.post('/api/v1/trigger-rules', json={
            'project_id': sample_project['id'],
            'name': 'To Delete',
            'trigger_event': 'push',
            'target_type': 'api_collection'
        }, headers=auth_headers)
        rule_id = create_response.get_json()['data']['id']

        response = client.delete(f'/api/v1/trigger-rules/{rule_id}', headers=auth_headers)
        assert response.status_code == 200

        get_response = client.get(
            f'/api/v1/trigger-rules?project_id={sample_project["id"]}',
            headers=auth_headers
        )
        assert len(get_response.get_json()['data']) == 0

    def test_delete_nonexistent_rule(self, client, auth_headers):
        """测试删除不存在的规则"""
        response = client.delete('/api/v1/trigger-rules/99999', headers=auth_headers)
        assert response.status_code == 404


class TestTriggerRuleService:
    """触发规则服务单元测试"""

    def test_create_rule(self, app, sample_project):
        """测试通过服务层创建规则"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            rule = create_rule(
                project_id=project.id,
                name='Test Rule',
                trigger_event='push',
                target_type='api_collection',
                created_by=1,
                target_branches=['main'],
                include_paths=['/api/**'],
            )
            assert rule.id is not None
            assert rule.name == 'Test Rule'
            assert rule.target_branches == ['main']
            assert rule.include_paths == ['/api/**']

    def test_evaluate_push_event_matching(self, app, sample_project):
        """测试 push 事件匹配规则"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_push_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='API Path Rule',
                trigger_event='push',
                target_type='api_collection',
                created_by=1,
                target_branches=['main'],
                include_paths=['/api/**'],
            )

            result = evaluate_push_event(
                ref='refs/heads/main',
                changed_files=['/api/users.py', '/api/auth.py'],
                commit_message='feat: update API',
                repository='owner/repo'
            )

            assert result['should_trigger'] is True
            assert len(result['matched_rules']) == 1

    def test_evaluate_push_event_no_match(self, app, sample_project):
        """测试 push 事件不匹配规则"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_push_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='Main Branch Rule',
                trigger_event='push',
                target_type='api_collection',
                created_by=1,
                target_branches=['main'],
            )

            result = evaluate_push_event(
                ref='refs/heads/develop',
                changed_files=['/api/users.py'],
                commit_message='feat: update',
                repository='owner/repo'
            )

            assert result['should_trigger'] is False

    def test_evaluate_push_event_file_path_match(self, app, sample_project):
        """测试文件路径匹配"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_push_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='Web Path Rule',
                trigger_event='push',
                target_type='web_collection',
                created_by=1,
                include_paths=['/src/**'],
                exclude_paths=['/src/**/*.test.*'],
            )

            result = evaluate_push_event(
                ref='refs/heads/main',
                changed_files=['/src/components/Button.tsx'],
                commit_message='feat: update button',
                repository='owner/repo'
            )
            assert result['should_trigger'] is True

            result = evaluate_push_event(
                ref='refs/heads/main',
                changed_files=['/src/utils/helper.test.ts'],
                commit_message='test: update tests',
                repository='owner/repo'
            )
            assert result['should_trigger'] is False

    def test_evaluate_pr_event(self, app, sample_project):
        """测试 PR 事件匹配"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_pr_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='PR to Main',
                trigger_event='pull_request',
                target_type='api_collection',
                created_by=1,
                target_branches=['main'],
            )

            result = evaluate_pr_event(
                action='opened',
                head_branch='feature/new-feature',
                base_branch='main',
                pr_number=42,
                pr_title='Add new feature',
                repository='owner/repo',
                changed_files=[]
            )

            assert result['should_trigger'] is True

    def test_evaluate_pr_event_wrong_branch(self, app, sample_project):
        """测试 PR 事件目标分支不匹配"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_pr_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='PR to Main',
                trigger_event='pull_request',
                target_type='api_collection',
                created_by=1,
                target_branches=['main'],
            )

            result = evaluate_pr_event(
                action='opened',
                head_branch='feature/new-feature',
                base_branch='develop',
                pr_number=42,
                pr_title='Add new feature',
                repository='owner/repo',
                changed_files=[]
            )

            assert result['should_trigger'] is False

    def test_multiple_rules_match(self, app, sample_project):
        """测试多个规则同时匹配"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_push_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='Rule 1',
                trigger_event='push',
                target_type='api_collection',
                created_by=1,
                target_branches=['main'],
            )
            create_rule(
                project_id=project.id,
                name='Rule 2',
                trigger_event='push',
                target_type='web_collection',
                created_by=1,
                target_branches=['main'],
            )

            result = evaluate_push_event(
                ref='refs/heads/main',
                changed_files=[],
                commit_message='update',
                repository='owner/repo'
            )

            assert result['should_trigger'] is True
            assert len(result['matched_rules']) == 2
            assert len(result['test_types']) == 2

    def test_exclude_paths(self, app, sample_project):
        """测试排除路径匹配"""
        with app.app_context():
            from app.services.trigger_rule_service import create_rule, evaluate_push_event
            from app.models.project import Project

            project = Project.query.get(sample_project['id'])
            create_rule(
                project_id=project.id,
                name='Exclude Docs',
                trigger_event='push',
                target_type='api_collection',
                created_by=1,
                include_paths=['/**'],
                exclude_paths=['/docs/**', '*.md'],
            )

            result = evaluate_push_event(
                ref='refs/heads/main',
                changed_files=['/docs/README.md', '/docs/api.md'],
                commit_message='update docs',
                repository='owner/repo'
            )
            assert result['should_trigger'] is False

            result = evaluate_push_event(
                ref='refs/heads/main',
                changed_files=['/src/main.py'],
                commit_message='update code',
                repository='owner/repo'
            )
            assert result['should_trigger'] is True
