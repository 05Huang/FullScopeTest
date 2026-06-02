"""
API 测试用例 Service

处理测试用例的 CRUD 操作
"""

from .base import BaseService
from ..extensions import db
from ..models.api_test_case import ApiTestCase
from ..utils.exceptions import NotFoundError, ValidationError


class ApiCaseService(BaseService):

    def get_cases(self, user_id: int, collection_id: int = None, project_id: int = None):
        """获取测试用例列表"""
        query = ApiTestCase.query.filter_by(user_id=user_id)
        if collection_id:
            query = query.filter_by(collection_id=collection_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        cases = query.order_by(ApiTestCase.created_at.desc()).all()
        return [c.to_dict() for c in cases]

    def get_case(self, case_id: int, user_id: int):
        """获取用例详情"""
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError("用例", case_id)
        return case.to_dict()

    def create_case(self, user_id: int, data: dict):
        """创建测试用例"""
        if not data.get('name'):
            raise ValidationError("name is required")
        if not data.get('method'):
            raise ValidationError("method is required")
        if not data.get('url'):
            raise ValidationError("url is required")

        case = ApiTestCase(
            name=data['name'],
            description=data.get('description', ''),
            method=data['method'].upper(),
            url=data['url'],
            headers=data.get('headers', {}),
            params=data.get('params', {}),
            body=data.get('body'),
            body_type=data.get('body_type', 'json'),
            pre_script=data.get('pre_script'),
            post_script=data.get('post_script'),
            assertions=data.get('assertions', []),
            collection_id=data.get('collection_id'),
            project_id=data.get('project_id'),
            environment_id=data.get('environment_id'),
            user_id=user_id,
            mock_enabled=data.get('mock_enabled', False),
            mock_response_code=data.get('mock_response_code', 200),
            mock_response_body=data.get('mock_response_body', ''),
            mock_response_headers=data.get('mock_response_headers', {}),
            mock_delay_ms=data.get('mock_delay_ms', 0)
        )

        with self.transaction():
            self.add(case)
            self.flush()
            result = case.to_dict()
        return result

    def update_case(self, case_id: int, user_id: int, data: dict):
        """更新测试用例"""
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError("用例", case_id)

        updatable_fields = [
            'name', 'description', 'method', 'url', 'headers', 'params',
            'body', 'body_type', 'pre_script', 'post_script', 'assertions',
            'collection_id', 'environment_id', 'mock_enabled',
            'mock_response_code', 'mock_response_body',
            'mock_response_headers', 'mock_delay_ms'
        ]
        for field in updatable_fields:
            if field in data:
                setattr(case, field, data[field])

        with self.transaction():
            result = case.to_dict()
        return result

    def delete_case(self, case_id: int, user_id: int):
        """删除测试用例"""
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError("用例", case_id)

        with self.transaction():
            self.delete(case)
