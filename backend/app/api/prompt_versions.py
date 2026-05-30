"""
Prompt 版本管理 API

提供 Prompt 版本的 CRUD、A/B 测试选择、统计刷新接口。
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..utils.response import success_response, error_response, paginate_response
from ..utils import get_current_user_id
from ..services.ai.prompt_version_service import prompt_version_service


@api_bp.route('/ai/prompt-versions', methods=['GET'])
@jwt_required()
def list_prompt_versions():
    """
    获取 Prompt 版本列表

    查询参数:
        feature: 按功能模块过滤（copilot / script_gen / swagger_gen / dedup）
        is_active: 按激活状态过滤（true / false）
        page: 页码（默认 1）
        per_page: 每页数量（默认 20）
    """
    feature = request.args.get('feature', '').strip() or None
    is_active_str = request.args.get('is_active', '').strip().lower()
    is_active = None
    if is_active_str == 'true':
        is_active = True
    elif is_active_str == 'false':
        is_active = False

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = prompt_version_service.list_versions(
        feature=feature,
        is_active=is_active,
        page=page,
        per_page=per_page,
    )

    return paginate_response(
        items=result['items'],
        total=result['total'],
        page=result['page'],
        per_page=result['per_page'],
    )


@api_bp.route('/ai/prompt-versions', methods=['POST'])
@jwt_required()
def create_prompt_version():
    """
    创建新的 Prompt 版本

    请求体:
        feature: 功能模块（必填）
        name: 版本名称（必填）
        system_prompt: 系统提示词（必填）
        user_prompt_template: 用户提示词模板（可选）
        temperature: 温度参数（默认 0.3）
        model_name: 指定模型（可选，为空使用全局默认）
        is_active: 是否激活（默认 false）
        traffic_weight: 流量权重（0.0-1.0，默认 1.0）
        change_notes: 变更说明（可选）
    """
    data = request.get_json() or {}

    feature = (data.get('feature') or '').strip()
    name = (data.get('name') or '').strip()
    system_prompt = (data.get('system_prompt') or '').strip()

    if not feature:
        return error_response(400, 'feature is required')
    if not name:
        return error_response(400, 'name is required')
    if not system_prompt:
        return error_response(400, 'system_prompt is required')

    # 验证 feature 合法值
    valid_features = {
        'copilot', 'script_gen', 'script_gen_web', 'script_gen_perf',
        'swagger_gen', 'dedup',
    }
    if feature not in valid_features:
        return error_response(400, f'feature must be one of: {", ".join(sorted(valid_features))}')

    user_id = get_current_user_id()

    pv = prompt_version_service.create_version(
        feature=feature,
        name=name,
        system_prompt=system_prompt,
        user_prompt_template=data.get('user_prompt_template'),
        temperature=float(data.get('temperature', 0.3)),
        model_name=data.get('model_name'),
        is_active=bool(data.get('is_active', False)),
        traffic_weight=float(data.get('traffic_weight', 1.0)),
        change_notes=data.get('change_notes'),
        created_by=user_id,
    )

    return success_response(data=pv.to_dict(), message='Prompt 版本创建成功', code=201)


@api_bp.route('/ai/prompt-versions/<int:version_id>', methods=['GET'])
@jwt_required()
def get_prompt_version(version_id):
    """获取单个 Prompt 版本详情"""
    pv = prompt_version_service.get_by_id(version_id)
    if not pv:
        return error_response(404, 'Prompt 版本不存在')
    return success_response(data=pv.to_dict())


@api_bp.route('/ai/prompt-versions/<int:version_id>', methods=['PUT'])
@jwt_required()
def update_prompt_version(version_id):
    """
    更新 Prompt 版本

    请求体（所有字段可选）:
        name, system_prompt, user_prompt_template, temperature,
        model_name, is_active, traffic_weight, change_notes
    """
    data = request.get_json() or {}

    pv = prompt_version_service.update_version(
        version_id,
        name=data.get('name'),
        system_prompt=data.get('system_prompt'),
        user_prompt_template=data.get('user_prompt_template'),
        temperature=data.get('temperature'),
        model_name=data.get('model_name'),
        is_active=data.get('is_active'),
        traffic_weight=data.get('traffic_weight'),
        change_notes=data.get('change_notes'),
    )

    if not pv:
        return error_response(404, 'Prompt 版本不存在')

    return success_response(data=pv.to_dict(), message='Prompt 版本更新成功')


@api_bp.route('/ai/prompt-versions/<int:version_id>', methods=['DELETE'])
@jwt_required()
def deactivate_prompt_version(version_id):
    """停用（软删除）Prompt 版本"""
    ok = prompt_version_service.deactivate_version(version_id)
    if not ok:
        return error_response(404, 'Prompt 版本不存在')
    return success_response(message='Prompt 版本已停用')


@api_bp.route('/ai/prompt-versions/select', methods=['POST'])
@jwt_required()
def select_prompt_version():
    """
    基于 A/B 测试流量权重选择一个激活的 Prompt 版本

    请求体:
        feature: 功能模块（必填）
    """
    data = request.get_json() or {}
    feature = (data.get('feature') or '').strip()

    if not feature:
        return error_response(400, 'feature is required')

    pv = prompt_version_service.select_version_for_ab_test(feature)
    if not pv:
        return error_response(404, f'没有找到 feature={feature} 的激活版本')

    return success_response(data=pv.to_dict())


@api_bp.route('/ai/prompt-versions/refresh-stats', methods=['POST'])
@jwt_required()
def refresh_prompt_version_stats():
    """
    刷新 Prompt 版本的统计数据（从 AIInvocationLog 重新聚合）

    查询参数:
        feature: 可选，只刷新指定 feature 的版本
    """
    feature = request.args.get('feature', '').strip() or None

    count = prompt_version_service.refresh_all_stats(feature=feature)

    return success_response(
        data={'refreshed_count': count},
        message=f'已刷新 {count} 个 Prompt 版本的统计数据',
    )
