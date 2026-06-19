"""FastAPI 性能测试模块"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from ...core.logging import get_logger
from ...extensions import db, celery
from ...models.perf_test_scenario import PerfTestScenario
from ...models.perf_test_result import PerformanceTestResult, PerformanceMetricSample
from ...models.perf_test_alert import PerformanceAlertRule, PerformanceAlertLog
from ...models.user import User
from ...utils.validators import is_valid_url, is_valid_http_method
from ...tasks import run_perf_test_task
from ...utils.ai_script_generator import generate_test_script
from .auth import get_current_user

logger = get_logger(__name__)
router = APIRouter(tags=["perf-tests"])


class ScenarioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = ""
    target_url: str = "http://localhost:8080"
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    user_count: int = Field(10, ge=1, le=2000)
    spawn_rate: int = Field(1, ge=1, le=50)
    duration: int = Field(60, ge=10, le=3600)
    step_load_enabled: bool = False
    step_users: Optional[int] = None
    step_duration: Optional[int] = None
    project_id: Optional[int] = None
    script_content: Optional[str] = None
    tags: Optional[List[str]] = None


class ScenarioUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    target_url: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None
    user_count: Optional[int] = Field(None, ge=1, le=2000)
    spawn_rate: Optional[int] = Field(None, ge=1, le=50)
    duration: Optional[int] = Field(None, ge=10, le=3600)
    step_load_enabled: Optional[bool] = None
    step_users: Optional[int] = None
    step_duration: Optional[int] = None
    script_content: Optional[str] = None
    tags: Optional[List[str]] = None


class ScenarioRunRequest(BaseModel):
    user_count: Optional[int] = None
    spawn_rate: Optional[int] = None
    duration: Optional[int] = None
    step_load_enabled: Optional[bool] = None
    step_users: Optional[int] = None
    step_duration: Optional[int] = None


class AlertRuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = ""
    scenario_id: Optional[int] = None
    condition_type: str = "absolute"
    metric_name: Optional[str] = None
    operator: Optional[str] = None
    threshold_value: Optional[float] = None
    relative_metric: Optional[str] = None
    degradation_percentage: Optional[float] = None
    notify_webhook: Optional[str] = None
    notify_users: Optional[List[int]] = None
    is_enabled: bool = True


class AlertRuleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    scenario_id: Optional[int] = None
    condition_type: Optional[str] = None
    metric_name: Optional[str] = None
    operator: Optional[str] = None
    threshold_value: Optional[float] = None
    relative_metric: Optional[str] = None
    degradation_percentage: Optional[float] = None
    notify_webhook: Optional[str] = None
    notify_users: Optional[List[int]] = None
    is_enabled: Optional[bool] = None


class AlertEvaluateRequest(BaseModel):
    test_result_id: int

def _parse_target_url(url):
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}", parsed.path or "/"
    except Exception:
        return url, "/"


def _generate_locust_script(method, endpoint_path, headers=None, body=None):
    method = method.upper()
    endpoint_path = endpoint_path or "/"
    headers_code = ""
    if headers:
        items = [f'            "{k}": "{v}"' for k, v in headers.items()]
        joined = ",\n".join(items)
        headers_code = f"\n        headers = {{\n{joined}\n        }}\n"
    if method == "POST":
        body_str = json.dumps(body, ensure_ascii=False) if body else "{}"
        req = f'self.client.post("{endpoint_path}", json={body_str}'
        if headers:
            req += ", headers=headers"
        req += ")"
    elif method == "PUT":
        body_str = json.dumps(body, ensure_ascii=False) if body else "{}"
        req = f'self.client.put("{endpoint_path}", json={body_str}'
        if headers:
            req += ", headers=headers"
        req += ")"
    elif method == "DELETE":
        req = f'self.client.delete("{endpoint_path}"'
        if headers:
            req += ", headers=headers"
        req += ")"
    else:
        req = f'self.client.get("{endpoint_path}"'
        if headers:
            req += ", headers=headers"
        req += ")"
    script = '"""Locust script (auto-generated)\n"""\n'
    script += 'from locust import HttpUser, task, between\n\n'
    script += 'class TestUser(HttpUser):\n'
    script += '    wait_time = between(1, 2)\n'
    script += headers_code + '\n'
    script += '    @task\n'
    script += '    def test_endpoint(self):\n'
    script += f'        {req}\n'
    return script

def _validate_perf_numbers(user_count, spawn_rate, duration):
    if not (1 <= user_count <= 2000):
        return None, "user_count must be between 1 and 2000"
    if not (1 <= spawn_rate <= 50):
        return None, "spawn_rate must be between 1 and 50"
    if not (10 <= duration <= 3600):
        return None, "duration must be between 10 and 3600"
    return (user_count, spawn_rate, duration), None

@router.get("/scenarios")
async def get_scenarios(project_id: Optional[int] = Query(None), user: User = Depends(get_current_user)):
    query = PerfTestScenario.query.filter_by(user_id=user.id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    return [s.to_dict() for s in query.order_by(PerfTestScenario.created_at.desc()).all()]


@router.post("/scenarios", status_code=201)
async def create_scenario(data: ScenarioCreate, user: User = Depends(get_current_user)):
    if not is_valid_url(data.target_url):
        raise HTTPException(400, "target_url must be valid")
    method = data.method.upper()
    if not is_valid_http_method(method):
        raise HTTPException(400, "method must be valid")
    numbers, error = _validate_perf_numbers(data.user_count, data.spawn_rate, data.duration)
    if error:
        raise HTTPException(400, error)
    user_count, spawn_rate, duration = numbers
    if data.step_load_enabled and (data.step_users is None or data.step_duration is None):
        raise HTTPException(400, "step_users and step_duration required when step_load_enabled")
    script_content = data.script_content
    if not script_content:
        _, ep = _parse_target_url(data.target_url)
        script_content = _generate_locust_script(method, ep, data.headers, data.body)
    s = PerfTestScenario(
        name=data.name, description=data.description or "", target_url=data.target_url,
        method=method, headers=data.headers, body=data.body,
        user_count=user_count, spawn_rate=spawn_rate, duration=duration,
        step_load_enabled=data.step_load_enabled, step_users=data.step_users or 10,
        step_duration=data.step_duration or 30, project_id=data.project_id,
        user_id=user.id, script_content=script_content, tags=data.tags,
    )
    db.session.add(s)
    db.session.commit()
    return s.to_dict()


@router.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: int, user: User = Depends(get_current_user)):
    s = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user.id).first()
    if not s:
        raise HTTPException(404, "场景不存在")
    return s.to_dict()


@router.put("/scenarios/{scenario_id}")
async def update_scenario(scenario_id: int, data: ScenarioUpdate, user: User = Depends(get_current_user)):
    s = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user.id).first()
    if not s:
        raise HTTPException(404, "Scenario not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    db.session.commit()
    return s.to_dict()


@router.delete("/scenarios/{scenario_id}")
async def delete_scenario(scenario_id: int, user: User = Depends(get_current_user)):
    s = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user.id).first()
    if not s:
        raise HTTPException(404, "场景不存在")
    if s.status == "running":
        try:
            celery.control.revoke(f"perf_test_{scenario_id}_{user.id}", terminate=True)
        except Exception:
            pass
    db.session.delete(s)
    db.session.commit()

@router.post("/scenarios/{scenario_id}/run")
async def run_scenario(scenario_id: int, data: ScenarioRunRequest = ScenarioRunRequest(), user: User = Depends(get_current_user)):
    s = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user.id).first()
    if not s:
        raise HTTPException(404, "Scenario not found")
    if s.status == "running":
        raise HTTPException(400, "Already running")
    uc = data.user_count or s.user_count
    sr = data.spawn_rate or s.spawn_rate
    dur = data.duration or s.duration
    sle = data.step_load_enabled if data.step_load_enabled is not None else s.step_load_enabled
    su = data.step_users or s.step_users
    sd = data.step_duration or s.step_duration
    numbers, error = _validate_perf_numbers(uc, sr, dur)
    if error:
        raise HTTPException(400, error)
    uc, sr, dur = numbers
    s.status = "running"
    s.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.session.commit()
    task = run_perf_test_task.apply_async(
        args=[scenario_id, uc, sr, dur, sle, su, sd],
        task_id=f"perf_test_{scenario_id}_{user.id}",
    )
    return {
        "message": "Scenario submitted", "task_id": task.id, "scenario_id": scenario_id,
        "config": {"users": uc, "spawn_rate": sr, "run_time": dur, "step_load_enabled": sle, "step_users": su, "step_duration": sd},
    }


@router.post("/scenarios/{scenario_id}/stop")
async def stop_scenario(scenario_id: int, user: User = Depends(get_current_user)):
    s = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user.id).first()
    if not s:
        raise HTTPException(404, "场景不存在")
    if s.status != "running":
        raise HTTPException(400, "测试未在运行")
    try:
        celery.control.revoke(f"perf_test_{scenario_id}_{user.id}", terminate=True)
        s.status = "stopped"
        db.session.commit()
        return {"message": "已停止"}
    except Exception as e:
        raise HTTPException(500, f"停止失败: {str(e)}")


@router.get("/scenarios/{scenario_id}/status")
async def get_scenario_status(scenario_id: int, user: User = Depends(get_current_user)):
    s = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user.id).first()
    if not s:
        raise HTTPException(404, "场景不存在")
    return {
        "status": s.status, "last_run_at": s.last_run_at.isoformat() + "Z" if s.last_run_at else None,
        "last_result": s.last_result, "avg_response_time": s.avg_response_time,
        "max_response_time": s.max_response_time, "min_response_time": s.min_response_time,
        "throughput": s.throughput, "error_rate": s.error_rate,
    }


@router.get("/running")
async def get_running_tests(user: User = Depends(get_current_user)):
    rs = PerfTestScenario.query.filter_by(user_id=user.id, status="running").all()
    return [{
        "id": s.id, "scenario_id": s.id, "name": s.name, "user_count": s.user_count,
        "duration": s.duration, "elapsed": 0, "status": s.status,
        "avg_response_time": s.avg_response_time or 0, "throughput": s.throughput or 0,
        "error_rate": s.error_rate or 0,
        "started_at": s.last_run_at.isoformat() + "Z" if s.last_run_at else None,
    } for s in rs]

@router.get("/results")
async def get_performance_results(
    project_id: Optional[int] = Query(None), scenario_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None), page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100), user: User = Depends(get_current_user),
):
    query = PerformanceTestResult.query.join(PerfTestScenario).filter(PerfTestScenario.user_id == user.id)
    if project_id:
        query = query.filter(PerformanceTestResult.project_id == project_id)
    if scenario_id:
        query = query.filter(PerformanceTestResult.scenario_id == scenario_id)
    if status:
        query = query.filter(PerformanceTestResult.status == status)
    total = query.count()
    items = query.order_by(PerformanceTestResult.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    return {"items": [r.to_dict() for r in items], "total": total, "page": page, "per_page": per_page}


@router.get("/results/{result_id}/metrics")
async def get_performance_result_metrics(result_id: int, limit: Optional[int] = Query(None), user: User = Depends(get_current_user)):
    result = PerformanceTestResult.query.join(PerfTestScenario).filter(
        PerformanceTestResult.id == result_id, PerfTestScenario.user_id == user.id).first()
    if not result:
        raise HTTPException(404, "测试结果不存在")
    q = PerformanceMetricSample.query.filter_by(test_result_id=result_id).order_by(PerformanceMetricSample.elapsed_seconds.asc())
    if limit:
        q = q.limit(limit)
    samples = q.all()
    return {"result": result.to_dict(), "metrics": [s.to_dict() for s in samples], "total_samples": len(samples)}


@router.get("/compare")
async def compare_performance_runs(run_ids: str = Query(..., description="Comma-separated result IDs"), user: User = Depends(get_current_user)):
    try:
        ids = [int(x.strip()) for x in run_ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(400, "run_ids must be comma-separated integers")
    if len(ids) < 2:
        raise HTTPException(400, "至少需要 2 个 ID")
    if len(ids) > 10:
        raise HTTPException(400, "最多 10 个 ID")
    results = PerformanceTestResult.query.filter(PerformanceTestResult.id.in_(ids)).all()
    if len(results) != len(ids):
        raise HTTPException(404, "部分 ID 未找到")
    results_sorted = sorted(results, key=lambda r: r.created_at or datetime.min)
    baseline = results_sorted[0]

    def _deg(c, b):
        if b is None or c is None or b == 0:
            return None
        return round(((c - b) / b) * 100, 2)

    runs = []
    for r in results_sorted:
        runs.append({
            "id": r.id, "scenario_id": r.scenario_id, "user_count": r.user_count,
            "spawn_rate": r.spawn_rate, "duration": r.duration, "status": r.status,
            "started_at": r.started_at.isoformat() + "Z" if r.started_at else None,
            "finished_at": r.finished_at.isoformat() + "Z" if r.finished_at else None,
            "metrics": {
                "total_requests": r.total_requests, "total_failures": r.total_failures,
                "error_rate": r.error_rate, "rps": r.rps, "avg_response_time": r.avg_response_time,
                "min_response_time": r.min_response_time, "max_response_time": r.max_response_time,
                "p50_response_time": r.p50_response_time, "p75_response_time": r.p75_response_time,
                "p95_response_time": r.p95_response_time, "p99_response_time": r.p99_response_time,
            },
            "degradation": {
                "rps": _deg(r.rps, baseline.rps),
                "avg_response_time": _deg(r.avg_response_time, baseline.avg_response_time),
                "p95_response_time": _deg(r.p95_response_time, baseline.p95_response_time),
                "p99_response_time": _deg(r.p99_response_time, baseline.p99_response_time),
                "error_rate": _deg(r.error_rate, baseline.error_rate),
            } if r.id != baseline.id else None,
        })
    return {"runs": runs, "baseline_id": baseline.id, "comparison_count": len(runs)}

@router.get("/alert-rules")
async def get_alert_rules(scenario_id: Optional[int] = Query(None), user: User = Depends(get_current_user)):
    q = PerformanceAlertRule.query
    if scenario_id:
        q = q.filter_by(scenario_id=scenario_id)
    return [r.to_dict() for r in q.order_by(PerformanceAlertRule.created_at.desc()).all()]


@router.post("/alert-rules", status_code=201)
async def create_alert_rule(data: AlertRuleCreate, user: User = Depends(get_current_user)):
    rule = PerformanceAlertRule(
        name=data.name, description=data.description or "", scenario_id=data.scenario_id,
        p95_threshold=data.p95_threshold if hasattr(data, 'p95_threshold') else None,
        p99_threshold=data.p99_threshold if hasattr(data, 'p99_threshold') else None,
        error_rate_threshold=data.error_rate_threshold if hasattr(data, 'error_rate_threshold') else None,
        rps_min_threshold=data.rps_min_threshold if hasattr(data, 'rps_min_threshold') else None,
        notify_webhook=data.notify_webhook if hasattr(data, 'notify_webhook') else None,
        enabled=data.is_enabled if hasattr(data, 'is_enabled') else True,
    )
    db.session.add(rule)
    db.session.commit()
    return rule.to_dict()


@router.get("/alert-rules/{rule_id}")
async def get_alert_rule(rule_id: int, user: User = Depends(get_current_user)):
    rule = PerformanceAlertRule.query.get(rule_id)
    if not rule:
        raise HTTPException(404, "告警规则不存在")
    return rule.to_dict()


@router.put("/alert-rules/{rule_id}")
async def update_alert_rule(rule_id: int, data: AlertRuleUpdate, user: User = Depends(get_current_user)):
    rule = PerformanceAlertRule.query.get(rule_id)
    if not rule:
        raise HTTPException(404, "告警规则不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(rule, k, v)
    db.session.commit()
    return rule.to_dict()


@router.delete("/alert-rules/{rule_id}")
async def delete_alert_rule(rule_id: int, user: User = Depends(get_current_user)):
    rule = PerformanceAlertRule.query.get(rule_id)
    if not rule:
        raise HTTPException(404, "告警规则不存在")
    db.session.delete(rule)
    db.session.commit()


@router.post("/alert-rules/{rule_id}/evaluate")
async def evaluate_alert_rule(rule_id: int, data: AlertEvaluateRequest, user: User = Depends(get_current_user)):
    from ...services.performance_alert_service import alert_service
    rule = PerformanceAlertRule.query.get(rule_id)
    if not rule:
        raise HTTPException(404, "告警规则不存在")
    alerts = alert_service.evaluate_rules(data.test_result_id)
    return {"alerts": alerts, "triggered_count": len(alerts)}


@router.get("/alert-logs")
async def get_alert_logs(
    rule_id: Optional[int] = Query(None), severity: Optional[str] = Query(None),
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
):
    q = PerformanceAlertLog.query
    if rule_id:
        q = q.filter_by(rule_id=rule_id)
    if severity:
        q = q.filter_by(severity=severity)
    total = q.count()
    items = q.order_by(PerformanceAlertLog.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    return {"items": [l.to_dict() for l in items], "total": total, "page": page, "per_page": per_page}


async def _authenticate_websocket(websocket: WebSocket) -> Optional[int]:
    """从 WebSocket 连接中验证 JWT Token"""
    token = websocket.query_params.get('token')
    if not token:
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


@router.websocket("/ws/perf-test-logs/{scenario_id}")
async def websocket_perf_test_logs(websocket: WebSocket, scenario_id: int):
    user_id = await _authenticate_websocket(websocket)
    if not user_id:
        await websocket.accept()
        await websocket.send_json({"type": "error", "message": "Authentication required"})
        await websocket.close(code=4001)
        return

    await websocket.accept()
    scenario = PerfTestScenario.query.get(scenario_id)
    if not scenario or scenario.user_id != user_id:
        await websocket.send_json({"type": "error", "message": "场景不存在"})
        await websocket.close()
        return
    try:
        while True:
            if scenario.status != "running":
                await websocket.send_json({
                    "type": "complete", "scenario_id": scenario_id,
                    "status": scenario.status, "last_result": scenario.last_result,
                })
                break
            await websocket.send_json({
                "type": "metrics", "scenario_id": scenario_id, "status": scenario.status,
                "avg_response_time": scenario.avg_response_time or 0,
                "max_response_time": scenario.max_response_time or 0,
                "min_response_time": scenario.min_response_time or 0,
                "throughput": scenario.throughput or 0,
                "error_rate": scenario.error_rate or 0,
                "last_result": scenario.last_result or {},
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


@router.post("/ai/generate")
async def generate_perf_script_endpoint(data: Dict[str, Any], user: User = Depends(get_current_user)):
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        raise HTTPException(400, "prompt is required")
    try:
        rc = {
            "AI_ASSISTANT_BASE_URL": os.environ.get("AI_ASSISTANT_BASE_URL", ""),
            "AI_ASSISTANT_API_KEY": os.environ.get("AI_ASSISTANT_API_KEY", ""),
            "AI_ASSISTANT_MODEL": os.environ.get("AI_ASSISTANT_MODEL", ""),
            "AI_ASSISTANT_TIMEOUT": os.environ.get("AI_ASSISTANT_TIMEOUT", "30"),
        }
        if data.get("base_url"):
            rc["AI_ASSISTANT_BASE_URL"] = str(data["base_url"]).strip()
        if data.get("model"):
            rc["AI_ASSISTANT_MODEL"] = str(data["model"]).strip()
        if data.get("api_key"):
            rc["AI_ASSISTANT_API_KEY"] = str(data["api_key"]).strip()
        script_content = generate_test_script(prompt, "perf", rc, user_id=user.id)
        return {"script_content": script_content, "message": "AI 脚本生成成功"}
    except Exception as exc:
        raise HTTPException(500, f"AI 脚本生成失败: {str(exc)}")
