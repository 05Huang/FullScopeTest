"""
结构化日志配置模块

使用 structlog 提供 JSON 格式的结构化日志，每条日志包含：
- timestamp: ISO 8601 时间戳
- level: 日志级别
- module: 模块名
- trace_id: 请求追踪 ID（Flask request context 中生成）

使用方式：
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.info("操作完成", user_id=123, action="create")
"""

import uuid
import logging
from typing import Optional

import structlog


def get_trace_id() -> str:
    """获取当前请求的 trace_id"""
    try:
        ctx = structlog.contextvars.get_merged_contextvars()
        return ctx.get("trace_id", "")
    except Exception:
        return ""


def set_trace_id(trace_id: Optional[str] = None) -> str:
    """
    设置当前请求的 trace_id

    Args:
        trace_id: 可选的 trace_id，如果为 None 则自动生成

    Returns:
        str: 实际使用的 trace_id
    """
    if trace_id is None:
        trace_id = uuid.uuid4().hex[:16]
    structlog.contextvars.bind_contextvars(trace_id=trace_id)
    return trace_id


def clear_trace_id():
    """清除当前 trace_id"""
    try:
        structlog.contextvars.unbind_contextvars("trace_id")
    except KeyError:
        pass


def _add_trace_id(logger, method_name, event_dict):
    """structlog processor: 自动为每条日志添加 trace_id"""
    event_dict["trace_id"] = get_trace_id()
    return event_dict


def _mask_sensitive_data(logger, method_name, event_dict):
    """structlog processor: 脱敏处理敏感字段"""
    sensitive_keys = {"api_key", "secret", "password", "token", "authorization"}
    for key in list(event_dict.keys()):
        if key.lower() in sensitive_keys:
            val = str(event_dict[key])
            if len(val) > 8:
                event_dict[key] = val[:4] + "***" + val[-4:]
            else:
                event_dict[key] = "***"
    return event_dict


def configure_structlog(
    log_level: str = "INFO",
    json_format: bool = True,
):
    """
    配置 structlog

    Args:
        log_level: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        json_format: 是否使用 JSON 格式（生产环境建议 True）
    """
    # 配置标准库 logging handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 共享处理器链：所有日志都经过这些步骤
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        _add_trace_id,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        _mask_sensitive_data,
        structlog.processors.StackInfoRenderer(),
    ]

    # 结构化 JSON 渲染器（生产）
    if json_format:
        renderer = structlog.processors.JSONRenderer(ensure_ascii=False)
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 将 ProcessorFormatter 作为标准库 handler 的 formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[*shared_processors, renderer],
    )
    handler.setFormatter(formatter)


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    获取一个绑定到指定模块的 structlog logger

    Args:
        name: 模块名，通常传入 __name__

    Returns:
        structlog.stdlib.BoundLogger 实例
    """
    return structlog.get_logger(name)
