"""
标签与优先级管理服务测试
"""

import pytest


class TestTagManagerService:
    """TagManagerService 测试"""

    def test_tag_stats_empty(self, app):
        """无用例时标签统计应为空"""
        with app.app_context():
            from app.services.tag_manager_service import TagManagerService
            svc = TagManagerService()
            stats = svc.get_tag_stats(project_id=99999)
            assert stats == []

    def test_tag_stats_with_cases(self, app, client):
        """有用例时标签统计应正确"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.tag_manager_service import TagManagerService

            project = Project(name="Tag测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            cases = [
                ApiTestCase(name="t1", method="GET", url="/a", project_id=project.id, user_id=1, tags=["smoke", "auth"]),
                ApiTestCase(name="t2", method="GET", url="/b", project_id=project.id, user_id=1, tags=["smoke"]),
                ApiTestCase(name="t3", method="GET", url="/c", project_id=project.id, user_id=1, tags=["regression"]),
            ]
            for c in cases:
                db.session.add(c)
            db.session.commit()

            svc = TagManagerService()
            stats = svc.get_tag_stats(project_id=project.id)
            assert len(stats) > 0
            smoke = next((s for s in stats if s["tag"] == "smoke"), None)
            assert smoke is not None
            assert smoke["count"] == 2

    def test_priority_stats(self, app, client):
        """优先级统计应包含所有优先级"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.tag_manager_service import TagManagerService

            project = Project(name="Prio测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            db.session.add(ApiTestCase(name="t1", method="GET", url="/a", project_id=project.id, user_id=1, priority=1))
            db.session.add(ApiTestCase(name="t2", method="GET", url="/b", project_id=project.id, user_id=1, priority=2))
            db.session.commit()

            svc = TagManagerService()
            stats = svc.get_priority_stats(project_id=project.id)
            assert stats["total"] == 2
            assert "1" in stats["by_priority"]
            assert "2" in stats["by_priority"]

    def test_filter_by_tags_any(self, app, client):
        """按标签过滤（任一匹配）"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.tag_manager_service import TagManagerService

            project = Project(name="Filter测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            db.session.add(ApiTestCase(name="t1", method="GET", url="/a", project_id=project.id, user_id=1, tags=["smoke"]))
            db.session.add(ApiTestCase(name="t2", method="GET", url="/b", project_id=project.id, user_id=1, tags=["regression"]))
            db.session.commit()

            svc = TagManagerService()
            result = svc.filter_by_tags(["smoke"], project_id=project.id)
            assert len(result) == 1
            assert result[0]["name"] == "t1"

    def test_filter_by_tags_all(self, app, client):
        """按标签过滤（全部匹配）"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.tag_manager_service import TagManagerService

            project = Project(name="FilterAll测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            db.session.add(ApiTestCase(name="t1", method="GET", url="/a", project_id=project.id, user_id=1, tags=["smoke", "auth"]))
            db.session.add(ApiTestCase(name="t2", method="GET", url="/b", project_id=project.id, user_id=1, tags=["smoke"]))
            db.session.commit()

            svc = TagManagerService()
            result = svc.filter_by_tags(["smoke", "auth"], project_id=project.id, match_all=True)
            assert len(result) == 1
            assert result[0]["name"] == "t1"

    def test_filter_by_priority(self, app, client):
        """按优先级过滤"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase
            from app.services.tag_manager_service import TagManagerService

            project = Project(name="PrioFilter测试", owner_id=1)
            db.session.add(project)
            db.session.commit()

            db.session.add(ApiTestCase(name="t1", method="GET", url="/a", project_id=project.id, user_id=1, priority=1))
            db.session.add(ApiTestCase(name="t2", method="GET", url="/b", project_id=project.id, user_id=1, priority=3))
            db.session.commit()

            svc = TagManagerService()
            result = svc.filter_by_priority([1], project_id=project.id)
            assert len(result) == 1
            assert result[0]["name"] == "t1"
