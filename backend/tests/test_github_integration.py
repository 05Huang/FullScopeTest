"""
GitHub 集成测试

测试 GitHub OAuth 集成的 API 端点
"""

import pytest
from unittest.mock import patch, MagicMock


class TestGitHubIntegrationAPI:
    """GitHub 集成 API 测试"""

    def test_get_integrations_empty(self, client):
        """测试获取 GitHub 状态（未认证）"""
        response = client.get('/api/v1/integrations/github/status')
        assert response.status_code == 401  # 未认证

    def test_auth_endpoint_requires_config(self, client):
        """测试 GitHub 未配置时返回错误"""
        response = client.get('/api/v1/integrations/github/auth')
        assert response.status_code == 401  # 未认证

    def test_callback_missing_code(self, client):
        """测试回调缺少 code 参数"""
        response = client.get('/api/v1/integrations/github/callback')
        assert response.status_code == 302  # 重定向到前端错误页面

    def test_callback_missing_state(self, client):
        """测试回调缺少 state 参数"""
        response = client.get('/api/v1/integrations/github/callback?code=abc')
        assert response.status_code == 302  # 重定向到前端错误页面

    def test_config_endpoint(self, client):
        """测试获取 GitHub OAuth 配置"""
        response = client.get('/api/v1/integrations/github/config')
        assert response.status_code == 200
        data = response.get_json()
        assert 'is_configured' in data['data']

    def test_unbind_nonexistent(self, client):
        """测试解绑不存在的集成"""
        response = client.post('/api/v1/integrations/github/unbind')
        assert response.status_code == 401  # 未认证


class TestGitHubIntegrationModel:
    """GitHub 集成模型测试"""

    def test_to_dict(self, app):
        """测试 to_dict 方法"""
        from app.models.github_integration import GitHubIntegration
        from datetime import datetime

        with app.app_context():
            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                github_email='test@example.com',
                github_avatar='https://avatars.githubusercontent.com/u/12345',
                access_token_encrypted='encrypted-token',
                scope='read:user',
                is_active=True,
            )

            data = integration.to_dict()
            assert data['github_username'] == 'testuser'
            assert data['github_user_id'] == '12345'
            assert data['is_active'] is True
            assert 'access_token' not in str(data)  # 确保不包含敏感信息
            assert data['token_valid'] is True

    def test_token_valid_when_inactive(self, app):
        """测试停用状态下 Token 无效"""
        from app.models.github_integration import GitHubIntegration

        with app.app_context():
            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted='encrypted-token',
                is_active=False,
            )

            assert integration._is_token_valid() is False

    def test_token_valid_when_expired(self, app):
        """测试过期 Token 无效"""
        from app.models.github_integration import GitHubIntegration
        from datetime import datetime, timedelta

        with app.app_context():
            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted='encrypted-token',
                is_active=True,
                token_expires_at=datetime.utcnow() - timedelta(hours=1),
            )

            assert integration._is_token_valid() is False


class TestGitHubOAuthService:
    """GitHub OAuth 服务测试"""

    def test_encrypt_decrypt_token(self):
        """测试 Token 加密解密"""
        from app.services.github_oauth_service import encrypt_token, decrypt_token

        original_token = 'ghp_test1234567890'
        encrypted = encrypt_token(original_token)
        decrypted = decrypt_token(encrypted)

        assert decrypted == original_token
        assert encrypted != original_token

    def test_generate_authorize_url(self):
        """测试生成授权 URL"""
        from app.services.github_oauth_service import generate_authorize_url

        url, state = generate_authorize_url('http://localhost:5000/callback')

        assert 'github.com/login/oauth/authorize' in url
        assert 'client_id=' in url
        assert 'state=' in url
        assert len(state) > 0


class TestGitHubCheckService:
    """GitHub Check Run 服务测试"""

    @patch('app.services.github_check_service.requests.request')
    def test_create_check_run_success(self, mock_request, app):
        """测试创建 Check Run 成功"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {'id': 12345, 'status': 'in_progress'}
            mock_response.content = b'{"id": 12345}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.create_check_run(
                repo_full_name='owner/repo',
                name='Test Check',
                head_sha='abc1234567890',
            )

            assert result is not None
            assert result['id'] == 12345
            mock_request.assert_called_once()

    @patch('app.services.github_check_service.requests.request')
    def test_create_check_run_with_output(self, mock_request, app):
        """测试创建 Check Run 带输出信息"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {'id': 12346, 'status': 'in_progress'}
            mock_response.content = b'{"id": 12346}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.create_check_run(
                repo_full_name='owner/repo',
                name='Test Check',
                head_sha='abc1234567890',
                output_title='Test Title',
                output_summary='Test Summary',
            )

            assert result is not None
            call_data = mock_request.call_args[1].get('json', mock_request.call_args[0][2] if len(mock_request.call_args[0]) > 2 else None)
            if call_data is None:
                call_args = mock_request.call_args
                call_data = call_args[1].get('json') if len(call_args) > 1 else None
            assert call_data['output']['title'] == 'Test Title'
            assert call_data['output']['summary'] == 'Test Summary'

    @patch('app.services.github_check_service.requests.request')
    def test_create_check_run_failure(self, mock_request, app):
        """测试创建 Check Run 失败"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 403
            mock_response.text = 'Forbidden'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.create_check_run(
                repo_full_name='owner/repo',
                name='Test Check',
                head_sha='abc1234567890',
            )

            assert result is None

    @patch('app.services.github_check_service.requests.request')
    def test_update_check_run_success(self, mock_request, app):
        """测试更新 Check Run 成功"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 12345, 'status': 'completed'}
            mock_response.content = b'{"id": 12345}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.update_check_run(
                repo_full_name='owner/repo',
                check_run_id=12345,
                status='completed',
                conclusion='success',
                output_title='Tests Passed',
                output_summary='All tests passed!',
            )

            assert result is not None
            assert result['status'] == 'completed'

    @patch('app.services.github_check_service.requests.request')
    def test_update_check_run_failure(self, mock_request, app):
        """测试更新 Check Run 失败"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.text = 'Internal Server Error'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.update_check_run(
                repo_full_name='owner/repo',
                check_run_id=12345,
                status='completed',
            )

            assert result is None

    @patch('app.services.github_check_service.requests.request')
    def test_start_test_check_run(self, mock_request, app):
        """测试开始测试时创建 Check Run"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {'id': 12347, 'status': 'in_progress'}
            mock_response.content = b'{"id": 12347}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            test_run = TestRun(
                project_id=1,
                test_type='api',
                status='running',
            )

            service = GitHubCheckService(integration)
            result = service.start_test_check_run(
                test_run=test_run,
                repo_full_name='owner/repo',
                head_sha='abc1234567890',
            )

            assert result is not None
            assert result['id'] == 12347

    @patch('app.services.github_check_service.requests.request')
    def test_update_test_progress(self, mock_request, app):
        """测试更新测试进度"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 12345}
            mock_response.content = b'{"id": 12345}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            test_run = TestRun(
                project_id=1,
                test_type='api',
                status='running',
                total_cases=10,
                passed=5,
                failed=2,
                skipped=2,
                error=1,
            )

            service = GitHubCheckService(integration)
            result = service.update_test_progress(
                repo_full_name='owner/repo',
                check_run_id=12345,
                test_run=test_run,
                current_step='Running test case #6',
            )

            assert result is not None
            call_args = mock_request.call_args
            call_data = call_args[1].get('json') if len(call_args) > 1 else None
            if call_data is None:
                call_data = call_args[0][2] if len(call_args[0]) > 2 else None
            assert 'output' in call_data
            assert 'Test Run #None' in call_data['output']['summary']
            assert 'Pass Rate' in call_data['output']['summary']

    @patch('app.services.github_check_service.requests.request')
    def test_complete_test_check_run_success(self, mock_request, app):
        """测试完成测试 Check Run - 成功"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 12345, 'conclusion': 'success'}
            mock_response.content = b'{"id": 12345}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            test_run = TestRun(
                project_id=1,
                test_type='api',
                status='success',
                total_cases=10,
                passed=10,
                failed=0,
                skipped=0,
                error=0,
                duration=12.5,
                environment_name='staging',
            )

            service = GitHubCheckService(integration)
            result = service.complete_test_check_run(
                repo_full_name='owner/repo',
                check_run_id=12345,
                test_run=test_run,
                report_url='https://example.com/report/1',
            )

            assert result is not None
            call_args = mock_request.call_args
            call_data = call_args[1].get('json') if len(call_args) > 1 else None
            if call_data is None:
                call_data = call_args[0][2] if len(call_args[0]) > 2 else None
            assert call_data['status'] == 'completed'
            assert call_data['conclusion'] == 'success'
            assert 'View Full Report' in call_data['output']['text']

    @patch('app.services.github_check_service.requests.request')
    def test_complete_test_check_run_failure(self, mock_request, app):
        """测试完成测试 Check Run - 失败"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 12345, 'conclusion': 'failure'}
            mock_response.content = b'{"id": 12345}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            test_run = TestRun(
                project_id=1,
                test_type='api',
                status='failed',
                total_cases=10,
                passed=7,
                failed=3,
                skipped=0,
                error=0,
                duration=8.3,
                results=[
                    {'name': 'Test Case 1', 'status': 'failed', 'error': 'AssertionError'},
                    {'name': 'Test Case 2', 'status': 'failed', 'error': 'TimeoutError'},
                    {'name': 'Test Case 3', 'status': 'failed', 'error': 'ConnectionError'},
                ],
            )

            service = GitHubCheckService(integration)
            result = service.complete_test_check_run(
                repo_full_name='owner/repo',
                check_run_id=12345,
                test_run=test_run,
            )

            assert result is not None
            call_args = mock_request.call_args
            call_data = call_args[1].get('json') if len(call_args) > 1 else None
            if call_data is None:
                call_data = call_args[0][2] if len(call_args[0]) > 2 else None
            assert call_data['status'] == 'completed'
            assert call_data['conclusion'] == 'failure'
            assert 'Failed Test Cases (3)' in call_data['output']['text']

    @patch('app.services.github_check_service.requests.request')
    def test_complete_test_check_run_with_failed_cases_limit(self, mock_request, app):
        """测试完成测试 Check Run - 失败用例超过 10 个时截断"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        from app.services.github_oauth_service import encrypt_token

        with app.app_context():
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'id': 12345}
            mock_response.content = b'{"id": 12345}'
            mock_request.return_value = mock_response

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            failed_cases = [{'name': f'Test {i}', 'status': 'failed', 'error': 'Error'} for i in range(15)]
            test_run = TestRun(
                project_id=1,
                test_type='api',
                status='failed',
                total_cases=15,
                passed=0,
                failed=15,
                results=failed_cases,
            )

            service = GitHubCheckService(integration)
            result = service.complete_test_check_run(
                repo_full_name='owner/repo',
                check_run_id=12345,
                test_run=test_run,
            )

            assert result is not None
            call_args = mock_request.call_args
            call_data = call_args[1].get('json') if len(call_args) > 1 else None
            if call_data is None:
                call_data = call_args[0][2] if len(call_args[0]) > 2 else None
            assert 'Failed Test Cases (15)' in call_data['output']['text']
            assert '5 more failed cases' in call_data['output']['text']

    @patch('app.services.github_check_service.requests.request')
    def test_timeout_handling(self, mock_request, app):
        """测试超时处理"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token
        import requests as req_lib

        with app.app_context():
            mock_request.side_effect = req_lib.exceptions.Timeout()

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.create_check_run(
                repo_full_name='owner/repo',
                name='Test Check',
                head_sha='abc1234567890',
            )

            assert result is None

    @patch('app.services.github_check_service.requests.request')
    def test_connection_error_handling(self, mock_request, app):
        """测试连接错误处理"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.services.github_oauth_service import encrypt_token
        import requests as req_lib

        with app.app_context():
            mock_request.side_effect = req_lib.exceptions.ConnectionError('Connection refused')

            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted=encrypt_token('ghp_test_token'),
                is_active=True,
            )

            service = GitHubCheckService(integration)
            result = service.create_check_run(
                repo_full_name='owner/repo',
                name='Test Check',
                head_sha='abc1234567890',
            )

            assert result is None

    def test_no_access_token(self, app):
        """测试无 access token 时返回 None"""
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration

        with app.app_context():
            integration = GitHubIntegration(
                user_id=1,
                github_user_id='12345',
                github_username='testuser',
                access_token_encrypted='',
                is_active=True,
            )

            service = GitHubCheckService(integration)
            token = service._get_access_token()
            assert token is None
