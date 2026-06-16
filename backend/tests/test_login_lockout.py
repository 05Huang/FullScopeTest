"""
登录失败锁定与密码策略测试

覆盖：失败计数、账户锁定、锁定解除、密码策略校验
"""
import uuid
import time


def _register_user(client, username=None, password="Passw0rd!"):
    """注册测试用户"""
    uid = uuid.uuid4().hex[:8]
    username = username or f"lock_{uid}"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={
        "username": username, "email": email, "password": password,
    })
    return username, password


# ══════════════════════════════════════════════════════════════════════════════
# 一、密码策略测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPasswordPolicy:
    """密码复杂度校验测试"""

    def test_password_too_short(self):
        from app.utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength("Ab1!")
        assert is_valid is False
        assert "8 位" in msg

    def test_password_no_uppercase(self):
        from app.utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength("abcdefg1!")
        assert is_valid is False
        assert "大写" in msg

    def test_password_no_lowercase(self):
        from app.utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength("ABCDEFG1!")
        assert is_valid is False
        assert "小写" in msg

    def test_password_no_digit(self):
        from app.utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength("Abcdefgh!")
        assert is_valid is False
        assert "数字" in msg

    def test_password_no_special_char(self):
        from app.utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength("Abcdefg1")
        assert is_valid is False
        assert "特殊字符" in msg

    def test_password_valid(self):
        from app.utils.validators import validate_password_strength
        is_valid, msg = validate_password_strength("Passw0rd!")
        assert is_valid is True
        assert msg is None


# ══════════════════════════════════════════════════════════════════════════════
# 二、登录失败计数与锁定测试
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginFailureTracking:
    """登录失败计数测试"""

    def test_record_failure_increments_count(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.password_policy import record_login_failure, get_login_failures, reset_login_failures
        with app.app_context():
            user = User(username=f"lf_{uuid.uuid4().hex[:6]}", email="lf@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            reset_login_failures(user.id)
            assert get_login_failures(user.id) == 0

            record_login_failure(user.id, ip_address="127.0.0.1")
            assert get_login_failures(user.id) == 1

            record_login_failure(user.id)
            assert get_login_failures(user.id) == 2

            reset_login_failures(user.id)
            db.session.rollback()

    def test_reset_failures_clears_count(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.password_policy import record_login_failure, get_login_failures, reset_login_failures
        with app.app_context():
            user = User(username=f"lf_{uuid.uuid4().hex[:6]}", email="lf2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            reset_login_failures(user.id)
            for _ in range(3):
                record_login_failure(user.id)
            assert get_login_failures(user.id) == 3

            reset_login_failures(user.id)
            assert get_login_failures(user.id) == 0
            db.session.rollback()


class TestAccountLockout:
    """账户锁定测试"""

    def test_account_locked_after_max_failures(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.password_policy import (
            record_login_failure, is_account_locked, reset_login_failures,
            MAX_LOGIN_FAILURES,
        )
        with app.app_context():
            user = User(username=f"lf_{uuid.uuid4().hex[:6]}", email="lf3@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            reset_login_failures(user.id)
            for _ in range(MAX_LOGIN_FAILURES):
                record_login_failure(user.id)

            locked, remaining = is_account_locked(user.id)
            assert locked is True
            assert remaining > 0

            reset_login_failures(user.id)
            db.session.rollback()

    def test_account_not_locked_below_threshold(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.password_policy import (
            record_login_failure, is_account_locked, reset_login_failures,
            MAX_LOGIN_FAILURES,
        )
        with app.app_context():
            user = User(username=f"lf_{uuid.uuid4().hex[:6]}", email="lf4@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            reset_login_failures(user.id)
            for _ in range(MAX_LOGIN_FAILURES - 1):
                record_login_failure(user.id)

            locked, _ = is_account_locked(user.id)
            assert locked is False

            reset_login_failures(user.id)
            db.session.rollback()

    def test_lockout_resets_on_successful_login(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.password_policy import (
            record_login_failure, is_account_locked, reset_login_failures, get_login_failures,
            MAX_LOGIN_FAILURES,
        )
        with app.app_context():
            user = User(username=f"lf_{uuid.uuid4().hex[:6]}", email="lf5@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            reset_login_failures(user.id)
            for _ in range(MAX_LOGIN_FAILURES):
                record_login_failure(user.id)

            # 模拟成功登录
            reset_login_failures(user.id)
            locked, _ = is_account_locked(user.id)
            assert locked is False
            assert get_login_failures(user.id) == 0

            db.session.rollback()


# ══════════════════════════════════════════════════════════════════════════════
# 三、登录 API 锁定集成测试
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginLockoutAPI:
    """登录 API 锁定机制集成测试"""

    def test_login_success_resets_failures(self, client, no_rate_limit):
        """成功登录后重置失败计数"""
        username, password = _register_user(client)

        # 先失败 2 次
        for _ in range(2):
            client.post("/api/v1/auth/login", json={
                "username": username, "password": "wrong_password",
            })

        # 正确登录
        resp = client.post("/api/v1/auth/login", json={
            "username": username, "password": password,
        })
        assert resp.status_code == 200
        assert resp.get_json()["data"]["access_token"] is not None

    def test_login_returns_failure_count(self, client, no_rate_limit):
        """登录失败时返回失败次数"""
        username, _ = _register_user(client)

        resp = client.post("/api/v1/auth/login", json={
            "username": username, "password": "wrong_password",
        })
        assert resp.status_code == 401
        data = resp.get_json()
        assert data["errors"]["failures"] >= 1

    def test_login_locked_returns_423(self, client, no_rate_limit):
        """连续 5 次失败后返回 423"""
        username, _ = _register_user(client)

        # 连续失败 5 次
        for _ in range(5):
            client.post("/api/v1/auth/login", json={
                "username": username, "password": "wrong_password",
            })

        # 第 6 次应返回 423
        resp = client.post("/api/v1/auth/login", json={
            "username": username, "password": "wrong_password",
        })
        assert resp.status_code == 423
        data = resp.get_json()
        assert data["errors"]["locked"] is True
        assert data["errors"]["remaining_seconds"] > 0

    def test_login_locked_with_correct_password_returns_423(self, client, no_rate_limit):
        """锁定后即使密码正确也返回 423"""
        username, password = _register_user(client)

        # 连续失败 5 次
        for _ in range(5):
            client.post("/api/v1/auth/login", json={
                "username": username, "password": "wrong_password",
            })

        # 正确密码也被锁定
        resp = client.post("/api/v1/auth/login", json={
            "username": username, "password": password,
        })
        assert resp.status_code == 423

    def test_login_nonexistent_user_returns_401(self, client, no_rate_limit):
        """不存在的用户返回 401（不泄露用户是否存在）"""
        resp = client.post("/api/v1/auth/login", json={
            "username": "nonexistent_user_xyz", "password": "any_password",
        })
        assert resp.status_code == 401


# ══════════════════════════════════════════════════════════════════════════════
# 四、密码修改时间追踪测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPasswordChangedAt:
    """密码修改时间字段测试"""

    def test_user_model_has_password_changed_at(self, app):
        from app.extensions import db
        from app.models.user import User
        with app.app_context():
            user = User(username=f"pc_{uuid.uuid4().hex[:6]}", email="pc@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            assert hasattr(user, 'password_changed_at')
            # 新用户默认为 None
            assert user.password_changed_at is None
            db.session.rollback()

    def test_password_changed_at_can_be_set(self, app):
        from app.extensions import db
        from app.models.user import User
        from datetime import datetime
        with app.app_context():
            user = User(username=f"pc_{uuid.uuid4().hex[:6]}", email="pc2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            now = datetime.utcnow()
            user.password_changed_at = now
            assert user.password_changed_at == now
            db.session.rollback()