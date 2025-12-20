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
from datetime import datetime


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
    """
    异步执行性能测试
    
    Args:
        self: Celery 任务实例
        scenario_id: 场景 ID
        user_count: 并发用户数
        spawn_rate: 用户生成速率
        run_time: 运行时间（秒）
        
    Returns:
        dict: 执行结果
    """
    try:
        # 获取场景
        scenario = PerfTestScenario.query.get(scenario_id)
        if not scenario:
            return {
                'success': False,
                'error': '场景不存在'
            }
        
        # 更新状态
        scenario.status = 'running'
        scenario.last_run_at = datetime.utcnow()
        db.session.commit()
        
        # 更新任务进度
        self.update_state(state='PROGRESS', meta={'status': '正在执行性能测试...'})
        
        # 创建临时目录和文件
        temp_dir = tempfile.mkdtemp()
        locustfile = os.path.join(temp_dir, 'locustfile.py')
        
        with open(locustfile, 'w', encoding='utf-8') as f:
            f.write(scenario.script_content)
        
        # CSV 输出前缀
        csv_prefix = os.path.join(temp_dir, 'results')
        
        # 构建 Locust 命令
        cmd = [
            sys.executable, '-m', 'locust',
            '-f', locustfile,
            '--headless',
            '--users', str(user_count),
            '--spawn-rate', str(spawn_rate),
            '--run-time', f'{run_time}s',
            '--html', os.path.join(temp_dir, 'report.html'),
            '--csv', csv_prefix
        ]
        
        if scenario.target_url:
            cmd.extend(['--host', scenario.target_url])
        
        try:
            # 执行测试
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=run_time + 60  # 额外60秒容错时间
            )
            
            # 解析结果
            results = _parse_locust_results(csv_prefix)
            
            # 更新场景状态
            success = result.returncode == 0
            scenario.status = 'completed' if success else 'failed'
            scenario.last_result = {
                'success': success,
                'stdout': result.stdout.decode('utf-8', errors='ignore'),
                'stderr': result.stderr.decode('utf-8', errors='ignore'),
                'results': results,
                'timestamp': datetime.utcnow().isoformat()
            }
            db.session.commit()
            
            return {
                'success': success,
                'scenario_id': scenario_id,
                'results': results
            }
            
        finally:
            # 清理临时文件
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except subprocess.TimeoutExpired:
        scenario.status = 'timeout'
        scenario.last_result = {
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
        scenario.status = 'failed'
        scenario.last_result = {
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }
        db.session.commit()
        
        return {
            'success': False,
            'error': str(e)
        }


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
