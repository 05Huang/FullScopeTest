"""
自然语言创建测试用例测试
"""

import pytest
from unittest.mock import patch, MagicMock


class TestNLTestCreation:
    """NL 测试用例创建测试"""

    def test_parse_nl_response_json(self, app):
        """解析单个用例 JSON"""
        with app.app_context():
            from app.utils.ai_copilot import _parse_nl_response
            content = '{"name": "test", "method": "GET", "url": "/api/test"}'
            result = _parse_nl_response(content)
            assert len(result) == 1
            assert result[0]["name"] == "test"

    def test_parse_nl_response_array(self, app):
        """解析用例数组 JSON"""
        with app.app_context():
            from app.utils.ai_copilot import _parse_nl_response
            content = '[{"name": "t1"}, {"name": "t2"}]'
            result = _parse_nl_response(content)
            assert len(result) == 2

    def test_parse_nl_response_codeblock(self, app):
        """解析带代码块的响应"""
        with app.app_context():
            from app.utils.ai_copilot import _parse_nl_response
            content = 'OK\n```json\n{"name": "test", "method": "POST"}\n```'
            result = _parse_nl_response(content)
            assert len(result) == 1

    def test_parse_nl_response_invalid(self, app):
        """无效 JSON 应返回空列表"""
        with app.app_context():
            from app.utils.ai_copilot import _parse_nl_response
            result = _parse_nl_response("not json")
            assert result == []
