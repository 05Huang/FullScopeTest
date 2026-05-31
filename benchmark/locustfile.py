"""
FullScopeTest 性能基准测试

使用 Locust 对 Flask (v1) 和 FastAPI (v2) 接口进行性能对比测试
"""

import json
import random
import string
from locust import HttpUser, task, between, events


class FlaskAPIUser(HttpUser):
    """Flask v1 API 用户模拟"""
    wait_time = between(1, 3)
    weight = 1

    def on_start(self):
        """用户启动时注册并登录"""
        self.username = f"flask_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
        self.email = f"{self.username}@benchmark.test"
        self.password = "Benchmark123!"
        self.access_token = None

        register_resp = self.client.post("/api/v1/auth/register", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })

        if register_resp.status_code == 201:
            login_resp = self.client.post("/api/v1/auth/login", json={
                "username": self.username,
                "password": self.password
            })
            if login_resp.status_code == 200:
                data = login_resp.json()
                self.access_token = data.get("data", {}).get("access_token")

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    @task(10)
    def health_check(self):
        self.client.get("/api/v1/health")

    @task(8)
    def get_current_user(self):
        if self.access_token:
            self.client.get("/api/v1/auth/me", headers=self._get_headers())

    @task(5)
    def get_projects(self):
        if self.access_token:
            self.client.get("/api/v1/projects?page=1&per_page=10", headers=self._get_headers())

    @task(3)
    def create_project(self):
        if self.access_token:
            project_name = f"BenchmarkProject_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            self.client.post("/api/v1/projects", json={
                "name": project_name,
                "description": "性能基准测试项目"
            }, headers=self._get_headers())

    @task(4)
    def get_environments(self):
        if self.access_token:
            self.client.get("/api/v1/environments?page=1&per_page=10", headers=self._get_headers())


class FastAPIUser(HttpUser):
    """FastAPI v2 API 用户模拟"""
    wait_time = between(1, 3)
    weight = 1

    def on_start(self):
        self.username = f"fastapi_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
        self.email = f"{self.username}@benchmark.test"
        self.password = "Benchmark123!"
        self.access_token = None

        register_resp = self.client.post("/api/v2/auth/register", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })

        if register_resp.status_code in [200, 201]:
            login_resp = self.client.post("/api/v2/auth/login", json={
                "username": self.username,
                "password": self.password
            })
            if login_resp.status_code == 200:
                data = login_resp.json()
                self.access_token = data.get("access_token") or data.get("data", {}).get("access_token")

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    @task(10)
    def health_check(self):
        self.client.get("/api/v2/health")

    @task(8)
    def get_current_user(self):
        if self.access_token:
            self.client.get("/api/v2/auth/me", headers=self._get_headers())

    @task(5)
    def get_test_cases(self):
        if self.access_token:
            self.client.get("/api/v2/test-cases?page=1&per_page=10", headers=self._get_headers())

    @task(3)
    def create_test_case(self):
        if self.access_token:
            case_name = f"BenchmarkCase_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            self.client.post("/api/v2/test-cases", json={
                "name": case_name,
                "description": "性能基准测试用例",
                "steps": [{"action": "click", "target": "#button"}]
            }, headers=self._get_headers())

    @task(4)
    def get_api_tests(self):
        if self.access_token:
            self.client.get("/api/v2/api-tests?page=1&per_page=10", headers=self._get_headers())


class MixedWorkloadUser(HttpUser):
    """混合负载用户模拟"""
    wait_time = between(2, 5)
    weight = 2

    def on_start(self):
        self.username = f"mixed_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
        self.email = f"{self.username}@benchmark.test"
        self.password = "Benchmark123!"
        self.access_token = None

        register_resp = self.client.post("/api/v1/auth/register", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })

        if register_resp.status_code in [200, 201]:
            login_resp = self.client.post("/api/v1/auth/login", json={
                "username": self.username,
                "password": self.password
            })
            if login_resp.status_code == 200:
                data = login_resp.json()
                self.access_token = data.get("data", {}).get("access_token")

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    @task(5)
    def flask_health(self):
        self.client.get("/api/v1/health")

    @task(5)
    def fastapi_health(self):
        self.client.get("/api/v2/health")

    @task(3)
    def flask_get_projects(self):
        if self.access_token:
            self.client.get("/api/v1/projects?page=1&per_page=10", headers=self._get_headers())

    @task(3)
    def fastapi_get_test_cases(self):
        if self.access_token:
            self.client.get("/api/v2/test-cases?page=1&per_page=10", headers=self._get_headers())

    @task(2)
    def flask_create_project(self):
        if self.access_token:
            project_name = f"MixedProject_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            self.client.post("/api/v1/projects", json={
                "name": project_name,
                "description": "混合负载测试项目"
            }, headers=self._get_headers())

    @task(2)
    def fastapi_create_test_case(self):
        if self.access_token:
            case_name = f"MixedCase_{''.join(random.choices(string.ascii_lowercase, k=6))}"
            self.client.post("/api/v2/test-cases", json={
                "name": case_name,
                "description": "混合负载测试用例",
                "steps": [{"action": "click", "target": "#button"}]
            }, headers=self._get_headers())
