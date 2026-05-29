"""
Celery Dead Letter Queue (DLQ) 配置测试

验证任务可靠性配置：死信队列路由、重试策略、任务 ACK 配置
"""

import os
import sys

import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.config import BaseConfig


# ──────────────────────────────────────────────────────────────
# 配置层面测试
# ──────────────────────────────────────────────────────────────

class TestDLQConfiguration:
    """验证 BaseConfig 中 DLQ 相关配置项正确设置"""

    def test_task_acks_late_enabled(self):
        """任务确认延迟启用：保证任务执行完才 ACK，worker 崩溃时任务不会丢失"""
        assert BaseConfig.CELERY_TASK_ACKS_LATE is True

    def test_task_reject_on_worker_lost_enabled(self):
        """Worker 丢失时拒绝任务：配合 acks_late 确保任务重新入队"""
        assert BaseConfig.CELERY_TASK_REJECT_ON_WORKER_LOST is True

    def test_task_routes_defined(self):
        """任务路由已配置"""
        assert isinstance(BaseConfig.CELERY_TASK_ROUTES, dict)
        assert 'tasks.*' in BaseConfig.CELERY_TASK_ROUTES

    def test_max_retries_configured(self):
        """最大重试次数已配置为 3"""
        assert BaseConfig.CELERY_TASK_MAX_RETRIES == 3

    def test_retry_delay_configured(self):
        """重试间隔已配置为 60 秒"""
        assert BaseConfig.CELERY_TASK_DEFAULT_RETRY_DELAY == 60


# ──────────────────────────────────────────────────────────────
# Celery app 初始化测试
# ──────────────────────────────────────────────────────────────

class TestCeleryAppInit:
    """验证 Celery 应用实例的 DLQ 配置正确应用"""

    @pytest.fixture(autouse=True)
    def _setup(self):
        os.environ.setdefault("FLASK_ENV", "testing")
        os.environ["CELERY_ENABLE"] = "false"

    def test_make_celery_has_dlq_settings(self):
        """make_celery 返回的实例包含 DLQ 相关配置"""
        from app.celery_app import make_celery
        celery_app = make_celery("testing")

        assert celery_app.conf.task_acks_late is True
        assert celery_app.conf.task_reject_on_worker_lost is True
        assert celery_app.conf.task_max_retries == 3
        assert celery_app.conf.task_default_retry_delay == 60

    def test_init_celery_has_dlq_settings(self, app):
        """init_celery 为 Flask 集成的 Celery 实例配置了 DLQ"""
        from app.celery_app import init_celery
        from app.extensions import celery

        init_celery(celery, app)

        assert celery.conf.task_acks_late is True
        assert celery.conf.task_reject_on_worker_lost is True
        assert celery.conf.task_max_retries == 3


# ──────────────────────────────────────────────────────────────
# ContextTask 基类测试
# ──────────────────────────────────────────────────────────────

class TestContextTaskBase:
    """验证 ContextTask 基类的默认任务可靠性属性"""

    @pytest.fixture(autouse=True)
    def _setup(self):
        os.environ.setdefault("FLASK_ENV", "testing")
        os.environ["CELERY_ENABLE"] = "false"

    def test_context_task_has_max_retries(self, app):
        """ContextTask 基类设置 max_retries=3"""
        from app.celery_app import init_celery
        from app.extensions import celery

        init_celery(celery, app)
        assert celery.Task.max_retries == 3

    def test_context_task_has_default_retry_delay(self, app):
        """ContextTask 基类设置 default_retry_delay=60"""
        from app.celery_app import init_celery
        from app.extensions import celery

        init_celery(celery, app)
        assert celery.Task.default_retry_delay == 60

    def test_context_task_acks_late(self, app):
        """ContextTask 基类设置 acks_late=True"""
        from app.celery_app import init_celery
        from app.extensions import celery

        init_celery(celery, app)
        assert celery.Task.acks_late is True

    def test_context_task_reject_on_worker_lost(self, app):
        """ContextTask 基类设置 reject_on_worker_lost=True"""
        from app.celery_app import init_celery
        from app.extensions import celery

        init_celery(celery, app)
        assert celery.Task.reject_on_worker_lost is True


# ──────────────────────────────────────────────────────────────
# 任务装饰器重试参数测试
# ──────────────────────────────────────────────────────────────

class TestTaskRetryConfiguration:
    """验证各 Celery 任务的装饰器中设置了正确的重试参数"""

    @pytest.fixture(autouse=True)
    def _setup(self):
        os.environ.setdefault("FLASK_ENV", "testing")
        os.environ["CELERY_ENABLE"] = "false"

    def _get_task(self, task_name):
        from app.extensions import celery
        return celery.tasks.get(task_name)

    def test_run_web_test_has_retry_config(self):
        """run_web_test 任务配置了重试参数"""
        task = self._get_task('tasks.run_web_test')
        assert task is not None
        assert task.max_retries == 3
        assert task.retry_backoff is True
        assert task.retry_jitter is True

    def test_run_perf_test_has_retry_config(self):
        """run_perf_test 任务配置了重试参数"""
        task = self._get_task('tasks.run_perf_test')
        assert task is not None
        assert task.max_retries == 3
        assert task.retry_backoff is True
        assert task.retry_jitter is True

    def test_cleanup_old_results_has_retry_config(self):
        """cleanup_old_results 任务配置了重试参数"""
        task = self._get_task('tasks.cleanup_old_results')
        assert task is not None
        assert task.max_retries == 3
        assert task.retry_backoff is True
        assert task.retry_jitter is True

    def test_run_app_test_has_retry_config(self):
        """run_app_test 任务配置了重试参数"""
        task = self._get_task('tasks.run_app_test')
        assert task is not None
        assert task.max_retries == 3
        assert task.retry_backoff is True
        assert task.retry_jitter is True


# ──────────────────────────────────────────────────────────────
# on_failure 回调测试
# ──────────────────────────────────────────────────────────────

class TestDLQFailureCallback:
    """验证 ContextTask 的 on_failure 回调（DLQ 日志记录）"""

    @pytest.fixture(autouse=True)
    def _setup(self):
        os.environ.setdefault("FLASK_ENV", "testing")
        os.environ["CELERY_ENABLE"] = "false"

    def test_context_task_has_on_failure(self, app):
        """ContextTask 基类定义了 on_failure 方法"""
        from app.celery_app import init_celery
        from app.extensions import celery

        init_celery(celery, app)
        assert hasattr(celery.Task, 'on_failure')
        assert callable(celery.Task.on_failure)
