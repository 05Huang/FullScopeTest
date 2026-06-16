"""
OpenTelemetry 分布式追踪中间件

自动追踪 HTTP 请求、SQL 查询等操作。
通过 TRACING_ENABLED 环境变量控制开关。
"""

import os
import time
from ..core.logging import get_logger

logger = get_logger(__name__)

TRACING_ENABLED = os.environ.get("TRACING_ENABLED", "false").lower() == "true"


class TracingMiddleware:
    """OpenTelemetry 追踪中间件"""

    def __init__(self, app=None):
        self.app = app
        self._tracer = None
        if TRACING_ENABLED:
            self._init_tracing()

    def _init_tracing(self):
        """初始化 OpenTelemetry（延迟导入，避免未安装时报错）"""
        try:
            from opentelemetry import trace
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            provider = TracerProvider()
            trace.set_tracer_provider(provider)
            self._tracer = trace.get_tracer(__name__)
            logger.info("OpenTelemetry tracing initialized")
        except ImportError:
            logger.warning("OpenTelemetry SDK not installed, tracing disabled")

    def instrument_app(self, app):
        """为 Flask app 添加追踪"""
        if not TRACING_ENABLED:
            logger.info("Tracing disabled (TRACING_ENABLED=false)")
            return

        @app.before_request
        def _start_trace():
            from flask import g, request
            g.trace_start = time.time()
            if self._tracer:
                span = self._tracer.start_span(f"{request.method} {request.path}")
                span.set_attribute("http.method", request.method)
                span.set_attribute("http.url", request.url)
                g.trace_span = span

        @app.after_request
        def _end_trace(response):
            from flask import g, request
            duration_ms = round((time.time() - getattr(g, "trace_start", time.time())) * 1000, 2)
            if hasattr(g, "trace_span"):
                g.trace_span.set_attribute("http.status_code", response.status_code)
                g.trace_span.set_attribute("duration_ms", duration_ms)
                g.trace_span.end()
            if duration_ms > 2000:
                logger.warning("慢请求", path=request.path, duration_ms=duration_ms)
            return response

        logger.info("Tracing middleware registered")


def setup_tracing(app):
    """设置追踪中间件"""
    middleware = TracingMiddleware()
    middleware.instrument_app(app)
    return middleware
