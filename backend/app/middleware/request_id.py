"""
请求链路追踪中间件

为每个请求生成唯一 Request ID，贯穿前后端全链路。
支持从外部网关传入 X-Request-ID（透传模式）。

功能：
- 生成格式：req_xxxx-xxxx-xxxx（UUID 段）
- Request ID 注入 structlog 上下文（自动附加到每条日志）
- 响应头返回 X-Request-ID（方便前端定位问题）
- 支持从请求头透传外部网关生成的 Request ID
"""

import uuid
from flask import request, g

from ..core.logging import get_logger, set_trace_id, clear_trace_id

logger = get_logger(__name__)


def _generate_request_id() -> str:
    """
    生成请求 ID

    格式：req_xxxx-xxxx-xxxx
    使用 UUID4 前 12 位（48 bit），碰撞概率极低
    """
    uuid_hex = uuid.uuid4().hex[:12]
    return f"req_{uuid_hex[:4]}-{uuid_hex[4:8]}-{uuid_hex[8:12]}"


def request_id_middleware(app):
    """
    注册请求 ID 中间件到 Flask app

    每个请求：
    1. 读取 X-Request-ID 请求头（如果有）
    2. 否则生成新的 Request ID
    3. 存储到 g.request_id
    4. 注入 structlog 上下文
    5. 响应头返回 X-Request-ID
    """
    @app.before_request
    def _inject_request_id():
        # 优先使用外部网关传入的 X-Request-ID
        request_id = request.headers.get('X-Request-ID', '').strip()

        # 如果外部未传入，自动生成
        if not request_id:
            request_id = _generate_request_id()

        # 存储到 Flask g 对象
        g.request_id = request_id

        # 同步更新 structlog trace_id（保持兼容）
        set_trace_id(request_id)

    @app.after_request
    def _add_request_id_to_response(response):
        """在响应头中返回 X-Request-ID"""
        request_id = getattr(g, 'request_id', '')
        if request_id:
            response.headers['X-Request-ID'] = request_id
        return response

    @app.teardown_appcontext
    def _clear_request_id(exc=None):
        """请求结束时清理上下文"""
        clear_trace_id()

    logger.info("请求链路追踪中间件已初始化")
