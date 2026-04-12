from flask import request, current_app
from flask_jwt_extended import jwt_required
from . import api_bp
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..utils.ai_search import execute_global_search

@api_bp.route('/ai/global-search', methods=['POST'])
@jwt_required()
def global_search():
    """AI 全局搜索资产"""
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    
    if not query:
        return error_response(400, 'query is required')
        
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
            'AI_ASSISTANT_TIMEOUT': current_app.config.get('AI_ASSISTANT_TIMEOUT', 30),
        }

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

        results = execute_global_search(query, user_id, runtime_config)
        return success_response(data={'results': results})
    except Exception as exc:
        return error_response(500, f'全局搜索失败: {str(exc)}')
