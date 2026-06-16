"""
敏感数据脱敏服务

自动检测并脱敏日志和报告中的敏感数据。
"""

import os
import re
from typing import Any, Dict
from ..core.logging import get_logger

logger = get_logger(__name__)

MASKING_ENABLED = os.environ.get("DATA_MASKING_ENABLED", "true").lower() == "true"

# 敏感字段名模式
SENSITIVE_FIELDS = {
    "password", "token", "secret", "authorization", "api_key",
    "access_token", "refresh_token", "private_key", "credit_card",
}

# 邮箱正则
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")
# 手机号正则（中国大陆）
PHONE_PATTERN = re.compile(r"1[3-9]\d{9}")
# 身份证正则
ID_CARD_PATTERN = re.compile(r"\d{17}[\dXx]")


class DataMaskingService:
    """敏感数据脱敏服务"""

    def mask_string(self, text: str) -> str:
        """对字符串进行脱敏处理"""
        if not text or not isinstance(text, str):
            return text
        if not MASKING_ENABLED:
            return text

        # 邮箱脱敏
        text = EMAIL_PATTERN.sub(lambda m: m.group(0)[:3] + "***@" + m.group(1), text)
        # 手机号脱敏
        text = PHONE_PATTERN.sub(lambda m: m.group(0)[:3] + "****" + m.group(0)[-4:], text)
        # 身份证脱敏
        text = ID_CARD_PATTERN.sub(lambda m: m.group(0)[:6] + "********" + m.group(0)[-4:], text)
        return text

    def mask_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """递归脱敏字典中的敏感字段"""
        if not data or not isinstance(data, dict):
            return data
        if not MASKING_ENABLED:
            return data

        result = {}
        for key, value in data.items():
            key_lower = key.lower()
            is_sensitive = any(sf in key_lower for sf in SENSITIVE_FIELDS)

            if is_sensitive and isinstance(value, str) and len(value) > 0:
                result[key] = "***"
            elif isinstance(value, dict):
                result[key] = self.mask_dict(value)
            elif isinstance(value, str):
                result[key] = self.mask_string(value)
            else:
                result[key] = value
        return result

    def mask_log_data(self, data: Any) -> Any:
        """对日志数据进行脱敏"""
        if isinstance(data, dict):
            return self.mask_dict(data)
        elif isinstance(data, str):
            return self.mask_string(data)
        return data


_instance = None


def get_data_masking_service():
    global _instance
    if _instance is None: _instance = DataMaskingService()
    return _instance
