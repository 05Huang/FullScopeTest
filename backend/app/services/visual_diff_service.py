"""
图像差异比较服务

使用 Pillow + imagehash 计算感知哈希差异
使用像素级对比生成红色高亮差异图
输出 diff_percentage 和 diff_image
"""

import os
import io
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

from PIL import Image, ImageChops, ImageDraw
import imagehash

from ..core.logging import get_logger

logger = get_logger(__name__)


class VisualDiffService:
    """图像差异比较服务"""

    def __init__(self, screenshot_service=None, diff_storage_path=None):
        """
        初始化差异比较服务

        Args:
            screenshot_service: ScreenshotService 实例，用于读取基准截图
            diff_storage_path: 差异图存储根目录（兼容旧参数）
        """
        self.screenshot_service = screenshot_service
        self.diff_storage_path = diff_storage_path or (
            screenshot_service.base_path if screenshot_service else None
        )

    def compare_images(
        self,
        baseline_image_path: str = None,
        current_image_data: bytes = None,
        baseline_base_path: str = None,
        diff_threshold: float = 5.0,
        # 兼容旧 API 的参数名
        baseline_data: bytes = None,
        threshold: float = None,
        diff_storage_path: str = None,
    ) -> Dict[str, Any]:
        """
        对比两张图片，生成差异报告

        Args:
            baseline_image_path: 基准截图的相对路径（从数据库读取）
            current_image_data: 当前截图的二进制数据
            baseline_base_path: 基准截图存储根目录
            diff_threshold: 差异阈值 (%)，超过则判定为视觉失败

        Returns:
            dict: 包含 diff_percentage, diff_image_path, similarity_score,
                  is_pass, diff_image_data 等字段
        """
        # 兼容旧 API
        if threshold is not None:
            diff_threshold = threshold
        if baseline_data is not None and baseline_image_path is None:
            baseline_image_data = baseline_data
        else:
            baseline_image_data = None

        # 确定实际使用的存储路径
        base_path = baseline_base_path or self.diff_storage_path

        # 读取基准图片
        if baseline_image_data is not None:
            try:
                baseline_img = Image.open(io.BytesIO(baseline_image_data)).convert("RGBA")
            except Exception as e:
                logger.error("无法打开基准图片数据", error=str(e))
                return self._error_result(str(e))
        elif baseline_image_path:
            full_baseline_path = os.path.join(base_path, baseline_image_path)
            if not os.path.exists(full_baseline_path):
                raise FileNotFoundError(f"基准截图文件不存在: {full_baseline_path}")
            try:
                baseline_img = Image.open(full_baseline_path).convert("RGBA")
            except Exception as e:
                logger.error("无法打开基准截图", path=full_baseline_path, error=str(e))
                return self._error_result(str(e))
        else:
            return self._error_result("未提供基准图片")

        # 读取当前图片
        try:
            current_img = Image.open(io.BytesIO(current_image_data)).convert("RGBA")
        except Exception as e:
            logger.error("无法打开当前截图", error=str(e))
            return self._error_result(str(e))

        baseline_size = baseline_img.size
        current_size = current_img.size

        # 确保尺寸一致，以基准图片尺寸为准
        if baseline_img.size != current_img.size:
            current_img = current_img.resize(baseline_img.size, Image.LANCZOS)

        total_pixels = baseline_img.size[0] * baseline_img.size[1]

        # 1. 像素级对比 — 生成红色高亮差异图
        diff_image = self._generate_diff_image(baseline_img, current_img)

        # 2. 计算差异百分比
        diff_percentage = self._calculate_diff_percentage(baseline_img, current_img)

        # 3. 计算感知哈希相似度
        similarity_score = self._calculate_similarity(baseline_img, current_img)

        # 4. 统计差异像素数
        diff_pixel_count = int(diff_percentage / 100.0 * total_pixels)

        # 5. 判断是否通过视觉检查
        is_visual_pass = diff_percentage <= diff_threshold

        # 6. 保存差异图（如果有输出路径）
        diff_image_path = None
        diff_image_data = None
        if diff_storage_path:
            diff_image_path = self._save_diff_image(diff_image, diff_storage_path)
        else:
            diff_image_data = self._image_to_bytes(diff_image)

        logger.info(
            "图片对比完成",
            diff_percentage=round(diff_percentage, 2),
            similarity=round(similarity_score, 4),
            is_pass=is_visual_pass,
        )

        return {
            "diff_percentage": round(diff_percentage, 4),
            "diff_image_path": diff_image_path,
            "diff_image_data": diff_image_data,
            "similarity_score": round(similarity_score, 4),
            "is_pass": is_visual_pass,
            "diff_pixel_count": diff_pixel_count,
            "total_pixel_count": total_pixels,
            "baseline_size": baseline_size,
            "current_size": current_size,
        }

    def compare_and_record(
        self,
        test_run_id: int,
        test_case_id: int,
        test_type: str,
        step_index: int,
        current_image_data: bytes,
        baseline_base_path: str = None,
        threshold: float = 5.0,
        baseline_id: int = None,
    ):
        """
        对比基准截图和当前截图，并将结果写入 VisualDiff 表

        Args:
            test_run_id: 测试执行记录 ID
            test_case_id: 测试用例 ID
            test_type: 测试类型 (api/web/app)
            step_index: 步骤索引
            current_image_data: 当前截图的二进制数据
            baseline_base_path: 基准截图存储根目录
            threshold: 差异阈值 (%)
            baseline_id: 指定基准截图 ID（可选）

        Returns:
            VisualDiff: 差异记录，如果无基准则返回 None
        """
        from ..extensions import db
        from ..models.visual_baseline import VisualBaseline
        from ..models.visual_diff import VisualDiff

        # 查找基准
        if baseline_id:
            baseline = VisualBaseline.query.get(baseline_id)
        else:
            baseline = VisualBaseline.query.filter_by(
                test_case_id=test_case_id,
                step_index=step_index,
                test_type=test_type,
                status="active",
            ).first()

        if not baseline:
            logger.info("未找到基准截图，跳过对比", test_case_id=test_case_id, step_index=step_index)
            return None

        # 加载当前图片
        current_img = Image.open(io.BytesIO(current_image_data)).convert("RGBA")

        # 加载基准图片 — 使用 screenshot_service 的 base_path
        base_path = baseline_base_path or (
            self.screenshot_service.base_path if self.screenshot_service else self.diff_storage_path
        )
        baseline_full_path = os.path.join(base_path, baseline.baseline_image_path) if base_path else None

        try:
            if baseline_full_path and os.path.exists(baseline_full_path):
                baseline_img = Image.open(baseline_full_path).convert("RGBA")
            else:
                raise FileNotFoundError(f"基准截图不存在: {baseline_full_path}")
        except Exception as e:
            logger.error("读取基准截图失败", error=str(e), path=baseline_full_path)
            return None

        # 如果尺寸不同，以基准为准
        if baseline_img.size != current_img.size:
            current_img = current_img.resize(baseline_img.size, Image.LANCZOS)

        # 对比
        diff_image = self._generate_diff_image(baseline_img, current_img)
        diff_percentage = float(self._calculate_diff_percentage(baseline_img, current_img))
        similarity_score = float(self._calculate_similarity(baseline_img, current_img))
        total_pixels = baseline_img.size[0] * baseline_img.size[1]
        diff_pixel_count = int(diff_percentage / 100.0 * total_pixels)

        is_pass = diff_percentage <= threshold

        # 保存差异图
        project_id = baseline.project_id
        diff_filename = f"diff_{test_run_id}_step{step_index}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"
        diff_relative_path = os.path.join(str(project_id), str(test_run_id), diff_filename)

        if base_path:
            full_diff_path = os.path.join(base_path, diff_relative_path)
            self._save_diff_image(diff_image, full_diff_path)

        # 写入数据库
        visual_diff = VisualDiff(
            test_run_id=test_run_id,
            baseline_id=baseline.id,
            test_case_id=test_case_id,
            test_type=test_type,
            step_index=step_index,
            current_image_path="",  # 当前截图路径（由调用方管理）
            diff_image_path=diff_relative_path,
            diff_percentage=round(diff_percentage, 4),
            diff_pixel_count=diff_pixel_count,
            total_pixel_count=total_pixels,
            similarity_score=round(similarity_score, 4),
            viewport_width=baseline.viewport_width,
            viewport_height=baseline.viewport_height,
            threshold=threshold,
            status="visual_pass" if is_pass else "visual_fail",
        )
        db.session.add(visual_diff)
        db.session.commit()

        logger.info(
            "视觉差异对比已记录",
            visual_diff_id=visual_diff.id,
            diff_percentage=round(diff_percentage, 2),
            status=visual_diff.status,
        )

        return visual_diff

    def _generate_diff_image(
        self, baseline: Image.Image, current: Image.Image
    ) -> Image.Image:
        """
        生成红色高亮差异图

        将差异区域用半透明红色叠加在基准图上

        Args:
            baseline: 基准图片
            current: 当前图片

        Returns:
            Image.Image: 标注了差异区域的对比图
        """
        # 转为 RGB 以便对比
        baseline_rgb = baseline.convert("RGB")
        current_rgb = current.convert("RGB")

        # 计算像素差异
        diff = ImageChops.difference(baseline_rgb, current_rgb)

        # 转灰度后二值化，找出差异区域
        diff_gray = diff.convert("L")
        threshold_val = 30  # 像素值差异阈值
        diff_binary = diff_gray.point(lambda p: 255 if p > threshold_val else 0)

        # 创建红色半透明遮罩
        red_overlay = Image.new("RGBA", baseline.size, (255, 0, 0, 80))
        import numpy as np
        mask = Image.fromarray(
            np.array(diff_binary) // 255 * 255
        ).convert("L")

        # 合成：基准图 + 红色遮罩（仅差异区域）
        result = baseline.convert("RGBA")
        result.paste(red_overlay, mask=mask)

        return result

    def _calculate_diff_percentage(
        self, baseline: Image.Image, current: Image.Image
    ) -> float:
        """
        计算差异百分比（像素级）

        Args:
            baseline: 基准图片
            current: 当前图片

        Returns:
            float: 差异百分比 (0-100)
        """
        import numpy as np

        baseline_arr = np.array(baseline.convert("RGB"))
        current_arr = np.array(current.convert("RGB"))

        # 计算绝对差值
        diff = np.abs(baseline_arr.astype(int) - current_arr.astype(int))

        # 阈值：像素差异超过 30 视为不同
        pixel_diff = np.any(diff > 30, axis=2)

        total_pixels = pixel_diff.size
        diff_pixels = np.sum(pixel_diff)

        return (diff_pixels / total_pixels) * 100.0 if total_pixels > 0 else 0.0

    def _calculate_similarity(
        self, baseline: Image.Image, current: Image.Image
    ) -> float:
        """
        计算感知哈希相似度

        Args:
            baseline: 基准图片
            current: 当前图片

        Returns:
            float: 相似度 (0-1)，1 表示完全相同
        """
        hash_baseline = imagehash.phash(baseline.convert("RGB"))
        hash_current = imagehash.phash(current.convert("RGB"))

        # hamming distance -> 相似度
        max_distance = hash_baseline.hash.size  # 64 位哈希
        distance = hash_baseline - hash_current
        similarity = 1.0 - (distance / max_distance)

        return max(0.0, min(1.0, similarity))

    def _save_diff_image(self, image: Image.Image, path: str) -> str:
        """
        保存差异图到磁盘

        Args:
            image: PIL Image 对象
            path: 输出文件路径

        Returns:
            str: 保存的相对路径
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image.save(path, "PNG")
        return path

    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """
        将 PIL Image 转为 PNG 二进制数据

        Args:
            image: PIL Image 对象

        Returns:
            bytes: PNG 二进制数据
        """
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return buf.getvalue()

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """生成错误结果字典"""
        return {
            "diff_percentage": 100.0,
            "diff_image_path": None,
            "diff_image_data": None,
            "similarity_score": 0.0,
            "is_pass": False,
            "diff_pixel_count": 0,
            "total_pixel_count": 0,
            "error": error_msg,
        }
