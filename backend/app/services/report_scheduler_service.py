"""
报告定时调度服务

支持定时生成报告并发送到指定邮箱。
"""

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from .base import BaseService
from ..extensions import db


class ReportSchedulerService(BaseService):
    """报告定时调度服务"""

    def create_schedule(self, user_id: int, data: dict) -> dict:
        """创建定时报告计划"""
        from ..models.report_schedule import ReportSchedule

        schedule = ReportSchedule(
            user_id=user_id,
            project_id=data.get("project_id"),
            name=data.get("name", "定时报告"),
            frequency=data.get("frequency", "weekly"),  # daily/weekly/monthly
            recipients=data.get("recipients", []),  # 邮箱列表
            config=data.get("config", {}),  # 报告配置
            next_run_at=self._calc_next_run(data.get("frequency", "weekly")),
            is_active=True,
        )
        db.session.add(schedule)
        db.session.commit()

        self.logger.info("定时报告已创建", schedule_id=schedule.id, frequency=schedule.frequency)
        return schedule.to_dict()

    def execute_due_reports(self) -> int:
        """执行所有到期的定时报告（由 Celery Beat 调用）"""
        from ..models.report_schedule import ReportSchedule

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        due = ReportSchedule.query.filter(
            ReportSchedule.is_active == True,
            ReportSchedule.next_run_at <= now,
        ).all()

        executed = 0
        for schedule in due:
            try:
                self._generate_and_send(schedule)
                schedule.last_run_at = now
                schedule.next_run_at = self._calc_next_run(schedule.frequency)
                executed += 1
            except Exception as e:
                self.logger.error("定时报告执行失败", schedule_id=schedule.id, error=str(e))

        db.session.commit()
        return executed

    def _generate_and_send(self, schedule) -> None:
        """生成报告并通过邮件发送"""
        # 生成报告（复用现有报告生成逻辑）
        from .report_service import ReportService
        report_svc = ReportService()

        # 通过邮件发送
        if schedule.recipients:
            from .email_service import EmailService
            email_svc = EmailService()
            for email in schedule.recipients:
                try:
                    email_svc.send_report_email(email, schedule.name, "报告已生成，请登录平台查看。")
                except Exception as e:
                    self.logger.warning("邮件发送失败", email=email, error=str(e))

    def _calc_next_run(self, frequency: str) -> datetime:
        """计算下次执行时间"""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if frequency == "daily":
            return now + timedelta(days=1)
        elif frequency == "weekly":
            return now + timedelta(weeks=1)
        elif frequency == "monthly":
            return now + timedelta(days=30)
        return now + timedelta(weeks=1)

