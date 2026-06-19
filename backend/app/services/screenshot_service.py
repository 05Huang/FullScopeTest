"""
截图存储服务

管理视觉回归测试的截图存储和基准截图管理
"""

import os
from datetime import datetime, timezone
from flask import current_app
from ..extensions import db
from ..models.visual_baseline import VisualBaseline
from ..models.visual_diff import VisualDiff
from ..core.logging import get_logger

logger = get_logger(__name__)


class ScreenshotService:
    """截图存储服务"""

    def __init__(self, base_path=None):
        """
        初始化截图服务

        Args:
            base_path: 截图存储根目录，默认从配置中获取
        """
        self.base_path = base_path or current_app.config.get(
            'SCREENSHOT_STORAGE_PATH',
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads', 'screenshots')
        )
        os.makedirs(self.base_path, exist_ok=True)

    def save_screenshot(self, image_data, project_id, test_run_id, step_index, test_case_id=None):
        """
        保存截图到存储

        Args:
            image_data: 图片二进制数据
            project_id: 项目 ID
            test_run_id: 测试执行记录 ID
            step_index: 步骤索引
            test_case_id: 测试用例 ID（可选）

        Returns:
            str: 截图存储路径
        """
        # 构建存储路径: {project_id}/{test_run_id}/{step}.png
        relative_path = os.path.join(
            str(project_id),
            str(test_run_id),
            f'step_{step_index}.png'
        )
        full_path = os.path.join(self.base_path, relative_path)

        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # 保存文件
        with open(full_path, 'wb') as f:
            f.write(image_data)

        logger.info(
            "截图已保存",
            path=relative_path,
            size=len(image_data),
            project_id=project_id,
            test_run_id=test_run_id
        )

        return relative_path

    def save_baseline_screenshot(self, image_data, project_id, test_case_id, step_index, 
                                  test_type='web', viewport_width=None, viewport_height=None,
                                  device_pixel_ratio=None, full_page=False):
        """
        保存基准截图

        Args:
            image_data: 图片二进制数据
            project_id: 项目 ID
            test_case_id: 测试用例 ID
            step_index: 步骤索引
            test_type: 测试类型 (api/web/app)
            viewport_width: 视口宽度
            viewport_height: 视口高度
            device_pixel_ratio: 设备像素比
            full_page: 是否全页截图

        Returns:
            VisualBaseline: 创建或更新的基准截图记录
        """
        # 查找现有的基准
        existing = VisualBaseline.query.filter_by(
            test_case_id=test_case_id,
            step_index=step_index,
            test_type=test_type,
            status='active'
        ).first()

        if existing:
            # 更新现有基准
            relative_path = self.save_screenshot(
                image_data, project_id, 0, step_index, test_case_id
            )
            existing.baseline_image_path = relative_path
            existing.version = (existing.version or 1) + 1
            existing.viewport_width = viewport_width
            existing.viewport_height = viewport_height
            existing.device_pixel_ratio = device_pixel_ratio
            existing.full_page = full_page
            existing.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            db.session.commit()

            logger.info(
                "基准截图已更新",
                baseline_id=existing.id,
                version=existing.version
            )
            return existing
        else:
            # 创建新的基准
            relative_path = self.save_screenshot(
                image_data, project_id, 0, step_index, test_case_id
            )
            baseline = VisualBaseline(
                test_case_id=test_case_id,
                test_type=test_type,
                project_id=project_id,
                step_index=step_index,
                baseline_image_path=relative_path,
                viewport_width=viewport_width,
                viewport_height=viewport_height,
                device_pixel_ratio=device_pixel_ratio,
                full_page=full_page,
                status='active',
                version=1
            )
            db.session.add(baseline)
            db.session.commit()

            logger.info(
                "基准截图已创建",
                baseline_id=baseline.id,
                test_case_id=test_case_id,
                step_index=step_index
            )
            return baseline

    def get_baseline(self, test_case_id, step_index, test_type='web'):
        """
        获取基准截图

        Args:
            test_case_id: 测试用例 ID
            step_index: 步骤索引
            test_type: 测试类型

        Returns:
            VisualBaseline: 基准截图记录，如果没有则返回 None
        """
        return VisualBaseline.query.filter_by(
            test_case_id=test_case_id,
            step_index=step_index,
            test_type=test_type,
            status='active'
        ).first()

    def approve_baseline(self, baseline_id, approved_by):
        """
        批准基准截图

        Args:
            baseline_id: 基准截图 ID
            approved_by: 批准人用户 ID

        Returns:
            VisualBaseline: 更新后的基准截图记录
        """
        baseline = VisualBaseline.query.get(baseline_id)
        if not baseline:
            raise ValueError(f"基准截图 {baseline_id} 不存在")

        baseline.approved_by = approved_by
        baseline.approved_at = datetime.now(timezone.utc).replace(tzinfo=None)
        baseline.status = 'active'
        db.session.commit()

        logger.info(
            "基准截图已批准",
            baseline_id=baseline_id,
            approved_by=approved_by
        )
        return baseline

    def delete_baseline(self, baseline_id):
        """
        删除基准截图

        Args:
            baseline_id: 基准截图 ID

        Returns:
            bool: 是否成功删除
        """
        baseline = VisualBaseline.query.get(baseline_id)
        if not baseline:
            return False

        # 删除物理文件
        full_path = os.path.join(self.base_path, baseline.baseline_image_path)
        if os.path.exists(full_path):
            os.remove(full_path)

        # 软删除，标记为 deprecated
        baseline.status = 'deprecated'
        db.session.commit()

        logger.info("基准截图已删除", baseline_id=baseline_id)
        return True

    def get_diffs(self, test_run_id=None, test_case_id=None, status=None):
        """
        查询差异记录

        Args:
            test_run_id: 测试执行记录 ID
            test_case_id: 测试用例 ID
            status: 状态过滤

        Returns:
            list: 差异记录列表
        """
        query = VisualDiff.query

        if test_run_id:
            query = query.filter_by(test_run_id=test_run_id)
        if test_case_id:
            query = query.filter_by(test_case_id=test_case_id)
        if status:
            query = query.filter_by(status=status)

        return query.order_by(VisualDiff.created_at.desc()).all()