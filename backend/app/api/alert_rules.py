"""
性能告警规则 API 接口模块
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.perf_test_alert import PerformanceAlertRule, PerformanceAlertLog
from ..models.perf_test_scenario import PerfTestScenario
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


def _get_rule_with_permission(rule_id, user_id):
    """获取告警规则并验证用户权限（通过 PerfTestScenario.user_id）"""
    rule = PerformanceAlertRule.query.get(rule_id)
    if not rule:
        return None, error_response(404, '告警规则不存在')
    if rule.scenario_id:
        scenario = PerfTestScenario.query.get(rule.scenario_id)
        if not scenario or scenario.user_id != user_id:
            logger.warning('IDOR attempt blocked on alert_rule',
                           user_id=user_id, rule_id=rule_id)
            return None, error_response(404, '告警规则不存在')
    return rule, None


@api_bp.route('/perf-test/alert-rules', methods=['GET'])
@jwt_required()
def get_alert_rules():
    """获取告警规则列表"""
    user_id = get_current_user_id()
    scenario_id = request.args.get('scenario_id', type=int)
    
    query = PerformanceAlertRule.query
    if scenario_id:
        query = query.filter_by(scenario_id=scenario_id)
    
    rules = query.order_by(PerformanceAlertRule.created_at.desc()).all()
    return success_response(data=[r.to_dict() for r in rules])


@api_bp.route('/perf-test/alert-rules', methods=['POST'])
@jwt_required()
def create_alert_rule():
    """创建告警规则"""
    user_id = get_current_user_id()
    data = request.get_json() or {}
    
    name = data.get('name')
    if not name:
        return error_response(400, 'name is required')
    
    condition_type = data.get('condition_type', 'absolute')
    if condition_type not in ('absolute', 'relative'):
        return error_response(400, 'condition_type must be absolute or relative')
    
    rule = PerformanceAlertRule(
        name=name,
        description=data.get('description', ''),
        scenario_id=data.get('scenario_id'),
        condition_type=condition_type,
        metric_name=data.get('metric_name'),
        operator=data.get('operator'),
        threshold_value=data.get('threshold_value'),
        relative_metric=data.get('relative_metric'),
        degradation_percentage=data.get('degradation_percentage'),
        notify_webhook=data.get('notify_webhook'),
        notify_users=data.get('notify_users', []),
        is_enabled=data.get('is_enabled', True),
    )
    
    db.session.add(rule)
    db.session.commit()
    
    return success_response(data=rule.to_dict(), message='告警规则创建成功')


@api_bp.route('/perf-test/alert-rules/<int:rule_id>', methods=['GET'])
@jwt_required()
def get_alert_rule(rule_id):
    """获取告警规则详情"""
    user_id = get_current_user_id()
    rule, err = _get_rule_with_permission(rule_id, user_id)
    if err:
        return err
    return success_response(data=rule.to_dict())


@api_bp.route('/perf-test/alert-rules/<int:rule_id>', methods=['PUT'])
@jwt_required()
def update_alert_rule(rule_id):
    """更新告警规则"""
    user_id = get_current_user_id()
    rule, err = _get_rule_with_permission(rule_id, user_id)
    if err:
        return err
    
    data = request.get_json() or {}
    
    for field in ['name', 'description', 'scenario_id', 'condition_type', 'metric_name',
                  'operator', 'threshold_value', 'relative_metric', 'degradation_percentage',
                  'notify_webhook', 'notify_users', 'is_enabled']:
        if field in data:
            setattr(rule, field, data[field])
    
    db.session.commit()
    return success_response(data=rule.to_dict(), message='告警规则更新成功')


@api_bp.route('/perf-test/alert-rules/<int:rule_id>', methods=['DELETE'])
@jwt_required()
def delete_alert_rule(rule_id):
    """删除告警规则"""
    user_id = get_current_user_id()
    rule, err = _get_rule_with_permission(rule_id, user_id)
    if err:
        return err
    
    db.session.delete(rule)
    db.session.commit()
    return success_response(message='告警规则删除成功')


@api_bp.route('/perf-test/alert-rules/<int:rule_id>/evaluate', methods=['POST'])
@jwt_required()
def evaluate_alert_rule(rule_id):
    """手动评估告警规则（指定测试结果 ID）"""
    from ..services.performance_alert_service import alert_service

    user_id = get_current_user_id()
    rule, err = _get_rule_with_permission(rule_id, user_id)
    if err:
        return err

    data = request.get_json() or {}
    test_result_id = data.get('test_result_id')
    if not test_result_id:
        return error_response(400, 'test_result_id is required')
    
    alerts = alert_service.evaluate_rules(test_result_id)
    return success_response(data=alerts, message=f'评估完成，触发 {len(alerts)} 条告警')


@api_bp.route('/perf-test/alert-logs', methods=['GET'])
@jwt_required()
def get_alert_logs():
    """获取告警日志"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    rule_id = request.args.get('rule_id', type=int)
    severity = request.args.get('severity', '').strip()
    
    query = PerformanceAlertLog.query
    
    if rule_id:
        query = query.filter_by(rule_id=rule_id)
    if severity:
        query = query.filter_by(severity=severity)
    
    pagination = query.order_by(PerformanceAlertLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    from ..utils.response import paginate_response
    return paginate_response(
        items=[l.to_dict() for l in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page
    )
