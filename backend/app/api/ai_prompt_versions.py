"""
AI Prompt 版本管理 API

提供 PromptVersion 的 CRUD 接口和统计查询。
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.prompt_version import PromptVersion
from ..models.ai_invocation_log import AIInvocationLog
from ..utils.response import success_response, error_response, paginate_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/ai/prompt-versions', methods=['GET'])
@jwt_required()
def list_prompt_versions():
    """
    获取 Prompt 版本列表

    查询参数:
        feature: 按功能模块过滤（script_gen_web/script_gen_perf/copilot 等）
        is_active: 按激活状态过滤（true/false）
        page: 页码（默认 1）
        per_page: 每页数量（默认 20）
    """
    feature = request.args.get('feature', '').strip()
    is_active_str = request.args.get('is_active', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = PromptVersion.query

    if feature:
        query = query.filter_by(feature=feature)
    if is_active_str.lower() in ('true', 'false'):
        query = query.filter_by(is_active=is_active_str.lower() == 'true')

    query = query.order_by(PromptVersion.feature, PromptVersion.version.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return paginate_response(
        items=[pv.to_dict() for pv in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page,
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
        traffic_weight: 流量权重（默认 1.0）
        is_active: 是否激活（默认 False）
        change_notes: 变更说明（可选）
    """
    data = request.get_json() or {}
    user_id = get_current_user_id()

    feature = (data.get('feature') or '').strip()
    name = (data.get('name') or '').strip()
    system_prompt = (data.get('system_prompt') or '').strip()

    if not feature:
        return error_response(400, 'feature is required')
    if not name:
        return error_response(400, 'name is required')
    if not system_prompt:
        return error_response(400, 'system_prompt is required')

    # 计算新版本号
    latest = PromptVersion.query.filter_by(feature=feature).order_by(
        PromptVersion.version.desc()
    ).first()
    new_version = (latest.version + 1) if latest else 1

    pv = PromptVersion(
        feature=feature,
        name=name,
        version=new_version,
        is_active=data.get('is_active', False),
        system_prompt=system_prompt,
        user_prompt_template=data.get('user_prompt_template'),
        temperature=data.get('temperature', 0.3),
        model_name=data.get('model_name'),
        traffic_weight=data.get('traffic_weight', 1.0),
        change_notes=data.get('change_notes'),
        created_by=user_id,
    )

    db.session.add(pv)
    db.session.commit()

    logger.info('PromptVersion created', id=pv.id, feature=feature, version=new_version)
    return success_response(data=pv.to_dict(), message='Prompt 版本创建成功')


@api_bp.route('/ai/prompt-versions/<int:version_id>', methods=['GET'])
@jwt_required()
def get_prompt_version(version_id):
    """获取 Prompt 版本详情"""
    pv = PromptVersion.query.get(version_id)
    if not pv:
        return error_response(404, 'Prompt 版本不存在')

    return success_response(data=pv.to_dict())


@api_bp.route('/ai/prompt-versions/<int:version_id>', methods=['PUT'])
@jwt_required()
def update_prompt_version(version_id):
    """
    更新 Prompt 版本

    可更新字段: name, system_prompt, user_prompt_template, temperature,
    model_name, is_active, traffic_weight, change_notes
    """
    pv = PromptVersion.query.get(version_id)
    if not pv:
        return error_response(404, 'Prompt 版本不存在')

    data = request.get_json() or {}

    updatable_fields = [
        'name', 'system_prompt', 'user_prompt_template', 'temperature',
        'model_name', 'is_active', 'traffic_weight', 'change_notes',
    ]

    for field in updatable_fields:
        if field in data:
            setattr(pv, field, data[field])

    db.session.commit()

    logger.info('PromptVersion updated', id=pv.id, feature=pv.feature)
    return success_response(data=pv.to_dict(), message='Prompt 版本更新成功')


@api_bp.route('/ai/prompt-versions/<int:version_id>', methods=['DELETE'])
@jwt_required()
def deactivate_prompt_version(version_id):
    """
    停用 Prompt 版本（软删除）

    将 is_active 设为 False，记录停用时间。
    不会物理删除数据，保留历史记录。
    """
    from datetime import datetime

    pv = PromptVersion.query.get(version_id)
    if not pv:
        return error_response(404, 'Prompt 版本不存在')

    pv.is_active = False
    pv.deactivated_at = datetime.utcnow()
    db.session.commit()

    logger.info('PromptVersion deactivated', id=pv.id, feature=pv.feature)
    return success_response(message='Prompt 版本已停用')


@api_bp.route('/ai/prompt-versions/<int:version_id>/stats', methods=['GET'])
@jwt_required()
def get_prompt_version_stats(version_id):
    """
    获取 Prompt 版本的详细统计

    包含：
    - 基本信息和聚合统计
    - 最近 N 次调用的成功率趋势
    - 平均延迟和 token 消耗
    """
    pv = PromptVersion.query.get(version_id)
    if not pv:
        return error_response(404, 'Prompt 版本不存在')

    # 获取最近 30 条调用日志用于趋势分析
    recent_logs = AIInvocationLog.query.filter_by(
        prompt_version_id=version_id
    ).order_by(AIInvocationLog.created_at.desc()).limit(30).all()

    trend = []
    for log in reversed(recent_logs):
        trend.append({
            'created_at': log.created_at.isoformat() if log.created_at else None,
            'success': log.success,
            'latency_ms': log.latency_ms,
            'total_tokens': log.total_tokens,
            'cost_estimate': log.cost_estimate,
        })

    stats = pv.to_dict()
    stats['recent_trend'] = trend

    return success_response(data=stats)
