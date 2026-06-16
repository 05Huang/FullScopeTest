"""
质量趋势分析服务

按周/月聚合测试通过率趋势，支持按测试类型分组统计。
用于 Dashboard 展示历史趋势图表。

返回格式：
    [{"date": "2026-01-01", "api": 95.5, "web": 88.2, "perf": 92.0}]
"""
from datetime import datetime, timedelta
from sqlalchemy import func, case, and_
from ..extensions import db
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)

# 测试类型列表
TEST_TYPES = ['api', 'web', 'performance']


def get_pass_rate_trend(
    project_id: int = None,
    days: int = 30,
    granularity: str = 'week',
) -> list:
    """
    获取通过率趋势

    Args:
        project_id: 项目 ID（None 表示全组织）
        days: 时间范围（天数，7/30/90）
        granularity: 聚合粒度（day/week/month）

    Returns:
        [{date, api, web, perf, total_runs, total_passed, total_failed}]
    """
    since = datetime.utcnow() - timedelta(days=days)

    # 基础查询：已完成的执行记录
    query = TestRun.query.filter(
        TestRun.created_at >= since,
        TestRun.status.in_(['success', 'failed']),
    )
    if project_id:
        query = query.filter_by(project_id=project_id)

    runs = query.order_by(TestRun.created_at.asc()).all()

    if not runs:
        return []

    # 按时间分桶
    buckets = {}
    for run in runs:
        bucket_key = _get_bucket_key(run.created_at, granularity)
        if bucket_key not in buckets:
            buckets[bucket_key] = {tt: {'total': 0, 'passed': 0} for tt in TEST_TYPES}
            buckets[bucket_key]['_meta'] = {'total': 0, 'passed': 0, 'failed': 0}

        tt = run.test_type
        if tt in buckets[bucket_key]:
            buckets[bucket_key][tt]['total'] += run.total_cases or 0
            buckets[bucket_key][tt]['passed'] += run.passed or 0

        buckets[bucket_key]['_meta']['total'] += 1
        if run.status == 'success':
            buckets[bucket_key]['_meta']['passed'] += 1
        else:
            buckets[bucket_key]['_meta']['failed'] += 1

    # 构建结果
    result = []
    for date_key in sorted(buckets.keys()):
        bucket = buckets[date_key]
        item = {'date': date_key}
        for tt in TEST_TYPES:
            total = bucket[tt]['total']
            passed = bucket[tt]['passed']
            item[tt] = round(passed / total * 100, 1) if total > 0 else None
        item['total_runs'] = bucket['_meta']['total']
        item['total_passed'] = bucket['_meta']['passed']
        item['total_failed'] = bucket['_meta']['failed']
        result.append(item)

    return result


def get_dashboard_stats(project_id: int = None, days: int = 30) -> dict:
    """
    获取 Dashboard 统计数据

    Args:
        project_id: 项目 ID
        days: 统计范围

    Returns:
        {period_days, total_runs, pass_rate, by_type: {api: {...}, ...}, daily: [...]}
    """
    since = datetime.utcnow() - timedelta(days=days)

    query = TestRun.query.filter(TestRun.created_at >= since)
    if project_id:
        query = query.filter_by(project_id=project_id)

    runs = query.all()

    total_runs = len(runs)
    success_runs = sum(1 for r in runs if r.status == 'success')
    pass_rate = round(success_runs / total_runs * 100, 1) if total_runs > 0 else 0

    # 按类型统计
    by_type = {}
    for tt in TEST_TYPES:
        type_runs = [r for r in runs if r.test_type == tt]
        type_total = len(type_runs)
        type_passed = sum(1 for r in type_runs if r.status == 'success')
        by_type[tt] = {
            'total': type_total,
            'passed': type_passed,
            'failed': type_total - type_passed,
            'pass_rate': round(type_passed / type_total * 100, 1) if type_total > 0 else 0,
        }

    # 每日趋势
    daily = get_pass_rate_trend(project_id, days, granularity='day')

    return {
        'period_days': days,
        'total_runs': total_runs,
        'pass_rate': pass_rate,
        'by_type': by_type,
        'daily': daily,
    }


def _get_bucket_key(dt: datetime, granularity: str) -> str:
    """根据粒度生成时间桶的 key"""
    if granularity == 'day':
        return dt.strftime('%Y-%m-%d')
    elif granularity == 'week':
        # ISO 周：YYYY-Www
        iso = dt.isocalendar()
        return f'{iso[0]}-W{iso[1]:02d}'
    elif granularity == 'month':
        return dt.strftime('%Y-%m')
    else:
        return dt.strftime('%Y-%m-%d')