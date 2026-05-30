"""
GitHub Check Run Service Tests
"""

import pytest
from unittest.mock import patch, MagicMock


class TestGitHubCheckService:

    def test_create_check_service(self, app):
        from app.services.github_check_service import create_check_service
        from app.models.github_integration import GitHubIntegration

        with app.app_context():
            integration = GitHubIntegration(
                user_id=1, github_user_id='12345', github_username='testuser',
                access_token_encrypted='encrypted-token', is_active=True,
            )
            service = create_check_service(integration)
            assert service is not None
            assert service.integration == integration

    @patch('app.services.github_check_service.requests.request')
    def test_create_check_run_success(self, mock_request, app):
        from app.services.github_check_service import GitHubCheckService
        from app.models.github_integration import GitHubIntegration

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 12345, 'status': 'in_progress'}
        mock_response.content = b'{}'
        mock_request.return_value = mock_response

        with app.app_context():
            integration = GitHubIntegration(
                user_id=1, github_user_id='12345', github_username='testuser',
                access_token_encrypted='encrypted-token', is_active=True,
            )
            service = GitHubCheckService(integration)
            with patch.object(service, '_get_access_token', return_value='test-token'):
                result = service.create_check_run(
                    repo_full_name='owner/repo', name='FullScopeTest - API Test',
                    head_sha='abc123def456', status='in_progress',
                    output_title='Running tests', output_summary='Starting test run...',
                )
            assert result is not None
            assert result['id'] == 12345
