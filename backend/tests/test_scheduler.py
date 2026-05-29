"""
调度器模块单元测试
"""

import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

import pytest
from flask import Flask


class TestRemoveJob:

    def test_remove_existing_job(self, app):
        from app.scheduler import remove_job, scheduler
        with app.app_context():
            with patch.object(scheduler, "get_job", return_value=MagicMock()):
                with patch.object(scheduler, "remove_job") as mock_remove:
                    remove_job(1)
                    mock_remove.assert_called_once_with("scheduled_task_1")

    def test_remove_nonexistent_job(self, app):
        from app.scheduler import remove_job, scheduler
        with app.app_context():
            with patch.object(scheduler, "get_job", return_value=None):
                with patch.object(scheduler, "remove_job") as mock_remove:
                    remove_job(999)
                    mock_remove.assert_not_called()


class TestExecuteScheduledTask:

    def test_execute_api_collection_task(self, app):
        from app.scheduler import execute_scheduled_task
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.is_active = True
        mock_task.target_type = "api_collection"
        mock_task.target_id = 10
        mock_task.name = "API Test"
        with patch("app.models.scheduled_task.ScheduledTask") as MockTask:
            MockTask.query.get.return_value = mock_task
            mock_run = MagicMock()
            mock_run.delay.return_value = MagicMock(id="celery-123")
            with patch.dict("sys.modules", {"app.tasks": MagicMock(run_api_collection_task=mock_run)}):
                with patch("app.scheduler.send_notification"):
                    with patch("app.scheduler.scheduler") as mock_sched:
                        mock_sched.app = app
                        with app.app_context():
                            execute_scheduled_task(1)
                            mock_run.delay.assert_called_once_with(10, None)

    def test_execute_inactive_task_returns_early(self, app):
        from app.scheduler import execute_scheduled_task
        mock_task = MagicMock()
        mock_task.is_active = False
        with patch("app.models.scheduled_task.ScheduledTask") as MockTask:
            MockTask.query.get.return_value = mock_task
            mock_run = MagicMock()
            with patch.dict("sys.modules", {"app.tasks": MagicMock(run_api_collection_task=mock_run)}):
                with patch("app.scheduler.scheduler") as mock_sched:
                    mock_sched.app = app
                    with app.app_context():
                        execute_scheduled_task(1)
                        mock_run.delay.assert_not_called()

    def test_execute_nonexistent_task_returns_early(self, app):
        from app.scheduler import execute_scheduled_task
        with patch("app.models.scheduled_task.ScheduledTask") as MockTask:
            MockTask.query.get.return_value = None
            mock_run = MagicMock()
            with patch.dict("sys.modules", {"app.tasks": MagicMock(run_api_collection_task=mock_run)}):
                with patch("app.scheduler.scheduler") as mock_sched:
                    mock_sched.app = app
                    with app.app_context():
                        execute_scheduled_task(999)
                        mock_run.delay.assert_not_called()

    def test_execute_web_collection_task(self, app):
        from app.scheduler import execute_scheduled_task
        mock_task = MagicMock()
        mock_task.id = 2
        mock_task.is_active = True
        mock_task.target_type = "web_collection"
        mock_task.target_id = 20
        mock_task.name = "Web Test"
        with patch("app.models.scheduled_task.ScheduledTask") as MockTask:
            MockTask.query.get.return_value = mock_task
            mock_run = MagicMock()
            mock_run.delay.return_value = MagicMock(id="celery-456")
            with patch.dict("sys.modules", {"app.tasks": MagicMock(run_web_collection_task=mock_run)}):
                with patch("app.scheduler.send_notification"):
                    with patch("app.scheduler.scheduler") as mock_sched:
                        mock_sched.app = app
                        with app.app_context():
                            execute_scheduled_task(2)
                            mock_run.delay.assert_called_once_with(20, None)

    def test_execute_perf_scenario_task(self, app):
        from app.scheduler import execute_scheduled_task
        mock_task = MagicMock()
        mock_task.id = 3
        mock_task.is_active = True
        mock_task.target_type = "perf_scenario"
        mock_task.target_id = 30
        mock_task.name = "Perf Test"
        with patch("app.models.scheduled_task.ScheduledTask") as MockTask:
            MockTask.query.get.return_value = mock_task
            mock_run = MagicMock()
            mock_run.delay.return_value = MagicMock(id="celery-789")
            with patch.dict("sys.modules", {"app.tasks": MagicMock(run_perf_scenario_task=mock_run)}):
                with patch("app.scheduler.send_notification"):
                    with patch("app.scheduler.scheduler") as mock_sched:
                        mock_sched.app = app
                        with app.app_context():
                            execute_scheduled_task(3)
                            mock_run.delay.assert_called_once_with(30)

    def test_execute_unknown_target_type(self, app):
        from app.scheduler import execute_scheduled_task
        mock_task = MagicMock()
        mock_task.id = 4
        mock_task.is_active = True
        mock_task.target_type = "unknown_type"
        mock_task.target_id = 40
        mock_task.name = "Unknown Test"
        with patch("app.models.scheduled_task.ScheduledTask") as MockTask:
            MockTask.query.get.return_value = mock_task
            mock_api = MagicMock()
            mock_web = MagicMock()
            mock_perf = MagicMock()
            with patch.dict("sys.modules", {"app.tasks": MagicMock(run_api_collection_task=mock_api, run_web_collection_task=mock_web, run_perf_scenario_task=mock_perf)}):
                with patch("app.scheduler.send_notification"):
                    with patch("app.scheduler.scheduler") as mock_sched:
                        mock_sched.app = app
                        with app.app_context():
                            execute_scheduled_task(4)
                            mock_api.delay.assert_not_called()
                            mock_web.delay.assert_not_called()
                            mock_perf.delay.assert_not_called()


class TestSendNotification:

    def test_no_notification_without_webhook(self, app):
        from app.scheduler import send_notification
        mock_task = MagicMock()
        mock_task.notify_webhook = None
        with patch("app.scheduler.requests") as mock_requests:
            send_notification(mock_task, "started")
            mock_requests.post.assert_not_called()

    def test_send_notification_with_webhook(self, app):
        from app.scheduler import send_notification
        mock_task = MagicMock()
        mock_task.notify_webhook = "https://example.com/webhook"
        mock_task.notify_events = "all"
        mock_task.name = "Test Task"
        mock_task.target_type = "api_collection"
        mock_task.target_id = 1
        with patch("app.scheduler.requests") as mock_requests:
            mock_requests.post.return_value = MagicMock(status_code=200)
            send_notification(mock_task, "started", task_id="task-123")
            mock_requests.post.assert_called_once()

    def test_notification_filtered_by_events(self, app):
        from app.scheduler import send_notification
        mock_task = MagicMock()
        mock_task.notify_webhook = "https://example.com/webhook"
        mock_task.notify_events = "failed"
        mock_task.name = "Test Task"
        mock_task.target_type = "api_collection"
        mock_task.target_id = 1
        with patch("app.scheduler.requests") as mock_requests:
            send_notification(mock_task, "started")
            mock_requests.post.assert_not_called()

    def test_notification_includes_error_info(self, app):
        from app.scheduler import send_notification
        mock_task = MagicMock()
        mock_task.notify_webhook = "https://example.com/webhook"
        mock_task.notify_events = "all"
        mock_task.name = "Test Task"
        mock_task.target_type = "api_collection"
        mock_task.target_id = 1
        with patch("app.scheduler.requests") as mock_requests:
            mock_requests.post.return_value = MagicMock(status_code=200)
            send_notification(mock_task, "failed", error="Connection timeout")
            call_args = mock_requests.post.call_args
            assert "Connection timeout" in str(call_args)

    def test_notification_handles_request_exception(self, app):
        from app.scheduler import send_notification
        mock_task = MagicMock()
        mock_task.notify_webhook = "https://example.com/webhook"
        mock_task.notify_events = "all"
        mock_task.name = "Test Task"
        mock_task.target_type = "api_collection"
        mock_task.target_id = 1
        with patch("app.scheduler.requests") as mock_requests:
            mock_requests.post.side_effect = Exception("Network error")
            send_notification(mock_task, "started")


class TestGetJobId:

    def test_get_job_id_format(self, app):
        from app.scheduler import get_job_id
        assert get_job_id(1) == "scheduled_task_1"
        assert get_job_id(100) == "scheduled_task_100"
        assert get_job_id("abc") == "scheduled_task_abc"


class TestPatchDummyScheduler:

    def test_dummy_scheduler_methods_return_none(self, app):
        from app.scheduler import _patch_dummy_scheduler
        mock_sched = MagicMock()
        _patch_dummy_scheduler(mock_sched)
        assert mock_sched.get_job("any_id") is None
        assert mock_sched.add_job() is None
        assert mock_sched.modify_job() is None
        assert mock_sched.remove_job() is None


class TestSchedulerFileLock:

    @pytest.mark.skipif(sys.platform == "win32", reason="fcntl not available on Windows")
    def test_first_process_acquires_lock(self):
        import fcntl
        lock_fd = None
        try:
            lock_fd = open("test_scheduler.lock", "w")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            assert True
        finally:
            if lock_fd:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()
                if os.path.exists("test_scheduler.lock"):
                    os.remove("test_scheduler.lock")

    @pytest.mark.skipif(sys.platform == "win32", reason="fcntl not available on Windows")
    def test_second_process_blocked_by_lock(self):
        import fcntl
        lock_fd1 = None
        lock_fd2 = None
        try:
            lock_fd1 = open("test_scheduler.lock", "w")
            fcntl.flock(lock_fd1, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_fd2 = open("test_scheduler.lock", "w")
            with pytest.raises(IOError):
                fcntl.flock(lock_fd2, fcntl.LOCK_EX | fcntl.LOCK_NB)
        finally:
            if lock_fd1:
                fcntl.flock(lock_fd1, fcntl.LOCK_UN)
                lock_fd1.close()
            if lock_fd2:
                lock_fd2.close()
            if os.path.exists("test_scheduler.lock"):
                os.remove("test_scheduler.lock")

    @pytest.mark.skipif(sys.platform == "win32", reason="fcntl not available on Windows")
    def test_lock_released_then_second_process_succeeds(self):
        import fcntl
        lock_fd = None
        try:
            lock_fd = open("test_scheduler.lock", "w")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
            lock_fd = None
            lock_fd = open("test_scheduler.lock", "w")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            assert True
        finally:
            if lock_fd:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()
            if os.path.exists("test_scheduler.lock"):
                os.remove("test_scheduler.lock")


class TestAddOrUpdateJob:

    def test_add_new_job(self, app):
        from app.scheduler import add_or_update_job, scheduler
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.name = "Test Task"
        mock_task.cron_expression = "0 9 * * *"
        with app.app_context():
            with patch.object(scheduler, "get_job", return_value=None):
                with patch.object(scheduler, "add_job") as mock_add:
                    add_or_update_job(mock_task)
                    mock_add.assert_called_once()

    def test_update_existing_job(self, app):
        from app.scheduler import add_or_update_job, scheduler
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.name = "Test Task"
        mock_task.cron_expression = "0 9 * * *"
        with app.app_context():
            with patch.object(scheduler, "get_job", return_value=MagicMock()):
                with patch.object(scheduler, "modify_job") as mock_modify:
                    add_or_update_job(mock_task)
                    mock_modify.assert_called_once()

    def test_invalid_cron_expression(self, app):
        from app.scheduler import add_or_update_job
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.name = "Test Task"
        mock_task.cron_expression = "invalid cron"
        with app.app_context():
            add_or_update_job(mock_task)


class TestInitScheduler:

    def test_init_scheduler_on_windows(self, app):
        from app.scheduler import init_scheduler, scheduler
        with app.app_context():
            with patch("app.scheduler.sys") as mock_sys:
                mock_sys.platform = "win32"
                with patch.object(scheduler, "init_app") as mock_init:
                    with patch.object(scheduler, "start") as mock_start:
                        init_scheduler(app)
                        mock_init.assert_called_once_with(app)
                        mock_start.assert_called_once()

    def test_init_scheduler_skips_when_lock_held(self, app):
        from app.scheduler import init_scheduler, scheduler
        with app.app_context():
            with patch("app.scheduler.fcntl") as mock_fcntl:
                mock_fcntl.flock.side_effect = IOError("Resource temporarily unavailable")
                mock_fcntl.LOCK_EX = 2
                mock_fcntl.LOCK_NB = 4
                with patch("app.scheduler.sys") as mock_sys:
                    mock_sys.platform = "linux"
                    with patch("builtins.open", return_value=MagicMock()):
                        with patch.object(scheduler, "init_app") as mock_init:
                            with patch.object(scheduler, "start") as mock_start:
                                init_scheduler(app)
                                mock_init.assert_not_called()
                                mock_start.assert_not_called()