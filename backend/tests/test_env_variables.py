"""
环境变量注入测试
"""

import pytest


class TestEnvVariables:
    """环境变量工具测试"""

    def test_replace_simple_variable(self, app):
        """简单变量替换"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables("{{url}}/users", {"url": "http://api.com"})
            assert result == "http://api.com/users"

    def test_replace_multiple_variables(self, app):
        """多变量替换"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables(
                "{{base_url}}/{{version}}/users/{{id}}",
                {"base_url": "http://api.com", "version": "v1", "id": "123"}
            )
            assert result == "http://api.com/v1/users/123"

    def test_builtin_timestamp(self, app):
        """内置时间戳变量"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables("{{$timestamp}}", {})
            assert result.isdigit()
            assert len(result) >= 10

    def test_builtin_uuid(self, app):
        """内置 UUID 变量"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables("{{$uuid}}", {})
            assert len(result) == 36  # UUID 格式
            assert "-" in result

    def test_builtin_random_int(self, app):
        """内置随机数变量"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables("{{$random_int}}", {})
            assert result.isdigit()
            assert len(result) == 6

    def test_variable_not_found_keeps_original(self, app):
        """未找到的变量保持原样"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables("{{unknown}}", {})
            assert result == "{{unknown}}"

    def test_replace_in_dict(self, app):
        """字典中的变量替换"""
        with app.app_context():
            from app.utils.env_variables import replace_variables_in_dict
            data = {"url": "{{base}}/api", "headers": {"Authorization": "Bearer {{token}}"}}
            result = replace_variables_in_dict(data, {"base": "http://api.com", "token": "abc123"})
            assert result["url"] == "http://api.com/api"
            assert result["headers"]["Authorization"] == "Bearer abc123"

    def test_extract_variables(self, app):
        """提取变量名"""
        with app.app_context():
            from app.utils.env_variables import extract_variables
            vars = extract_variables("{{url}}/{{id}}/test")
            assert "url" in vars
            assert "id" in vars

    def test_no_variables_returns_original(self, app):
        """无变量时返回原文"""
        with app.app_context():
            from app.utils.env_variables import replace_variables
            result = replace_variables("no variables here", {"key": "value"})
            assert result == "no variables here"
