"""
单例模式工具

提供统一的单例装饰器，避免各服务手动实现不一致。
"""

from functools import wraps
from typing import TypeVar, Type

T = TypeVar('T')


def singleton(cls: Type[T]) -> Type[T]:
    """
    单例类装饰器

    用法：
        @singleton
        class MyService:
            pass

        instance = MyService()  # 始终返回同一个实例
    """
    _instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs) -> T:
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return get_instance


def singleton_function(func):
    """
    单例函数装饰器（用于 get_xxx_service 模式）

    用法：
        _instance = None

        @singleton_function
        def get_my_service():
            return MyService()
    """
    _instance = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal _instance
        if _instance is None:
            _instance = func(*args, **kwargs)
        return _instance

    return wrapper
