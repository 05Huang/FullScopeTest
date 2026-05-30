"""
Prompt 版本管理服务测试

测试 PromptVersionService 的 CRUD、A/B 测试选择、统计更新功能
"""

import uuid
import pytest
from datetime import datetime


def _unique_feature(prefix='test_feat'):
    """生成唯一的 feature 名称，避免跨测试数据冲突"""
    return f'{prefix}_{uuid.uuid4().hex[:8]}'


class TestPromptVersionCRUD:
    """PromptVersion CRUD 操作测试"""

    def test_create_version(self, app):
        """测试创建 Prompt 版本"""
        from app.services.ai.prompt_version_service import prompt_version_service
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            feature = _unique_feature('crud')
            pv = prompt_version_service.create_version(
                feature=feature,
                name='baseline',
                system_prompt='You are a test assistant.',
                is_active=True,
                created_by=1,
            )

            assert pv.id is not None
            assert pv.feature == feature
            assert pv.name == 'baseline'
            assert pv.version == 1
            assert pv.is_active is True
            assert pv.system_prompt == 'You are a test assistant.'
            assert pv.created_by == 1

    def test_create_version_auto_increments(self, app):
        """测试版本号自动递增"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            feature = _unique_feature('incr')
            pv1 = prompt_version_service.create_version(
                feature=feature, name='inc-v1', system_prompt='prompt 1',
            )
            pv2 = prompt_version_service.create_version(
                feature=feature, name='inc-v2', system_prompt='prompt 2',
            )
            pv3 = prompt_version_service.create_version(
                feature=_unique_feature('incr'), name='inc-v1', system_prompt='prompt copilot',
            )

            # 版本号应在现有基础上递增（独立 feature 从 1 开始）
            assert pv1.version == 1
            assert pv2.version == 2
            # 不同 feature 的版本号独立
            assert pv3.version == 1

    def test_get_by_id(self, app):
        """测试按 ID 查询"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            pv = prompt_version_service.create_version(
                feature=_unique_feature('getid'), name='test', system_prompt='prompt',
            )
            found = prompt_version_service.get_by_id(pv.id)
            assert found is not None
            assert found.id == pv.id

            not_found = prompt_version_service.get_by_id(99999)
            assert not_found is None

    def test_get_active_versions(self, app):
        """测试获取激活版本列表"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            feature = _unique_feature('active')

            prompt_version_service.create_version(
                feature=feature, name='active-1', system_prompt='p1', is_active=True,
            )
            prompt_version_service.create_version(
                feature=feature, name='active-2', system_prompt='p2', is_active=True,
            )
            prompt_version_service.create_version(
                feature=feature, name='inactive-1', system_prompt='p3', is_active=False,
            )

            active = prompt_version_service.get_active_versions(feature)
            assert len(active) == 2

            # 不同 feature 不影响
            feature2 = _unique_feature('active2')
            prompt_version_service.create_version(
                feature=feature2, name='cop-1', system_prompt='p-cop', is_active=True,
            )
            active2 = prompt_version_service.get_active_versions(feature2)
            assert len(active2) == 1

    def test_list_versions(self, app):
        """测试分页列表查询"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            feature = _unique_feature('list')
            for i in range(3):
                prompt_version_service.create_version(
                    feature=feature, name=f'list-v{i}', system_prompt=f'p{i}',
                )

            result = prompt_version_service.list_versions(feature=feature, page=1, per_page=2)
            assert result['total'] == 3
            assert len(result['items']) == 2
            assert result['pages'] == 2

    def test_update_version(self, app):
        """测试更新 Prompt 版本"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            pv = prompt_version_service.create_version(
                feature=_unique_feature('upd'), name='v1', system_prompt='old prompt',
            )

            updated = prompt_version_service.update_version(
                pv.id,
                name='v1-updated',
                system_prompt='new prompt',
                temperature=0.5,
            )

            assert updated.name == 'v1-updated'
            assert updated.system_prompt == 'new prompt'
            assert updated.temperature == 0.5

    def test_update_version_not_found(self, app):
        """测试更新不存在的版本"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            result = prompt_version_service.update_version(99999, name='x')
            assert result is None

    def test_deactivate_version(self, app):
        """测试停用版本"""
        from app.services.ai.prompt_version_service import prompt_version_service
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            pv = prompt_version_service.create_version(
                feature=_unique_feature('deact'), name='v1', system_prompt='p', is_active=True,
            )

            ok = prompt_version_service.deactivate_version(pv.id)
            assert ok is True

            refreshed = PromptVersion.query.get(pv.id)
            assert refreshed.is_active is False
            assert refreshed.deactivated_at is not None

    def test_deactivate_version_not_found(self, app):
        """测试停用不存在的版本"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            ok = prompt_version_service.deactivate_version(99999)
            assert ok is False


class TestABTestSelection:
    """A/B 测试选择功能测试"""

    def test_select_single_version(self, app):
        """测试只有一个激活版本时直接返回"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            feature = _unique_feature('ab_single')
            pv = prompt_version_service.create_version(
                feature=feature, name='single-version', system_prompt='p', is_active=True,
            )

            selected = prompt_version_service.select_version_for_ab_test(feature)
            assert selected is not None
            assert selected.feature == feature

    def test_select_by_weight(self, app):
        """测试按权重选择（多版本）"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            feature = _unique_feature('ab_weight')
            pv_a = prompt_version_service.create_version(
                feature=feature, name='w-A', system_prompt='pa',
                is_active=True, traffic_weight=0.9,
            )
            pv_b = prompt_version_service.create_version(
                feature=feature, name='w-B', system_prompt='pb',
                is_active=True, traffic_weight=0.1,
            )

            # 多次选择，统计分布
            counts = {pv_a.id: 0, pv_b.id: 0}
            for _ in range(200):
                selected = prompt_version_service.select_version_for_ab_test(feature)
                if selected.id in counts:
                    counts[selected.id] += 1

            # A 的权重是 B 的 9 倍，所以 A 应该被选中更多次
            assert counts[pv_a.id] > counts[pv_b.id]

    def test_select_no_active_versions(self, app):
        """测试没有激活版本时返回 None"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            import uuid
            unique_feature = f'no_active_{uuid.uuid4().hex[:8]}'
            prompt_version_service.create_version(
                feature=unique_feature, name='inactive-only', system_prompt='p', is_active=False,
            )

            selected = prompt_version_service.select_version_for_ab_test(unique_feature)
            assert selected is None


class TestStatsRefresh:
    """统计刷新功能测试"""

    def test_refresh_stats(self, app):
        """测试刷新单个版本统计"""
        from app.extensions import db
        from app.services.ai.prompt_version_service import prompt_version_service
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            feature = _unique_feature('stats')
            pv = prompt_version_service.create_version(
                feature=feature, name='v1', system_prompt='p', is_active=True,
            )

            # 模拟调用日志
            for i in range(5):
                log = AIInvocationLog(
                    feature=feature,
                    prompt_version_id=pv.id,
                    prompt='test prompt',
                    model_name='gpt-4',
                    success=i < 3,  # 3 成功 2 失败
                    latency_ms=1000 + i * 100,
                    total_tokens=50 + i * 10,
                    cost_estimate=0.001 * (i + 1),
                )
                db.session.add(log)
            db.session.commit()

            refreshed = prompt_version_service.refresh_stats(pv.id)
            assert refreshed is not None
            assert refreshed.total_invocations == 5
            assert refreshed.success_count == 3
            assert refreshed.failure_count == 2
            assert refreshed.avg_latency_ms > 0
            assert refreshed.avg_tokens > 0

    def test_refresh_all_stats(self, app):
        """测试批量刷新统计"""
        from app.services.ai.prompt_version_service import prompt_version_service
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            f1 = _unique_feature('rall')
            f2 = _unique_feature('rall')
            prompt_version_service.create_version(
                feature=f1, name='refresh-v1', system_prompt='p1',
            )
            prompt_version_service.create_version(
                feature=f2, name='refresh-v1', system_prompt='p2',
            )

            count = prompt_version_service.refresh_all_stats()
            assert count >= 2  # At least the 2 we just created

    def test_refresh_stats_not_found(self, app):
        """测试刷新不存在版本的统计"""
        from app.services.ai.prompt_version_service import prompt_version_service

        with app.app_context():
            result = prompt_version_service.refresh_stats(99999)
            assert result is None


class TestPromptVersionAPI:
    """Prompt 版本 API 接口测试"""

    def _get_auth_header(self, app, client):
        """获取认证 header（使用 unique 用户名避免冲突）"""
        import uuid
        unique_suffix = uuid.uuid4().hex[:8]
        username = f'pv_test_{unique_suffix}'
        email = f'pv_{unique_suffix}@test.com'

        with app.app_context():
            from app.extensions import db
            from app.models.user import User
            from werkzeug.security import generate_password_hash

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash('test123'),
                role='admin',
            )
            db.session.add(user)
            db.session.commit()

        resp = client.post('/api/v1/auth/login', json={
            'username': username,
            'password': 'test123',
        })
        token = resp.get_json().get('data', {}).get('access_token', '')
        return {'Authorization': f'Bearer {token}'}

    def test_list_prompt_versions_empty(self, app, client):
        """测试列表接口（使用不存在的 feature 过滤得到空结果）"""
        headers = self._get_auth_header(app, client)
        resp = client.get('/api/v1/ai/prompt-versions?feature=nonexistent_feature_xyz', headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['code'] == 200
        assert data['data']['pagination']['total'] == 0

    def test_create_prompt_version(self, app, client):
        """测试创建 Prompt 版本"""
        headers = self._get_auth_header(app, client)
        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'copilot',
            'name': 'test-v1',
            'system_prompt': 'You are a test assistant.',
            'temperature': 0.5,
            'is_active': True,
        }, headers=headers)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['data']['feature'] == 'copilot'
        assert data['data']['name'] == 'test-v1'
        assert data['data']['is_active'] is True

    def test_create_prompt_version_validation(self, app, client):
        """测试创建时参数校验"""
        headers = self._get_auth_header(app, client)

        # 缺少 feature
        resp = client.post('/api/v1/ai/prompt-versions', json={
            'name': 'test',
            'system_prompt': 'prompt',
        }, headers=headers)
        assert resp.status_code == 400

        # 缺少 system_prompt
        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'script_gen',
            'name': 'test',
        }, headers=headers)
        assert resp.status_code == 400

        # 缺少 name
        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'script_gen',
            'system_prompt': 'prompt',
        }, headers=headers)
        assert resp.status_code == 400

        # 无效 feature
        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'invalid_feature',
            'name': 'test',
            'system_prompt': 'prompt',
        }, headers=headers)
        assert resp.status_code == 400

    def test_get_prompt_version(self, app, client):
        """测试获取单个版本"""
        headers = self._get_auth_header(app, client)

        # 创建
        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'copilot', 'name': 'v1', 'system_prompt': 'p',
        }, headers=headers)
        version_id = resp.get_json()['data']['id']

        # 获取
        resp = client.get(f'/api/v1/ai/prompt-versions/{version_id}', headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['id'] == version_id

    def test_get_prompt_version_not_found(self, app, client):
        """测试获取不存在的版本"""
        headers = self._get_auth_header(app, client)
        resp = client.get('/api/v1/ai/prompt-versions/99999', headers=headers)
        assert resp.status_code == 404

    def test_update_prompt_version(self, app, client):
        """测试更新版本"""
        headers = self._get_auth_header(app, client)

        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'copilot', 'name': 'v1', 'system_prompt': 'old',
        }, headers=headers)
        version_id = resp.get_json()['data']['id']

        resp = client.put(f'/api/v1/ai/prompt-versions/{version_id}', json={
            'name': 'v1-updated',
            'system_prompt': 'new prompt',
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['name'] == 'v1-updated'

    def test_deactivate_prompt_version(self, app, client):
        """测试停用版本"""
        headers = self._get_auth_header(app, client)

        resp = client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'copilot', 'name': 'v1', 'system_prompt': 'p',
        }, headers=headers)
        version_id = resp.get_json()['data']['id']

        resp = client.delete(f'/api/v1/ai/prompt-versions/{version_id}', headers=headers)
        assert resp.status_code == 200

    def test_select_prompt_version(self, app, client):
        """测试 A/B 测试选择"""
        headers = self._get_auth_header(app, client)

        # 创建并激活
        client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'copilot', 'name': 'v1', 'system_prompt': 'p',
            'is_active': True,
        }, headers=headers)

        resp = client.post('/api/v1/ai/prompt-versions/select', json={
            'feature': 'copilot',
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['feature'] == 'copilot'

    def test_select_prompt_version_none_active(self, app, client):
        """测试没有激活版本时的选择"""
        import uuid
        headers = self._get_auth_header(app, client)
        unique_feature = f'no_active_{uuid.uuid4().hex[:8]}'
        resp = client.post('/api/v1/ai/prompt-versions/select', json={
            'feature': unique_feature,
        }, headers=headers)
        assert resp.status_code == 404

    def test_refresh_stats_endpoint(self, app, client):
        """测试统计刷新端点"""
        headers = self._get_auth_header(app, client)

        client.post('/api/v1/ai/prompt-versions', json={
            'feature': 'script_gen', 'name': 'v1', 'system_prompt': 'p',
        }, headers=headers)

        resp = client.post('/api/v1/ai/prompt-versions/refresh-stats', headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['refreshed_count'] >= 1
