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
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '').strip()
    
    query = Project.query.filter_by(owner_id=user_id)
    
    if keyword:
        query = query.filter(Project.name.ilike(f'%{keyword}%'))
    
    pagination = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(
        items=[p.to_dict() for p in pagination.items],
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
    data = request.get_json()
    
    name = data['name'].strip()
    description = data.get('description', '').strip()
    
    # 验证名称长度
    if len(name) < 1 or len(name) > 100:
        return error_response(400, '项目名称长度应为 1-100 个字符')
    
    # 检查同名项目
    existing = Project.query.filter_by(owner_id=user_id, name=name).first()
    if existing:
        return error_response(400, '项目名称已存在')
    
    project = Project(
        name=name,
        description=description,
        owner_id=user_id
    )
    
    db.session.add(project)
    db.session.commit()
    
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
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    
    if not project:
        return error_response(404, '项目不存在')
    
    return success_response(data=project.to_dict())


@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """更新项目"""
    user_id = get_current_user_id()
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    
    if not project:
        return error_response(404, '项目不存在')
    
    data = request.get_json()
    
    if 'name' in data:
        name = data['name'].strip()
        if len(name) < 1 or len(name) > 100:
            return error_response(400, '项目名称长度应为 1-100 个字符')
        
        # 检查同名项目
        existing = Project.query.filter(
            Project.owner_id == user_id,
            Project.name == name,
            Project.id != project_id
        ).first()
        if existing:
            return error_response(400, '项目名称已存在')
        
        project.name = name
    
    if 'description' in data:
        project.description = data['description'].strip()
    
    if 'settings' in data:
        project.settings = data['settings']
    
    db.session.commit()
    
    return success_response(
        data=project.to_dict(),
        message='更新成功'
    )


@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """删除项目"""
    user_id = get_current_user_id()
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    
    if not project:
        return error_response(404, '项目不存在')
    
    db.session.delete(project)
    db.session.commit()
    
    return success_response(message='删除成功')
