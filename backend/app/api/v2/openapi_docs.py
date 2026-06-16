# This file will be written using a different approach
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from ...core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["openapi-docs"])

OPENAPI_TAGS = [
    {"name": "auth", "description": "用户认证与授权\n\n提供用户注册、登录、Token 刷新等认证相关接口。\n所有需要认证的接口必须在 Header 中携带 `Authorization: Bearer <token>`。"},
    {"name": "test-cases", "description": "接口测试用例管理\n\n管理 API 测试用例和测试集合的 CRUD 操作。\n支持按项目和集合分组管理测试用例。"},
    {"name": "api-tests", "description": "接口测试执行\n\n执行 HTTP 接口测试，支持单个用例执行和批量集合执行。\n通过 WebSocket 实时推送执行日志。"},
    {"name": "ui-tests", "description": "Web UI 自动化测试\n\n基于 Playwright 的 Web UI 测试执行与结果查询。\n支持视觉回归测试（截图对比）。"},
    {"name": "perf-tests", "description": "性能测试\n\n基于 Locust 的性能测试管理，支持场景配置、执行、实时指标流、历史对比和告警规则。\n通过 WebSocket 实时推送性能指标。"},
    {"name": "openapi-docs", "description": "OpenAPI 文档工具\n\n提供 API 文档导出功能，支持 Postman Collection 和 MeterSphere 格式导入。"},
]

def _build_postman_request(method, path, summary, description="", body_example=None, headers=None):
    url_parts = path.split("/")
    url_obj = {"raw": "{{base_url}}" + path, "host": ["{{base_url}}"], "path": [p for p in url_parts if p]}
    req = {"method": method.upper(), "header": headers or [{"key": "Content-Type", "value": "application/json"}, {"key": "Authorization", "value": "Bearer {{access_token}}"}], "url": url_obj, "description": description or summary}
    if body_example and method.upper() in ("POST", "PUT", "PATCH"):
        req["body"] = {"mode": "raw", "raw": json.dumps(body_example, indent=2, ensure_ascii=False), "options": {"raw": {"language": "json"}}}
    return req

def _generate_postman_collection(openapi_schema):
    paths = openapi_schema.get("paths", {})
    items = []
    for path, methods in sorted(paths.items()):
        for method, details in methods.items():
            if method in ("get", "post", "put", "patch", "delete"):
                summary = details.get("summary", "")
                description = details.get("description", "")
                tags = details.get("tags", ["default"])
                tag_name = tags[0] if tags else "default"
                body_example = None
                request_body = details.get("requestBody", {})
                content = request_body.get("content", {})
                json_content = content.get("application/json", {})
                schema = json_content.get("schema", {})
                if "$ref" in schema:
                    ref_name = schema["$ref"].split("/")[-1]
                    schemas = openapi_schema.get("components", {}).get("schemas", {})
                    if ref_name in schemas:
                        schema = schemas[ref_name]
                properties = schema.get("properties", {})
                if properties:
                    body_example = {k: "<" + v.get("type", "string") + ">" for k, v in properties.items()}
                req = _build_postman_request(method.upper(), path, summary, description, body_example)
                # Add response examples based on OpenAPI responses
                responses = details.get("responses", {})
                response_list = []
                for status_code, resp_def in responses.items():
                    resp_example = {
                        "name": resp_def.get("description", f"Response {status_code}"),
                        "status": int(status_code) if status_code.isdigit() else 200,
                        "_postman_previewlanguage": "json",
                    }
                    resp_content = resp_def.get("content", {})
                    resp_json = resp_content.get("application/json", {})
                    resp_schema = resp_json.get("schema", {})
                    if resp_schema:
                        if "$ref" in resp_schema:
                            ref_name = resp_schema["$ref"].split("/")[-1]
                            all_schemas = openapi_schema.get("components", {}).get("schemas", {})
                            if ref_name in all_schemas:
                                resp_schema = all_schemas[ref_name]
                        resp_properties = resp_schema.get("properties", {})
                        if resp_properties:
                            resp_example["body"] = json.dumps({k: "<" + v.get("type", "string") + ">" for k, v in resp_properties.items()}, indent=2)
                    response_list.append(resp_example)
                item = {"name": summary or path, "request": req, "response": response_list}
                items.append({"name": tag_name, "item": [item]})
    grouped = {}
    for item in items:
        tag = item["name"]
        if tag not in grouped:
            grouped[tag] = []
        grouped[tag].extend(item["item"])
    grouped_items = [{"name": tag, "item": tag_items} for tag, tag_items in sorted(grouped.items())]
    return {"info": {"name": "FullScopeTest API v2", "description": openapi_schema.get("info", {}).get("description", "") + "\n\n## Authentication\nAll endpoints require Bearer token authentication except for login and register.", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json", "_exporter_id": "fullscopetest"}, "auth": {"type": "bearer", "bearer": [{"key": "token", "value": "{{access_token}}", "type": "string"}]}, "variable": [{"key": "base_url", "value": "http://localhost:8000", "type": "string"}, {"key": "access_token", "value": "", "type": "string"}], "item": grouped_items}

def _generate_metersphere_format(openapi_schema):
    paths = openapi_schema.get("paths", {})
    schemas = openapi_schema.get("components", {}).get("schemas", {})
    modules = []
    for path, methods in sorted(paths.items()):
        for method, details in methods.items():
            if method in ("get", "post", "put", "patch", "delete"):
                summary = details.get("summary", "")
                description = details.get("description", "")
                tags = details.get("tags", ["default"])
                tag_name = tags[0] if tags else "default"
                parameters = []
                for param in details.get("parameters", []):
                    parameters.append({"name": param.get("name", ""), "in": param.get("in", "query"), "required": param.get("required", False), "description": param.get("description", ""), "type": param.get("schema", {}).get("type", "string")})
                request_body_schema = {}
                request_body = details.get("requestBody", {})
                content = request_body.get("content", {})
                json_content = content.get("application/json", {})
                schema_ref = json_content.get("schema", {})
                if "$ref" in schema_ref:
                    ref_name = schema_ref["$ref"].split("/")[-1]
                    if ref_name in schemas:
                        schema_def = schemas[ref_name]
                        properties = schema_def.get("properties", {})
                        required_fields = schema_def.get("required", [])
                        for field_name, field_def in properties.items():
                            request_body_schema[field_name] = {"type": field_def.get("type", "string"), "description": field_def.get("description", ""), "required": field_name in required_fields, "example": field_def.get("example", "")}
                responses = {}
                for status_code, resp_def in details.get("responses", {}).items():
                    resp_content = resp_def.get("content", {})
                    resp_json = resp_content.get("application/json", {})
                    resp_schema = resp_json.get("schema", {})
                    resp_desc = resp_def.get("description", "")
                    # Add common response descriptions
                    status_desc_map = {"200": "请求成功", "201": "创建成功", "400": "请求参数错误", "401": "未授权访问", "403": "禁止访问", "404": "资源不存在", "500": "服务器内部错误"}
                    if not resp_desc and status_code in status_desc_map:
                        resp_desc = status_desc_map[status_code]
                    responses[status_code] = {"description": resp_desc, "schema": resp_schema}
                # Add default assertions for common status codes
                assertions = []
                if "200" in details.get("responses", {}):
                    assertions.append({"type": "status", "expression": "", "comparison": "equals", "value": "200", "description": "验证返回状态码为 200"})
                elif "201" in details.get("responses", {}):
                    assertions.append({"type": "status", "expression": "", "comparison": "equals", "value": "201", "description": "验证返回状态码为 201"})
                api_def = {"id": f"{method}_{path.replace(chr(47), chr(95)).strip(chr(95))}", "name": summary or f"{method.upper()} {path}", "description": description, "method": method.upper(), "path": path, "headers": [{"name": "Content-Type", "value": "application/json"}, {"name": "Authorization", "value": "Bearer {{token}}"}], "parameters": parameters, "body": request_body_schema, "responses": responses, "assertions": assertions, "tags": tags, "sort_order": 0}
                modules.append({"name": tag_name, "apis": [api_def]})
    merged = {}
    for mod in modules:
        tag = mod["name"]
        if tag not in merged:
            merged[tag] = {"name": tag, "apis": []}
        merged[tag]["apis"].extend(mod["apis"])
    return {"project_name": "FullScopeTest", "version": "2.0.0", "description": openapi_schema.get("info", {}).get("description", ""), "modules": list(merged.values()), "import_time": datetime.utcnow().isoformat() + "Z"}

@router.get("/openapi/postman", summary="导出 Postman Collection", description="将当前 OpenAPI schema 转换为 Postman Collection v2.1 格式。", response_class=JSONResponse)
async def export_postman_collection():
    from ...fastapi_app import create_fastapi_app
    app = create_fastapi_app("production")
    openapi_schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    collection = _generate_postman_collection(openapi_schema)
    return JSONResponse(content=collection, headers={"Content-Disposition": "attachment; filename=fullscopetest-api-v2.postman_collection.json"})

@router.get("/openapi/metersphere", summary="导出 MeterSphere 兼容格式", description="将当前 OpenAPI schema 转换为 MeterSphere 可导入的接口定义格式。", response_class=JSONResponse)
async def export_metersphere_format():
    from ...fastapi_app import create_fastapi_app
    app = create_fastapi_app("production")
    openapi_schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    ms_format = _generate_metersphere_format(openapi_schema)
    return JSONResponse(content=ms_format, headers={"Content-Disposition": "attachment; filename=fullscopetest-api-v2.metersphere.json"})

@router.get("/openapi/schema", summary="获取完整 OpenAPI Schema", description="返回当前 FastAPI 应用的完整 OpenAPI 3.0 Schema。", response_class=JSONResponse)
async def get_full_openapi_schema():
    from ...fastapi_app import create_fastapi_app
    app = create_fastapi_app("production")
    schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    # 增强 schema：添加认证说明和示例
    schema = _enhance_openapi_schema(schema)
    return schema

@router.get("/openapi/stats", summary="获取 API 统计信息", description="返回当前 API 的端点数量、标签分布、认证方式等统计信息。")
async def get_api_stats():
    from ...fastapi_app import create_fastapi_app
    app = create_fastapi_app("production")
    openapi_schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    paths = openapi_schema.get("paths", {})
    total_endpoints = 0
    tag_counts = {}
    method_counts = {}
    for path, methods in paths.items():
        for method, details in methods.items():
            if method in ("get", "post", "put", "patch", "delete"):
                total_endpoints += 1
                method_counts[method.upper()] = method_counts.get(method.upper(), 0) + 1
                for tag in details.get("tags", ["default"]):
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return {"total_endpoints": total_endpoints, "by_method": method_counts, "by_tag": tag_counts, "security_schemes": list(openapi_schema.get("components", {}).get("securitySchemes", {}).keys()), "version": openapi_schema.get("info", {}).get("version", "unknown")}


def _enhance_openapi_schema(schema: dict) -> dict:
    """
    增强 OpenAPI Schema

    添加认证说明、安全方案、通用响应示例。
    """
    # 增强 API 描述
    enhanced_description = (
        schema.get("info", {}).get("description", "") +
        "\n\n## Authentication\n\n" +
        "All endpoints require authentication via one of:\n\n" +
        "1. **JWT Bearer Token** - Obtained via `/api/v2/auth/login`. "
        "Include `Authorization: Bearer <token>` header.\n" +
        "2. **API Token** - Created via `/api/v1/tokens`. "
        "Include `Authorization: Bearer <api_token>` header.\n\n" +
        "Some endpoints (login, register) are public and do not require authentication."
    )
    schema.setdefault("info", {})["description"] = enhanced_description

    # 添加安全方案
    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT Bearer Token from /api/v2/auth/login",
    }
    schema["components"]["securitySchemes"]["ApiToken"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "API Token",
        "description": "API Token from /api/v1/tokens",
    }

    # 添加通用错误响应 schema
    schema["components"].setdefault("schemas", {})
    schema["components"]["schemas"]["ErrorResponse"] = {
        "type": "object",
        "properties": {
            "code": {"type": "integer", "description": "HTTP status code"},
            "message": {"type": "string", "description": "Error message"},
            "errors": {"type": "object", "description": "Detailed errors"},
            "timestamp": {"type": "string", "format": "date-time"},
        },
    }

    return schema
