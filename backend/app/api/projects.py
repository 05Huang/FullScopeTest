"""
项目管理接口模块

提供项目的 CRUD 操作
"""

from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..extensions import db
from ..models.project import Project
from ..utils.response import success_response, error_response, paginate_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id
from ..utils.org_filter import get_org_id_for_create, filter_by_owner_or_org
from ..services.cache_service import get_cache_service, projects_key, PROJECTS_TTL


@api_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    """
    获取项目列表

    查询参数:
        page: 页码 (默认 1)
        per_page: 每页数量 (默认 20)
        keyword: 搜索关键词
    """
    user_id = get_current_user_id()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    keyword = request.args.get('keyword', '').strip()

    # 仅首页无搜索关键词时使用缓存
    cache = get_cache_service()
    if cache and page == 1 and not keyword:
        cached = cache.get(projects_key(user_id))
        if cached is not None:
            return success_response(data=cached)

    query = filter_by_owner_or_org(Project.query, Project, user_id)

    if keyword:
        query = query.filter(Project.name.ilike(f'%{keyword}%'))

    # 置顶项目排在最前，按置顶时间排序，然后按创建时间倒序
    pagination = query.order_by(
        Project.is_pinned.desc(),
        Project.pinned_at.desc().nullslast(),
        Project.created_at.desc(),
    ).paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = {
        'items': [p.to_dict() for p in pagination.items],
        'pagination': {
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
        }
    }

    # 写入缓存
    if cache and page == 1 and not keyword:
        cache.set(projects_key(user_id), result, ttl=PROJECTS_TTL)

    return paginate_response(
        items=result['items'],
        total=pagination.total,
        page=page,
        per_page=per_page
    )


@api_bp.route('/projects', methods=['POST'])
@jwt_required()
@validate_json('name')
def create_project():
    """
    创建项目

    请求体:
        name: 项目名称
        description: 项目描述 (可选)
    """
    user_id = get_current_user_id()
    org_id = get_org_id_for_create()
    data = request.get_json()

    name = data['name'].strip()
    description = data.get('description', '').strip()

    # 验证名称长度
    if len(name) < 1 or len(name) > 100:
        return error_response(400, '项目名称长度应为 1-100 个字符')

    # 检查同名项目
    existing = Project.query.filter_by(owner_id=user_id, name=name)
    if org_id:
        existing = existing.filter_by(organization_id=org_id)
    existing = existing.first()
    if existing:
        return error_response(400, '项目名称已存在')

    project = Project(
        name=name,
        description=description,
        owner_id=user_id,
        organization_id=org_id,
    )

    db.session.add(project)
    db.session.commit()

    # 失效项目列表缓存
    cache = get_cache_service()
    if cache:
        cache.delete(projects_key(user_id))

    return success_response(
        data=project.to_dict(),
        message='创建成功',
        code=201
    )


@api_bp.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """获取项目详情"""
    user_id = get_current_user_id()
    query = filter_by_owner_or_org(Project.query, Project, user_id)
    project = query.filter_by(id=project_id).first()

    if not project:
        return error_response(404, '项目不存在')

    return success_response(data=project.to_dict())


@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """更新项目"""
    user_id = get_current_user_id()
    query = filter_by_owner_or_org(Project.query, Project, user_id)
    project = query.filter_by(id=project_id).first()

    if not project:
        return error_response(404, '项目不存在')

    data = request.get_json()

    if 'name' in data:
        name = data['name'].strip()
        if len(name) < 1 or len(name) > 100:
            return error_response(400, '项目名称长度应为 1-100 个字符')

        # 检查同名项目
        existing = filter_by_owner_or_org(Project.query, Project, user_id)
        existing = existing.filter(Project.name == name, Project.id != project_id).first()
        if existing:
            return error_response(400, '项目名称已存在')

        project.name = name
    
    if 'description' in data:
        project.description = data['description'].strip()
    
    if 'settings' in data:
        project.settings = data['settings']
    
    db.session.commit()

    # 失效项目列表缓存
    cache = get_cache_service()
    if cache:
        cache.delete(projects_key(user_id))

    return success_response(
        data=project.to_dict(),
        message='更新成功'
    )


@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """删除项目"""
    user_id = get_current_user_id()
    query = filter_by_owner_or_org(Project.query, Project, user_id)
    project = query.filter_by(id=project_id).first()

    if not project:
        return error_response(404, '项目不存在')
    
    db.session.delete(project)
    db.session.commit()

    # 失效项目列表缓存
    cache = get_cache_service()
    if cache:
        cache.delete(projects_key(user_id))

    return success_response(message='删除成功')


@api_bp.route('/projects/<int:project_id>/pin', methods=['PUT'])
@jwt_required()
def toggle_pin_project(project_id):
    """置顶/取消置顶项目"""
    user_id = get_current_user_id()
    query = filter_by_owner_or_org(Project.query, Project, user_id)
    project = query.filter_by(id=project_id).first()

    if not project:
        return error_response(404, '项目不存在')

    project.is_pinned = not project.is_pinned
    project.pinned_at = datetime.utcnow() if project.is_pinned else None
    db.session.commit()

    # 失效项目列表缓存
    cache = get_cache_service()
    if cache:
        cache.delete(projects_key(user_id))

    action = '置顶' if project.is_pinned else '取消置顶'
    return success_response(data=project.to_dict(), message=f'{action}成功')
