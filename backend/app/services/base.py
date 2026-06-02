"""
Service 基类

提供统一的事务管理、日志记录，所有 Service 应继承此类
"""

from contextlib import contextmanager
from ..extensions import db
from ..core.logging import get_logger


class BaseService:
    """Service 基类，提供统一的事务管理"""

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    @contextmanager
    def transaction(self):
        """
        统一事务上下文管理器

        用法:
            with self.transaction():
                db.session.add(entity)
                # 无需手动 commit，退出时自动提交
            # 如果抛异常，自动 rollback
        """
        try:
            yield
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def add(self, *entities):
        """添加实体到 session"""
        for entity in entities:
            db.session.add(entity)

    def delete(self, *entities):
        """从 session 删除实体"""
        for entity in entities:
            db.session.delete(entity)

    def flush(self):
        """刷新 session（获取自增 ID 等，但不提交）"""
        db.session.flush()

    def rollback(self):
        """手动回滚"""
        db.session.rollback()
