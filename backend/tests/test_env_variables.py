"""
环境变量工具测试

覆盖：变量替换、字典替换、变量提取
"""

from app.utils.env_variables import (
    replace_variables,
    replace_variables_in_dict,
    extract_variables,
)


class TestReplaceVariables:
    """变量替换测试"""

    def test_simple_replacement(self):
        """简单变量替换"""
        result = replace_variables(
            "http://api.com/{{version}}/user",
            {"version": "v1"},
        )
        assert result == "http://api.com/v1/user"

    def test_multiple_variables(self):
        """多个变量替换"""
        result = replace_variables(
            "http://{{host}}/{{version}}/{{resource}}",
            {"host": "api.example.com", "version": "v2", "resource": "users"},
        )
        assert result == "http://api.example.com/v2/users"

    def test_missing_variable_keeps_original(self):
        """缺失的变量保持原样"""
        result = replace_variables(
            "http://api.com/{{version}}/{{missing}}",
            {"version": "v1"},
        )
        assert result == "http://api.com/v1/{{missing}}"

    def test_empty_text(self):
        """空文本返回空"""
        assert replace_variables("", {"key": "value"}) == ""

    def test_none_text(self):
        """None 返回 None"""
        assert replace_variables(None, {"key": "value"}) is None

    def test_empty_variables(self):
        """空变量字典返回原文本"""
        text = "http://api.com/{{version}}"
        assert replace_variables(text, {}) == text

    def test_none_variables(self):
        """None 变量字典返回原文本"""
        text = "http://api.com/{{version}}"
        assert replace_variables(text, None) == text

    def test_whitespace_in_variable_name(self):
        """变量名中的空格应该被去除"""
        result = replace_variables(
            "http://api.com/{{ version }}",
            {"version": "v1"},
        )
        assert result == "http://api.com/v1"

    def test_non_string_variable_value(self):
        """非字符串变量值应该被转换为字符串"""
        result = replace_variables(
            "count: {{count}}",
            {"count": 42},
        )
        assert result == "count: 42"

    def test_no_variables_in_text(self):
        """没有变量的文本应该原样返回"""
        text = "http://api.com/v1/users"
        assert replace_variables(text, {"key": "value"}) == text


class TestReplaceVariablesInDict:
    """字典变量替换测试"""

    def test_simple_dict(self):
        """简单字典替换"""
        data = {
            "url": "http://{{host}}/api",
            "method": "GET",
        }
        result = replace_variables_in_dict(data, {"host": "example.com"})
        assert result["url"] == "http://example.com/api"
        assert result["method"] == "GET"

    def test_nested_dict(self):
        """嵌套字典替换"""
        data = {
            "request": {
                "url": "http://{{host}}/api",
                "headers": {
                    "Authorization": "Bearer {{token}}",
                },
            },
        }
        result = replace_variables_in_dict(data, {"host": "example.com", "token": "abc123"})
        assert result["request"]["url"] == "http://example.com/api"
        assert result["request"]["headers"]["Authorization"] == "Bearer abc123"

    def test_list_in_dict(self):
        """字典中的列表替换"""
        data = {
            "urls": ["http://{{host}}/a", "http://{{host}}/b"],
        }
        result = replace_variables_in_dict(data, {"host": "example.com"})
        assert result["urls"] == ["http://example.com/a", "http://example.com/b"]

    def test_empty_dict(self):
        """空字典返回空字典"""
        assert replace_variables_in_dict({}, {"key": "value"}) == {}

    def test_none_dict(self):
        """None 返回 None"""
        assert replace_variables_in_dict(None, {"key": "value"}) is None


class TestExtractVariables:
    """变量提取测试"""

    def test_extract_single(self):
        """提取单个变量"""
        result = extract_variables("http://api.com/{{version}}/user")
        assert result == ["version"]

    def test_extract_multiple(self):
        """提取多个变量"""
        result = extract_variables("http://{{host}}/{{version}}/{{resource}}")
        assert result == ["host", "version", "resource"]

    def test_extract_empty_text(self):
        """空文本返回空列表"""
        assert extract_variables("") == []

    def test_extract_none_text(self):
        """None 返回空列表"""
        assert extract_variables(None) == []

    def test_extract_no_variables(self):
        """没有变量返回空列表"""
        assert extract_variables("http://api.com/v1/users") == []

    def test_extract_duplicate_variables(self):
        """重复变量应该全部提取"""
        result = extract_variables("http://{{host}}/{{host}}/api")
        assert result == ["host", "host"]
