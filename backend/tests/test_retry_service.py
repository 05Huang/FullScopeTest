"""
测试执行重试服务测试
"""

import pytest


class TestRetryService:
    """RetryService 测试"""

    def test_no_retry_on_success(self, app):
        """成功执行不应重试"""
        with app.app_context():
            from app.services.retry_service import RetryService
            svc = RetryService(max_retries=3)
            result = svc.execute_with_retry(lambda: {"passed": True})
            assert result["passed"] is True
            assert result["retries"] == 0
            assert result["status"] == "passed"

    def test_retry_on_server_error(self, app):
        """5xx 错误应重试"""
        with app.app_context():
            from app.services.retry_service import RetryService
            call_count = [0]

            def execute():
                call_count[0] += 1
                if call_count[0] < 3:
                    return {"passed": False, "status_code": 500, "error_type": "server_error"}
                return {"passed": True}

            svc = RetryService(max_retries=3, base_delay=0.01)
            result = svc.execute_with_retry(execute, case_name="test_retry")
            assert result["passed"] is True
            assert result["retries"] == 2
            assert result["status"] == "flaky"

    def test_no_retry_on_404(self, app):
        """404 不应重试"""
        with app.app_context():
            from app.services.retry_service import RetryService
            svc = RetryService(max_retries=3)
            result = svc.execute_with_retry(
                lambda: {"passed": False, "status_code": 404, "error_type": "client_error"}
            )
            assert result["passed"] is False
            assert result["retries"] == 0
            assert result["status"] == "failed"

    def test_retry_on_timeout(self, app):
        """超时应重试"""
        with app.app_context():
            from app.services.retry_service import RetryService
            call_count = [0]

            def execute():
                call_count[0] += 1
                if call_count[0] < 2:
                    return {"passed": False, "error_type": "timeout"}
                return {"passed": True}

            svc = RetryService(max_retries=3, base_delay=0.01)
            result = svc.execute_with_retry(execute)
            assert result["passed"] is True
            assert result["retries"] == 1

    def test_max_retries_exhausted(self, app):
        """重试用尽应返回失败"""
        with app.app_context():
            from app.services.retry_service import RetryService
            svc = RetryService(max_retries=2, base_delay=0.01)
            result = svc.execute_with_retry(
                lambda: {"passed": False, "status_code": 500, "error_type": "server_error"}
            )
            assert result["passed"] is False
            assert result["retries"] == 2
            assert result["status"] == "failed"

    def test_retry_history_recorded(self, app):
        """重试历史应被记录"""
        with app.app_context():
            from app.services.retry_service import RetryService
            svc = RetryService(max_retries=2, base_delay=0.01)
            result = svc.execute_with_retry(
                lambda: {"passed": False, "status_code": 500, "error_type": "server_error"}
            )
            assert "retry_history" in result
            assert len(result["retry_history"]) == 2

    def test_classify_timeout_exception(self, app):
        """超时异常应正确分类"""
        with app.app_context():
            from app.services.retry_service import RetryService
            error_type = RetryService._classify_exception(TimeoutError("request timeout error"))
            assert error_type == "timeout"

    def test_exponential_backoff_delay(self, app):
        """延迟应呈指数增长"""
        with app.app_context():
            from app.services.retry_service import RetryService
            svc = RetryService(base_delay=1.0, max_delay=16.0)
            d0 = svc._calc_delay(0)
            d1 = svc._calc_delay(1)
            d2 = svc._calc_delay(2)
            assert d0 < d1 < d2  # 抖动可能导致不严格递增，但趋势应正确
