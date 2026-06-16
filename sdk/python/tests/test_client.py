"""
FullScopeTest SDK 客户端测试

覆盖：客户端初始化、认证、请求方法、CLI 命令
"""
import json
import pytest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fullscopetest.client import FullScopeTestClient


# ══════════════════════════════════════════════════════════════════════════════
# 一、客户端初始化测试
# ══════════════════════════════════════════════════════════════════════════════

class TestClientInit:
    """客户端初始化测试"""

    def test_init_with_api_token(self):
        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="test-token")
        assert client.base_url == "http://localhost:8000"
        assert "Bearer test-token" in client._session.headers["Authorization"]

    def test_init_with_jwt_token(self):
        client = FullScopeTestClient(base_url="http://localhost:8000", jwt_token="jwt-token")
        assert "Bearer jwt-token" in client._session.headers["Authorization"]

    def test_init_no_token_raises(self):
        with pytest.raises(ValueError, match="必须提供"):
            FullScopeTestClient(base_url="http://localhost:8000")

    def test_init_strips_trailing_slash(self):
        client = FullScopeTestClient(base_url="http://localhost:8000/", api_token="t")
        assert client.base_url == "http://localhost:8000"

    def test_init_custom_timeout(self):
        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t", timeout=60)
        assert client.timeout == 60

    def test_init_custom_retries(self):
        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t", max_retries=5)
        assert client.max_retries == 5


# ══════════════════════════════════════════════════════════════════════════════
# 二、请求方法测试
# ══════════════════════════════════════════════════════════════════════════════

class TestClientRequests:
    """请求方法测试"""

    @patch("fullscopetest.client.requests.Session.request")
    def test_get_request(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"code": 200, "data": []}
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value = mock_resp

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t")
        result = client._get("/api/v1/projects")
        assert result["code"] == 200
        mock_request.assert_called_once()

    @patch("fullscopetest.client.requests.Session.request")
    def test_post_request(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"code": 201, "data": {"id": 1}}
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value = mock_resp

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t")
        result = client._post("/api/v1/projects", json={"name": "Test"})
        assert result["data"]["id"] == 1

    @patch("fullscopetest.client.requests.Session.request")
    def test_retry_on_server_error(self, mock_request):
        fail_resp = MagicMock()
        fail_resp.status_code = 500
        fail_resp.raise_for_status.side_effect = Exception("500")
        ok_resp = MagicMock()
        ok_resp.status_code = 200
        ok_resp.json.return_value = {"code": 200}
        ok_resp.raise_for_status = MagicMock()
        mock_request.side_effect = [fail_resp, ok_resp]

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t", retry_delay=0.01)
        with patch("fullscopetest.client.time.sleep"):
            result = client._get("/api/v1/test")
        assert result["code"] == 200

    @patch("fullscopetest.client.requests.Session.request")
    def test_max_retries_exceeded(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.raise_for_status.side_effect = Exception("500")
        mock_request.return_value = mock_resp

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t", max_retries=2, retry_delay=0.01)
        with patch("fullscopetest.client.time.sleep"):
            with pytest.raises(Exception):
                client._get("/api/v1/test")
        assert mock_request.call_count == 2


# ══════════════════════════════════════════════════════════════════════════════
# 三、高级方法测试
# ══════════════════════════════════════════════════════════════════════════════

class TestClientMethods:
    """高级方法测试"""

    @patch("fullscopetest.client.requests.Session.request")
    def test_create_project(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"code": 201, "data": {"id": 1, "name": "Test"}}
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value = mock_resp

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t")
        result = client.create_project("Test")
        assert result["data"]["name"] == "Test"

    @patch("fullscopetest.client.requests.Session.request")
    def test_create_test_run(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"code": 201, "data": {"id": 1, "status": "pending"}}
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value = mock_resp

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t")
        result = client.create_test_run(project_id=1, test_type="api")
        assert result["data"]["status"] == "pending"

    @patch("fullscopetest.client.requests.Session.request")
    def test_import_postman(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"code": 200, "data": {"total": 3, "imported": 3}}
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value = mock_resp

        client = FullScopeTestClient(base_url="http://localhost:8000", api_token="t")
        result = client.import_postman(project_id=1, content='{"item": []}')
        assert result["data"]["imported"] == 3


# ══════════════════════════════════════════════════════════════════════════════
# 四、CLI 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCLI:
    """CLI 命令测试"""

    def test_cli_help(self):
        from fullscopetest.cli import main
        with patch("sys.argv", ["fst", "--help"]):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0

    def test_cli_no_command(self):
        from fullscopetest.cli import main
        with patch("sys.argv", ["fst"]):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 1

    @patch("fullscopetest.client.requests.Session.request")
    def test_cli_run(self, mock_request, capsys):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {"code": 201, "data": {"id": 1, "status": "pending"}}
        mock_resp.raise_for_status = MagicMock()
        mock_request.return_value = mock_resp

        from fullscopetest.cli import main
        with patch("sys.argv", ["fst", "--api-token", "t", "run", "--project-id", "1", "--type", "api"]):
            main()
        captured = capsys.readouterr()
        assert "Run ID=1" in captured.out

    def test_get_client_no_token_exits(self):
        from fullscopetest.cli import get_client
        args = MagicMock()
        args.base_url = "http://localhost:8000"
        args.api_token = None
        args.jwt_token = None

        # 清除环境变量
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(SystemExit):
                get_client(args)