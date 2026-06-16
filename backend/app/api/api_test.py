"""
接口测试模块 - API
实现接口测试相关功能：用例管理、执行测试、结果存储
"""

from flask import request, current_app, Response, make_response
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.api_test_case import ApiTestCollection, ApiTestCase
from ..models.environment import Environment
from ..models.project import Project
from ..models.test_run import TestRun
from ..models.test_report import TestReport
from ..utils.response import success_response, error_response
from ..utils.validators import validate_required
from ..utils import get_current_user_id
from ..utils.ai_planner import generate_api_test_plan
from ..utils.ai_data_synthesizer import synthesize_test_cases
from ..utils.ai_reviewer import review_api_collection
from ..core.logging import get_logger
import time
from datetime import datetime

# 导入 Service 层
from ..services.api_collection_service import ApiCollectionService
from ..services.api_case_service import ApiCaseService
from ..services.api_execution_service import ApiExecutionService
from ..services.ai_config_service import AiConfigService
from ..utils.exceptions import AppError, NotFoundError, ValidationError, PermissionError


logger = get_logger(__name__)


# 初始化 Service 实例
collection_service = ApiCollectionService()
case_service = ApiCaseService()
execution_service = ApiExecutionService()
ai_config_service = AiConfigService()


def _build_ai_runtime_config(data: dict, *, timeout: int = 30) -> dict:
    """从 Flask config 和请求 data 中构建 AI runtime_config，支持前端 per-request 覆盖。"""
    from flask import current_app
    runtime_config = {
        "AI_ASSISTANT_ENABLED": current_app.config.get("AI_ASSISTANT_ENABLED", True),
        "AI_ASSISTANT_BASE_URL": current_app.config.get("AI_ASSISTANT_BASE_URL", ""),
        "AI_ASSISTANT_API_KEY": current_app.config.get("AI_ASSISTANT_API_KEY", ""),
        "AI_ASSISTANT_MODEL": current_app.config.get("AI_ASSISTANT_MODEL", ""),
        "AI_VISION_BASE_URL": current_app.config.get("AI_VISION_BASE_URL", ""),
        "AI_VISION_API_KEY": current_app.config.get("AI_VISION_API_KEY", ""),
        "AI_VISION_MODEL": current_app.config.get("AI_VISION_MODEL", ""),
        "AI_ASSISTANT_TIMEOUT": current_app.config.get("AI_ASSISTANT_TIMEOUT", timeout),
    }
    # Frontend runtime override
    if data.get("base_url"):
        runtime_config["AI_ASSISTANT_BASE_URL"] = str(data.get("base_url")).strip()
    if data.get("model"):
        runtime_config["AI_ASSISTANT_MODEL"] = str(data.get("model")).strip()
    if data.get("api_key"):
        runtime_config["AI_ASSISTANT_API_KEY"] = str(data.get("api_key")).strip()
    if data.get("vision_base_url"):
        runtime_config["AI_VISION_BASE_URL"] = str(data.get("vision_base_url")).strip()
    if data.get("vision_model"):
        runtime_config["AI_VISION_MODEL"] = str(data.get("vision_model")).strip()
    if data.get("vision_api_key"):
        runtime_config["AI_VISION_API_KEY"] = str(data.get("vision_api_key")).strip()
    return runtime_config


@api_bp.route("/api-test/health", methods=["GET"])
def api_test_health():
    """接口测试模块健康检查"""
    return success_response(message="接口测试模块正常")


@api_bp.route("/api-test/ai/config", methods=["GET"])
@jwt_required()
def get_ai_config():
    """Get the current global AI assistant configuration"""
    try:
        config = ai_config_service.get_config()
        return success_response(data=config, message="AI configuration fetched")
    except Exception as exc:
        logger.error("get ai config failed", error=str(exc))
        return error_response(500, f"获取 AI 配置失败: {str(exc)}")


@api_bp.route("/api-test/ai/config", methods=["POST"])
@jwt_required()
def save_ai_config():
    data = request.get_json() or {}
    try:
        result = ai_config_service.save_config(data)
        if not result["success"]:
            return error_response(400, result["error"])
        return success_response(data=result["data"], message="AI 配置已保存到 .env")
    except Exception as exc:
        logger.error("save ai config failed", error=str(exc))
        return error_response(500, f"保存 AI 配置失败: {str(exc)}")


@api_bp.route("/api-test/ai/plan", methods=["POST"])
@jwt_required()
def generate_ai_plan():
    """Generate AI operations plan for API workspace."""
    user_id = get_current_user_id()
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()

    if not prompt:
        return error_response(400, "prompt is required")

    collections = ApiTestCollection.query.filter_by(user_id=user_id).all()
    cases = (
        ApiTestCase.query
        .filter_by(user_id=user_id)
        .order_by(ApiTestCase.updated_at.desc())
        .limit(200)
        .all()
    )
    projects = Project.query.filter_by(owner_id=user_id).all()
    project_ids = [p.id for p in projects]
    envs = []
    if project_ids:
        envs = Environment.query.filter(Environment.project_id.in_(project_ids)).all()

    context = {
        "selected_collection_id": data.get("collection_id"),
        "selected_case_id": data.get("case_id"),
        "selected_env_id": data.get("environment_id"),
        "project_id": data.get("project_id"),
        "collections": [
            {"id": c.id, "name": c.name, "project_id": c.project_id}
            for c in collections
        ],
        "cases": [
            {
                "id": c.id,
                "name": c.name,
                "method": c.method,
                "url": c.url,
                "collection_id": c.collection_id,
                "environment_id": c.environment_id,
            }
            for c in cases
        ],
        "environments": [
            {
                "id": e.id,
                "name": e.name,
                "project_id": e.project_id,
                "base_url": e.base_url,
            }
            for e in envs
        ],
    }

    try:
        runtime_config = _build_ai_runtime_config(data)
        plan = generate_api_test_plan(prompt=prompt, context=context, config=runtime_config)
        return success_response(data=plan, message="AI plan generated")
    except ValueError as exc:
        return error_response(400, str(exc))
    except Exception as exc:
        logger.error("AI plan generation failed", error=str(exc), exc_info=True)
        return error_response(500, f"AI plan generation failed: {str(exc)}")


@api_bp.route("/api-test/ai/synthesize-cases", methods=["POST"])
@jwt_required()
def synthesize_api_cases():
    """AI 智能扩充接口测试用例"""
    data = request.get_json() or {}
    base_request = data.get("base_request")
    count = data.get("count", 5)

    if not base_request:
        return error_response(400, "base_request is required")

    try:
        runtime_config = _build_ai_runtime_config(data)
        cases = synthesize_test_cases(base_request, count, runtime_config)
        return success_response(data={"cases": cases}, message="AI 用例扩充成功")
    except Exception as exc:
        return error_response(500, f"AI 用例扩充失败: {str(exc)}")


@api_bp.route("/api-test/ai/review-collection", methods=["POST"])
@jwt_required()
def review_collection_cases():
    """AI 智能评审测试用例集合并补充用例"""
    user_id = get_current_user_id()
    data = request.get_json() or {}
    collection_id = data.get("collection_id")

    if not collection_id:
        return error_response(400, "collection_id is required")

    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
    if not collection:
        return error_response(404, "集合不存在")

    cases = ApiTestCase.query.filter_by(collection_id=collection_id, user_id=user_id).all()
    if not cases:
        return error_response(400, "该集合下没有测试用例，无法评审")

    case_list = []
    for c in cases:
        case_list.append({
            "name": c.name,
            "method": c.method,
            "url": c.url,
            "headers": c.headers,
            "params": c.params,
            "body": c.body,
            "body_type": c.body_type,
        })

    try:
        runtime_config = _build_ai_runtime_config(data, timeout=60)
        result = review_api_collection(collection.name, case_list, runtime_config)
        return success_response(data=result, message="AI 评审完成")
    except Exception as exc:
        return error_response(500, f"AI 评审失败: {str(exc)}")



# ==================== 用例集合 ====================


@api_bp.route("/api-test/collections", methods=["GET"])
@jwt_required()
def get_collections():
    """获取用例集合列表"""
    user_id = get_current_user_id()
    project_id = request.args.get("project_id", type=int)
    try:
        data = collection_service.get_collections(user_id, project_id)
        return success_response(data=data)
    except Exception as exc:
        logger.error("get collections failed", error=str(exc))
        return error_response(500, f"获取集合失败: {str(exc)}")


@api_bp.route("/api-test/collections", methods=["POST"])
@jwt_required()
def create_collection():
    """创建用例集合"""
    user_id = get_current_user_id()
    data = request.get_json()

    error = validate_required(data, ["name"])
    if error:
        return error_response(400, error)

    try:
        result = collection_service.create_collection(
            user_id=user_id,
            name=data["name"],
            description=data.get("description", ""),
            project_id=data.get("project_id")
        )
        return success_response(data=result, message="创建成功")
    except Exception as exc:
        logger.error("create collection failed", error=str(exc))
        return error_response(500, f"创建集合失败: {str(exc)}")


@api_bp.route("/api-test/collections/<int:collection_id>", methods=["PUT"])
@jwt_required()
def update_collection(collection_id):
    """更新用例集合"""
    user_id = get_current_user_id()
    data = request.get_json()
    try:
        result = collection_service.update_collection(collection_id, user_id, data)
        return success_response(data=result, message="更新成功")
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error("update collection failed", error=str(exc))
        return error_response(500, f"更新集合失败: {str(exc)}")


@api_bp.route("/api-test/collections/<int:collection_id>", methods=["DELETE"])
@jwt_required()
def delete_collection(collection_id):
    """删除用例集合"""
    user_id = get_current_user_id()
    try:
        collection_service.delete_collection(collection_id, user_id)
        return success_response(message="删除成功")
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error("delete collection failed", error=str(exc))
        return error_response(500, f"删除集合失败: {str(exc)}")



# ==================== 测试用例 ====================


@api_bp.route("/api-test/cases", methods=["GET"])
@jwt_required()
def get_cases():
    """获取测试用例列表"""
    user_id = get_current_user_id()
    collection_id = request.args.get("collection_id", type=int)
    project_id = request.args.get("project_id", type=int)
    try:
        data = case_service.get_cases(user_id, collection_id, project_id)
        return success_response(data=data)
    except Exception as exc:
        logger.error("get cases failed", error=str(exc))
        return error_response(500, f"获取用例失败: {str(exc)}")


@api_bp.route("/api-test/cases", methods=["POST"])
@jwt_required()
def create_case():
    """创建测试用例"""
    user_id = get_current_user_id()
    data = request.get_json()

    try:
        result = case_service.create_case(user_id, data)
        return success_response(data=result, message="创建成功")
    except ValidationError as exc:
        return error_response(400, str(exc))
    except Exception as exc:
        logger.error("create case failed", error=str(exc))
        return error_response(500, f"创建用例失败: {str(exc)}")


@api_bp.route("/api-test/cases/<int:case_id>", methods=["GET"])
@jwt_required()
def get_case(case_id):
    """获取用例详情"""
    user_id = get_current_user_id()
    try:
        result = case_service.get_case(case_id, user_id)
        return success_response(data=result)
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error("get case failed", error=str(exc))
        return error_response(500, f"获取用例失败: {str(exc)}")


@api_bp.route("/api-test/cases/<int:case_id>", methods=["PUT"])
@jwt_required()
def update_case(case_id):
    """更新测试用例"""
    user_id = get_current_user_id()
    data = request.get_json()
    try:
        result = case_service.update_case(case_id, user_id, data)
        return success_response(data=result, message="更新成功")
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error("update case failed", error=str(exc))
        return error_response(500, f"更新用例失败: {str(exc)}")


@api_bp.route("/api-test/cases/<int:case_id>", methods=["DELETE"])
@jwt_required()
def delete_case(case_id):
    """删除测试用例"""
    user_id = get_current_user_id()
    try:
        case_service.delete_case(case_id, user_id)
        return success_response(message="删除成功")
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error("delete case failed", error=str(exc))
        return error_response(500, f"删除用例失败: {str(exc)}")



# ==================== Mock Server ====================


@api_bp.route("/api-test/mock/<int:case_id>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def mock_api_endpoint(case_id):
    """
    Mock Server 端点
    根据用例 ID 返回预设的 Mock 数据
    允许跨域，方便前端直接调用
    """
    # 处理跨域 OPTIONS 请求
    if request.method == "OPTIONS":
        resp = make_response()
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return resp

    case = ApiTestCase.query.get(case_id)

    if not case:
        return error_response(404, "用例不存在")

    if not case.mock_enabled:
        return error_response(400, "该用例未开启 Mock 功能")

    # 模拟延迟
    if case.mock_delay_ms and case.mock_delay_ms > 0:
        time.sleep(case.mock_delay_ms / 1000.0)

    # 构建响应
    resp = make_response(case.mock_response_body or "")
    resp.status_code = case.mock_response_code or 200

    # 设置响应头
    if case.mock_response_headers:
        for k, v in case.mock_response_headers.items():
            resp.headers[k] = v

    # 默认 Content-Type 为 application/json 如果未设置
    if "Content-Type" not in [k.title() for k in (case.mock_response_headers or {}).keys()]:
        resp.headers["Content-Type"] = "application/json"

    # 允许跨域
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


# ==================== 导入导出 ====================

@api_bp.route("/api-test/import/postman", methods=["POST"])
@jwt_required()
def import_postman():
    """
    从 Postman Collection JSON 导入用例

    请求体:
        project_id: 项目 ID (必填)
        collection_id: 集合 ID (可选)
        content: JSON 字符串 (必填)
    """
    from ..services.import_export_service import import_from_postman_json
    user_id = int(get_current_user_id())
    data = request.get_json(silent=True) or {}

    project_id = data.get('project_id')
    if not project_id:
        return error_response(400, '缺少 project_id')

    content = data.get('content', '')
    if not content:
        return error_response(400, '缺少导入内容')

    try:
        results = import_from_postman_json(
            user_id=user_id,
            project_id=project_id,
            json_content=content,
            collection_id=data.get('collection_id'),
        )
        return success_response(data=results, message=f'导入完成: {results["imported"]} 条用例')
    except AppError as e:
        return error_response(e.code, e.message, errors=e.errors)


@api_bp.route("/api-test/import/csv", methods=["POST"])
@jwt_required()
def import_csv():
    """
    从 CSV 格式批量导入用例

    请求体:
        project_id: 项目 ID (必填)
        collection_id: 集合 ID (可选)
        content: CSV 文本 (必填)
    """
    from ..services.import_export_service import import_from_csv
    user_id = int(get_current_user_id())
    data = request.get_json(silent=True) or {}

    project_id = data.get('project_id')
    if not project_id:
        return error_response(400, '缺少 project_id')

    content = data.get('content', '')
    if not content:
        return error_response(400, '缺少导入内容')

    try:
        results = import_from_csv(
            user_id=user_id,
            project_id=project_id,
            csv_content=content,
            collection_id=data.get('collection_id'),
        )
        return success_response(data=results, message=f'导入完成: {results["imported"]} 条用例')
    except AppError as e:
        return error_response(e.code, e.message, errors=e.errors)


@api_bp.route("/api-test/import/template", methods=["GET"])
@jwt_required()
def get_csv_template():
    """获取 CSV 导入模板"""
    from ..services.import_export_service import generate_csv_template
    template = generate_csv_template()
    return success_response(data={'template': template})



# ==================== 执行测试 ====================


@api_bp.route("/api-test/execute", methods=["POST"])
@jwt_required()
def execute_request():
    """
    执行 HTTP 请求（快速测试）

    不保存用例，直接执行并返回结果
    支持环境配置的应用、前置脚本和后置断言
    """
    user_id = get_current_user_id()
    data = request.get_json()

    error = validate_required(data, ["method", "url"])
    if error:
        return error_response(400, error)

    try:
        result = execution_service.execute_request(data, user_id)
        if result.get("success", True):
            return success_response(data=result)
        else:
            return error_response(
                result.get("status_code", 400),
                result.get("error", "请求执行失败"),
                errors=result.get("script_execution")
            )
    except Exception as exc:
        logger.error("execute request failed", error=str(exc))
        return error_response(500, f"请求执行失败: {str(exc)}")


@api_bp.route("/api-test/cases/<int:case_id>/run", methods=["POST"])
@jwt_required()
def run_case(case_id):
    """执行单个测试用例（支持前置脚本和后置断言）"""
    user_id = get_current_user_id()
    env_id = request.args.get("env_id", type=int)

    try:
        result = execution_service.run_case(case_id, user_id, env_id)
        return success_response(data=result)
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except Exception as exc:
        logger.error("run case failed", error=str(exc))
        return error_response(500, f"执行用例失败: {str(exc)}")


@api_bp.route("/api-test/collections/<int:collection_id>/run", methods=["POST"])
@jwt_required()
def run_collection(collection_id):
    """批量执行集合中的所有用例，并生成测试报告"""
    user_id = get_current_user_id()
    data = request.get_json() or {}
    env_id = data.get("env_id") if "env_id" in data else request.args.get("env_id", type=int)

    try:
        result = execution_service.run_collection(collection_id, user_id, env_id)
        return success_response(data=result, message="测试执行完成")
    except NotFoundError as exc:
        return error_response(404, str(exc))
    except ValidationError as exc:
        return error_response(400, str(exc))
    except PermissionError as exc:
        return error_response(403, str(exc))
    except Exception as exc:
        logger.error("run collection failed", error=str(exc), exc_info=True)
        return error_response(500, f"执行集合失败: {str(exc)}")
