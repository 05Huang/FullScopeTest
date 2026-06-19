"""
测试计划服务

管理测试计划的 CRUD、执行轮次、用例结果和通过率趋势。
"""
from datetime import datetime, timezone
from .base import BaseService
from ..extensions import db
from ..models.test_plan import TestPlan, TestPlanRun, TestPlanCaseResult
from ..models.api_test_case import ApiTestCase
from ..utils.exceptions import NotFoundError, ValidationError
from ..utils.org_filter import filter_by_org_projects, get_org_id_for_create
from ..core.logging import get_logger

logger = get_logger(__name__)


class PlanService(BaseService):
    """测试计划服务"""

    # ── 计划 CRUD ────────────────────────────────────────────────────────────

    def create_plan(self, user_id: int, project_id: int, name: str,
                    description: str = '', include_cases: list = None,
                    tags: list = None, organization_id: int = None) -> dict:
        """
        创建测试计划

        Args:
            user_id: 创建者 ID
            project_id: 项目 ID
            name: 计划名称
            description: 描述
            include_cases: 用例列表 [{case_type, case_id}]
            tags: 标签
            organization_id: 组织 ID

        Returns:
            创建的计划字典
        """
        if not name or not name.strip():
            raise ValidationError("计划名称不能为空")

        # 校验 include_cases 格式
        if include_cases:
            for item in include_cases:
                if not isinstance(item, dict) or 'case_type' not in item or 'case_id' not in item:
                    raise ValidationError("用例格式无效，需要 {case_type, case_id}")

        plan = TestPlan(
            project_id=project_id,
            user_id=user_id,
            organization_id=organization_id,
            name=name.strip(),
            description=description,
            include_cases=include_cases or [],
            tags=tags or [],
        )

        with self.transaction():
            self.add(plan)

        logger.info("测试计划已创建", plan_id=plan.id, name=plan.name, project_id=project_id)
        return plan.to_dict()

    def get_plans(self, project_id: int, page: int = 1, per_page: int = 20,
                  status: str = None) -> dict:
        """
        获取项目下的测试计划列表

        Args:
            project_id: 项目 ID
            page: 页码
            per_page: 每页数量
            status: 状态过滤

        Returns:
            分页结果
        """
        query = TestPlan.query.filter_by(project_id=project_id)
        # 组织隔离：确保项目属于当前组织
        query = filter_by_org_projects(query, TestPlan, 'project_id')
        if status:
            query = query.filter_by(status=status)

        total = query.count()
        plans = query.order_by(TestPlan.updated_at.desc()) \
            .offset((page - 1) * per_page) \
            .limit(per_page) \
            .all()

        return {
            'items': [p.to_dict() for p in plans],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
        }

    def get_plan(self, plan_id: int) -> dict:
        """获取计划详情（包含最近轮次）"""
        plan = TestPlan.query.get(plan_id)
        if not plan:
            raise NotFoundError("测试计划", plan_id)
        return plan.to_dict(include_runs=True)

    def update_plan(self, plan_id: int, **kwargs) -> dict:
        """
        更新测试计划

        可更新字段：name, description, include_cases, tags, status
        """
        plan = TestPlan.query.get(plan_id)
        if not plan:
            raise NotFoundError("测试计划", plan_id)

        allowed_fields = {'name', 'description', 'include_cases', 'tags', 'status'}
        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(plan, key, value)

        if plan.name and not plan.name.strip():
            raise ValidationError("计划名称不能为空")

        with self.transaction():
            self.add(plan)  # 触发 updated_at 更新

        logger.info("测试计划已更新", plan_id=plan_id)
        return plan.to_dict()

    def delete_plan(self, plan_id: int):
        """删除测试计划（级联删除轮次和结果）"""
        plan = TestPlan.query.get(plan_id)
        if not plan:
            raise NotFoundError("测试计划", plan_id)

        with self.transaction():
            self.delete(plan)

        logger.info("测试计划已删除", plan_id=plan_id)

    # ── 执行轮次 ─────────────────────────────────────────────────────────────

    def create_run(self, plan_id: int, user_id: int,
                   environment_id: int = None,
                   environment_name: str = '',
                   notes: str = '',
                   triggered_by: str = 'manual') -> dict:
        """
        从测试计划创建执行轮次

        自动根据计划的 include_cases 初始化每个用例的待执行记录。
        """
        plan = TestPlan.query.get(plan_id)
        if not plan:
            raise NotFoundError("测试计划", plan_id)

        cases = plan.include_cases or []
        if not cases:
            raise ValidationError("计划中没有关联用例，无法创建执行轮次")

        run = TestPlanRun(
            plan_id=plan_id,
            user_id=user_id,
            status='pending',
            total_cases=len(cases),
            environment_id=environment_id,
            environment_name=environment_name,
            notes=notes,
            triggered_by=triggered_by,
            started_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        with self.transaction():
            self.add(run)
            self.flush()

            # 为每个用例创建待执行记录
            for case_ref in cases:
                case_type = case_ref.get('case_type', 'api')
                case_id = case_ref.get('case_id')
                case_name = self._resolve_case_name(case_type, case_id)
                result = TestPlanCaseResult(
                    run_id=run.id,
                    case_type=case_type,
                    case_id=case_id,
                    case_name=case_name,
                    status='pending',
                )
                self.add(result)

            # 更新计划统计
            plan.total_runs = (plan.total_runs or 0) + 1
            self.add(plan)

        logger.info("执行轮次已创建", run_id=run.id, plan_id=plan_id, total_cases=len(cases))
        return run.to_dict(include_cases=True)

    def get_runs(self, plan_id: int, page: int = 1, per_page: int = 20) -> dict:
        """获取计划的执行轮次列表"""
        plan = TestPlan.query.get(plan_id)
        if not plan:
            raise NotFoundError("测试计划", plan_id)

        query = TestPlanRun.query.filter_by(plan_id=plan_id)
        total = query.count()
        runs = query.order_by(TestPlanRun.created_at.desc()) \
            .offset((page - 1) * per_page) \
            .limit(per_page) \
            .all()

        return {
            'items': [r.to_dict() for r in runs],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
        }

    def get_run(self, run_id: int) -> dict:
        """获取执行轮次详情（包含用例结果）"""
        run = TestPlanRun.query.get(run_id)
        if not run:
            raise NotFoundError("执行轮次", run_id)
        return run.to_dict(include_cases=True)

    def update_case_result(self, run_id: int, case_type: str, case_id: int,
                           status: str, duration: float = None,
                           error_message: str = None,
                           result_detail: dict = None,
                           test_run_id: int = None) -> dict:
        """
        更新单个用例的执行结果

        在测试执行完成后调用，更新用例状态并刷新轮次统计。
        """
        result = TestPlanCaseResult.query.filter_by(
            run_id=run_id, case_type=case_type, case_id=case_id,
        ).first()
        if not result:
            raise NotFoundError("用例结果", f"{case_type}:{case_id}")

        result.status = status
        result.duration = duration
        result.error_message = error_message
        result.result_detail = result_detail
        result.test_run_id = test_run_id
        result.executed_at = datetime.now(timezone.utc).replace(tzinfo=None)

        with self.transaction():
            self.add(result)
            # 刷新轮次统计
            self._refresh_run_stats(run_id)

        return result.to_dict()

    def complete_run(self, run_id: int) -> dict:
        """标记执行轮次完成"""
        run = TestPlanRun.query.get(run_id)
        if not run:
            raise NotFoundError("执行轮次", run_id)

        run.status = 'completed'
        run.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        if run.started_at:
            run.duration = (run.finished_at - run.started_at).total_seconds()

        with self.transaction():
            self._refresh_run_stats(run_id)
            self.add(run)

            # 更新计划的最后执行信息
            plan = TestPlan.query.get(run.plan_id)
            if plan:
                plan.last_run_at = run.finished_at
                plan.last_pass_rate = run.pass_rate
                self.add(plan)

        logger.info("执行轮次已完成", run_id=run_id, pass_rate=run.pass_rate)
        return run.to_dict()

    def get_pass_rate_trend(self, plan_id: int, limit: int = 20) -> list:
        """
        获取计划的通过率趋势

        Returns:
            [{run_id, pass_rate, created_at, total_cases, passed, failed}]
        """
        runs = TestPlanRun.query.filter_by(plan_id=plan_id) \
            .filter(TestPlanRun.status == 'completed') \
            .order_by(TestPlanRun.created_at.asc()) \
            .limit(limit) \
            .all()

        return [{
            'run_id': r.id,
            'pass_rate': r.pass_rate,
            'total_cases': r.total_cases,
            'passed': r.passed,
            'failed': r.failed,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        } for r in runs]

    # ── 内部工具 ─────────────────────────────────────────────────────────────

    def _refresh_run_stats(self, run_id: int):
        """刷新执行轮次的统计信息（兼容 SQLite 和 PostgreSQL）"""
        results = TestPlanCaseResult.query.filter_by(run_id=run_id).all()

        run = TestPlanRun.query.get(run_id)
        if run:
            run.total_cases = len(results)
            run.passed = sum(1 for r in results if r.status == 'passed')
            run.failed = sum(1 for r in results if r.status == 'failed')
            run.skipped = sum(1 for r in results if r.status == 'skipped')
            run.error = sum(1 for r in results if r.status == 'error')
            run.pass_rate = round(run.passed / run.total_cases * 100, 2) if run.total_cases > 0 else 0

    def _resolve_case_name(self, case_type: str, case_id: int) -> str:
        """根据用例类型和 ID 解析用例名称"""
        try:
            if case_type == 'api':
                case = ApiTestCase.query.get(case_id)
                return case.name if case else f'API Case #{case_id}'
        except Exception:
            pass
        return f'{case_type} Case #{case_id}'