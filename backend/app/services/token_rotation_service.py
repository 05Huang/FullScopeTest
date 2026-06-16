"""
API 密钥轮换服务

提供 Token 过期、自动轮换和使用审计能力。
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from ..core.logging import get_logger

logger = get_logger(__name__)

# Token 过期时间选项（天）
EXPIRY_OPTIONS = {"30d": 30, "90d": 90, "365d": 365, "never": None}
ROTATION_WARNING_DAYS = 7  # 到期前 7 天提醒


class TokenRotationService:
    """Token 轮换服务"""

    def generate_token(self) -> str:
        """生成新的 API Token"""
        return f"fst_{secrets.token_hex(32)}"

    def hash_token(self, token: str) -> str:
        """计算 Token 哈希（存储时使用）"""
        return hashlib.sha256(token.encode()).hexdigest()

    def calculate_expiry(self, period: str = "365d") -> Optional[datetime]:
        """计算过期时间"""
        days = EXPIRY_OPTIONS.get(period)
        if days is None:
            return None
        return datetime.utcnow() + timedelta(days=days)

    def is_expiring_soon(self, expires_at: Optional[datetime]) -> bool:
        """检查是否即将过期"""
        if expires_at is None:
            return False
        return (expires_at - datetime.utcnow()).days <= ROTATION_WARNING_DAYS

    def is_expired(self, expires_at: Optional[datetime]) -> bool:
        """检查是否已过期"""
        if expires_at is None:
            return False
        return datetime.utcnow() > expires_at

    def rotate_token(self, old_token_hash: str = None) -> Dict[str, Any]:
        """
        轮换 Token

        Returns:
            Dict: {token, token_hash, expires_at}
        """
        new_token = self.generate_token()
        new_hash = self.hash_token(new_token)
        expires_at = self.calculate_expiry("365d")

        logger.info("Token 轮换完成", old_hash_prefix=old_token_hash[:8] if old_token_hash else None)
        return {
            "token": new_token,
            "token_hash": new_hash,
            "expires_at": expires_at.isoformat() if expires_at else None,
        }


_instance = None


def get_token_rotation_service():
    global _instance
    if _instance is None: _instance = TokenRotationService()
    return _instance
