"""
性能测试模块 - API
实现基于 Locust 的性能测试功能
"""

from flask import request, current_app
from flask_jwt_extended import jwt_required
from urllib.parse import urlparse
from . import api_bp
from ..extensions import db, celery
from ..models.perf_test_scenario import PerfTestScenario
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required, is_valid_url, is_valid_http_method
from ..utils import get_current_user_id
from ..tasks import run_perf_test_task
import subprocess
import tempfile
import os
import json
import time
import signal
from datetime import datetime


# ==================== URL 解析工具 ====================

def _parse_target_url(url: str) -> tuple:
    """
    解析目标 URL，提取 base_host 和 endpoint_path

    Args:
        url: 用户输入的完整 URL，如 https://api.example.com/v1/users?name=test

    Returns:
        (base_host, endpoint_path):
            - base_host: https://api.example.com（用于 Locust --host）
            - endpoint_path: /v1/users（用于脚本中的路径）
    """
    try:
        parsed = urlparse(url)
        # base_host = scheme://netloc（包含端口）
        base_host = f"{parsed.scheme}://{parsed.netloc}"
        # endpoint_path = path（去掉 query 和 fragment）
        endpoint_path = parsed.path or "/"
        return base_host, endpoint_path
    except Exception:
        # 解析失败时的兜底处理
        return url, "/"


def _get_perf_limits() -> dict:
    limits = current_app.config.get('PERF_TEST_LIMITS', {})
    return {
        'min_users': limits.get('min_users', 1),
        'max_users': limits.get('max_users', 200),
        'min_spawn_rate': limits.get('min_spawn_rate', 1),
        'max_spawn_rate': limits.get('max_spawn_rate', 50),
        'min_duration': limits.get('min_duration', 10),
        'max_duration': limits.get('max_duration', 3600),
    }


def _parse_int(value, field_name: str):
    try:
        return int(value), None
    except (TypeError, ValueError):
        return None, f'{field_name} must be an integer'


def _validate_perf_numbers(user_count, spawn_rate, duration):
    limits = _get_perf_limits()

    user_count, error = _parse_int(user_count, 'user_count')
    if error:
        return None, error
    spawn_rate, error = _parse_int(spawn_rate, 'spawn_rate')
    if error:
        return None, error
    duration, error = _parse_int(duration, 'duration')
    if error:
        return None, error

    if not limits['min_users'] <= user_count <= limits['max_users']:
        return None, f'user_count must be between {limits["min_users"]} and {limits["max_users"]}'
    if not limits['min_spawn_rate'] <= spawn_rate <= limits['max_spawn_rate']:
        return None, f'spawn_rate must be between {limits["min_spawn_rate"]} and {limits["max_spawn_rate"]}'
    if not limits['min_duration'] <= duration <= limits['max_duration']:
        return None, f'duration must be between {limits["min_duration"]} and {limits["max_duration"]} seconds'

    return (user_count, spawn_rate, duration), None


def _normalize_endpoint_path(endpoint: str):
    endpoint = (endpoint or '/').strip()
    parsed = urlparse(endpoint)
    if parsed.scheme or parsed.netloc:
        return None, 'endpoint must be a relative path'
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    return endpoint, None


def _generate_locust_script(method: str, endpoint_path: str,
                            headers: dict = None, body: dict = None) -> str:
    """
    根据请求方法生成 Locust 脚本

    Args:
        method: HTTP 方法（GET/POST/PUT/DELETE）
        endpoint_path: 接口路径
        headers: 请求头
        body: 请求体

    Returns:
        str: 生成的 Locust 脚本内容
    """
    method = method.upper()
    endpoint_path = endpoint_path or "/"

    # 生成 headers 代码
    headers_code = ""
    if headers:
        headers_items = [f'            "{k}": "{v}"' for k, v in headers.items()]
        headers_code = f"""

        # 请求头
        headers = {{
{",\n".join(headers_items)}
        }}
"""

    # 生成请求代码
    if method == "GET":
        request_code = f'self.client.get("{endpoint_path}"'
        if headers:
            request_code += ', headers=headers'
        request_code += ")"
    elif method == "POST":
        body_str = json.dumps(body, ensure_ascii=False) if body else "{}"
        request_code = f'self.client.post("{endpoint_path}", json={body_str}'
        if headers:
            request_code += ', headers=headers'
        request_code += ")"
    elif method == "PUT":
        body_str = json.dumps(body, ensure_ascii=False) if body else "{}"
        request_code = f'self.client.put("{endpoint_path}", json={body_str}'
        if headers:
            request_code += ', headers=headers'
        request_code += ")"
    elif method == "DELETE":
        request_code = f'self.client.delete("{endpoint_path}"'
        if headers:
            request_code += ', headers=headers'
        request_code += ")"
    else:
        request_code = f'self.client.get("{endpoint_path}")'

    # 组装完整脚本
    script = f'''"""
Locust 性能测试脚本（自动生成）
"""
from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 2)
{headers_code}
    @task
    def test_endpoint(self):
        """测试接口"""
        {request_code}
'''
    return script


# ==================== Locust 脚本模板 ====================

DEFAULT_LOCUST_SCRIPT = '''"""
Locust 性能测试脚本（自动生成）
"""
from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_endpoint(self):
        """测试接口"""
        self.client.get("{{endpoint_path}}")
'''

LOCUST_TEMPLATES = [
    {
        'name': '基础 GET 请求',
        'description': '最简单的 GET 请求测试',
        'code': '''"""
基础 GET 请求测试
"""
from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_request(self):
        """GET 请求"""
        self.client.get("{{endpoint_path}}")
'''
    },
    {
        'name': 'POST 请求测试',
        'description': '带 JSON 请求体的 POST 测试',
        'code': '''"""
POST 请求测试
"""
from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def post_request(self):
        """POST 请求"""
        self.client.post("{{endpoint_path}}", json={
            "username": "test_user",
            "email": "test@example.com"
        })
'''
    },
    {
        'name': '带认证的 API 测试',
        'description': '模拟登录后进行 API 调用',
        'code': '''"""
带认证的 API 测试
"""
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 2)
    token = None

    def on_start(self):
        """用户启动时登录获取 token"""
        response = self.client.post("/api/login", json={
            "username": "test",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")

    @task(3)
    def get_data(self):
        """获取数据"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.client.get("{{endpoint_path}}", headers=headers)

    @task(1)
    def create_data(self):
        """创建数据"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.client.post("{{endpoint_path}}", json={"name": "test"}, headers=headers)
'''
    },
    {
        'name': '混合场景测试',
        'description': '模拟真实用户行为的混合场景',
        'code': '''"""
混合场景测试
"""
from locust import HttpUser, task, between, tag

class MixedUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    @tag('browse')
    def browse(self):
        """浏览"""
        self.client.get("{{endpoint_path}}")

    @task(2)
    @tag('search')
    def search(self):
        """搜索"""
        self.client.get("{{endpoint_path}}/search?q=test")

    @task(1)
    @tag('action')
    def action(self):
        """操作"""
        self.client.post("{{endpoint_path}}/action", json={"action": "test"})
'''
    },
    {
        'name': 'HTTPBin 示例',
        'description': '适用于 httpbin.org 的测试（仅用于学习和测试）',
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
    }
]


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
    """Create a performance test scenario."""
    user_id = get_current_user_id()
    data = request.get_json()

    error = validate_required(data, ['name'])
    if error:
        return error_response(400, error)

    target_url = data.get('target_url', 'http://localhost:8080')
    if not is_valid_url(target_url):
        return error_response(400, 'target_url must be a valid http/https URL')

    method = data.get('method', 'GET').upper()
    if not is_valid_http_method(method):
        return error_response(400, 'method must be a valid HTTP method')

    headers = data.get('headers')
    if headers is not None and not isinstance(headers, dict):
        return error_response(400, 'headers must be an object')

    body = data.get('body')
    user_count = data.get('user_count', 10)
    spawn_rate = data.get('spawn_rate', 1)
    duration = data.get('duration', 60)

    numbers, error = _validate_perf_numbers(user_count, spawn_rate, duration)
    if error:
        return error_response(400, error)
    user_count, spawn_rate, duration = numbers

    # Generate script when no custom script is provided.
    script_content = data.get('script_content')
    if not script_content:
        _, endpoint_path = _parse_target_url(target_url)
        script_content = _generate_locust_script(method, endpoint_path, headers, body)

    scenario = PerfTestScenario(
        name=data['name'],
        description=data.get('description', ''),
        target_url=target_url,
        method=method,
        headers=headers,
        body=body,
        user_count=user_count,
        spawn_rate=spawn_rate,
        duration=duration,
        project_id=data.get('project_id'),
        user_id=user_id,
        script_content=script_content
    )

    db.session.add(scenario)
    db.session.commit()

    return success_response(data=scenario.to_dict(), message='Created')


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
    """Update a performance test scenario."""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()

    if not scenario:
        return error_response(404, 'Scenario not found')

    data = request.get_json()

    if 'target_url' in data:
        if not is_valid_url(data['target_url']):
            return error_response(400, 'target_url must be a valid http/https URL')
        scenario.target_url = data['target_url']

    if 'method' in data:
        method = str(data['method']).upper()
        if not is_valid_http_method(method):
            return error_response(400, 'method must be a valid HTTP method')
        scenario.method = method

    if 'headers' in data:
        headers = data['headers']
        if headers is not None and not isinstance(headers, dict):
            return error_response(400, 'headers must be an object')
        scenario.headers = headers

    if 'body' in data:
        scenario.body = data['body']

    if 'name' in data:
        scenario.name = data['name']
    if 'description' in data:
        scenario.description = data['description']
    if 'script_content' in data:
        scenario.script_content = data['script_content']

    limits = _get_perf_limits()
    if 'user_count' in data:
        user_count, error = _parse_int(data['user_count'], 'user_count')
        if error:
            return error_response(400, error)
        if not limits['min_users'] <= user_count <= limits['max_users']:
            return error_response(400, f'user_count must be between {limits["min_users"]} and {limits["max_users"]}')
        scenario.user_count = user_count

    if 'spawn_rate' in data:
        spawn_rate, error = _parse_int(data['spawn_rate'], 'spawn_rate')
        if error:
            return error_response(400, error)
        if not limits['min_spawn_rate'] <= spawn_rate <= limits['max_spawn_rate']:
            return error_response(400, f'spawn_rate must be between {limits["min_spawn_rate"]} and {limits["max_spawn_rate"]}')
        scenario.spawn_rate = spawn_rate

    if 'duration' in data:
        duration, error = _parse_int(data['duration'], 'duration')
        if error:
            return error_response(400, error)
        if not limits['min_duration'] <= duration <= limits['max_duration']:
            return error_response(400, f'duration must be between {limits["min_duration"]} and {limits["max_duration"]} seconds')
        scenario.duration = duration

    db.session.commit()

    return success_response(data=scenario.to_dict(), message='Updated')


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
    """Run a performance test scenario (async)."""
    user_id = get_current_user_id()
    scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()

    if not scenario:
        return error_response(404, 'Scenario not found')

    if scenario.status == 'running':
        return error_response(400, 'Scenario is already running')

    try:
        try:
            data = request.get_json(force=True, silent=True) or {}
        except Exception:
            data = {}

        user_count = data.get('user_count', scenario.user_count)
        spawn_rate = data.get('spawn_rate', scenario.spawn_rate)
        run_time = data.get('duration', scenario.duration)

        numbers, error = _validate_perf_numbers(user_count, spawn_rate, run_time)
        if error:
            return error_response(400, error)
        user_count, spawn_rate, run_time = numbers

        task = run_perf_test_task.apply_async(
            args=[scenario_id, user_count, spawn_rate, run_time],
            task_id=f'perf_test_{scenario_id}_{user_id}'
        )

        return success_response(data={
            'message': 'Scenario submitted',
            'task_id': task.id,
            'scenario_id': scenario_id,
            'config': {
                'users': user_count,
                'spawn_rate': spawn_rate,
                'run_time': run_time
            }
        })

    except Exception as e:
        return error_response(500, f'Failed to submit: {str(e)}')


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
    """Quick performance test (no scenario saved)."""
    data = request.get_json()

    error = validate_required(data, ['target_host'])
    if error:
        return error_response(400, error)

    target_host = data['target_host']
    if not is_valid_url(target_host):
        return error_response(400, 'target_host must be a valid http/https URL')

    endpoint, error = _normalize_endpoint_path(data.get('endpoint', '/'))
    if error:
        return error_response(400, error)

    method = data.get('method', 'GET').upper()
    if not is_valid_http_method(method):
        return error_response(400, 'method must be a valid HTTP method')

    user_count = data.get('user_count', 5)
    spawn_rate = data.get('spawn_rate', 1)
    run_time = data.get('run_time', 10)

    numbers, error = _validate_perf_numbers(user_count, spawn_rate, run_time)
    if error:
        return error_response(400, error)
    user_count, spawn_rate, run_time = numbers

    script = f"""
from locust import HttpUser, task, between

class QuickTestUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def test_endpoint(self):
        self.client.{method.lower()}("{endpoint}")
"""

    try:
        temp_dir = tempfile.mkdtemp()
        script_file = os.path.join(temp_dir, 'locustfile.py')
        csv_prefix = os.path.join(temp_dir, 'results')

        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)

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

        results = _parse_locust_results(csv_prefix)

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
            'error': 'Test timed out'
        })

    except Exception as e:
        return error_response(500, f'Test failed: {str(e)}')


@api_bp.route('/perf-test/templates', methods=['GET'])
def get_perf_templates():
    """获取性能测试脚本模板"""
    return success_response(data=LOCUST_TEMPLATES)



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
