"""
Swagger 智能用例生成服务测试

测试 OpenAPI/Swagger 解析、接口提取、AI 用例生成、数据库保存等功能
"""

import json
import pytest
from unittest.mock import patch, MagicMock


# ---- 测试用的 Swagger 样本 ----

SAMPLE_SWAGGER_JSON = {
    "openapi": "3.0.0",
    "info": {
        "title": "Pet Store API",
        "version": "1.0.0",
        "description": "A sample Pet Store API for testing"
    },
    "paths": {
        "/pets": {
            "get": {
                "operationId": "listPets",
                "summary": "List all pets",
                "tags": ["pets"],
                "parameters": [
                    {
                        "name": "limit",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "minimum": 1, "maximum": 100}
                    },
                    {
                        "name": "status",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "string", "enum": ["available", "pending", "sold"]}
                    }
                ],
                "responses": {
                    "200": {"description": "A list of pets"},
                    "400": {"description": "Invalid query parameters"}
                }
            },
            "post": {
                "operationId": "createPet",
                "summary": "Create a pet",
                "tags": ["pets"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name", "status"],
                                "properties": {
                                    "name": {"type": "string", "description": "Pet name"},
                                    "status": {"type": "string", "enum": ["available", "pending", "sold"]},
                                    "tag": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Pet created"},
                    "400": {"description": "Invalid input"},
                    "409": {"description": "Pet already exists"}
                }
            }
        },
        "/pets/{petId}": {
            "get": {
                "operationId": "getPet",
                "summary": "Get a pet by ID",
                "tags": ["pets"],
                "parameters": [
                    {
                        "name": "petId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {"description": "Pet details"},
                    "404": {"description": "Pet not found"}
                }
            },
            "delete": {
                "operationId": "deletePet",
                "summary": "Delete a pet",
                "tags": ["pets"],
                "parameters": [
                    {
                        "name": "petId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "204": {"description": "Pet deleted"},
                    "404": {"description": "Pet not found"}
                }
            }
        }
    }
}

SAMPLE_SWAGGER_YAML = """\
openapi: "3.0.0"
info:
  title: "Simple API"
  version: "1.0.0"
paths:
  /items:
    get:
      summary: "Get items"
      parameters:
        - name: page
          in: query
          required: false
          schema:
            type: integer
      responses:
        "200":
          description: "Success"
"""

MOCK_AI_RESPONSE = json.dumps([
    {
        "name": "获取宠物列表-正常",
        "description": "使用有效的 limit 参数获取宠物列表",
        "method": "GET",
        "url": "{baseUrl}/pets?limit=10",
        "headers": {"Accept": "application/json"},
        "params": {"limit": 10},
        "body": None,
        "body_type": None,
        "expected_status": 200,
        "expected_contains": [],
        "priority": 2,
        "category": "normal",
        "tags": ["pets"]
    },
    {
        "name": "获取宠物列表-limit为0",
        "description": "测试 limit 参数为 0 的边界情况",
        "method": "GET",
        "url": "{baseUrl}/pets?limit=0",
        "headers": {"Accept": "application/json"},
        "params": {"limit": 0},
        "body": None,
        "body_type": None,
        "expected_status": 400,
        "expected_contains": [],
        "priority": 3,
        "category": "boundary",
        "tags": ["pets"]
    },
    {
        "name": "获取宠物列表-limit超大值",
        "description": "测试 limit 参数超过最大值",
        "method": "GET",
        "url": "{baseUrl}/pets?limit=99999",
        "headers": {"Accept": "application/json"},
        "params": {"limit": 99999},
        "body": None,
        "body_type": None,
        "expected_status": 400,
        "expected_contains": [],
        "priority": 3,
        "category": "boundary",
        "tags": ["pets"]
    },
    {
        "name": "创建宠物-正常",
        "description": "使用完整参数创建宠物",
        "method": "POST",
        "url": "{baseUrl}/pets",
        "headers": {"Content-Type": "application/json", "Accept": "application/json"},
        "params": {},
        "body": {"name": "Buddy", "status": "available", "tag": "dog"},
        "body_type": "json",
        "expected_status": 201,
        "expected_contains": ["Buddy"],
        "priority": 1,
        "category": "normal",
        "tags": ["pets"]
    },
    {
        "name": "创建宠物-缺少必填字段",
        "description": "不传 name 字段",
        "method": "POST",
        "url": "{baseUrl}/pets",
        "headers": {"Content-Type": "application/json"},
        "params": {},
        "body": {"status": "available"},
        "body_type": "json",
        "expected_status": 400,
        "expected_contains": [],
        "priority": 2,
        "category": "error",
        "tags": ["pets"]
    },
    {
        "name": "获取宠物-不存在的ID",
        "description": "使用不存在的 petId",
        "method": "GET",
        "url": "{baseUrl}/pets/99999999",
        "headers": {"Accept": "application/json"},
        "params": {},
        "body": None,
        "body_type": None,
        "expected_status": 404,
        "expected_contains": [],
        "priority": 2,
        "category": "error",
        "tags": ["pets"]
    }
])


class TestSwaggerParser:
    """Swagger 解析功能测试"""

    def test_parse_json_swagger(self):
        """测试解析 JSON 格式的 Swagger"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        spec = svc.parse_swagger(json.dumps(SAMPLE_SWAGGER_JSON), 'json')

        assert spec['openapi'] == '3.0.0'
        assert spec['info']['title'] == 'Pet Store API'
        assert '/pets' in spec['paths']

    def test_parse_yaml_swagger(self):
        """测试解析 YAML 格式的 Swagger"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        spec = svc.parse_swagger(SAMPLE_SWAGGER_YAML, 'yaml')

        assert spec['openapi'] == '3.0.0'
        assert spec['info']['title'] == 'Simple API'

    def test_parse_invalid_json(self):
        """测试解析无效 JSON"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        with pytest.raises(ValueError, match='JSON 解析失败'):
            svc.parse_swagger('not valid json {{{', 'json')

    def test_parse_invalid_yaml(self):
        """测试解析无效 YAML"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        with pytest.raises(ValueError, match='YAML 解析失败'):
            svc.parse_swagger('invalid:\nyaml:\n  - {{{', 'yaml')

    def test_parse_no_paths(self):
        """测试解析没有 paths 的规范"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        with pytest.raises(ValueError, match='未找到 paths'):
            svc.parse_swagger(json.dumps({"openapi": "3.0.0"}), 'json')

    def test_parse_not_object(self):
        """测试解析非对象内容"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        with pytest.raises(ValueError, match='有效的 JSON/YAML 对象'):
            svc.parse_swagger(json.dumps([1, 2, 3]), 'json')


class TestEndpointExtractor:
    """接口提取功能测试"""

    def test_extract_all_endpoints(self):
        """测试提取所有接口"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        endpoints = svc.extract_endpoints(SAMPLE_SWAGGER_JSON)

        # 应该有 4 个接口：GET /pets, POST /pets, GET /pets/{petId}, DELETE /pets/{petId}
        assert len(endpoints) == 4

        methods = [(e['method'], e['path']) for e in endpoints]
        assert ('GET', '/pets') in methods
        assert ('POST', '/pets') in methods
        assert ('GET', '/pets/{petId}') in methods
        assert ('DELETE', '/pets/{petId}') in methods

    def test_extract_endpoint_details(self):
        """测试提取接口详细信息"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        endpoints = svc.extract_endpoints(SAMPLE_SWAGGER_JSON)

        # 找到 POST /pets
        post_pet = next(e for e in endpoints if e['method'] == 'POST' and e['path'] == '/pets')
        assert post_pet['summary'] == 'Create a pet'
        assert post_pet['operation_id'] == 'createPet'
        assert 'pets' in post_pet['tags']
        assert post_pet['request_body'] is not None
        assert post_pet['request_body']['required'] is True

    def test_extract_parameters(self):
        """测试提取路径参数"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        endpoints = svc.extract_endpoints(SAMPLE_SWAGGER_JSON)

        get_pet = next(e for e in endpoints if e['method'] == 'GET' and e['path'] == '/pets/{petId}')
        assert len(get_pet['parameters']) == 1
        assert get_pet['parameters'][0]['name'] == 'petId'
        assert get_pet['parameters'][0]['in'] == 'path'
        assert get_pet['parameters'][0]['required'] is True

    def test_extract_responses(self):
        """测试提取响应定义"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        endpoints = svc.extract_endpoints(SAMPLE_SWAGGER_JSON)

        post_pet = next(e for e in endpoints if e['method'] == 'POST' and e['path'] == '/pets')
        assert '201' in post_pet['responses']
        assert '400' in post_pet['responses']
        assert '409' in post_pet['responses']

    def test_empty_paths(self):
        """测试空路径"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        endpoints = svc.extract_endpoints({"paths": {}})
        assert endpoints == []


class TestCaseGeneration:
    """用例生成功能测试"""

    @patch('app.services.ai.swagger_case_generator.SwaggerCaseGeneratorService.simple_chat')
    def test_generate_cases_success(self, mock_simple_chat):
        """测试成功生成用例"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        mock_simple_chat.return_value = {
            'role': 'assistant',
            'content': MOCK_AI_RESPONSE
        }

        svc = SwaggerCaseGeneratorService()
        result = svc.generate_cases(
            swagger_content=json.dumps(SAMPLE_SWAGGER_JSON),
            content_type='json',
        )

        assert 'spec_info' in result
        assert result['spec_info']['title'] == 'Pet Store API'
        assert result['endpoints_count'] == 4
        assert len(result['generated_cases']) == 6
        assert result['summary']['total_cases'] == 6
        assert result['summary']['by_category']['normal'] == 2
        assert result['summary']['by_category']['boundary'] == 2
        assert result['summary']['by_category']['error'] == 2
        mock_simple_chat.assert_called_once()

    @patch('app.services.ai.swagger_case_generator.SwaggerCaseGeneratorService.simple_chat')
    def test_generate_cases_with_markdown_wrapper(self, mock_simple_chat):
        """测试 AI 返回带 markdown 代码块的响应"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        wrapped_response = f"```json\n{MOCK_AI_RESPONSE}\n```"
        mock_simple_chat.return_value = {
            'role': 'assistant',
            'content': wrapped_response
        }

        svc = SwaggerCaseGeneratorService()
        result = svc.generate_cases(
            swagger_content=json.dumps(SAMPLE_SWAGGER_JSON),
        )

        assert len(result['generated_cases']) == 6

    def test_generate_cases_empty_paths(self):
        """测试空路径时抛出异常"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        with pytest.raises(ValueError, match='未找到可用的 API 接口'):
            svc.generate_cases(
                swagger_content=json.dumps({"paths": {}}),
            )

    def test_parse_cases_response_invalid_json(self):
        """测试解析无效 JSON 响应"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        cases = svc._parse_cases_response('this is not json at all')
        assert cases == []

    def test_parse_cases_response_with_extra_text(self):
        """测试解析带额外文本的 JSON 响应"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        response_text = (
            "Here are the generated test cases:\n"
            '[{"method": "GET", "url": "/test", "name": "test"}]'
        )
        cases = svc._parse_cases_response(response_text)
        assert len(cases) == 1
        assert cases[0]['method'] == 'GET'


class TestApiEndpoint:
    """API 端点测试"""

    def _get_auth_header(self, client, app):
        """获取认证 header"""
        import uuid
        with app.app_context():
            from app.extensions import db
            from app.models.user import User
            from werkzeug.security import generate_password_hash

            username = f'swagger_test_{uuid.uuid4().hex[:8]}'
            user = User(
                username=username,
                email=f'{username}@test.com',
                password_hash=generate_password_hash('test123'),
                role='admin',
            )
            db.session.add(user)
            db.session.commit()

        resp = client.post('/api/v1/auth/login', json={
            'username': username,
            'password': 'test123',
        })
        token = resp.get_json().get('data', {}).get('access_token', '')
        return {'Authorization': f'Bearer {token}'}

    def test_generate_cases_empty_content(self, client, app):
        """测试空 swagger_content 返回 400"""
        headers = self._get_auth_header(client, app)
        resp = client.post('/api/v1/ai/generate-cases-from-swagger', json={
            'swagger_content': '',
        }, headers=headers)
        assert resp.status_code == 400

    def test_generate_cases_invalid_content_type(self, client, app):
        """测试无效 content_type 返回 400"""
        headers = self._get_auth_header(client, app)
        resp = client.post('/api/v1/ai/generate-cases-from-swagger', json={
            'swagger_content': '{}',
            'content_type': 'xml',
        }, headers=headers)
        assert resp.status_code == 400

    def test_generate_cases_invalid_swagger(self, client, app):
        """测试无效 Swagger 内容返回 400"""
        headers = self._get_auth_header(client, app)
        resp = client.post('/api/v1/ai/generate-cases-from-swagger', json={
            'swagger_content': 'not a swagger',
            'content_type': 'json',
        }, headers=headers)
        assert resp.status_code == 400

    def test_generate_cases_success(self, client, app):
        """测试成功生成用例（mock AI）"""
        headers = self._get_auth_header(client, app)

        with patch('app.api.swagger_gen.swagger_case_generator.generate_cases') as mock_gen:
            mock_gen.return_value = {
                'spec_info': {'title': 'Test API', 'version': '1.0', 'description': ''},
                'endpoints_count': 2,
                'generated_cases': [
                    {
                        'name': 'Test Case 1',
                        'method': 'GET',
                        'url': '/test',
                        'category': 'normal',
                        'priority': 2,
                    }
                ],
                'summary': {'total_cases': 1, 'by_category': {'normal': 1, 'boundary': 0, 'error': 0}, 'by_method': {'GET': 1}},
            }

            resp = client.post('/api/v1/ai/generate-cases-from-swagger', json={
                'swagger_content': json.dumps(SAMPLE_SWAGGER_JSON),
            }, headers=headers)

            assert resp.status_code == 200
            data = resp.get_json()
            assert data['data']['summary']['total_cases'] == 1

    def test_save_cases_empty(self, client, app):
        """测试保存空用例列表返回 400"""
        headers = self._get_auth_header(client, app)
        resp = client.post('/api/v1/ai/generate-cases-from-swagger/save', json={
            'cases': [],
            'project_id': 1,
        }, headers=headers)
        assert resp.status_code == 400

    def test_save_cases_no_project(self, client, app):
        """测试保存时缺少 project_id 返回 400"""
        headers = self._get_auth_header(client, app)
        resp = client.post('/api/v1/ai/generate-cases-from-swagger/save', json={
            'cases': [{'method': 'GET', 'url': '/test', 'name': 'test'}],
        }, headers=headers)
        assert resp.status_code == 400

    def test_save_cases_to_db(self, client, app):
        """测试将用例保存到数据库"""
        headers = self._get_auth_header(client, app)

        # 先创建一个项目
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            project = Project(name='Test Project', description='test', owner_id=1)
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        resp = client.post('/api/v1/ai/generate-cases-from-swagger/save', json={
            'cases': [
                {
                    'name': 'Test Case 1',
                    'description': 'Test',
                    'method': 'GET',
                    'url': '{baseUrl}/api/test',
                    'headers': {'Accept': 'application/json'},
                    'params': {'limit': '10'},
                    'body': None,
                    'body_type': None,
                    'expected_status': 200,
                    'expected_contains': [],
                    'priority': 2,
                    'category': 'normal',
                    'tags': ['test'],
                },
                {
                    'name': 'Test Case 2',
                    'description': 'Error test',
                    'method': 'POST',
                    'url': '{baseUrl}/api/test',
                    'headers': {'Content-Type': 'application/json'},
                    'params': {},
                    'body': {'name': ''},
                    'body_type': 'json',
                    'expected_status': 400,
                    'expected_contains': ['error'],
                    'priority': 1,
                    'category': 'error',
                    'tags': ['test'],
                }
            ],
            'project_id': project_id,
            'collection_name': 'AI Test Cases',
        }, headers=headers)

        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['saved_count'] == 2

        # 验证数据库中的用例
        with app.app_context():
            from app.models.api_test_case import ApiTestCase, ApiTestCollection
            cases = ApiTestCase.query.filter_by(project_id=project_id).all()
            assert len(cases) == 2
            assert cases[0].method == 'GET'
            assert cases[1].method == 'POST'
            assert 'ai-generated' in cases[0].tags
            assert 'ai-gen:normal' in cases[0].tags
            assert 'ai-gen:error' in cases[1].tags


class TestPromptFormatting:
    """Prompt 格式化功能测试"""

    def test_format_endpoint_for_prompt(self):
        """测试接口信息格式化"""
        from app.services.ai.swagger_case_generator import SwaggerCaseGeneratorService

        svc = SwaggerCaseGeneratorService()
        endpoint = {
            'method': 'POST',
            'path': '/pets',
            'summary': 'Create a pet',
            'description': 'Creates a new pet',
            'tags': ['pets'],
            'parameters': [
                {'name': 'petId', 'in': 'path', 'required': True, 'type': 'integer'}
            ],
            'request_body': {'required': True, 'schema': {'type': 'object'}},
            'responses': {'201': 'Created', '400': 'Bad Request'},
        }

        text = svc._format_endpoint_for_prompt(endpoint)
        assert 'POST' in text
        assert '/pets' in text
        assert 'Create a pet' in text
        assert 'petId' in text
        assert '201' in text
