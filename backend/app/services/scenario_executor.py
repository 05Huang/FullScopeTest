"""
场景编排执行器

支持多步骤链式请求编排：
- 按步骤顺序执行 HTTP 请求
- 步骤间变量提取（从响应 Body/Header 提取值传给下一步）
- 条件分支（根据上一步结果决定下一步执行路径）
"""

import json
import re
import time
import requests
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from .base import BaseService
from ..extensions import db
from ..utils.url_safety import is_safe_url
from ..utils.env_variables import replace_variables, replace_variables_in_dict
from ..utils.assertion_evaluator import get_assertion_evaluator


class ScenarioStep:
    """场景步骤定义"""

    def __init__(self, step_data: dict):
        self.id = step_data.get("id", "")
        self.name = step_data.get("name", "未命名步骤")
        self.method = step_data.get("method", "GET").upper()
        self.url = step_data.get("url", "")
        self.headers = step_data.get("headers", {}) or {}
        self.params = step_data.get("params", {}) or {}
        self.body = step_data.get("body")
        self.body_type = step_data.get("body_type", "json")
        self.timeout = step_data.get("timeout", 30)
        # 变量提取规则
        self.extractors = step_data.get("extractors", [])
        # 断言规则
        self.assertions = step_data.get("assertions", [])
        # 条件分支
        self.condition = step_data.get("condition")
        self.on_success = step_data.get("on_success")  # 成功后跳转的步骤 ID
        self.on_failure = step_data.get("on_failure")  # 失败后跳转的步骤 ID
        # 步骤间延迟
        self.delay_ms = step_data.get("delay_ms", 0)



class ScenarioExecutor(BaseService):
    """场景编排执行器 — 按步骤顺序执行链式请求"""

    def execute_scenario(self, steps_data: List[dict], context: dict) -> dict:
        """
        执行完整的场景

        Args:
            steps_data: 步骤定义列表
            context: { env_vars, user_id, base_url }

        Returns:
            { total, passed, failed, duration, step_results, variables }
        """
        steps = [ScenarioStep(s) for s in steps_data]
        env_vars = context.get("env_vars", {})
        base_url = context.get("base_url", "")

        # 步骤间共享变量上下文
        variables: Dict[str, Any] = dict(context.get("variables", {}))
        step_results: List[dict] = []
        step_map = {s.id: s for s in steps}

        total_passed = 0
        total_failed = 0
        start_time = time.time()

        # 按顺序遍历步骤
        step_index = 0
        max_iterations = len(steps) * 3  # 防止无限循环
        iteration = 0

        while step_index < len(steps) and iteration < max_iterations:
            iteration += 1
            step = steps[step_index]

            # 步骤间延迟
            if step.delay_ms > 0 and step_results:
                time.sleep(step.delay_ms / 1000.0)

            # 检查条件分支
            if step.condition and step_results:
                should_execute = self._evaluate_condition(step.condition, variables, step_results[-1])
                if not should_execute:
                    step_results.append({
                        "step_id": step.id, "name": step.name, "skipped": True,
                        "reason": "条件不满足", "duration": 0
                    })
                    step_index += 1
                    continue

            # 执行步骤
            result = self._execute_step(step, env_vars, variables, base_url)
            step_results.append(result)

            if result["passed"]:
                total_passed += 1
            else:
                total_failed += 1

            # 提取变量
            if result["success"] and step.extractors:
                extracted = self._extract_variables(step.extractors, result)
                variables.update(extracted)

            # 条件分支跳转
            next_step_id = None
            if step.on_success and result["passed"]:
                next_step_id = step.on_success
            elif step.on_failure and not result["passed"]:
                next_step_id = step.on_failure

            if next_step_id and next_step_id in step_map:
                # 跳转到指定步骤
                target_index = next((i for i, s in enumerate(steps) if s.id == next_step_id), None)
                if target_index is not None:
                    step_index = target_index
                    continue

            step_index += 1

        total_duration = time.time() - start_time

        return {
            "total": len(step_results),
            "passed": total_passed,
            "failed": total_failed,
            "duration": round(total_duration, 2),
            "step_results": step_results,
            "variables": variables,
        }

    def _execute_step(self, step: ScenarioStep, env_vars: dict, variables: dict, base_url: str) -> dict:
        """执行单个步骤"""
        step_start = time.time()

        try:
            url = step.url
            headers = dict(step.headers)
            params = dict(step.params)
            body = step.body

            # 应用变量替换
            all_vars = {**env_vars, **variables}
            if all_vars:
                url = replace_variables(url, all_vars)
                headers = replace_variables_in_dict(headers, all_vars)
                params = replace_variables_in_dict(params, all_vars)
                if isinstance(body, dict):
                    body = replace_variables_in_dict(body, all_vars)
                elif isinstance(body, str):
                    body = replace_variables(body, all_vars)

            # 补全 base_url
            if base_url and not url.startswith(("http://", "https://")):
                url = base_url.rstrip("/") + "/" + url.lstrip("/")

            # SSRF 防护
            safe, reason = is_safe_url(url)
            if not safe:
                elapsed = (time.time() - step_start) * 1000
                return {
                    "step_id": step.id, "name": step.name, "success": False,
                    "passed": False, "error": reason, "duration": round(elapsed, 2)
                }

            # 发送请求
            request_kwargs = {
                "method": step.method, "url": url, "headers": headers,
                "params": params, "timeout": step.timeout,
                "verify": False, "allow_redirects": True
            }
            if body and step.method in ["POST", "PUT", "PATCH"]:
                if step.body_type == "json":
                    request_kwargs["json"] = body
                else:
                    request_kwargs["data"] = body

            response = requests.request(**request_kwargs)
            elapsed = (time.time() - step_start) * 1000

            try:
                response_body = response.json()
            except Exception:
                response_body = response.text

            # 执行断言
            passed = response.status_code < 400
            assertion_result = None
            if step.assertions:
                try:
                    evaluator = get_assertion_evaluator()
                    assertion_result = evaluator.evaluate(step.assertions, {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "body": response_body,
                        "response_time": round(elapsed, 2),
                    })
                    passed = assertion_result["failed"] == 0
                except Exception as e:
                    self.logger.error("步骤断言执行异常", step_id=step.id, error=str(e))

            return {
                "step_id": step.id, "name": step.name, "success": True,
                "passed": passed, "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response_body,
                "response_time": round(elapsed, 2),
                "assertions": assertion_result,
                "duration": round(elapsed, 2),
            }

        except Exception as e:
            elapsed = (time.time() - step_start) * 1000
            self.logger.error("步骤执行失败", step_id=step.id, error=str(e))
            return {
                "step_id": step.id, "name": step.name, "success": False,
                "passed": False, "error": str(e),
                "duration": round(elapsed, 2),
            }

    def _extract_variables(self, extractors: List[dict], result: dict) -> dict:
        """
        从响应中提取变量

        提取规则格式：
            { name: "token", source: "body", path: "data.access_token" }
            { name: "status", source: "status_code" }
            { name: "content_type", source: "header", path: "content-type" }
        """
        extracted = {}
        for extractor in extractors:
            name = extractor.get("name", "")
            source = extractor.get("source", "body")
            path = extractor.get("path", "")
            if not name:
                continue

            try:
                if source == "body":
                    value = self._extract_from_body(result.get("body"), path)
                elif source == "header":
                    headers = result.get("headers", {})
                    value = headers.get(path.lower()) or headers.get(path)
                elif source == "status_code":
                    value = result.get("status_code")
                elif source == "response_time":
                    value = result.get("response_time")
                else:
                    value = None

                if value is not None:
                    extracted[name] = value
                    self.logger.debug("提取变量", name=name, source=source, value=str(value)[:100])
            except Exception as e:
                self.logger.warning("变量提取失败", name=name, error=str(e))

        return extracted

    def _extract_from_body(self, body: Any, path: str) -> Any:
        """从响应体中提取值（与 assertion_evaluator 相同的 JSONPath 逻辑）"""
        if not path or body is None:
            return body
        current = body
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

    def _evaluate_condition(self, condition: dict, variables: dict, last_result: dict) -> bool:
        """
        评估条件表达式

        条件格式：
            { type: "status", operator: "equals", value: 200 }
            { type: "variable", name: "token", operator: "exists" }
            { type: "last_passed", value: true }
        """
        ctype = condition.get("type", "")
        operator = condition.get("operator", "equals")
        expected = condition.get("value")

        if ctype == "status":
            actual = last_result.get("status_code")
            return self._compare(actual, expected, operator)
        elif ctype == "variable":
            var_name = condition.get("name", "")
            actual = variables.get(var_name)
            if operator == "exists":
                return actual is not None
            elif operator == "not_exists":
                return actual is None
            return self._compare(actual, expected, operator)
        elif ctype == "last_passed":
            return last_result.get("passed", False) == bool(expected)

        return True  # 未知条件默认执行

    def _compare(self, actual, expected, operator: str) -> bool:
        """简单值比较"""
        try:
            if operator == "equals": return str(actual) == str(expected)
            if operator == "not_equals": return str(actual) != str(expected)
            if operator == "greater_than": return float(actual) > float(expected)
            if operator == "less_than": return float(actual) < float(expected)
            if operator == "contains": return str(expected) in str(actual)
            if operator == "exists": return actual is not None
        except (TypeError, ValueError):
            return False
        return False


# 模块级单例
_executor = None


def get_scenario_executor() -> ScenarioExecutor:
    """获取场景执行器单例"""
    global _executor
    if _executor is None:
        _executor = ScenarioExecutor()
    return _executor
