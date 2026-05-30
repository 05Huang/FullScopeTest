"""
质量门禁 API 接口模块

提供质量门禁规则的 CRUD 和评估功能
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.quality_gate import QualityGate
from ..models.test_run import TestRun
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/quality-gates', methods=['GET'])
@jwt_required()
def get_quality_gates():
    """获取质量门禁列表"""
    project_id = request.args.get('project_id', type=int)

    query = QualityGate.query
    if project_id:
        query = query.filter_by(project_id=project_id)

    gates = query.order_by(QualityGate.created_at.desc()).all()
    return success_response(data=[g.to_dict() for g in gates])


@api_bp.route('/quality-gates', methods=['POST'])
@jwt_required()
def create_quality_gate():
    """创建质量门禁规则"""
    user_id = get_current_user_id()
    data = request.get_json() or {}

    name = data.get('name')
    project_id = data.get('project_id')
    if not name or not project_id:
        return error_response(400, 'name and project_id are required')

    gate = QualityGate(
        project_id=project_id,
        name=name,
        description=data.get('description', ''),
        is_active=data.get('is_active', True),
        min_pass_rate=data.get('min_pass_rate', 100.0),
        max_p95_response_time=data.get('max_p95_response_time'),
        max_visual_diff_percentage=data.get('max_visual_diff_percentage'),
        created_by=user_id,
    )

    db.session.add(gate)
    db.session.commit()

    return success_response(data=gate.to_dict(), message='质量门禁创建成功')


@api_bp.route('/quality-gates/<int:gate_id>', methods=['GET'])
@jwt_required()
def get_quality_gate(gate_id):
    """获取质量门禁详情"""
    gate = QualityGate.query.get(gate_id)
    if not gate:
        return error_response(404, '质量门禁不存在')
    return success_response(data=gate.to_dict())


@api_bp.route('/quality-gates/<int:gate_id>', methods=['PUT'])
@jwt_required()
def update_quality_gate(gate_id):
    """更新质量门禁规则"""
    gate = QualityGate.query.get(gate_id)
    if not gate:
        return error_response(404, '质量门禁不存在')

    data = request.get_json() or {}

    for field in ['name', 'description', 'is_active', 'min_pass_rate',
                  'max_p95_response_time', 'max_visual_diff_percentage']:
        if field in data:
            setattr(gate, field, data[field])

    db.session.commit()
    return success_response(data=gate.to_dict(), message='质量门禁更新成功')


@api_bp.route('/quality-gates/<int:gate_id>', methods=['DELETE'])
@jwt_required()
def delete_quality_gate(gate_id):
    """删除质量门禁规则"""
    gate = QualityGate.query.get(gate_id)
    if not gate:
        return error_response(404, '质量门禁不存在')

    db.session.delete(gate)
    db.session.commit()
    return success_response(message='质量门禁删除成功')


@api_bp.route('/quality-gates/<int:gate_id>/evaluate', methods=['POST'])
@jwt_required()
def evaluate_quality_gate(gate_id):
    """评估质量门禁"""
    gate = QualityGate.query.get(gate_id)
    if not gate:
        return error_response(404, '质量门禁不存在')

    data = request.get_json() or {}
    test_run_id = data.get('test_run_id')
    if not test_run_id:
        return error_response(400, 'test_run_id is required')

    test_run = TestRun.query.get(test_run_id)
    if not test_run:
        return error_response(404, '测试运行记录不存在')

    evaluation_details = {}
    passed = True

    # 检查通过率
    if gate.min_pass_rate is not None and test_run.total_cases > 0:
        pass_rate = (test_run.passed / test_run.total_cases) * 100
        evaluation_details['pass_rate'] = {
            'threshold': gate.min_pass_rate,
            'actual': round(pass_rate, 2),
            'passed': pass_rate >= gate.min_pass_rate,
        }
        if pass_rate < gate.min_pass_rate:
            passed = False

    # 检查 P95 响应时间
    if gate.max_p95_response_time is not None:
        p95 = None
        if test_run.results and isinstance(test_run.results, dict):
            p95 = test_run.results.get('p95_response_time')
        elif test_run.results and isinstance(test_run.results, list):
            for r in test_run.results:
                if isinstance(r, dict) and 'p95_response_time' in r:
                    p95 = r['p95_response_time']
                    break

        if p95 is not None:
            evaluation_details['p95_response_time'] = {
                'threshold': gate.max_p95_response_time,
                'actual': p95,
                'passed': p95 <= gate.max_p95_response_time,
            }
            if p95 > gate.max_p95_response_time:
                passed = False

    # 检查视觉差异
    if gate.max_visual_diff_percentage is not None:
        visual_diff = None
        if test_run.results and isinstance(test_run.results, dict):
            visual_diff = test_run.results.get('visual_diff_percentage')
        elif test_run.results and isinstance(test_run.results, list):
            for r in test_run.results:
                if isinstance(r, dict) and 'visual_diff_percentage' in r:
                    visual_diff = r['visual_diff_percentage']
                    break

        if visual_diff is not None:
            evaluation_details['visual_diff'] = {
                'threshold': gate.max_visual_diff_percentage,
                'actual': visual_diff,
                'passed': visual_diff <= gate.max_visual_diff_percentage,
            }
            if visual_diff > gate.max_visual_diff_percentage:
                passed = False

    if not evaluation_details:
        evaluation_details['note'] = 'No checks configured'

    # 同步到 GitHub Check Run
    if data.get('github_check_run_id'):
        try:
            from ..services.github_check_service import create_check_service
            from ..models.github_integration import GitHubIntegration

            integration = GitHubIntegration.query.filter_by(user_id=gate.created_by, is_active=True).first()
            if integration:
                service = create_check_service(integration)
                conclusion = 'success' if passed else 'failure'
                status_text = 'PASSED' if passed else 'FAILED'

                summary = f'Quality Gate: {gate.name}\n\n'
                summary += f'Overall Status: {status_text}\n\n'
                for check_name, details in evaluation_details.items():
                    check_status = 'PASS' if details.get('passed') else 'FAIL'
                    summary += f'- {check_status} {check_name}: {details.get("actual")} (threshold: {details.get("threshold")})\n'

                service.update_check_run(
                    repo_full_name='',
                    check_run_id=data.get('github_check_run_id'),
                    status='completed',
                    conclusion=conclusion,
                    output_title=f'Quality Gate {status_text}',
                    output_summary=summary,
                )
        except Exception as e:
            logger.error(f'Failed to sync to GitHub Check Run: {e}')

    return success_response(data={'passed': passed, 'details': evaluation_details, 'gate_id': gate_id, 'test_run_id': test_run_id}, message='评估完成')


@api_bp.route('/quality-gates/<int:gate_id>/evaluations', methods=['GET'])
@jwt_required()
def get_quality_gate_evaluations(gate_id):
    """获取质量门禁评估历史"""
    gate = QualityGate.query.get(gate_id)
    if not gate:
        return error_response(404, '质量门禁不存在')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    evaluations = QualityGateEvaluation.query.filter_by(
        quality_gate_id=gate_id
    ).order_by(
        QualityGateEvaluation.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return success_response(data={
        'items': [e.to_dict() for e in evaluations.items],
        'total': evaluations.total,
        'page': page,
        'per_page': per_page,
    })
