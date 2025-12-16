"""
Web 自动化测试模块 - API
实现基于 Playwright 的 Web 自动化测试功能
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.web_test_script import WebTestScript
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
import subprocess
import tempfile
import os
import json
import threading
import time
from datetime import datetime


# 存储运行中的脚本进程
running_scripts = {}


@api_bp.route('/web-test/health', methods=['GET'])
def web_test_health():
    """Web 测试模块健康检查"""
    return success_response(message='Web 测试模块正常')


# ==================== 脚本管理 ====================

@api_bp.route('/web-test/scripts', methods=['GET'])
@jwt_required()
def get_scripts():
    """获取 Web 测试脚本列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    
    query = WebTestScript.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    
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
        
        # 截图
        page.screenshot(path="screenshot.png")
        
        # 关闭浏览器
        browser.close()
        
        return {"status": "success", "title": title}

if __name__ == "__main__":
    result = run()
    print(result)
'''
    
    script = WebTestScript(
        name=data['name'],
        description=data.get('description', ''),
        script_content=data.get('script_content', default_code),
        browser=data.get('browser', 'chromium'),
        headless=data.get('headless', True),
        timeout=data.get('timeout', 30000),
        project_id=data.get('project_id'),
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
        return error_response(message='脚本不存在', code=404)
    
    return success_response(data=script.to_dict())


@api_bp.route('/web-test/scripts/<int:script_id>', methods=['PUT'])
@jwt_required()
def update_script(script_id):
    """更新 Web 测试脚本"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(message='脚本不存在', code=404)
    
    data = request.get_json()
    
    for field in ['name', 'description', 'script_content', 'browser', 'headless', 'timeout']:
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
        return error_response(message='脚本不存在', code=404)
    
    db.session.delete(script)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 执行脚本 ====================

@api_bp.route('/web-test/scripts/<int:script_id>/run', methods=['POST'])
@jwt_required()
def run_script(script_id):
    """运行 Web 测试脚本"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(message='脚本不存在', code=404)
    
    # 检查是否已在运行
    run_key = f'{user_id}_{script_id}'
    if run_key in running_scripts:
        return error_response(message='脚本正在运行中')
    
    try:
        # 创建临时文件运行脚本
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script.script_code)
            temp_file = f.name
        
        # 更新状态
        script.status = 'running'
        script.last_run_at = datetime.utcnow()
        db.session.commit()
        
        # 运行脚本
        start_time = time.time()
        
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=script.timeout / 1000,  # 转换为秒
            cwd=tempfile.gettempdir()
        )
        
        elapsed_time = (time.time() - start_time) * 1000
        
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass
        
        # 更新状态
        success = result.returncode == 0
        script.status = 'completed' if success else 'failed'
        script.last_result = {
            'success': success,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'duration': round(elapsed_time, 2)
        }
        db.session.commit()
        
        return success_response(data={
            'success': success,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'duration': round(elapsed_time, 2)
        })
        
    except subprocess.TimeoutExpired:
        script.status = 'timeout'
        script.last_result = {'error': '执行超时'}
        db.session.commit()
        
        return success_response(data={
            'success': False,
            'error': '脚本执行超时'
        })
        
    except Exception as e:
        script.status = 'failed'
        script.last_result = {'error': str(e)}
        db.session.commit()
        
        return error_response(message=f'执行失败: {str(e)}')
    
    finally:
        if run_key in running_scripts:
            del running_scripts[run_key]


@api_bp.route('/web-test/execute', methods=['POST'])
@jwt_required()
def execute_web_code():
    """
    直接执行 Web 自动化代码（快速测试）
    
    不保存脚本，直接执行并返回结果
    """
    data = request.get_json()
    
    error = validate_required(data, ['code'])
    if error:
        return error_response(message=error)
    
    code = data['code']
    timeout = data.get('timeout', 30000) / 1000  # 转换为秒
    
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        start_time = time.time()
        
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir()
        )
        
        elapsed_time = (time.time() - start_time) * 1000
        
        # 清理
        try:
            os.unlink(temp_file)
        except:
            pass
        
        return success_response(data={
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'duration': round(elapsed_time, 2)
        })
        
    except subprocess.TimeoutExpired:
        return success_response(data={
            'success': False,
            'error': '执行超时'
        })
        
    except Exception as e:
        return error_response(message=f'执行失败: {str(e)}')


@api_bp.route('/web-test/scripts/<int:script_id>/stop', methods=['POST'])
@jwt_required()
def stop_script(script_id):
    """停止运行中的脚本"""
    user_id = get_current_user_id()
    run_key = f'{user_id}_{script_id}'
    
    if run_key not in running_scripts:
        return error_response(message='脚本未在运行')
    
    try:
        process = running_scripts[run_key]
        process.terminate()
        del running_scripts[run_key]
        
        script = WebTestScript.query.get(script_id)
        if script:
            script.status = 'stopped'
            db.session.commit()
        
        return success_response(message='已停止')
    except Exception as e:
        return error_response(message=f'停止失败: {str(e)}')


@api_bp.route('/web-test/scripts/<int:script_id>/status', methods=['GET'])
@jwt_required()
def get_script_status(script_id):
    """获取脚本运行状态"""
    user_id = get_current_user_id()
    script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
    
    if not script:
        return error_response(message='脚本不存在', code=404)
    
    run_key = f'{user_id}_{script_id}'
    is_running = run_key in running_scripts
    
    return success_response(data={
        'status': script.status,
        'is_running': is_running,
        'last_run_at': script.last_run_at.isoformat() if script.last_run_at else None,
        'last_result': script.last_result
    })


# ==================== 录制功能 ====================

@api_bp.route('/web-test/record/start', methods=['POST'])
@jwt_required()
def start_recording():
    """
    启动 Playwright 录制模式
    
    注意：这需要在本地环境运行，远程服务器可能不支持
    """
    data = request.get_json() or {}
    url = data.get('url', 'https://example.com')
    
    try:
        # 启动 codegen
        process = subprocess.Popen(
            ['python', '-m', 'playwright', 'codegen', url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return success_response(data={
            'message': '录制模式已启动',
            'pid': process.pid
        })
        
    except Exception as e:
        return error_response(message=f'启动录制失败: {str(e)}')


@api_bp.route('/web-test/browsers', methods=['GET'])
def get_supported_browsers():
    """获取支持的浏览器列表"""
    return success_response(data=[
        {'value': 'chromium', 'label': 'Chromium'},
        {'value': 'firefox', 'label': 'Firefox'},
        {'value': 'webkit', 'label': 'WebKit (Safari)'}
    ])


@api_bp.route('/web-test/templates', methods=['GET'])
def get_script_templates():
    """获取脚本模板列表"""
    templates = [
        {
            'name': '基础导航',
            'description': '简单的页面导航和截图',
            'code': '''from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        print(f"Title: {page.title()}")
        page.screenshot(path="screenshot.png")
        browser.close()

if __name__ == "__main__":
    run()
'''
        },
        {
            'name': '表单填写',
            'description': '自动填写表单并提交',
            'code': '''from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com/login")
        
        # 填写表单
        page.fill('input[name="username"]', 'testuser')
        page.fill('input[name="password"]', 'testpass')
        
        # 点击提交
        page.click('button[type="submit"]')
        
        # 等待导航
        page.wait_for_load_state('networkidle')
        
        print(f"登录后页面: {page.url}")
        browser.close()

if __name__ == "__main__":
    run()
'''
        },
        {
            'name': '元素断言',
            'description': '检查页面元素是否存在',
            'code': '''from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        
        # 断言元素可见
        expect(page.locator("h1")).to_be_visible()
        
        # 断言文本内容
        expect(page.locator("h1")).to_contain_text("Example")
        
        print("所有断言通过!")
        browser.close()

if __name__ == "__main__":
    run()
'''
        }
    ]
    
    return success_response(data=templates)
