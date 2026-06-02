"""
AI 配置 Service

处理 AI 助手配置的读取和保存
"""

import os
import re
from flask import current_app

from .base import BaseService
from ..core.logging import get_logger


logger = get_logger(__name__)


AI_CONFIG_ENV_MAP = {
    "base_url": "AI_ASSISTANT_BASE_URL",
    "model": "AI_ASSISTANT_MODEL",
    "api_key": "AI_ASSISTANT_API_KEY",
    "vision_base_url": "AI_VISION_BASE_URL",
    "vision_model": "AI_VISION_MODEL",
    "vision_api_key": "AI_VISION_API_KEY",
}


def _mask_secret(value: str) -> str:
    if not value:
        return value
    if len(value) > 8:
        return f"{value[:4]}...{value[-4:]}"
    return "***"


def _sanitize_env_value(value: str) -> str:
    return str(value or "").replace(chr(10), "").replace(chr(13), "").strip()


class AiConfigService(BaseService):

    def get_config(self):
        """获取当前 AI 配置"""
        config = {
            "base_url": current_app.config.get("AI_ASSISTANT_BASE_URL", ""),
            "model": current_app.config.get("AI_ASSISTANT_MODEL", ""),
            "api_key": current_app.config.get("AI_ASSISTANT_API_KEY", ""),
            "vision_base_url": current_app.config.get("AI_VISION_BASE_URL", ""),
            "vision_model": current_app.config.get("AI_VISION_MODEL", ""),
            "vision_api_key": current_app.config.get("AI_VISION_API_KEY", "")
        }
        config["api_key"] = _mask_secret(config["api_key"])
        config["vision_api_key"] = _mask_secret(config["vision_api_key"])
        return config

    def save_config(self, data: dict):
        """保存 AI 配置到 .env 文件"""
        payload = {}
        for field_name, env_key in AI_CONFIG_ENV_MAP.items():
            if field_name in data:
                payload[env_key] = _sanitize_env_value(data.get(field_name))

        required_fields = ["AI_ASSISTANT_BASE_URL", "AI_ASSISTANT_MODEL", "AI_ASSISTANT_API_KEY"]
        for required_field in required_fields:
            value = payload.get(required_field) or current_app.config.get(required_field, "")
            if not str(value).strip():
                return {"success": False, "error": f"{required_field} is required"}

        vision_defaults = {
            "AI_VISION_BASE_URL": payload.get("AI_ASSISTANT_BASE_URL") or current_app.config.get("AI_ASSISTANT_BASE_URL", ""),
            "AI_VISION_MODEL": payload.get("AI_ASSISTANT_MODEL") or current_app.config.get("AI_ASSISTANT_MODEL", ""),
            "AI_VISION_API_KEY": payload.get("AI_ASSISTANT_API_KEY") or current_app.config.get("AI_ASSISTANT_API_KEY", ""),
        }
        for key, default_value in vision_defaults.items():
            if key not in payload:
                payload[key] = _sanitize_env_value(default_value)

        env_path = os.path.join(os.path.dirname(current_app.root_path), ".env")
        try:
            self._upsert_env_file(env_path, payload)
            for key, value in payload.items():
                os.environ[key] = value
                current_app.config[key] = value
        except Exception as exc:
            logger.error("save ai config failed", error=str(exc), exc_info=True)
            return {"success": False, "error": f"保存 AI 配置失败: {str(exc)}"}

        return {
            "success": True,
            "data": {
                "base_url": current_app.config.get("AI_ASSISTANT_BASE_URL", ""),
                "model": current_app.config.get("AI_ASSISTANT_MODEL", ""),
                "api_key": _mask_secret(current_app.config.get("AI_ASSISTANT_API_KEY", "")),
                "vision_base_url": current_app.config.get("AI_VISION_BASE_URL", ""),
                "vision_model": current_app.config.get("AI_VISION_MODEL", ""),
                "vision_api_key": _mask_secret(current_app.config.get("AI_VISION_API_KEY", "")),
            }
        }


    def _upsert_env_file(self, file_path: str, mapping: dict):
        """更新或追加 .env 文件中的配置项"""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        else:
            lines = []

        for env_key, env_value in mapping.items():
            pattern = re.compile(rf"^\s*{re.escape(env_key)}\s*=")
            replaced = False
            for idx, line in enumerate(lines):
                if pattern.match(line):
                    lines[idx] = f"{env_key}={env_value}"
                    replaced = True
                    break
            if not replaced:
                lines.append(f"{env_key}={env_value}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chr(10).join(lines) + chr(10))
