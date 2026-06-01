"""
触发器与定时任务模块 (CI/CD)

提供 Webhook 触发和定时任务调度的相关接口
"""

import uuid
from flask import request, current_app, Blueprint
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.webhook_token import WebhookToken
from ..models.scheduled_task import ScheduledTask
from ..models.project import Project
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..utils.security import verify_hmac_signature, sanitize_log_message
import requests
from ..core.logging import get_logger

logger = get_logger(__name__)

# ==================== Webhook 触发器 ====================

@api_bp.route('/webhooks', methods=['GET'])
@jwt_required()
def get_webhooks():
    """获取项目的 Webhook 列表"""
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return error_response(400, '缺少 project_id 参数')
        
    webhooks = WebhookToken.query.filter_by(project_id=project_id).all()
    return success_response(data=[w.to_dict() for w in webhooks])


@api_bp.route('/webhooks', methods=['POST'])
@jwt_required()
def create_webhook():
    """创建 Webhook"""
    data = request.get_json()
    project_id = data.get('project_id')
    name = data.get('name')
    target_type = data.get('target_type')
    target_id = data.get('target_id')
    
    if not all([project_id, name, target_type, target_id]):
        return error_response(400, '参数不完整')
        
    webhook = WebhookToken(
        project_id=project_id,
        name=name,
        target_type=target_type,
        target_id=target_id,
        token=uuid.uuid4().hex
    )
    db.session.add(webhook)
    db.session.commit()
    return success_response(data=webhook.to_dict(), message='Webhook 创建成功')


@api_bp.route('/webhooks/<int:webhook_id>', methods=['DELETE'])
@jwt_required()
def delete_webhook(webhook_id):
    """删除 Webhook"""
    user_id = get_current_user_id()
    webhook = WebhookToken.query.get(webhook_id)
    if not webhook:
        return error_response(404, 'Webhook 不存在')

    # 校验权限：Webhook 所属项目必须属于当前用户
    project = Project.query.filter_by(id=webhook.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权删除该 Webhook')

    db.session.delete(webhook)
    db.session.commit()
    return success_response(message='Webhook 删除成功')


# ==================== 触发规则 ====================

@api_bp.route('/trigger-rules', methods=['GET'])
@jwt_required()
def get_trigger_rules():
    """获取项目的触发规则列表"""
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return error_response(400, '缺少 project_id 参数')

    from ..services.trigger_rule_service import get_rules_by_project
    rules = get_rules_by_project(project_id)
    return success_response(data=[r.to_dict() for r in rules])


@api_bp.route('/trigger-rules', methods=['POST'])
@jwt_required()
def create_trigger_rule():
    """创建触发规则"""
    data = request.get_json()
    user_id = get_current_user_id()

    required_fields = ['project_id', 'name', 'trigger_event', 'target_type']
    if not all(data.get(f) for f in required_fields):
        return error_response(400, '参数不完整')

    from ..services.trigger_rule_service import create_rule
    rule = create_rule(
        project_id=data.get('project_id'),
        name=data.get('name'),
        trigger_event=data.get('trigger_event'),
        target_type=data.get('target_type'),
        description=data.get('description'),
        target_branches=data.get('target_branches'),
        target_tags=data.get('target_tags'),
        include_paths=data.get('include_paths'),
        exclude_paths=data.get('exclude_paths'),
        test_types=data.get('test_types'),
        tags=data.get('tags'),
        target_id=data.get('target_id'),
        created_by=user_id,
    )
    return success_response(data=rule.to_dict(), message='触发规则创建成功')


@api_bp.route('/trigger-rules/<int:rule_id>', methods=['PUT'])
@jwt_required()
def update_trigger_rule(rule_id):
    """更新触发规则"""
    from ..services.trigger_rule_service import update_rule
    data = request.get_json()

    rule = update_rule(rule_id, **data)
    if not rule:
        return error_response(404, '规则不存在')

    return success_response(data=rule.to_dict(), message='触发规则更新成功')


@api_bp.route('/trigger-rules/<int:rule_id>', methods=['DELETE'])
@jwt_required()
def delete_trigger_rule(rule_id):
    """删除触发规则"""
    from ..services.trigger_rule_service import delete_rule

    success = delete_rule(rule_id)
    if not success:
        return error_response(404, '规则不存在')

    return success_response(message='触发规则删除成功')


# 公开执行端点，不需要认证
@api_bp.route('/triggers/<string:token>', methods=['POST', 'GET'])
def trigger_webhook(token):
    """通过 Webhook Token 触发执行"""
    webhook = WebhookToken.query.filter_by(token=token).first()
    if not webhook:
        logger.warning("Webhook 触发失败: 无效的 Token")
        return error_response(404, '无效的 Token')

    # 验证 HMAC 签名 (如果配置了密钥)
    webhook_secret = current_app.config.get('WEBHOOK_SECRET')
    if webhook_secret and request.method == 'POST':
        signature = request.headers.get('X-Hub-Signature-256') or request.headers.get('X-Signature-256')
        if not signature:
            logger.warning("Webhook 触发失败: 缺少签名头")
            return error_response(401, '缺少签名头')

        payload = request.get_data()
        if not verify_hmac_signature(payload, signature, webhook_secret):
            logger.warning("Webhook 触发失败: 签名验证失败")
            return error_response(401, '签名验证失败')

    # 根据 target_type 调用相应的执行逻辑
    try:
        from ..tasks import run_api_collection_task, run_web_collection_task, run_perf_scenario_task

        task = None
        if webhook.target_type == 'api_collection':
            task = run_api_collection_task.delay(webhook.target_id, None)
        elif webhook.target_type == 'web_collection':
            task = run_web_collection_task.delay(webhook.target_id, None)
        elif webhook.target_type == 'perf_scenario':
            task = run_perf_scenario_task.delay(webhook.target_id)
        else:
            return error_response(400, '不支持的 target_type')

        logger.info("Webhook 触发成功", webhook_name=webhook.name, task_id=task.id if task else None)
        return success_response(data={'task_id': task.id if task else None}, message='任务已触发')
    except Exception as e:
        logger.error("Webhook 触发异常", error=str(e))
        return error_response(500, f'触发失败: {str(e)}')


# ==================== 定时任务 ====================

@api_bp.route('/schedules', methods=['GET'])
@jwt_required()
def get_schedules():
    """获取项目的定时任务列表"""
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return error_response(400, '缺少 project_id 参数')
        
    tasks = ScheduledTask.query.filter_by(project_id=project_id).all()
    return success_response(data=[t.to_dict() for t in tasks])


@api_bp.route('/schedules', methods=['POST'])
@jwt_required()
def create_schedule():
    """创建定时任务"""
    data = request.get_json()
    
    required_fields = ['project_id', 'name', 'cron_expression', 'target_type', 'target_id']
    if not all(data.get(f) for f in required_fields):
        return error_response(400, '参数不完整')
        
    task = ScheduledTask(
        project_id=data.get('project_id'),
        name=data.get('name'),
        cron_expression=data.get('cron_expression'),
        target_type=data.get('target_type'),
        target_id=data.get('target_id'),
        notify_webhook=data.get('notify_webhook'),
        notify_events=data.get('notify_events', 'all')
    )
    db.session.add(task)
    db.session.commit()
    
    # 这里应调用 APScheduler 添加任务
    from ..scheduler import add_or_update_job
    add_or_update_job(task)
    
    return success_response(data=task.to_dict(), message='定时任务创建成功')


@api_bp.route('/schedules/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_schedule(task_id):
    """更新定时任务"""
    user_id = get_current_user_id()
    task = ScheduledTask.query.get(task_id)
    if not task:
        return error_response(404, '任务不存在')

    # 校验权限
    project = Project.query.filter_by(id=task.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权修改该定时任务')

    data = request.get_json()
    if 'name' in data: task.name = data['name']
    if 'cron_expression' in data: task.cron_expression = data['cron_expression']
    if 'is_active' in data: task.is_active = data['is_active']
    if 'notify_webhook' in data: task.notify_webhook = data['notify_webhook']
    if 'notify_events' in data: task.notify_events = data['notify_events']
    
    db.session.commit()
    
    # 更新 APScheduler
    from ..scheduler import add_or_update_job, remove_job
    if task.is_active:
        add_or_update_job(task)
    else:
        remove_job(task.id)
        
    return success_response(data=task.to_dict(), message='定时任务更新成功')


@api_bp.route('/schedules/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(task_id):
    """删除定时任务"""
    user_id = get_current_user_id()
    task = ScheduledTask.query.get(task_id)
    if not task:
        return error_response(404, '任务不存在')

    # 校验权限
    project = Project.query.filter_by(id=task.project_id, owner_id=user_id).first()
    if not project:
        return error_response(403, '无权删除该定时任务')

    db.session.delete(task)
    db.session.commit()
    
    # 从 APScheduler 移除
    from ..scheduler import remove_job
    remove_job(task_id)
    
    return success_response(message='定时任务删除成功')
