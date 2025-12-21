"""
Celery 应用配置

初始化 Celery 应用，配置任务队列
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
    )

    class ContextTask(celery_app.Task):
        """带有 Flask 应用上下文的任务基类"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
