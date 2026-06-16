"""
双因素认证（2FA/TOTP）服务

支持 TOTP（Time-based One-Time Password）双因素认证。
兼容 Google Authenticator、Microsoft Authenticator。
"""

import os
import hmac
import hashlib
import struct
import time
import base64
import secrets
from typing import Dict, Any, List, Optional, Tuple
from ..core.logging import get_logger

logger = get_logger(__name__)

# TOTP 配置
TOTP_PERIOD = 30  # 时间步长（秒）
TOTP_DIGITS = 6   # 验证码位数
TOTP_ALGORITHM = "sha1"
RECOVERY_CODE_COUNT = 8


class TwoFactorService:
    """双因素认证服务"""

    def generate_secret(self) -> str:
        """生成 TOTP 密钥（Base32 编码）"""
        return base64.b32encode(os.urandom(20)).decode("utf-8")

    def generate_totp(self, secret: str, timestamp: int = None) -> str:
        """
        生成 TOTP 验证码

        Args:
            secret: Base32 编码的密钥
            timestamp: 时间戳（默认当前时间）

        Returns:
            str: 6 位验证码
        """
        if timestamp is None:
            timestamp = int(time.time())

        # 计算时间步长
        counter = timestamp // TOTP_PERIOD

        # 将步长转为 8 字节大端序
        counter_bytes = struct.pack(">Q", counter)

        # 解码密钥
        key = base64.b32decode(secret)

        # HMAC-SHA1
        hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

        # 动态截断
        offset = hmac_hash[-1] & 0x0F
        code = struct.unpack(">I", hmac_hash[offset:offset + 4])[0]
        code = code & 0x7FFFFFFF

        # 取模得到指定位数
        code = code % (10 ** TOTP_DIGITS)

        return str(code).zfill(TOTP_DIGITS)

    def verify_totp(self, secret: str, code: str, timestamp: int = None,
                    window: int = 1) -> bool:
        """
        验证 TOTP 验证码

        Args:
            secret: Base32 编码的密钥
            code: 用户输入的验证码
            timestamp: 当前时间戳
            window: 允许的时间窗口（前后各 N 个步长）

        Returns:
            bool: 验证是否通过
        """
        if timestamp is None:
            timestamp = int(time.time())

        for offset in range(-window, window + 1):
            expected = self.generate_totp(secret, timestamp + offset * TOTP_PERIOD)
            if hmac.compare_digest(expected, code):
                return True
        return False

    def generate_recovery_codes(self) -> List[str]:
        """
        生成一次性恢复码

        Returns:
            List[str]: 8 个恢复码（格式：XXXX-XXXX）
        """
        codes = []
        for _ in range(RECOVERY_CODE_COUNT):
            code = secrets.token_hex(4).upper()
            formatted = f"{code[:4]}-{code[4:]}"
            codes.append(formatted)
        return codes

    def generate_provisioning_uri(self, secret: str, email: str,
                                  issuer: str = "FullScopeTest") -> str:
        """
        生成 TOTP 配置 URI（用于生成 QR Code）

        Args:
            secret: Base32 编码的密钥
            email: 用户邮箱
            issuer: 应用名称

        Returns:
            str: otpauth:// URI
        """
        return f"otpauth://totp/{issuer}:{email}?secret={secret}&issuer={issuer}&digits={TOTP_DIGITS}&period={TOTP_PERIOD}"

    def setup_2fa(self, email: str) -> Dict[str, Any]:
        """
        设置 2FA（生成密钥和恢复码）

        Args:
            email: 用户邮箱

        Returns:
            Dict: {secret, provisioning_uri, recovery_codes}
        """
        secret = self.generate_secret()
        recovery_codes = self.generate_recovery_codes()
        uri = self.generate_provisioning_uri(secret, email)

        return {
            "secret": secret,
            "provisioning_uri": uri,
            "recovery_codes": recovery_codes,
        }

    def verify_and_activate(self, secret: str, code: str) -> bool:
        """
        验证并激活 2FA（设置时确认验证码）

        Args:
            secret: 密钥
            code: 用户输入的验证码

        Returns:
            bool: 验证通过返回 True
        """
        return self.verify_totp(secret, code)


_instance = None


def get_two_factor_service() -> TwoFactorService:
    global _instance
    if _instance is None:
        _instance = TwoFactorService()
    return _instance