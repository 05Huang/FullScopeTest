"""
FullScopeTest API 客户端

支持 API Token 和 JWT 两种认证方式，自动重试和超时处理。

用法：
    # API Token 认证
    client = FullScopeTestClient(base_url="http://localhost:8000", api_token="your-token")

    # JWT 认证
    client = FullScopeTestClient(base_url="http://localhost:8000", jwt_token="your-jwt")

    # 创建测试运行
    run = client.create_test_run(project_id=1, test_type="api")
"""
import time
import requests
from typing import Any, Dict, List, Optional


class FullScopeTestClient:
    """
    FullScopeTest API 客户端

    Args:
        base_url: API 基础 URL（如 http://localhost:8000）
        api_token: API Token（与 jwt_token 二选一）
        jwt_token: JWT Token（与 api_token 二选一）
        timeout: 请求超时时间（秒，默认 30）
        max_retries: 最大重试次数（默认 3）
        retry_delay: 重试间隔（秒，默认 1）
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_token: str = None,
        jwt_token: str = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._session = requests.Session()

        # 设置认证头
        if api_token:
            self._session.headers["Authorization"] = f"Bearer {api_token}"
        elif jwt_token:
            self._session.headers["Authorization"] = f"Bearer {jwt_token}"
        else:
            raise ValueError("必须提供 api_token 或 jwt_token")

        self._session.headers["Content-Type"] = "application/json"

    # ── 项目管理 ──────────────────────────────────────────────────────────────

    def list_projects(self, page: int = 1, per_page: int = 20) -> dict:
        """获取项目列表"""
        return self._get("/api/v1/projects", params={"page": page, "per_page": per_page})

    def create_project(self, name: str, description: str = "") -> dict:
        """创建项目"""
        return self._post("/api/v1/projects", json={"name": name, "description": description})

    def get_project(self, project_id: int) -> dict:
        """获取项目详情"""
        return self._get(f"/api/v1/projects/{project_id}")

    # ── 测试用例 ──────────────────────────────────────────────────────────────

    def list_test_cases(self, project_id: int = None, collection_id: int = None) -> dict:
        """获取测试用例列表"""
        params = {}
        if project_id:
            params["project_id"] = project_id
        if collection_id:
            params["collection_id"] = collection_id
        return self._get("/api/v1/api-test/cases", params=params)

    def create_test_case(
        self,
        project_id: int,
        name: str,
        method: str = "GET",
        url: str = "",
        headers: dict = None,
        body: dict = None,
        collection_id: int = None,
    ) -> dict:
        """创建测试用例"""
        data = {
            "project_id": project_id,
            "name": name,
            "method": method,
            "url": url,
        }
        if headers:
            data["headers"] = headers
        if body:
            data["body"] = body
        if collection_id:
            data["collection_id"] = collection_id
        return self._post("/api/v1/api-test/cases", json=data)

    def get_test_case(self, case_id: int) -> dict:
        """获取测试用例详情"""
        return self._get(f"/api/v1/api-test/cases/{case_id}")

    def update_test_case(self, case_id: int, **kwargs) -> dict:
        """更新测试用例"""
        return self._put(f"/api/v1/api-test/cases/{case_id}", json=kwargs)

    def delete_test_case(self, case_id: int) -> dict:
        """删除测试用例"""
        return self._delete(f"/api/v1/api-test/cases/{case_id}")

    # ── 测试执行 ──────────────────────────────────────────────────────────────

    def list_test_runs(self, project_id: int = None, test_type: str = None, page: int = 1) -> dict:
        """获取测试执行记录列表"""
        params = {"page": page}
        if project_id:
            params["project_id"] = project_id
        if test_type:
            params["test_type"] = test_type
        return self._get("/api/v1/test-runs", params=params)

    def create_test_run(self, project_id: int, test_type: str = "api", test_object_name: str = None) -> dict:
        """创建测试执行记录"""
        data = {"project_id": project_id, "test_type": test_type}
        if test_object_name:
            data["test_object_name"] = test_object_name
        return self._post("/api/v1/test-runs", json=data)

    def get_test_run(self, run_id: int) -> dict:
        """获取测试执行详情"""
        return self._get(f"/api/v1/test-runs/{run_id}")

    # ── 测试计划 ──────────────────────────────────────────────────────────────

    def list_test_plans(self, project_id: int, page: int = 1) -> dict:
        """获取测试计划列表"""
        return self._get("/api/v1/test-plans", params={"project_id": project_id, "page": page})

    def create_test_plan(self, project_id: int, name: str, include_cases: list = None, tags: list = None) -> dict:
        """创建测试计划"""
        data = {"project_id": project_id, "name": name}
        if include_cases:
            data["include_cases"] = include_cases
        if tags:
            data["tags"] = tags
        return self._post("/api/v1/test-plans", json=data)

    def create_test_plan_run(self, plan_id: int) -> dict:
        """从测试计划创建执行轮次"""
        return self._post(f"/api/v1/test-plans/{plan_id}/runs", json={})

    # ── 报告 ──────────────────────────────────────────────────────────────────

    def get_report_statistics(self, project_id: int = None, days: int = 7) -> dict:
        """获取报告统计"""
        params = {"days": days}
        if project_id:
            params["project_id"] = project_id
        return self._get("/api/v1/reports/statistics", params=params)

    def get_quality_trend(self, project_id: int = None, days: int = 30, granularity: str = "week") -> dict:
        """获取质量趋势"""
        params = {"days": days, "granularity": granularity}
        if project_id:
            params["project_id"] = project_id
        return self._get("/api/v1/reports/trend", params=params)

    def get_team_metrics(self, project_id: int = None, days: int = 30) -> dict:
        """获取团队效能度量"""
        params = {"days": days}
        if project_id:
            params["project_id"] = project_id
        return self._get("/api/v1/reports/team-metrics", params=params)

    # ── 批量操作 ──────────────────────────────────────────────────────────────

    def import_postman(self, project_id: int, content: str) -> dict:
        """导入 Postman Collection"""
        return self._post("/api/v1/api-test/import/postman", json={
            "project_id": project_id, "content": content,
        })

    def import_csv(self, project_id: int, content: str) -> dict:
        """导入 CSV 用例"""
        return self._post("/api/v1/api-test/import/csv", json={
            "project_id": project_id, "content": content,
        })

    def get_csv_template(self) -> str:
        """获取 CSV 导入模板"""
        resp = self._get("/api/v1/api-test/import/template")
        return resp.get("data", {}).get("template", "")

    # ── 评论 ──────────────────────────────────────────────────────────────────

    def create_comment(self, resource_type: str, resource_id: int, content: str) -> dict:
        """创建评论"""
        return self._post("/api/v1/comments", json={
            "resource_type": resource_type, "resource_id": resource_id, "content": content,
        })

    def list_comments(self, resource_type: str, resource_id: int) -> dict:
        """获取评论列表"""
        return self._get(f"/api/v1/comments/{resource_type}/{resource_id}")

    # ── 内部方法 ──────────────────────────────────────────────────────────────

    def _get(self, path: str, params: dict = None) -> dict:
        return self._request("GET", path, params=params)

    def _post(self, path: str, json: dict = None) -> dict:
        return self._request("POST", path, json=json)

    def _put(self, path: str, json: dict = None) -> dict:
        return self._request("PUT", path, json=json)

    def _delete(self, path: str) -> dict:
        return self._request("DELETE", path)

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """
        发送 HTTP 请求（带自动重试）
        """
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = self._session.request(method, url, **kwargs)
                if resp.status_code >= 500 and attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as exc:
                last_error = exc
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))

        raise last_error