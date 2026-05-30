"""
AI 服务模块

提供统一的 LLM 调用接口，自动记录调用日志，支持重试和降级。
"""

from .base import AIServiceBase

__all__ = ['AIServiceBase']
