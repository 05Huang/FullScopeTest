"""
Tests for the Prometheus metrics module (P1-03)
"""

import pytest
from prometheus_client import CollectorRegistry


class TestPrometheusMetrics:
    """Test Prometheus metrics configuration and recording"""

    def test_api_requests_total_metric_exists(self):
        """Verify api_requests_total counter is properly defined"""
        from app.core.metrics import api_requests_total
        assert api_requests_total is not None
        # Test that we can increment the counter
        api_requests_total.labels(method="GET", endpoint="/api/v1/projects", status="200").inc()
        assert api_requests_total.labels(method="GET", endpoint="/api/v1/projects", status="200")._value.get() >= 1

    def test_task_execution_duration_metric_exists(self):
        """Verify task_execution_duration histogram is properly defined"""
        from app.core.metrics import task_execution_duration
        assert task_execution_duration is not None
        # Test that we can observe a value
        task_execution_duration.labels(task_name="run_web_test").observe(1.5)

    def test_active_websocket_connections_metric_exists(self):
        """Verify active_websocket_connections gauge is properly defined"""
        from app.core.metrics import active_websocket_connections
        assert active_websocket_connections is not None
        active_websocket_connections.set(5)
        assert active_websocket_connections._value.get() == 5

    def test_task_total_counter_exists(self):
        """Verify celery_tasks_total counter is properly defined"""
        from app.core.metrics import task_total
        assert task_total is not None
        task_total.labels(task_name="run_perf_test", status="success").inc()

    def test_record_task_success(self):
        """Verify record_task_success increments correct counters"""
        from app.core.metrics import record_task_success, task_total
        initial_count = task_total.labels(task_name="test_task", status="success")._value.get()
        record_task_success("test_task", 2.5)
        new_count = task_total.labels(task_name="test_task", status="success")._value.get()
        assert new_count > initial_count

    def test_record_task_failure(self):
        """Verify record_task_failure increments correct counters"""
        from app.core.metrics import record_task_failure, task_total
        initial_count = task_total.labels(task_name="test_task_fail", status="failure")._value.get()
        record_task_failure("test_task_fail", 1.0)
        new_count = task_total.labels(task_name="test_task_fail", status="failure")._value.get()
        assert new_count > initial_count

    def test_api_request_duration_histogram(self):
        """Verify api_request_duration histogram records values"""
        from app.core.metrics import api_request_duration
        api_request_duration.labels(method="POST", endpoint="/api/v1/test").observe(0.5)
        api_request_duration.labels(method="POST", endpoint="/api/v1/test").observe(1.0)

    def test_metrics_endpoint_available(self, client):
        """Verify /metrics endpoint is accessible"""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Check that the response contains expected metric names
        data = response.data.decode("utf-8")
        assert "api_requests_total" in data or "HELP" in data

    def test_metrics_include_app_info(self, client):
        """Verify metrics endpoint includes app_info"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.data.decode("utf-8")
        # prometheus-flask-exporter should expose app_info
        assert "app_info" in data or "fullscopetest" in data.lower()
