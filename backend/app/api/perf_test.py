"""
性能测试模块 - API
实现基于 Locust 的性能测试功能
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db, celery
from ..models.perf_test_scenario import PerfTestScenario
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
from ..tasks import run_perf_test_task
import subprocess
import tempfile
import os
import json
import time
import signal
from datetime import datetime


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
        return error_response(400, error)
    
    # 默认的 Locust 脚本模板
    default_script = '''"""
Locust 性能测试脚本

适用于 httpbin.org 等 HTTP 测试服务
"""
from locust import HttpUser, task, between

class TestUser(HttpUser):
    # 等待时间：每个任务之间等待 1-2 秒
    wait_time = between(1, 2)

    @task(3)
    def get_endpoint(self):
        """获取请求数据"""
        self.client.get("/get")

    @task(1)
    def delay_endpoint(self):
        """延迟测试（模拟慢请求）"""
        self.client.get("/delay/1")

    @task(1)
    def headers_endpoint(self):
        """获取请求头"""
        self.client.get("/headers")

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
        method=data.get('method', 'GET'),
        user_count=data.get('user_count', 10),
        spawn_rate=data.get('spawn_rate', 1),
        duration=data.get('duration', 60),
        project_id=data.get('project_id'),
        user_id=user_id,
        script_content=data.get('script_content', default_script)
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
        return error_response(404, '场景不存在')
    
    return success_response(data=scenario.to_dict())


@api_bp.route('/perf-test/scenarios/<int:scenario_id>', methods=['PUT'])
@jwt_required()
def update_scenario(scenario_id):
    """更新性能测试场景"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(404, '场景不存在')
    
    data = request.get_json()

    for field in ['name', 'description', 'target_url', 'method',
                  'user_count', 'spawn_rate', 'duration', 'script_content']:
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
        return error_response(404, '场景不存在')
    
    # 如果正在运行，先停止
    if scenario.status == 'running':
        try:
            task_id = f'perf_test_{scenario_id}_{user_id}'
            celery.control.revoke(task_id, terminate=True)
        except:
            pass
    
    db.session.delete(scenario)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 执行测试 ====================

@api_bp.route('/perf-test/scenarios/<int:scenario_id>/run', methods=['POST'])
@jwt_required()
def run_scenario(scenario_id):
    """运行性能测试场景（异步）"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(404, '场景不存在')

    # 检查是否已在运行
    if scenario.status == 'running':
        return error_response(400, '测试正在运行中')

    try:
        # 获取请求参数（前端可能不传 body）
        try:
            data = request.get_json(force=True, silent=True) or {}
        except Exception:
            data = {}
        user_count = data.get('user_count', scenario.user_count)
        spawn_rate = data.get('spawn_rate', scenario.spawn_rate)
        run_time = data.get('duration', scenario.duration)
        
        # 异步执行测试任务
        task = run_perf_test_task.apply_async(
            args=[scenario_id, user_count, spawn_rate, run_time],
            task_id=f'perf_test_{scenario_id}_{user_id}'
        )
        
        return success_response(data={
            'message': '测试已提交，正在后台执行',
            'task_id': task.id,
            'scenario_id': scenario_id,
            'config': {
                'users': user_count,
                'spawn_rate': spawn_rate,
                'run_time': run_time
            }
        })
        
    except Exception as e:
        return error_response(500, f'提交失败: {str(e)}')





@api_bp.route('/perf-test/scenarios/<int:scenario_id>/stop', methods=['POST'])
@jwt_required()
def stop_scenario(scenario_id):
    """停止运行中的性能测试"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    
    if not scenario:
        return error_response(404, '场景不存在')
    
    if scenario.status != 'running':
        return error_response(400, '测试未在运行')
    
    try:
        # 尝试撤销 Celery 任务
        task_id = f'perf_test_{scenario_id}_{user_id}'
        celery.control.revoke(task_id, terminate=True)
        
        # 更新状态
        scenario.status = 'stopped'
        db.session.commit()
        
        return success_response(message='已停止')
    except Exception as e:
        return error_response(500, f'停止失败: {str(e)}')



@api_bp.route('/perf-test/scenarios/<int:scenario_id>/status', methods=['GET'])
@jwt_required()
def get_scenario_status(scenario_id):
    """获取场景执行状态"""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()

    if not scenario:
        return error_response(404, '场景不存在')

    # 从 last_result 中获取实时数据，如果没有则使用数据库中的值
    result_data = scenario.last_result or {}
    return success_response(data={
        'status': scenario.status,
        'last_run_at': scenario.last_run_at.isoformat() + 'Z' if scenario.last_run_at else None,
        'last_result': scenario.last_result,
        'avg_response_time': scenario.avg_response_time,
        'max_response_time': scenario.max_response_time,
        'min_response_time': scenario.min_response_time,
        'throughput': scenario.throughput,
        'error_rate': scenario.error_rate,
    })


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
        return error_response(400, error)
    
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
        return error_response(500, f'测试失败: {str(e)}')


# ==================== 模板 ====================

@api_bp.route('/perf-test/templates', methods=['GET'])
def get_perf_templates():
    """获取性能测试脚本模板"""
    templates = [
        {
            'name': 'HTTPBin 测试',
            'description': '适用于 httpbin.org 的标准测试脚本',
            'code': '''"""
HTTPBin 测试脚本

适用于 https://httpbin.org
"""
from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def get_endpoint(self):
        """获取请求数据"""
        self.client.get("/get")

    @task(1)
    def delay_endpoint(self):
        """延迟测试"""
        self.client.get("/delay/1")

    @task(1)
    def headers_endpoint(self):
        """获取请求头"""
        self.client.get("/headers")
'''
        },
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

    # 查询数据库中状态为 running 的场景
    running_scenarios = PerfTestScenario.query.filter_by(
        user_id=user_id,
        status='running'
    ).all()

    user_tests = [{
        'id': s.id,  # 前端需要 id 字段
        'scenario_id': s.id,
        'name': s.name,
        'user_count': s.user_count,
        'duration': s.duration,
        'elapsed': 0,  # 计算已运行时间
        'status': s.status,
        'avg_response_time': s.avg_response_time or 0,
        'throughput': s.throughput or 0,
        'error_rate': s.error_rate or 0,
        'started_at': s.last_run_at.isoformat() + 'Z' if s.last_run_at else None
    } for s in running_scenarios]

    return success_response(data=user_tests)
