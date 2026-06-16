"""
GraphQL 测试执行器

支持 GraphQL 协议的测试用例执行。
支持 Query、Mutation、Subscription。
"""

import json
import time
import requests
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)


class GraphQLTestCase:
    """GraphQL 测试用例"""

    def __init__(self, name: str = "", endpoint: str = "",
                 query: str = "", variables: Dict = None,
                 headers: Dict = None, operation_name: str = "",
                 timeout: int = 30, assertions: List[Dict] = None):
        self.name = name
        self.endpoint = endpoint
        self.query = query
        self.variables = variables or {}
        self.headers = headers or {}
        self.operation_name = operation_name
        self.timeout = timeout
        self.assertions = assertions or []

    def execute(self) -> Dict[str, Any]:
        """执行 GraphQL 请求"""
        start_time = time.time()
        try:
            payload = {"query": self.query}
            if self.variables:
                payload["variables"] = self.variables
            if self.operation_name:
                payload["operationName"] = self.operation_name

            headers = {"Content-Type": "application/json"}
            headers.update(self.headers)

            resp = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )

            duration = time.time() - start_time
            response_data = resp.json()

            passed = self._validate_response(resp.status_code, response_data)

            return {
                "passed": passed,
                "status_code": resp.status_code,
                "response": response_data,
                "duration_ms": round(duration * 1000, 2),
                "endpoint": self.endpoint,
            }

        except Exception as exc:
            duration = time.time() - start_time
            return {
                "passed": False,
                "error": str(exc),
                "error_type": "graphql_error",
                "duration_ms": round(duration * 1000, 2),
            }

    def _validate_response(self, status_code: int, response: Dict) -> bool:
        """验证 GraphQL 响应"""
        # GraphQL 错误在 body 中而非 HTTP 状态码
        if "errors" in response and not response.get("data"):
            return False

        for assertion in self.assertions:
            atype = assertion.get("type")
            if atype == "status_code":
                if status_code != assertion.get("expected"):
                    return False
            elif atype == "no_errors":
                if "errors" in response:
                    return False
            elif atype == "data_path":
                path = assertion.get("path", "").split(".")
                value = response.get("data", {})
                for key in path:
                    if isinstance(value, dict):
                        value = value.get(key)
                    else:
                        return False
                if assertion.get("expected") is not None and value != assertion.get("expected"):
                    return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name, "endpoint": self.endpoint,
            "query": self.query, "variables": self.variables,
            "headers": self.headers, "operation_name": self.operation_name,
            "timeout": self.timeout, "assertions": self.assertions,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphQLTestCase":
        return cls(**data)


class GraphQLExecutor:
    """GraphQL 测试执行器"""

    def execute_test(self, test_case: GraphQLTestCase) -> Dict[str, Any]:
        """执行 GraphQL 测试用例"""
        logger.info("执行 GraphQL 测试", endpoint=test_case.endpoint)
        return test_case.execute()

    def introspect_schema(self, endpoint: str, headers: Dict = None) -> Dict[str, Any]:
        """Schema 内省：获取 GraphQL schema"""
        introspection_query = """
            query IntrospectionQuery {
                __schema {
                    types {
                        name
                        kind
                        fields {
                            name
                            type { name kind }
                        }
                    }
                }
            }
        """
        try:
            resp = requests.post(
                endpoint,
                json={"query": introspection_query},
                headers=headers or {"Content-Type": "application/json"},
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"HTTP {resp.status_code}"}
        except Exception as exc:
            return {"error": str(exc)}


_instance = None


def get_graphql_executor() -> GraphQLExecutor:
    global _instance
    if _instance is None:
        _instance = GraphQLExecutor()
    return _instance