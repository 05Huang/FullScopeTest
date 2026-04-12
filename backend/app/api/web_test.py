"""
Web 自动化测试模块 - API
实现基于 Playwright 的 Web 自动化测试功能
"""

from flask import request, current_app, send_from_directory, Response, stream_with_context
import os
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db, celery
from ..models.web_test_collection import WebTestCollection
from ..models.web_test_script import WebTestScript
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
from ..tasks import run_web_test_task
from ..utils.ai_script_generator import generate_test_script
from ..utils.ai_script_healer import analyze_test_error
from ..utils.ai_web_explorer import run_exploration_task
import requests
import subprocess
import sys
import time
import json
import threading
from queue import Queue, Empty
from datetime import datetime
from urllib.parse import quote_plus
import uuid


# 存储录制进程（录制功能仍使用进程方式）
recording_processes = {}
live_view_sessions = {}


def _build_runtime_ai_config(data: dict) -> dict:
    runtime_config = {
        'AI_ASSISTANT_ENABLED': current_app.config.get('AI_ASSISTANT_ENABLED', True),
        'AI_ASSISTANT_BASE_URL': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
        'AI_ASSISTANT_API_KEY': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
        'AI_ASSISTANT_MODEL': current_app.config.get('AI_ASSISTANT_MODEL', ''),
        'AI_VISION_BASE_URL': current_app.config.get('AI_VISION_BASE_URL', ''),
        'AI_VISION_API_KEY': current_app.config.get('AI_VISION_API_KEY', ''),
        'AI_VISION_MODEL': current_app.config.get('AI_VISION_MODEL', ''),
        'AI_EXPLORE_BROWSER_HEADLESS': current_app.config.get('AI_EXPLORE_BROWSER_HEADLESS', 'true'),
        'AI_EXPLORE_BROWSER_SLOW_MO': current_app.config.get('AI_EXPLORE_BROWSER_SLOW_MO', 0),
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
    if 'explore_browser_headless' in data:
        runtime_config['AI_EXPLORE_BROWSER_HEADLESS'] = data.get('explore_browser_headless')
    if data.get('explore_browser_slow_mo') is not None:
        runtime_config['AI_EXPLORE_BROWSER_SLOW_MO'] = int(data.get('explore_browser_slow_mo'))

    return runtime_config


def _format_sse(event: str, payload: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"


def _resolve_live_view_url(data: dict, start_url: str) -> str:
    direct_url = str(data.get('live_view_url') or '').strip()
    if direct_url.startswith('http://') or direct_url.startswith('https://'):
        return direct_url
    template = str(
        data.get('live_view_url_template')
        or current_app.config.get('AI_EXPLORE_LIVE_VIEW_URL_TEMPLATE')
        or ''
    ).strip()
    if not template:
        return ''
    return (
        template
        .replace('{start_url}', quote_plus(start_url))
        .replace('{start_url_raw}', start_url)
    )


def _build_internal_live_view_url(start_url: str, session_id: str) -> str:
    template = str(current_app.config.get('AI_EXPLORE_LIVE_VIEW_INTERNAL_URL_TEMPLATE') or '').strip()
    if not template:
        return ''
    return (
        template
        .replace('{session_id}', quote_plus(session_id))
        .replace('{session_id_raw}', session_id)
        .replace('{start_url}', quote_plus(start_url))
        .replace('{start_url_raw}', start_url)
    )


def _allocate_internal_live_view_session(start_url: str, objective: str, max_steps: int, user_id: int) -> dict:
    session_id = str(uuid.uuid4())
    url = _build_internal_live_view_url(start_url, session_id)
    if not url:
        return {}
    live_view_sessions[session_id] = {
        'session_id': session_id,
        'user_id': user_id,
        'start_url': start_url,
        'objective': objective,
        'max_steps': max_steps,
        'created_at': time.time(),
    }
    return {
        'url': url,
        'source': 'internal',
        'session_id': session_id,
    }


def _allocate_live_view_session(data: dict, start_url: str, objective: str, max_steps: int, user_id: int) -> dict:
    direct_url = str(data.get('live_view_url') or '').strip()
    if direct_url.startswith('http://') or direct_url.startswith('https://'):
        return {'url': direct_url, 'source': 'manual'}
    allocator_url = str(
        data.get('live_view_allocator_url')
        or current_app.config.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_URL')
        or ''
    ).strip()
    if not allocator_url:
        internal_session = _allocate_internal_live_view_session(start_url, objective, max_steps, user_id)
        if internal_session:
            return internal_session
        fallback_url = _resolve_live_view_url(data, start_url)
        return {'url': fallback_url, 'source': 'template'} if fallback_url else {}
    allocator_token = str(
        data.get('live_view_allocator_token')
        or current_app.config.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TOKEN')
        or ''
    ).strip()
    timeout_seconds = int(
        data.get('live_view_allocator_timeout')
        or current_app.config.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TIMEOUT')
        or 15
    )
    headers = {'Content-Type': 'application/json'}
    if allocator_token:
        headers['Authorization'] = f'Bearer {allocator_token}'
    payload = {
        'start_url': start_url,
        'objective': objective,
        'max_steps': max_steps,
        'user_id': user_id,
        'requested_by': 'fullscopetest-web-explorer',
    }
    try:
        response = requests.post(
            allocator_url,
            json=payload,
            headers=headers,
            timeout=timeout_seconds,
        )
        if response.status_code >= 400:
            raise RuntimeError(f'allocator http {response.status_code}')
        body = response.json() if response.text else {}
        url = str(body.get('url') or body.get('live_view_url') or '').strip()
        if not url:
            raise RuntimeError('allocator missing url')
        return {
            'url': url,
            'source': str(body.get('source') or 'allocator'),
            'session_id': body.get('session_id'),
            'release_url': body.get('release_url'),
        }
    except Exception as exc:
        current_app.logger.warning('allocate live view session failed: %s', str(exc))
        fallback_url = _resolve_live_view_url(data, start_url)
        return {'url': fallback_url, 'source': 'template'} if fallback_url else {}


def _release_live_view_session(session: dict):
    if not isinstance(session, dict):
        return
    session_id = str(session.get('session_id') or '').strip()
    if session_id and session_id in live_view_sessions:
        live_view_sessions.pop(session_id, None)
    release_url = str(session.get('release_url') or '').strip()
    if not release_url and session_id:
        release_template = str(
            current_app.config.get('AI_EXPLORE_LIVE_VIEW_RELEASE_URL')
            or ''
        ).strip()
        if release_template:
            release_url = release_template.replace('{session_id}', quote_plus(session_id)).replace('{session_id_raw}', session_id)
    if not release_url:
        return
    timeout_seconds = int(current_app.config.get('AI_EXPLORE_LIVE_VIEW_RELEASE_TIMEOUT') or 6)
    try:
        response = requests.delete(release_url, timeout=timeout_seconds)
        if response.status_code >= 400:
            requests.post(release_url, timeout=timeout_seconds)
    except Exception as exc:
        current_app.logger.warning('release live view session failed: %s', str(exc))


def _get_collection_or_404(collection_id: int, user_id: int):
    collection = WebTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    if not collection:
        return None, error_response(message='用例集不存在', code=404)
    return collection, None


@api_bp.route('/web-test/health', methods=['GET'])
def web_test_health():
    """Web 测试模块健康检查"""
    return success_response(message='Web 测试模块正常')


@api_bp.route('/web-test/ai/generate', methods=['POST'])
@jwt_required()
def generate_web_script():
    """AI 生成 Web 测试脚本"""
    data = request.get_json() or {}
    prompt = (data.get('prompt') or '').strip()
    
    if not prompt:
        return error_response(400, 'prompt is required')
        
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

        # Frontend runtime override
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

        script_content = generate_test_script(prompt, "web", runtime_config)
        return success_response(data={'script_content': script_content}, message='AI 脚本生成成功')
    except Exception as exc:
        return error_response(500, f'AI 脚本生成失败: {str(exc)}')


@api_bp.route('/web-test/ai/analyze-error', methods=['POST'])
@jwt_required()
def analyze_web_test_error():
    """AI 智能诊断测试错误并提供修复建议"""
    data = request.get_json() or {}
    script_id = data.get('script_id')
    error_log = data.get('error_log')
    
    if not script_id or not error_log:
        return error_response(400, 'script_id and error_log are required')
        
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    if not script:
        return error_response(404, '脚本不存在')
        
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

        # Frontend runtime override
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

        result = analyze_test_error(
            script_content=script.script_content,
            error_log=error_log,
            test_type="web",
            config=runtime_config
        )
        return success_response(data=result, message='AI 诊断完成')
    except Exception as exc:
        return error_response(500, f'AI 诊断失败: {str(exc)}')


@api_bp.route('/web-test/ai/explore', methods=['POST'])
@jwt_required()
def explore_web_app():
    """AI 探索性测试 (Autonomous Web Explorer)"""
    data = request.get_json() or {}
    start_url = data.get('start_url')
    objective = data.get('objective', '尽可能多地点击不同页面并寻找报错')
    max_steps = int(data.get('max_steps', 10))
    
    if not start_url:
        return error_response(400, 'start_url is required')
        
    try:
        runtime_config = _build_runtime_ai_config(data)

        report = run_exploration_task(start_url, max_steps, objective, runtime_config)
        
        return success_response(data=report, message='AI 探索测试完成')
    except Exception as exc:
        return error_response(500, f'AI 探索测试失败: {str(exc)}')


@api_bp.route('/web-test/ai/explore/stream', methods=['POST'])
@jwt_required()
def explore_web_app_stream():
    data = request.get_json() or {}
    user_id = get_current_user_id()
    start_url = data.get('start_url')
    objective = data.get('objective', '尽可能多地点击不同页面并寻找报错')
    max_steps = int(data.get('max_steps', 10))

    if not start_url:
        return error_response(400, 'start_url is required')

    runtime_config = _build_runtime_ai_config(data)
    live_view_session = _allocate_live_view_session(data, start_url, objective, max_steps, user_id)

    def generate():
        log_queue: Queue = Queue()
        progress_queue: Queue = Queue()
        state = {'report': None, 'error': None}
        done_event = threading.Event()

        def push_log(line: str):
            log_queue.put(line)

        def push_progress(payload: dict):
            progress_queue.put(payload)

        def worker():
            try:
                state['report'] = run_exploration_task(
                    start_url=start_url,
                    max_steps=max_steps,
                    objective=objective,
                    config=runtime_config,
                    log_callback=push_log,
                    progress_callback=push_progress,
                )
            except Exception as exc:
                state['error'] = str(exc)
            finally:
                done_event.set()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

        if live_view_session.get('url'):
            yield _format_sse('live_view', {
                'url': live_view_session.get('url'),
                'source': live_view_session.get('source') or 'allocator',
                'session_id': live_view_session.get('session_id'),
            })
        yield _format_sse('log', {'line': f'探索任务已创建，目标 URL: {start_url}'})
        yield _format_sse('log', {'line': f'探索目标: {objective}'})
        yield _format_sse('log', {'line': f'最大步数: {max_steps}'})

        while not done_event.is_set() or not log_queue.empty() or not progress_queue.empty():
            try:
                line = log_queue.get(timeout=0.2)
                yield _format_sse('log', {'line': str(line)})
            except Empty:
                pass
            try:
                progress_payload = progress_queue.get_nowait()
                if isinstance(progress_payload, dict):
                    yield _format_sse('progress', progress_payload)
            except Empty:
                pass

        try:
            if state['error']:
                yield _format_sse('error', {'message': state['error']})
            else:
                yield _format_sse('report', state['report'] or {})
            yield _format_sse('done', {'ok': state['error'] is None})
        finally:
            _release_live_view_session(live_view_session)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )

# ==================== 用例集管理 ====================

@api_bp.route('/web-test/collections', methods=['GET'])
@jwt_required()
def get_web_collections():
    """获取 Web 用例集列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)

    query = WebTestCollection.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)

    collections = query.order_by(WebTestCollection.created_at.desc()).all()
    return success_response(data=[c.to_dict() for c in collections])


@api_bp.route('/web-test/collections', methods=['POST'])
@jwt_required()
def create_web_collection():
    """创建 Web 用例集"""
    user_id = get_current_user_id()
    data = request.get_json() or {}

    error = validate_required(data, ['name'])
    if error:
        return error_response(400, error)

    collection = WebTestCollection(
        name=data['name'],
        description=data.get('description', ''),
        project_id=data.get('project_id'),
        sort_order=data.get('sort_order', 0),
        user_id=user_id,
    )
    db.session.add(collection)
    db.session.commit()

    return success_response(data=collection.to_dict(), message='创建成功')


@api_bp.route('/web-test/collections/<int:collection_id>', methods=['PUT'])
@jwt_required()
def update_web_collection(collection_id):
    """更新 Web 用例集"""
    user_id = get_current_user_id()
    collection, err = _get_collection_or_404(collection_id, user_id)
    if err:
        return err

    data = request.get_json() or {}
    for field in ['name', 'description', 'sort_order']:
        if field in data:
            setattr(collection, field, data[field])

    db.session.commit()
    return success_response(data=collection.to_dict(), message='更新成功')


@api_bp.route('/web-test/collections/<int:collection_id>', methods=['DELETE'])
@jwt_required()
def delete_web_collection(collection_id):
    """删除 Web 用例集"""
    user_id = get_current_user_id()
    collection, err = _get_collection_or_404(collection_id, user_id)
    if err:
        return err

    WebTestScript.query.filter_by(collection_id=collection.id, user_id=user_id).update(
        {'collection_id': None},
        synchronize_session=False
    )
    db.session.delete(collection)
    db.session.commit()
    return success_response(message='删除成功')


@api_bp.route('/web-test/collections/<int:collection_id>/run', methods=['POST'])
@jwt_required()
def run_web_collection(collection_id):
    """批量运行用例集内脚本（逐脚本异步提交）"""
    user_id = get_current_user_id()
    collection, err = _get_collection_or_404(collection_id, user_id)
    if err:
        return err

    scripts = WebTestScript.query.filter_by(
        user_id=user_id,
        collection_id=collection.id,
        is_enabled=True
    ).all()
    if not scripts:
        return error_response(message='用例集内没有可执行脚本')

    submitted = []
    skipped = []

    for script in scripts:
        if script.status == 'running':
            skipped.append({'script_id': script.id, 'reason': 'running'})
            continue
        try:
            task = run_web_test_task.apply_async(
                args=[script.id, user_id],
                task_id=f'web_test_{script.id}_{user_id}'
            )
            script.status = 'running'
            script.last_status = 'running'
            script.last_run_at = datetime.utcnow()
            submitted.append({'script_id': script.id, 'task_id': task.id})
        except Exception as exc:
            skipped.append({'script_id': script.id, 'reason': str(exc)})

    db.session.commit()

    return success_response(data={
        'collection_id': collection.id,
        'collection_name': collection.name,
        'submitted_count': len(submitted),
        'submitted': submitted,
        'skipped': skipped,
    }, message='批量提交完成')


# ==================== 脚本管理 ====================

@api_bp.route('/web-test/scripts', methods=['GET'])
@jwt_required()
def get_scripts():
    """获取 Web 测试脚本列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    collection_id = request.args.get('collection_id', type=int)
    
    query = WebTestScript.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    if collection_id is not None:
        query = query.filter_by(collection_id=collection_id)
    
    scripts = query.order_by(WebTestScript.created_at.desc()).all()
    
    return success_response(data=[s.to_dict() for s in scripts])


@api_bp.route('/web-test/scripts', methods=['POST'])
@jwt_required()
def create_script():
    """创建 Web 测试脚本"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    error = validate_required(data, ['name'])
    if error:
        return error_response(message=error)
    
    # 默认的 Playwright 脚本模板
    default_code = '''"""
Playwright 自动化测试脚本
"""
from playwright.sync_api import sync_playwright, expect
from fst_vision import assert_snapshot  # 导入视觉回归测试断言

def run():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 访问页面
        page.goto("https://example.com")
        
        # 获取标题
        title = page.title()
        print(f"页面标题: {title}")
        
        # 视觉回归测试 (第一次运行会生成基线图片，后续运行会进行像素级对比)
        assert_snapshot(page, "example_homepage", mismatch_tolerance=0.01)
        
        # 关闭浏览器
        browser.close()
        
        return {"status": "success", "title": title}

if __name__ == "__main__":
    result = run()
    print(result)
'''
    
    project_id = data.get('project_id')
    collection_id = data.get('collection_id')
    if collection_id is not None:
        collection, err = _get_collection_or_404(collection_id, user_id)
        if err:
            return err
        if collection.project_id and project_id and collection.project_id != project_id:
            return error_response(400, 'collection_id 与 project_id 不匹配')
        if project_id is None:
            project_id = collection.project_id
    else:
        collection = None

    script = WebTestScript(
        name=data['name'],
        description=data.get('description', ''),
        script_content=data.get('script_content', default_code),
        target_url=data.get('target_url', ''),
        browser=data.get('browser', 'chromium'),
        headless=data.get('headless', True),
        timeout=data.get('timeout', 30000),
        collection_id=collection.id if collection else None,
        project_id=project_id,
        user_id=user_id
    )
    
    db.session.add(script)
    db.session.commit()
    
    return success_response(data=script.to_dict(), message='创建成功')


@api_bp.route('/web-test/scripts/<int:script_id>', methods=['GET'])
@jwt_required()
def get_script(script_id):
    """获取脚本详情"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(404, '脚本不存在')
    
    return success_response(data=script.to_dict())


@api_bp.route('/web-test/scripts/<int:script_id>', methods=['PUT'])
@jwt_required()
def update_script(script_id):
    """更新 Web 测试脚本"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(404, '脚本不存在')
    
    data = request.get_json()

    if 'collection_id' in data:
        collection_id = data.get('collection_id')
        if collection_id is None:
            script.collection_id = None
        else:
            collection, err = _get_collection_or_404(collection_id, user_id)
            if err:
                return err
                if script.project_id and collection.project_id and script.project_id != collection.project_id:
                    return error_response(400, 'collection_id 与脚本项目不匹配')
            script.collection_id = collection.id
            if script.project_id is None:
                script.project_id = collection.project_id
    
    for field in ['name', 'description', 'script_content', 'target_url', 'browser', 'headless', 'timeout']:
        if field in data:
            setattr(script, field, data[field])
    
    db.session.commit()
    
    return success_response(data=script.to_dict(), message='更新成功')


@api_bp.route('/web-test/scripts/<int:script_id>', methods=['DELETE'])
@jwt_required()
def delete_script(script_id):
    """删除 Web 测试脚本"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(404, '脚本不存在')
    
    db.session.delete(script)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 执行脚本 ====================

@api_bp.route('/web-test/scripts/<int:script_id>/snapshots/<image_type>/<snapshot_name>', methods=['GET'])
@jwt_required()
def get_snapshot_image(script_id, image_type, snapshot_name):
    """
    获取视觉回归测试截图 (baseline, actual, diff)
    """
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(404, '脚本不存在')
        
    if image_type not in ['baseline', 'actual', 'diff']:
        return error_response(400, '无效的图片类型')
        
    if not snapshot_name.endswith('.png'):
        snapshot_name += '.png'
        
    work_dir = os.path.join(os.path.dirname(current_app.root_path), 'data', 'web_tests', str(script_id))
    image_dir = os.path.join(work_dir, 'snapshots', image_type)
    
    if not os.path.exists(os.path.join(image_dir, snapshot_name)):
        return error_response(404, '图片不存在')
        
    return send_from_directory(image_dir, snapshot_name)

@api_bp.route('/web-test/scripts/<int:script_id>/run', methods=['POST'])
@jwt_required()
def run_script(script_id):
    """运行 Web 测试脚本（异步）"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(message='脚本不存在', code=404)
    
    # 检查是否已在运行
    if script.status == 'running':
        return error_response(400, '脚本正在运行中')
    
    try:
        # 异步执行测试任务
        task = run_web_test_task.apply_async(
            args=[script_id, user_id],
            task_id=f'web_test_{script_id}_{user_id}'
        )

        # 提交成功后立即更新为 running，前端可及时感知状态
        script.status = 'running'
        script.last_status = 'running'
        script.last_run_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(data={
            'message': '测试已提交，正在后台执行',
            'task_id': task.id,
            'script_id': script_id
        })
        
    except Exception as e:
        return error_response(500, f'提交失败: {str(e)}')


@api_bp.route('/web-test/record/start', methods=['POST'])
@jwt_required()
def start_recording():
    """
    启动 Playwright 录制模式
    
    注意：这需要在本地环境运行，远程服务器可能不支持
    """
    user_id = get_current_user_id()
    data = request.get_json() or {}
    url = data.get('url', 'https://example.com')
    browser = data.get('browser', 'chromium')
    
    # 检查是否已有录制进程在运行
    if user_id in recording_processes:
        old_process = recording_processes[user_id]
        if old_process.poll() is None:
            return error_response(400, '已有录制进程在运行，请先停止')
    
    try:
        # 获取当前 Python 解释器路径（支持虚拟环境）
        python_path = sys.executable
        
        # 构建命令
        cmd = [python_path, '-m', 'playwright', 'codegen']
        
        # 添加浏览器参数
        if browser != 'chromium':
            cmd.extend(['--browser', browser])
        
        # 添加目标 URL
        cmd.append(url)
        
        # 启动 codegen（不使用 PIPE，避免缓冲区问题导致进程退出）
        # 使用 DEVNULL 忽略输出，或者不捕获输出让其显示在控制台
        if sys.platform == 'win32':
            # Windows: 创建新的控制台窗口，不捕获输出
            process = subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                # 不使用 PIPE，让输出显示在新控制台
                stdout=None,
                stderr=None
            )
        else:
            # Linux/Mac: 使用 DEVNULL 或不捕获
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # 等待一小段时间确认进程启动成功
        time.sleep(1)
        if process.poll() is not None:
            return error_response(500, '录制器启动失败，进程立即退出，请检查 Playwright 是否正确安装')
        
        # 保存进程
        recording_processes[user_id] = process
        
        return success_response(data={
            'message': '录制器已启动，请在打开的浏览器窗口中进行操作',
            'pid': process.pid,
            'browser': browser,
            'url': url
        })
        
    except FileNotFoundError:
        return error_response(message='Playwright 未安装，请先运行: pip install playwright && playwright install')
    except Exception as e:
        return error_response(message=f'启动录制失败: {str(e)}')


@api_bp.route('/web-test/record/stop', methods=['POST'])
@jwt_required()
def stop_recording():
    """
    停止 Playwright 录制
    """
    user_id = get_current_user_id()
    
    if user_id not in recording_processes:
        return error_response(message='没有正在运行的录制进程')
    
    process = recording_processes[user_id]
    
    try:
        # 终止进程
        process.terminate()
        process.wait(timeout=5)
        
        # 清理
        del recording_processes[user_id]
        
        return success_response(message='录制已停止')
        
    except Exception as e:
        return error_response(message=f'停止录制失败: {str(e)}')


@api_bp.route('/web-test/record/status', methods=['GET'])
@jwt_required()
def recording_status():
    """
    获取录制状态
    """
    user_id = get_current_user_id()
    
    if user_id not in recording_processes:
        return success_response(data={
            'is_recording': False,
            'python_path': sys.executable
        })
    
    process = recording_processes[user_id]
    is_running = process.poll() is None
    
    if not is_running:
        # 进程已结束，获取退出码
        exit_code = process.returncode
        # 清理
        del recording_processes[user_id]
        
        return success_response(data={
            'is_recording': False,
            'exit_code': exit_code,
            'message': f'进程已退出，退出码: {exit_code}',
            'python_path': sys.executable
        })
    
    return success_response(data={
        'is_recording': is_running,
        'pid': process.pid,
        'python_path': sys.executable
    })
