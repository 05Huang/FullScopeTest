"""
Sentry 错误追踪集成

自动收集线上错误并告警。
通过 SENTRY_DSN 环境变量启用。
"""

import os
from ..core.logging import get_logger

logger = get_logger(__name__)

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "development")
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.1"))


def init_sentry(app=None):
    """
    初始化 Sentry

    Args:
        app: Flask app（可选）
    """
    if not SENTRY_DSN:
        logger.info("Sentry DSN not configured, error tracking disabled")
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=SENTRY_ENVIRONMENT,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
            integrations=[
                FlaskIntegration(),
                SqlalchemyIntegration(),
            ],
            before_send=_filter_sensitive_data,
        )
        logger.info("Sentry initialized", environment=SENTRY_ENVIRONMENT)
    except ImportError:
        logger.warning("sentry-sdk not installed, error tracking disabled")


def _filter_sensitive_data(event, hint):
    """过滤敏感数据"""
    # 移除 Authorization header
    if "request" in event and "headers" in event["request"]:
        headers = event["request"]["headers"]
        if "Authorization" in headers:
            headers["Authorization"] = "[Filtered]"
    # 移除密码字段
    if "request" in event and "data" in event["request"]:
        data = event["request"]["data"]
        if isinstance(data, dict):
            for key in ("password", "token", "secret", "api_key"):
                if key in data:
                    data[key] = "[Filtered]"
    return event


def capture_exception(exc, user_id=None, request_id=None, extra=None):
    """手动捕获异常"""
    if not SENTRY_DSN:
        return
    try:
        import sentry_sdk
        with sentry_sdk.new_scope() as scope:
            if user_id:
                scope.user = {"id": str(user_id)}
            if request_id:
                scope.set_tag("request_id", request_id)
            if extra:
                for k, v in extra.items():
                    scope.set_extra(k, v)
            sentry_sdk.capture_exception(exc)
    except Exception:
        pass  # Sentry 本身不应影响业务
