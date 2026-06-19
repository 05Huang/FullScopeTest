"""性能测试异步任务"""

from app.extensions import celery, db
from app.models.perf_test_scenario import PerfTestScenario
from app.core.logging import get_logger
from app.core.metrics import record_task_success, record_task_failure
import subprocess
import tempfile
import sys
import time
import os
import json
import threading
from datetime import datetime, timezone

from app.utils.sandbox import check_script_safety
from .common import _get_flask_app, _build_step_stages, _inject_step_load_shape, _build_locust_command

logger = get_logger(__name__)


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
            scenario.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
                    'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z',
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
                started_at=datetime.now(timezone.utc).replace(tzinfo=None),
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
                                timestamp=datetime.now(timezone.utc).replace(tzinfo=None),
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
                                    'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z',
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
                'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
            }
            db.session.commit()

            # 更新性能测试结果记录
            try:
                from app.models.perf_test_result import PerformanceTestResult
                perf_result = PerformanceTestResult.query.get(perf_result_id)
                if perf_result:
                    perf_result.status = 'completed' if proc.returncode == 0 else 'failed'
                    perf_result.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
                    'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
                }
                db.session.commit()

            # 标记性能测试结果为失败
            try:
                from app.models.perf_test_result import PerformanceTestResult
                if perf_result_id is not None:
                    perf_result = PerformanceTestResult.query.get(perf_result_id)
                    if perf_result:
                        perf_result.status = 'failed'
                        perf_result.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
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

