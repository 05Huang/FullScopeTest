"""
响应压缩中间件

功能：
- Gzip 压缩（阈值 1KB 以上才压缩）
- 通过环境变量 COMPRESSION_ENABLED（默认 true）控制开关

注：Flask 内置支持较小，此中间件提供基础 Gzip 压缩。
生产环境建议在 Nginx/反向代理层处理压缩。
"""

import gzip
import os
from io import BytesIO
from flask import request, after_this_request
from ..core.logging import get_logger

logger = get_logger(__name__)

# 最小压缩阈值（字节）
MIN_COMPRESS_SIZE = 1024  # 1KB

# 不压缩的内容类型
_NO_COMPRESS_TYPES = {
    'image/png', 'image/jpeg', 'image/gif', 'image/webp',
    'application/zip', 'application/gzip', 'application/pdf',
    'video/', 'audio/',
}


def compression_middleware(app):
    """
    注册响应压缩中间件

    仅压缩 text/html、application/json、text/css、application/javascript
    等文本类型响应，且响应体大于 1KB。
    """
    enabled = os.environ.get('COMPRESSION_ENABLED', 'true').lower() == 'true'
    if not enabled:
        logger.info("响应压缩已禁用（COMPRESSION_ENABLED=false）")
        return

    @app.after_request
    def _compress_response(response):
        # 检查客户端是否支持 gzip
        accept_encoding = request.headers.get('Accept-Encoding', '')
        if 'gzip' not in accept_encoding:
            return response

        # 检查内容类型
        content_type = response.content_type or ''
        should_compress = False
        for ct in ('text/html', 'application/json', 'text/css', 'application/javascript', 'text/plain', 'text/xml', 'application/xml'):
            if ct in content_type:
                should_compress = True
                break
        for ct in _NO_COMPRESS_TYPES:
            if ct in content_type:
                should_compress = False
                break

        if not should_compress:
            return response

        # 检查响应体大小
        response_data = response.get_data()
        if len(response_data) < MIN_COMPRESS_SIZE:
            return response

        # 压缩
        try:
            compressed = gzip.compress(response_data)
            # 仅在压缩后更小时使用
            if len(compressed) < len(response_data):
                response.set_data(compressed)
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Content-Length'] = len(compressed)
                response.headers['Vary'] = 'Accept-Encoding'
        except Exception:
            pass  # 压缩失败不影响原始响应

        return response

    logger.info("响应压缩中间件已初始化（Gzip，阈值 1KB）")
