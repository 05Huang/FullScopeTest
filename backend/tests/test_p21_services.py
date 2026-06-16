"""
P21 商业化运营服务测试
"""

import pytest


class TestQuotaEnforcement:
    """配额执行服务测试"""

    def test_check_quota_no_record(self, app):
        """无配额记录时应允许"""
        with app.app_context():
            from app.services.quota_enforcement_service import QuotaService
            svc = QuotaService()
            assert svc.check_quota(org_id=99999, resource_type="projects") is True

    def test_quota_exceeded(self, app):
        """配额超限应抛出异常"""
        with app.app_context():
            from app.extensions import db
            from app.models.quota import Quota
            from app.services.quota_enforcement_service import QuotaService, QuotaExceededError

            quota = Quota(organization_id=1, resource_type="projects", limit=5, used=5)
            db.session.add(quota)
            db.session.commit()

            svc = QuotaService()
            with pytest.raises(QuotaExceededError):
                svc.check_quota(org_id=1, resource_type="projects", amount=1)

    def test_quota_unlimited(self, app):
        """配额 -1 表示无限制"""
        with app.app_context():
            from app.extensions import db
            from app.models.quota import Quota
            from app.services.quota_enforcement_service import QuotaService

            quota = Quota(organization_id=1, resource_type="ai_calls_monthly", limit=-1, used=999999)
            db.session.add(quota)
            db.session.commit()

            svc = QuotaService()
            assert svc.check_quota(org_id=1, resource_type="ai_calls_monthly") is True

    def test_get_quota_usage(self, app):
        """获取配额使用情况"""
        with app.app_context():
            from app.extensions import db
            from app.models.quota import Quota
            from app.services.quota_enforcement_service import QuotaService

            quota = Quota(organization_id=88888, resource_type="projects", limit=10, used=3)
            db.session.add(quota)
            db.session.commit()

            svc = QuotaService()
            usage = svc.get_quota_usage(org_id=88888)
            assert "projects" in usage
            assert usage["projects"]["used"] == 3
            assert usage["projects"]["remaining"] == 7


class TestActivityTracker:
    """用户行为追踪测试"""

    def test_track_event(self, app):
        """记录事件"""
        with app.app_context():
            from app.services.activity_tracking_service import ActivityTracker
            tracker = ActivityTracker()
            tracker.track(user_id=1, event_type="feature_use", event_name="create_project")
            events = tracker.get_events(user_id=1)
            assert len(events) == 1
            assert events[0]["event_name"] == "create_project"

    def test_get_dau(self, app):
        """获取日活用户数"""
        with app.app_context():
            from app.services.activity_tracking_service import ActivityTracker
            tracker = ActivityTracker()
            tracker.track(user_id=1, event_type="page_view", event_name="dashboard")
            tracker.track(user_id=2, event_type="page_view", event_name="dashboard")
            tracker.track(user_id=1, event_type="feature_use", event_name="create_case")
            assert tracker.get_dau() == 2

    def test_feature_usage(self, app):
        """获取功能使用频率"""
        with app.app_context():
            from app.services.activity_tracking_service import ActivityTracker
            tracker = ActivityTracker()
            tracker.track(user_id=1, event_type="feature_use", event_name="create_case")
            tracker.track(user_id=1, event_type="feature_use", event_name="create_case")
            tracker.track(user_id=1, event_type="feature_use", event_name="run_test")
            usage = tracker.get_feature_usage()
            assert usage["create_case"] == 2
            assert usage["run_test"] == 1

    def test_filter_by_event_type(self, app):
        """按事件类型过滤"""
        with app.app_context():
            from app.services.activity_tracking_service import ActivityTracker
            tracker = ActivityTracker()
            tracker.track(user_id=1, event_type="page_view", event_name="dashboard")
            tracker.track(user_id=1, event_type="feature_use", event_name="create_case")
            events = tracker.get_events(event_type="feature_use")
            assert len(events) == 1


class TestAdminService:
    """管理员服务测试"""

    def test_platform_overview(self, app, client):
        """平台概览应返回正确结构"""
        with app.app_context():
            from app.services.admin_service import AdminService
            svc = AdminService()
            overview = svc.get_platform_overview()
            assert "total_users" in overview
            assert "active_users" in overview
            assert "total_organizations" in overview
            assert "total_projects" in overview

    def test_tenant_list(self, app):
        """租户列表应返回列表"""
        with app.app_context():
            from app.services.admin_service import AdminService
            svc = AdminService()
            tenants = svc.get_tenant_list()
            assert isinstance(tenants, list)
