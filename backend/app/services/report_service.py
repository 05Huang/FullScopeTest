"""
报告 Service

处理测试报告和执行记录的 CRUD 操作
"""

from datetime import datetime, timedelta
from sqlalchemy import func

from .base import BaseService
from ..extensions import db
from ..models.test_run import TestRun
from ..models.test_report import TestReport
from ..utils.exceptions import NotFoundError, ValidationError


class ReportService(BaseService):

    def get_test_runs(self, user_id: int, project_id: int = None, test_type: str = None,
                      status: str = None, page: int = 1, per_page: int = 20):
        """获取测试执行记录列表（组织级过滤）"""
        from ..middleware.tenant import get_current_organization_id
        from ..models.project import Project

        org_id = get_current_organization_id()

        query = TestRun.query

        # 组织级过滤
        if org_id:
            query = query.join(Project, TestRun.project_id == Project.id).filter(
                Project.organization_id == org_id
            )

        if project_id:
            query = query.filter(TestRun.project_id == project_id)
        if test_type:
            query = query.filter(TestRun.test_type == test_type)
        if status:
            query = query.filter(TestRun.status == status)

        total = query.count()
        runs = query.order_by(TestRun.created_at.desc()) \
            .offset((page - 1) * per_page) \
            .limit(per_page) \
            .all()

        return {
            "items": [r.to_dict() for r in runs],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    def get_test_run(self, run_id: int):
        """获取执行记录详情"""
        run = TestRun.query.get(run_id)
        if not run:
            raise NotFoundError("执行记录", run_id)
        return run.to_dict()

    def delete_test_run(self, run_id: int):
        """删除执行记录"""
        run = TestRun.query.get(run_id)
        if not run:
            raise NotFoundError("执行记录", run_id)

        with self.transaction():
            self.delete(run)

    def get_dashboard_stats(self, project_id: int = None):
        """获取仪表盘统计数据"""
        query = TestRun.query
        if project_id:
            query = query.filter_by(project_id=project_id)

        # 获取各类测试的统计
        api_tests = query.filter_by(test_type="api").all()
        web_tests = query.filter_by(test_type="web").all()
        perf_tests = query.filter_by(test_type="performance").all()

        def calc_stats(runs):
            total = len(runs)
            passed = sum(1 for r in runs if r.status == "success")
            failed = sum(1 for r in runs if r.status == "failed")
            return {"total": total, "passed": passed, "failed": failed}

        # 最近的执行记录
        recent_runs = TestRun.query
        if project_id:
            recent_runs = recent_runs.filter_by(project_id=project_id)
        recent_runs = recent_runs.order_by(TestRun.created_at.desc()).limit(10).all()

        return {
            "api_tests": calc_stats(api_tests),
            "web_tests": calc_stats(web_tests),
            "perf_tests": {
                "total": len(perf_tests),
                "running": sum(1 for r in perf_tests if r.status == "running")
            },
            "recent_runs": [r.to_dict() for r in recent_runs]
        }
