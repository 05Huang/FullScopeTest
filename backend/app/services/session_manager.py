"""
会话管理服务
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger
from ..utils.singleton import singleton_function

logger = get_logger(__name__)

SESSION_TIMEOUT = int(os.environ.get("SESSION_TIMEOUT", "7200"))
MAX_SESSIONS_PER_USER = int(os.environ.get("MAX_SESSIONS_PER_USER", "10"))


class UserSession:
    """用户会话记录"""

    def __init__(self, user_id, session_id=None, ip_address="", user_agent="", created_at=None, last_active=None, is_active=True):
        self.user_id = user_id
        self.session_id = session_id or secrets.token_hex(32)
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = created_at or datetime.utcnow()
        self.last_active = last_active or datetime.utcnow()
        self.is_active = is_active

    def is_expired(self):
        if not self.is_active: return True
        return datetime.utcnow() - self.last_active > timedelta(seconds=SESSION_TIMEOUT)

    def touch(self): self.last_active = datetime.utcnow()

    def to_dict(self):
        return {"session_id": self.session_id, "ip_address": self.ip_address, "user_agent": self.user_agent, "created_at": self.created_at.isoformat() if self.created_at else None, "last_active": self.last_active.isoformat() if self.last_active else None, "is_active": self.is_active, "is_expired": self.is_expired()}


class SessionManager:
    """会话管理器"""

    def __init__(self):
        self._sessions: Dict[str, UserSession] = {}
        self._user_sessions: Dict[int, List[str]] = {}

    def create_session(self, user_id, ip_address="", user_agent=""):
        self._cleanup_expired(user_id)
        user_sessions = self._user_sessions.get(user_id, [])
        if len(user_sessions) >= MAX_SESSIONS_PER_USER:
            oldest_id = user_sessions.pop(0)
            self._sessions.pop(oldest_id, None)
        session = UserSession(user_id=user_id, ip_address=ip_address, user_agent=user_agent)
        self._sessions[session.session_id] = session
        if user_id not in self._user_sessions: self._user_sessions[user_id] = []
        self._user_sessions[user_id].append(session.session_id)
        return session

    def get_session(self, session_id):
        session = self._sessions.get(session_id)
        if session and not session.is_expired(): session.touch(); return session
        return None

    def get_user_sessions(self, user_id):
        self._cleanup_expired(user_id)
        return [self._sessions[sid] for sid in self._user_sessions.get(user_id, []) if sid in self._sessions and self._sessions[sid].is_active]

    def invalidate_session(self, session_id):
        session = self._sessions.get(session_id)
        if session: session.is_active = False; return True
        return False

    def invalidate_user_sessions(self, user_id, exclude_session=None):
        count = 0
        for sid in self._user_sessions.get(user_id, []):
            if sid != exclude_session and sid in self._sessions and self._sessions[sid].is_active:
                self._sessions[sid].is_active = False
                count += 1
        return count

    def cleanup_all_expired(self):
        expired = [sid for sid, s in self._sessions.items() if s.is_expired()]
        for sid in expired:
            s = self._sessions.pop(sid, None)
            if s and sid in self._user_sessions.get(s.user_id, []):
                self._user_sessions[s.user_id].remove(sid)
        return len(expired)

    def _cleanup_expired(self, user_id):
        sids = self._user_sessions.get(user_id, [])
        expired = [sid for sid in sids if sid in self._sessions and self._sessions[sid].is_expired()]
        for sid in expired:
            self._sessions.pop(sid, None)
            sids.remove(sid)

    def get_session_count(self, user_id): return len(self.get_user_sessions(user_id))


@singleton_function
def get_session_manager():
    return SessionManager()
