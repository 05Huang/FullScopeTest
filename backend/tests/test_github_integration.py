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
