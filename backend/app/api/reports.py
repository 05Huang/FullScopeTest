"""
测试报告模块 - API

实现测试报告相关功能：报告列表、详情、统计、导出
"""

from flask import request, send_file
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func, or_
import json
import os
import tempfile

from . import api_bp
from ..extensions import db
from ..models.test_run import TestRun
from ..models.test_report import TestReport
from ..models.project import Project
from ..models.api_test_case import ApiTestCase
from ..models.web_test_script import WebTestScript
from ..models.perf_test_scenario import PerfTestScenario
from ..utils.response import success_response, error_response, paginate_response
from ..utils import get_current_user_id


@api_bp.route('/reports/health', methods=['GET'])
def reports_health():
    """报告模块健康检查"""
    return success_response(message='报告模块正常')


# ==================== 测试执行记录 ====================

@api_bp.route('/test-runs', methods=['GET'])
@jwt_required()
def get_test_runs():
    """
    获取测试执行记录列表
    
    查询参数:
        project_id: 项目 ID
        test_type: 测试类型 (api/web/performance)
        status: 状态 (pending/running/success/failed/cancelled)
        page: 页码
        per_page: 每页数量
        start_date: 开始日期
        end_date: 结束日期
    """
    user_id = get_current_user_id()
    
    # 获取查询参数
    project_id = request.args.get('project_id', type=int)
    test_type = request.args.get('test_type')
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 构建查询 - 只查询用户拥有的项目的测试记录
    query = db.session.query(TestRun).join(
        Project, TestRun.project_id == Project.id
    ).filter(Project.owner_id == user_id)
    
    if project_id:
        query = query.filter(TestRun.project_id == project_id)
    if test_type:
        query = query.filter(TestRun.test_type == test_type)
    if status:
        query = query.filter(TestRun.status == status)
    if start_date:
        query = query.filter(TestRun.created_at >= start_date)
    if end_date:
        query = query.filter(TestRun.created_at <= end_date)
    
    # 分页
    pagination = query.order_by(TestRun.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(
        items=[r.to_dict() for r in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page
    )


@api_bp.route('/test-runs', methods=['POST'])
@jwt_required()
def create_test_run():
    """
    创建测试执行记录
    """
    user_id = get_current_user_id()
    data = request.get_json()
    
    project_id = data.get('project_id')
    if not project_id:
        return error_response(400, '项目 ID 不能为空')
    
    # 验证项目权限
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return error_response(404, '项目不存在')
    
    test_run = TestRun(
        project_id=project_id,
        test_type=data.get('test_type', 'api'),
        test_object_id=data.get('test_object_id'),
        test_object_name=data.get('test_object_name'),
        status='pending',
        total_cases=data.get('total_cases', 0),
        environment_id=data.get('environment_id'),
        environment_name=data.get('environment_name'),
        triggered_by=data.get('triggered_by', 'manual'),
        triggered_user_id=user_id
    )
    
    db.session.add(test_run)
    db.session.commit()
    
    return success_response(data=test_run.to_dict(), message='创建成功', code=201)


@api_bp.route('/test-runs/<int:run_id>', methods=['GET'])
@jwt_required()
def get_test_run(run_id):
    """获取测试执行记录详情"""
    user_id = get_current_user_id()
    
    test_run = db.session.query(TestRun).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        TestRun.id == run_id,
        Project.owner_id == user_id
    ).first()
    
    if not test_run:
        return error_response(404, '测试记录不存在')
    
    return success_response(data=test_run.to_dict())


@api_bp.route('/test-runs/<int:run_id>', methods=['PUT'])
@jwt_required()
def update_test_run(run_id):
    """更新测试执行记录"""
    user_id = get_current_user_id()
    
    test_run = db.session.query(TestRun).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        TestRun.id == run_id,
        Project.owner_id == user_id
    ).first()
    
    if not test_run:
        return error_response(404, '测试记录不存在')
    
    data = request.get_json()
    
    # 更新字段
    for field in ['status', 'total_cases', 'passed', 'failed', 'skipped', 'error',
                  'duration', 'started_at', 'finished_at', 'results', 'report_path',
                  'allure_report_path', 'error_message']:
        if field in data:
            value = data[field]
            # 处理日期时间字段
            if field in ['started_at', 'finished_at'] and value:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            setattr(test_run, field, value)
    
    db.session.commit()
    
    return success_response(data=test_run.to_dict(), message='更新成功')


@api_bp.route('/test-runs/<int:run_id>', methods=['DELETE'])
@jwt_required()
def delete_test_run(run_id):
    """删除测试执行记录"""
    user_id = get_current_user_id()
    
    test_run = db.session.query(TestRun).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        TestRun.id == run_id,
        Project.owner_id == user_id
    ).first()
    
    if not test_run:
        return error_response(404, '测试记录不存在')
    
    db.session.delete(test_run)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 报告统计 ====================

@api_bp.route('/reports/statistics', methods=['GET'])
@jwt_required()
def get_report_statistics():
    """
    获取测试报告统计数据
    
    查询参数:
        project_id: 项目 ID (可选)
        days: 统计天数 (默认 7)
    """
    user_id = get_current_user_id()
    project_id = request.args.get('project_id', type=int)
    days = request.args.get('days', 7, type=int)
    
    # 计算时间范围
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 构建基础查询
    base_query = db.session.query(TestRun).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        Project.owner_id == user_id,
        TestRun.created_at >= start_date
    )
    
    if project_id:
        base_query = base_query.filter(TestRun.project_id == project_id)
    
    # 总体统计
    total_runs = base_query.count()
    success_runs = base_query.filter(TestRun.status == 'success').count()
    failed_runs = base_query.filter(TestRun.status == 'failed').count()
    running_runs = base_query.filter(TestRun.status == 'running').count()
    
    # 按测试类型统计
    type_stats = db.session.query(
        TestRun.test_type,
        func.count(TestRun.id).label('count'),
        func.sum(TestRun.passed).label('passed'),
        func.sum(TestRun.failed).label('failed')
    ).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        Project.owner_id == user_id,
        TestRun.created_at >= start_date
    )
    
    if project_id:
        type_stats = type_stats.filter(TestRun.project_id == project_id)
    
    type_stats = type_stats.group_by(TestRun.test_type).all()
    
    # 每日趋势统计
    daily_stats = db.session.query(
        func.date(TestRun.created_at).label('date'),
        func.sum(TestRun.passed).label('passed'),
        func.sum(TestRun.failed).label('failed'),
        func.count(TestRun.id).label('total')
    ).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        Project.owner_id == user_id,
        TestRun.created_at >= start_date
    )
    
    if project_id:
        daily_stats = daily_stats.filter(TestRun.project_id == project_id)
    
    daily_stats = daily_stats.group_by(
        func.date(TestRun.created_at)
    ).order_by(func.date(TestRun.created_at)).all()
    
    # 构建完整的日期范围
    daily_stats_dict = {
        str(stat.date): {
            'passed': stat.passed or 0,
            'failed': stat.failed or 0,
            'total': stat.total or 0
        }
        for stat in daily_stats
    }
    
    daily_trend = []
    for i in range(days - 1, -1, -1):
        # 注意：这里需要与 func.date() 返回的格式一致，通常为 YYYY-MM-DD
        date_str = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
        daily_trend.append({
            'date': date_str,
            'passed': daily_stats_dict.get(date_str, {}).get('passed', 0),
            'failed': daily_stats_dict.get(date_str, {}).get('failed', 0),
            'total': daily_stats_dict.get(date_str, {}).get('total', 0)
        })
    
    return success_response(data={
        'summary': {
            'total_runs': total_runs,
            'success_runs': success_runs,
            'failed_runs': failed_runs,
            'running_runs': running_runs,
            'success_rate': round(success_runs / total_runs * 100, 2) if total_runs > 0 else 0
        },
        'by_type': [
            {
                'type': stat.test_type,
                'count': stat.count,
                'passed': stat.passed or 0,
                'failed': stat.failed or 0
            }
            for stat in type_stats
        ],
        'daily_trend': daily_trend
    })


@api_bp.route('/reports/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """
    获取仪表盘统计数据
    """
    user_id = get_current_user_id()
    
    # 获取用户的所有项目 ID
    project_ids = [p.id for p in Project.query.filter_by(owner_id=user_id).all()]
    
    # API 测试统计
    api_total = ApiTestCase.query.filter(
        or_(ApiTestCase.project_id.in_(project_ids), ApiTestCase.user_id == user_id) if project_ids else ApiTestCase.user_id == user_id
    ).count()
    
    api_passed = ApiTestCase.query.filter(
        or_(ApiTestCase.project_id.in_(project_ids), ApiTestCase.user_id == user_id) if project_ids else ApiTestCase.user_id == user_id,
        ApiTestCase.last_status == 'passed'
    ).count()
    
    api_failed = ApiTestCase.query.filter(
        or_(ApiTestCase.project_id.in_(project_ids), ApiTestCase.user_id == user_id) if project_ids else ApiTestCase.user_id == user_id,
        ApiTestCase.last_status == 'failed'
    ).count()
    
    # Web 测试统计
    web_total = WebTestScript.query.filter(
        or_(WebTestScript.project_id.in_(project_ids), WebTestScript.user_id == user_id) if project_ids else WebTestScript.user_id == user_id
    ).count()
    
    web_passed = WebTestScript.query.filter(
        or_(WebTestScript.project_id.in_(project_ids), WebTestScript.user_id == user_id) if project_ids else WebTestScript.user_id == user_id,
        WebTestScript.status == 'passed'
    ).count()
    
    web_failed = WebTestScript.query.filter(
        or_(WebTestScript.project_id.in_(project_ids), WebTestScript.user_id == user_id) if project_ids else WebTestScript.user_id == user_id,
        WebTestScript.status == 'failed'
    ).count()
    
    # 性能测试统计
    perf_total = PerfTestScenario.query.filter(
        or_(PerfTestScenario.project_id.in_(project_ids), PerfTestScenario.user_id == user_id) if project_ids else PerfTestScenario.user_id == user_id
    ).count()
    
    perf_running = PerfTestScenario.query.filter(
        or_(PerfTestScenario.project_id.in_(project_ids), PerfTestScenario.user_id == user_id) if project_ids else PerfTestScenario.user_id == user_id,
        PerfTestScenario.status == 'running'
    ).count()
    
    # 最近执行记录
    recent_runs_query = TestRun.query
    if project_ids:
        recent_runs_query = recent_runs_query.filter(
            or_(
                TestRun.project_id.in_(project_ids),
                TestRun.triggered_user_id == user_id
            )
        )
    else:
        recent_runs_query = recent_runs_query.filter(
            TestRun.triggered_user_id == user_id
        )
    recent_runs = recent_runs_query.order_by(TestRun.created_at.desc()).limit(10).all()
    
    return success_response(data={
        'api_tests': {
            'total': api_total,
            'passed': api_passed,
            'failed': api_failed
        },
        'web_tests': {
            'total': web_total,
            'passed': web_passed,
            'failed': web_failed
        },
        'perf_tests': {
            'total': perf_total,
            'running': perf_running
        },
        'recent_runs': [r.to_dict() for r in recent_runs]
    })


# ==================== 报告导出 ====================

@api_bp.route('/reports/<int:run_id>/export', methods=['GET'])
@jwt_required()
def export_report(run_id):
    """
    导出测试报告
    
    查询参数:
        format: 导出格式 (json/html)
    """
    user_id = get_current_user_id()
    export_format = request.args.get('format', 'json')
    
    test_run = db.session.query(TestRun).join(
        Project, TestRun.project_id == Project.id
    ).filter(
        TestRun.id == run_id,
        Project.owner_id == user_id
    ).first()
    
    if not test_run:
        return error_response(404, '测试记录不存在')
    
    if export_format == 'json':
        # 导出 JSON 格式
        report_data = {
            'report': test_run.to_dict(),
            'generated_at': datetime.utcnow().isoformat(),
            'generated_by': 'FullScopeTest'
        }
        return success_response(data=report_data)
    
    elif export_format == 'html':
        # 生成 HTML 报告
        html_content = generate_html_report(test_run)
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        return send_file(
            temp_path,
            mimetype='text/html',
            as_attachment=True,
            download_name=f'report_{run_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        )
    
    else:
        return error_response(400, '不支持的导出格式')


def generate_html_report(test_run):
    """生成 HTML 格式的测试报告"""
    pass_rate = round(test_run.passed / test_run.total_cases * 100, 2) if test_run.total_cases > 0 else 0
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - {test_run.test_object_name or test_run.id}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ font-size: 24px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.8; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .card h2 {{ font-size: 18px; color: #333; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .stat-item {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .stat-value {{ font-size: 28px; font-weight: bold; color: #333; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
        .passed {{ color: #52c41a; }}
        .failed {{ color: #ff4d4f; }}
        .progress-bar {{ height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin: 15px 0; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #52c41a, #73d13d); border-radius: 10px; transition: width 0.5s; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        .status-success {{ color: #52c41a; }}
        .status-failed {{ color: #ff4d4f; }}
        .footer {{ text-align: center; padding: 20px; color: #999; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 测试报告</h1>
            <p>{test_run.test_object_name or f'测试执行 #{test_run.id}'}</p>
        </div>
        
        <div class="card">
            <h2>📈 测试概览</h2>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{test_run.total_cases}</div>
                    <div class="stat-label">总用例数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value passed">{test_run.passed}</div>
                    <div class="stat-label">通过</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value failed">{test_run.failed}</div>
                    <div class="stat-label">失败</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{test_run.skipped}</div>
                    <div class="stat-label">跳过</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{pass_rate}%</div>
                    <div class="stat-label">通过率</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{test_run.duration or 0:.2f}s</div>
                    <div class="stat-label">执行时间</div>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {pass_rate}%"></div>
            </div>
        </div>
        
        <div class="card">
            <h2>📋 执行信息</h2>
            <table>
                <tr><td><strong>测试类型</strong></td><td>{test_run.test_type}</td></tr>
                <tr><td><strong>执行状态</strong></td><td class="status-{'success' if test_run.status == 'success' else 'failed'}">{test_run.status}</td></tr>
                <tr><td><strong>测试环境</strong></td><td>{test_run.environment_name or '-'}</td></tr>
                <tr><td><strong>触发方式</strong></td><td>{test_run.triggered_by}</td></tr>
                <tr><td><strong>开始时间</strong></td><td>{test_run.started_at or '-'}</td></tr>
                <tr><td><strong>结束时间</strong></td><td>{test_run.finished_at or '-'}</td></tr>
            </table>
        </div>
        
        <div class="footer">
            <p>由 FullScopeTest 自动化测试平台生成 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>'''
    
    return html


# ==================== 测试报告 API ====================

@api_bp.route('/test-reports', methods=['GET'])
@jwt_required()
def get_test_reports():
    """
    获取测试报告列表
    
    查询参数:
        project_id: 项目 ID
        test_type: 测试类型 (api/web/performance)
        page: 页码
        per_page: 每页数量
    """
    user_id = get_current_user_id()
    
    # 获取查询参数
    project_id = request.args.get('project_id', type=int)
    test_type = request.args.get('test_type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 构建查询
    query = TestReport.query.join(TestRun).join(Project)
    
    if project_id:
        query = query.filter(TestReport.project_id == project_id)
    
    if test_type:
        query = query.filter(TestReport.test_type == test_type)
    
    # 只查询用户有权限的项目
    query = query.filter(Project.owner_id == user_id)
    
    # 排序
    query = query.order_by(TestReport.created_at.desc())
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return paginate_response(
        items=[report.to_dict() for report in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page
    )


@api_bp.route('/test-reports/<int:report_id>', methods=['GET'])
@jwt_required()
def get_test_report(report_id):
    """获取测试报告详情"""
    user_id = get_current_user_id()
    
    report = TestReport.query.join(TestRun).join(Project).filter(
        TestReport.id == report_id,
        Project.owner_id == user_id
    ).first()
    
    if not report:
        return error_response(message='报告不存在', code=404)
    
    return success_response(data=report.to_detail_dict())


@api_bp.route('/test-reports/<int:report_id>/html', methods=['GET'])
@jwt_required()
def get_test_report_html(report_id):
    """获取测试报告 HTML"""
    user_id = get_current_user_id()
    
    report = TestReport.query.join(TestRun).join(Project).filter(
        TestReport.id == report_id,
        Project.owner_id == user_id
    ).first()
    
    if not report:
        return error_response(message='报告不存在', code=404)
    
    # 如果没有 HTML 报告，生成一个
    if not report.report_html:
        results = report.report_data.get('results', []) if report.report_data else []

        def _render_body(body, limit=2000):
            try:
                if isinstance(body, (dict, list)):
                    text = json.dumps(body, ensure_ascii=False, indent=2)
                else:
                    text = str(body) if body is not None else '-'
            except Exception:
                text = str(body) if body is not None else '-'
            return text if len(text) <= limit else text[:limit] + '...'

        def _render_attachments(attachments):
            if not attachments:
                return '-'
            lines = []
            for att in attachments:
                if not isinstance(att, dict):
                    lines.append(str(att))
                    continue
                name = att.get('name') or 'attachment'
                att_type = att.get('type') or 'text'
                lines.append(f"{name} ({att_type})")
            return '<br>'.join(lines)

        results_rows = "".join([f'''
                <tr>
                    <td>{result.get('name', '')}</td>
                    <td class="{'passed' if result.get('passed') else 'failed'}">
                        {'✓ 通过' if result.get('passed') else '✗ 失败'}
                    </td>
                    <td>{result.get('status_code', '-')}</td>
                    <td>{result.get('response_time', 0)}</td>
                    <td><pre style="white-space: pre-wrap;">{_render_body(result.get('response_body'))}</pre></td>
                    <td>{result.get('error') or '-'}</td>
                    <td>{_render_attachments(result.get('attachments'))}</td>
                </tr>
                ''' for result in results])

        # 简单的 HTML 报告模板
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{report.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .summary-card {{ background: #f9f9f9; padding: 20px; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #666; font-size: 14px; }}
        .summary-card p {{ margin: 0; font-size: 28px; font-weight: bold; color: #333; }}
        .passed {{ color: #4CAF50; }}
        .failed {{ color: #f44336; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f5f5f5; font-weight: bold; }}
        tr:hover {{ background: #f9f9f9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{report.title}</h1>
        <div class="summary">
            <div class="summary-card">
                <h3>总用例数</h3>
                <p>{report.summary.get('total', 0)}</p>
            </div>
            <div class="summary-card">
                <h3>通过数</h3>
                <p class="passed">{report.summary.get('passed', 0)}</p>
            </div>
            <div class="summary-card">
                <h3>失败数</h3>
                <p class="failed">{report.summary.get('failed', 0)}</p>
            </div>
            <div class="summary-card">
                <h3>成功率</h3>
                <p>{report.summary.get('success_rate', 0)}%</p>
            </div>
            <div class="summary-card">
                <h3>执行耗时</h3>
                <p>{report.summary.get('duration', 0)}s</p>
            </div>
        </div>
        <h2>测试结果详情</h2>
        <table>
            <thead>
                <tr>
                    <th>用例名称</th>
                    <th>状态</th>
                    <th>状态码</th>
                    <th>耗时(ms)</th>
                    <th>响应数据</th>
                    <th>错误/异常</th>
                    <th>附件</th>
                </tr>
            </thead>
            <tbody>
                {results_rows}
            </tbody>
        </table>
        <div style="margin-top: 30px; padding: 20px; background: #f5f5f5; border-radius: 5px;">
            <p style="margin: 0; color: #666;">生成时间: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
        """
        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    
    return report.report_html, 200, {'Content-Type': 'text/html; charset=utf-8'}


@api_bp.route('/test-reports/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_test_report(report_id):
    """删除测试报告"""
    user_id = get_current_user_id()

    # 使用更健壮的查询方式，直接通过 project_id JOIN
    from ..models.project import Project
    from sqlalchemy import delete as sql_delete

    # 先检查权限
    report = db.session.query(TestReport).join(
        Project, TestReport.project_id == Project.id
    ).filter(
        TestReport.id == report_id,
        Project.owner_id == user_id
    ).first()

    if not report:
        return error_response(message='报告不存在或无权访问', code=404)

    try:
        # 使用原始 SQL DELETE，绕过 ORM 的关系处理
        # 避免 SQLAlchemy 尝试更新关联的 TestRun
        stmt = sql_delete(TestReport).where(TestReport.id == report_id)
        db.session.execute(stmt)
        db.session.commit()

        return success_response(message='删除成功')
    except Exception as e:
        db.session.rollback()
        return error_response(message=f'删除失败: {str(e)}', code=500)

