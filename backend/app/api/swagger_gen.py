"""
Swagger 智能用例生成 API

基于 OpenAPI/Swagger 规范自动生成测试用例。
"""

import json
from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..services.ai.swagger_case_generator import swagger_case_generator
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/ai/generate-cases-from-swagger', methods=['POST'])
@jwt_required()
def generate_cases_from_swagger():
    """
    基于 Swagger/OpenAPI 规范生成测试用例

    请求体:
        swagger_content: Swagger JSON 或 YAML 字符串（必填）
        content_type: 'json' 或 'yaml'（默认 'json'）
        project_id: 可选，关联的项目 ID
        collection_name: 可选，创建的测试集合名称（默认使用 Swagger 标题）
        save: 是否直接保存到数据库（默认 false，仅返回生成结果）

    Returns:
        生成的测试用例列表
    """
    data = request.get_json() or {}
    user_id = get_current_user_id()

    swagger_content = data.get('swagger_content', '')
    if not swagger_content or not swagger_content.strip():
        return error_response(400, 'swagger_content is required')

    content_type = data.get('content_type', 'json')
    if content_type not in ('json', 'yaml'):
        return error_response(400, 'content_type must be "json" or "yaml"')

    project_id = data.get('project_id')
    collection_name = data.get('collection_name')
    save_to_db = data.get('save', False)

    try:
        # 生成用例
        result = swagger_case_generator.generate_cases(
            swagger_content=swagger_content,
            content_type=content_type,
            user_id=user_id,
        )

        # 如果需要保存到数据库
        saved_count = 0
        if save_to_db:
            saved_count = _save_cases_to_db(
                result=result,
                user_id=user_id,
                project_id=project_id,
                collection_name=collection_name,
            )

        response_data = {
            'spec_info': result['spec_info'],
            'endpoints_count': result['endpoints_count'],
            'generated_cases': result['generated_cases'],
            'summary': result['summary'],
        }
        if save_to_db:
            response_data['saved_count'] = saved_count

        return success_response(
            data=response_data,
            message=f"成功生成 {result['summary']['total_cases']} 个测试用例"
        )

    except ValueError as exc:
        return error_response(400, str(exc))
    except Exception as exc:
        logger.error('Swagger case generation failed', error=str(exc))
        return error_response(500, f'用例生成失败: {str(exc)}')


@api_bp.route('/ai/generate-cases-from-swagger/save', methods=['POST'])
@jwt_required()
def save_generated_cases():
    """
    将生成的测试用例保存到数据库

    请求体:
        cases: 测试用例数组（必填）
        project_id: 项目 ID（必填）
        collection_name: 集合名称（可选）
        environment_id: 关联的环境 ID（可选）
    """
    data = request.get_json() or {}
    user_id = get_current_user_id()

    cases = data.get('cases', [])
    if not cases:
        return error_response(400, 'cases is required and must be a non-empty array')

    project_id = data.get('project_id')
    if not project_id:
        return error_response(400, 'project_id is required')

    collection_name = data.get('collection_name', 'AI Generated Cases')
    environment_id = data.get('environment_id')

    try:
        saved_count = _save_cases_to_db(
            result={'generated_cases': cases, 'spec_info': {}},
            user_id=user_id,
            project_id=project_id,
            collection_name=collection_name,
            environment_id=environment_id,
        )
        return success_response(
            data={'saved_count': saved_count},
            message=f'成功保存 {saved_count} 个测试用例'
        )
    except Exception as exc:
        logger.error('Failed to save generated cases', error=str(exc))
        return error_response(500, f'保存失败: {str(exc)}')


def _save_cases_to_db(
    result: dict,
    user_id: int,
    project_id=None,
    collection_name=None,
    environment_id=None,
) -> int:
    """将生成的用例保存到数据库，返回保存数量"""
    from ..extensions import db
    from ..models.api_test_case import ApiTestCollection, ApiTestCase

    cases = result.get('generated_cases', [])
    if not cases:
        return 0

    # 创建或获取集合
    if not collection_name:
        spec_info = result.get('spec_info', {})
        collection_name = spec_info.get('title', 'AI Generated Cases')

    collection = ApiTestCollection(
        project_id=project_id,
        user_id=user_id,
        name=collection_name,
        description=f"AI generated from OpenAPI spec - {collection_name}",
    )
    db.session.add(collection)
    db.session.flush()  # 获取 ID

    saved_count = 0
    for case_data in cases:
        try:
            # 构建 URL
            url = case_data.get('url', '')
            if url.startswith('{baseUrl}'):
                url = url.replace('{baseUrl}', '', 1)

            # 构建断言
            assertions = []
            expected_status = case_data.get('expected_status')
            if expected_status:
                assertions.append({
                    'type': 'status_code',
                    'operator': 'equals',
                    'expected': expected_status,
                })
            for expected_text in case_data.get('expected_contains', []):
                assertions.append({
                    'type': 'body_contains',
                    'operator': 'contains',
                    'expected': expected_text,
                })

            # 构建标签
            tags = case_data.get('tags', [])
            category = case_data.get('category', '')
            if category and category not in tags:
                tags.append(f'ai-gen:{category}')
            if 'ai-generated' not in tags:
                tags.append('ai-generated')

            test_case = ApiTestCase(
                collection_id=collection.id,
                project_id=project_id,
                user_id=user_id,
                environment_id=environment_id,
                name=case_data.get('name', f"{case_data.get('method', 'GET')} {url}"),
                description=case_data.get('description', ''),
                method=case_data.get('method', 'GET'),
                url=url,
                headers=case_data.get('headers') or {},
                params=case_data.get('params') or {},
                body=case_data.get('body'),
                body_type=case_data.get('body_type') or 'json',
                assertions=assertions,
                tags=tags,
                priority=case_data.get('priority', 2),
                is_enabled=True,
            )
            db.session.add(test_case)
            saved_count += 1
        except Exception as exc:
            logger.warning(
                'Failed to save individual test case',
                case_name=case_data.get('name', ''),
                error=str(exc),
            )
            continue

    db.session.commit()
    return saved_count
