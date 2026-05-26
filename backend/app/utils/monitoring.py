"""
监控和可观测性模块

提供错误追踪、性能监控、指标收集等功能
"""

import time
import logging
import functools
from typing import Optional, Callable, Any
from flask import request, g, current_app

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """性能监控器"""

    @staticmethod
    def track_execution_time(func: Callable) -> Callable:
        """装饰器：跟踪函数执行时间"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"{func.__name__} executed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"{func.__name__} failed after {duration:.3f}s: {str(e)}")
                raise
        return wrapper

    @staticmethod
    def track_api_call(endpoint: str, method: str = 'GET'):
        """记录 API 调用指标"""
        logger.info(f"API Call: {method} {endpoint}")


class ErrorTracker:
    """错误追踪器"""

    @staticmethod
    def capture_exception(error: Exception, context: Optional[dict] = None):
        """捕获并记录异常"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {},
        }

        # 添加请求上下文
        if request:
            error_info['request'] = {
                'method': request.method,
                'url': request.url,
                'endpoint': request.endpoint,
                'user_agent': str(request.user_agent),
            }

        # 添加用户上下文
        if hasattr(g, 'current_user_id'):
            error_info['user_id'] = g.current_user_id

        logger.error(f"Exception captured: {error_info}", exc_info=True)

        # 如果配置了 Sentry，发送到 Sentry
        try:
            import sentry_sdk
            with sentry_sdk.push_scope() as scope:
                if context:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                sentry_sdk.capture_exception(error)
        except ImportError:
            pass  # Sentry 未安装
        except Exception as e:
            logger.warning(f"Failed to send error to Sentry: {str(e)}")

    @staticmethod
    def capture_message(message: str, level: str = 'info', context: Optional[dict] = None):
        """捕获并记录消息"""
        logger.log(getattr(logging, level.upper(), logging.INFO), message)

        try:
            import sentry_sdk
            sentry_sdk.capture_message(message, level)
        except (ImportError, Exception):
            pass


class MetricsCollector:
    """指标收集器"""

    def __init__(self):
        self._metrics = {}

    def increment(self, name: str, value: int = 1, tags: Optional[dict] = None):
        """递增计数器"""
        key = self._build_key(name, tags)
        self._metrics[key] = self._metrics.get(key, 0) + value

    def gauge(self, name: str, value: float, tags: Optional[dict] = None):
        """设置仪表盘值"""
        key = self._build_key(name, tags)
        self._metrics[key] = value

    def timing(self, name: str, duration: float, tags: Optional[dict] = None):
        """记录时间指标"""
        key = self._build_key(name, tags)
        if key not in self._metrics:
            self._metrics[key] = []
        self._metrics[key].append(duration)

    def get_metrics(self) -> dict:
        """获取所有指标"""
        return self._metrics.copy()

    def reset(self):
        """重置所有指标"""
        self._metrics.clear()

    @staticmethod
    def _build_key(name: str, tags: Optional[dict] = None) -> str:
        """构建指标键"""
        if not tags:
            return name
        tag_str = ','.join(f'{k}={v}' for k, v in sorted(tags.items()))
        return f"{name}#{tag_str}"


# 全局指标收集器实例
metrics = MetricsCollector()


def init_monitoring(app):
    """初始化监控系统"""

    # 初始化 Sentry（如果配置了）
    sentry_dsn = app.config.get('SENTRY_DSN')
    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration

            sentry_logging = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )

            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[FlaskIntegration(), sentry_logging],
                traces_sample_rate=app.config.get('SENTRY_TRACES_SAMPLE_RATE', 0.1),
                environment=app.config.get('FLASK_ENV', 'development'),
            )
            logger.info("Sentry monitoring initialized")
        except ImportError:
            logger.warning("sentry-sdk not installed, skipping Sentry initialization")
        except Exception as e:
            logger.error(f"Failed to initialize Sentry: {str(e)}")

    # 注册请求钩子
    @app.before_request
    def before_request_monitoring():
        g.request_start_time = time.time()

    @app.after_request
    def after_request_monitoring(response):
        if hasattr(g, 'request_start_time'):
            duration = time.time() - g.request_start_time
            metrics.timing('request.duration', duration, {
                'method': request.method,
                'endpoint': request.endpoint or 'unknown',
                'status': response.status_code,
            })

            # 记录慢请求
            if duration > 1.0:
                logger.warning(f"Slow request: {request.method} {request.path} took {duration:.3f}s")

        return response

    logger.info("Monitoring system initialized")
