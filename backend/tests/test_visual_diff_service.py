"""
图像差异比较服务测试
"""

import os
import tempfile
from io import BytesIO

import pytest
from PIL import Image

from app.extensions import db
from app.services.screenshot_service import ScreenshotService
from app.services.visual_diff_service import VisualDiffService
from app.models.visual_baseline import VisualBaseline
from app.models.visual_diff import VisualDiff


def _make_png(width=100, height=100, color=(128, 128, 128)):
    """生成纯色 PNG 图片的二进制数据"""
    img = Image.new("RGB", (width, height), color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()


def _make_png_with_rect(width=100, height=100, base_color=(128, 128, 128),
                        rect_color=(255, 0, 0), rect_coords=(20, 20, 40, 40)):
    """生成带有矩形色块的 PNG 图片"""
    img = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle(rect_coords, fill=rect_color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()


from PIL import ImageDraw


@pytest.fixture
def screenshot_service(app):
    with app.app_context():
        db.session.rollback()
        db.session.remove()
        VisualBaseline.query.delete()
        db.session.commit()
        with tempfile.TemporaryDirectory() as tmpdir:
            yield ScreenshotService(base_path=tmpdir)


@pytest.fixture
def visual_diff_service(app, screenshot_service):
    with app.app_context():
        yield VisualDiffService(screenshot_service=screenshot_service)


class TestVisualDiffServiceCompareImages:
    """测试图像对比功能"""

    def test_identical_images(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            image_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                image_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            result = visual_diff_service.compare_images(
                baseline.baseline_image_path, image_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert result["diff_percentage"] == 0.0
            assert result["is_pass"] == True
            assert result["similarity_score"] == 1.0
            assert result["diff_image_data"] is not None
            assert len(result["diff_image_data"]) > 0

    def test_different_images(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            current_data = _make_png(100, 100, (0, 0, 0))
            result = visual_diff_service.compare_images(
                baseline.baseline_image_path, current_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert result["diff_percentage"] > 0
            assert result["similarity_score"] < 1.0
            assert result["is_pass"] == False

    def test_threshold_pass(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            # 微小差异
            current_data = _make_png_with_rect(
                100, 100, (128, 128, 128), (130, 130, 130), (0, 0, 2, 2)
            )
            result = visual_diff_service.compare_images(
                baseline.baseline_image_path, current_data,
                baseline_base_path=screenshot_service.base_path, diff_threshold=5.0,
            )
            assert result["diff_percentage"] <= 5.0
            assert result["is_pass"] == True

    def test_threshold_fail(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            # 大面积差异
            current_data = _make_png(100, 100, (0, 0, 0))
            result = visual_diff_service.compare_images(
                baseline.baseline_image_path, current_data,
                baseline_base_path=screenshot_service.base_path, diff_threshold=1.0,
            )
            assert result["diff_percentage"] > 1.0
            assert result["is_pass"] == False

    def test_different_sizes(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            current_data = _make_png(200, 150, (128, 128, 128))
            result = visual_diff_service.compare_images(
                baseline.baseline_image_path, current_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert result["baseline_size"] == (100, 100)
            assert result["current_size"] == (200, 150)

    def test_missing_baseline_file(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            image_data = _make_png()
            with pytest.raises(FileNotFoundError):
                visual_diff_service.compare_images(
                    "nonexistent/path.png", image_data,
                    baseline_base_path=screenshot_service.base_path,
                )

    def test_diff_image_is_valid_png(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            current_data = _make_png(100, 100, (0, 0, 0))
            result = visual_diff_service.compare_images(
                baseline.baseline_image_path, current_data,
                baseline_base_path=screenshot_service.base_path,
            )
            diff_img = Image.open(BytesIO(result["diff_image_data"]))
            assert diff_img.format == "PNG"
            assert diff_img.size == (100, 100)


class TestVisualDiffServiceCompareAndRecord:
    """测试对比并记录功能"""

    def test_record_pass(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            image_data = _make_png(100, 100, (128, 128, 128))
            screenshot_service.save_baseline_screenshot(
                image_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            visual_diff = visual_diff_service.compare_and_record(
                test_run_id=1, test_case_id=10, test_type="web",
                step_index=0, current_image_data=image_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert visual_diff is not None
            assert visual_diff.status == "visual_pass"
            assert float(visual_diff.diff_percentage) == 0.0

    def test_record_fail(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            current_data = _make_png(100, 100, (0, 0, 0))
            visual_diff = visual_diff_service.compare_and_record(
                test_run_id=1, test_case_id=10, test_type="web",
                step_index=0, current_image_data=current_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert visual_diff is not None
            assert visual_diff.status == "visual_fail"
            assert float(visual_diff.diff_percentage) > 0

    def test_no_baseline_returns_none(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            image_data = _make_png()
            result = visual_diff_service.compare_and_record(
                test_run_id=1, test_case_id=999, test_type="web",
                step_index=0, current_image_data=image_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert result is None

    def test_diff_image_saved(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            current_data = _make_png(100, 100, (0, 0, 0))
            visual_diff = visual_diff_service.compare_and_record(
                test_run_id=1, test_case_id=10, test_type="web",
                step_index=0, current_image_data=current_data,
                baseline_base_path=screenshot_service.base_path,
            )
            assert visual_diff.diff_image_path is not None
            full_path = os.path.join(screenshot_service.base_path, visual_diff.diff_image_path)
            assert os.path.exists(full_path)

    def test_custom_threshold(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            baseline_data = _make_png(100, 100, (128, 128, 128))
            screenshot_service.save_baseline_screenshot(
                baseline_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            # 相同图片，但阈值设为 99.0，验证阈值参数被正确存储
            visual_diff = visual_diff_service.compare_and_record(
                test_run_id=1, test_case_id=10, test_type="web",
                step_index=0, current_image_data=baseline_data,
                threshold=99.0,
                baseline_base_path=screenshot_service.base_path,
            )
            assert visual_diff.status == "visual_pass"
            assert visual_diff.threshold == 99.0

    def test_record_with_baseline_id(self, app, screenshot_service, visual_diff_service):
        with app.app_context():
            image_data = _make_png(100, 100, (128, 128, 128))
            baseline = screenshot_service.save_baseline_screenshot(
                image_data, project_id=1, test_case_id=10, step_index=0, test_type="web"
            )
            visual_diff = visual_diff_service.compare_and_record(
                test_run_id=1, test_case_id=10, test_type="web",
                step_index=0, current_image_data=image_data,
                baseline_id=baseline.id,
                baseline_base_path=screenshot_service.base_path,
            )
            assert visual_diff is not None
            assert visual_diff.baseline_id == baseline.id
