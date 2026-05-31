"""
Prometheus Metrics 配置模块

提供自定义指标，用于监控应用运行状态：
- api_requests_total: 按路由、方法、状态码统计 API 请求总数
- task_execution_duration_seconds: 按任务类型统计任务执行耗时
- active_websocket_connections: 当前活跃的 WebSocket 连接数
"""

import os
from prometheus_client import Counter, Histogram, Gauge
from app.core.logging import get_logger

logger = get_logger(__name__)

# /metrics 端点访问令牌（生产环境应设置此环境变量）
METRICS_TOKEN = os.environ.get('METRICS_TOKEN', '')

# ──────────────────────────────────────────────
# API 请求指标
# ──────────────────────────────────────────────

api_requests_total = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status"],
)

api_request_duration = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# ──────────────────────────────────────────────
# Celery 任务指标
# ──────────────────────────────────────────────

task_execution_duration = Histogram(
    "task_execution_duration_seconds",
    "Celery task execution duration in seconds",
    ["task_name"],
    buckets=(0.1, 0.5, 1.0, 5.0, 15.0, 30.0, 60.0, 120.0, 300.0),
)

task_total = Counter(
    "celery_tasks_total",
    "Total number of Celery tasks executed",
    ["task_name", "status"],
)

# ──────────────────────────────────────────────
# WebSocket 指标
# ──────────────────────────────────────────────

active_websocket_connections = Gauge(
    "active_websocket_connections",
    "Number of currently active WebSocket connections",
)

# ──────────────────────────────────────────────
# 限流指标
# ──────────────────────────────────────────────

rate_limit_counter = Counter(
    "rate_limit_exceeded_total",
    "Total number of rate limit violations",
    ["user_type", "endpoint"],
)


def record_task_success(task_name: str, duration: float) -> None:
    """记录成功的 Celery 任务执行"""
    task_total.labels(task_name=task_name, status="success").inc()
    task_execution_duration.labels(task_name=task_name).observe(duration)


def record_task_failure(task_name: str, duration: float) -> None:
    """记录失败的 Celery 任务执行"""
    task_total.labels(task_name=task_name, status="failure").inc()
    task_execution_duration.labels(task_name=task_name).observe(duration)


def init_metrics(app):
    """
    初始化 Prometheus metrics 集成到 Flask 应用

    - 注册 before_request / after_request hook 来自动采集 API 指标
    - 暴露 /metrics 端点（prometheus-flask-exporter 自动完成）
    - 生产环境下 /metrics 端点需要 METRICS_TOKEN 认证
    """
    from prometheus_flask_exporter import PrometheusMetrics

    # /metrics 端点认证中间件
    @app.before_request
    def _protect_metrics():
        from flask import request
        if request.path == '/metrics' and METRICS_TOKEN:
            auth_header = request.headers.get('Authorization', '')
            token = request.args.get('token', '')
            if auth_header == f'Bearer {METRICS_TOKEN}' or token == METRICS_TOKEN:
                return None
            from flask import jsonify
            return jsonify({'error': 'Unauthorized', 'message': 'Invalid or missing metrics token'}), 401

    metrics = PrometheusMetrics(app, group_by="url_rule")

    # 额外暴露应用级常量标签
    metrics.info("app_info", "FullScopeTest application info", version="1.0.0")

    logger.info("Prometheus metrics initialized", endpoint="/metrics",
                authenticated=bool(METRICS_TOKEN))

    return metrics
