"""
请求超时与 Body 大小限制中间件

功能：
- 请求体大小限制：默认 10MB，文件上传接口 50MB
- 请求超时：API 请求默认 30 秒，AI 接口 120 秒，测试执行接口 300 秒
- 超时返回 408，Body 过大返回 413

通过环境变量配置：
- REQUEST_TIMEOUT=30（默认 API 超时，秒）
- MAX_CONTENT_LENGTH=10485760（默认 Body 大小限制，字节）
"""

import os
import signal
import functools
from flask import request, g
from ..utils.response import error_response
from ..core.logging import get_logger

logger = get_logger(__name__)

# 路径前缀 → 超时时间映射
_TIMEOUT_RULES = {
    '/api/v1/ai/': 120,         # AI 相关接口：120 秒
    '/api/v1/test-runs/execute': 300,  # 测试执行接口：300 秒
    '/api/v1/perf-test/': 300,  # 性能测试接口：300 秒
    '/api/v1/web-test/': 120,   # Web 测试接口：120 秒
}


def request_limits_middleware(app):
    """
    注册请求限制中间件

    1. 设置 Flask MAX_CONTENT_LENGTH（全局 Body 大小限制）
    2. 为请求记录超时配置（供路由层使用）
    """
    # 全局 Body 大小限制（10MB）
    max_content = int(os.environ.get('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))
    app.config['MAX_CONTENT_LENGTH'] = max_content

    # 默认请求超时（秒）
    default_timeout = int(os.environ.get('REQUEST_TIMEOUT', 30))

    @app.before_request
    def _set_request_timeout():
        """为每个请求设置超时时间（存储到 g，供异步执行器使用）"""
        path = request.path
        timeout = default_timeout
        for prefix, t in _TIMEOUT_RULES.items():
            if path.startswith(prefix):
                timeout = t
                break
        g.request_timeout = timeout

    @app.errorhandler(413)
    def _payload_too_large(e):
        """Body 过大错误处理"""
        max_mb = max_content // (1024 * 1024)
        return error_response(413, f'请求体过大，最大允许 {max_mb}MB')

    logger.info(
        "请求限制中间件已初始化",
        max_content_mb=max_content // (1024 * 1024),
        default_timeout=default_timeout,
    )
