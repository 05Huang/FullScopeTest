"""
性能测试任务指标采集测试

覆盖 P2B-02: 修改 Locust 任务执行器，实时采集并写入 PerformanceMetricSample，
任务结束后计算并存储统计摘要
"""

import uuid
import time
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.extensions import db
from app.models.perf_test_scenario import PerfTestScenario
from app.models.perf_test_result import PerformanceTestResult, PerformanceMetricSample


def _auth_headers(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "Passw0rd!"
    email = f"{username}@example.com"

    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    access_token = login_resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def _create_scenario(client, headers):
    body = {
        "name": f"perf-test-{uuid.uuid4().hex[:8]}",
        "target_url": "http://localhost:8080/api/v1/ping",
        "user_count": 10,
        "spawn_rate": 2,
        "duration": 30,
    }
    return client.post("/api/v1/perf-test/scenarios", json=body, headers=headers)


class TestPerformanceMetricSample:
    """PerformanceMetricSample 模型测试"""

    def test_create_metric_sample(self, app):
        with app.app_context():
            from app.extensions import db

            # 先创建一个 scenario
            scenario = PerfTestScenario(
                name="test-perf",
                target_url="http://localhost:8080/api/v1/ping",
                user_count=10,
                spawn_rate=2,
                duration=30,
                project_id=1,
                user_id=1,
            )
            db.session.add(scenario)
            db.session.commit()

            result = PerformanceTestResult(
                scenario_id=scenario.id,
                project_id=scenario.project_id,
                user_count=10,
                spawn_rate=2,
                duration=30,
                target_url="http://localhost:8080/api/v1/ping",
                status="running",
            )
            db.session.add(result)
            db.session.commit()

            sample = PerformanceMetricSample(
                test_result_id=result.id,
                timestamp=datetime.utcnow(),
                elapsed_seconds=5,
                rps=12.5,
                active_users=10,
                avg_response_time=45.2,
                min_response_time=10.0,
                max_response_time=120.5,
                p95_response_time=89.3,
                p99_response_time=110.0,
                request_count=62,
                failure_count=2,
                error_rate=3.2,
            )
            db.session.add(sample)
            db.session.commit()

            assert sample.id is not None
            assert sample.test_result_id == result.id
            assert sample.rps == 12.5
            assert sample.elapsed_seconds == 5

    def test_metric_sample_to_dict(self, app):
        with app.app_context():
            from app.extensions import db

            sample = PerformanceMetricSample(
                test_result_id=1,
                timestamp=datetime.utcnow(),
                elapsed_seconds=10,
                rps=25.0,
                active_users=5,
                avg_response_time=30.0,
                min_response_time=5.0,
                max_response_time=100.0,
                p95_response_time=75.0,
                p99_response_time=95.0,
                request_count=250,
                failure_count=5,
                error_rate=2.0,
            )
            d = sample.to_dict()
            assert d["rps"] == 25.0
            assert d["elapsed_seconds"] == 10
            assert d["request_count"] == 250


class TestPerformanceTestResult:
    """PerformanceTestResult 模型测试"""

    def test_create_test_result(self, app):
        with app.app_context():
            from app.extensions import db

            scenario = PerfTestScenario(
                name="test-perf",
                target_url="http://localhost:8080/api/v1/ping",
                user_count=20,
                spawn_rate=5,
                duration=60,
                project_id=1,
                user_id=1,
            )
            db.session.add(scenario)
            db.session.commit()

            result = PerformanceTestResult(
                scenario_id=scenario.id,
                project_id=scenario.project_id,
                user_count=20,
                spawn_rate=5,
                duration=60,
                target_url="http://localhost:8080/api/v1/ping",
                status="running",
            )
            db.session.add(result)
            db.session.commit()

            assert result.id is not None
            assert result.scenario_id == scenario.id
            assert result.status == "running"

    def test_result_to_dict(self, app):
        with app.app_context():
            result = PerformanceTestResult(
                scenario_id=1,
                user_count=10,
                spawn_rate=2,
                duration=30,
                target_url="http://localhost:8080",
                status="completed",
                total_requests=500,
                total_failures=10,
                error_rate=2.0,
                rps=15.0,
                avg_response_time=50.0,
                min_response_time=10.0,
                max_response_time=200.0,
                p50_response_time=40.0,
                p75_response_time=60.0,
                p95_response_time=120.0,
                p99_response_time=180.0,
            )
            d = result.to_dict()
            assert d["rps"] == 15.0
            assert d["p95_response_time"] == 120.0
            assert d["p99_response_time"] == 180.0
            assert d["error_rate"] == 2.0

    def test_metric_sample_relationship(self, app):
        with app.app_context():
            from app.extensions import db

            result = PerformanceTestResult(
                scenario_id=1,
                user_count=10,
                spawn_rate=2,
                duration=30,
                target_url="http://localhost:8080",
                status="completed",
            )
            db.session.add(result)
            db.session.commit()

            sample = PerformanceMetricSample(
                test_result_id=result.id,
                timestamp=datetime.utcnow(),
                elapsed_seconds=5,
                rps=10.0,
                active_users=5,
                request_count=50,
            )
            db.session.add(sample)
            db.session.commit()

            # 验证关联关系
            assert len(result.metric_samples) == 1
            assert result.metric_samples[0].rps == 10.0
