"""Web 测试异步任务"""

from app.extensions import celery, db
from app.models.web_test_script import WebTestScript
from app.models.test_run import TestRun
from app.models.test_report import TestReport
from app.core.logging import get_logger
from app.core.metrics import record_task_success, record_task_failure
import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

from app.utils.sandbox import execute_script, check_script_safety
from .common import _get_flask_app

logger = get_logger(__name__)


def _build_web_case_result(script, success, duration, result_payload):
    """Build a report-friendly result item for a single web script run."""
    payload = result_payload or {}
    stdout = payload.get('stdout') or ''
    stderr = payload.get('stderr') or ''
    error_message = payload.get('error')
    if not error_message and not success and stderr:
        error_message = stderr.strip()[:1000]

    attachments = []
    if stdout:
        attachments.append({
            'name': 'stdout',
            'type': 'text',
            'content': stdout[:2000],
        })
    if stderr:
        attachments.append({
            'name': 'stderr',
            'type': 'text',
            'content': stderr[:2000],
        })

    return {
        'case_id': script.id,
        'name': script.name,
        'passed': success,
        'status_code': None,
        'response_time': round((duration or 0) * 1000, 2),
        'error': error_message,
        'attachments': attachments,
    }


def _finalize_web_test_run(script, test_run, success, duration, result_payload):
    """
    Persist WebTestScript status and optional TestRun/TestReport records.

    Returns:
        tuple[int | None, int | None]: (test_run_id, report_id)
    """
    script.status = 'passed' if success else 'failed'
    script.last_status = script.status
    script.last_run_duration = duration
    script.last_result = result_payload

    report_id = None
    test_run_id = None

    if test_run:
        case_result = _build_web_case_result(
            script=script,
            success=success,
            duration=duration,
            result_payload=result_payload,
        )
        test_run.status = 'success' if success else 'failed'
        test_run.passed = 1 if success else 0
        test_run.failed = 0 if success else 1
        test_run.error = 0 if success else 1
        test_run.duration = duration
        test_run.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        test_run.results = [case_result]
        test_run_id = test_run.id

        report = TestReport(
            test_run_id=test_run.id,
            project_id=test_run.project_id,
            test_type='web',
            title=f'{script.name} - Web Test Report',
            summary={
                'total': 1,
                'passed': 1 if success else 0,
                'failed': 0 if success else 1,
                'success_rate': 100 if success else 0,
                'duration': round(duration, 2),
                'environment': script.browser or 'chromium',
            },
            report_data={
                'script': {
                    'id': script.id,
                    'name': script.name,
                    'target_url': script.target_url,
                    'browser': script.browser,
                },
                'results': [case_result],
                'execution': {
                    'success': success,
                    'duration': duration,
                },
            },
            status='generated',
        )
        db.session.add(report)
        db.session.flush()
        report_id = report.id

    db.session.commit()
    return test_run_id, report_id


def _process_visual_diffs(
    test_run_id: int,
    test_case_id: int,
    vision_results: Dict[str, Any],
    screenshot_base_path: str,
    visual_threshold: float = 5.0,
) -> List[Dict[str, Any]]:
    """
    处理视觉回归测试结果：将截图与基准对比，写入 VisualDiff 表。

    即使视觉差异超过阈值也 **不中断** 测试执行，仅标记该步骤为视觉失败。

    Args:
        test_run_id: 测试执行记录 ID
        test_case_id: 测试用例 ID（即 script_id）
        vision_results: vision_results.json 的内容
        screenshot_base_path: 截图存储根目录
        visual_threshold: 差异阈值 (%)

    Returns:
        list[dict]: 每个步骤的视觉对比摘要
    """
    if not vision_results:
        return []

    from app.services.visual_diff_service import VisualDiffService

    diff_service = VisualDiffService(diff_storage_path=screenshot_base_path)
    steps = vision_results.get('steps') or []
    summaries = []

    for idx, step in enumerate(steps):
        screenshot_path = step.get('screenshot_path') or step.get('path')
        step_name = step.get('name') or step.get('description') or f'step_{idx}'

        if not screenshot_path:
            continue

        # 读取当前截图
        full_screenshot_path = os.path.join(screenshot_base_path, screenshot_path)
        if not os.path.exists(full_screenshot_path):
            logger.warning("截图文件不存在，跳过视觉对比", path=full_screenshot_path)
            continue

        try:
            with open(full_screenshot_path, 'rb') as f:
                current_image_data = f.read()
        except Exception as e:
            logger.error("读取截图文件失败", path=full_screenshot_path, error=str(e))
            continue

        # 调用视觉差异服务进行对比并记录
        try:
            visual_diff = diff_service.compare_and_record(
                test_run_id=test_run_id,
                test_case_id=test_case_id,
                test_type='web',
                step_index=idx,
                current_image_data=current_image_data,
                threshold=visual_threshold,
            )

            summary = {
                'step_index': idx,
                'step_name': step_name,
                'screenshot_path': screenshot_path,
                'status': 'skipped',
            }

            if visual_diff:
                summary.update({
                    'diff_percentage': visual_diff.diff_percentage,
                    'status': visual_diff.status,
                    'visual_diff_id': visual_diff.id,
                })
                if visual_diff.status == 'visual_fail':
                    logger.warning(
                        "步骤视觉差异超标",
                        step_index=idx,
                        diff_percentage=visual_diff.diff_percentage,
                        threshold=visual_threshold,
                    )

            summaries.append(summary)
        except Exception as e:
            logger.error("视觉对比处理失败", step_index=idx, error=str(e))
            summaries.append({
                'step_index': idx,
                'step_name': step_name,
                'screenshot_path': screenshot_path,
                'status': 'error',
                'error': str(e),
            })

    return summaries


@celery.task(
    bind=True,
    name='tasks.run_web_test',
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    autoretry_for=(IOError, OSError, TimeoutError),
)
def run_web_test_task(self, script_id, user_id):
    """Run a web script asynchronously and persist unified reporting records."""
    task_start_time = time.time()
    with _get_flask_app().app_context():
        script = None
        test_run = None
        work_dir = None

        try:
            script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
            if not script:
                record_task_failure('run_web_test', time.time() - task_start_time)
                return {
                    'success': False,
                    'error': 'Script not found',
                }

            script.status = 'running'
            script.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)

            # Create a unified test run when script is bound to a project.
            if script.project_id:
                test_run = TestRun(
                    project_id=script.project_id,
                    test_type='web',
                    test_object_id=script.id,
                    test_object_name=script.name,
                    status='running',
                    total_cases=1,
                    passed=0,
                    failed=0,
                    skipped=0,
                    error=0,
                    started_at=datetime.now(timezone.utc).replace(tzinfo=None),
                    triggered_by='manual',
                    triggered_user_id=user_id,
                )
                db.session.add(test_run)

            db.session.commit()

            self.update_state(state='PROGRESS', meta={'status': 'Running web test script...'})

            # 准备工作目录
            work_dir = os.path.join(os.path.dirname(_get_flask_app().root_path), 'data', 'web_tests', str(script_id))
            os.makedirs(work_dir, exist_ok=True)

            # 通过沙箱执行脚本（AST 检查 + 子进程隔离 + 审计日志）
            sandbox_result = execute_script(
                script_content=script.script_content,
                user_id=user_id,
                timeout=int(script.timeout / 1000) if script.timeout else 300,
                work_dir=work_dir,
                script_id=script_id,
                script_type="web",
            )

            try:
                duration = sandbox_result['duration']
                success = sandbox_result['success']
                result_stdout = sandbox_result['stdout']
                result_stderr = sandbox_result['stderr']
                result_returncode = sandbox_result.get('return_code', 1)

                vision_results_path = os.path.join(work_dir, 'vision_results.json')
                vision_data = None
                if os.path.exists(vision_results_path):
                    try:
                        with open(vision_results_path, 'r', encoding='utf-8') as f:
                            vision_data = json.load(f)
                    except Exception:
                        pass

                # 视觉回归测试：处理截图对比
                visual_diff_summaries = []
                if vision_data and test_run:
                    try:
                        visual_diff_summaries = _process_visual_diffs(
                            test_run_id=test_run.id,
                            test_case_id=script.id,
                            vision_results=vision_data,
                            screenshot_base_path=work_dir,
                        )
                    except Exception as ve:
                        logger.error("视觉回归处理失败", error=str(ve))

                run_payload = {
                    'success': success,
                    'duration': duration,
                    'stdout': result_stdout,
                    'stderr': result_stderr,
                    'return_code': result_returncode,
                    'vision_results': vision_data,
                    'visual_diff_summaries': visual_diff_summaries,
                    'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                }
                test_run_id, report_id = _finalize_web_test_run(
                    script=script,
                    test_run=test_run,
                    success=success,
                    duration=duration,
                    result_payload=run_payload,
                )

                if success:
                    record_task_success('run_web_test', time.time() - task_start_time)
                else:
                    record_task_failure('run_web_test', time.time() - task_start_time)

                return {
                    'success': success,
                    'script_id': script_id,
                    'test_run_id': test_run_id,
                    'report_id': report_id,
                    'duration': duration,
                    'stdout': result_stdout,
                    'stderr': result_stderr,
                    'return_code': result_returncode,
                }

            except Exception as e:
                if script:
                    vision_data = None
                    try:
                        if work_dir:
                            vision_results_path = os.path.join(work_dir, 'vision_results.json')
                            if os.path.exists(vision_results_path):
                                with open(vision_results_path, 'r', encoding='utf-8') as f:
                                    vision_data = json.load(f)
                    except Exception:
                        pass

                    is_timeout = 'timeout' in str(e).lower() or 'TimeoutExpired' in type(e).__name__
                    run_payload = {
                        'success': False,
                        'error': str(e),
                        'vision_results': vision_data,
                        'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                    }
                    timeout_seconds = script.timeout / 1000 if script.timeout else 0
                    test_run_id, report_id = _finalize_web_test_run(
                        script=script,
                        test_run=test_run,
                        success=False,
                        duration=timeout_seconds if is_timeout else 0,
                        result_payload=run_payload,
                    )
                else:
                    test_run_id, report_id = None, None

                record_task_failure('run_web_test', time.time() - task_start_time)
                return {
                    'success': False,
                    'error': str(e),
                    'test_run_id': test_run_id,
                    'report_id': report_id,
                }

        except Exception as outer_e:
            logger.error("Web 测试任务异常", error=str(outer_e), script_id=script_id)
            record_task_failure('run_web_test', time.time() - task_start_time)
            return {
                'success': False,
                'error': str(outer_e),
            }

