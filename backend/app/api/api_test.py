"""
接口测试模块 - API
实现接口测试相关功能：用例管理、执行测试、结果存储
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.api_test_case import ApiTestCollection, ApiTestCase
from ..models.environment import Environment
from ..models.test_run import TestRun
from ..models.test_report import TestReport
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
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
import time
from datetime import datetime

# 配置日志
logger = logging.getLogger(__name__)


@api_bp.route('/api-test/health', methods=['GET'])
def api_test_health():
    """接口测试模块健康检查"""
    return success_response(message='接口测试模块正常')


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
        user_id=user_id
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
                  'body', 'body_type', 'pre_script', 'post_script', 'assertions', 'environment_id']:
        if field in data:
            setattr(case, field, data[field])
    
    db.session.commit()
    
    return success_response(data=case.to_dict(), message='更新成功')


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
        started_at=datetime.utcnow()
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
