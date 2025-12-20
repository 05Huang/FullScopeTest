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
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
import requests
import json
import time
from datetime import datetime


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
                  'body', 'body_type', 'pre_script', 'post_script', 'assertions']:
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
    支持环境配置的应用
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
    
    # 应用环境配置
    if env_id:
        env = Environment.query.filter_by(id=env_id).first()
        if env:
            # 合并环境的 headers
            env_headers = env.headers or {}
            headers = {**env_headers, **headers}
            
            # 处理环境变量替换 ({{var}} 格式)
            env_vars = env.variables or {}
            
            # 替换 URL 中的变量
            for var_name, var_value in env_vars.items():
                url = url.replace(f'{{{{{var_name}}}}}', str(var_value))
            
            # 替换 headers 中的变量
            for key, value in headers.items():
                if isinstance(value, str):
                    for var_name, var_value in env_vars.items():
                        value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                    headers[key] = value
            
            # 替换 params 中的变量
            for key, value in params.items():
                if isinstance(value, str):
                    for var_name, var_value in env_vars.items():
                        value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                    params[key] = value
    
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
            'verify': False,  # 跳过 SSL 验证
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
        
        elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
        
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
        
        return success_response(data={
            'success': True,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response_body,
            'response_time': round(elapsed_time, 2),
            'response_size': size_str,
            'cookies': dict(response.cookies)
        })
        
    except requests.exceptions.Timeout:
        elapsed_time = (time.time() - start_time) * 1000
        return success_response(data={
            'success': False,
            'error': '请求超时',
            'response_time': round(elapsed_time, 2)
        })
        
    except requests.exceptions.ConnectionError as e:
        elapsed_time = (time.time() - start_time) * 1000
        return success_response(data={
            'success': False,
            'error': f'连接错误: {str(e)}',
            'response_time': round(elapsed_time, 2)
        })
        
    except Exception as e:
        elapsed_time = (time.time() - start_time) * 1000
        return success_response(data={
            'success': False,
            'error': str(e),
            'response_time': round(elapsed_time, 2)
        })


@api_bp.route('/api-test/cases/<int:case_id>/run', methods=['POST'])
@jwt_required()
def run_case(case_id):
    """执行单个测试用例"""
    user_id = get_current_user_id()
    case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
    
    if not case:
        return error_response(message='用例不存在', code=404)
    
    # 获取环境ID（从请求参数中）
    env_id = request.args.get('env_id', type=int)
    
    # 执行请求
    start_time = time.time()
    
    try:
        # 准备初始请求参数
        url = case.url
        headers = case.headers or {}
        params = case.params or {}
        
        # 应用环境配置
        if env_id:
            env = Environment.query.filter_by(id=env_id).first()
            if env:
                # 合并环境的 headers
                env_headers = env.headers or {}
                headers = {**env_headers, **headers}
                
                # 处理环境变量替换
                env_vars = env.variables or {}
                
                # 替换 URL 中的变量
                for var_name, var_value in env_vars.items():
                    url = url.replace(f'{{{{{var_name}}}}}', str(var_value))
                
                # 替换 headers 中的变量
                for key, value in headers.items():
                    if isinstance(value, str):
                        for var_name, var_value in env_vars.items():
                            value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                        headers[key] = value
                
                # 替换 params 中的变量
                for key, value in params.items():
                    if isinstance(value, str):
                        for var_name, var_value in env_vars.items():
                            value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                        params[key] = value
        
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
                request_kwargs['json'] = case.body
            else:
                request_kwargs['data'] = case.body
        
        response = requests.request(**request_kwargs)
        elapsed_time = (time.time() - start_time) * 1000
        
        # 更新用例状态
        case.last_run_at = datetime.utcnow()
        case.last_status = 'passed' if response.status_code < 400 else 'failed'
        db.session.commit()
        
        try:
            response_body = response.json()
        except:
            response_body = response.text
        
        return success_response(data={
            'success': True,
            'status_code': response.status_code,
            'body': response_body,
            'response_time': round(elapsed_time, 2)
        })
        
    except Exception as e:
        case.last_run_at = datetime.utcnow()
        case.last_status = 'failed'
        db.session.commit()
        
        return success_response(data={
            'success': False,
            'error': str(e)
        })


@api_bp.route('/api-test/collections/<int:collection_id>/run', methods=['POST'])
@jwt_required()
def run_collection(collection_id):
    """批量执行集合中的所有用例"""
    user_id = get_current_user_id()
    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    
    if not collection:
        return error_response(message='集合不存在', code=404)
    
    cases = ApiTestCase.query.filter_by(collection_id=collection_id, is_enabled=True).all()
    
    if not cases:
        return error_response(message='集合中没有可执行的用例')
    
    # 获取环境ID（从请求参数中）
    env_id = request.args.get('env_id', type=int)
    
    results = []
    total_passed = 0
    total_failed = 0
    
    for case in cases:
        try:
            # 准备初始请求参数
            url = case.url
            headers = case.headers or {}
            params = case.params or {}
            
            # 应用环境配置
            if env_id:
                env = Environment.query.filter_by(id=env_id).first()
                if env:
                    # 合并环境的 headers
                    env_headers = env.headers or {}
                    headers = {**env_headers, **headers}
                    
                    # 处理环境变量替换
                    env_vars = env.variables or {}
                    
                    # 替换 URL 中的变量
                    for var_name, var_value in env_vars.items():
                        url = url.replace(f'{{{{{var_name}}}}}', str(var_value))
                    
                    # 替换 headers 中的变量
                    for key, value in headers.items():
                        if isinstance(value, str):
                            for var_name, var_value in env_vars.items():
                                value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                            headers[key] = value
                    
                    # 替换 params 中的变量
                    for key, value in params.items():
                        if isinstance(value, str):
                            for var_name, var_value in env_vars.items():
                                value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
                            params[key] = value
            
            request_kwargs = {
                'method': case.method,
                'url': url,
                'headers': headers,
                'params': params,
                'timeout': case.timeout or 30,
                'verify': False
            }
            
            if case.body and case.method in ['POST', 'PUT', 'PATCH']:
                if case.body_type == 'json':
                    request_kwargs['json'] = case.body
                else:
                    request_kwargs['data'] = case.body
            
            start_time = time.time()
            response = requests.request(**request_kwargs)
            elapsed_time = (time.time() - start_time) * 1000
            
            passed = response.status_code < 400
            
            case.last_run_at = datetime.utcnow()
            case.last_status = 'passed' if passed else 'failed'
            
            if passed:
                total_passed += 1
            else:
                total_failed += 1
            
            results.append({
                'case_id': case.id,
                'name': case.name,
                'passed': passed,
                'status_code': response.status_code,
                'response_time': round(elapsed_time, 2)
            })
            
        except Exception as e:
            total_failed += 1
            case.last_run_at = datetime.utcnow()
            case.last_status = 'failed'
            
            results.append({
                'case_id': case.id,
                'name': case.name,
                'passed': False,
                'error': str(e)
            })
    
    db.session.commit()
    
    return success_response(data={
        'total': len(cases),
        'passed': total_passed,
        'failed': total_failed,
        'results': results
    })
