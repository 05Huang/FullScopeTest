"""
安全响应头中间件

为所有 HTTP 响应注入标准安全头：
- X-Content-Type-Options: 防止 MIME 嗅探
- X-Frame-Options: 防止 Clickjacking
- X-XSS-Protection: 现代浏览器靠 CSP，旧浏览器保留最低防护
- Strict-Transport-Security: 强制 HTTPS（仅生产环境）
- Content-Security-Policy: 防止 XSS / 数据注入
- Referrer-Policy: 控制 Referer 泄露
- Permissions-Policy: 禁用敏感浏览器特性

通过环境变量 SECURITY_HEADERS_ENABLED（默认 true）控制开关。
开发环境自动放宽 CSP 以支持 Vite HMR。
"""

import os

from ..core.logging import get_logger

logger = get_logger(__name__)


def security_headers_middleware(app):
    """
    注册安全响应头 after_request 钩子

    在 app/__init__.py 的 init_extensions 阶段调用。
    """

    # 是否启用（可通过环境变量关闭，便于调试）
    enabled = os.environ.get('SECURITY_HEADERS_ENABLED', 'true').strip().lower() == 'true'
    if not enabled:
        logger.info('Security headers middleware disabled by env')
        return

    is_production = not app.debug

    @app.after_request
    def _set_security_headers(response):
        # 基础安全头（所有响应）
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '0'  # 现代浏览器靠 CSP
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'

        # HSTS：仅生产环境启用，避免开发环境 HTTPS 要求
        if is_production:
            response.headers['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains'
            )

        # CSP 策略
        if is_production:
            # 生产环境严格 CSP
            csp = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' https://fonts.gstatic.com; "
                "connect-src 'self'; "
                "frame-ancestors 'none'"
            )
        else:
            # 开发环境：放宽 CSP 以支持 Vite HMR（eval + ws）
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-eval' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https: blob:; "
                "font-src 'self' https://fonts.gstatic.com data:; "
                "connect-src 'self' ws: wss: http: https:; "
                "frame-ancestors 'none'"
            )

        response.headers['Content-Security-Policy'] = csp

        return response

    logger.info(
        'Security headers middleware initialized',
        mode='production' if is_production else 'development',
    )
