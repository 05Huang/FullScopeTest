"""
Webhook 通知服务测试

覆盖：payload 构建、重试机制、渠道适配
"""
from unittest.mock import patch, MagicMock
import pytest


class TestBuildPayload:
    """通知 payload 构建测试"""

    def test_webhook_payload_format(self):
        from app.services.notification_service import _build_payload
        payload = _build_payload('webhook', 'test_completed', 'Test', 'OK', {'key': 'val'})
        assert payload['event'] == 'test_completed'
        assert payload['title'] == 'Test'
        assert payload['source'] == 'fullscopetest'
        assert payload['data'] == {'key': 'val'}

    def test_dingtalk_payload_format(self):
        from app.services.notification_service import _build_payload
        payload = _build_payload('dingtalk', 'test_failed', 'Fail', 'Error')
        assert payload['msgtype'] == 'markdown'
        assert 'Fail' in payload['markdown']['title']

    def test_feishu_payload_format(self):
        from app.services.notification_service import _build_payload
        payload = _build_payload('feishu', 'test_completed', 'OK', 'Done')
        assert payload['msg_type'] == 'interactive'
        assert payload['card']['header']['title']['content'] == 'OK'

    def test_slack_payload_format(self):
        from app.services.notification_service import _build_payload
        payload = _build_payload('slack', 'test_completed', 'OK', 'Done')
        assert 'blocks' in payload
        assert payload['blocks'][0]['type'] == 'header'


class TestSendNotification:
    """通知发送测试"""

    @patch('app.services.notification_service.requests.post')
    def test_send_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        from app.services.notification_service import send_notification
        result = send_notification('webhook', 'http://test.webhook', 'test_completed', 'T', 'C')
        assert result['success'] is True
        assert result['status_code'] == 200

    @patch('app.services.notification_service.requests.post')
    def test_send_retries_on_failure(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_post.return_value = mock_resp

        from app.services.notification_service import send_notification
        with patch('app.services.notification_service.time.sleep'):
            result = send_notification('webhook', 'http://test.webhook', 'test_failed', 'T', 'C')
        assert result['success'] is False
        assert mock_post.call_count == 3  # MAX_RETRIES = 3

    @patch('app.services.notification_service.requests.post')
    def test_send_retries_on_connection_error(self, mock_post):
        import requests as req_lib
        mock_post.side_effect = req_lib.ConnectionError('refused')

        from app.services.notification_service import send_notification
        with patch('app.services.notification_service.time.sleep'):
            result = send_notification('webhook', 'http://test.webhook', 'test_failed', 'T', 'C')
        assert result['success'] is False
        assert mock_post.call_count == 3

    @patch('app.services.notification_service.requests.post')
    def test_send_succeeds_after_retry(self, mock_post):
        import requests as req_lib
        fail_resp = MagicMock()
        fail_resp.status_code = 500
        ok_resp = MagicMock()
        ok_resp.status_code = 200
        mock_post.side_effect = [fail_resp, ok_resp]

        from app.services.notification_service import send_notification
        with patch('app.services.notification_service.time.sleep'):
            result = send_notification('webhook', 'http://test.webhook', 'test_completed', 'T', 'C')
        assert result['success'] is True
        assert mock_post.call_count == 2


class TestNotifyTestResult:
    """测试结果通知便捷方法测试"""

    @patch('app.services.notification_service.requests.post')
    def test_notify_completed(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        from app.services.notification_service import notify_test_result
        result = notify_test_result('http://test.webhook', 'webhook', 'Login Test', 'completed', 5.2)
        assert result['success'] is True
        call_args = mock_post.call_args
        assert 'Login Test' in str(call_args)

    @patch('app.services.notification_service.requests.post')
    def test_notify_failed(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        from app.services.notification_service import notify_test_result
        result = notify_test_result('http://test.webhook', 'dingtalk', 'API Test', 'failed', 10.0, 'Timeout')
        assert result['success'] is True
