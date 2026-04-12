from flask import request, current_app
from flask_jwt_extended import jwt_required
from . import api_bp
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..utils.ai_copilot import process_copilot_chat

@api_bp.route('/copilot/chat', methods=['POST'])
@jwt_required()
def copilot_chat():
    """全局 AI Copilot 聊天接口"""
    data = request.get_json() or {}
    messages = data.get('messages', [])
    
    if not messages:
        return error_response(400, 'messages is required')
        
    try:
        user_id = get_current_user_id()
        runtime_config = {
            'AI_ASSISTANT_ENABLED': current_app.config.get('AI_ASSISTANT_ENABLED', True),
            'AI_ASSISTANT_BASE_URL': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
            'AI_ASSISTANT_API_KEY': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
            'AI_ASSISTANT_MODEL': current_app.config.get('AI_ASSISTANT_MODEL', ''),
            'AI_VISION_BASE_URL': current_app.config.get('AI_VISION_BASE_URL', ''),
            'AI_VISION_API_KEY': current_app.config.get('AI_VISION_API_KEY', ''),
            'AI_VISION_MODEL': current_app.config.get('AI_VISION_MODEL', ''),
        }

        # 允许前端覆盖配置
        if data.get('base_url'):
            runtime_config['AI_ASSISTANT_BASE_URL'] = str(data.get('base_url')).strip()
        if data.get('model'):
            runtime_config['AI_ASSISTANT_MODEL'] = str(data.get('model')).strip()
        if data.get('api_key'):
            runtime_config['AI_ASSISTANT_API_KEY'] = str(data.get('api_key')).strip()
        if data.get('vision_base_url'):
            runtime_config['AI_VISION_BASE_URL'] = str(data.get('vision_base_url')).strip()
        if data.get('vision_model'):
            runtime_config['AI_VISION_MODEL'] = str(data.get('vision_model')).strip()
        if data.get('vision_api_key'):
            runtime_config['AI_VISION_API_KEY'] = str(data.get('vision_api_key')).strip()

        reply = process_copilot_chat(messages, user_id, runtime_config)
        return success_response(data=reply)
    except Exception as exc:
        return error_response(500, f'Copilot request failed: {str(exc)}')
