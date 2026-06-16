"""
通知配置 API

提供通知渠道配置的 CRUD 和测试发送。
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.notification_config import NotificationConfig
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/notifications/configs', methods=['GET'])
@jwt_required()
def get_notification_configs():
    """获取当前用户的通知配置列表"""
    user_id = get_current_user_id()
    configs = NotificationConfig.query.filter_by(user_id=user_id).order_by(
        NotificationConfig.created_at.desc()
    ).all()
    return success_response(data=[c.to_dict() for c in configs])


@api_bp.route('/notifications/configs', methods=['POST'])
@jwt_required()
def create_notification_config():
    """创建通知配置"""
    user_id = get_current_user_id()
    data = request.get_json() or {}

    name = (data.get('name') or '').strip()
    channel = (data.get('channel_type') or data.get('channel') or '').strip()
    webhook_url = (data.get('webhook_url') or '').strip()

    if not name:
        return error_response(400, 'name 不能为空')
    if not channel:
        return error_response(400, 'channel_type 不能为空')
    if not webhook_url:
        return error_response(400, 'webhook_url 不能为空')

    valid_channels = ('webhook', 'dingtalk', 'feishu', 'slack')
    if channel not in valid_channels:
        return error_response(400, f'channel_type 必须是 {"/".join(valid_channels)} 之一')

    config = NotificationConfig(
        user_id=user_id,
        name=name,
        channel=channel,
        webhook_url=webhook_url,
        token=data.get('token', ''),
        events=data.get('events', []),
        is_active=data.get('is_active', True),
    )
    db.session.add(config)
    db.session.commit()

    logger.info('通知配置已创建', config_id=config.id, channel=channel)
    return success_response(data=config.to_dict(), message='创建成功', code=201)


@api_bp.route('/notifications/configs/<int:config_id>', methods=['PUT'])
@jwt_required()
def update_notification_config(config_id):
    """更新通知配置"""
    user_id = get_current_user_id()
    config = NotificationConfig.query.filter_by(id=config_id, user_id=user_id).first()
    if not config:
        return error_response(404, '通知配置不存在')

    data = request.get_json() or {}

    if 'name' in data:
        config.name = data['name']
    if 'channel_type' in data or 'channel' in data:
        channel = data.get('channel_type') or data.get('channel')
        if channel:
            config.channel = channel
    if 'webhook_url' in data:
        config.webhook_url = data['webhook_url']
    if 'token' in data:
        config.token = data['token']
    if 'events' in data:
        config.events = data['events']
    if 'is_active' in data:
        config.is_active = data['is_active']

    db.session.commit()
    return success_response(data=config.to_dict(), message='更新成功')


@api_bp.route('/notifications/configs/<int:config_id>', methods=['DELETE'])
@jwt_required()
def delete_notification_config(config_id):
    """删除通知配置"""
    user_id = get_current_user_id()
    config = NotificationConfig.query.filter_by(id=config_id, user_id=user_id).first()
    if not config:
        return error_response(404, '通知配置不存在')

    db.session.delete(config)
    db.session.commit()
    return success_response(message='删除成功')


@api_bp.route('/notifications/configs/<int:config_id>/test', methods=['POST'])
@jwt_required()
def test_notification(config_id):
    """测试发送通知"""
    user_id = get_current_user_id()
    config = NotificationConfig.query.filter_by(id=config_id, user_id=user_id).first()
    if not config:
        return error_response(404, '通知配置不存在')

    from ..services.notification_service import send_notification
    result = send_notification(
        channel=config.channel,
        webhook_url=config.webhook_url,
        event='test',
        title='通知测试',
        content=f'这是一条来自 FullScopeTest 的测试通知（渠道: {config.channel}）',
        token=config.token,
    )

    if result.get('success'):
        return success_response(message='测试通知发送成功')
    else:
        return error_response(500, f'测试通知发送失败: {result.get("error", "未知错误")}')
