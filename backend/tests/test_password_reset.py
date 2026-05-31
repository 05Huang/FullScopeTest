"""
密码重置功能集成测试

测试完整的密码重置流程：
1. 请求重置 → 获取 token
2. 使用 token 重置密码
3. 用旧密码登录失败
4. 用新密码登录成功
"""

import pytest


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def registered_user(client):
    """注册一个测试用户"""
    client.post('/api/v1/auth/register', json={
        'username': 'reset_test_user',
        'email': 'reset@test.com',
        'password': 'OldPass@123',
    })
    return {'username': 'reset_test_user', 'email': 'reset@test.com', 'password': 'OldPass@123'}


class TestPasswordReset:
    """密码重置测试"""

    def test_forgot_password_returns_token(self, client, registered_user):
        """忘记密码接口返回重置 token"""
        resp = client.post('/api/v1/auth/forgot-password', json={
            'email': registered_user['email'],
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'reset_token' in data['data']

    def test_forgot_password_nonexistent_email(self, client):
        """不存在的邮箱也返回成功（防止邮箱枚举）"""
        resp = client.post('/api/v1/auth/forgot-password', json={
            'email': 'nonexistent@test.com',
        })
        assert resp.status_code == 200

    def test_reset_password_success(self, client, registered_user):
        """使用有效 token 重置密码成功"""
        # 获取 token
        resp = client.post('/api/v1/auth/forgot-password', json={
            'email': registered_user['email'],
        })
        token = resp.get_json()['data']['reset_token']

        # 重置密码
        resp = client.post('/api/v1/auth/reset-password', json={
            'token': token,
            'new_password': 'NewPass@456',
        })
        assert resp.status_code == 200

        # 用旧密码登录失败
        resp = client.post('/api/v1/auth/login', json={
            'username': registered_user['username'],
            'password': registered_user['password'],
        })
        assert resp.status_code == 401

        # 用新密码登录成功
        resp = client.post('/api/v1/auth/login', json={
            'username': registered_user['username'],
            'password': 'NewPass@456',
        })
        assert resp.status_code == 200

    def test_reset_password_invalid_token(self, client):
        """使用无效 token 重置密码失败"""
        resp = client.post('/api/v1/auth/reset-password', json={
            'token': 'invalid_token_123',
            'new_password': 'NewPass@456',
        })
        assert resp.status_code == 400

    def test_reset_password_weak_password(self, client, registered_user):
        """使用弱密码重置失败"""
        resp = client.post('/api/v1/auth/forgot-password', json={
            'email': registered_user['email'],
        })
        token = resp.get_json()['data']['reset_token']

        resp = client.post('/api/v1/auth/reset-password', json={
            'token': token,
            'new_password': 'weak',
        })
        assert resp.status_code == 400

    def test_token_single_use(self, client, registered_user):
        """重置 token 只能使用一次"""
        resp = client.post('/api/v1/auth/forgot-password', json={
            'email': registered_user['email'],
        })
        token = resp.get_json()['data']['reset_token']

        # 第一次使用成功
        resp = client.post('/api/v1/auth/reset-password', json={
            'token': token,
            'new_password': 'NewPass@456',
        })
        assert resp.status_code == 200

        # 第二次使用失败
        resp = client.post('/api/v1/auth/reset-password', json={
            'token': token,
            'new_password': 'AnotherPass@789',
        })
        assert resp.status_code == 400
