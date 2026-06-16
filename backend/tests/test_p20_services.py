"""
P20 开发者体验测试（CLI 格式化 + SDK）
"""

import pytest
import json


class TestFormatters:
    """CLI 格式化工具测试"""

    def test_format_text_dict(self, app):
        """格式化字典为文本"""
        with app.app_context():
            import sys
            sys.path.insert(0, "../sdk/python")
            from fullscopetest.formatters import format_output
            data = {"name": "test", "status": "passed"}
            result = format_output(data, fmt="text")
            assert "name: test" in result
            assert "status: passed" in result

    def test_format_json_dict(self, app):
        """格式化字典为 JSON"""
        with app.app_context():
            import sys
            sys.path.insert(0, "../sdk/python")
            from fullscopetest.formatters import format_output
            data = {"name": "test", "count": 5}
            result = format_output(data, fmt="json")
            parsed = json.loads(result)
            assert parsed["name"] == "test"
            assert parsed["count"] == 5

    def test_format_text_list(self, app):
        """格式化列表为文本"""
        with app.app_context():
            import sys
            sys.path.insert(0, "../sdk/python")
            from fullscopetest.formatters import format_output
            data = [{"name": "case1"}, {"name": "case2"}]
            result = format_output(data, fmt="text")
            assert "case1" in result
            assert "case2" in result

    def test_format_with_title(self, app):
        """带标题的格式化"""
        with app.app_context():
            import sys
            sys.path.insert(0, "../sdk/python")
            from fullscopetest.formatters import format_output
            result = format_output({"key": "val"}, fmt="text", title="Test Title")
            assert "Test Title" in result
