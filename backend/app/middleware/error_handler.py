"""
统一错误处理中间件

功能：
- 生产环境：500 错误不暴露堆栈，仅返回 {"code": 500, "message": "服务器内部错误", "request_id": "req_xxx"}
- 开发环境：500 错误包含完整堆栈（便于调试）
- 所有异常自动记录 structlog 日志（含 request_id、异常详情）
"""

import os
import traceback
from flask import jsonify, g
from ..utils.exceptions import AppError
from ..core.logging import get_logger

logger = get_logger(__name__)


def error_handler_middleware(app):
    """
    注册全局错误处理器

    覆盖 Flask 默认的错误处理，提供统一的 JSON 错误响应格式。
    """
    is_production = os.environ.get('FLASK_ENV') == 'production'

    @app.errorhandler(AppError)
    def handle_app_error(e):
        """统一处理自定义异常"""
        request_id = getattr(g, 'request_id', '')
        logger.warning(
            "应用异常",
            error_type=type(e).__name__,
            message=e.message,
            code=e.code,
            request_id=request_id,
        )
        response = {
            'code': e.code,
            'message': e.message,
            'errors': e.errors,
            'request_id': request_id,
        }
        return jsonify(response), e.code

    @app.errorhandler(400)
    def bad_request(e):
        request_id = getattr(g, 'request_id', '')
        return jsonify({
            'code': 400,
            'message': '请求参数错误',
            'request_id': request_id,
        }), 400

    @app.errorhandler(401)
    def unauthorized(e):
        request_id = getattr(g, 'request_id', '')
        return jsonify({
            'code': 401,
            'message': '未授权访问',
            'request_id': request_id,
        }), 401

    @app.errorhandler(403)
    def forbidden(e):
        request_id = getattr(g, 'request_id', '')
        return jsonify({
            'code': 403,
            'message': '禁止访问',
            'request_id': request_id,
        }), 403

    @app.errorhandler(404)
    def not_found(e):
        request_id = getattr(g, 'request_id', '')
        return jsonify({
            'code': 404,
            'message': '资源不存在',
            'request_id': request_id,
        }), 404

    @app.errorhandler(408)
    def request_timeout(e):
        request_id = getattr(g, 'request_id', '')
        return jsonify({
            'code': 408,
            'message': '请求超时',
            'request_id': request_id,
        }), 408

    @app.errorhandler(500)
    def internal_error(e):
        request_id = getattr(g, 'request_id', '')

        # 记录完整堆栈到日志（始终记录，生产环境也需要排查问题）
        logger.error(
            "服务器内部错误",
            request_id=request_id,
            error=str(e),
            traceback=traceback.format_exc(),
        )

        response = {
            'code': 500,
            'message': '服务器内部错误',
            'request_id': request_id,
        }

        # 开发环境返回堆栈信息（便于调试）
        if not is_production:
            response['debug'] = {
                'error': str(e),
                'traceback': traceback.format_exc(),
            }

        return jsonify(response), 500

    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        """捕获所有未处理的异常（兜底）"""
        request_id = getattr(g, 'request_id', '')

        logger.error(
            "未处理的异常",
            request_id=request_id,
            error_type=type(e).__name__,
            error=str(e),
        )

        response = {
            'code': 500,
            'message': '服务器内部错误',
            'request_id': request_id,
        }

        if not is_production:
            response['debug'] = {
                'error': str(e),
                'type': type(e).__name__,
                'traceback': traceback.format_exc(),
            }

        return jsonify(response), 500

    logger.info("全局错误处理器已初始化", production=is_production)
