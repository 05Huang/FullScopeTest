"""
插件模块

提供插件基类、注册表和事件系统。
"""

from .base import PluginBase
from .registry import PluginRegistry, plugin_registry

__all__ = ['PluginBase', 'PluginRegistry', 'plugin_registry']