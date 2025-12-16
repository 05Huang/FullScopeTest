"""
性能测试模块 - API
实现基于 Locust 的性能测试功能
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.perf_test_scenario import PerfTestScenario
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
import subprocess
import tempfile
import os
import json
import threading
import time
import signal
from datetime import datetime


# 存储运行中的性能测试进程
running_tests = {}


@api_bp.route('/perf-test/health', methods=['GET'])
def perf_test_health():
    """性能测试模块健康检查"""
    return success_response(message='性能测试模块正常')


# ==================== 场景管理 ====================

@api_bp.route('/perf-test/scenarios', methods=['GET'])
@jwt_required()
def get_scenarios():
    """获取性能测试场景列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    
    query = PerfTestScenario.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    scenarios = query.order_by(PerfTestScenario.created_at.desc()).all()
    
    return success_response(data=[s.to_dict() for s in scenarios])


@api_bp.route('/perf-test/scenarios', methods=['POST'])
@jwt_required()
def create_scenario():
    """创建性能测试场景"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    error = validate_required(data, ['name'])
    if error:
        return error_response(message=error)
    
    # 默认的 Locust 脚本模板
    default_script = '''"""
Locust 性能测试脚本
"""
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # 等待时间：每个任务之间等待 1-3 秒
    wait_time = between(1, 3)
    
    @task(1)
    def index_page(self):
        """访问首页"""
        self.client.get("/")
    
    @task(2)
    def about_page(self):
        """访问关于页面"""
        self.client.get("/about")
    
    def on_start(self):
        """用户启动时执行"""
        pass
    
    def on_stop(self):
        """用户停止时执行"""
        pass
'''
    
    scenario = PerfTestScenario(
        name=data['name'],
        description=data.get('description', ''),
        target_url=data.get('target_url', 'http://localhost:8080'),
        user_count=data.get('user_count', 10),
        spawn_rate=data.get('spawn_rate', 1),
        duration=data.get('duration', 60),
        project_id=data.get('project_id'),
        user_id=user_id
    )
    
    db.session.add(scenario)
    db.session.commit()
    
    return success_response(data=scenario.to_dict(), message='创建成功')


@api_bp.route('/perf-test/scenarios/<int:scenario_id>', methods=['GET'])
@jwt_required()
def get_scenario(scenario_id):
    """获取场景详情"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(message='场景不存在', code=404)
    
    return success_response(data=scenario.to_dict())


@api_bp.route('/perf-test/scenarios/<int:scenario_id>', methods=['PUT'])
@jwt_required()
def update_scenario(scenario_id):
    """更新性能测试场景"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(message='场景不存在', code=404)
    
    data = request.get_json()
    
    for field in ['name', 'description', 'target_url', 
                  'user_count', 'spawn_rate', 'duration']:
        if field in data:
            setattr(scenario, field, data[field])
    
    db.session.commit()
    
    return success_response(data=scenario.to_dict(), message='更新成功')


@api_bp.route('/perf-test/scenarios/<int:scenario_id>', methods=['DELETE'])
@jwt_required()
def delete_scenario(scenario_id):
    """删除性能测试场景"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(message='场景不存在', code=404)
    
    # 如果正在运行，先停止
    run_key = f'{user_id}_{scenario_id}'
    if run_key in running_tests:
        try:
            running_tests[run_key]['process'].terminate()
            del running_tests[run_key]
        except:
            pass
    
    db.session.delete(scenario)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 执行测试 ====================

@api_bp.route('/perf-test/scenarios/<int:scenario_id>/run', methods=['POST'])
@jwt_required()
def run_scenario(scenario_id):
    """运行性能测试场景"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(message='场景不存在', code=404)
    
    run_key = f'{user_id}_{scenario_id}'
    
    # 检查是否已在运行
    if run_key in running_tests:
        return error_response(message='测试正在运行中')
    
    try:
        # 创建临时目录存放脚本和结果
        temp_dir = tempfile.mkdtemp()
        script_file = os.path.join(temp_dir, 'locustfile.py')
        csv_prefix = os.path.join(temp_dir, 'results')
        
        # 写入默认Locust脚本（因为模型中没有存储脚本代码）
        default_script = '''from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def load_test(self):
        self.client.get("/")
'''
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(default_script)
        
        # 覆盖请求参数
        data = request.get_json() or {}
        user_count = data.get('user_count', scenario.user_count)
        spawn_rate = data.get('spawn_rate', scenario.spawn_rate)
        run_time = data.get('duration', scenario.duration)
        
        # 构建 Locust 命令
        cmd = [
            'locust',
            '-f', script_file,
            '--host', scenario.target_url,
            '--users', str(user_count),
            '--spawn-rate', str(spawn_rate),
            '--run-time', f'{run_time}s',
            '--headless',
            '--csv', csv_prefix,
            '--only-summary'
        ]
        
        # 启动进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=temp_dir
        )
        
        # 记录运行状态
        running_tests[run_key] = {
            'process': process,
            'temp_dir': temp_dir,
            'csv_prefix': csv_prefix,
            'start_time': time.time(),
            'scenario_id': scenario_id
        }
        
        # 更新状态
        scenario.status = 'running'
        scenario.last_run_at = datetime.utcnow()
        db.session.commit()
        
        # 启动后台线程监控进程
        monitor_thread = threading.Thread(
            target=_monitor_test,
            args=(run_key, scenario_id, process, temp_dir, csv_prefix)
        )
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return success_response(data={
            'message': '测试已启动',
            'run_key': run_key,
            'config': {
                'users': user_count,
                'spawn_rate': spawn_rate,
                'run_time': run_time
            }
        })
        
    except Exception as e:
        scenario.status = 'failed'
        db.session.commit()
        return error_response(message=f'启动失败: {str(e)}')


def _monitor_test(run_key, scenario_id, process, temp_dir, csv_prefix):
    """后台监控测试进程"""
    try:
        # 等待进程完成
        stdout, stderr = process.communicate()
        
        # 读取结果
        results = _parse_locust_results(csv_prefix)
        
        # 更新数据库
        from flask import current_app
        with current_app.app_context():
            scenario = PerfTestScenario.query.get(scenario_id)
            if scenario:
                scenario.status = 'completed' if process.returncode == 0 else 'failed'
                scenario.last_result = {
                    'success': process.returncode == 0,
                    'stdout': stdout.decode('utf-8', errors='ignore'),
                    'stderr': stderr.decode('utf-8', errors='ignore'),
                    'results': results
                }
                db.session.commit()
        
    except Exception as e:
        print(f'Monitor error: {e}')
    
    finally:
        # 清理
        if run_key in running_tests:
            del running_tests[run_key]
        
        # 清理临时文件
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
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


@api_bp.route('/perf-test/scenarios/<int:scenario_id>/stop', methods=['POST'])
@jwt_required()
def stop_scenario(scenario_id):
    """停止运行中的性能测试"""
    user_id = get_current_user_id()
    run_key = f'{user_id}_{scenario_id}'
    
    if run_key not in running_tests:
        return error_response(message='测试未在运行')
    
    try:
        test_info = running_tests[run_key]
        process = test_info['process']
        
        # 停止进程
        process.terminate()
        process.wait(timeout=5)
        
        # 清理
        del running_tests[run_key]
        
        # 更新状态
        scenario = PerfTestScenario.query.get(scenario_id)
        if scenario:
            scenario.status = 'stopped'
            db.session.commit()
        
        return success_response(message='测试已停止')
        
    except Exception as e:
        return error_response(message=f'停止失败: {str(e)}')


@api_bp.route('/perf-test/scenarios/<int:scenario_id>/status', methods=['GET'])
@jwt_required()
def get_scenario_status(scenario_id):
    """获取性能测试状态"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(message='场景不存在', code=404)
    
    run_key = f'{user_id}_{scenario_id}'
    is_running = run_key in running_tests
    
    response_data = {
        'status': scenario.status,
        'is_running': is_running,
        'last_run_at': scenario.last_run_at.isoformat() if scenario.last_run_at else None,
        'last_result': scenario.last_result
    }
    
    # 如果正在运行，添加运行时间
    if is_running:
        test_info = running_tests[run_key]
        response_data['running_time'] = round(time.time() - test_info['start_time'], 2)
    
    return success_response(data=response_data)


# ==================== 快速测试 ====================

@api_bp.route('/perf-test/quick-test', methods=['POST'])
@jwt_required()
def quick_test():
    """
    快速性能测试（不保存场景）
    
    用于快速验证接口性能
    """
    data = request.get_json()
    
    error = validate_required(data, ['target_host'])
    if error:
        return error_response(message=error)
    
    target_host = data['target_host']
    endpoint = data.get('endpoint', '/')
    method = data.get('method', 'GET').upper()
    user_count = data.get('user_count', 5)
    spawn_rate = data.get('spawn_rate', 1)
    run_time = data.get('run_time', 10)
    
    # 生成临时脚本
    script = f'''
from locust import HttpUser, task, between

class QuickTestUser(HttpUser):
    wait_time = between(0.5, 1)
    
    @task
    def test_endpoint(self):
        self.client.{method.lower()}("{endpoint}")
'''
    
    try:
        # 创建临时文件
        temp_dir = tempfile.mkdtemp()
        script_file = os.path.join(temp_dir, 'locustfile.py')
        csv_prefix = os.path.join(temp_dir, 'results')
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        # 运行 Locust
        result = subprocess.run(
            [
                'locust',
                '-f', script_file,
                '--host', target_host,
                '--users', str(user_count),
                '--spawn-rate', str(spawn_rate),
                '--run-time', f'{run_time}s',
                '--headless',
                '--csv', csv_prefix,
                '--only-summary'
            ],
            capture_output=True,
            text=True,
            timeout=run_time + 30,
            cwd=temp_dir
        )
        
        # 解析结果
        results = _parse_locust_results(csv_prefix)
        
        # 清理
        import shutil
        shutil.rmtree(temp_dir)
        
        return success_response(data={
            'success': result.returncode == 0,
            'results': results,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
        
    except subprocess.TimeoutExpired:
        return success_response(data={
            'success': False,
            'error': '测试超时'
        })
        
    except Exception as e:
        return error_response(message=f'测试失败: {str(e)}')


# ==================== 模板 ====================

@api_bp.route('/perf-test/templates', methods=['GET'])
def get_perf_templates():
    """获取性能测试脚本模板"""
    templates = [
        {
            'name': '基础负载测试',
            'description': '简单的 GET 请求负载测试',
            'code': '''from locust import HttpUser, task, between

class BasicUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def index(self):
        self.client.get("/")
'''
        },
        {
            'name': 'API 测试',
            'description': '带认证的 API 接口测试',
            'code': '''from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 2)
    token = None
    
    def on_start(self):
        # 登录获取 token
        response = self.client.post("/api/login", json={
            "username": "test",
            "password": "test"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
    
    @task
    def get_data(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.client.get("/api/data", headers=headers)
'''
        },
        {
            'name': '混合场景测试',
            'description': '模拟真实用户行为的混合场景',
            'code': '''from locust import HttpUser, task, between, tag

class MixedUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    @tag('browse')
    def browse_products(self):
        self.client.get("/products")
    
    @task(2)
    @tag('search')
    def search(self):
        self.client.get("/search?q=test")
    
    @task(1)
    @tag('purchase')
    def add_to_cart(self):
        self.client.post("/cart", json={"product_id": 1})
'''
        }
    ]
    
    return success_response(data=templates)


@api_bp.route('/perf-test/running', methods=['GET'])
@jwt_required()
def get_running_tests():
    """获取当前用户运行中的测试列表"""
    user_id = get_current_user_id()
    
    user_tests = []
    for run_key, test_info in running_tests.items():
        if run_key.startswith(f'{user_id}_'):
            user_tests.append({
                'scenario_id': test_info['scenario_id'],
                'running_time': round(time.time() - test_info['start_time'], 2)
            })
    
    return success_response(data=user_tests)
