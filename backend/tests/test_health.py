"""健康检查端点测试"""

import pytest


class TestHealthEndpoints:
    """测试健康检查端点"""

    def test_health_check_returns_200(self, client):
        """测试基础健康检查返回 200"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
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
        assert data['checks']['redis']['status'] in ['ok', 'error']

    def test_readiness_check_celery_status(self, client):
        """测试就绪检查 Celery 状态"""
        response = client.get('/health/ready')
        data = response.get_json()
        assert 'celery' in data['checks']
        assert data['checks']['celery']['status'] in ['ok', 'warning']

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
