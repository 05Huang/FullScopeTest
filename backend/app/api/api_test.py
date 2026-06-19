"""
接口测试模块 - API
实现接口测试相关功能：用例管理、执行测试、结果存储
"""

from flask import request, current_app, Response, make_response
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.api_test_case import ApiTestCollection, ApiTestCase
from ..utils.org_filter import filter_by_org_projects, filter_by_owner_or_org
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

    collections = filter_by_org_projects(ApiTestCollection.query, ApiTestCollection).filter_by(user_id=user_id).all()
    cases = (
        filter_by_org_projects(ApiTestCase.query, ApiTestCase)
        .filter_by(user_id=user_id)
        .order_by(ApiTestCase.updated_at.desc())
        .limit(200)
        .all()
    )
    projects = filter_by_owner_or_org(Project.query, Project, user_id).all()
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
    """获取测试用例列表（支持多维筛选）"""
    user_id = get_current_user_id()
    collection_id = request.args.get("collection_id", type=int)
    project_id = request.args.get("project_id", type=int)
    method = request.args.get("method")
    url_contains = request.args.get("url_contains")
    tags = request.args.get("tags")
    priority = request.args.get("priority")
    try:
        data = case_service.get_cases(
            user_id, collection_id, project_id,
            method=method, url_contains=url_contains, tags=tags, priority=priority,
        )
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
        # 保存响应历史
        if result.get("success"):
            try:
                from ..models.response_history import ResponseHistory
                history = ResponseHistory(
                    case_id=data.get('case_id'),
                    user_id=user_id,
                    url=data.get('url', ''),
                    method=data.get('method', 'GET').upper(),
                    status_code=result.get('status_code'),
                    response_time=result.get('response_time'),
                    response_size=result.get('response_size'),
                    request_headers=data.get('headers'),
                    response_headers=result.get('headers'),
                    response_body=result.get('body'),
                    environment_id=data.get('env_id'),
                )
                db.session.add(history)
                db.session.commit()
            except Exception:
                db.session.rollback()
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


@api_bp.route("/api-test/runs/<int:run_id>/progress", methods=["GET"])
@jwt_required()
def get_run_progress(run_id):
    """获取测试执行进度"""
    try:
        progress = execution_service.get_progress(run_id)
        if progress:
            return success_response(data=progress)
        return success_response(data={'current': 0, 'total': 0, 'passed': 0, 'failed': 0, 'status': 'unknown'})
    except Exception as exc:
        return error_response(500, f"获取进度失败: {str(exc)}")


# ==================== 用例版本历史 ====================

@api_bp.route("/api-test/cases/<int:case_id>/versions", methods=["GET"])
@jwt_required()
def get_case_versions(case_id):
    """
    获取用例的版本历史列表

    查询参数:
        page: 页码 (默认 1)
        per_page: 每页数量 (默认 20)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    try:
        result = case_service.get_versions(case_id, page, per_page)
        return success_response(data=result)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route("/api-test/versions/<int:version_id>", methods=["GET"])
@jwt_required()
def get_version_detail(version_id):
    """获取指定版本详情"""
    try:
        version = case_service.get_version(version_id)
        return success_response(data=version)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route("/api-test/versions/diff", methods=["GET"])
@jwt_required()
def diff_versions():
    """
    对比两个版本的差异

    查询参数:
        v1: 旧版本 ID (必填)
        v2: 新版本 ID (必填)
    """
    v1 = request.args.get('v1', type=int)
    v2 = request.args.get('v2', type=int)

    if not v1 or not v2:
        return error_response(400, '缺少 v1 或 v2 参数')

    try:
        result = case_service.diff_two_versions(v1, v2)
        return success_response(data=result)
    except AppError as e:
        return error_response(e.code, e.message)


import re
import shlex


def parse_curl(curl_command: str) -> dict:
    """
    解析 cURL 命令为结构化数据

    支持：
    - 多行 cURL（\\ 换行）
    - --data-raw、--data-binary、-d 等变体
    - --compressed 参数（忽略）
    - 单引号和双引号

    Args:
        curl_command: cURL 命令字符串

    Returns:
        dict: {method, url, headers, body}

    Raises:
        ValueError: 解析失败时返回具体错误位置
    """
    # 预处理：合并多行（去除 \ 换行）
    curl_command = curl_command.strip()
    if not curl_command:
        raise ValueError("cURL 命令为空")

    # 合续行：将 \ + 换行替换为空格
    curl_command = re.sub(r'\\\s*\n\s*', ' ', curl_command)

    # 去掉开头的 curl 命令
    if curl_command.startswith('curl '):
        curl_command = curl_command[5:]
    elif curl_command == 'curl':
        raise ValueError("cURL 命令缺少参数")

    # 使用 shlex 分词（正确处理引号）
    try:
        tokens = shlex.split(curl_command)
    except ValueError as e:
        raise ValueError(f"cURL 命令格式错误: {e}")

    method = 'GET'
    url = ''
    headers = {}
    body = ''
    data_parts = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token in ('-X', '--request'):
            i += 1
            if i >= len(tokens):
                raise ValueError(f"参数 {token} 缺少值")
            method = tokens[i].upper()

        elif token in ('-H', '--header'):
            i += 1
            if i >= len(tokens):
                raise ValueError(f"参数 {token} 缺少值")
            header_str = tokens[i]
            if ':' in header_str:
                key, value = header_str.split(':', 1)
                headers[key.strip()] = value.strip()

        elif token in ('-d', '--data', '--data-raw', '--data-binary', '--data-urlencode'):
            i += 1
            if i >= len(tokens):
                raise ValueError(f"参数 {token} 缺少值")
            data_parts.append(tokens[i])
            if method == 'GET':
                method = 'POST'

        elif token == '--compressed':
            pass  # 忽略

        elif token.startswith('-'):
            # 未知参数，跳过
            pass

        elif not url and not token.startswith('-'):
            url = token

        i += 1

    if data_parts:
        body = '&'.join(data_parts)

    if not url:
        raise ValueError("cURL 命令中未找到 URL")

    return {
        'method': method,
        'url': url,
        'headers': headers,
        'body': body,
    }


@api_bp.route("/api-test/import-curl", methods=["POST"])
@jwt_required()
def import_curl():
    """
    导入 cURL 命令

    请求体:
        curl: cURL 命令字符串（支持多行）

    返回:
        解析后的请求结构 {method, url, headers, body}
    """
    data = request.get_json()
    curl_command = data.get('curl', '')

    if not curl_command:
        return error_response(400, '缺少 curl 参数')

    try:
        result = parse_curl(curl_command)
        return success_response(data=result)
    except ValueError as e:
        return error_response(400, f'cURL 解析失败: {e}')


@api_bp.route('/api-test/execute-scenario', methods=['POST'])
@jwt_required()
def execute_scenario():
    """
    执行场景编排（多步骤链式请求）

    请求体:
        steps: 步骤定义列表
        env_id: 环境 ID（可选）
        base_url: 基础 URL（可选）
        variables: 初始变量（可选）

    返回:
        { total, passed, failed, duration, step_results, variables }
    """
    from ..services.scenario_executor import get_scenario_executor

    current_user = get_jwt_identity()
    data = request.get_json()
    steps = data.get('steps', [])

    if not steps:
        return error_response(400, '缺少步骤定义')

    # 获取环境变量
    env_vars = {}
    env_id = data.get('env_id')
    if env_id:
        from ..models.environment import Environment
        env = Environment.query.filter_by(id=env_id).first()
        if env:
            env_vars = env.variables or {}

    try:
        executor = get_scenario_executor()
        result = executor.execute_scenario(steps, {
            'env_vars': env_vars,
            'user_id': current_user,
            'base_url': data.get('base_url', ''),
            'variables': data.get('variables', {}),
        })
        return success_response(data=result)
    except Exception as e:
        from ..core.logging import get_logger
        logger = get_logger(__name__)
        logger.error('场景执行失败', error=str(e))
        return error_response(500, f'场景执行失败: {str(e)}')


@api_bp.route('/api-test/history', methods=['GET'])
@jwt_required()
def get_response_history():
    """
    获取响应历史列表

    查询参数:
        case_id: 用例 ID（可选，不传则获取当前用户所有历史）
        limit: 数量限制（默认 50）
    """
    from ..models.response_history import ResponseHistory

    current_user = get_jwt_identity()
    case_id = request.args.get('case_id', type=int)
    limit = request.args.get('limit', 50, type=int)

    query = ResponseHistory.query.filter_by(user_id=current_user)
    if case_id:
        query = query.filter_by(case_id=case_id)

    histories = query.order_by(ResponseHistory.created_at.desc()).limit(limit).all()
    return success_response(data=[h.to_dict() for h in histories])


@api_bp.route('/api-test/history', methods=['POST'])
@jwt_required()
def save_response_history():
    """
    保存响应历史记录

    请求体: 响应历史数据
    """
    from ..models.response_history import ResponseHistory

    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        history = ResponseHistory(
            case_id=data.get('case_id'),
            user_id=current_user,
            url=data.get('url', ''),
            method=data.get('method', 'GET'),
            status_code=data.get('status_code'),
            response_time=data.get('response_time'),
            response_size=data.get('response_size'),
            request_headers=data.get('request_headers'),
            request_body=data.get('request_body'),
            response_headers=data.get('response_headers'),
            response_body=data.get('response_body'),
            error=data.get('error'),
            environment_id=data.get('environment_id'),
        )
        db.session.add(history)
        db.session.commit()
        return success_response(data=history.to_dict(), message='历史记录已保存', code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(500, f'保存失败: {str(e)}')


@api_bp.route('/api-test/history/trend', methods=['GET'])
@jwt_required()
def get_response_history_trend():
    """
    获取响应时间趋势数据

    查询参数:
        case_id: 用例 ID（必填）
        limit: 数据点数量（默认 30）
    """
    from ..models.response_history import ResponseHistory

    current_user = get_jwt_identity()
    case_id = request.args.get('case_id', type=int)
    limit = request.args.get('limit', 30, type=int)

    if not case_id:
        return error_response(400, '缺少 case_id 参数')

    histories = ResponseHistory.query.filter_by(
        user_id=current_user, case_id=case_id
    ).order_by(ResponseHistory.created_at.desc()).limit(limit).all()

    trend = [{
        'timestamp': h.created_at.isoformat() if h.created_at else None,
        'response_time': h.response_time,
        'status_code': h.status_code,
    } for h in reversed(histories)]

    return success_response(data=trend)


@api_bp.route('/api-test/history/<int:history_id>', methods=['GET'])
@jwt_required()
def get_response_history_detail(history_id):
    """获取响应历史详情"""
    from ..models.response_history import ResponseHistory

    current_user = get_jwt_identity()
    history = ResponseHistory.query.filter_by(id=history_id, user_id=current_user).first()
    if not history:
        return error_response(404, '历史记录不存在')

    return success_response(data=history.to_detail_dict())


@api_bp.route('/api-test/smart-select', methods=['POST'])
@jwt_required()
def smart_test_select():
    """智能测试选择 — 根据变更文件推荐测试用例"""
    from ..services.ai.test_selector_service import get_test_selector_service
    from ..utils import get_current_user_id
    from ..models.project import Project
    from ..utils.org_filter import filter_by_org_projects

    data = request.get_json() or {}
    changed_files = data.get('changed_files', [])
    if not changed_files:
        return error_response(400, '请提供变更文件列表')

    project_id = data.get('project_id')
    tags = data.get('tags', [])
    max_cases = data.get('max_cases', 50)

    # 权限校验：限定用户所属组织的项目
    if project_id:
        current_user = get_current_user_id()
        project = Project.query.get(project_id)
        if not project:
            return error_response(404, '项目不存在')
        # 组织隔离
        from flask import g
        if hasattr(g, 'organization_id') and g.organization_id:
            if project.organization_id and project.organization_id != g.organization_id:
                return error_response(403, '无权访问该项目')

    try:
        selector = get_test_selector_service()
        result = selector.select_tests(
            changed_files=changed_files,
            project_id=project_id,
            tags=tags if tags else None,
            max_cases=max_cases,
        )
        return success_response(data=result, message='智能选测完成')
    except Exception as exc:
        logger.error('智能选测失败', error=str(exc))
        return error_response(500, f'智能选测失败: {str(exc)}')


@api_bp.route('/api-test/heal-case', methods=['POST'])
@jwt_required()
def heal_test_case():
    """AI 用例自愈 — 为失败用例生成修复建议"""
    from ..services.ai.healing_service import HealingService

    data = request.get_json() or {}
    case_id = data.get('case_id')
    failure_info = data.get('failure_info', {})

    if not case_id:
        return error_response(400, '缺少 case_id')

    # 校验用例存在且属于当前用户的组织
    case = ApiTestCase.query.get(case_id)
    if not case:
        return error_response(404, '用例不存在')

    try:
        current_user = get_jwt_identity()
        service = HealingService()
        result = service.heal_case(case_id=case_id, failure_info=failure_info, user_id=current_user)
        return success_response(data=result, message='AI 修复建议生成成功')
    except Exception as exc:
        logger.error('AI 自愈失败', case_id=case_id, error=str(exc))
        return error_response(500, f'AI 自愈失败: {str(exc)}')


@api_bp.route('/api-test/apply-heal', methods=['POST'])
@jwt_required()
def apply_heal_fix():
    """应用 AI 自愈修复"""
    from ..services.ai.healing_service import HealingService

    data = request.get_json() or {}
    case_id = data.get('case_id')
    fixes = data.get('fixes', [])

    if not case_id:
        return error_response(400, '缺少 case_id')
    if not fixes:
        return error_response(400, '缺少修复项')

    try:
        current_user = get_jwt_identity()
        service = HealingService()
        result = service.apply_fix(case_id=case_id, fixes=fixes, user_id=current_user)
        return success_response(data=result, message='修复已应用')
    except Exception as exc:
        logger.error('应用修复失败', case_id=case_id, error=str(exc))
        return error_response(500, f'应用修复失败: {str(exc)}')


@api_bp.route('/api-test/tags/stats', methods=['GET'])
@jwt_required()
def get_tag_stats():
    """获取标签统计"""
    from ..services.tag_manager_service import get_tag_manager_service

    project_id = request.args.get('project_id', type=int)

    try:
        service = get_tag_manager_service()
        stats = service.get_tag_stats(project_id=project_id)
        return success_response(data=stats)
    except Exception as exc:
        logger.error('获取标签统计失败', error=str(exc))
        return error_response(500, f'获取标签统计失败: {str(exc)}')


@api_bp.route('/api-test/tags/filter', methods=['POST'])
@jwt_required()
def filter_by_tags():
    """按标签过滤用例"""
    from ..services.tag_manager_service import get_tag_manager_service

    data = request.get_json() or {}
    tags = data.get('tags', [])
    project_id = data.get('project_id')
    match_all = data.get('match_all', False)

    if not tags:
        return error_response(400, '请提供标签列表')

    try:
        service = get_tag_manager_service()
        cases = service.filter_by_tags(tags=tags, project_id=project_id, match_all=match_all)
        return success_response(data=cases, message=f'找到 {len(cases)} 个匹配用例')
    except Exception as exc:
        logger.error('标签过滤失败', error=str(exc))
        return error_response(500, f'标签过滤失败: {str(exc)}')


@api_bp.route('/api-test/validate-schema', methods=['POST'])
@jwt_required()
def validate_response_schema():
    """校验 API 响应是否符合 Schema"""
    from ..services.schema_validation_service import get_schema_validation_service

    data = request.get_json() or {}
    schema = data.get('schema')
    response_body = data.get('response_body', '')
    status_code = data.get('status_code', 200)

    if not schema:
        return error_response(400, '缺少 schema 定义')

    try:
        service = get_schema_validation_service()
        result = service.validate_response(
            schema=schema,
            response_body=response_body,
            status_code=status_code,
        )
        return success_response(data=result)
    except Exception as exc:
        logger.error('Schema 校验失败', error=str(exc))
        return error_response(500, f'Schema 校验失败: {str(exc)}')


@api_bp.route('/api-test/generate-schema', methods=['POST'])
@jwt_required()
def generate_response_schema():
    """从 API 响应自动生成 JSON Schema"""
    from ..services.schema_validation_service import get_schema_validation_service

    data = request.get_json() or {}
    response_body = data.get('response_body', '')
    max_depth = data.get('max_depth', 5)

    try:
        service = get_schema_validation_service()
        schema = service.generate_schema_from_response(
            response_body=response_body,
            max_depth=max_depth,
        )
        return success_response(data=schema, message='Schema 生成成功')
    except Exception as exc:
        logger.error('Schema 生成失败', error=str(exc))
        return error_response(500, f'Schema 生成失败: {str(exc)}')
