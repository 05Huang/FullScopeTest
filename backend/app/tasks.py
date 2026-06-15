"""
Celery 异步任务模块

包含 Web 测试、性能测试等异步任务
"""

from app.extensions import celery, db
from app.models.web_test_script import WebTestScript
from app.models.perf_test_scenario import PerfTestScenario
from app.models.test_run import TestRun
from app.models.test_report import TestReport
from app.core.logging import get_logger
from app.core.metrics import record_task_success, record_task_failure
import subprocess
import tempfile
import sys
import time
import os
import json
import threading
import queue
from datetime import datetime
from typing import Optional, Dict, Any, List

from app.utils.sandbox import execute_script, check_script_safety

logger = get_logger(__name__)


_flask_app_cache = None


def _get_flask_app():
    """延迟获取 Flask 应用实例，避免循环导入（缓存复用）"""
    global _flask_app_cache
    if _flask_app_cache is None:
        from app import create_app
        _flask_app_cache = create_app()
    return _flask_app_cache


class RealtimeStatsCollector:
    """实时统计数据收集器"""

    def __init__(self):
        self.request_count = 0
        self.failure_count = 0
        self.response_times = []
        self.lock = threading.Lock()
        self.last_update = time.time()

    def record_request(self, response_time, success=True):
        """记录请求数据"""
        with self.lock:
            self.request_count += 1
            if not success:
                self.failure_count += 1
            self.response_times.append(response_time)
            self.last_update = time.time()

    def get_stats(self):
        """获取当前统计数据"""
        with self.lock:
            if self.request_count == 0:
                return {
                    'request_count': 0,
                    'failure_count': 0,
                    'error_rate': 0,
                    'avg_response_time': 0,
                    'min_response_time': 0,
                    'max_response_time': 0,
                    'throughput': 0
                }

            avg_response_time = sum(self.response_times) / len(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
            error_rate = (self.failure_count / self.request_count) * 100

            # 计算吞吐量（请求/秒）
            elapsed = time.time() - self.last_update
            throughput = self.request_count / elapsed if elapsed > 0 else 0

            return {
                'request_count': self.request_count,
                'failure_count': self.failure_count,
                'error_rate': error_rate,
                'avg_response_time': avg_response_time,
                'min_response_time': min_response_time,
                'max_response_time': max_response_time,
                'throughput': throughput
            }


def _build_step_stages(user_count, step_users, step_duration, run_time):
    """Build staged load plan where step_users means incremental users per step."""
    if user_count <= 0 or step_users <= 0 or step_duration <= 0 or run_time <= 0:
        return []

    stages = []
    step_spawn_rate = max(1, (step_users + step_duration - 1) // step_duration)
    current_users = 0
    stage_start = 0

    while stage_start < run_time:
        if current_users < user_count:
            current_users = min(current_users + step_users, user_count)
        stage_end = min(stage_start + step_duration, run_time)
        stages.append({
            'start': int(stage_start),
            'end': int(stage_end),
            'users': int(current_users),
            'spawn_rate': int(step_spawn_rate),
        })
        stage_start += step_duration

    return stages


def _inject_step_load_shape(script_content, stages):
    if not stages:
        return script_content

    shape_script = f'''

from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    stages = {json.dumps(stages)}

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["end"]:
                return (stage["users"], stage["spawn_rate"])
        return None
'''
    return script_content.rstrip() + shape_script + '\n'


def _build_locust_command(locustfile, base_host, csv_prefix, run_time, user_count, spawn_rate, step_load_enabled):
    cmd = [
        sys.executable, '-m', 'locust',
        '-f', locustfile,
        '--host', base_host,
        '--run-time', f'{run_time}s',
        '--headless',
        '--csv', csv_prefix,
        '--loglevel', 'WARNING',
        '--only-summary',
        '--csv-full-history'
    ]

    if not step_load_enabled:
        cmd.extend([
            '--users', str(user_count),
            '--spawn-rate', str(spawn_rate),
        ])

    return cmd


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
        test_run.finished_at = datetime.utcnow()
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
            script.last_run_at = datetime.utcnow()

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
                    started_at=datetime.utcnow(),
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
                    'timestamp': datetime.utcnow().isoformat(),
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
                        'timestamp': datetime.utcnow().isoformat(),
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


@celery.task(
    bind=True,
    name='tasks.run_perf_test',
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    autoretry_for=(IOError, OSError, TimeoutError),
)
def run_perf_test_task(
    self,
    scenario_id,
    user_count,
    spawn_rate,
    run_time,
    step_load_enabled=False,
    step_users=None,
    step_duration=None
):
    """异步执行性能测试：改为子进程运行 Locust，避免 Celery/greenlet 冲突"""
    task_start_time = time.time()
    with _get_flask_app().app_context():
        from app.api.perf_test import _parse_target_url

        scenario = None
        temp_dir = None
        monitor_thread = None
        stop_monitor = threading.Event()
        perf_result_id = None

        def _safe_float(val, default=0.0):
            try:
                return float(val)
            except Exception:
                return default

        def _read_latest_stats(csv_prefix):
            """读取 stats_history 最新一行，提取实时指标（单位：ms/req/s/%）"""
            history_file = f"{csv_prefix}_stats_history.csv"
            if not os.path.exists(history_file):
                return None
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    lines = [ln.strip() for ln in f.readlines() if ln.strip()]
                if len(lines) < 2:
                    return None
                headers = lines[0].split(',')
                last = lines[-1].split(',')
                row = dict(zip(headers, last))

                total_req = _safe_float(row.get('Total Request Count') or row.get('Total Requests') or row.get('Requests') or 0)
                total_fail = _safe_float(row.get('Total Failure Count') or row.get('Total Failures') or row.get('Failures') or row.get('Fails') or 0)
                throughput = _safe_float(row.get('Requests/s') or row.get('RPS') or 0)
                avg_ms = _safe_float(row.get('Total Average Response Time') or row.get('Average Response Time') or row.get('Avg') or 0)
                p95_ms = _safe_float(row.get('95%') or row.get('95%ile') or 0)
                min_ms = _safe_float(row.get('Total Min Response Time') or row.get('Min Response Time') or row.get('Min') or 0)
                max_ms = _safe_float(row.get('Total Max Response Time') or row.get('Max Response Time') or row.get('Max') or 0)
                error_rate = (total_fail / total_req * 100) if total_req else 0

                return {
                    'request_count': int(total_req),
                    'failure_count': int(total_fail),
                    'avg_response_time_ms': avg_ms,
                    'p95_response_time_ms': p95_ms,
                    'min_response_time_ms': min_ms,
                    'max_response_time_ms': max_ms,
                    'throughput': throughput,
                    'error_rate': error_rate,
                }
            except Exception:
                return None

        try:
            scenario = PerfTestScenario.query.get(scenario_id)
            if not scenario:
                return {'success': False, 'error': '场景不存在'}

            if not scenario.target_url:
                return {'success': False, 'error': '目标地址未配置'}

            scenario.status = 'running'
            scenario.last_run_at = datetime.utcnow()
            db.session.commit()

            # 解析 URL 获取 base_host 和 endpoint_path
            base_host, endpoint_path = _parse_target_url(scenario.target_url)

            temp_dir = tempfile.mkdtemp()
            locustfile = os.path.join(temp_dir, 'locustfile.py')
            csv_prefix = os.path.join(temp_dir, 'rt')

            # AST 安全检查：在执行前验证脚本安全性
            safe, safety_reason = check_script_safety(scenario.script_content)
            if not safe:
                scenario.status = 'failed'
                scenario.last_result = {
                    'success': False,
                    'error': f'脚本安全检查未通过: {safety_reason}',
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                }
                db.session.commit()
                record_task_failure('run_perf_test', time.time() - task_start_time)
                return {'success': False, 'error': f'脚本安全检查未通过: {safety_reason}'}

            # 替换脚本中的占位符
            script_content = scenario.script_content.replace('{{endpoint_path}}', endpoint_path)
            if step_load_enabled:
                stages = _build_step_stages(
                    user_count=user_count,
                    step_users=step_users,
                    step_duration=step_duration,
                    run_time=run_time
                )
                if not stages:
                    return {'success': False, 'error': 'Invalid step load configuration'}
                script_content = _inject_step_load_shape(script_content, stages)

            with open(locustfile, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 创建性能测试结果记录
            from app.models.perf_test_result import PerformanceTestResult, PerformanceMetricSample
            perf_result = PerformanceTestResult(
                scenario_id=scenario_id,
                project_id=scenario.project_id,
                user_count=user_count,
                spawn_rate=spawn_rate,
                duration=run_time,
                target_url=scenario.target_url,
                status='running',
                started_at=datetime.utcnow(),
            )
            db.session.add(perf_result)
            db.session.commit()
            perf_result_id = perf_result.id
            logger.info("已创建性能测试结果记录", perf_result_id=perf_result_id, scenario_id=scenario_id)

            # 监控线程：每2秒读取 CSV 并写入时间序列数据
            def monitor_realtime():
                app = _get_flask_app()
                test_start = time.time()
                while not stop_monitor.is_set():
                    time.sleep(2)
                    stats = _read_latest_stats(csv_prefix)
                    if not stats:
                        continue
                    try:
                        with app.app_context():
                            # 写入时间序列采样数据
                            elapsed = int(time.time() - test_start)
                            sample = PerformanceMetricSample(
                                test_result_id=perf_result_id,
                                timestamp=datetime.utcnow(),
                                elapsed_seconds=elapsed,
                                rps=stats['throughput'],
                                active_users=user_count,
                                avg_response_time=stats['avg_response_time_ms'],
                                min_response_time=stats['min_response_time_ms'],
                                max_response_time=stats['max_response_time_ms'],
                                p95_response_time=stats['p95_response_time_ms'],
                                request_count=stats['request_count'],
                                failure_count=stats['failure_count'],
                                error_rate=stats['error_rate'],
                            )
                            db.session.add(sample)
                            db.session.commit()

                            # 同时更新场景实时状态
                            s = PerfTestScenario.query.get(scenario_id)
                            if s and s.status == 'running':
                                s.avg_response_time = stats['avg_response_time_ms']
                                s.min_response_time = stats['min_response_time_ms']
                                s.max_response_time = stats['max_response_time_ms']
                                s.throughput = stats['throughput']
                                s.error_rate = stats['error_rate']
                                if not s.last_result:
                                    s.last_result = {}
                                s.last_result['realtime'] = {
                                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                                    'stats': stats,
                                }
                                db.session.commit()
                    except Exception as e:
                        logger.error("更新实时数据失败", error=str(e), scenario_id=scenario_id)

            monitor_thread = threading.Thread(target=monitor_realtime, daemon=True)
            monitor_thread.start()

            # 启动 Locust 子进程（隔离 gevent）
            cmd = _build_locust_command(
                locustfile=locustfile,
                base_host=base_host,
                csv_prefix=csv_prefix,
                run_time=run_time,
                user_count=user_count,
                spawn_rate=spawn_rate,
                step_load_enabled=step_load_enabled,
            )

            proc = subprocess.Popen(
                cmd,
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.update_state(state='PROGRESS', meta={'status': '正在执行性能测试...'})

            try:
                proc.wait(timeout=run_time + 30)
            except subprocess.TimeoutExpired:
                proc.terminate()
            finally:
                stop_monitor.set()
                if monitor_thread:
                    monitor_thread.join(timeout=3)

            stdout, stderr = proc.communicate()

            # 解析最终结果
            results = _parse_locust_results(csv_prefix)
            agg = results.get('aggregated') or {}

            total_req = _safe_float(agg.get('Requests') or agg.get('Request Count') or 0)
            total_fail = _safe_float(agg.get('Fails') or agg.get('Failure Count') or 0)
            avg_ms = _safe_float(agg.get('Average Response Time') or agg.get('Average') or agg.get('Avg') or 0)
            min_ms = _safe_float(agg.get('Min Response Time') or agg.get('Min') or 0)
            max_ms = _safe_float(agg.get('Max Response Time') or agg.get('Max') or 0)
            p50_ms = _safe_float(agg.get('50%') or agg.get('50%ile') or 0)
            p75_ms = _safe_float(agg.get('75%') or agg.get('75%ile') or 0)
            p95_ms = _safe_float(agg.get('95%') or agg.get('95%ile') or 0)
            p99_ms = _safe_float(agg.get('99%') or agg.get('99%ile') or 0)
            throughput = _safe_float(agg.get('Requests/s') or agg.get('RPS') or 0)
            error_rate = (total_fail / total_req * 100) if total_req else 0

            scenario.status = 'completed' if proc.returncode == 0 else 'failed'
            scenario.avg_response_time = avg_ms
            scenario.min_response_time = min_ms
            scenario.max_response_time = max_ms
            scenario.throughput = throughput
            scenario.error_rate = error_rate

            scenario.last_result = {
                'success': proc.returncode == 0,
                'error': stderr if proc.returncode else None,
                'stdout': stdout,
                'error_rate': error_rate,
                'request_count': int(total_req),
                'failure_count': int(total_fail),
                'results': results,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            db.session.commit()

            # 更新性能测试结果记录
            try:
                from app.models.perf_test_result import PerformanceTestResult
                perf_result = PerformanceTestResult.query.get(perf_result_id)
                if perf_result:
                    perf_result.status = 'completed' if proc.returncode == 0 else 'failed'
                    perf_result.finished_at = datetime.utcnow()
                    perf_result.total_requests = int(total_req)
                    perf_result.total_failures = int(total_fail)
                    perf_result.error_rate = error_rate
                    perf_result.rps = throughput
                    perf_result.avg_response_time = avg_ms
                    perf_result.min_response_time = min_ms
                    perf_result.max_response_time = max_ms
                    perf_result.p50_response_time = p50_ms
                    perf_result.p75_response_time = p75_ms
                    perf_result.p95_response_time = p95_ms
                    perf_result.p99_response_time = p99_ms
                    perf_result.raw_result = results
                    db.session.commit()
                    logger.info("性能测试结果已更新", perf_result_id=perf_result_id)
            except Exception as e:
                logger.error("更新性能测试结果失败", error=str(e))

            if proc.returncode == 0:
                record_task_success('run_perf_test', time.time() - task_start_time)
            else:
                record_task_failure('run_perf_test', time.time() - task_start_time)

            return {
                'success': proc.returncode == 0,
                'scenario_id': scenario_id,
                'error_rate': error_rate,
                'results': results
            }

        except Exception as e:
            stop_monitor.set()
            if monitor_thread:
                monitor_thread.join(timeout=3)

            if scenario:
                scenario.status = 'failed'
                scenario.last_result = {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                }
                db.session.commit()

            # 标记性能测试结果为失败
            try:
                from app.models.perf_test_result import PerformanceTestResult
                if perf_result_id is not None:
                    perf_result = PerformanceTestResult.query.get(perf_result_id)
                    if perf_result:
                        perf_result.status = 'failed'
                        perf_result.finished_at = datetime.utcnow()
                        db.session.commit()
            except Exception:
                pass

            record_task_failure('run_perf_test', time.time() - task_start_time)
            return {'success': False, 'error': str(e)}

        finally:
            if temp_dir and os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass


def _parse_locust_results(csv_prefix):
    """解析 Locust CSV 结果"""
    results = {}
    
    try:
        # 读取统计数据
        stats_file = f'{csv_prefix}_stats.csv'
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    headers = lines[0].strip().split(',')
                    for line in lines[1:]:
                        values = line.strip().split(',')
                        if len(values) == len(headers):
                            row = dict(zip(headers, values))
                            if row.get('Name') == 'Aggregated':
                                results['aggregated'] = row
        
        # 读取历史数据
        history_file = f'{csv_prefix}_stats_history.csv'
        if os.path.exists(history_file):
            results['history'] = []
            with open(history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    headers = lines[0].strip().split(',')
                    for line in lines[1:]:
                        values = line.strip().split(',')
                        if len(values) == len(headers):
                            results['history'].append(dict(zip(headers, values)))
        
    except Exception as e:
        results['parse_error'] = str(e)
    
    return results


@celery.task(
    name='tasks.cleanup_old_results',
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    autoretry_for=(IOError, OSError),
)
def cleanup_old_results_task():
    """
    清理旧的测试结果（定时任务）

    清理超过 30 天的测试结果
    """
    task_start_time = time.time()
    # 使用 Flask 应用上下文
    with _get_flask_app().app_context():
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=30)

            # 清理 Web 测试结果
            old_scripts = WebTestScript.query.filter(
                WebTestScript.last_run_at < cutoff_date
            ).all()

            for script in old_scripts:
                script.last_result = None

            # 清理性能测试结果
            old_scenarios = PerfTestScenario.query.filter(
                PerfTestScenario.last_run_at < cutoff_date
            ).all()

            for scenario in old_scenarios:
                scenario.last_result = None

            db.session.commit()

            record_task_success('cleanup_old_results', time.time() - task_start_time)
            return {
                'success': True,
                'cleaned_scripts': len(old_scripts),
                'cleaned_scenarios': len(old_scenarios)
            }

        except Exception as e:
            record_task_failure('cleanup_old_results', time.time() - task_start_time)
            return {
                'success': False,
                'error': str(e)
            }


@celery.task(
    bind=True,
    name='tasks.run_app_test',
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    autoretry_for=(IOError, OSError, TimeoutError),
)
def run_app_test_task(self, script_id, user_id):
    """异步执行 APP 测试脚本（Appium）"""
    task_start_time = time.time()
    with _get_flask_app().app_context():
        from app.models.app_test_script import AppTestScript

        script = None
        try:
            script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()
            if not script:
                record_task_failure('run_app_test', time.time() - task_start_time)
                return {'success': False, 'error': 'Script not found'}

            script.status = 'running'
            script.last_run_at = datetime.utcnow()
            db.session.commit()

            self.update_state(state='PROGRESS', meta={'status': 'Running Appium test...'})

            # 准备工作目录
            work_dir = os.path.join(os.path.dirname(_get_flask_app().root_path), 'data', 'app_tests', str(script_id))
            os.makedirs(work_dir, exist_ok=True)

            # 通过沙箱执行脚本（AST 检查 + 子进程隔离 + 审计日志）
            sandbox_result = execute_script(
                script_content=script.script_content,
                user_id=user_id,
                timeout=300,  # 5 分钟超时
                work_dir=work_dir,
                script_id=script_id,
                script_type="app",
            )

            duration = sandbox_result['duration']
            success = sandbox_result['success']

            # 更新脚本状态
            script.status = 'passed' if success else 'failed'
            script.last_result = {
                'success': success,
                'duration': duration,
                'stdout': sandbox_result['stdout'],
                'stderr': sandbox_result['stderr'],
                'return_code': sandbox_result.get('return_code'),
                'error': sandbox_result.get('error'),
                'script_hash': sandbox_result.get('script_hash'),
                'timestamp': datetime.utcnow().isoformat(),
            }
            db.session.commit()

            if success:
                record_task_success('run_app_test', time.time() - task_start_time)
            else:
                record_task_failure('run_app_test', time.time() - task_start_time)

            return {
                'success': success,
                'script_id': script_id,
                'duration': duration,
                'stdout': sandbox_result['stdout'],
                'stderr': sandbox_result['stderr'],
                'return_code': sandbox_result.get('return_code'),
            }

        except subprocess.TimeoutExpired:
            # 安全网：sandbox 内部已处理超时，此处为防御性代码
            if script:
                script.status = 'failed'
                script.last_result = {
                    'success': False,
                    'error': 'Execution timeout (5 minutes)',
                    'timestamp': datetime.utcnow().isoformat(),
                }
                db.session.commit()
            record_task_failure('run_app_test', time.time() - task_start_time)
            return {'success': False, 'error': 'Execution timeout'}

        except Exception as e:
            if script:
                script.status = 'failed'
                script.last_result = {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat(),
                }
                db.session.commit()
            record_task_failure('run_app_test', time.time() - task_start_time)
            return {'success': False, 'error': str(e)}
