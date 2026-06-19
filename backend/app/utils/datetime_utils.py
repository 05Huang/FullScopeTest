"""
日期时间工具

提供兼容 Python 3.12+ 的 UTC 时间获取方法。
"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    获取当前 UTC 时间（替代已废弃的 datetime.utcnow()）

    Returns:
        datetime: 当前 UTC 时间（naive，兼容 SQLAlchemy）
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
