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
        from .api_test import _build_ai_runtime_config
        user_id = get_current_user_id()
        runtime_config = _build_ai_runtime_config(data)

        results = execute_global_search(query, user_id, runtime_config)
        return success_response(data={'results': results})
    except Exception as exc:
        return error_response(500, f'全局搜索失败: {str(exc)}')
