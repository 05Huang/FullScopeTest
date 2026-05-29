"""
Celery 应用配置

初始化 Celery 应用，配置任务队列、死信队列（DLQ）和任务可靠性保障
"""

from celery import Celery
from app.config import config


def make_celery(config_name='development'):
    """
    创建并配置 Celery 应用实例

    Args:
        config_name: 配置环境名称

    Returns:
        Celery: 配置好的 Celery 实例
    """
    celery = Celery(__name__)

    # 加载 Celery 配置
    app_config = config[config_name]
    celery.conf.update(
        broker_url=app_config.CELERY_BROKER_URL,
        result_backend=app_config.CELERY_RESULT_BACKEND,
        task_track_started=app_config.CELERY_TASK_TRACK_STARTED,
        task_time_limit=app_config.CELERY_TASK_TIME_LIMIT,
        accept_content=app_config.CELERY_ACCEPT_CONTENT,
        task_serializer=app_config.CELERY_TASK_SERIALIZER,
        result_serializer=app_config.CELERY_RESULT_SERIALIZER,
        timezone='Asia/Shanghai',
        enable_utc=True,
        # 可靠性配置
        task_acks_late=app_config.CELERY_TASK_ACKS_LATE,
        task_reject_on_worker_lost=app_config.CELERY_TASK_REJECT_ON_WORKER_LOST,
        task_routes=app_config.CELERY_TASK_ROUTES,
        task_default_retry_delay=app_config.CELERY_TASK_DEFAULT_RETRY_DELAY,
        task_max_retries=app_config.CELERY_TASK_MAX_RETRIES,
        # 死信队列：失败任务路由到 DLQ
        task_queue_max_priority=10,
        task_default_priority=5,
    )

    return celery


def init_celery(celery_app, app):
    """
    将 Celery 与 Flask 应用集成

    Args:
        celery_app: Celery 实例
        app: Flask 应用实例
    """
    # 正确映射 Flask 配置到 Celery 配置
    celery_app.conf.update(
        broker_url=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        result_backend=app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        task_track_started=app.config.get('CELERY_TASK_TRACK_STARTED', True),
        task_time_limit=app.config.get('CELERY_TASK_TIME_LIMIT', 30 * 60),
        accept_content=app.config.get('CELERY_ACCEPT_CONTENT', ['json']),
        task_serializer=app.config.get('CELERY_TASK_SERIALIZER', 'json'),
        result_serializer=app.config.get('CELERY_RESULT_SERIALIZER', 'json'),
        timezone='Asia/Shanghai',
        enable_utc=True,
        # 可靠性配置
        task_acks_late=app.config.get('CELERY_TASK_ACKS_LATE', True),
        task_reject_on_worker_lost=app.config.get('CELERY_TASK_REJECT_ON_WORKER_LOST', True),
        task_routes=app.config.get('CELERY_TASK_ROUTES', {'tasks.*': {'queue': 'default'}}),
        task_default_retry_delay=app.config.get('CELERY_TASK_DEFAULT_RETRY_DELAY', 60),
        task_max_retries=app.config.get('CELERY_TASK_MAX_RETRIES', 3),
        # 死信队列优先级配置
        task_queue_max_priority=10,
        task_default_priority=5,
    )

    class ContextTask(celery_app.Task):
        """带有 Flask 应用上下文的任务基类，支持自动重试和失败日志"""
        abstract = True
        max_retries = 3
        default_retry_delay = 60
        acks_late = True
        reject_on_worker_lost = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """任务最终失败时（重试耗尽）的回调，记录告警日志"""
            from app.core.logging import get_logger
            task_logger = get_logger('celery.dlq')
            task_logger.error(
                "Task permanently failed — moved to dead letter queue",
                task_id=task_id,
                task_name=self.name,
                exception_type=type(exc).__name__,
                exception_message=str(exc),
                retries_exhausted=True,
                args=str(args),
                kwargs=str(kwargs),
            )

    celery_app.Task = ContextTask
    return celery_app
