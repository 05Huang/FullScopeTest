"""
测试用例语义去重 API

提供基于语义相似度的测试用例去重检测接口。
"""

from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..services.ai.semantic_dedup_service import find_duplicates
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/ai/find-duplicates', methods=['POST'])
@jwt_required()
def find_test_duplicates():
    """
    查找项目中语义相似的测试用例

    请求体:
        project_id: 项目 ID（必填）
        threshold: 相似度阈值（可选，默认 0.85，范围 0.0-1.0）
        case_type: 用例类型（可选，默认 'api'，可选 'web'）
        limit: 最多分析的用例数量（可选，默认 500）

    Returns:
        重复用例对列表，按相似度降序排列
    """
    data = request.get_json() or {}

    project_id = data.get('project_id')
    if not project_id:
        return error_response(400, 'project_id is required')

    threshold = data.get('threshold', 0.85)
    if not isinstance(threshold, (int, float)) or not (0.0 <= threshold <= 1.0):
        return error_response(400, 'threshold must be a number between 0.0 and 1.0')

    case_type = data.get('case_type', 'api')
    if case_type not in ('api', 'web'):
        return error_response(400, 'case_type must be "api" or "web"')

    limit = data.get('limit', 500)
    if not isinstance(limit, int) or limit < 1:
        return error_response(400, 'limit must be a positive integer')

    # 获取运行时 AI 配置
    from flask import current_app
    config = {
        'AI_ASSISTANT_BASE_URL': current_app.config.get('AI_ASSISTANT_BASE_URL', ''),
        'AI_ASSISTANT_API_KEY': current_app.config.get('AI_ASSISTANT_API_KEY', ''),
        'AI_ASSISTANT_MODEL': current_app.config.get('AI_ASSISTANT_MODEL', ''),
    }

    # 允许前端覆盖配置
    if data.get('embedding_base_url'):
        config['AI_EMBEDDING_BASE_URL'] = str(data['embedding_base_url']).strip()
    if data.get('embedding_api_key'):
        config['AI_EMBEDDING_API_KEY'] = str(data['embedding_api_key']).strip()
    if data.get('embedding_model'):
        config['AI_EMBEDDING_MODEL'] = str(data['embedding_model']).strip()

    try:
        result = find_duplicates(
            project_id=project_id,
            threshold=threshold,
            case_type=case_type,
            config=config,
            limit=limit,
        )

        return success_response(
            data=result,
            message=f'发现 {result["summary"]["duplicate_count"]} 组重复用例'
        )

    except Exception as exc:
        logger.error('Dedup scan failed', error=str(exc), project_id=project_id)
        return error_response(500, f'去重检测失败: {str(exc)}')
