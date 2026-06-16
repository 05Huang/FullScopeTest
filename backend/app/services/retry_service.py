"""
测试执行重试与容错服务

在网络抖动或临时故障时自动重试失败的测试用例。

特性：
- 用例级重试配置：最大重试次数（0-5）、重试间隔（秒）
- 自动重试条件：网络错误、5xx 错误、超时（不重试 4xx）
- 重试间隔：指数退避（1s, 2s, 4s, 8s, 16s）
- 最终结果标记：passed、failed、flaky（重试后通过）
"""

import time
import random
from typing import Dict, Any, Callable, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# 可重试的错误类型
RETRYABLE_ERRORS = {"timeout", "connection_error", "server_error", "rate_limit"}

# 不重试的 HTTP 状态码
NON_RETRYABLE_STATUS = {400, 401, 403, 404, 405, 422}


class RetryService:
    """测试执行重试服务"""

    def __init__(self, max_retries: int = 0, base_delay: float = 1.0, max_delay: float = 16.0):
        """
        Args:
            max_retries: 最大重试次数（0-5）
            base_delay: 基础重试间隔（秒）
            max_delay: 最大重试间隔（秒）
        """
        self.max_retries = min(max(max_retries, 0), 5)
        self.base_delay = base_delay
        self.max_delay = max_delay

    def execute_with_retry(
        self,
        execute_fn: Callable,
        case_data: Any = None,
        case_name: str = "unknown",
    ) -> Dict[str, Any]:
        """
        带重试的执行

        Args:
            execute_fn: 执行函数 () -> result_dict
            case_data: 用例数据（用于日志）
            case_name: 用例名称（用于日志）

        Returns:
            Dict: {passed, attempts, retries, status, ...}
        """
        attempts = 0
        retries = 0
        last_result = None
        retry_history = []

        while attempts <= self.max_retries:
            attempts += 1
            try:
                result = execute_fn()
                if isinstance(result, dict):
                    # 检查是否需要重试
                    if self._should_retry(result) and attempts <= self.max_retries:
                        delay = self._calc_delay(retries)
                        logger.info(
                            "用例执行失败，准备重试",
                            case_name=case_name, attempt=attempts,
                            retry_in=delay, reason=result.get("error_type", "unknown"),
                        )
                        retry_history.append({
                            "attempt": attempts,
                            "result": result,
                            "retry_delay": delay,
                        })
                        time.sleep(delay)
                        retries += 1
                        last_result = result
                        continue

                    # 成功或不可重试的失败
                    passed = result.get("passed", False)
                    status = "passed" if passed else "failed"
                    if passed and retries > 0:
                        status = "flaky"  # 重试后通过标记为 flaky

                    result["attempts"] = attempts
                    result["retries"] = retries
                    result["status"] = status
                    result["retry_history"] = retry_history
                    return result

            except Exception as exc:
                error_result = {
                    "passed": False,
                    "error": str(exc),
                    "error_type": self._classify_exception(exc),
                }
                if self._should_retry(error_result) and attempts <= self.max_retries:
                    delay = self._calc_delay(retries)
                    logger.warning(
                        "用例执行异常，准备重试",
                        case_name=case_name, attempt=attempts, error=str(exc),
                    )
                    retry_history.append({"attempt": attempts, "error": str(exc), "retry_delay": delay})
                    time.sleep(delay)
                    retries += 1
                    last_result = error_result
                    continue

                # 不可重试的异常
                error_result["attempts"] = attempts
                error_result["retries"] = retries
                error_result["status"] = "failed"
                error_result["retry_history"] = retry_history
                return error_result

        # 所有重试用尽
        if last_result:
            last_result["attempts"] = attempts
            last_result["retries"] = retries
            last_result["status"] = "failed"
            last_result["retry_history"] = retry_history
        return last_result or {"passed": False, "attempts": attempts, "retries": retries, "status": "failed"}

    def _should_retry(self, result: Dict[str, Any]) -> bool:
        """判断是否应该重试"""
        if result.get("passed", False):
            return False  # 成功不重试

        # HTTP 状态码检查
        status_code = result.get("status_code", 0)
        if status_code in NON_RETRYABLE_STATUS:
            return False  # 客户端错误不重试

        # 错误类型检查
        error_type = result.get("error_type", "")
        return error_type in RETRYABLE_ERRORS or status_code >= 500

    def _calc_delay(self, retry_num: int) -> float:
        """计算指数退避延迟（带随机抖动）"""
        delay = min(self.base_delay * (2 ** retry_num), self.max_delay)
        jitter = random.uniform(0, delay * 0.5)
        return round(delay + jitter, 2)

    @staticmethod
    def _classify_exception(exc: Exception) -> str:
        """分类异常类型"""
        exc_str = str(exc).lower()
        if "timeout" in exc_str:
            return "timeout"
        if "connection" in exc_str:
            return "connection_error"
        return "unknown"


def get_retry_service(max_retries: int = 0) -> RetryService:
    """获取重试服务"""
    return RetryService(max_retries=max_retries)