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
    user_id = get_current_user_id()
    script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()

    if not script:
        return error_response(404, '脚本不存在')

    if script.status == 'running':
        return error_response(400, '脚本正在执行中')

    # TODO: 接入 Celery 异步任务执行 Appium 脚本
    # 暂时返回成功，标记为 running
    script.status = 'running'
    db.session.commit()

    return success_response(
        data={'script_id': script.id, 'status': 'running'},
        message='脚本已提交执行'
    )
