"""
健康检查增强测试

覆盖：存活探针、就绪探针、综合健康检查、组件检查函数、
     Kubernetes 兼容格式、错误降级
"""
from unittest.mock import patch, MagicMock


class TestHealthEndpoints:
    """基础健康检查端点测试（兼容旧测试）"""

    def test_health_check_returns_200(self, client):
        """测试基础健康检查返回 200"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'fullscopetest'
        assert 'version' in data

    def test_readiness_check_database_ok(self, client):
        """测试就绪检查数据库连通性"""
        response = client.get('/health/ready')
        data = response.get_json()
        assert 'checks' in data
        assert 'database' in data['checks']
        assert data['checks']['database']['status'] == 'ok'

    def test_readiness_check_redis_ok(self, client):
        """测试就绪检查 Redis 连通性"""
        response = client.get('/health/ready')
        data = response.get_json()
        assert 'redis' in data['checks']
        # Redis 可能未运行，但结构应该正确
        assert data['checks']['redis']['status'] in ['ok', 'warning', 'error']

    def test_readiness_check_celery_status(self, client):
        """测试就绪检查 Celery 状态"""
        response = client.get('/health/ready')
        data = response.get_json()
        assert 'celery' in data['checks']
        assert data['checks']['celery']['status'] in ['ok', 'warning', 'disabled']

    def test_readiness_check_returns_valid_structure(self, client):
        """测试就绪检查返回结构完整"""
        response = client.get('/health/ready')
        data = response.get_json()
        assert 'status' in data
        assert 'checks' in data
        assert data['status'] in ['ok', 'degraded']

    def test_health_check_no_auth_required(self, client):
        """测试健康检查端点无需认证"""
        # 不带 Authorization header 也应该能访问
        response = client.get('/health')
        assert response.status_code == 200

    def test_readiness_check_no_auth_required(self, client):
        """测试就绪检查端点无需认证"""
        # 不带 Authorization header 也应该能访问
        response = client.get('/health/ready')
        assert response.status_code in [200, 503]


class TestLivenessProbe:
    """存活探针测试"""

    def test_liveness_returns_200(self, client):
        resp = client.get('/health/live')
        assert resp.status_code == 200

    def test_liveness_response_structure(self, client):
        resp = client.get('/health/live')
        data = resp.get_json()
        assert data['status'] == 'ok'
        assert data['service'] == 'fullscopetest'
        assert 'version' in data
        assert 'timestamp' in data

    def test_liveness_always_ok(self, client):
        """存活探针应始终返回 200（不检查依赖）"""
        resp = client.get('/health/live')
        assert resp.status_code == 200
        assert resp.get_json()['status'] == 'ok'


class TestReadinessProbe:
    """就绪探针测试"""

    def test_readiness_has_timestamp(self, client):
        resp = client.get('/health/ready')
        data = resp.get_json()
        assert 'timestamp' in data

    def test_readiness_with_db_error_returns_503(self, client):
        """数据库故障时返回 503"""
        with patch('app.core.health._check_database', return_value={'status': 'error', 'message': 'Connection refused'}):
            resp = client.get('/health/ready')
            assert resp.status_code == 503
            data = resp.get_json()
            assert data['status'] == 'error'

    def test_readiness_with_redis_warning_still_200(self, client):
        """Redis 故障时状态为 degraded 但仍返回 200"""
        with patch('app.core.health._check_redis', return_value={'status': 'warning', 'message': 'Connection refused'}):
            resp = client.get('/health/ready')
            assert resp.status_code == 200
            data = resp.get_json()
            assert data['status'] == 'degraded'

    def test_readiness_all_ok(self, client):
        """所有组件正常时返回 ok"""
        with patch('app.core.health._check_database', return_value={'status': 'ok'}):
            with patch('app.core.health._check_redis', return_value={'status': 'ok'}):
                with patch('app.core.health._check_celery', return_value={'status': 'ok'}):
                    resp = client.get('/health/ready')
                    assert resp.status_code == 200
                    data = resp.get_json()
                    assert data['status'] == 'ok'


class TestComponentChecks:
    """组件检查函数测试"""

    def test_check_database_ok(self, app):
        from app.core.health import _check_database
        with app.app_context():
            result = _check_database()
            assert result['status'] == 'ok'

    def test_check_database_error(self, app):
        from app.core.health import _check_database
        with app.app_context():
            with patch('app.core.health.db') as mock_db:
                mock_db.session.execute.side_effect = Exception("Connection failed")
                result = _check_database()
                assert result['status'] == 'error'
                assert 'Connection failed' in result['message']

    def test_check_redis_returns_result(self):
        from app.core.health import _check_redis
        result = _check_redis()
        assert result['status'] in ('ok', 'warning')

    def test_check_celery_disabled(self):
        from app.core.health import _check_celery
        import os
        with patch.dict(os.environ, {'CELERY_ENABLE': 'false'}):
            result = _check_celery()
            assert result['status'] == 'disabled'

    def test_check_celery_no_workers(self):
        from app.core.health import _check_celery
        import os
        with patch.dict(os.environ, {'CELERY_ENABLE': 'true'}):
            with patch('app.core.health.celery') as mock_celery:
                mock_inspect = MagicMock()
                mock_inspect.active.return_value = {}
                mock_celery.control.inspect.return_value = mock_inspect
                result = _check_celery()
                assert result['status'] == 'warning'

    def test_check_celery_with_workers(self):
        from app.core.health import _check_celery
        import os
        with patch.dict(os.environ, {'CELERY_ENABLE': 'true'}):
            with patch('app.core.health.celery') as mock_celery:
                mock_inspect = MagicMock()
                mock_inspect.active.return_value = {'worker1': []}
                mock_celery.control.inspect.return_value = mock_inspect
                result = _check_celery()
                assert result['status'] == 'ok'
                assert 'worker1' in result['workers']

    def test_check_celery_error(self):
        from app.core.health import _check_celery
        import os
        with patch.dict(os.environ, {'CELERY_ENABLE': 'true'}):
            with patch('app.core.health.celery') as mock_celery:
                mock_celery.control.inspect.side_effect = Exception("Timeout")
                result = _check_celery()
                assert result['status'] == 'warning'


class TestKubernetesCompatibility:
    """Kubernetes 探针格式测试"""

    def test_liveness_is_k8s_compatible(self, client):
        resp = client.get('/health/live')
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'

    def test_readiness_is_k8s_compatible(self, client):
        resp = client.get('/health/ready')
        assert resp.status_code in (200, 503)
        assert resp.content_type == 'application/json'

    def test_response_has_required_fields(self, client):
        resp = client.get('/health/ready')
        data = resp.get_json()
        assert 'status' in data
        assert 'checks' in data
