"""FastAPI 接口测试执行模块

提供接口测试执行相关路由：
- POST /execute: 快速执行 HTTP 请求
- POST /cases/{case_id}/run: 执行单个测试用例
- POST /collections/{collection_id}/run: 批量执行集合
- GET /results/{run_id}: 获取测试执行结果
- WebSocket /ws/api-test-logs/{run_id}: 实时日志推送
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests as http_requests
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from ...core.logging import get_logger
from ...extensions import db
from ...models.api_test_case import ApiTestCollection, ApiTestCase
from ...models.environment import Environment
from ...models.test_report import TestReport
from ...models.test_run import TestRun
from ...models.user import User
from ...utils.env_variables import (
    merge_headers_with_env,
    replace_variables,
    replace_variables_in_dict,
)
from ...utils.js_executor import get_executor
from ...utils.script_context import (
    apply_env_changes,
    apply_pre_script_changes,
    build_post_script_context,
    build_pre_script_context,
    calculate_case_passed,
)
from .auth import get_current_user

logger = get_logger(__name__)

router = APIRouter(tags=["api-tests"])


# ==================== Pydantic Schemas ====================


class ExecuteRequest(BaseModel):
    """快速执行 HTTP 请求（不保存用例）"""
    method: str = Field(..., description="HTTP 方法")
    url: str = Field(..., min_length=1, description="请求 URL")
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    body: Optional[Any] = None
    body_type: Optional[str] = "json"
    timeout: Optional[int] = 30
    env_id: Optional[int] = None
    pre_script: Optional[str] = None
    post_script: Optional[str] = None
    mock_enabled: Optional[bool] = False
    mock_response_code: Optional[int] = 200
    mock_response_body: Optional[str] = ""
    mock_response_headers: Optional[Dict[str, str]] = None
    mock_delay_ms: Optional[int] = 0
    case_id: Optional[int] = None


class ExecuteResponse(BaseModel):
    """执行结果响应"""
    success: bool
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[Any] = None
    response_time: Optional[float] = None
    response_size: Optional[str] = None
    cookies: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    passed: Optional[bool] = None
    is_mock: Optional[bool] = None
    script_execution: Optional[Dict[str, Any]] = None


class CollectionRunRequest(BaseModel):
    """批量执行集合请求"""
    env_id: Optional[int] = Field(None, description="统一环境 ID")


class TestRunResponse(BaseModel):
    """测试运行结果响应"""
    test_run_id: int
    report_id: Optional[int] = None
    total: int
    passed: int
    failed: int
    duration: float
    results: List[Dict[str, Any]]
    message: str = "测试执行完成"


class TestRunDetailResponse(BaseModel):
    """测试运行详情"""
    id: int
    project_id: Optional[int] = None
    test_type: Optional[str] = None
    test_object_id: Optional[int] = None
    test_object_name: Optional[str] = None
    status: Optional[str] = None
    total_cases: Optional[int] = None
    passed: Optional[int] = None
    failed: Optional[int] = None
    skipped: Optional[int] = None
    duration: Optional[float] = None
    pass_rate: Optional[float] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    environment_id: Optional[int] = None
    environment_name: Optional[str] = None
    triggered_by: Optional[str] = None
    results: Optional[List[Dict[str, Any]]] = None
    report: Optional[Dict[str, Any]] = None


# ==================== WebSocket 连接管理 ====================


class ConnectionManager:
    """WebSocket 连接管理器，用于实时日志推送"""

    def __init__(self):
        self._connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, run_id: int):
        await websocket.accept()
        if run_id not in self._connections:
            self._connections[run_id] = []
        self._connections[run_id].append(websocket)
        logger.info("WebSocket connected", run_id=run_id)

    def disconnect(self, websocket: WebSocket, run_id: int):
        if run_id in self._connections:
            self._connections[run_id] = [
                ws for ws in self._connections[run_id] if ws != websocket
            ]
            if not self._connections[run_id]:
                del self._connections[run_id]
        logger.info("WebSocket disconnected", run_id=run_id)

    async def broadcast(self, run_id: int, message: Dict[str, Any]):
        if run_id not in self._connections:
            return
        dead = []
        for ws in self._connections[run_id]:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections[run_id].remove(ws)

    def get_active_runs(self) -> List[int]:
        return list(self._connections.keys())


manager = ConnectionManager()


def _safe_text(value: Any, limit: int = 2000) -> str:
    """将数据安全转成可展示的文本，限制长度"""
    try:
        if isinstance(value, (dict, list)):
            text = json.dumps(value, ensure_ascii=False)
        else:
            text = str(value)
    except Exception:
        text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


# ==================== Routes ====================


@router.post("/execute", response_model=ExecuteResponse)
async def execute_request_v2(
    data: ExecuteRequest,
    user: User = Depends(get_current_user),
):
    """
    执行 HTTP 请求（快速测试）

    不保存用例，直接执行并返回结果。
    支持环境配置的应用、前置脚本和后置断言。
    """
    method = data.method.upper()
    url = data.url
    headers = data.headers or {}
    params = data.params or {}
    body = data.body
    body_type = data.body_type or "json"
    timeout = data.timeout or 30

    # 获取环境变量
    env_vars: Dict[str, Any] = {}
    if data.env_id:
        env = Environment.query.filter_by(id=data.env_id).first()
        if env:
            env_vars = env.variables or {}
            env_headers = env.headers or {}
            headers = {**env_headers, **headers}

    # ========== 前置脚本执行 ==========
    script_execution = {
        "pre_script": {"executed": False, "passed": True},
        "post_script": {"executed": False, "passed": True},
    }

    if data.pre_script and data.pre_script.strip():
        try:
            pre_context = build_pre_script_context(
                environment_vars=env_vars,
                request_data={"method": method, "url": url, "headers": headers,
                              "params": params, "body": body},
            )
            executor = get_executor(timeout=3)
            pre_result = executor.execute_pre_script(data.pre_script, pre_context)
            script_execution["pre_script"] = pre_result

            if not pre_result.get("passed", True):
                return ExecuteResponse(
                    success=False,
                    error=pre_result.get("error", "前置脚本执行失败"),
                    script_execution=script_execution,
                )

            rd = {"method": method, "url": url, "headers": headers,
                  "params": params, "body": body}
            rd = apply_pre_script_changes(rd, pre_result)
            url, headers, body = rd["url"], rd["headers"], rd["body"]
            env_vars = apply_env_changes(env_vars, pre_result)
        except Exception as e:
            logger.error("前置脚本执行异常", error=str(e))
            return ExecuteResponse(
                success=False, error=f"前置脚本执行异常: {str(e)}",
                script_execution=script_execution,
            )

    # 应用环境变量替换
    if env_vars:
        url = replace_variables(url, env_vars)
        headers = replace_variables_in_dict(headers, env_vars)
        params = replace_variables_in_dict(params, env_vars)

    # Mock 模式
    if data.mock_enabled:
        mock_body = data.mock_response_body
        if mock_body and isinstance(mock_body, str):
            try:
                mock_body = json.loads(mock_body)
            except Exception:
                pass
        mock_delay_ms = data.mock_delay_ms or 0
        if mock_delay_ms > 0:
            await asyncio.sleep(mock_delay_ms / 1000.0)
        return ExecuteResponse(
            success=True, status_code=data.mock_response_code or 200,
            body=mock_body, headers=data.mock_response_headers or {},
            response_time=float(mock_delay_ms), script_execution=script_execution,
            passed=True, is_mock=True,
        )

    # 数据库 case_id 兜底 Mock
    if data.case_id and not data.mock_enabled:
        case = ApiTestCase.query.get(data.case_id)
        if case and case.mock_enabled:
            mock_body = case.mock_response_body
            if mock_body:
                try:
                    mock_body = json.loads(mock_body)
                except Exception:
                    pass
            if case.mock_delay_ms and case.mock_delay_ms > 0:
                await asyncio.sleep(case.mock_delay_ms / 1000.0)
            return ExecuteResponse(
                success=True, status_code=case.mock_response_code or 200,
                body=mock_body, headers=case.mock_response_headers or {},
                response_time=float(case.mock_delay_ms or 0),
                script_execution=script_execution, passed=True, is_mock=True,
            )

    # 执行真实 HTTP 请求
    start_time = time.time()
    try:
        request_kwargs: Dict[str, Any] = {
            "method": method, "url": url, "headers": headers, "params": params,
            "timeout": timeout, "verify": False, "allow_redirects": True,
        }
        if body and method in ("POST", "PUT", "PATCH"):
            request_kwargs["json" if body_type == "json" else "data"] = body

        response = http_requests.request(**request_kwargs)
        elapsed_time = (time.time() - start_time) * 1000

        try:
            response_body = response.json()
        except Exception:
            response_body = response.text

        response_size = len(response.content)
        if response_size > 1024 * 1024:
            size_str = f"{response_size / (1024 * 1024):.2f} MB"
        elif response_size > 1024:
            size_str = f"{response_size / 1024:.2f} KB"
        else:
            size_str = f"{response_size} B"

        # 后置断言
        if data.post_script and data.post_script.strip():
            try:
                post_context = build_post_script_context(
                    environment_vars=env_vars,
                    response_data={"status_code": response.status_code,
                                   "headers": dict(response.headers), "body": response_body,
                                   "response_time": round(elapsed_time, 2), "response_size": size_str},
                )
                executor = get_executor(timeout=3)
                post_result = executor.execute_post_script(data.post_script, post_context)
                script_execution["post_script"] = post_result
            except Exception as e:
                logger.error("后置断言执行异常", error=str(e))
                script_execution["post_script"] = {
                    "executed": True, "passed": False, "error": str(e),
                    "assertions": {"total": 0, "passed": 0, "failed": 0, "details": []},
                }

        return ExecuteResponse(
            success=True, status_code=response.status_code,
            headers=dict(response.headers), body=response_body,
            response_time=round(elapsed_time, 2), response_size=size_str,
            cookies=dict(response.cookies), script_execution=script_execution,
        )
    except http_requests.exceptions.Timeout:
        elapsed_time = (time.time() - start_time) * 1000
        return ExecuteResponse(success=False, error="请求超时",
                              response_time=round(elapsed_time, 2), script_execution=script_execution)
    except http_requests.exceptions.ConnectionError as e:
        elapsed_time = (time.time() - start_time) * 1000
        return ExecuteResponse(success=False, error=f"连接错误: {str(e)}",
                              response_time=round(elapsed_time, 2), script_execution=script_execution)
    except Exception as e:
        elapsed_time = (time.time() - start_time) * 1000
        return ExecuteResponse(success=False, error=str(e),
                              response_time=round(elapsed_time, 2), script_execution=script_execution)


@router.post("/cases/{case_id}/run", response_model=ExecuteResponse)
async def run_case_v2(
    case_id: int,
    env_id: Optional[int] = Query(None, description="环境 ID"),
    user: User = Depends(get_current_user),
):
    """执行单个测试用例（支持前置脚本和后置断言）"""
    case = ApiTestCase.query.filter_by(id=case_id, user_id=user.id).first()
    if not case:
        raise HTTPException(status_code=404, detail="用例不存在")

    env_vars: Dict[str, Any] = {}
    if env_id:
        env = Environment.query.filter_by(id=env_id).first()
        if env:
            env_vars = env.variables or {}

    script_execution = {
        "pre_script": {"executed": False, "passed": True},
        "post_script": {"executed": False, "passed": True},
    }

    if case.pre_script and case.pre_script.strip():
        try:
            pre_context = build_pre_script_context(
                environment_vars=env_vars,
                request_data={"method": case.method, "url": case.url,
                              "headers": case.headers or {}, "params": case.params or {},
                              "body": case.body},
            )
            executor = get_executor(timeout=3)
            pre_result = executor.execute_pre_script(case.pre_script, pre_context)
            script_execution["pre_script"] = pre_result

            if not pre_result.get("passed", True):
                case.last_run_at = datetime.utcnow()
                case.last_status = "failed"
                db.session.commit()
                return ExecuteResponse(
                    success=False, error=pre_result.get("error", "前置脚本执行失败"),
                    script_execution=script_execution,
                )

            url, headers, params, body = case.url, case.headers or {}, case.params or {}, case.body
            rd = apply_pre_script_changes(
                {"method": case.method, "url": url, "headers": headers, "params": params, "body": body},
                pre_result,
            )
            url, headers, body = rd["url"], rd["headers"], rd["body"]
            env_vars = apply_env_changes(env_vars, pre_result)
        except Exception as e:
            logger.error("前置脚本执行异常", error=str(e))
            case.last_run_at = datetime.utcnow()
            case.last_status = "failed"
            db.session.commit()
            return ExecuteResponse(success=False, error=f"前置脚本执行异常: {str(e)}",
                                  script_execution=script_execution)
    else:
        url, headers, params, body = case.url, case.headers or {}, case.params or {}, case.body

    if case.mock_enabled:
        case.last_run_at = datetime.utcnow()
        case.last_status = "passed"
        mock_result = {
            "success": True, "status_code": case.mock_response_code or 200,
            "body": case.mock_response_body, "headers": case.mock_response_headers,
            "response_time": case.mock_delay_ms or 0, "script_execution": script_execution,
            "passed": True, "is_mock": True,
        }
        case.last_result = mock_result
        db.session.commit()
        return ExecuteResponse(**mock_result)

    if env_vars:
        url = replace_variables(url, env_vars)
        headers = replace_variables_in_dict(headers, env_vars)
        params = replace_variables_in_dict(params, env_vars)
        if isinstance(body, dict):
            body = replace_variables_in_dict(body, env_vars)
        elif isinstance(body, str):
            body = replace_variables(body, env_vars)

    if env_id:
        headers = merge_headers_with_env(headers, env_id, db)

    start_time = time.time()
    try:
        request_kwargs: Dict[str, Any] = {
            "method": case.method, "url": url, "headers": headers, "params": params,
            "timeout": case.timeout or 30, "verify": False, "allow_redirects": True,
        }
        if case.body and case.method in ("POST", "PUT", "PATCH"):
            if case.body_type == "json":
                request_kwargs["json"] = body
            else:
                request_kwargs["data"] = body

        response = http_requests.request(**request_kwargs)
        elapsed_time = (time.time() - start_time) * 1000

        try:
            response_body = response.json()
        except Exception:
            response_body = response.text

        if case.post_script and case.post_script.strip():
            try:
                post_context = build_post_script_context(
                    environment_vars=env_vars,
                    response_data={"status_code": response.status_code,
                                   "headers": dict(response.headers), "body": response_body,
                                   "response_time": round(elapsed_time, 2)},
                )
                executor = get_executor(timeout=3)
                post_result = executor.execute_post_script(case.post_script, post_context)
                script_execution["post_script"] = post_result
            except Exception as e:
                logger.error("后置断言执行异常", error=str(e))
                script_execution["post_script"] = {
                    "executed": True, "passed": False, "error": str(e),
                    "assertions": {"total": 0, "passed": 0, "failed": 0, "details": []},
                }

        has_script = bool(case.pre_script or case.post_script)
        passed = calculate_case_passed(script_execution, response.status_code, has_script=has_script)

        case.last_run_at = datetime.utcnow()
        case.last_status = "passed" if passed else "failed"
        db.session.commit()

        return ExecuteResponse(
            success=True, status_code=response.status_code, body=response_body,
            response_time=round(elapsed_time, 2), script_execution=script_execution, passed=passed,
        )
    except Exception as e:
        case.last_run_at = datetime.utcnow()
        case.last_status = "failed"
        db.session.commit()
        return ExecuteResponse(success=False, error=str(e), script_execution=script_execution)


@router.post("/collections/{collection_id}/run", response_model=TestRunResponse)
async def run_collection_v2(
    collection_id: int,
    data: CollectionRunRequest = CollectionRunRequest(),
    user: User = Depends(get_current_user),
):
    """批量执行集合中的所有用例，并生成测试报告"""
    collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user.id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="集合不存在")

    cases = ApiTestCase.query.filter_by(collection_id=collection_id, is_enabled=True).all()
    if not cases:
        raise HTTPException(status_code=400, detail="集合中没有可执行的用例")

    env_id = data.env_id
    unified_env_name = None
    unified_env_variables: Dict[str, Any] = {}
    env_obj = None
    use_unified_env = env_id is not None

    if use_unified_env:
        env_obj = db.session.get(Environment, env_id)
        if env_obj:
            unified_env_name = env_obj.name
            unified_env_variables = env_obj.variables or {}

    project_id = collection.project_id
    if not project_id:
        if use_unified_env and env_obj:
            project_id = env_obj.project_id
        if not project_id and cases:
            project_id = cases[0].project_id
            if not project_id and cases[0].environment_id:
                case_env = db.session.get(Environment, cases[0].environment_id)
                if case_env:
                    project_id = case_env.project_id

    test_run = TestRun(
        project_id=project_id, test_type="api", test_object_id=collection_id,
        test_object_name=collection.name, status="running", total_cases=len(cases),
        environment_id=env_id,
        environment_name=unified_env_name if use_unified_env else "用例自身环境",
        started_at=datetime.utcnow(), triggered_by="manual", triggered_user_id=user.id,
    )
    db.session.add(test_run)
    db.session.commit()

    run_id = test_run.id
    asyncio.get_event_loop().create_task(
        manager.broadcast(run_id, {"type": "run_started", "run_id": run_id, "total": len(cases)})
    )

    results: List[Dict[str, Any]] = []
    total_passed = 0
    total_failed = 0
    overall_start_time = time.time()

    for idx, case in enumerate(cases):
        case_start_time = time.time()
        script_execution = {
            "pre_script": {"executed": False, "passed": True},
            "post_script": {"executed": False, "passed": True},
        }

        try:
            # Mock
            if case.mock_enabled:
                case.last_run_at = datetime.utcnow()
                case.last_status = "passed"
                mock_result = {
                    "case_id": case.id, "name": case.name, "method": case.method,
                    "url": case.url, "passed": True,
                    "status_code": case.mock_response_code or 200,
                    "response_time": case.mock_delay_ms or 0,
                    "response_body": case.mock_response_body,
                    "response_headers": case.mock_response_headers,
                    "response_cookies": {}, "request_headers": case.headers,
                    "request_params": case.params, "request_body": case.body,
                    "attachments": [], "script_execution": script_execution,
                    "environment_id": env_id, "environment_name": unified_env_name,
                    "is_mock": True,
                }
                total_passed += 1
                results.append(mock_result)
                case.last_result = {"success": True, "status_code": case.mock_response_code or 200,
                                    "body": case.mock_response_body, "headers": case.mock_response_headers,
                                    "response_time": case.mock_delay_ms or 0,
                                    "script_execution": script_execution, "passed": True, "is_mock": True}
                db.session.commit()
                asyncio.get_event_loop().create_task(
                    manager.broadcast(run_id, {"type": "case_completed", "index": idx + 1,
                                               "total": len(cases), "case_id": case.id,
                                               "name": case.name, "passed": True, "is_mock": True})
                )
                continue

            url, headers, params, body = case.url, case.headers or {}, case.params or {}, case.body
            effective_env_id = env_id if use_unified_env else case.environment_id
            effective_env_name = unified_env_name if use_unified_env else None
            effective_env_variables: Dict[str, Any] = dict(unified_env_variables) if use_unified_env else {}

            if not use_unified_env and case.environment_id:
                case_env = db.session.get(Environment, case.environment_id)
                if case_env:
                    effective_env_name = case_env.name
                    effective_env_variables = dict(case_env.variables or {})

            logger.info("执行用例", case_id=case.id, case_name=case.name, method=case.method, url=url,
                        environment=effective_env_name or "无")

            asyncio.get_event_loop().create_task(
                manager.broadcast(run_id, {"type": "case_starting", "index": idx + 1,
                                           "total": len(cases), "case_id": case.id,
                                           "name": case.name, "method": case.method, "url": url})
            )

            # 前置脚本
            if case.pre_script and case.pre_script.strip():
                try:
                    pre_context = build_pre_script_context(
                        environment_vars=effective_env_variables,
                        request_data={"method": case.method, "url": url, "headers": headers,
                                      "params": params, "body": body},
                    )
                    executor = get_executor(timeout=3)
                    pre_result = executor.execute_pre_script(case.pre_script, pre_context)
                    script_execution["pre_script"] = pre_result

                    if not pre_result.get("passed", True):
                        elapsed_time = (time.time() - case_start_time) * 1000
                        total_failed += 1
                        case.last_run_at = datetime.utcnow()
                        case.last_status = "failed"
                        db.session.commit()
                        case_result = {"case_id": case.id, "name": case.name, "method": case.method,
                                       "url": url, "passed": False, "status_code": None,
                                       "response_time": round(elapsed_time, 2),
                                       "script_execution": script_execution,
                                       "error": pre_result.get("error", "前置脚本执行失败"),
                                       "environment_id": effective_env_id,
                                       "environment_name": effective_env_name}
                        results.append(case_result)
                        asyncio.get_event_loop().create_task(
                            manager.broadcast(run_id, {"type": "case_completed", "index": idx + 1,
                                                       "total": len(cases), "case_id": case.id,
                                                       "name": case.name, "passed": False,
                                                       "error": case_result["error"]})
                        )
                        continue

                    rd = apply_pre_script_changes(
                        {"method": case.method, "url": url, "headers": headers,
                         "params": params, "body": body}, pre_result)
                    url, headers, body = rd["url"], rd["headers"], rd["body"]
                    effective_env_variables = apply_env_changes(effective_env_variables, pre_result)
                except Exception as e:
                    logger.error("前置脚本执行异常", error=str(e))
                    elapsed_time = (time.time() - case_start_time) * 1000
                    total_failed += 1
                    case.last_run_at = datetime.utcnow()
                    case.last_status = "failed"
                    db.session.commit()
                    script_execution["pre_script"] = {"executed": True, "passed": False, "error": str(e)}
                    case_result = {"case_id": case.id, "name": case.name, "method": case.method,
                                   "url": url, "passed": False, "status_code": None,
                                   "response_time": round(elapsed_time, 2),
                                   "script_execution": script_execution,
                                   "error": f"前置脚本执行异常: {str(e)}",
                                   "environment_id": effective_env_id,
                                   "environment_name": effective_env_name}
                    results.append(case_result)
                    asyncio.get_event_loop().create_task(
                        manager.broadcast(run_id, {"type": "case_completed", "index": idx + 1,
                                                   "total": len(cases), "case_id": case.id,
                                                   "name": case.name, "passed": False,
                                                   "error": case_result["error"]})
                    )
                    continue

            # 环境变量替换
            if effective_env_variables:
                try:
                    url = replace_variables(url, effective_env_variables)
                    headers = replace_variables_in_dict(headers, effective_env_variables)
                    params = replace_variables_in_dict(params, effective_env_variables)
                    if isinstance(body, dict):
                        body = replace_variables_in_dict(body, effective_env_variables)
                    elif isinstance(body, str):
                        body = replace_variables(body, effective_env_variables)
                except Exception as e:
                    logger.error("环境变量替换失败", error=str(e))

            if effective_env_id:
                try:
                    headers = merge_headers_with_env(headers, effective_env_id, db)
                except Exception as e:
                    logger.error("合并请求头失败", error=str(e))

            request_kwargs: Dict[str, Any] = {
                "method": case.method, "url": url, "headers": headers, "params": params,
                "timeout": case.timeout or 30, "verify": False,
            }
            if body and case.method in ("POST", "PUT", "PATCH"):
                if case.body_type == "json":
                    request_kwargs["json"] = body
                else:
                    request_kwargs["data"] = body

            response = http_requests.request(**request_kwargs)
            elapsed_time = (time.time() - case_start_time) * 1000

            try:
                response_body = response.json()
            except Exception:
                response_body = response.text

            if case.post_script and case.post_script.strip():
                try:
                    post_context = build_post_script_context(
                        environment_vars=effective_env_variables,
                        response_data={"status_code": response.status_code,
                                       "headers": dict(response.headers), "body": response_body,
                                       "response_time": round(elapsed_time, 2)},
                    )
                    executor = get_executor(timeout=3)
                    post_result = executor.execute_post_script(case.post_script, post_context)
                    script_execution["post_script"] = post_result
                except Exception as e:
                    logger.error("后置断言执行异常", error=str(e))
                    script_execution["post_script"] = {
                        "executed": True, "passed": False, "error": str(e),
                        "assertions": {"total": 0, "passed": 0, "failed": 0, "details": []},
                    }

            has_script = bool(case.pre_script or case.post_script)
            passed = calculate_case_passed(script_execution, response.status_code, has_script=has_script)

            response_headers = dict(response.headers)
            response_cookies = dict(response.cookies)
            response_body_preview = _safe_text(response_body, limit=2000)

            attachments = [
                {"name": "response_body", "type": "text", "content": response_body_preview},
                {"name": "response_headers", "type": "json", "content": _safe_text(response_headers, limit=2000)},
            ]
            request_body_preview = _safe_text(body, limit=2000) if body else None
            if request_body_preview:
                attachments.append({"name": "request_body", "type": "text", "content": request_body_preview})

            error_message = None
            if not passed:
                pre_script_error = script_execution.get("pre_script", {}).get("error")
                post_script_error = script_execution.get("post_script", {}).get("error")
                if pre_script_error:
                    error_message = f"前置脚本失败: {pre_script_error}"
                elif post_script_error:
                    error_message = f"后置断言失败: {post_script_error}"
                elif response.status_code >= 400:
                    error_message = f"HTTP {response.status_code}"
                    if isinstance(response_body, str) and response_body:
                        error_message = f"{error_message}: {response_body_preview}"

            case.last_run_at = datetime.utcnow()
            case.last_status = "passed" if passed else "failed"
            if passed:
                total_passed += 1
            else:
                total_failed += 1

            case_result = {
                "case_id": case.id, "name": case.name, "method": case.method, "url": url,
                "passed": passed, "status_code": response.status_code,
                "response_time": round(elapsed_time, 2), "response_body": response_body,
                "response_headers": response_headers, "response_cookies": response_cookies,
                "request_headers": headers, "request_params": params, "request_body": body,
                "attachments": attachments, "script_execution": script_execution,
                "error": error_message, "environment_id": effective_env_id,
                "environment_name": effective_env_name,
            }
            results.append(case_result)

            asyncio.get_event_loop().create_task(
                manager.broadcast(run_id, {"type": "case_completed", "index": idx + 1,
                                           "total": len(cases), "case_id": case.id,
                                           "name": case.name, "passed": passed,
                                           "status_code": response.status_code,
                                           "response_time": round(elapsed_time, 2)})
            )

        except Exception as e:
            elapsed_time = (time.time() - case_start_time) * 1000
            total_failed += 1
            logger.error("执行用例失败", case_id=case.id, case_name=case.name, error=str(e), exc_info=True)
            case.last_run_at = datetime.utcnow()
            case.last_status = "failed"
            db.session.commit()

            resp_exc = getattr(e, "response", None)
            resp_status = getattr(resp_exc, "status_code", None) if resp_exc else None
            resp_headers_dict = dict(resp_exc.headers) if resp_exc else None
            resp_cookies_dict = dict(resp_exc.cookies) if resp_exc else None
            resp_body = None
            if resp_exc is not None:
                try:
                    resp_body = resp_exc.json()
                except Exception:
                    try:
                        resp_body = resp_exc.text
                    except Exception:
                        resp_body = None

            error_preview = _safe_text(str(e), limit=1000)
            case_result = {
                "case_id": case.id, "name": case.name, "method": case.method, "url": case.url,
                "passed": False, "status_code": resp_status, "response_time": round(elapsed_time, 2),
                "response_body": resp_body, "response_headers": resp_headers_dict,
                "response_cookies": resp_cookies_dict, "request_headers": case.headers or {},
                "request_params": case.params or {}, "request_body": case.body,
                "attachments": [{"name": "exception", "type": "text", "content": error_preview}],
                "script_execution": script_execution, "error": error_preview,
                "environment_id": effective_env_id if "effective_env_id" in locals() else None,
                "environment_name": effective_env_name if "effective_env_name" in locals() else None,
            }
            results.append(case_result)
            asyncio.get_event_loop().create_task(
                manager.broadcast(run_id, {"type": "case_completed", "index": idx + 1,
                                           "total": len(cases), "case_id": case.id,
                                           "name": case.name, "passed": False, "error": error_preview})
            )

    total_duration = time.time() - overall_start_time
    test_run.status = "success" if total_failed == 0 else "failed"
    test_run.passed = total_passed
    test_run.failed = total_failed
    test_run.duration = total_duration
    test_run.finished_at = datetime.utcnow()
    test_run.results = results

    report = TestReport(
        test_run_id=test_run.id, project_id=project_id, test_type="api",
        title=f"{collection.name} - 接口测试报告",
        summary={"total": len(cases), "passed": total_passed, "failed": total_failed,
                 "success_rate": round(total_passed / len(cases) * 100, 2) if cases else 0,
                 "duration": round(total_duration, 2),
                 "environment": unified_env_name if use_unified_env else "混合环境",
                 "environment_mode": "unified" if use_unified_env else "individual"},
        report_data={"collection": {"id": collection.id, "name": collection.name,
                                    "description": collection.description},
                     "environment": ({"id": env_id, "name": unified_env_name, "mode": "unified"}
                                     if use_unified_env
                                     else {"mode": "individual", "description": "各用例使用自身配置的环境"}),
                     "results": results},
        status="generated",
    )
    db.session.add(report)
    test_run.report_id = report.id
    db.session.commit()

    asyncio.get_event_loop().create_task(
        manager.broadcast(run_id, {"type": "run_completed", "run_id": run_id,
                                   "status": test_run.status, "total": len(cases),
                                   "passed": total_passed, "failed": total_failed,
                                   "duration": round(total_duration, 2)})
    )

    return TestRunResponse(
        test_run_id=test_run.id, report_id=report.id, total=len(cases),
        passed=total_passed, failed=total_failed,
        duration=round(total_duration, 2), results=results,
    )


@router.get("/results/{run_id}", response_model=TestRunDetailResponse)
async def get_test_run_results_v2(
    run_id: int,
    user: User = Depends(get_current_user),
):
    """获取测试执行结果详情"""
    test_run = TestRun.query.get(run_id)
    if not test_run:
        raise HTTPException(status_code=404, detail="测试运行不存在")

    report_data = None
    if test_run.report_id:
        report = TestReport.query.get(test_run.report_id)
        if report:
            report_data = report.to_dict()

    return TestRunDetailResponse(
        id=test_run.id, project_id=test_run.project_id, test_type=test_run.test_type,
        test_object_id=test_run.test_object_id, test_object_name=test_run.test_object_name,
        status=test_run.status, total_cases=test_run.total_cases,
        passed=test_run.passed, failed=test_run.failed, skipped=test_run.skipped,
        duration=test_run.duration,
        pass_rate=(round(test_run.passed / test_run.total_cases * 100, 2)
                   if test_run.total_cases and test_run.total_cases > 0 else 0),
        started_at=test_run.started_at.isoformat() if test_run.started_at else None,
        finished_at=test_run.finished_at.isoformat() if test_run.finished_at else None,
        environment_id=test_run.environment_id, environment_name=test_run.environment_name,
        triggered_by=test_run.triggered_by, results=test_run.results, report=report_data,
    )


# ==================== WebSocket 端点 ====================


async def _authenticate_websocket(websocket: WebSocket) -> Optional[int]:
    """从 WebSocket 连接中验证 JWT Token"""
    from fastapi.security import HTTPAuthorizationCredentials
    token = websocket.query_params.get('token')
    if not token:
        # 也检查 Authorization header
        auth_header = websocket.headers.get('authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
    if not token:
        return None
    try:
        from flask_jwt_extended import decode_token
        decoded = decode_token(token)
        return int(decoded.get('sub', 0))
    except Exception:
        return None


@router.websocket("/ws/api-test-logs/{run_id}")
async def websocket_api_test_logs(websocket: WebSocket, run_id: int):
    """
    WebSocket 端点：实时推送接口测试日志

    认证方式：连接时通过 ?token=<jwt> 或 Authorization: Bearer <jwt> 传递

    消息类型：
    - run_started: 测试开始
    - case_starting: 用例开始执行
    - case_completed: 用例执行完成
    - run_completed: 测试执行完成
    """
    user_id = await _authenticate_websocket(websocket)
    if not user_id:
        await websocket.accept()
        await websocket.send_json({"type": "error", "message": "Authentication required"})
        await websocket.close(code=4001)
        return

    await manager.connect(websocket, run_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, run_id)
    except Exception:
        manager.disconnect(websocket, run_id)
