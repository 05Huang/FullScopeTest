"""
APP 测试接口模块

提供 APP 测试脚本和用例集的 CRUD 操作及执行功能
"""

from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..extensions import db
from ..models.app_test_script import AppTestScript
from ..models.app_test_collection import AppTestCollection
from ..utils.response import success_response, error_response, paginate_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id


# ==================== 健康检查 ====================

@api_bp.route('/app-test/health', methods=['GET'])
def app_test_health():
    """APP 测试模块健康检查"""
    return success_response(data={'status': 'ok'}, message='APP 测试模块正常')


# ==================== 用例集管理 ====================

@api_bp.route('/app-test/collections', methods=['GET'])
@jwt_required()
def get_app_collections():
    """获取用例集列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)

    query = AppTestCollection.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)

    collections = query.order_by(AppTestCollection.sort_order, AppTestCollection.created_at.desc()).all()
    return success_response(data=[c.to_dict() for c in collections])


@api_bp.route('/app-test/collections', methods=['POST'])
@jwt_required()
@validate_json('name')
def create_app_collection():
    """创建用例集"""
    user_id = get_current_user_id()
    data = request.get_json()

    collection = AppTestCollection(
        name=data['name'],
        description=data.get('description', ''),
        project_id=data.get('project_id'),
        user_id=user_id,
    )
    db.session.add(collection)
    db.session.commit()

    return success_response(data=collection.to_dict(), message='创建成功', code=201)


@api_bp.route('/app-test/collections/<int:collection_id>', methods=['PUT'])
@jwt_required()
def update_app_collection(collection_id):
    """更新用例集"""
    user_id = get_current_user_id()
    collection = AppTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()

    if not collection:
        return error_response(404, '用例集不存在')

    data = request.get_json()
    if 'name' in data:
        collection.name = data['name']
    if 'description' in data:
        collection.description = data['description']
    if 'sort_order' in data:
        collection.sort_order = data['sort_order']

    db.session.commit()
    return success_response(data=collection.to_dict(), message='更新成功')


@api_bp.route('/app-test/collections/<int:collection_id>', methods=['DELETE'])
@jwt_required()
def delete_app_collection(collection_id):
    """删除用例集"""
    user_id = get_current_user_id()
    collection = AppTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()

    if not collection:
        return error_response(404, '用例集不存在')

    db.session.delete(collection)
    db.session.commit()
    return success_response(message='删除成功')


# ==================== 脚本管理 ====================

@api_bp.route('/app-test/scripts', methods=['GET'])
@jwt_required()
def get_app_scripts():
    """获取脚本列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    collection_id = request.args.get('collection_id', type=int)

    query = AppTestScript.query.filter_by(user_id=user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    if collection_id:
        query = query.filter_by(collection_id=collection_id)

    scripts = query.order_by(AppTestScript.sort_order, AppTestScript.created_at.desc()).all()
    return success_response(data=[s.to_dict() for s in scripts])


@api_bp.route('/app-test/scripts', methods=['POST'])
@jwt_required()
@validate_json('name')
def create_app_script():
    """创建脚本"""
    user_id = get_current_user_id()
    data = request.get_json()

    script = AppTestScript(
        name=data['name'],
        description=data.get('description', ''),
        project_id=data.get('project_id'),
        collection_id=data.get('collection_id'),
        platform=data.get('platform', 'android'),
        app_path=data.get('app_path'),
        app_package=data.get('app_package'),
        app_activity=data.get('app_activity'),
        bundle_id=data.get('bundle_id'),
        device_name=data.get('device_name'),
        platform_version=data.get('platform_version'),
        automation_name=data.get('automation_name', 'UiAutomator2'),
        appium_server=data.get('appium_server', 'http://localhost:4723'),
        script_content=data.get('script_content', ''),
        user_id=user_id,
    )
    db.session.add(script)
    db.session.commit()

    return success_response(data=script.to_dict(), message='创建成功', code=201)


@api_bp.route('/app-test/scripts/<int:script_id>', methods=['GET'])
@jwt_required()
def get_app_script(script_id):
    """获取单个脚本"""
    user_id = get_current_user_id()
    script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()

    if not script:
        return error_response(404, '脚本不存在')

    return success_response(data=script.to_dict())


@api_bp.route('/app-test/scripts/<int:script_id>', methods=['PUT'])
@jwt_required()
def update_app_script(script_id):
    """更新脚本"""
    user_id = get_current_user_id()
    script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()

    if not script:
        return error_response(404, '脚本不存在')

    data = request.get_json()
    updatable_fields = [
        'name', 'description', 'collection_id', 'platform', 'app_path',
        'app_package', 'app_activity', 'bundle_id', 'device_name',
        'platform_version', 'automation_name', 'appium_server',
        'script_content', 'is_enabled', 'sort_order'
    ]

    for field in updatable_fields:
        if field in data:
            setattr(script, field, data[field])

    db.session.commit()
    return success_response(data=script.to_dict(), message='更新成功')


@api_bp.route('/app-test/scripts/<int:script_id>', methods=['DELETE'])
@jwt_required()
def delete_app_script(script_id):
    """删除脚本"""
    user_id = get_current_user_id()
    script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()

    if not script:
        return error_response(404, '脚本不存在')

    db.session.delete(script)
    db.session.commit()
    return success_response(message='删除成功')


# ==================== 执行测试 ====================

@api_bp.route('/app-test/scripts/<int:script_id>/run', methods=['POST'])
@jwt_required()
def run_app_script(script_id):
    """执行单个脚本"""
    from flask import current_app

    user_id = get_current_user_id()
    script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()

    if not script:
        return error_response(404, '脚本不存在')

    if script.status == 'running':
        return error_response(400, '脚本正在执行中')

    # 检查 Celery 是否启用
    if current_app.config.get('CELERY_ENABLE', False):
        from ..tasks import run_app_test_task
        task = run_app_test_task.apply_async(args=[script_id, user_id])
        return success_response(
            data={'script_id': script.id, 'task_id': task.id, 'status': 'running'},
            message='脚本已提交执行'
        )
    else:
        # Celery 未启用时，同步执行
        script.status = 'running'
        script.last_run_at = datetime.utcnow()
        db.session.commit()

        try:
            import subprocess
            import sys
            import tempfile
            import os

            work_dir = os.path.join(os.path.dirname(current_app.root_path), 'data', 'app_tests', str(script_id))
            os.makedirs(work_dir, exist_ok=True)

            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8', dir=work_dir) as f:
                f.write(script.script_content)
                temp_file = f.name

            try:
                start_time = __import__('time').time()
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=work_dir,
                )
                duration = __import__('time').time() - start_time
                success = result.returncode == 0

                script.status = 'passed' if success else 'failed'
                script.last_result = {
                    'success': success,
                    'duration': duration,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'return_code': result.returncode,
                    'timestamp': datetime.utcnow().isoformat(),
                }
                db.session.commit()

                return success_response(
                    data={'script_id': script.id, 'status': script.status, 'result': script.last_result},
                    message='脚本执行完成'
                )
            finally:
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass

        except Exception as e:
            script.status = 'failed'
            script.last_result = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
            }
            db.session.commit()
            return error_response(500, f'执行失败: {str(e)}')
