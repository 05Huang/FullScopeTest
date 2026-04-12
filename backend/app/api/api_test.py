"""
接口测试模块 - API
实现接口测试相关功能：用例管理、执行测试、结果存储
"""

from flask import request, current_app, Response, make_response
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.api_test_case import ApiTestCollection, ApiTestCase
from ..models.environment import Environment
from ..models.project import Project
from ..models.test_run import TestRun
from ..models.test_report import TestReport
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
from ..utils.ai_planner import generate_api_test_plan
from ..utils.ai_data_synthesizer import synthesize_test_cases
from ..utils.ai_reviewer import review_api_collection
from ..utils.env_variables import replace_variables, replace_variables_in_dict, get_environment_variables, merge_headers_with_env
from ..utils.js_executor import get_executor
from ..utils.script_context import (
    build_pre_script_context,
    build_post_script_context,
    apply_pre_script_changes,
    apply_env_changes,
    calculate_case_passed
)
import requests
import json
import logging
import os
import re
import time
from datetime import datetime

# 配置日志
logger = logging.getLogger(__name__)


AI_CONFIG_ENV_MAP = {
    'base_url': 'AI_ASSISTANT_BASE_URL',
    'model': 'AI_ASSISTANT_MODEL',
    'api_key': 'AI_ASSISTANT_API_KEY',
    'vision_base_url': 'AI_VISION_BASE_URL',
    'vision_model': 'AI_VISION_MODEL',
    'vision_api_key': 'AI_VISION_API_KEY',
}


def _mask_secret(value: str) -> str:
    if not value:
        return value
    if len(value) > 8:
        return f"{value[:4]}...{value[-4:]}"
    return "***"


def _sanitize_env_value(value: str) -> str:
    return str(value or '').replace('\n', '').replace('\r', '').strip()


def _get_backend_env_path() -> str:
    return os.path.join(os.path.dirname(current_app.root_path), '.env')


def _upsert_env_file(file_path: str, mapping: dict) -> None:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    else:
        lines = []

    for env_key, env_value in mapping.items():
        pattern = re.compile(rf'^\s*{re.escape(env_key)}\s*=')
        replaced = False
        for idx, line in enumerate(lines):
            if pattern.match(line):
                lines[idx] = f"{env_key}={env_value}"
                replaced = True
                break
        if not replaced:
            lines.append(f"{env_key}={env_value}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


@api_bp.route('/api-test/health', methods=['GET'])
def api_test_health():
    """接口测试模块健康检查"""
    return success_response(message='接口测试模块正常')


@api_bp.route('/api-test/ai/config', methods=['GET'])
@jwt_required()
def get_ai_config():
    """Get the current global AI assistant configuration"""
    runtime_config = {
        'base_url': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
        'model': current_app.config.get('AI_ASSISTANT_MODEL', ''),
        'api_key': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
        'vision_base_url': current_app.config.get('AI_VISION_BASE_URL', ''),
        'vision_model': current_app.config.get('AI_VISION_MODEL', ''),
        'vision_api_key': current_app.config.get('AI_VISION_API_KEY', '')
    }
    
    runtime_config['api_key'] = _mask_secret(runtime_config['api_key'])
    runtime_config['vision_api_key'] = _mask_secret(runtime_config['vision_api_key'])

    return success_response(data=runtime_config, message='AI configuration fetched')


@api_bp.route('/api-test/ai/config', methods=['POST'])
@jwt_required()
def save_ai_config():
    data = request.get_json() or {}
    payload = {}
    for field_name, env_key in AI_CONFIG_ENV_MAP.items():
        if field_name in data:
            payload[env_key] = _sanitize_env_value(data.get(field_name))

    required_fields = ['AI_ASSISTANT_BASE_URL', 'AI_ASSISTANT_MODEL', 'AI_ASSISTANT_API_KEY']
    for required_field in required_fields:
        value = payload.get(required_field) or current_app.config.get(required_field, '')
        if not str(value).strip():
            return error_response(400, f'{required_field} is required')

    vision_defaults = {
        'AI_VISION_BASE_URL': payload.get('AI_ASSISTANT_BASE_URL') or current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
        'AI_VISION_MODEL': payload.get('AI_ASSISTANT_MODEL') or current_app.config.get('AI_ASSISTANT_MODEL', ''),
        'AI_VISION_API_KEY': payload.get('AI_ASSISTANT_API_KEY') or current_app.config.get('AI_ASSISTANT_API_KEY', ''),
    }
    for key, default_value in vision_defaults.items():
        if key not in payload:
            payload[key] = _sanitize_env_value(default_value)

    env_path = _get_backend_env_path()
    try:
        _upsert_env_file(env_path, payload)
        for key, value in payload.items():
            os.environ[key] = value
            current_app.config[key] = value
    except Exception as exc:
        logger.error('save ai config failed: %s', str(exc), exc_info=True)
        return error_response(500, f'保存 AI 配置失败: {str(exc)}')

    response_data = {
        'base_url': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
        'model': current_app.config.get('AI_ASSISTANT_MODEL', ''),
        'api_key': _mask_secret(current_app.config.get('AI_ASSISTANT_API_KEY', '')),
        'vision_base_url': current_app.config.get('AI_VISION_BASE_URL', ''),
        'vision_model': current_app.config.get('AI_VISION_MODEL', ''),
        'vision_api_key': _mask_secret(current_app.config.get('AI_VISION_API_KEY', '')),
    }
    return success_response(data=response_data, message='AI 配置已保存到 .env')


@api_bp.route('/api-test/ai/plan', methods=['POST'])
@jwt_required()
def generate_ai_plan():
    """Generate AI operations plan for API workspace."""
    user_id = get_current_user_id()
    data = request.get_json() or {}
    prompt = (data.get('prompt') or '').strip()

    if not prompt:
        return error_response(400, 'prompt is required')

    collections = ApiTestCollection.query.filter_by(user_id=user_id).all()
    cases = (
        ApiTestCase.query
        .filter_by(user_id=user_id)
        .order_by(ApiTestCase.updated_at.desc())
        .limit(200)
        .all()
    )
    projects = Project.query.filter_by(owner_id=user_id).all()
    project_ids = [p.id for p in projects]
    envs = []
    if project_ids:
        envs = Environment.query.filter(Environment.project_id.in_(project_ids)).all()

    context = {
        'selected_collection_id': data.get('collection_id'),
        'selected_case_id': data.get('case_id'),
        'selected_env_id': data.get('environment_id'),
        'project_id': data.get('project_id'),
        'collections': [
            {'id': c.id, 'name': c.name, 'project_id': c.project_id}
            for c in collections
        ],
        'cases': [
            {
                'id': c.id,
                'name': c.name,
                'method': c.method,
                'url': c.url,
                'collection_id': c.collection_id,
                'environment_id': c.environment_id,
            }
            for c in cases
        ],
        'environments': [
            {
                'id': e.id,
                'name': e.name,
                'project_id': e.project_id,
                'base_url': e.base_url,
            }
            for e in envs
        ],
    }

    try:
        runtime_config = {
            'AI_ASSISTANT_ENABLED': current_app.config.get('AI_ASSISTANT_ENABLED', True),
            'AI_ASSISTANT_BASE_URL': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
            'AI_ASSISTANT_API_KEY': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
            'AI_ASSISTANT_MODEL': current_app.config.get('AI_ASSISTANT_MODEL', ''),
            'AI_VISION_BASE_URL': current_app.config.get('AI_VISION_BASE_URL', ''),
            'AI_VISION_API_KEY': current_app.config.get('AI_VISION_API_KEY', ''),
            'AI_VISION_MODEL': current_app.config.get('AI_VISION_MODEL', ''),
            'AI_ASSISTANT_TIMEOUT': current_app.config.get('AI_ASSISTANT_TIMEOUT', 30),
        }

        # Frontend runtime override: allow per-request model provider settings.
        if data.get('base_url'):
            runtime_config['AI_ASSISTANT_BASE_URL'] = str(data.get('base_url')).strip()
        if data.get('model'):
            runtime_config['AI_ASSISTANT_MODEL'] = str(data.get('model')).strip()
        if data.get('api_key'):
            runtime_config['AI_ASSISTANT_API_KEY'] = str(data.get('api_key')).strip()
        if data.get('vision_base_url'):
            runtime_config['AI_VISION_BASE_URL'] = str(data.get('vision_base_url')).strip()
        if data.get('vision_model'):
            runtime_config['AI_VISION_MODEL'] = str(data.get('vision_model')).strip()
        if data.get('vision_api_key'):
            runtime_config['AI_VISION_API_KEY'] = str(data.get('vision_api_key')).strip()

        plan = generate_api_test_plan(
            prompt=prompt,
            context=context,
            config=runtime_config,
        )
        return success_response(data=plan, message='AI plan generated')
    except ValueError as exc:
        return error_response(400, str(exc))
    except Exception as exc:
        logger.error('AI plan generation failed: %s', str(exc), exc_info=True)
        return error_response(500, f'AI plan generation failed: {str(exc)}')


@api_bp.route('/api-test/ai/synthesize-cases', methods=['POST'])
@jwt_required()
def synthesize_api_cases():
    """AI 智能扩充接口测试用例"""
    data = request.get_json() or {}
    base_request = data.get('base_request')
    count = data.get('count', 5)  # 默认生成 5 个
    
    if not base_request:
        return error_response(400, 'base_request is required')
        
    try:
        runtime_config = {
            'AI_ASSISTANT_ENABLED': current_app.config.get('AI_ASSISTANT_ENABLED', True),
            'AI_ASSISTANT_BASE_URL': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
            'AI_ASSISTANT_API_KEY': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
            'AI_ASSISTANT_MODEL': current_app.config.get('AI_ASSISTANT_MODEL', ''),
            'AI_VISION_BASE_URL': current_app.config.get('AI_VISION_BASE_URL', ''),
            'AI_VISION_API_KEY': current_app.config.get('AI_VISION_API_KEY', ''),
            'AI_VISION_MODEL': current_app.config.get('AI_VISION_MODEL', ''),
            'AI_ASSISTANT_TIMEOUT': current_app.config.get('AI_ASSISTANT_TIMEOUT', 30),
        }

        if data.get('base_url'):
            runtime_config['AI_ASSISTANT_BASE_URL'] = str(data.get('base_url')).strip()
        if data.get('model'):
            runtime_config['AI_ASSISTANT_MODEL'] = str(data.get('model')).strip()
        if data.get('api_key'):
            runtime_config['AI_ASSISTANT_API_KEY'] = str(data.get('api_key')).strip()
        if data.get('vision_base_url'):
            runtime_config['AI_VISION_BASE_URL'] = str(data.get('vision_base_url')).strip()
        if data.get('vision_model'):
            runtime_config['AI_VISION_MODEL'] = str(data.get('vision_model')).strip()
        if data.get('vision_api_key'):
            runtime_config['AI_VISION_API_KEY'] = str(data.get('vision_api_key')).strip()

        cases = synthesize_test_cases(base_request, count, runtime_config)
        return success_response(data={'cases': cases}, message='AI 用例扩充成功')
    except Exception as exc:
        return error_response(500, f'AI 用例扩充失败: {str(exc)}')

@api_bp.route('/api-test/ai/review-collection', methods=['POST'])
@jwt_required()
def review_collection_cases():
    """AI 智能评审测试用例集合并补充用例"""
    user_id = get_current_user_id()
    data = request.get_json() or {}
    collection_id = data.get('collection_id')
    
    if not collection_id:
        return error_response(400, 'collection_id is required')
        
    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    if not collection:
        return error_response(404, '集合不存在')
        
    cases = ApiTestCase.query.filter_by(collection_id=collection_id, user_id=user_id).all()
    if not cases:
        return error_response(400, '该集合下没有测试用例，无法评审')
        
    case_list = []
    for c in cases:
        case_list.append({
            'name': c.name,
            'method': c.method,
            'url': c.url,
            'headers': c.headers,
            'params': c.params,
            'body': c.body,
            'body_type': c.body_type,
        })
        
    try:
        runtime_config = {
            'AI_ASSISTANT_ENABLED': current_app.config.get('AI_ASSISTANT_ENABLED', True),
            'AI_ASSISTANT_BASE_URL': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
            'AI_ASSISTANT_API_KEY': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
            'AI_ASSISTANT_MODEL': current_app.config.get('AI_ASSISTANT_MODEL', ''),
            'AI_VISION_BASE_URL': current_app.config.get('AI_VISION_BASE_URL', ''),
            'AI_VISION_API_KEY': current_app.config.get('AI_VISION_API_KEY', ''),
            'AI_VISION_MODEL': current_app.config.get('AI_VISION_MODEL', ''),
            'AI_ASSISTANT_TIMEOUT': current_app.config.get('AI_ASSISTANT_TIMEOUT', 60),
        }

        if data.get('base_url'):
            runtime_config['AI_ASSISTANT_BASE_URL'] = str(data.get('base_url')).strip()
        if data.get('model'):
            runtime_config['AI_ASSISTANT_MODEL'] = str(data.get('model')).strip()
        if data.get('api_key'):
            runtime_config['AI_ASSISTANT_API_KEY'] = str(data.get('api_key')).strip()
        if data.get('vision_base_url'):
            runtime_config['AI_VISION_BASE_URL'] = str(data.get('vision_base_url')).strip()
        if data.get('vision_model'):
            runtime_config['AI_VISION_MODEL'] = str(data.get('vision_model')).strip()
        if data.get('vision_api_key'):
            runtime_config['AI_VISION_API_KEY'] = str(data.get('vision_api_key')).strip()

        result = review_api_collection(collection.name, case_list, runtime_config)
        return success_response(data=result, message='AI 评审完成')
    except Exception as exc:
        return error_response(500, f'AI 评审失败: {str(exc)}')



# ==================== 用例集合 ====================

@api_bp.route('/api-test/collections', methods=['GET'])
@jwt_required()
def get_collections():
    """获取用例集合列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    
    query = ApiTestCollection.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    collections = query.order_by(ApiTestCollection.created_at.desc()).all()
    
    return success_response(data=[c.to_dict() for c in collections])


@api_bp.route('/api-test/collections', methods=['POST'])
@jwt_required()
def create_collection():
    """创建用例集合"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    error = validate_required(data, ['name'])
    if error:
        return error_response(message=error)
    
    collection = ApiTestCollection(
        name=data['name'],
        description=data.get('description', ''),
        project_id=data.get('project_id'),
        user_id=user_id
    )
    
    db.session.add(collection)
    db.session.commit()
    
    return success_response(data=collection.to_dict(), message='创建成功')


@api_bp.route('/api-test/collections/<int:collection_id>', methods=['PUT'])
@jwt_required()
def update_collection(collection_id):
    """更新用例集合"""
    user_id = get_current_user_id()
    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    
    if not collection:
        return error_response(message='集合不存在', code=404)
    
    data = request.get_json()
    if 'name' in data:
        collection.name = data['name']
    if 'description' in data:
        collection.description = data['description']
    
    db.session.commit()
    
    return success_response(data=collection.to_dict(), message='更新成功')


@api_bp.route('/api-test/collections/<int:collection_id>', methods=['DELETE'])
@jwt_required()
def delete_collection(collection_id):
    """删除用例集合"""
    user_id = get_current_user_id()
    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    
    if not collection:
        return error_response(message='集合不存在', code=404)
    
    db.session.delete(collection)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 测试用例 ====================

@api_bp.route('/api-test/cases', methods=['GET'])
@jwt_required()
def get_cases():
    """获取测试用例列表"""
    user_id = get_current_user_id()
    collection_id = request.args.get('collection_id', type=int)
    project_id = request.args.get('project_id', type=int)
    
    query = ApiTestCase.query.filter_by(user_id=user_id)
    if collection_id:
        query = query.filter_by(collection_id=collection_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    cases = query.order_by(ApiTestCase.created_at.desc()).all()
    
    return success_response(data=[c.to_dict() for c in cases])


@api_bp.route('/api-test/cases', methods=['POST'])
@jwt_required()
def create_case():
    """创建测试用例"""
    user_id = get_current_user_id()
    data = request.get_json()

    error = validate_required(data, ['name', 'method', 'url'])
    if error:
        return error_response(message=error)

    case = ApiTestCase(
        name=data['name'],
        description=data.get('description', ''),
        method=data['method'].upper(),
        url=data['url'],
        headers=data.get('headers', {}),
        params=data.get('params', {}),
        body=data.get('body'),
        body_type=data.get('body_type', 'json'),
        pre_script=data.get('pre_script'),
        post_script=data.get('post_script'),
        assertions=data.get('assertions', []),
        collection_id=data.get('collection_id'),
        project_id=data.get('project_id'),
        environment_id=data.get('environment_id'),
        user_id=user_id,
        mock_enabled=data.get('mock_enabled', False),
        mock_response_code=data.get('mock_response_code', 200),
        mock_response_body=data.get('mock_response_body', ''),
        mock_response_headers=data.get('mock_response_headers', {}),
        mock_delay_ms=data.get('mock_delay_ms', 0)
    )

    db.session.add(case)
    db.session.commit()

    return success_response(data=case.to_dict(), message='创建成功')


@api_bp.route('/api-test/cases/<int:case_id>', methods=['GET'])
@jwt_required()
def get_case(case_id):
    """获取用例详情"""
    user_id = get_current_user_id()
    case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
    
    if not case:
        return error_response(message='用例不存在', code=404)
    
    return success_response(data=case.to_dict())


@api_bp.route('/api-test/cases/<int:case_id>', methods=['PUT'])
@jwt_required()
def update_case(case_id):
    """更新测试用例"""
    user_id = get_current_user_id()
    case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
    
    if not case:
        return error_response(message='用例不存在', code=404)
    
    data = request.get_json()
    
    # 更新字段
    for field in ['name', 'description', 'method', 'url', 'headers', 'params',
                  'body', 'body_type', 'pre_script', 'post_script', 'assertions',
                  'collection_id', 'environment_id', 'mock_enabled', 
                  'mock_response_code', 'mock_response_body', 
                  'mock_response_headers', 'mock_delay_ms']:
        if field in data:
            setattr(case, field, data[field])
    
    db.session.commit()
    
    return success_response(data=case.to_dict(), message='更新成功')


@api_bp.route('/api-test/mock/<int:case_id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def mock_api_endpoint(case_id):
    """
    Mock Server 端点
    根据用例 ID 返回预设的 Mock 数据
    允许跨域，方便前端直接调用
    """
    # 处理跨域 OPTIONS 请求
    if request.method == 'OPTIONS':
        resp = make_response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp

    case = ApiTestCase.query.get(case_id)
    
    if not case:
        return error_response(404, '用例不存在')
        
    if not case.mock_enabled:
        return error_response(400, '该用例未开启 Mock 功能')
        
    # 模拟延迟
    if case.mock_delay_ms and case.mock_delay_ms > 0:
        time.sleep(case.mock_delay_ms / 1000.0)
        
    # 构建响应
    resp = make_response(case.mock_response_body or '')
    resp.status_code = case.mock_response_code or 200
    
    # 设置响应头
    if case.mock_response_headers:
        for k, v in case.mock_response_headers.items():
            resp.headers[k] = v
            
    # 默认 Content-Type 为 application/json 如果未设置
    if 'Content-Type' not in [k.title() for k in (case.mock_response_headers or {}).keys()]:
        resp.headers['Content-Type'] = 'application/json'
        
    # 允许跨域
    resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

@api_bp.route('/api-test/cases/<int:case_id>', methods=['DELETE'])
@jwt_required()
def delete_case(case_id):
    """删除测试用例"""
    user_id = get_current_user_id()
    case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
    
    if not case:
        return error_response(message='用例不存在', code=404)
    
    db.session.delete(case)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 执行测试 ====================

@api_bp.route('/api-test/execute', methods=['POST'])
@jwt_required()
def execute_request():
    """
    执行 HTTP 请求（快速测试）

    不保存用例，直接执行并返回结果
    支持环境配置的应用、前置脚本和后置断言
    """
    user_id = get_current_user_id()
    data = request.get_json()

    error = validate_required(data, ['method', 'url'])
    if error:
        return error_response(message=error)

    method = data['method'].upper()
    url = data['url']
    headers = data.get('headers', {})
    params = data.get('params', {})
    body = data.get('body')
    body_type = data.get('body_type', 'json')
    timeout = data.get('timeout', 30)
    env_id = data.get('env_id')
    pre_script = data.get('pre_script', '')
    post_script = data.get('post_script', '')

    # 获取环境变量
    env_vars = {}
    if env_id:
        env = Environment.query.filter_by(id=env_id).first()
        if env:
            env_vars = env.variables or {}
            # 合并环境的 headers
            env_headers = env.headers or {}
            headers = {**env_headers, **headers}

    # ========== 前置脚本执行 ==========
    script_execution = {
        'pre_script': {'executed': False, 'passed': True},
        'post_script': {'executed': False, 'passed': True}
    }

    if pre_script and pre_script.strip():
        try:
            # 构建前置脚本上下文
            pre_context = build_pre_script_context(
                environment_vars=env_vars,
                request_data={
                    'method': method,
                    'url': url,
                    'headers': headers,
                    'params': params,
                    'body': body
                }
            )

            # 执行前置脚本
            executor = get_executor(timeout=3)
            pre_result = executor.execute_pre_script(pre_script, pre_context)
            script_execution['pre_script'] = pre_result

            # 前置脚本失败则直接返回
            if not pre_result.get('passed', True):
                return success_response(data={
                    'success': False,
                    'error': pre_result.get('error', '前置脚本执行失败'),
                    'script_execution': script_execution
                })

            # 应用前置脚本的修改
            request_data = {
                'method': method,
                'url': url,
                'headers': headers,
                'params': params,
                'body': body
            }
            request_data = apply_pre_script_changes(request_data, pre_result)
            url = request_data['url']
            headers = request_data['headers']
            body = request_data['body']

            # 更新环境变量（供后置脚本使用）
            env_vars = apply_env_changes(env_vars, pre_result)

        except Exception as e:
            logger.error(f"前置脚本执行异常: {str(e)}")
            return success_response(data={
                'success': False,
                'error': f'前置脚本执行异常: {str(e)}',
                'script_execution': script_execution
            })

    # 应用环境变量替换 ({{var}} 格式)
    if env_vars:
        url = replace_variables(url, env_vars)
        headers = replace_variables_in_dict(headers, env_vars)
        params = replace_variables_in_dict(params, env_vars)

    # 如果前端传来了 mock_enabled 参数并开启了 Mock，直接返回 Mock 数据
    if data.get('mock_enabled'):
        mock_body = data.get('mock_response_body')
        if mock_body and isinstance(mock_body, str):
            try:
                mock_body = json.loads(mock_body)
            except Exception:
                pass
                
        mock_delay_ms = data.get('mock_delay_ms', 0)
        if mock_delay_ms and mock_delay_ms > 0:
            time.sleep(mock_delay_ms / 1000.0)
            
        return success_response(data={
            'success': True,
            'status_code': data.get('mock_response_code', 200),
            'body': mock_body,
            'headers': data.get('mock_response_headers', {}),
            'response_time': mock_delay_ms,
            'script_execution': script_execution,
            'passed': True,
            'is_mock': True
        })

    # 如果是通过集合等触发且依赖数据库 case (作为兜底)
    case_id = data.get('case_id')
    if case_id and not data.get('mock_enabled'):
        case = ApiTestCase.query.get(case_id)
        if case and case.mock_enabled:
            mock_body = case.mock_response_body
            if mock_body:
                try:
                    mock_body = json.loads(mock_body)
                except Exception:
                    pass
                    
            if case.mock_delay_ms and case.mock_delay_ms > 0:
                time.sleep(case.mock_delay_ms / 1000.0)
                
            return success_response(data={
                'success': True,
                'status_code': case.mock_response_code or 200,
                'body': mock_body,
                'headers': case.mock_response_headers or {},
                'response_time': case.mock_delay_ms or 0,
                'script_execution': script_execution,
                'passed': True,
                'is_mock': True
            })

    # 执行请求
    start_time = time.time()

    try:
        # 准备请求参数
        request_kwargs = {
            'method': method,
            'url': url,
            'headers': headers,
            'params': params,
            'timeout': timeout,
            'verify': False,
            'allow_redirects': True
        }

        # 处理请求体
        if body and method in ['POST', 'PUT', 'PATCH']:
            if body_type == 'json':
                request_kwargs['json'] = body
            elif body_type == 'form':
                request_kwargs['data'] = body
            else:
                request_kwargs['data'] = body

        # 发送请求
        response = requests.request(**request_kwargs)

        elapsed_time = (time.time() - start_time) * 1000

        # 尝试解析 JSON 响应
        try:
            response_body = response.json()
        except:
            response_body = response.text

        # 计算响应大小
        response_size = len(response.content)
        if response_size > 1024 * 1024:
            size_str = f'{response_size / (1024 * 1024):.2f} MB'
        elif response_size > 1024:
            size_str = f'{response_size / 1024:.2f} KB'
        else:
            size_str = f'{response_size} B'

        # ========== 后置断言执行 ==========
        if post_script and post_script.strip():
            try:
                # 构建后置断言上下文
                post_context = build_post_script_context(
                    environment_vars=env_vars,
                    response_data={
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'body': response_body,
                        'response_time': round(elapsed_time, 2),
                        'response_size': size_str
                    }
                )

                # 执行后置断言
                executor = get_executor(timeout=3)
                post_result = executor.execute_post_script(post_script, post_context)
                script_execution['post_script'] = post_result

            except Exception as e:
                logger.error(f"后置断言执行异常: {str(e)}")
                script_execution['post_script'] = {
                    'executed': True,
                    'passed': False,
                    'error': str(e),
                    'assertions': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
                }

        return success_response(data={
            'success': True,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response_body,
            'response_time': round(elapsed_time, 2),
            'response_size': size_str,
            'cookies': dict(response.cookies),
            'script_execution': script_execution
        })

    except requests.exceptions.Timeout:
        elapsed_time = (time.time() - start_time) * 1000
        return success_response(data={
            'success': False,
            'error': '请求超时',
            'response_time': round(elapsed_time, 2),
            'script_execution': script_execution
        })

    except requests.exceptions.ConnectionError as e:
        elapsed_time = (time.time() - start_time) * 1000
        return success_response(data={
            'success': False,
            'error': f'连接错误: {str(e)}',
            'response_time': round(elapsed_time, 2),
            'script_execution': script_execution
        })

    except Exception as e:
        elapsed_time = (time.time() - start_time) * 1000
        return success_response(data={
            'success': False,
            'error': str(e),
            'response_time': round(elapsed_time, 2),
            'script_execution': script_execution
        })


@api_bp.route('/api-test/cases/<int:case_id>/run', methods=['POST'])
@jwt_required()
def run_case(case_id):
    """执行单个测试用例（支持前置脚本和后置断言）"""
    user_id = get_current_user_id()
    case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()

    if not case:
        return error_response(message='用例不存在', code=404)

    # 获取环境ID（从请求参数中）
    env_id = request.args.get('env_id', type=int)

    # 获取环境变量
    env_vars = {}
    if env_id:
        env = Environment.query.filter_by(id=env_id).first()
        if env:
            env_vars = env.variables or {}

    # 脚本执行结果
    script_execution = {
        'pre_script': {'executed': False, 'passed': True},
        'post_script': {'executed': False, 'passed': True}
    }

    # ========== 前置脚本执行 ==========
    if case.pre_script and case.pre_script.strip():
        try:
            pre_context = build_pre_script_context(
                environment_vars=env_vars,
                request_data={
                    'method': case.method,
                    'url': case.url,
                    'headers': case.headers or {},
                    'params': case.params or {},
                    'body': case.body
                }
            )

            executor = get_executor(timeout=3)
            pre_result = executor.execute_pre_script(case.pre_script, pre_context)
            script_execution['pre_script'] = pre_result

            # 前置脚本失败
            if not pre_result.get('passed', True):
                case.last_run_at = datetime.utcnow()
                case.last_status = 'failed'
                db.session.commit()

                return success_response(data={
                    'success': False,
                    'error': pre_result.get('error', '前置脚本执行失败'),
                    'script_execution': script_execution
                })

            # 应用前置脚本的修改
            url = case.url
            headers = case.headers or {}
            params = case.params or {}
            body = case.body

            request_data = apply_pre_script_changes({
                'method': case.method,
                'url': url,
                'headers': headers,
                'params': params,
                'body': body
            }, pre_result)

            url = request_data['url']
            headers = request_data['headers']
            body = request_data['body']

            # 更新环境变量
            env_vars = apply_env_changes(env_vars, pre_result)

        except Exception as e:
            logger.error(f"前置脚本执行异常: {str(e)}")
            case.last_run_at = datetime.utcnow()
            case.last_status = 'failed'
            db.session.commit()

            return success_response(data={
                'success': False,
                'error': f'前置脚本执行异常: {str(e)}',
                'script_execution': script_execution
            })
    else:
        url = case.url
        headers = case.headers or {}
        params = case.params or {}
        body = case.body

    # 如果开启了 Mock，直接返回 Mock 数据
    if case.mock_enabled:
        case.last_run_at = datetime.utcnow()
        case.last_status = 'passed'
        
        mock_result = {
            'success': True,
            'status_code': case.mock_response_code or 200,
            'body': case.mock_response_body,
            'headers': case.mock_response_headers,
            'response_time': case.mock_delay_ms or 0,
            'script_execution': script_execution,
            'passed': True,
            'is_mock': True
        }
        
        case.last_result = mock_result
        db.session.commit()
        
        return success_response(data=mock_result)

    # 应用环境变量替换
    if env_vars:
        url = replace_variables(url, env_vars)
        headers = replace_variables_in_dict(headers, env_vars)
        params = replace_variables_in_dict(params, env_vars)
        if isinstance(body, dict):
            body = replace_variables_in_dict(body, env_vars)
        elif isinstance(body, str):
            body = replace_variables(body, env_vars)

    # 合并环境 headers
    if env_id:
        headers = merge_headers_with_env(headers, env_id, db)

    # 执行请求
    start_time = time.time()

    try:
        request_kwargs = {
            'method': case.method,
            'url': url,
            'headers': headers,
            'params': params,
            'timeout': case.timeout or 30,
            'verify': False,
            'allow_redirects': True
        }

        if case.body and case.method in ['POST', 'PUT', 'PATCH']:
            if case.body_type == 'json':
                request_kwargs['json'] = body
            else:
                request_kwargs['data'] = body

        response = requests.request(**request_kwargs)
        elapsed_time = (time.time() - start_time) * 1000

        try:
            response_body = response.json()
        except:
            response_body = response.text

        # ========== 后置断言执行 ==========
        if case.post_script and case.post_script.strip():
            try:
                post_context = build_post_script_context(
                    environment_vars=env_vars,
                    response_data={
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'body': response_body,
                        'response_time': round(elapsed_time, 2)
                    }
                )

                executor = get_executor(timeout=3)
                post_result = executor.execute_post_script(case.post_script, post_context)
                script_execution['post_script'] = post_result

            except Exception as e:
                logger.error(f"后置断言执行异常: {str(e)}")
                script_execution['post_script'] = {
                    'executed': True,
                    'passed': False,
                    'error': str(e),
                    'assertions': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
                }

        # 计算最终通过状态
        has_script = bool(case.pre_script or case.post_script)
        passed = calculate_case_passed(
            script_execution,
            response.status_code,
            has_script=has_script
        )

        # 更新用例状态
        case.last_run_at = datetime.utcnow()
        case.last_status = 'passed' if passed else 'failed'
        db.session.commit()

        return success_response(data={
            'success': True,
            'status_code': response.status_code,
            'body': response_body,
            'response_time': round(elapsed_time, 2),
            'script_execution': script_execution,
            'passed': passed
        })

    except Exception as e:
        case.last_run_at = datetime.utcnow()
        case.last_status = 'failed'
        db.session.commit()

        return success_response(data={
            'success': False,
            'error': str(e),
            'script_execution': script_execution
        })


@api_bp.route('/api-test/collections/<int:collection_id>/run', methods=['POST'])
@jwt_required()
def run_collection(collection_id):
    """批量执行集合中的所有用例，并生成测试报告"""
    user_id = get_current_user_id()
    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    
    if not collection:
        return error_response(message='集合不存在', code=404)
    
    cases = ApiTestCase.query.filter_by(collection_id=collection_id, is_enabled=True).all()
    
    if not cases:
        return error_response(message='集合中没有可执行的用例')
    
    # 获取环境ID（从请求体或参数中）
    # None 表示使用各用例自身的 environment_id，而非统一环境
    data = request.get_json() or {}
    # 注意：使用 'env_id' in data 来区分未传递和传递 None
    env_id = data.get('env_id') if 'env_id' in data else request.args.get('env_id', type=int)

    # 获取统一环境信息（如果指定了env_id）
    unified_env_name = None
    unified_env_variables = {}
    env = None  # 初始化env变量
    if env_id is not None:
        env = db.session.get(Environment, env_id)
        if env:
            unified_env_name = env.name
            unified_env_variables = env.variables or {}
    
    # 判断是否使用统一环境模式
    use_unified_env = env_id is not None
    
    # 创建测试执行记录
    # 如果集合没有 project_id，尝试从环境或第一个用例获取
    project_id = collection.project_id
    if not project_id:
        # 尝试从统一环境获取 project_id
        if use_unified_env and env:
            project_id = env.project_id
        # 如果没有统一环境，尝试从第一个用例获取
        if not project_id and cases:
            project_id = cases[0].project_id
            # 如果用例本身也没有 project_id，但用例有环境，从用例的环境获取
            if not project_id and cases[0].environment_id:
                case_env = db.session.get(Environment, cases[0].environment_id)
                if case_env:
                    project_id = case_env.project_id

    test_run = TestRun(
        project_id=project_id,  # 使用获取到的 project_id
        test_type='api',
        test_object_id=collection_id,
        test_object_name=collection.name,
        status='running',
        total_cases=len(cases),
        environment_id=env_id,
        environment_name=unified_env_name if use_unified_env else '用例自身环境',
        started_at=datetime.utcnow(),
        triggered_by='manual',
        triggered_user_id=user_id
    )
    db.session.add(test_run)
    db.session.commit()
    
    def _safe_text(value, limit=2000):
        """将数据安全转成可展示的文本，限制长度"""
        try:
            if isinstance(value, (dict, list)):
                text = json.dumps(value, ensure_ascii=False)
            else:
                text = str(value)
        except Exception:
            text = str(value)
        return text if len(text) <= limit else text[:limit] + '...'

    results = []
    total_passed = 0
    total_failed = 0
    start_time = time.time()
    
    for case in cases:
        case_start_time = time.time()

        # 初始化脚本执行结果
        script_execution = {
            'pre_script': {'executed': False, 'passed': True},
            'post_script': {'executed': False, 'passed': True}
        }

        try:
            # 如果开启了 Mock，直接走 Mock 逻辑
            if case.mock_enabled:
                case.last_run_at = datetime.utcnow()
                case.last_status = 'passed'
                
                mock_result = {
                    'case_id': case.id,
                    'name': case.name,
                    'method': case.method,
                    'url': case.url,
                    'passed': True,
                    'status_code': case.mock_response_code or 200,
                    'response_time': case.mock_delay_ms or 0,
                    'response_body': case.mock_response_body,
                    'response_headers': case.mock_response_headers,
                    'response_cookies': {},
                    'request_headers': case.headers,
                    'request_params': case.params,
                    'request_body': case.body,
                    'attachments': [],
                    'script_execution': script_execution,
                    'environment_id': env_id,
                    'environment_name': unified_env_name,
                    'is_mock': True
                }
                
                total_passed += 1
                results.append(mock_result)
                case.last_result = {
                    'success': True,
                    'status_code': case.mock_response_code or 200,
                    'body': case.mock_response_body,
                    'headers': case.mock_response_headers,
                    'response_time': case.mock_delay_ms or 0,
                    'script_execution': script_execution,
                    'passed': True,
                    'is_mock': True
                }
                db.session.commit()
                continue

            # 准备请求参数
            url = case.url
            headers = case.headers or {}
            params = case.params or {}
            body = case.body

            # 确定实际使用的环境ID和变量
            effective_env_id = env_id if use_unified_env else case.environment_id
            effective_env_name = unified_env_name if use_unified_env else None
            effective_env_variables = dict(unified_env_variables) if use_unified_env else {}

            # 如果不是统一环境模式，且用例有自己的环境ID，获取该环境的配置
            if not use_unified_env and case.environment_id:
                case_env = db.session.get(Environment, case.environment_id)
                if case_env:
                    effective_env_name = case_env.name
                    effective_env_variables = dict(case_env.variables or {})

            logger.info(f"执行用例 {case.id}: {case.name} - {case.method} {url} [环境: {effective_env_name or '无'}]")

            # ========== 前置脚本执行 ==========
            if case.pre_script and case.pre_script.strip():
                try:
                    pre_context = build_pre_script_context(
                        environment_vars=effective_env_variables,
                        request_data={
                            'method': case.method,
                            'url': url,
                            'headers': headers,
                            'params': params,
                            'body': body
                        }
                    )

                    executor = get_executor(timeout=3)
                    pre_result = executor.execute_pre_script(case.pre_script, pre_context)
                    script_execution['pre_script'] = pre_result

                    # 前置脚本失败，跳过该用例
                    if not pre_result.get('passed', True):
                        elapsed_time = (time.time() - case_start_time) * 1000
                        total_failed += 1
                        case.last_run_at = datetime.utcnow()
                        case.last_status = 'failed'
                        db.session.commit()

                        logger.warning(f"用例 {case.name} 前置脚本执行失败，跳过")

                        results.append({
                            'case_id': case.id,
                            'name': case.name,
                            'method': case.method,
                            'url': url,
                            'passed': False,
                            'status_code': None,
                            'response_time': round(elapsed_time, 2),
                            'script_execution': script_execution,
                            'error': pre_result.get('error', '前置脚本执行失败'),
                            'environment_id': effective_env_id,
                            'environment_name': effective_env_name
                        })
                        continue

                    # 应用前置脚本的修改
                    request_data = apply_pre_script_changes({
                        'method': case.method,
                        'url': url,
                        'headers': headers,
                        'params': params,
                        'body': body
                    }, pre_result)

                    url = request_data['url']
                    headers = request_data['headers']
                    body = request_data['body']

                    # 更新环境变量
                    effective_env_variables = apply_env_changes(effective_env_variables, pre_result)

                except Exception as e:
                    logger.error(f"前置脚本执行异常: {str(e)}")
                    elapsed_time = (time.time() - case_start_time) * 1000
                    total_failed += 1
                    case.last_run_at = datetime.utcnow()
                    case.last_status = 'failed'
                    db.session.commit()

                    script_execution['pre_script'] = {
                        'executed': True,
                        'passed': False,
                        'error': str(e)
                    }

                    results.append({
                        'case_id': case.id,
                        'name': case.name,
                        'method': case.method,
                        'url': url,
                        'passed': False,
                        'status_code': None,
                        'response_time': round(elapsed_time, 2),
                        'script_execution': script_execution,
                        'error': f'前置脚本执行异常: {str(e)}',
                        'environment_id': effective_env_id,
                        'environment_name': effective_env_name
                    })
                    continue

            # 应用环境变量替换
            if effective_env_variables:
                try:
                    url = replace_variables(url, effective_env_variables)
                    headers = replace_variables_in_dict(headers, effective_env_variables)
                    params = replace_variables_in_dict(params, effective_env_variables)
                    if isinstance(body, dict):
                        body = replace_variables_in_dict(body, effective_env_variables)
                    elif isinstance(body, str):
                        body = replace_variables(body, effective_env_variables)
                    logger.debug(f"环境变量替换后 URL: {url}")
                except Exception as e:
                    logger.error(f"环境变量替换失败: {str(e)}")

            # 合并环境的公共请求头
            if effective_env_id:
                try:
                    headers = merge_headers_with_env(headers, effective_env_id, db)
                except Exception as e:
                    logger.error(f"合并请求头失败: {str(e)}")

            request_kwargs = {
                'method': case.method,
                'url': url,
                'headers': headers,
                'params': params,
                'timeout': case.timeout or 30,
                'verify': False
            }

            if body and case.method in ['POST', 'PUT', 'PATCH']:
                if case.body_type == 'json':
                    request_kwargs['json'] = body
                else:
                    request_kwargs['data'] = body

            response = requests.request(**request_kwargs)
            elapsed_time = (time.time() - case_start_time) * 1000

            # 尝试解析响应体
            try:
                response_body = response.json()
            except:
                response_body = response.text

            # ========== 后置断言执行 ==========
            if case.post_script and case.post_script.strip():
                try:
                    post_context = build_post_script_context(
                        environment_vars=effective_env_variables,
                        response_data={
                            'status_code': response.status_code,
                            'headers': dict(response.headers),
                            'body': response_body,
                            'response_time': round(elapsed_time, 2)
                        }
                    )

                    executor = get_executor(timeout=3)
                    post_result = executor.execute_post_script(case.post_script, post_context)
                    script_execution['post_script'] = post_result

                except Exception as e:
                    logger.error(f"后置断言执行异常: {str(e)}")
                    script_execution['post_script'] = {
                        'executed': True,
                        'passed': False,
                        'error': str(e),
                        'assertions': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
                    }

            # 计算最终通过状态
            has_script = bool(case.pre_script or case.post_script)
            passed = calculate_case_passed(
                script_execution,
                response.status_code,
                has_script=has_script
            )

            response_body_preview = _safe_text(response_body, limit=2000)
            response_headers = dict(response.headers)
            response_cookies = dict(response.cookies)
            request_body_preview = _safe_text(body, limit=2000) if body else None

            # 构造附件信息
            attachments = []
            attachments.append({
                'name': 'response_body',
                'type': 'text',
                'content': response_body_preview
            })
            attachments.append({
                'name': 'response_headers',
                'type': 'json',
                'content': _safe_text(response_headers, limit=2000)
            })
            if request_body_preview:
                attachments.append({
                    'name': 'request_body',
                    'type': 'text',
                    'content': request_body_preview
                })

            # 获取错误信息
            error_message = None
            if not passed:
                # 优先显示脚本错误
                pre_script_error = script_execution.get('pre_script', {}).get('error')
                post_script_error = script_execution.get('post_script', {}).get('error')

                if pre_script_error:
                    error_message = f"前置脚本失败: {pre_script_error}"
                elif post_script_error:
                    error_message = f"后置断言失败: {post_script_error}"
                elif response.status_code >= 400:
                    error_message = f"HTTP {response.status_code}"
                    if isinstance(response_body, str) and response_body:
                        error_message = f"{error_message}: {response_body_preview}"

            # 更新用例状态
            case.last_run_at = datetime.utcnow()
            case.last_status = 'passed' if passed else 'failed'

            if passed:
                total_passed += 1
                logger.info(f"用例 {case.name} 执行成功 - {response.status_code}")
            else:
                total_failed += 1
                logger.warning(f"用例 {case.name} 执行失败")

            results.append({
                'case_id': case.id,
                'name': case.name,
                'method': case.method,
                'url': url,
                'passed': passed,
                'status_code': response.status_code,
                'response_time': round(elapsed_time, 2),
                'response_body': response_body,
                'response_headers': response_headers,
                'response_cookies': response_cookies,
                'request_headers': headers,
                'request_params': params,
                'request_body': body,
                'attachments': attachments,
                'script_execution': script_execution,
                'error': error_message,
                'environment_id': effective_env_id,
                'environment_name': effective_env_name
            })

        except Exception as e:
            elapsed_time = (time.time() - case_start_time) * 1000
            total_failed += 1
            logger.error(f"执行用例 {case.id} ({case.name}) 失败: {str(e)}", exc_info=True)

            case.last_run_at = datetime.utcnow()
            case.last_status = 'failed'
            db.session.commit()

            # 捕获可能存在的响应信息
            resp = getattr(e, 'response', None)
            resp_status = getattr(resp, 'status_code', None) if resp else None
            resp_headers = dict(resp.headers) if resp else None
            resp_cookies = dict(resp.cookies) if resp else None
            resp_body = None
            if resp is not None:
                try:
                    resp_body = resp.json()
                except Exception:
                    try:
                        resp_body = resp.text
                    except Exception:
                        resp_body = None

            error_preview = _safe_text(str(e), limit=1000)
            attachments = [
                {
                    'name': 'exception',
                    'type': 'text',
                    'content': error_preview
                }
            ]
            if resp_body is not None:
                attachments.append({
                    'name': 'response_body',
                    'type': 'text',
                    'content': _safe_text(resp_body, limit=2000)
                })

            results.append({
                'case_id': case.id,
                'name': case.name,
                'method': case.method,
                'url': case.url,
                'passed': False,
                'status_code': resp_status,
                'response_time': round(elapsed_time, 2),
                'response_body': resp_body,
                'response_headers': resp_headers,
                'response_cookies': resp_cookies,
                'request_headers': headers if 'headers' in locals() else {},
                'request_params': params if 'params' in locals() else {},
                'request_body': body if 'body' in locals() else None,
                'attachments': attachments,
                'script_execution': script_execution,
                'error': error_preview,
                'environment_id': effective_env_id if 'effective_env_id' in locals() else None,
                'environment_name': effective_env_name if 'effective_env_name' in locals() else None
            })
    
    # 计算总耗时
    total_duration = time.time() - start_time
    
    # 更新测试执行记录
    test_run.status = 'success' if total_failed == 0 else 'failed'
    test_run.passed = total_passed
    test_run.failed = total_failed
    test_run.duration = total_duration
    test_run.finished_at = datetime.utcnow()
    test_run.results = results
    
    # 生成测试报告
    report = TestReport(
        test_run_id=test_run.id,
        project_id=project_id,  # 使用相同的 project_id
        test_type='api',
        title=f'{collection.name} - 接口测试报告',
        summary={
            'total': len(cases),
            'passed': total_passed,
            'failed': total_failed,
            'success_rate': round(total_passed / len(cases) * 100, 2) if cases else 0,
            'duration': round(total_duration, 2),
            'environment': unified_env_name if use_unified_env else '混合环境',
            'environment_mode': 'unified' if use_unified_env else 'individual'
        },
        report_data={
            'collection': {
                'id': collection.id,
                'name': collection.name,
                'description': collection.description
            },
            'environment': {
                'id': env_id,
                'name': unified_env_name,
                'mode': 'unified'
            } if use_unified_env else {
                'mode': 'individual',
                'description': '各用例使用自身配置的环境'
            },
            'results': results
        },
        status='generated'
    )
    
    db.session.add(report)
    test_run.report_id = report.id
    db.session.commit()
    
    return success_response(data={
        'test_run_id': test_run.id,
        'report_id': report.id,
        'total': len(cases),
        'passed': total_passed,
        'failed': total_failed,
        'duration': round(total_duration, 2),
        'results': results
    }, message='测试执行完成')
