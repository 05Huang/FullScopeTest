"""GitHub Check Run tests"""
from unittest.mock import patch, MagicMock

class TestGitHubCheckService:
    def test_create_check_service(self):
        from app.services.github_check_service import create_check_service
        from app.models.github_integration import GitHubIntegration
        integration = MagicMock(spec=GitHubIntegration)
        service = create_check_service(integration)
        assert service is not None
        assert service.integration == integration

    def test_get_access_token_no_integration(self):
        from app.services.github_check_service import GitHubCheckService
        service = GitHubCheckService(None)
        token = service._get_access_token()
        assert token is None

    def test_create_check_run_success(self):
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        integration = MagicMock(spec=GitHubIntegration)
        integration.access_token_encrypted = 'encrypted_token'
        service = GitHubCheckService(integration)
        mock_response = {'id': 12345, 'status': 'in_progress'}
        with patch('app.services.github_oauth_service.decrypt_token', return_value='token'):
            with patch.object(service, '_make_request', return_value=mock_response):
                result = service.create_check_run(repo_full_name='owner/repo', name='Test', head_sha='abc123')
                assert result == mock_response
                assert result['id'] == 12345

    def test_start_test_check_run(self):
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        integration = MagicMock(spec=GitHubIntegration)
        integration.access_token_encrypted = 'encrypted_token'
        service = GitHubCheckService(integration)
        test_run = MagicMock(spec=TestRun)
        test_run.id = 1
        test_run.test_type = 'api'
        test_run.project_id = 10
        mock_response = {'id': 12345}
        with patch('app.services.github_oauth_service.decrypt_token', return_value='token'):
            with patch.object(service, 'create_check_run', return_value=mock_response) as mock_create:
                result = service.start_test_check_run(test_run, 'owner/repo', 'abc123')
                assert result == mock_response
                mock_create.assert_called_once()

    def test_complete_test_check_run_success(self):
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        integration = MagicMock(spec=GitHubIntegration)
        integration.access_token_encrypted = 'encrypted_token'
        service = GitHubCheckService(integration)
        test_run = MagicMock(spec=TestRun)
        test_run.id = 1
        test_run.test_type = 'api'
        test_run.status = 'success'
        test_run.total_cases = 10
        test_run.passed = 10
        test_run.failed = 0
        test_run.skipped = 0
        test_run.error = 0
        test_run.duration = 5.5
        test_run.environment_name = 'staging'
        test_run.results = []
        mock_response = {'id': 12345}
        with patch('app.services.github_oauth_service.decrypt_token', return_value='token'):
            with patch.object(service, 'update_check_run', return_value=mock_response) as mock_update:
                result = service.complete_test_check_run('owner/repo', 12345, test_run, report_url='https://example.com/report')
                assert result == mock_response
                call_kwargs = mock_update.call_args[1]
                assert call_kwargs['status'] == 'completed'
                assert call_kwargs['conclusion'] == 'success'
                assert 'View Full Report' in call_kwargs['output_text']

    def test_complete_test_check_run_failure(self):
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration
        from app.models.test_run import TestRun
        integration = MagicMock(spec=GitHubIntegration)
        integration.access_token_encrypted = 'encrypted_token'
        service = GitHubCheckService(integration)
        test_run = MagicMock(spec=TestRun)
        test_run.id = 1
        test_run.test_type = 'api'
        test_run.status = 'failed'
        test_run.total_cases = 10
        test_run.passed = 8
        test_run.failed = 2
        test_run.skipped = 0
        test_run.error = 0
        test_run.duration = 5.5
        test_run.environment_name = None
        test_run.results = [
            {'name': 'Test 1', 'status': 'passed'},
            {'name': 'Test 2', 'status': 'failed', 'error': 'AssertionError'},
            {'name': 'Test 3', 'status': 'failed', 'error_message': 'Timeout'},
        ]
        mock_response = {'id': 12345}
        with patch('app.services.github_oauth_service.decrypt_token', return_value='token'):
            with patch.object(service, 'update_check_run', return_value=mock_response) as mock_update:
                result = service.complete_test_check_run('owner/repo', 12345, test_run)
                assert result == mock_response
                call_kwargs = mock_update.call_args[1]
                assert call_kwargs['conclusion'] == 'failure'
                assert 'Failed Test Cases' in call_kwargs['output_text']
                assert 'Test 2' in call_kwargs['output_text']
                assert 'Test 3' in call_kwargs['output_text']
