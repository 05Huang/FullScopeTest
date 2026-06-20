"""
API 测试执行 Service

处理 HTTP 请求执行、前置/后置脚本、环境变量替换等核心执行逻辑
"""

import json
import time
import requests
from datetime import datetime, timezone

from .base import BaseService
from ..extensions import db
from ..models.api_test_case import ApiTestCase, ApiTestCollection
from ..models.environment import Environment
from ..models.project import Project
from ..models.test_run import TestRun
from ..models.test_report import TestReport
from ..utils.exceptions import NotFoundError, ValidationError
from ..utils.url_safety import is_safe_url
from ..utils.env_variables import (
    replace_variables, replace_variables_in_dict,
    get_environment_variables, merge_headers_with_env
)
from ..utils.js_executor import get_executor
from ..utils.assertion_evaluator import get_assertion_evaluator
from ..utils.script_context import (
    build_pre_script_context, build_post_script_context,
    apply_pre_script_changes, apply_env_changes, calculate_case_passed
)


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


class ApiExecutionService(BaseService):

    def _update_progress(self, key: str, data: dict):
        """更新执行进度到 Redis"""
        try:
            import redis as redis_lib
            import os
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
            r = redis_lib.from_url(redis_url, decode_responses=True, socket_timeout=1)
            r.setex(key, 300, json.dumps(data))  # TTL 5 分钟
        except Exception:
            pass  # Redis 不可用时静默忽略

    def get_progress(self, run_id: int) -> dict:
        """获取执行进度"""
        try:
            import redis as redis_lib
            import os
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
            r = redis_lib.from_url(redis_url, decode_responses=True, socket_timeout=1)
            data = r.get(f"test_run_progress:{run_id}")
            if data:
                return json.loads(data)
        except Exception:
            pass
        return None

    def execute_request(self, data: dict, user_id: int):
        """执行 HTTP 请求（快速测试）"""
        method = data.get('method', '').upper()
        url = data.get('url', '')
        headers = data.get('headers', {})
        params = data.get('params', {})
        body = data.get('body')
        body_type = data.get('body_type', 'json')
        timeout = data.get('timeout', 30)
        env_id = data.get('env_id')
        pre_script = data.get('pre_script', '')
        post_script = data.get('post_script', '')

        env_vars = {}
        if env_id:
            env = Environment.query.filter_by(id=env_id).first()
            if env:
                env_vars = env.variables or {}

        script_execution = {
            'pre_script': {'executed': False, 'passed': True},
            'post_script': {'executed': False, 'passed': True}
        }

        # ========== 前置脚本执行 ==========
        if pre_script and pre_script.strip():
            try:
                pre_context = build_pre_script_context(
                    environment_vars=env_vars,
                    request_data={'method': method, 'url': url, 'headers': headers, 'params': params, 'body': body}
                )
                executor = get_executor(timeout=3)
                pre_result = executor.execute_pre_script(pre_script, pre_context)
                script_execution['pre_script'] = pre_result

                if not pre_result.get('passed', True):
                    return {'success': False, 'error': pre_result.get('error', '前置脚本执行失败'), 'script_execution': script_execution}

                request_data = apply_pre_script_changes(
                    {'method': method, 'url': url, 'headers': headers, 'params': params, 'body': body}, pre_result
                )
                url = request_data['url']
                headers = request_data['headers']
                body = request_data['body']
                env_vars = apply_env_changes(env_vars, pre_result)

            except Exception as e:
                self.logger.error('前置脚本执行异常', error=str(e))
                return {'success': False, 'error': f'前置脚本执行异常: {str(e)}', 'script_execution': script_execution}

        # 应用环境变量替换
        if env_vars:
            url = replace_variables(url, env_vars)
            headers = replace_variables_in_dict(headers, env_vars)
            params = replace_variables_in_dict(params, env_vars)

        # 合并环境 headers
        if env_id:
            headers = merge_headers_with_env(headers, env_id, db)

        # Mock 响应处理
        if data.get('mock_enabled'):
            return self._handle_mock_response(data, script_execution)

        # 通过 case_id 检查 mock
        case_id = data.get('case_id')
        if case_id and not data.get('mock_enabled'):
            case = ApiTestCase.query.get(case_id)
            if case and case.mock_enabled:
                return self._handle_case_mock(case, script_execution)

        # SSRF 防护：校验最终 URL
        safe, reason = is_safe_url(url)
        if not safe:
            return {'success': False, 'error': reason, 'script_execution': script_execution}

        # 执行真实请求（携带可视化断言规则）
        return self._send_request(method, url, headers, params, body, body_type, timeout, script_execution, post_script, env_vars, data.get('assertions'))


    def run_case(self, case_id: int, user_id: int, env_id: int = None):
        """执行单个测试用例"""
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError('用例', case_id)

        env_vars = {}
        if env_id:
            env = Environment.query.filter_by(id=env_id).first()
            if env:
                env_vars = env.variables or {}

        script_execution = {
            'pre_script': {'executed': False, 'passed': True},
            'post_script': {'executed': False, 'passed': True}
        }

        url = case.url
        headers = case.headers or {}
        params = case.params or {}
        body = case.body

        # ========== 前置脚本执行 ==========
        if case.pre_script and case.pre_script.strip():
            try:
                pre_context = build_pre_script_context(
                    environment_vars=env_vars,
                    request_data={'method': case.method, 'url': url, 'headers': headers, 'params': params, 'body': body}
                )
                executor = get_executor(timeout=3)
                pre_result = executor.execute_pre_script(case.pre_script, pre_context)
                script_execution['pre_script'] = pre_result

                if not pre_result.get('passed', True):
                    case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
                    case.last_status = 'failed'
                    db.session.commit()
                    return {'success': False, 'error': pre_result.get('error', '前置脚本执行失败'), 'script_execution': script_execution}

                request_data = apply_pre_script_changes(
                    {'method': case.method, 'url': url, 'headers': headers, 'params': params, 'body': body}, pre_result
                )
                url = request_data['url']
                headers = request_data['headers']
                body = request_data['body']
                env_vars = apply_env_changes(env_vars, pre_result)

            except Exception as e:
                self.logger.error('前置脚本执行异常', error=str(e))
                case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
                case.last_status = 'failed'
                db.session.commit()
                return {'success': False, 'error': f'前置脚本执行异常: {str(e)}', 'script_execution': script_execution}


        # Mock 处理
        if case.mock_enabled:
            case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
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
            return mock_result

        # 应用环境变量替换
        if env_vars:
            url = replace_variables(url, env_vars)
            headers = replace_variables_in_dict(headers, env_vars)
            params = replace_variables_in_dict(params, env_vars)
            if isinstance(body, dict):
                body = replace_variables_in_dict(body, env_vars)
            elif isinstance(body, str):
                body = replace_variables(body, env_vars)

        if env_id:
            headers = merge_headers_with_env(headers, env_id, db)

        # SSRF 防护：校验最终 URL
        safe, reason = is_safe_url(url)
        if not safe:
            case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
            case.last_status = 'failed'
            db.session.commit()
            return {'success': False, 'error': reason, 'script_execution': script_execution}

        # 执行请求
        start_time = time.time()
        try:
            request_kwargs = {
                'method': case.method, 'url': url, 'headers': headers,
                'params': params, 'timeout': case.timeout or 30,
                'verify': False, 'allow_redirects': True
            }
            if body is not None and case.method in ['POST', 'PUT', 'PATCH']:
                if case.body_type == 'json':
                    request_kwargs['json'] = body
                else:
                    request_kwargs['data'] = body

            response = requests.request(**request_kwargs)
            elapsed_time = (time.time() - start_time) * 1000

            try:
                response_body = response.json()
            except Exception:
                response_body = response.text

            # 后置断言执行
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
                    self.logger.error('后置断言执行异常', error=str(e))
                    script_execution['post_script'] = {
                        'executed': True, 'passed': False, 'error': str(e),
                        'assertions': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
                    }

            # ========== 可视化断言执行 ==========
            if case.assertions:
                try:
                    evaluator = get_assertion_evaluator()
                    assertion_result = evaluator.evaluate(case.assertions, {
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'body': response_body,
                        'response_time': round(elapsed_time, 2),
                    })
                    script_execution['visual_assertions'] = assertion_result
                except Exception as e:
                    self.logger.error('可视化断言执行异常', error=str(e))
                    script_execution['visual_assertions'] = {
                        'total': 0, 'passed': 0, 'failed': 0,
                        'details': [], 'error': str(e)
                    }

            has_script = bool(case.pre_script or case.post_script or case.assertions)
            passed = calculate_case_passed(script_execution, response.status_code, has_script=has_script)

            case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
            case.last_status = 'passed' if passed else 'failed'
            db.session.commit()

            return {
                'success': True,
                'status_code': response.status_code,
                'body': response_body,
                'response_time': round(elapsed_time, 2),
                'script_execution': script_execution,
                'passed': passed
            }

        except Exception as e:
            case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
            case.last_status = 'failed'
            db.session.commit()
            return {'success': False, 'error': str(e), 'script_execution': script_execution}


    def create_pending_run(self, collection_id: int, user_id: int, env_id: int = None) -> int:
        """P30-5: 创建待执行的 run 记录并返回 run_id（用于异步模式）"""
        collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            raise NotFoundError('集合', collection_id)

        cases = ApiTestCase.query.filter_by(collection_id=collection_id, is_enabled=True).all()
        if not cases:
            raise ValidationError('集合中没有可执行的用例')

        env = db.session.get(Environment, env_id) if env_id else None
        project_id = self._resolve_project_id(collection, env, cases, user_id)

        test_run = TestRun(
            project_id=project_id,
            test_type='api',
            test_object_id=collection_id,
            test_object_name=collection.name,
            status='running',
            total_cases=len(cases),
            environment_id=env_id,
            environment_name=env.name if env else '用例自身环境',
            started_at=datetime.now(timezone.utc).replace(tzinfo=None),
            triggered_by='manual',
            triggered_user_id=user_id
        )
        db.session.add(test_run)
        db.session.commit()
        return test_run.id

    def run_collection(self, collection_id: int, user_id: int, env_id: int = None, existing_run_id: int = None):
        """批量执行集合中的所有用例，并生成测试报告

        Args:
            existing_run_id: P30-5 — 若传入则复用已创建的 run 记录（异步模式）
        """
        collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            raise NotFoundError('集合', collection_id)

        if collection.user_id != user_id:
            self.logger.warning('IDOR attempt blocked', user_id=user_id, collection_id=collection_id, actual_owner=collection.user_id)
            from ..utils.exceptions import PermissionError as PermErr
            raise PermErr('无权限执行该集合')

        cases = ApiTestCase.query.filter_by(collection_id=collection_id, is_enabled=True).all()
        if not cases:
            raise ValidationError('集合中没有可执行的用例')

        # 环境处理
        use_unified_env = env_id is not None
        unified_env_name = None
        unified_env_variables = {}
        env = None
        if env_id is not None:
            env = db.session.get(Environment, env_id)
            if env:
                unified_env_name = env.name
                unified_env_variables = env.variables or {}

        # 确定 project_id
        project_id = self._resolve_project_id(collection, env, cases, user_id)

        # 复用已有 run 记录或创建新的
        if existing_run_id:
            test_run = db.session.get(TestRun, existing_run_id)
            if not test_run:
                raise NotFoundError('执行记录', existing_run_id)
        else:
            test_run = TestRun(
                project_id=project_id,
                test_type='api',
                test_object_id=collection_id,
                test_object_name=collection.name,
                status='running',
                total_cases=len(cases),
                environment_id=env_id,
                environment_name=unified_env_name if use_unified_env else '用例自身环境',
                started_at=datetime.now(timezone.utc).replace(tzinfo=None),
                triggered_by='manual',
                triggered_user_id=user_id
            )
            db.session.add(test_run)
            db.session.commit()

        results = []
        total_passed = 0
        total_failed = 0
        start_time = time.time()
        total_cases = len(cases)

        # 初始化进度（写入 Redis）
        progress_key = f"test_run_progress:{test_run.id}"
        self._update_progress(progress_key, {
            'current': 0, 'total': total_cases,
            'passed': 0, 'failed': 0, 'status': 'running',
        })

        for idx, case in enumerate(cases):
            case_result = self._execute_single_case_in_collection(
                case, use_unified_env, env_id, unified_env_name, unified_env_variables
            )
            results.append(case_result['result'])
            if case_result['passed']:
                total_passed += 1
            else:
                total_failed += 1

            # 更新进度
            self._update_progress(progress_key, {
                'current': idx + 1, 'total': total_cases,
                'passed': total_passed, 'failed': total_failed,
                'status': 'running',
            })

        total_duration = time.time() - start_time

        # 更新最终进度
        self._update_progress(progress_key, {
            'current': total_cases, 'total': total_cases,
            'passed': total_passed, 'failed': total_failed,
            'status': 'completed' if total_failed == 0 else 'failed',
        })

        # 更新测试执行记录
        test_run.status = 'success' if total_failed == 0 else 'failed'
        test_run.passed = total_passed
        test_run.failed = total_failed
        test_run.duration = total_duration
        test_run.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        test_run.results = results

        # 生成测试报告
        report = TestReport(
            test_run_id=test_run.id,
            project_id=project_id,
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
                    'id': env_id, 'name': unified_env_name, 'mode': 'unified'
                } if use_unified_env else {
                    'mode': 'individual', 'description': '各用例使用自身配置的环境'
                },
                'results': results
            },
            status='generated'
        )

        db.session.add(report)
        test_run.report_id = report.id
        db.session.commit()

        return {
            'test_run_id': test_run.id,
            'report_id': report.id,
            'total': len(cases),
            'passed': total_passed,
            'failed': total_failed,
            'duration': round(total_duration, 2),
            'results': results
        }


    # ========== 内部辅助方法 ==========

    def _resolve_project_id(self, collection, env, cases, user_id):
        """确定 project_id"""
        project_id = collection.project_id
        if not project_id:
            if env:
                project_id = env.project_id
            if not project_id and cases:
                project_id = cases[0].project_id
                if not project_id and cases[0].environment_id:
                    case_env = db.session.get(Environment, cases[0].environment_id)
                    if case_env:
                        project_id = case_env.project_id
        if not project_id:
            user_project = Project.query.filter_by(owner_id=user_id).first()
            if user_project:
                project_id = user_project.id
        return project_id

    def _handle_mock_response(self, data, script_execution):
        """处理 Mock 响应"""
        mock_body = data.get('mock_response_body')
        if mock_body and isinstance(mock_body, str):
            try:
                mock_body = json.loads(mock_body)
            except Exception:
                pass

        mock_delay_ms = data.get('mock_delay_ms', 0)
        if mock_delay_ms and mock_delay_ms > 0:
            time.sleep(mock_delay_ms / 1000.0)

        return {
            'success': True,
            'status_code': data.get('mock_response_code', 200),
            'body': mock_body,
            'headers': data.get('mock_response_headers', {}),
            'response_time': mock_delay_ms,
            'script_execution': script_execution,
            'passed': True,
            'is_mock': True
        }

    def _handle_case_mock(self, case, script_execution):
        """处理用例级 Mock"""
        mock_body = case.mock_response_body
        if mock_body:
            try:
                mock_body = json.loads(mock_body)
            except Exception:
                pass

        if case.mock_delay_ms and case.mock_delay_ms > 0:
            time.sleep(case.mock_delay_ms / 1000.0)

        return {
            'success': True,
            'status_code': case.mock_response_code or 200,
            'body': mock_body,
            'headers': case.mock_response_headers or {},
            'response_time': case.mock_delay_ms or 0,
            'script_execution': script_execution,
            'passed': True,
            'is_mock': True
        }


    def _send_request(self, method, url, headers, params, body, body_type, timeout, script_execution, post_script='', env_vars=None, visual_assertions=None):
        """发送 HTTP 请求并处理响应"""
        start_time = time.time()

        try:
            request_kwargs = {
                'method': method, 'url': url, 'headers': headers,
                'params': params, 'timeout': timeout,
                'verify': False, 'allow_redirects': True
            }

            if body and method in ['POST', 'PUT', 'PATCH']:
                if body_type == 'json':
                    request_kwargs['json'] = body
                elif body_type == 'form':
                    request_kwargs['data'] = body
                else:
                    request_kwargs['data'] = body

            response = requests.request(**request_kwargs)
            elapsed_time = (time.time() - start_time) * 1000

            try:
                response_body = response.json()
            except (json.JSONDecodeError, ValueError):
                response_body = response.text

            response_size = len(response.content)
            if response_size > 1024 * 1024:
                size_str = f'{response_size / (1024 * 1024):.2f} MB'
            elif response_size > 1024:
                size_str = f'{response_size / 1024:.2f} KB'
            else:
                size_str = f'{response_size} B'

            # 后置断言执行
            if post_script and post_script.strip():
                try:
                    post_context = build_post_script_context(
                        environment_vars=env_vars or {},
                        response_data={
                            'status_code': response.status_code,
                            'headers': dict(response.headers),
                            'body': response_body,
                            'response_time': round(elapsed_time, 2),
                            'response_size': size_str
                        }
                    )
                    executor = get_executor(timeout=3)
                    post_result = executor.execute_post_script(post_script, post_context)
                    script_execution['post_script'] = post_result
                except Exception as e:
                    self.logger.error('后置断言执行异常', error=str(e))
                    script_execution['post_script'] = {
                        'executed': True, 'passed': False, 'error': str(e),
                        'assertions': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
                    }

            # ========== 可视化断言执行 ==========
            if visual_assertions:
                try:
                    evaluator = get_assertion_evaluator()
                    assertion_result = evaluator.evaluate(visual_assertions, {
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'body': response_body,
                        'response_time': round(elapsed_time, 2),
                    })
                    script_execution['visual_assertions'] = assertion_result
                except Exception as e:
                    self.logger.error('可视化断言执行异常', error=str(e))
                    script_execution['visual_assertions'] = {
                        'total': 0, 'passed': 0, 'failed': 0,
                        'details': [], 'error': str(e)
                    }

            return {
                'success': True,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'body': response_body,
                'response_time': round(elapsed_time, 2),
                'response_size': size_str,
                'cookies': dict(response.cookies),
                'script_execution': script_execution
            }

        except requests.exceptions.Timeout:
            elapsed_time = (time.time() - start_time) * 1000
            return {
                'success': False,
                'error': '请求超时',
                'response_time': round(elapsed_time, 2),
                'script_execution': script_execution
            }
        except requests.exceptions.ConnectionError as e:
            elapsed_time = (time.time() - start_time) * 1000
            return {
                'success': False,
                'error': f'连接错误: {str(e)}',
                'response_time': round(elapsed_time, 2),
                'script_execution': script_execution
            }
        except Exception as e:
            elapsed_time = (time.time() - start_time) * 1000
            return {
                'success': False,
                'error': str(e),
                'response_time': round(elapsed_time, 2),
                'script_execution': script_execution
            }


    def _execute_single_case_in_collection(self, case, use_unified_env, env_id, unified_env_name, unified_env_variables):
        """在集合执行中执行单个用例"""
        case_start_time = time.time()

        script_execution = {
            'pre_script': {'executed': False, 'passed': True},
            'post_script': {'executed': False, 'passed': True}
        }

        try:
            # Mock 处理
            if case.mock_enabled:
                case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
                case.last_status = 'passed'
                mock_result = {
                    'case_id': case.id, 'name': case.name, 'method': case.method, 'url': case.url,
                    'passed': True, 'status_code': case.mock_response_code or 200,
                    'response_time': case.mock_delay_ms or 0,
                    'response_body': case.mock_response_body, 'response_headers': case.mock_response_headers,
                    'response_cookies': {}, 'request_headers': case.headers,
                    'request_params': case.params, 'request_body': case.body,
                    'attachments': [], 'script_execution': script_execution,
                    'environment_id': env_id, 'environment_name': unified_env_name, 'is_mock': True
                }
                case.last_result = {
                    'success': True, 'status_code': case.mock_response_code or 200,
                    'body': case.mock_response_body, 'headers': case.mock_response_headers,
                    'response_time': case.mock_delay_ms or 0,
                    'script_execution': script_execution, 'passed': True, 'is_mock': True
                }
                db.session.commit()
                return {'result': mock_result, 'passed': True}

            url = case.url
            headers = case.headers or {}
            params = case.params or {}
            body = case.body

            effective_env_id = env_id if use_unified_env else case.environment_id
            effective_env_name = unified_env_name if use_unified_env else None
            effective_env_variables = dict(unified_env_variables) if use_unified_env else {}

            if not use_unified_env and case.environment_id:
                case_env = db.session.get(Environment, case.environment_id)
                if case_env:
                    effective_env_name = case_env.name
                    effective_env_variables = dict(case_env.variables or {})

            self.logger.info('执行用例', case_id=case.id, case_name=case.name, method=case.method, url=url, environment=effective_env_name or '无')

            # 前置脚本
            if case.pre_script and case.pre_script.strip():
                try:
                    pre_context = build_pre_script_context(
                        environment_vars=effective_env_variables,
                        request_data={'method': case.method, 'url': url, 'headers': headers, 'params': params, 'body': body}
                    )
                    executor = get_executor(timeout=3)
                    pre_result = executor.execute_pre_script(case.pre_script, pre_context)
                    script_execution['pre_script'] = pre_result

                    if not pre_result.get('passed', True):
                        elapsed_time = (time.time() - case_start_time) * 1000
                        case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
                        case.last_status = 'failed'
                        db.session.commit()
                        return {'result': {
                            'case_id': case.id, 'name': case.name, 'method': case.method, 'url': url,
                            'passed': False, 'status_code': None, 'response_time': round(elapsed_time, 2),
                            'script_execution': script_execution,
                            'error': pre_result.get('error', '前置脚本执行失败'),
                            'environment_id': effective_env_id, 'environment_name': effective_env_name
                        }, 'passed': False}

                    request_data = apply_pre_script_changes(
                        {'method': case.method, 'url': url, 'headers': headers, 'params': params, 'body': body}, pre_result
                    )
                    url = request_data['url']
                    headers = request_data['headers']
                    body = request_data['body']
                    effective_env_variables = apply_env_changes(effective_env_variables, pre_result)

                except Exception as e:
                    self.logger.error('前置脚本执行异常', error=str(e))
                    elapsed_time = (time.time() - case_start_time) * 1000
                    case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
                    case.last_status = 'failed'
                    db.session.commit()
                    script_execution['pre_script'] = {'executed': True, 'passed': False, 'error': str(e)}
                    return {'result': {
                        'case_id': case.id, 'name': case.name, 'method': case.method, 'url': url,
                        'passed': False, 'status_code': None, 'response_time': round(elapsed_time, 2),
                        'script_execution': script_execution,
                        'error': f'前置脚本执行异常: {str(e)}',
                        'environment_id': effective_env_id, 'environment_name': effective_env_name
                    }, 'passed': False}


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
                except Exception as e:
                    self.logger.error('环境变量替换失败', error=str(e))

            if effective_env_id:
                try:
                    headers = merge_headers_with_env(headers, effective_env_id, db)
                except Exception as e:
                    self.logger.error('合并请求头失败', error=str(e))

            # SSRF 防护：校验最终 URL
            safe, reason = is_safe_url(url)
            if not safe:
                elapsed_time = (time.time() - case_start_time) * 1000
                case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
                case.last_status = 'failed'
                db.session.commit()
                return {'result': {
                    'case_id': case.id, 'name': case.name, 'method': case.method, 'url': url,
                    'passed': False, 'status_code': None, 'response_time': round(elapsed_time, 2),
                    'script_execution': script_execution,
                    'error': reason,
                    'environment_id': effective_env_id, 'environment_name': effective_env_name
                }, 'passed': False}

            # 发送请求
            request_kwargs = {
                'method': case.method, 'url': url, 'headers': headers,
                'params': params, 'timeout': case.timeout or 30,
                'verify': False, 'allow_redirects': True
            }
            if body and case.method in ['POST', 'PUT', 'PATCH']:
                if case.body_type == 'json':
                    request_kwargs['json'] = body
                else:
                    request_kwargs['data'] = body

            response = requests.request(**request_kwargs)
            elapsed_time = (time.time() - case_start_time) * 1000

            try:
                response_body = response.json()
            except Exception:
                response_body = response.text


            # 后置断言
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
                    self.logger.error('后置断言执行异常', error=str(e))
                    script_execution['post_script'] = {
                        'executed': True, 'passed': False, 'error': str(e),
                        'assertions': {'total': 0, 'passed': 0, 'failed': 0, 'details': []}
                    }

            # ========== 可视化断言执行（集合执行） ==========
            if case.assertions:
                try:
                    evaluator = get_assertion_evaluator()
                    assertion_result = evaluator.evaluate(case.assertions, {
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'body': response_body,
                        'response_time': round(elapsed_time, 2),
                    })
                    script_execution['visual_assertions'] = assertion_result
                except Exception as e:
                    self.logger.error('可视化断言执行异常', error=str(e))
                    script_execution['visual_assertions'] = {
                        'total': 0, 'passed': 0, 'failed': 0,
                        'details': [], 'error': str(e)
                    }

            has_script = bool(case.pre_script or case.post_script or case.assertions)
            passed = calculate_case_passed(script_execution, response.status_code, has_script=has_script)

            response_body_preview = _safe_text(response_body, limit=2000)
            response_headers = dict(response.headers)
            response_cookies = dict(response.cookies)
            request_body_preview = _safe_text(body, limit=2000) if body else None

            attachments = [
                {'name': 'response_body', 'type': 'text', 'content': response_body_preview},
                {'name': 'response_headers', 'type': 'json', 'content': _safe_text(response_headers, limit=2000)}
            ]
            if request_body_preview:
                attachments.append({'name': 'request_body', 'type': 'text', 'content': request_body_preview})

            error_message = None
            if not passed:
                pre_script_error = script_execution.get('pre_script', {}).get('error')
                post_script_error = script_execution.get('post_script', {}).get('error')
                if pre_script_error:
                    error_message = f'前置脚本失败: {pre_script_error}'
                elif post_script_error:
                    error_message = f'后置断言失败: {post_script_error}'
                elif response.status_code >= 400:
                    error_message = f'HTTP {response.status_code}'
                    if isinstance(response_body, str) and response_body:
                        error_message = f'{error_message}: {response_body_preview}'

            case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
            case.last_status = 'passed' if passed else 'failed'

            if passed:
                self.logger.info('用例执行成功', case_name=case.name, status_code=response.status_code)
            else:
                self.logger.warning('用例执行失败', case_name=case.name)

            result = {
                'case_id': case.id, 'name': case.name, 'method': case.method, 'url': url,
                'passed': passed, 'status_code': response.status_code,
                'response_time': round(elapsed_time, 2),
                'response_body': response_body, 'response_headers': response_headers,
                'response_cookies': response_cookies,
                'request_headers': headers, 'request_params': params, 'request_body': body,
                'attachments': attachments, 'script_execution': script_execution,
                'error': error_message,
                'environment_id': effective_env_id, 'environment_name': effective_env_name
            }
            return {'result': result, 'passed': passed}

        except Exception as e:
            elapsed_time = (time.time() - case_start_time) * 1000
            self.logger.error('执行用例失败', case_id=case.id, case_name=case.name, error=str(e), exc_info=True)

            case.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
            case.last_status = 'failed'
            db.session.commit()

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
            attachments = [{'name': 'exception', 'type': 'text', 'content': error_preview}]
            if resp_body is not None:
                attachments.append({'name': 'response_body', 'type': 'text', 'content': _safe_text(resp_body, limit=2000)})

            result = {
                'case_id': case.id, 'name': case.name, 'method': case.method, 'url': case.url,
                'passed': False, 'status_code': resp_status,
                'response_time': round(elapsed_time, 2),
                'response_body': resp_body, 'response_headers': resp_headers,
                'response_cookies': resp_cookies,
                'request_headers': {}, 'request_params': {}, 'request_body': None,
                'attachments': attachments, 'script_execution': script_execution,
                'error': error_preview,
                'environment_id': None, 'environment_name': None
            }
            return {'result': result, 'passed': False}
