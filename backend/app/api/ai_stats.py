"""
AI 能力统计 API

提供 AI 功能的统计数据，用于前端看板展示。
"""

from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy import func, case
from . import api_bp
from ..extensions import db
from ..models.ai_invocation_log import AIInvocationLog
from ..models.prompt_version import PromptVersion
from ..utils.response import success_response, error_response
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/ai/stats/overview', methods=['GET'])
@jwt_required()
def get_ai_stats_overview():
    """
    获取 AI 功能概览统计

    返回:
        total_invocations: 总调用次数
        success_rate: 成功率 (%)
        total_tokens: 总 token 消耗
        total_cost: 总成本估算
        avg_latency_ms: 平均延迟
        features: 各功能模块的调用量分布
    """
    # 总调用次数
    total = db.session.query(func.count(AIInvocationLog.id)).scalar() or 0

    # 成功次数
    success_count = db.session.query(
        func.count(AIInvocationLog.id)
    ).filter(AIInvocationLog.success == True).scalar() or 0

    # 成功率
    success_rate = round(success_count / total * 100, 2) if total > 0 else 0.0

    # 总 token 消耗
    total_tokens = db.session.query(
        func.coalesce(func.sum(AIInvocationLog.total_tokens), 0)
    ).scalar() or 0

    # 总成本
    total_cost = db.session.query(
        func.coalesce(func.sum(AIInvocationLog.cost_estimate), 0.0)
    ).scalar() or 0.0

    # 平均延迟
    avg_latency = db.session.query(
        func.coalesce(func.avg(AIInvocationLog.latency_ms), 0)
    ).scalar() or 0

    # 各功能模块调用量
    feature_rows = db.session.query(
        AIInvocationLog.feature,
        func.count(AIInvocationLog.id)
    ).group_by(AIInvocationLog.feature).all()

    features = {row[0]: row[1] for row in feature_rows}

    return success_response(data={
        'total_invocations': total,
        'success_rate': success_rate,
        'total_tokens': int(total_tokens),
        'total_cost': round(float(total_cost), 4),
        'avg_latency_ms': round(float(avg_latency), 1),
        'features': features,
    })


@api_bp.route('/ai/stats/success-rate-trend', methods=['GET'])
@jwt_required()
def get_success_rate_trend():
    """
    获取 AI 调用成功率趋势

    查询参数:
        days: 天数（默认 30）
        feature: 可选，按功能模块过滤

    返回:
        按天聚合的成功率趋势数据
    """
    days = request.args.get('days', 30, type=int)
    feature = request.args.get('feature', '').strip()

    since = datetime.utcnow() - timedelta(days=days)

    query = db.session.query(
        func.date(AIInvocationLog.created_at).label('date'),
        func.count(AIInvocationLog.id).label('total'),
        func.sum(case((AIInvocationLog.success == True, 1), else_=0)).label('success'),
    ).filter(AIInvocationLog.created_at >= since)

    if feature:
        query = query.filter(AIInvocationLog.feature == feature)

    query = query.group_by(func.date(AIInvocationLog.created_at)).order_by(
        func.date(AIInvocationLog.created_at)
    )

    rows = query.all()

    trend = []
    for row in rows:
        total = row.total or 0
        success = row.success or 0
        trend.append({
            'date': str(row.date),
            'total': total,
            'success': success,
            'success_rate': round(success / total * 100, 2) if total > 0 else 0.0,
        })

    return success_response(data=trend)


@api_bp.route('/ai/stats/latency-trend', methods=['GET'])
@jwt_required()
def get_latency_trend():
    """
    获取平均响应时间趋势

    查询参数:
        days: 天数（默认 30）
        feature: 可选，按功能模块过滤

    返回:
        按天聚合的平均延迟趋势数据
    """
    days = request.args.get('days', 30, type=int)
    feature = request.args.get('feature', '').strip()

    since = datetime.utcnow() - timedelta(days=days)

    query = db.session.query(
        func.date(AIInvocationLog.created_at).label('date'),
        func.avg(AIInvocationLog.latency_ms).label('avg_latency'),
        func.avg(AIInvocationLog.total_tokens).label('avg_tokens'),
    ).filter(AIInvocationLog.created_at >= since)

    if feature:
        query = query.filter(AIInvocationLog.feature == feature)

    query = query.group_by(func.date(AIInvocationLog.created_at)).order_by(
        func.date(AIInvocationLog.created_at)
    )

    rows = query.all()

    trend = []
    for row in rows:
        trend.append({
            'date': str(row.date),
            'avg_latency_ms': round(float(row.avg_latency or 0), 1),
            'avg_tokens': round(float(row.avg_tokens or 0), 1),
        })

    return success_response(data=trend)


@api_bp.route('/ai/stats/token-consumption', methods=['GET'])
@jwt_required()
def get_token_consumption():
    """
    获取 token 消耗统计

    查询参数:
        days: 天数（默认 30）

    返回:
        按天聚合的 token 消耗数据
    """
    days = request.args.get('days', 30, type=int)

    since = datetime.utcnow() - timedelta(days=days)

    query = db.session.query(
        func.date(AIInvocationLog.created_at).label('date'),
        func.coalesce(func.sum(AIInvocationLog.prompt_tokens), 0).label('prompt_tokens'),
        func.coalesce(func.sum(AIInvocationLog.completion_tokens), 0).label('completion_tokens'),
        func.coalesce(func.sum(AIInvocationLog.total_tokens), 0).label('total_tokens'),
        func.coalesce(func.sum(AIInvocationLog.cost_estimate), 0.0).label('cost'),
    ).filter(
        AIInvocationLog.created_at >= since
    ).group_by(
        func.date(AIInvocationLog.created_at)
    ).order_by(
        func.date(AIInvocationLog.created_at)
    )

    rows = query.all()

    data = []
    for row in rows:
        data.append({
            'date': str(row.date),
            'prompt_tokens': int(row.prompt_tokens),
            'completion_tokens': int(row.completion_tokens),
            'total_tokens': int(row.total_tokens),
            'cost': round(float(row.cost), 4),
        })

    return success_response(data=data)


@api_bp.route('/ai/stats/prompt-versions-comparison', methods=['GET'])
@jwt_required()
def get_prompt_versions_comparison():
    """
    获取 Prompt 版本效果对比

    查询参数:
        feature: 可选，按功能模块过滤

    返回:
        各 Prompt 版本的统计数据对比
    """
    feature = request.args.get('feature', '').strip()

    query = PromptVersion.query
    if feature:
        query = query.filter_by(feature=feature)

    versions = query.order_by(
        PromptVersion.feature, PromptVersion.version.desc()
    ).all()

    data = []
    for pv in versions:
        success_rate = 0.0
        if pv.total_invocations > 0:
            success_rate = round(pv.success_count / pv.total_invocations * 100, 2)

        data.append({
            'id': pv.id,
            'feature': pv.feature,
            'name': pv.name,
            'version': pv.version,
            'is_active': pv.is_active,
            'total_invocations': pv.total_invocations,
            'success_count': pv.success_count,
            'failure_count': pv.failure_count,
            'success_rate': success_rate,
            'avg_latency_ms': round(pv.avg_latency_ms, 1) if pv.avg_latency_ms else 0,
            'avg_tokens': round(pv.avg_tokens, 1) if pv.avg_tokens else 0,
            'avg_cost': round(pv.avg_cost, 4) if pv.avg_cost else 0,
        })

    return success_response(data=data)
