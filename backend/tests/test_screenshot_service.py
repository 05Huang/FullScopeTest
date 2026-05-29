"""
截图存储服务测试
"""

import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest
from app.extensions import db
from app.services.screenshot_service import ScreenshotService
from app.models.visual_baseline import VisualBaseline


@pytest.fixture
def screenshot_service(app):
    """创建截图服务实例"""
    with app.app_context():
        # 清理数据库
        db.session.rollback()
        db.session.remove()
        VisualBaseline.query.delete()
        db.session.commit()

        with tempfile.TemporaryDirectory() as tmpdir:
            service = ScreenshotService(base_path=tmpdir)
            yield service


class TestScreenshotService:
    """测试截图存储服务"""

    def test_save_screenshot(self, app, screenshot_service):
        """测试保存截图"""
        with app.app_context():
            image_data = b'fake png data'
            path = screenshot_service.save_screenshot(
                image_data,
                project_id=1,
                test_run_id=100,
                step_index=0
            )
            assert path is not None
            assert '1' in path
            assert '100' in path
            assert 'step_0.png' in path

    def test_save_baseline_screenshot_new(self, app, screenshot_service):
        """测试保存新的基准截图"""
        with app.app_context():
            image_data = b'fake png data'
            baseline = screenshot_service.save_baseline_screenshot(
                image_data,
                project_id=1,
                test_case_id=10,
                step_index=0,
                test_type='web'
            )
            assert baseline is not None
            assert baseline.test_case_id == 10
            assert baseline.step_index == 0
            assert baseline.version == 1
            assert baseline.status == 'active'

    def test_save_baseline_screenshot_update(self, app, screenshot_service):
        """测试更新现有基准截图"""
        with app.app_context():
            # 创建初始基准
            image_data1 = b'fake png data 1'
            baseline1 = screenshot_service.save_baseline_screenshot(
                image_data1,
                project_id=1,
                test_case_id=10,
                step_index=0,
                test_type='web'
            )
            assert baseline1.version == 1

            # 更新基准
            image_data2 = b'fake png data 2'
            baseline2 = screenshot_service.save_baseline_screenshot(
                image_data2,
                project_id=1,
                test_case_id=10,
                step_index=0,
                test_type='web'
            )
            assert baseline2.id == baseline1.id
            assert baseline2.version == 2

    def test_get_baseline(self, app, screenshot_service):
        """测试获取基准截图"""
        with app.app_context():
            # 创建基准
            image_data = b'fake png data'
            screenshot_service.save_baseline_screenshot(
                image_data,
                project_id=1,
                test_case_id=10,
                step_index=0,
                test_type='web'
            )

            # 获取基准
            baseline = screenshot_service.get_baseline(
                test_case_id=10,
                step_index=0,
                test_type='web'
            )
            assert baseline is not None
            assert baseline.test_case_id == 10

    def test_get_baseline_not_found(self, app, screenshot_service):
        """测试获取不存在的基准截图"""
        with app.app_context():
            baseline = screenshot_service.get_baseline(
                test_case_id=999,
                step_index=0,
                test_type='web'
            )
            assert baseline is None

    def test_approve_baseline(self, app, screenshot_service):
        """测试批准基准截图"""
        with app.app_context():
            # 创建基准
            image_data = b'fake png data'
            baseline = screenshot_service.save_baseline_screenshot(
                image_data,
                project_id=1,
                test_case_id=10,
                step_index=0,
                test_type='web'
            )

            # 批准基准
            approved = screenshot_service.approve_baseline(
                baseline.id,
                approved_by=1
            )
            assert approved.approved_by == 1
            assert approved.approved_at is not None

    def test_delete_baseline(self, app, screenshot_service):
        """测试删除基准截图"""
        with app.app_context():
            # 创建基准
            image_data = b'fake png data'
            baseline = screenshot_service.save_baseline_screenshot(
                image_data,
                project_id=1,
                test_case_id=10,
                step_index=0,
                test_type='web'
            )

            # 删除基准
            result = screenshot_service.delete_baseline(baseline.id)
            assert result is True

            # 验证已标记为 deprecated
            deleted = VisualBaseline.query.get(baseline.id)
            assert deleted.status == 'deprecated'

    def test_delete_baseline_not_found(self, app, screenshot_service):
        """测试删除不存在的基准截图"""
        with app.app_context():
            result = screenshot_service.delete_baseline(999)
            assert result is False

    def test_get_diffs(self, app, screenshot_service):
        """测试查询差异记录"""
        with app.app_context():
            from app.models.visual_diff import VisualDiff

            # 创建测试数据
            diff = VisualDiff(
                test_run_id=1,
                baseline_id=1,
                test_case_id=10,
                test_type='web',
                step_index=0,
                current_image_path='test/current.png',
                diff_percentage=5.0,
                status='pending'
            )
            db.session.add(diff)
            db.session.commit()

            # 查询差异记录
            diffs = screenshot_service.get_diffs(test_run_id=1)
            assert len(diffs) == 1
            assert diffs[0].test_run_id == 1

    def test_screenshot_directory_creation(self, app):
        """测试截图目录自动创建"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, 'a', 'b', 'c')
            service = ScreenshotService(base_path=nested_path)
            assert os.path.exists(nested_path)