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
import requests

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
    webhook = WebhookToken.query.get(webhook_id)
    if not webhook:
        return error_response(404, 'Webhook 不存在')
        
    db.session.delete(webhook)
    db.session.commit()
    return success_response(message='Webhook 删除成功')


# 公开执行端点，不需要认证
@api_bp.route('/triggers/<string:token>', methods=['POST', 'GET'])
def trigger_webhook(token):
    """通过 Webhook Token 触发执行"""
    webhook = WebhookToken.query.filter_by(token=token).first()
    if not webhook:
        return error_response(404, '无效的 Token')
        
    # 根据 target_type 调用相应的执行逻辑
    # 注意：这里我们通过模拟内部请求或调用对应的执行函数来运行测试
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
            
        return success_response(data={'task_id': task.id if task else None}, message='任务已触发')
    except Exception as e:
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
    task = ScheduledTask.query.get(task_id)
    if not task:
        return error_response(404, '任务不存在')
        
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
    task = ScheduledTask.query.get(task_id)
    if not task:
        return error_response(404, '任务不存在')
        
    db.session.delete(task)
    db.session.commit()
    
    # 从 APScheduler 移除
    from ..scheduler import remove_job
    remove_job(task_id)
    
    return success_response(message='定时任务删除成功')
