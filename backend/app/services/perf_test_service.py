"""
性能测试 Service

处理性能测试场景的 CRUD 操作
"""

from datetime import datetime

from .base import BaseService
from ..extensions import db
from ..models.perf_test_scenario import PerfTestScenario
from ..utils.exceptions import NotFoundError, ValidationError


class PerfTestService(BaseService):

    def get_scenarios(self, user_id: int, project_id: int = None):
        """获取性能测试场景列表"""
        query = PerfTestScenario.query.filter_by(user_id=user_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        scenarios = query.order_by(PerfTestScenario.created_at.desc()).all()
        return [s.to_dict() for s in scenarios]

    def get_scenario(self, scenario_id: int, user_id: int):
        """获取场景详情"""
        scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
        if not scenario:
            raise NotFoundError("场景", scenario_id)
        return scenario.to_dict()

    def create_scenario(self, user_id: int, data: dict):
        """创建性能测试场景"""
        if not data.get("name"):
            raise ValidationError("name is required")
        if not data.get("target_url"):
            raise ValidationError("target_url is required")

        scenario = PerfTestScenario(
            name=data["name"],
            description=data.get("description", ""),
            target_url=data["target_url"],
            method=data.get("method", "GET"),
            headers=data.get("headers", {}),
            body=data.get("body"),
            user_count=data.get("user_count", 10),
            spawn_rate=data.get("spawn_rate", 1),
            duration=data.get("duration", 60),
            project_id=data.get("project_id"),
            user_id=user_id
        )
        with self.transaction():
            self.add(scenario)
            self.flush()
            result = scenario.to_dict()
        return result

    def update_scenario(self, scenario_id: int, user_id: int, data: dict):
        """更新性能测试场景"""
        scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
        if not scenario:
            raise NotFoundError("场景", scenario_id)

        updatable_fields = [
            "name", "description", "target_url", "method", "headers", "body",
            "user_count", "spawn_rate", "duration", "project_id"
        ]
        for field in updatable_fields:
            if field in data:
                setattr(scenario, field, data[field])

        with self.transaction():
            result = scenario.to_dict()
        return result

    def delete_scenario(self, scenario_id: int, user_id: int):
        """删除性能测试场景"""
        scenario = PerfTestScenario.query.filter_by(id=scenario_id, user_id=user_id).first()
        if not scenario:
            raise NotFoundError("场景", scenario_id)

        with self.transaction():
            self.delete(scenario)
