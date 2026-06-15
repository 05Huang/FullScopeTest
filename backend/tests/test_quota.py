"""
多租户资源配额测试

覆盖：配额初始化、查询、消耗、释放、更新、计划默认值
"""
import uuid


class TestQuotaDefaults:
    """默认配额计划测试"""

    def test_free_plan_defaults(self):
        from app.services.quota_service import DEFAULT_PLANS
        free = DEFAULT_PLANS['free']
        assert free['projects'] == 5
        assert free['test_cases'] == 100
        assert free['parallel_executions'] == 1
        assert free['ai_calls_monthly'] == 100
        assert free['storage_mb'] == 500

    def test_pro_plan_defaults(self):
        from app.services.quota_service import DEFAULT_PLANS
        pro = DEFAULT_PLANS['pro']
        assert pro['projects'] == 50
        assert pro['test_cases'] == 1000

    def test_enterprise_plan_unlimited(self):
        from app.services.quota_service import DEFAULT_PLANS
        ent = DEFAULT_PLANS['enterprise']
        for val in ent.values():
            assert val == -1


class TestQuotaInitAndQuery:
    """配额初始化和查询测试"""

    def test_init_quota_creates_all_resource_types(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, get_all_quotas

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg", slug=f"testorg-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'free')
            quotas = get_all_quotas(org.id)
            assert len(quotas) == 5
            types = {q['resource_type'] for q in quotas}
            assert types == {'projects', 'test_cases', 'parallel_executions', 'ai_calls_monthly', 'storage_mb'}

            # 清理
            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()

    def test_get_quota_returns_correct_limit(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, get_quota

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg2", slug=f"testorg2-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'free')
            q = get_quota(org.id, 'projects')
            assert q is not None
            assert q.limit == 5
            assert q.used == 0

            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()


class TestQuotaConsumeAndRelease:
    """配额消耗和释放测试"""

    def test_consume_quota_success(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, consume_quota, get_quota

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg3", slug=f"testorg3-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'free')
            result = consume_quota(org.id, 'projects', 1)
            assert result is True
            q = get_quota(org.id, 'projects')
            assert q.used == 1

            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()

    def test_consume_quota_exhausted(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, consume_quota

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q4@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg4", slug=f"testorg4-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'free')
            # 消耗完所有 5 个项目配额
            for _ in range(5):
                assert consume_quota(org.id, 'projects', 1) is True
            # 第 6 次应失败
            assert consume_quota(org.id, 'projects', 1) is False

            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()

    def test_release_quota(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, consume_quota, release_quota, get_quota

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q5@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg5", slug=f"testorg5-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'free')
            consume_quota(org.id, 'projects', 3)
            release_quota(org.id, 'projects', 2)
            q = get_quota(org.id, 'projects')
            assert q.used == 1

            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()

    def test_enterprise_unlimited_consume(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, consume_quota

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q6@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg6", slug=f"testorg6-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'enterprise')
            # 企业版不限量，消耗 1000 次也应成功
            for _ in range(1000):
                assert consume_quota(org.id, 'ai_calls_monthly', 1) is True

            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()


class TestQuotaUpdate:
    """管理员配额修改测试"""

    def test_update_quota_limit(self, app):
        from app.extensions import db
        from app.models.organization import Organization
        from app.models.user import User
        from app.services.quota_service import init_quota_for_organization, update_quota, get_quota

        with app.app_context():
            user = User(username=f"quota_{uuid.uuid4().hex[:6]}", email="q7@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            org = Organization(name="TestOrg7", slug=f"testorg7-{uuid.uuid4().hex[:6]}", owner_id=user.id)
            db.session.add(org)
            db.session.commit()

            init_quota_for_organization(org.id, 'free')
            update_quota(org.id, 'projects', 100, 'pro')
            q = get_quota(org.id, 'projects')
            assert q.limit == 100
            assert q.plan == 'pro'

            from app.models.quota import Quota
            Quota.query.filter_by(organization_id=org.id).delete()
            db.session.delete(org)
            db.session.delete(user)
            db.session.commit()

    def test_check_quota_no_config_returns_true(self, app):
        """未配置配额时默认允许（向后兼容）"""
        from app.services.quota_service import check_quota
        with app.app_context():
            assert check_quota(99999, 'projects') is True
