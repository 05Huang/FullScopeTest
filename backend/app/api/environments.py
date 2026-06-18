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
from ..utils.org_filter import filter_by_org_projects, filter_by_owner_or_org
from ..utils import get_current_user_id
from ..services.cache_service import get_cache_service, environments_key, ENVIRONMENTS_TTL


@api_bp.route('/environments', methods=['GET'])
@jwt_required()
def get_all_environments():
    """获取用户所有环境列表"""
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)

    # 检查缓存（仅无 project_id 过滤时）
    cache = get_cache_service()
    if cache and not project_id:
        cached = cache.get(environments_key(user_id))
        if cached is not None:
            return success_response(data=cached)

    # 获取用户所有项目（组织隔离）
    user_projects = filter_by_owner_or_org(Project.query, Project, user_id).all()
    project_ids = [p.id for p in user_projects]

    if not project_ids:
        return success_response(data=[])

    query = Environment.query.filter(Environment.project_id.in_(project_ids))

    if project_id:
        query = query.filter_by(project_id=project_id)

    environments = query.all()
    result = [e.to_dict() for e in environments]

    # 写入缓存
    if cache and not project_id:
        cache.set(environments_key(user_id), result, ttl=ENVIRONMENTS_TTL)

    return success_response(data=result)


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
            project = Project(name='默认项目', owner_id=user_id, settings={})
            db.session.add(project)
            db.session.commit()
        project_id = project.id
    else:
        # 验证项目权限（组织隔离）
        query = filter_by_owner_or_org(Project.query, Project, user_id)
        project = query.filter_by(id=project_id).first()
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
        is_default=data.get('is_default', False)
    )
    
    # 如果设为默认，取消其他环境的默认状态
    if env.is_default:
        Environment.query.filter_by(project_id=project_id, is_default=True).update({'is_default': False})
    
    db.session.add(env)
    db.session.commit()

    # 失效环境列表缓存
    cache = get_cache_service()
    if cache:
        cache.invalidate_pattern(f"envs:user:{user_id}")

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

    # 失效环境列表缓存
    cache = get_cache_service()
    if cache:
        cache.invalidate_pattern(f"envs:user:{user_id}")

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

    # 失效环境列表缓存
    cache = get_cache_service()
    if cache:
        cache.invalidate_pattern(f"envs:user:{user_id}")

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

    # 失效环境列表缓存
    cache = get_cache_service()
    if cache:
        cache.invalidate_pattern(f"envs:user:{user_id}")

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


@api_bp.route('/environments/<int:env_id>/export', methods=['GET'])
@jwt_required()
def export_environment(env_id):
    """导出环境变量为 JSON"""
    user_id = get_current_user_id()

    env = Environment.query.get(env_id)
    if not env:
        return error_response(404, '环境不存在')

    project = Project.query.filter_by(id=env.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权访问此环境')

    export_data = {
        'version': '1.0',
        'export_time': datetime.utcnow().isoformat(),
        'environment': {
            'name': env.name,
            'base_url': env.base_url,
            'variables': env.variables or {},
            'headers': env.headers or {},
            'description': env.description,
        }
    }

    return success_response(data=export_data)


@api_bp.route('/projects/<int:project_id>/environments/import', methods=['POST'])
@jwt_required()
def import_environment(project_id):
    """
    导入环境变量

    请求体:
        data: 导出的 JSON 数据
        mode: 'override'（覆盖）或 'merge'（合并）

    支持两种格式：
    1. 导出的 JSON 格式
    2. .env 文件格式（KEY=VALUE）
    """
    user_id = get_current_user_id()

    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权访问此项目')

    data = request.get_json()
    import_data = data.get('data')
    mode = data.get('mode', 'merge')

    if not import_data:
        return error_response(400, '缺少导入数据')

    try:
        # 解析导入数据
        if isinstance(import_data, str):
            # .env 格式
            variables = {}
            for line in import_data.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    variables[key.strip()] = value.strip().strip('"\'')

            env_name = f'导入的环境 {datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
            env = Environment(
                name=env_name,
                project_id=project_id,
                user_id=user_id,
                variables=variables,
            )
            db.session.add(env)
        elif isinstance(import_data, dict):
            # JSON 格式
            env_info = import_data.get('environment', import_data)
            env_name = env_info.get('name', f'导入的环境 {datetime.utcnow().strftime("%Y%m%d%H%M%S")}')

            # 查找同名环境
            existing = Environment.query.filter_by(
                project_id=project_id,
                name=env_name,
                user_id=user_id,
            ).first()

            if existing and mode == 'override':
                existing.variables = env_info.get('variables', {})
                existing.headers = env_info.get('headers', {})
                existing.base_url = env_info.get('base_url', existing.base_url)
                existing.description = env_info.get('description', existing.description)
                env = existing
            elif existing and mode == 'merge':
                existing_vars = existing.variables or {}
                new_vars = env_info.get('variables', {})
                existing_vars.update(new_vars)
                existing.variables = existing_vars
                env = existing
            else:
                env = Environment(
                    name=env_name,
                    project_id=project_id,
                    user_id=user_id,
                    base_url=env_info.get('base_url', ''),
                    variables=env_info.get('variables', {}),
                    headers=env_info.get('headers', {}),
                    description=env_info.get('description', ''),
                )
                db.session.add(env)
        else:
            return error_response(400, '不支持的数据格式')

        db.session.commit()

        return success_response(
            data=env.to_dict(),
            message=f'导入成功（{mode}模式）'
        )
    except Exception as e:
        return error_response(400, f'导入失败: {str(e)}')
