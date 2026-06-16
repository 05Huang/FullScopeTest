"""
会话管理服务测试
"""

import pytest


class TestSessionManager:
    """SessionManager 测试"""

    def test_create_session(self, app):
        """创建会话应返回有效会话"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            session = mgr.create_session(user_id=1, ip_address="127.0.0.1")
            assert session.user_id == 1
            assert session.is_active is True
            assert len(session.session_id) == 64

    def test_get_session(self, app):
        """获取会话应返回正确会话"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            session = mgr.create_session(user_id=1)
            retrieved = mgr.get_session(session.session_id)
            assert retrieved is not None
            assert retrieved.user_id == 1

    def test_get_expired_session(self, app):
        """过期会话应返回 None"""
        with app.app_context():
            from app.services.session_manager import SessionManager, UserSession
            mgr = SessionManager()
            session = mgr.create_session(user_id=1)
            session.is_active = False
            assert mgr.get_session(session.session_id) is None

    def test_get_user_sessions(self, app):
        """获取用户所有活跃会话"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            mgr.create_session(user_id=1)
            mgr.create_session(user_id=1)
            sessions = mgr.get_user_sessions(user_id=1)
            assert len(sessions) == 2

    def test_invalidate_session(self, app):
        """注销会话应成功"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            session = mgr.create_session(user_id=1)
            assert mgr.invalidate_session(session.session_id) is True
            assert mgr.get_session(session.session_id) is None

    def test_invalidate_user_sessions(self, app):
        """批量注销用户会话"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            mgr.create_session(user_id=1)
            mgr.create_session(user_id=1)
            current = mgr.create_session(user_id=1)
            count = mgr.invalidate_user_sessions(user_id=1, exclude_session=current.session_id)
            assert count == 2
            assert mgr.get_session(current.session_id) is not None

    def test_max_sessions_limit(self, app):
        """会话数应受限制"""
        with app.app_context():
            from app.services.session_manager import SessionManager, MAX_SESSIONS_PER_USER
            mgr = SessionManager()
            for _ in range(MAX_SESSIONS_PER_USER + 2):
                mgr.create_session(user_id=1)
            sessions = mgr.get_user_sessions(user_id=1)
            assert len(sessions) <= MAX_SESSIONS_PER_USER

    def test_session_count(self, app):
        """会话计数应正确"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            mgr.create_session(user_id=1)
            mgr.create_session(user_id=1)
            assert mgr.get_session_count(user_id=1) == 2

    def test_to_dict(self, app):
        """会话序列化应包含所有字段"""
        with app.app_context():
            from app.services.session_manager import SessionManager
            mgr = SessionManager()
            session = mgr.create_session(user_id=1, ip_address="10.0.0.1")
            d = session.to_dict()
            assert "session_id" in d
            assert "ip_address" in d
            assert d["ip_address"] == "10.0.0.1"
