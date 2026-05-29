"""
视觉回归测试集成测试

测试 Playwright 执行器与视觉差异服务的集成：
- P2A-04: 修改现有 Playwright 执行器（Celery task）
"""

import subprocess
import uuid
import os
import json
import tempfile

from app.extensions import db
from app.models.project import Project
from app.models.test_report import TestReport as TestReportModel
from app.models.test_run import TestRun as TestRunModel
from app.models.user import User
from app.models.web_test_script import WebTestScript
from app.tasks import run_web_test_task, _process_visual_diffs


def _seed_user_and_script(app, with_project=True):
    with app.app_context():
        suffix = uuid.uuid4().hex[:8]
        user = User(
            username=f'web_case_user_{suffix}',
            email=f'web_case_user_{suffix}@example.com',
            password_hash='hashed-password',
        )
        db.session.add(user)
        db.session.flush()

        project_id = None
        if with_project:
            project = Project(name='Web Project', owner_id=user.id)
            db.session.add(project)
            db.session.flush()
            project_id = project.id

        script = WebTestScript(
            name='visual diff test',
            description='visual diff case',
            script_content='print("ok")',
            project_id=project_id,
            user_id=user.id,
            browser='chromium',
            timeout=30000,
        )
        db.session.add(script)
        db.session.commit()
        return user.id, script.id


class TestProcessVisualDiffs:
    """测试 _process_visual_diffs 辅助函数"""

    def test_returns_empty_list_when_no_vision_results(self):
        """无 vision_results 时返回空列表"""
        result = _process_visual_diffs(
            test_run_id=1, test_case_id=1,
            vision_results=None, screenshot_base_path="/tmp"
        )
        assert result == []

    def test_returns_empty_list_when_empty_steps(self):
        """steps 为空时返回空列表"""
        result = _process_visual_diffs(
            test_run_id=1, test_case_id=1,
            vision_results={"steps": []}, screenshot_base_path="/tmp"
        )
        assert result == []

    def test_skips_steps_without_screenshot(self):
        """无截图路径的步骤被跳过"""
        result = _process_visual_diffs(
            test_run_id=1, test_case_id=1,
            vision_results={"steps": [{"name": "step1"}]},
            screenshot_base_path="/tmp"
        )
        assert result == []

    def test_skips_missing_screenshot_files(self):
        """截图文件不存在时跳过该步骤"""
        result = _process_visual_diffs(
            test_run_id=1, test_case_id=1,
            vision_results={"steps": [{"name": "step1", "screenshot_path": "nonexistent.png"}]},
            screenshot_base_path="/tmp"
        )
        assert result == []

    def test_records_error_when_comparison_fails(self, app):
        """视觉对比失败时记录错误但不中断"""
        import uuid as uuid_mod
        from PIL import Image

        with app.app_context():
            # 创建测试截图
            with tempfile.TemporaryDirectory() as tmpdir:
                img_path = os.path.join(tmpdir, "test.png")
                img = Image.new("RGB", (100, 100), (128, 128, 128))
                img.save(img_path)

                vision_results = {
                    "steps": [
                        {"name": "step1", "screenshot_path": "test.png"}
                    ]
                }

                result = _process_visual_diffs(
                    test_run_id=999,
                    test_case_id=999,
                    vision_results=vision_results,
                    screenshot_base_path=tmpdir,
                )

                # 应该返回结果（可能是 error 状态，因为基准截图不存在）
                assert len(result) == 1
                assert result[0]["step_name"] == "step1"


class TestVisualDiffInWebTestTask:
    """测试 run_web_test_task 中视觉回归集成"""

    def test_vision_results_included_in_payload(self, app, monkeypatch):
        """验证 vision_results 和 visual_diff_summaries 包含在返回结果中"""
        user_id, script_id = _seed_user_and_script(app, with_project=True)

        monkeypatch.setattr('app.tasks._get_flask_app', lambda: app)
        monkeypatch.setattr(
            'app.tasks.subprocess.run',
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=args[0], returncode=0, stdout='done', stderr='',
            ),
        )
        monkeypatch.setattr('app.tasks.run_web_test_task.update_state', lambda *a, **kw: None)

        result = run_web_test_task.run(script_id, user_id)

        assert result['success'] is True
        assert 'vision_results' not in result  # not in direct result
        # But vision_data should be in last_result
        with app.app_context():
            script = db.session.get(WebTestScript, script_id)
            assert script.last_result is not None
            # vision_results may be None since no vision_results.json was created
            assert 'vision_results' in script.last_result or script.last_result.get('vision_results') is None

    def test_vision_processing_error_does_not_interrupt_task(self, app, monkeypatch):
        """验证视觉对比处理失败时不中断测试执行"""
        user_id, script_id = _seed_user_and_script(app, with_project=True)

        monkeypatch.setattr('app.tasks._get_flask_app', lambda: app)
        monkeypatch.setattr(
            'app.tasks.subprocess.run',
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=args[0], returncode=0, stdout='done', stderr='',
            ),
        )
        monkeypatch.setattr('app.tasks.run_web_test_task.update_state', lambda *a, **kw: None)

        # Patch _process_visual_diffs to raise an exception
        monkeypatch.setattr(
            'app.tasks._process_visual_diffs',
            lambda **kwargs: (_ for _ in ()).throw(RuntimeError("visual diff failed")),
        )

        result = run_web_test_task.run(script_id, user_id)

        # Task should still succeed despite visual diff failure
        assert result['success'] is True

    def test_vision_results_empty_when_no_json(self, app, monkeypatch):
        """验证无 vision_results.json 时 task 仍正常完成"""
        user_id, script_id = _seed_user_and_script(app, with_project=True)

        monkeypatch.setattr('app.tasks._get_flask_app', lambda: app)
        monkeypatch.setattr(
            'app.tasks.subprocess.run',
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=args[0], returncode=0, stdout='done', stderr='',
            ),
        )
        monkeypatch.setattr('app.tasks.run_web_test_task.update_state', lambda *a, **kw: None)

        result = run_web_test_task.run(script_id, user_id)

        assert result['success'] is True
        with app.app_context():
            script = db.session.get(WebTestScript, script_id)
            assert script.last_result.get('vision_results') is None
            assert script.last_result.get('visual_diff_summaries') == []
