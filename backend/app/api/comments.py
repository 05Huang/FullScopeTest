"""
评论与讨论 API

提供评论的 CRUD、@提及、软删除功能。
"""
from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id
from ..services.comment_service import CommentService
from ..utils.exceptions import AppError
from ..core.logging import get_logger

logger = get_logger(__name__)
comment_service = CommentService()


@api_bp.route('/comments', methods=['POST'])
@jwt_required()
@validate_json('resource_type', 'resource_id', 'content')
def create_comment():
    """
    创建评论

    请求体:
        resource_type: 资源类型 (必填: test_case/test_run/test_plan)
        resource_id: 资源 ID (必填)
        content: 评论内容 (必填, Markdown 格式)
        parent_id: 父评论 ID (可选, 用于回复)
    """
    user_id = int(get_current_user_id())
    data = request.get_json()

    try:
        comment = comment_service.create_comment(
            user_id=user_id,
            resource_type=data['resource_type'],
            resource_id=data['resource_id'],
            content=data['content'],
            parent_id=data.get('parent_id'),
        )
        return success_response(data=comment, message='评论创建成功', code=201)
    except AppError as e:
        return error_response(e.code, e.message, errors=e.errors)


@api_bp.route('/comments/<string:resource_type>/<int:resource_id>', methods=['GET'])
@jwt_required()
def list_comments(resource_type, resource_id):
    """
    获取资源的评论列表

    查询参数:
        page: 页码 (默认 1)
        per_page: 每页数量 (默认 50)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    try:
        result = comment_service.get_comments(resource_type, resource_id, page, per_page)
        return success_response(data=result)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/comments/<int:comment_id>', methods=['GET'])
@jwt_required()
def get_comment(comment_id):
    """获取单条评论详情"""
    try:
        comment = comment_service.get_comment(comment_id)
        return success_response(data=comment)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
@validate_json('content')
def update_comment(comment_id):
    """
    编辑评论（仅作者或管理员）

    请求体:
        content: 新的评论内容 (必填)
    """
    user_id = int(get_current_user_id())
    data = request.get_json()

    try:
        comment = comment_service.update_comment(
            comment_id=comment_id,
            user_id=user_id,
            content=data['content'],
        )
        return success_response(data=comment, message='评论已更新')
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """软删除评论（仅作者或管理员）"""
    user_id = int(get_current_user_id())

    try:
        comment_service.delete_comment(comment_id, user_id)
        return success_response(message='评论已删除')
    except AppError as e:
        return error_response(e.code, e.message)