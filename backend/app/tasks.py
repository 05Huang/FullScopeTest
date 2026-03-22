"""
Celery 异步任务模块

包含 Web 测试、性能测试等异步任务
"""

from app.extensions import celery, db
from app.models.web_test_script import WebTestScript
from app.models.perf_test_scenario import PerfTestScenario
from app.models.test_run import TestRun
from app.models.test_report import TestReport
import subprocess
import tempfile
import sys
import time
import os
import json
import threading
import queue
from datetime import datetime


def _get_flask_app():
    """延迟获取 Flask 应用实例，避免循环导入"""
    from app import create_app
    return create_app()


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


@celery.task(bind=True, name='tasks.run_web_test')
def run_web_test_task(self, script_id, user_id):
    """Run a web script asynchronously and persist unified reporting records."""
    with _get_flask_app().app_context():
        script = None
        test_run = None
        work_dir = None

        try:
            script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
            if not script:
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
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8', dir=work_dir) as f:
                f.write(script.script_content)
                temp_file = f.name

            try:
                start_time = time.time()
                env = os.environ.copy()
                env['PYTHONPATH'] = os.path.dirname(_get_flask_app().root_path) + os.pathsep + env.get('PYTHONPATH', '')
                
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=script.timeout / 1000,
                    cwd=work_dir,
                    env=env
                )
                duration = time.time() - start_time
                success = result.returncode == 0

                vision_results_path = os.path.join(work_dir, 'vision_results.json')
                vision_data = None
                if os.path.exists(vision_results_path):
                    try:
                        with open(vision_results_path, 'r', encoding='utf-8') as f:
                            vision_data = json.load(f)
                    except Exception:
                        pass

                run_payload = {
                    'success': success,
                    'duration': duration,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode,
                    'vision_results': vision_data,
                    'timestamp': datetime.utcnow().isoformat(),
                }
                test_run_id, report_id = _finalize_web_test_run(
                    script=script,
                    test_run=test_run,
                    success=success,
                    duration=duration,
                    result_payload=run_payload,
                )

                return {
                    'success': success,
                    'script_id': script_id,
                    'test_run_id': test_run_id,
                    'report_id': report_id,
                    'duration': duration,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode,
                }
            finally:
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass

        except subprocess.TimeoutExpired:
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

                timeout_seconds = script.timeout / 1000 if script.timeout else 0
                run_payload = {
                    'success': False,
                    'error': 'Execution timeout',
                    'vision_results': vision_data,
                    'timestamp': datetime.utcnow().isoformat(),
                }
                test_run_id, report_id = _finalize_web_test_run(
                    script=script,
                    test_run=test_run,
                    success=False,
                    duration=timeout_seconds,
                    result_payload=run_payload,
                )
            else:
                test_run_id, report_id = None, None

            return {
                'success': False,
                'error': 'Execution timeout',
                'test_run_id': test_run_id,
                'report_id': report_id,
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

                run_payload = {
                    'success': False,
                    'error': str(e),
                    'vision_results': vision_data,
                    'timestamp': datetime.utcnow().isoformat(),
                }
                test_run_id, report_id = _finalize_web_test_run(
                    script=script,
                    test_run=test_run,
                    success=False,
                    duration=0,
                    result_payload=run_payload,
                )
            else:
                test_run_id, report_id = None, None

            return {
                'success': False,
                'error': str(e),
                'test_run_id': test_run_id,
                'report_id': report_id,
            }


@celery.task(bind=True, name='tasks.run_perf_test')
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
    with _get_flask_app().app_context():
        from app.api.perf_test import _parse_target_url

        scenario = None
        temp_dir = None
        monitor_thread = None
        stop_monitor = threading.Event()

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

            # 监控线程：每2秒读取 CSV 并写库
            def monitor_realtime():
                app = _get_flask_app()
                while not stop_monitor.is_set():
                    time.sleep(2)
                    stats = _read_latest_stats(csv_prefix)
                    if not stats:
                        continue
                    try:
                        with app.app_context():
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
                        print(f"更新实时数据失败: {e}")

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


@celery.task(name='tasks.cleanup_old_results')
def cleanup_old_results_task():
    """
    清理旧的测试结果（定时任务）

    清理超过 30 天的测试结果
    """
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

            return {
                'success': True,
                'cleaned_scripts': len(old_scripts),
                'cleaned_scenarios': len(old_scenarios)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
