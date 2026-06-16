"""
OpenAPI 文档自动生成测试

覆盖：Schema 生成、Postman 导出、MeterSphere 导出、
     API 统计、Schema 增强、认证说明
"""
from unittest.mock import patch, MagicMock


# ══════════════════════════════════════════════════════════════════════════════
# 一、Schema 增强测试
# ══════════════════════════════════════════════════════════════════════════════

class TestSchemaEnhancement:
    """OpenAPI Schema 增强测试"""

    def test_enhance_adds_auth_description(self):
        from app.api.v2.openapi_docs import _enhance_openapi_schema
        schema = {
            "info": {"title": "Test", "version": "1.0", "description": "Base desc"},
            "paths": {},
        }
        enhanced = _enhance_openapi_schema(schema)
        assert "Authentication" in enhanced["info"]["description"]
        assert "JWT Bearer Token" in enhanced["info"]["description"]
        assert "API Token" in enhanced["info"]["description"]

    def test_enhance_adds_security_schemes(self):
        from app.api.v2.openapi_docs import _enhance_openapi_schema
        schema = {"info": {"description": ""}, "paths": {}}
        enhanced = _enhance_openapi_schema(schema)
        schemes = enhanced["components"]["securitySchemes"]
        assert "BearerAuth" in schemes
        assert "ApiToken" in schemes
        assert schemes["BearerAuth"]["type"] == "http"
        assert schemes["BearerAuth"]["scheme"] == "bearer"

    def test_enhance_adds_error_response_schema(self):
        from app.api.v2.openapi_docs import _enhance_openapi_schema
        schema = {"info": {"description": ""}, "paths": {}}
        enhanced = _enhance_openapi_schema(schema)
        schemas = enhanced["components"]["schemas"]
        assert "ErrorResponse" in schemas
        assert "code" in schemas["ErrorResponse"]["properties"]
        assert "message" in schemas["ErrorResponse"]["properties"]

    def test_enhance_preserves_existing_data(self):
        from app.api.v2.openapi_docs import _enhance_openapi_schema
        schema = {
            "info": {"title": "My API", "version": "2.0", "description": "Existing"},
            "paths": {"/test": {"get": {"summary": "Test"}}},
            "components": {"securitySchemes": {"ExistingScheme": {"type": "apiKey"}}},
        }
        enhanced = _enhance_openapi_schema(schema)
        assert enhanced["info"]["title"] == "My API"
        assert "/test" in enhanced["paths"]
        assert "ExistingScheme" in enhanced["components"]["securitySchemes"]


# ══════════════════════════════════════════════════════════════════════════════
# 二、Postman 导出测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPostmanExport:
    """Postman Collection 导出测试"""

    def test_generate_postman_collection(self):
        from app.api.v2.openapi_docs import _generate_postman_collection
        schema = {
            "info": {"description": "Test API"},
            "paths": {
                "/api/v2/auth/login": {
                    "post": {
                        "summary": "Login",
                        "description": "User login",
                        "tags": ["auth"],
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "properties": {
                                            "username": {"type": "string"},
                                            "password": {"type": "string"},
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "properties": {
                                                "access_token": {"type": "string"},
                                            }
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
            },
        }
        collection = _generate_postman_collection(schema)
        assert collection["info"]["name"] == "FullScopeTest API v2"
        assert collection["auth"]["type"] == "bearer"
        assert len(collection["item"]) >= 1

    def test_postman_collection_has_auth(self):
        from app.api.v2.openapi_docs import _generate_postman_collection
        schema = {"info": {"description": ""}, "paths": {}}
        collection = _generate_postman_collection(schema)
        assert collection["auth"]["type"] == "bearer"
        assert "base_url" in [v["key"] for v in collection["variable"]]


# ══════════════════════════════════════════════════════════════════════════════
# 三、MeterSphere 导出测试
# ══════════════════════════════════════════════════════════════════════════════

class TestMeterSphereExport:
    """MeterSphere 格式导出测试"""

    def test_generate_metersphere_format(self):
        from app.api.v2.openapi_docs import _generate_metersphere_format
        schema = {
            "info": {"description": "Test"},
            "paths": {
                "/api/v2/test": {
                    "get": {
                        "summary": "Test endpoint",
                        "tags": ["test"],
                        "parameters": [
                            {"name": "page", "in": "query", "required": False, "schema": {"type": "integer"}},
                        ],
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            },
            "components": {"schemas": {}},
        }
        result = _generate_metersphere_format(schema)
        assert result["project_name"] == "FullScopeTest"
        assert len(result["modules"]) >= 1
        assert "import_time" in result

    def test_metersphere_has_assertions(self):
        from app.api.v2.openapi_docs import _generate_metersphere_format
        schema = {
            "info": {"description": ""},
            "paths": {
                "/test": {
                    "post": {
                        "summary": "Create",
                        "tags": ["test"],
                        "responses": {"201": {"description": "Created"}},
                    }
                }
            },
            "components": {"schemas": {}},
        }
        result = _generate_metersphere_format(schema)
        apis = result["modules"][0]["apis"]
        assert len(apis) >= 1
        assert len(apis[0]["assertions"]) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# 四、Pydantic Schema 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPydanticSchemas:
    """Pydantic Schema 验证测试"""

    def test_project_create_schema(self):
        from app.schemas.common import ProjectCreate
        project = ProjectCreate(name="Test Project", description="Desc")
        assert project.name == "Test Project"

    def test_project_create_requires_name(self):
        from app.schemas.common import ProjectCreate
        import pytest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            ProjectCreate()

    def test_test_case_create_schema(self):
        from app.schemas.common import TestCaseCreate
        case = TestCaseCreate(
            name="Test", method="GET", url="https://example.com", project_id=1,
        )
        assert case.name == "Test"
        assert case.project_id == 1

    def test_comment_create_schema(self):
        from app.schemas.common import CommentCreate
        comment = CommentCreate(
            resource_type="test_case", resource_id=1, content="Hello",
        )
        assert comment.resource_type == "test_case"

    def test_error_response_schema(self):
        from app.schemas.common import ErrorResponse
        error = ErrorResponse(code=400, message="Bad request")
        assert error.code == 400
        assert error.timestamp is not None

    def test_test_plan_create_schema(self):
        from app.schemas.common import TestPlanCreate
        plan = TestPlanCreate(name="Plan", project_id=1)
        assert plan.name == "Plan"

    def test_api_response_schema(self):
        from app.schemas.common import ApiResponse
        resp = ApiResponse(code=200, message="ok", data={"key": "val"})
        assert resp.code == 200


# ══════════════════════════════════════════════════════════════════════════════
# 五、OpenAPI Tags 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestOpenAPITags:
    """OpenAPI Tags 定义测试"""

    def test_tags_defined(self):
        from app.api.v2.openapi_docs import OPENAPI_TAGS
        assert len(OPENAPI_TAGS) >= 5
        tag_names = [t["name"] for t in OPENAPI_TAGS]
        assert "auth" in tag_names
        assert "test-cases" in tag_names
        assert "api-tests" in tag_names

    def test_tags_have_descriptions(self):
        from app.api.v2.openapi_docs import OPENAPI_TAGS
        for tag in OPENAPI_TAGS:
            assert "name" in tag
            assert "description" in tag
            assert len(tag["description"]) > 10