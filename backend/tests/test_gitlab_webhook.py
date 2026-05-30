"""GitLab Webhook 测试"""

import json
import hashlib
import hmac
import pytest


def _sign_payload(payload_bytes, secret):
    """生成 GitLab webhook 签名"""
    return 'sha256=' + hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()


@pytest.fixture(autouse=True)
def clear_gitlab_secret(app):
    """每个测试后清除 GitLab webhook secret"""
    yield
    with app.app_context():
        app.config['GITLAB_WEBHOOK_SECRET'] = ''


class TestGitLabWebhookPush:
    """GitLab push 事件测试"""

    def test_push_event_without_secret(self, client):
        """无 webhook secret 时直接处理"""
        payload = {
            'project': {'path_with_namespace': 'user/repo', 'name': 'repo'},
            'ref': 'refs/heads/main',
            'commits': [
                {'id': 'abc123', 'message': 'feat: add test', 'added': [], 'modified': ['src/app.py'], 'removed': []}
            ],
            'head_commit': {'id': 'abc123', 'message': 'feat: add test'},
        }

        response = client.post(
            '/api/v1/webhooks/gitlab',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'X-Gitlab-Event': 'Push Hook'},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200

    def test_push_event_with_invalid_signature(self, client):
        """无效签名的 push 事件"""
        secret = 'test-secret'
        
        with client.application.app_context():
            client.application.config['GITLAB_WEBHOOK_SECRET'] = secret

        response = client.post(
            '/api/v1/webhooks/gitlab',
            data=json.dumps({'project': {}}),
            content_type='application/json',
            headers={
                'X-Gitlab-Event': 'Push Hook',
                'X-Gitlab-Token': 'sha256=invalid',
            },
        )

        assert response.status_code == 401


class TestGitLabWebhookMR:
    """GitLab merge request 事件测试"""

    def test_mr_event_open(self, client):
        """MR opened 事件"""
        payload = {
            'object_attributes': {
                'action': 'open',
                'iid': 1,
                'title': 'Add new feature',
                'source_branch': 'feature-branch',
                'target_branch': 'main',
            },
            'project': {'path_with_namespace': 'user/repo', 'name': 'repo'},
        }

        response = client.post(
            '/api/v1/webhooks/gitlab',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'X-Gitlab-Event': 'Merge Request Hook'},
        )

        assert response.status_code == 200

    def test_mr_event_ignored_action(self, client):
        """忽略非 open/update/reopen 事件"""
        payload = {
            'object_attributes': {
                'action': 'close',
                'iid': 1,
                'title': 'Close PR',
            },
            'project': {'path_with_namespace': 'user/repo', 'name': 'repo'},
        }

        response = client.post(
            '/api/v1/webhooks/gitlab',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'X-Gitlab-Event': 'Merge Request Hook'},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'Ignored' in data['message']


class TestGitLabWebhookPing:
    """GitLab ping 事件测试"""

    def test_unknown_event_ignored(self, client):
        """未知事件类型被忽略"""
        response = client.post(
            '/api/v1/webhooks/gitlab',
            data=json.dumps({'zen': 'Keep it simple'}),
            content_type='application/json',
            headers={'X-Gitlab-Event': 'SomeOtherEvent'},
        )

        assert response.status_code == 200
