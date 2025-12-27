"""
Celery 异步任务模块

包含 Web 测试、性能测试等异步任务
"""

from app.extensions import celery, db
from app.models.web_test_script import WebTestScript
from app.models.perf_test_scenario import PerfTestScenario
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


@celery.task(bind=True, name='tasks.run_web_test')
def run_web_test_task(self, script_id, user_id):
    """
    异步执行 Web 测试脚本

    Args:
        self: Celery 任务实例
        script_id: 脚本 ID
        user_id: 用户 ID

    Returns:
        dict: 执行结果
    """
    # 使用 Flask 应用上下文
    with _get_flask_app().app_context():
        try:
            # 获取脚本
            script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
            if not script:
                return {
                    'success': False,
                    'error': '脚本不存在'
                }

            # 更新状态为运行中
            script.status = 'running'
            script.last_run_at = datetime.utcnow()
            db.session.commit()

            # 更新任务进度
            self.update_state(state='PROGRESS', meta={'status': '正在执行脚本...'})

            # 创建临时文件运行脚本
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script.script_content)
                temp_file = f.name

            try:
                # 运行脚本
                start_time = time.time()

                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=script.timeout / 1000,  # 转换为秒
                    cwd=tempfile.gettempdir()
                )

                end_time = time.time()
                duration = end_time - start_time

                # 判断执行结果
                success = result.returncode == 0

                # 更新脚本状态
                script.status = 'success' if success else 'failed'
                script.last_result = {
                    'success': success,
                    'duration': duration,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode,
                    'timestamp': datetime.utcnow().isoformat()
                }
                db.session.commit()

                return {
                    'success': success,
                    'script_id': script_id,
                    'duration': duration,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode
                }

            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except subprocess.TimeoutExpired:
            script.status = 'timeout'
            script.last_result = {
                'success': False,
                'error': '执行超时',
                'timestamp': datetime.utcnow().isoformat()
            }
            db.session.commit()

            return {
                'success': False,
                'error': '执行超时'
            }

        except Exception as e:
            script.status = 'failed'
            script.last_result = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
            db.session.commit()

            return {
                'success': False,
                'error': str(e)
            }


@celery.task(bind=True, name='tasks.run_perf_test')
def run_perf_test_task(self, scenario_id, user_count, spawn_rate, run_time):
    """异步执行性能测试：改为子进程运行 Locust，避免 Celery/greenlet 冲突"""
    with _get_flask_app().app_context():
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

                total_req = _safe_float(row.get('Total Requests') or row.get('Requests') or 0)
                total_fail = _safe_float(row.get('Total Failures') or row.get('Failures') or row.get('Fails') or 0)
                throughput = _safe_float(row.get('Requests/s') or row.get('RPS') or 0)
                avg_ms = _safe_float(row.get('Avg') or row.get('Average Response Time') or 0)
                p95_ms = _safe_float(row.get('95%') or row.get('95%ile') or row.get('95') or 0)
                min_ms = _safe_float(row.get('Min') or 0)
                max_ms = _safe_float(row.get('Max') or 0)
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

            temp_dir = tempfile.mkdtemp()
            locustfile = os.path.join(temp_dir, 'locustfile.py')
            csv_prefix = os.path.join(temp_dir, 'rt')

            with open(locustfile, 'w', encoding='utf-8') as f:
                f.write(scenario.script_content)

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
            cmd = [
                sys.executable, '-m', 'locust',
                '-f', locustfile,
                '--host', scenario.target_url,
                '--users', str(user_count),
                '--spawn-rate', str(spawn_rate),
                '--run-time', f'{run_time}s',
                '--headless',
                '--csv', csv_prefix,
                '--loglevel', 'WARNING',
                '--only-summary',
                '--csv-full-history'
            ]

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
