"""
Web 自动化测试模块 - API
实现基于 Playwright 的 Web 自动化测试功能
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db, celery
from ..models.web_test_script import WebTestScript
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
from ..tasks import run_web_test_task
import subprocess
import sys
from datetime import datetime


# 存储录制进程（录制功能仍使用进程方式）
recording_processes = {}


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
        target_url=data.get('target_url', ''),
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
        return error_response(message='脚本不存在', code=404)
    
    db.session.delete(script)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 执行脚本 ====================

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
        return error_response(message='脚本正在运行中')
    
    try:
        # 异步执行测试任务
        task = run_web_test_task.apply_async(
            args=[script_id, user_id],
            task_id=f'web_test_{script_id}_{user_id}'
        )
        
        return success_response(data={
            'message': '测试已提交，正在后台执行',
            'task_id': task.id,
            'script_id': script_id
        })
        
    except Exception as e:
        return error_response(message=f'提交失败: {str(e)}')


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
        if old_process.poll() is None:  # 进程还在运行
            return error_response(message='已有录制进程在运行，请先停止')
    
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
            return error_response(message='录制器启动失败，进程立即退出，请检查 Playwright 是否正确安装')
        
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


