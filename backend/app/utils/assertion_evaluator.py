"""
可视化断言评估器

支持的断言类型：
- status_code: 状态码断言（等于/不等于/属于范围）
- response_time: 响应时间断言（小于/大于 N ms）
- header: 响应头断言（存在/不存在/值匹配）
- body: 响应体断言（JSONPath 提取 + 等于/包含/正则/类型检查）
"""

import re
from typing import Any, Dict, List, Optional


class AssertionResult:
    """单条断言结果"""

    def __init__(self, name: str, passed: bool, actual: Any = None,
                 expected: Any = None, error: str = None, assertion_type: str = None):
        self.name = name
        self.passed = passed
        self.actual = actual
        self.expected = expected
        self.error = error
        self.assertion_type = assertion_type

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "actual": self.actual,
            "expected": self.expected,
            "error": self.error,
            "assertion_type": self.assertion_type,
        }


class AssertionEvaluator:
    """断言评估器 — 在请求执行后评估所有可视化断言"""

    def evaluate(self, assertions: List[dict], response_data: dict) -> dict:
        """评估所有断言"""
        if not assertions:
            return {"total": 0, "passed": 0, "failed": 0, "details": []}

        results: List[AssertionResult] = []
        for assertion in assertions:
            try:
                result = self._evaluate_single(assertion, response_data)
            except Exception as e:
                result = AssertionResult(
                    name=assertion.get("description") or assertion.get("type", "unknown"),
                    passed=False,
                    error=f"断言执行异常: {str(e)}",
                    assertion_type=assertion.get("type")
                )
            results.append(result)

        passed_count = sum(1 for r in results if r.passed)
        failed_count = len(results) - passed_count

        return {
            "total": len(results),
            "passed": passed_count,
            "failed": failed_count,
            "details": [r.to_dict() for r in results]
        }

    def _evaluate_single(self, assertion: dict, response_data: dict) -> AssertionResult:
        """评估单条断言"""
        atype = assertion.get("type", "")
        description = assertion.get("description") or atype

        if atype == "status_code":
            return self._eval_status_code(assertion, response_data, description)
        elif atype == "response_time":
            return self._eval_response_time(assertion, response_data, description)
        elif atype == "header":
            return self._eval_header(assertion, response_data, description)
        elif atype == "body":
            return self._eval_body(assertion, response_data, description)
        else:
            return AssertionResult(name=description, passed=False,
                error=f"未知的断言类型: {atype}", assertion_type=atype)

    def _eval_status_code(self, assertion, response_data, description):
        """评估状态码断言"""
        operator = assertion.get("operator", "equals")
        expected = assertion.get("expected_value", 200)
        actual = response_data.get("status_code")
        if actual is None:
            return AssertionResult(name=description, passed=False, actual=None, expected=expected,
                error="响应中未包含状态码", assertion_type="status_code")
        passed = self._compare_numeric(actual, expected, operator)
        return AssertionResult(name=description, passed=passed, actual=actual, expected=expected, assertion_type="status_code")

    def _eval_response_time(self, assertion, response_data, description):
        """评估响应时间断言（单位：毫秒）"""
        operator = assertion.get("operator", "less_than")
        expected = assertion.get("expected_value", 1000)
        actual = response_data.get("response_time")
        if actual is None:
            return AssertionResult(name=description, passed=False, actual=None, expected=expected,
                error="响应中未包含耗时信息", assertion_type="response_time")
        passed = self._compare_numeric(actual, expected, operator)
        return AssertionResult(name=description, passed=passed, actual=actual, expected=expected, assertion_type="response_time")

    def _eval_header(self, assertion, response_data, description):
        """评估响应头断言"""
        header_name = assertion.get("header_name", "")
        operator = assertion.get("operator", "exists")
        expected = assertion.get("expected_value")
        headers = response_data.get("headers", {}) or {}
        actual = headers.get(header_name.lower()) or headers.get(header_name)
        if operator == "exists":
            exists = header_name.lower() in {k.lower() for k in headers}
            return AssertionResult(name=description, passed=exists,
                actual=header_name if exists else None, expected=f"Header {header_name} 存在", assertion_type="header")
        elif operator == "not_exists":
            exists = header_name.lower() in {k.lower() for k in headers}
            return AssertionResult(name=description, passed=not exists,
                actual=header_name if exists else None, expected=f"Header {header_name} 不存在", assertion_type="header")
        elif operator == "equals":
            passed = actual is not None and str(actual) == str(expected)
            return AssertionResult(name=description, passed=passed, actual=actual, expected=expected, assertion_type="header")
        elif operator == "contains":
            passed = actual is not None and str(expected) in str(actual)
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"包含 '{expected}'", assertion_type="header")
        return AssertionResult(name=description, passed=False, error=f"未知的 Header 操作符: {operator}", assertion_type="header")

    def _eval_body(self, assertion, response_data, description):
        """评估响应体断言（JSONPath 提取 + 条件比较）"""
        body_path = assertion.get("body_path", "")
        operator = assertion.get("operator", "equals")
        expected = assertion.get("expected_value")
        body = response_data.get("body")
        actual = self._extract_value(body, body_path) if body_path else body

        if operator == "exists":
            exists = actual is not None
            return AssertionResult(name=description, passed=exists,
                actual=actual if exists else None, expected=f"路径 {body_path} 存在", assertion_type="body")
        elif operator == "not_exists":
            exists = actual is not None
            return AssertionResult(name=description, passed=not exists,
                actual=actual if exists else None, expected=f"路径 {body_path} 不存在", assertion_type="body")
        elif operator == "equals":
            passed = str(actual) == str(expected)
            return AssertionResult(name=description, passed=passed, actual=actual, expected=expected, assertion_type="body")
        elif operator == "not_equals":
            passed = str(actual) != str(expected)
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"不等于 {expected}", assertion_type="body")
        elif operator == "contains":
            passed = (expected is not None and str(expected) in str(actual)) if actual is not None else False
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"包含 '{expected}'", assertion_type="body")
        elif operator == "not_contains":
            passed = str(expected) not in str(actual) if actual is not None else True
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"不包含 '{expected}'", assertion_type="body")
        elif operator == "regex":
            try:
                passed = re.search(str(expected), str(actual)) is not None if actual is not None else False
            except re.error as e:
                return AssertionResult(name=description, passed=False, error=f"正则表达式错误: {str(e)}", assertion_type="body")
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"正则匹配", assertion_type="body")
        elif operator == "type_is":
            type_map = {"string": str, "number": (int, float), "boolean": bool, "array": list, "object": dict, "null": type(None)}
            expected_type = type_map.get(str(expected).lower())
            if expected_type is None:
                return AssertionResult(name=description, passed=False, error=f"未知类型: {expected}", assertion_type="body")
            passed = isinstance(actual, expected_type) if actual is not None else (expected == "null")
            return AssertionResult(name=description, passed=passed, actual=type(actual).__name__, expected=expected, assertion_type="body")
        elif operator == "greater_than":
            passed = self._compare_numeric(actual, expected, "greater_than")
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"> {expected}", assertion_type="body")
        elif operator == "less_than":
            passed = self._compare_numeric(actual, expected, "less_than")
            return AssertionResult(name=description, passed=passed, actual=actual, expected=f"< {expected}", assertion_type="body")
        elif operator == "length_equals":
            actual_len = len(actual) if actual is not None else 0
            passed = actual_len == int(expected) if expected is not None else False
            return AssertionResult(name=description, passed=passed, actual=actual_len, expected=f"长度 = {expected}", assertion_type="body")
        elif operator == "is_empty":
            passed = not actual if actual is not None else True
            return AssertionResult(name=description, passed=passed, actual=actual, expected="为空", assertion_type="body")
        elif operator == "is_not_empty":
            passed = bool(actual) if actual is not None else False
            return AssertionResult(name=description, passed=passed, actual=actual, expected="不为空", assertion_type="body")
        return AssertionResult(name=description, passed=False, error=f"未知的操作符: {operator}", assertion_type="body")

    # ========== 工具方法 ==========

    def _compare_numeric(self, actual, expected, operator: str) -> bool:
        """数值比较"""
        try:
            a = float(actual)
            e = float(expected)
        except (TypeError, ValueError):
            return False
        ops = {
            "equals": lambda a, e: a == e,
            "not_equals": lambda a, e: a != e,
            "greater_than": lambda a, e: a > e,
            "greater_than_or_equals": lambda a, e: a >= e,
            "less_than": lambda a, e: a < e,
            "less_than_or_equals": lambda a, e: a <= e,
        }
        fn = ops.get(operator)
        return fn(a, e) if fn else False

    def _extract_value(self, data: Any, path: str) -> Any:
        """
        从响应体中提取值，支持简单的 JSONPath 风格路径。
        示例：data.name, data[0], data.items[0].id
        """
        if not path or not data:
            return data
        current = data
        tokens = re.findall(r'([^\.\[\]]+)|\[(\d+)\]', path)
        for name_token, index_token in tokens:
            if current is None:
                return None
            if index_token:
                idx = int(index_token)
                if isinstance(current, list) and 0 <= idx < len(current):
                    current = current[idx]
                else:
                    return None
            elif name_token:
                if isinstance(current, dict) and name_token in current:
                    current = current[name_token]
                else:
                    return None
        return current


# 模块级单例
_evaluator = None


def get_assertion_evaluator() -> AssertionEvaluator:
    """获取断言评估器单例"""
    global _evaluator
    if _evaluator is None:
        _evaluator = AssertionEvaluator()
    return _evaluator
