"""
数据归档与清理服务测试

覆盖：保留策略配置、清理逻辑、截图清理、手动触发
"""

import os
import tempfile
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest


class TestRetentionConfig:
    """保留策略配置测试"""

    def test_default_raw_retention_days(self):
        from app.services.data_retention_service import RAW_RETENTION_DAYS
        assert RAW_RETENTION_DAYS == 90

    def test_default_attachment_retention_days(self):
        from app.services.data_retention_service import ATTACHMENT_RETENTION_DAYS
        assert ATTACHMENT_RETENTION_DAYS == 30

    def test_default_summary_retention_days(self):
        from app.services.data_retention_service import SUMMARY_RETENTION_DAYS
        assert SUMMARY_RETENTION_DAYS == 365

    def test_custom_retention_days(self, monkeypatch):
        monkeypatch.setenv("RETENTION_RAW_DAYS", "60")
        # 重新加载模块以读取新的环境变量
        import importlib
        import app.services.data_retention_service as mod
        importlib.reload(mod)
        assert mod.RAW_RETENTION_DAYS == 60

    def test_invalid_retention_days_falls_back_to_default(self, monkeypatch):
        monkeypatch.setenv("RETENTION_RAW_DAYS", "not_a_number")
        import importlib
        import app.services.data_retention_service as mod
        importlib.reload(mod)
        assert mod.RAW_RETENTION_DAYS == 90


class TestRawTestRunCleanup:
    """原始测试执行记录清理测试"""

    def test_cleanup_returns_stats_dict(self, app):
        from app.services.data_retention_service import cleanup_raw_test_runs
        with app.app_context():
            result = cleanup_raw_test_runs()
        assert "deleted_runs" in result
        assert "cutoff_date" in result
        assert isinstance(result["deleted_runs"], int)

    def test_cleanup_does_not_delete_recent_runs(self, app):
        """不应删除未过期的执行记录"""
        from app.extensions import db
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.models.user import User
        from app.services.data_retention_service import cleanup_raw_test_runs

        with app.app_context():
            user = User(username="retention_user", email="ret@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            project = Project(name="RetProj", owner_id=user.id)
            db.session.add(project)
            db.session.flush()
            recent_run = TestRun(
                project_id=project.id,
                test_type="api",
                status="completed",
                created_at=datetime.utcnow(),
            )
            db.session.add(recent_run)
            db.session.commit()
            run_id = recent_run.id

            result = cleanup_raw_test_runs()
            assert result["deleted_runs"] == 0

            still_exists = db.session.get(TestRun, run_id)
            assert still_exists is not None

            # 清理测试数据
            db.session.delete(recent_run)
            db.session.delete(project)
            db.session.delete(user)
            db.session.commit()


class TestScreenshotCleanup:
    """截图文件清理测试"""

    def test_cleanup_empty_directory(self):
        from app.services.data_retention_service import cleanup_old_screenshots
        with tempfile.TemporaryDirectory() as tmpdir:
            result = cleanup_old_screenshots(tmpdir)
        assert result["deleted_files"] == 0
        assert result["freed_bytes"] == 0

    def test_cleanup_nonexistent_directory(self):
        from app.services.data_retention_service import cleanup_old_screenshots
        result = cleanup_old_screenshots("/nonexistent/path/12345")
        assert result["deleted_files"] == 0

    def test_cleanup_old_files(self):
        """清理超过保留期的文件"""
        from app.services.data_retention_service import cleanup_old_screenshots, ATTACHMENT_RETENTION_DAYS
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建一个"过期"文件（修改时间为 60 天前）
            old_file = os.path.join(tmpdir, "old_screenshot.png")
            with open(old_file, "w") as f:
                f.write("old content")
            old_time = time.time() - (ATTACHMENT_RETENTION_DAYS + 10) * 86400
            os.utime(old_file, (old_time, old_time))

            # 创建一个"新"文件
            new_file = os.path.join(tmpdir, "new_screenshot.png")
            with open(new_file, "w") as f:
                f.write("new content")

            result = cleanup_old_screenshots(tmpdir)
            assert result["deleted_files"] == 1
            assert not os.path.exists(old_file)
            assert os.path.exists(new_file)


class TestFullCleanup:
    """完整清理流程测试"""

    def test_run_full_cleanup_returns_all_stats(self, app):
        from app.services.data_retention_service import run_full_cleanup
        with app.app_context():
            with tempfile.TemporaryDirectory() as tmpdir:
                result = run_full_cleanup(storage_path=tmpdir)
        assert "raw_runs" in result
        assert "reports" in result
        assert "screenshots" in result
        assert "timestamp" in result
