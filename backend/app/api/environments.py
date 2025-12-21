"""
环境管理接口模块

提供测试环境的 CRUD 操作
"""

from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..extensions import db
from ..models.project import Project
from ..models.environment import Environment
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id


@api_bp.route('/environments', methods=['GET'])
@jwt_required()
def get_all_environments():
    """获取用户所有环境列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    
    # 获取用户所有项目
    user_projects = Project.query.filter_by(owner_id=user_id).all()
    project_ids = [p.id for p in user_projects]
    
    if not project_ids:
        return success_response(data=[])
    
    query = Environment.query.filter(Environment.project_id.in_(project_ids))
    
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    environments = query.all()
    
    return success_response(data=[e.to_dict() for e in environments])


@api_bp.route('/environments', methods=['POST'])
@jwt_required()
def create_global_environment():
    """创建环境（从全局入口）"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    if not data:
        return error_response(400, '请求数据不能为空')
    
    name = data.get('name', '').strip()
    base_url = data.get('base_url', '').strip()
    
    if not name:
        return error_response(400, '环境名称不能为空')
    
    # 获取project_id，如果没有提供则使用用户的第一个项目
    project_id = data.get('project_id')
    if not project_id:
        project = Project.query.filter_by(owner_id=user_id).first()
        if not project:
            # 自动创建默认项目
            project = Project(name='默认项目', owner_id=user_id)
            db.session.add(project)
            db.session.commit()
        project_id = project.id
    else:
        # 验证项目权限
        project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
        if not project:
            return error_response(404, '项目不存在')
    
    # 检查同名环境
    existing = Environment.query.filter_by(project_id=project_id, name=name).first()
    if existing:
        return error_response(400, '环境名称已存在')

    # 验证 variables 字段
    variables = data.get('variables', {})
    if isinstance(variables, dict):
        if len(variables) > 100:
            return error_response(400, f'环境变量不能超过100个，当前有{len(variables)}个')
    elif isinstance(variables, list):
        return error_response(400, 'variables 必须是对象类型（如 {"key": "value"}），不能是数组')
    else:
        variables = {}

    env = Environment(
        project_id=project_id,
        name=name,
        base_url=base_url,
        variables=variables,
        headers=data.get('headers', {}),
        is_default=data.get('is_active', False)
    )
    
    # 如果设为默认，取消其他环境的默认状态
    if env.is_default:
        Environment.query.filter_by(project_id=project_id, is_default=True).update({'is_default': False})
    
    db.session.add(env)
    db.session.commit()
    
    return success_response(
        data=env.to_dict(),
        message='创建成功',
        code=201
    )


@api_bp.route('/projects/<int:project_id>/environments', methods=['GET'])
@jwt_required()
def get_environments(project_id):
    """获取项目的环境列表"""
    user_id = get_current_user_id()
    
    # 验证项目权限
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return error_response(404, '项目不存在')
    
    environments = Environment.query.filter_by(project_id=project_id).all()
    
    return success_response(data=[e.to_dict() for e in environments])


@api_bp.route('/projects/<int:project_id>/environments', methods=['POST'])
@jwt_required()
@validate_json('name', 'base_url')
def create_environment(project_id):
    """创建环境"""
    user_id = get_current_user_id()
    
    # 验证项目权限
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return error_response(404, '项目不存在')
    
    data = request.get_json()
    
    name = data['name'].strip()
    base_url = data['base_url'].strip()
    
    # 检查同名环境
    existing = Environment.query.filter_by(project_id=project_id, name=name).first()
    if existing:
        return error_response(400, '环境名称已存在')
    
    # 验证 variables 字段
    variables = data.get('variables', {})
    if isinstance(variables, dict):
        if len(variables) > 100:
            return error_response(400, f'环境变量不能超过100个，当前有{len(variables)}个')
    elif isinstance(variables, list):
        return error_response(400, 'variables 必须是对象类型（如 {"key": "value"}），不能是数组')
    else:
        variables = {}

    env = Environment(
        project_id=project_id,
        name=name,
        base_url=base_url,
        variables=variables,
        headers=data.get('headers', {}),
        is_default=data.get('is_default', False)
    )
    
    # 如果设为默认，取消其他环境的默认状态
    if env.is_default:
        Environment.query.filter_by(project_id=project_id, is_default=True).update({'is_default': False})
    
    db.session.add(env)
    db.session.commit()
    
    return success_response(
        data=env.to_dict(),
        message='创建成功',
        code=201
    )


@api_bp.route('/environments/<int:env_id>', methods=['GET'])
@jwt_required()
def get_environment(env_id):
    """获取环境详情"""
    user_id = get_current_user_id()
    
    env = Environment.query.get(env_id)
    if not env:
        return error_response(404, '环境不存在')
    
    # 验证项目权限
    project = Project.query.filter_by(id=env.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权访问此环境')
    
    return success_response(data=env.to_dict())


@api_bp.route('/environments/<int:env_id>', methods=['PUT'])
@jwt_required()
def update_environment(env_id):
    """更新环境"""
    user_id = get_current_user_id()
    
    env = Environment.query.get(env_id)
    if not env:
        return error_response(404, '环境不存在')
    
    # 验证项目权限
    project = Project.query.filter_by(id=env.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权访问此环境')
    
    data = request.get_json()
    
    if 'name' in data:
        name = data['name'].strip()
        existing = Environment.query.filter(
            Environment.project_id == env.project_id,
            Environment.name == name,
            Environment.id != env_id
        ).first()
        if existing:
            return error_response(400, '环境名称已存在')
        env.name = name
    
    if 'base_url' in data:
        env.base_url = data['base_url'].strip()

    if 'variables' in data:
        variables = data['variables']
        # 验证 variables 类型
        if isinstance(variables, dict):
            # 限制变量数量
            if len(variables) > 100:
                return error_response(400, f'环境变量不能超过100个，当前有{len(variables)}个')
            env.variables = variables
        elif isinstance(variables, list):
            return error_response(400, 'variables 必须是对象类型（如 {"key": "value"}），不能是数组')
        else:
            return error_response(400, 'variables 格式不正确，必须是有效的 JSON 对象')
    
    if 'headers' in data:
        env.headers = data['headers']
    
    if 'is_default' in data and data['is_default']:
        Environment.query.filter(
            Environment.project_id == env.project_id,
            Environment.id != env_id,
            Environment.is_default == True
        ).update({'is_default': False})
        env.is_default = True
    
    db.session.commit()
    
    return success_response(
        data=env.to_dict(),
        message='更新成功'
    )


@api_bp.route('/environments/<int:env_id>', methods=['DELETE'])
@jwt_required()
def delete_environment(env_id):
    """删除环境"""
    user_id = get_current_user_id()
    
    env = Environment.query.get(env_id)
    if not env:
        return error_response(404, '环境不存在')
    
    # 验证项目权限
    project = Project.query.filter_by(id=env.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权访问此环境')
    
    db.session.delete(env)
    db.session.commit()
    
    return success_response(message='删除成功')


@api_bp.route('/environments/<int:env_id>/default', methods=['POST'])
@jwt_required()
def set_default_environment(env_id):
    """设置默认环境"""
    user_id = get_current_user_id()
    
    env = Environment.query.get(env_id)
    if not env:
        return error_response(404, '环境不存在')
    
    # 验证项目权限
    project = Project.query.filter_by(id=env.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权访问此环境')
    
    # 取消其他环境的默认状态
    Environment.query.filter(
        Environment.project_id == env.project_id,
        Environment.is_default == True
    ).update({'is_default': False})
    
    env.is_default = True
    db.session.commit()
    
    return success_response(message='设置成功')
