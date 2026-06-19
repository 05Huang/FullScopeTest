"""
可视化断言评估器单元测试
"""
import pytest
from app.utils.assertion_evaluator import AssertionEvaluator, get_assertion_evaluator


class TestAssertionEvaluator:
    def setup_method(self):
        self.evaluator = AssertionEvaluator()

    def test_empty_assertions(self):
        result = self.evaluator.evaluate([], {"status_code": 200})
        assert result["total"] == 0
        assert result["passed"] == 0
        assert result["details"] == []

    def test_status_code_equals_pass(self):
        result = self.evaluator.evaluate(
            [{"type": "status_code", "operator": "equals", "expected_value": 200}],
            {"status_code": 200})
        assert result["total"] == 1
        assert result["passed"] == 1
        assert result["details"][0]["passed"] is True

    def test_status_code_equals_fail(self):
        result = self.evaluator.evaluate(
            [{"type": "status_code", "operator": "equals", "expected_value": 200}],
            {"status_code": 404})
        assert result["passed"] == 0
        assert result["failed"] == 1
        assert result["details"][0]["actual"] == 404

    def test_response_time_less_than_pass(self):
        result = self.evaluator.evaluate(
            [{"type": "response_time", "operator": "less_than", "expected_value": 1000}],
            {"response_time": 500})
        assert result["details"][0]["passed"] is True

    def test_header_exists(self):
        result = self.evaluator.evaluate(
            [{"type": "header", "header_name": "content-type", "operator": "exists"}],
            {"headers": {"content-type": "application/json"}})
        assert result["details"][0]["passed"] is True

    def test_body_equals(self):
        result = self.evaluator.evaluate(
            [{"type": "body", "body_path": "status", "operator": "equals", "expected_value": "ok"}],
            {"body": {"status": "ok"}})
        assert result["details"][0]["passed"] is True

    def test_body_contains(self):
        result = self.evaluator.evaluate(
            [{"type": "body", "body_path": "msg", "operator": "contains", "expected_value": "success"}],
            {"body": {"msg": "operation success"}})
        assert result["details"][0]["passed"] is True

    def test_body_nested_path(self):
        result = self.evaluator.evaluate(
            [{"type": "body", "body_path": "data.items[0].id", "operator": "equals", "expected_value": "123"}],
            {"body": {"data": {"items": [{"id": "123"}]}}})
        assert result["details"][0]["passed"] is True

    def test_multiple_assertions(self):
        result = self.evaluator.evaluate([
            {"type": "status_code", "operator": "equals", "expected_value": 200},
            {"type": "response_time", "operator": "less_than", "expected_value": 2000},
            {"type": "body", "body_path": "success", "operator": "type_is", "expected_value": "boolean"},
        ], {"status_code": 200, "response_time": 500, "body": {"success": True}})
        assert result["total"] == 3
        assert result["passed"] == 3

    def test_unknown_type(self):
        result = self.evaluator.evaluate(
            [{"type": "unknown", "operator": "equals", "expected_value": 1}],
            {"status_code": 200})
        assert result["details"][0]["passed"] is False

    def test_singleton(self):
        e = get_assertion_evaluator()
        assert isinstance(e, AssertionEvaluator)
        assert get_assertion_evaluator() is e
