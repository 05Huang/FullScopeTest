"""
Redis 滑动窗口限流中间件

集成到 Flask 请求处理流程中，支持：
- 基于用户身份的限流
- 基于组织的限流
- 429 响应 + Retry-After header
- Prometheus 指标记录
"""

from functools import wraps
from flask import request, g, jsonify
from ..services.rate_limit_service import (
    sliding_window_rate_limit,
    get_rate_limit_headers,
    get_user_rate_limit,
    get_org_rate_limit,
)
from ..core.logging import get_logger

logger = get_logger(__name__)


def rate_limit_middleware(app):
    """初始化限流中间件"""

    @app.before_request
    def check_rate_limit():
        """检查请求是否超过限流"""
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

            # 跳过健康检查和静态资源
            if request.endpoint in ('health.health', 'health.health_check', 'static'):
                return None

            # 获取用户身份
            user_id = None
            is_api_token = False
            try:
                verify_jwt_in_request(optional=True)
                user_id = get_jwt_identity()
                is_api_token = 'Authorization' not in request.headers
            except Exception:
                pass

            # 构建限流键
            if user_id:
                rate_key = f'rate_limit:user:{user_id}'
                limit = get_user_rate_limit(user_id, is_api_token)
            else:
                # 未认证用户使用 IP 限流
                ip = request.remote_addr or '127.0.0.1'
                rate_key = f'rate_limit:ip:{ip}'
                limit = 50  # 未认证用户更严格

            # 检查是否超过限流
            if not sliding_window_rate_limit(rate_key, limit):
                headers = get_rate_limit_headers(rate_key, limit)
                logger.warning(
                    'Rate limit exceeded',
                    user_id=user_id,
                    rate_key=rate_key,
                    limit=limit,
                )
                # 记录 Prometheus 指标
                try:
                    from ..core.metrics import rate_limit_counter
                    rate_limit_counter.labels(
                        user_type='api_token' if is_api_token else 'user',
                        endpoint=request.endpoint or 'unknown',
                    ).inc()
                except Exception:
                    pass

                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'请求频率超过限制 ({limit} req/min)',
                    'retry_after': int(headers.get('Retry-After', 60)),
                }), 429, headers

        except Exception as exc:
            # 限流中间件不应影响正常请求
            logger.error('Rate limit check failed', error=str(exc))

    logger.info('Rate limit middleware initialized')
