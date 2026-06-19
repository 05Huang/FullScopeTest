"""FastAPI Web 自动化测试模块

提供基于 Playwright 的 Web UI 测试执行路由：
- POST /run: 触发 Web 测试脚本执行
- GET /results/{run_id}: 获取测试运行结果
- GET /visual-diffs/{run_id}: 获取视觉差异记录
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ...core.logging import get_logger
from ...extensions import db
from ...models.test_run import TestRun
from ...models.test_report import TestReport
from ...models.user import User
from ...models.visual_diff import VisualDiff
from .auth import get_current_user

logger = get_logger(__name__)

router = APIRouter(tags=["ui-tests"])


# ==================== Pydantic Schemas ====================


class RunWebRequest(BaseModel):
    """触发 Web 测试执行"""
    script_id: int = Field(..., description="Web 测试脚本 ID")


class RunWebResponse(BaseModel):
    """Web 测试触发响应"""
    message: str
    task_id: Optional[str] = None
    script_id: int


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


class VisualDiffResponse(BaseModel):
    """视觉差异记录"""
    id: int
    test_run_id: int
    test_case_id: int
    test_type: Optional[str] = None
    step_index: Optional[int] = None
    step_name: Optional[str] = None
    current_image_path: Optional[str] = None
    diff_image_path: Optional[str] = None
    diff_percentage: Optional[float] = None
    diff_pixel_count: Optional[int] = None
    total_pixel_count: Optional[int] = None
    similarity_score: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


# ==================== Routes ====================


@router.post("/run", response_model=RunWebResponse)
async def run_web_test(
    data: RunWebRequest,
    user: User = Depends(get_current_user),
):
    """
    触发 Web 测试脚本执行

    通过 Celery 异步执行 Playwright 测试脚本。
    """
    from ...models.web_test_script import WebTestScript
    from ...tasks import run_web_test_task

    script = WebTestScript.query.filter_by(
        id=data.script_id, user_id=user.id
    ).first()
    if not script:
        raise HTTPException(status_code=404, detail="脚本不存在")

    if script.status == "running":
        raise HTTPException(status_code=400, detail="脚本正在运行中")

    try:
        task = run_web_test_task.apply_async(
            args=[data.script_id, user.id],
            task_id=f"web_test_{data.script_id}_{user.id}",
        )

        script.status = "running"
        script.last_status = "running"
        script.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.session.commit()

        return RunWebResponse(
            message="测试已提交，正在后台执行",
            task_id=task.id,
            script_id=data.script_id,
        )
    except Exception as e:
        logger.error("提交 Web 测试失败", error=str(e))
        raise HTTPException(status_code=500, detail=f"提交失败: {str(e)}")


@router.get("/results/{run_id}", response_model=TestRunDetailResponse)
async def get_web_test_results(
    run_id: int,
    user: User = Depends(get_current_user),
):
    """获取 Web 测试运行结果详情"""
    test_run = TestRun.query.get(run_id)
    if not test_run:
        raise HTTPException(status_code=404, detail="测试运行不存在")

    report_data = None
    if test_run.report_id:
        report = TestReport.query.get(test_run.report_id)
        if report:
            report_data = report.to_dict()

    return TestRunDetailResponse(
        id=test_run.id,
        project_id=test_run.project_id,
        test_type=test_run.test_type,
        test_object_id=test_run.test_object_id,
        test_object_name=test_run.test_object_name,
        status=test_run.status,
        total_cases=test_run.total_cases,
        passed=test_run.passed,
        failed=test_run.failed,
        skipped=test_run.skipped,
        duration=test_run.duration,
        pass_rate=(
            round(test_run.passed / test_run.total_cases * 100, 2)
            if test_run.total_cases and test_run.total_cases > 0
            else 0
        ),
        started_at=test_run.started_at.isoformat() if test_run.started_at else None,
        finished_at=test_run.finished_at.isoformat() if test_run.finished_at else None,
        environment_id=test_run.environment_id,
        environment_name=test_run.environment_name,
        triggered_by=test_run.triggered_by,
        results=test_run.results,
        report=report_data,
    )


@router.get("/visual-diffs/{run_id}", response_model=List[VisualDiffResponse])
async def get_visual_diffs(
    run_id: int,
    status: Optional[str] = Query(None, description="按状态过滤"),
    user: User = Depends(get_current_user),
):
    """获取指定测试运行的视觉差异记录"""
    test_run = TestRun.query.get(run_id)
    if not test_run:
        raise HTTPException(status_code=404, detail="测试运行不存在")

    query = VisualDiff.query.filter_by(test_run_id=run_id)
    if status:
        query = query.filter_by(status=status)

    diffs = query.order_by(VisualDiff.step_index).all()

    return [
        VisualDiffResponse(
            id=d.id,
            test_run_id=d.test_run_id,
            test_case_id=d.test_case_id,
            test_type=d.test_type,
            step_index=d.step_index,
            step_name=d.step_name,
            current_image_path=d.current_image_path,
            diff_image_path=d.diff_image_path,
            diff_percentage=d.diff_percentage,
            diff_pixel_count=d.diff_pixel_count,
            total_pixel_count=d.total_pixel_count,
            similarity_score=d.similarity_score,
            status=d.status,
            created_at=d.created_at.isoformat() if d.created_at else None,
        )
        for d in diffs
    ]
