"""
插件注册表

管理插件的注册、加载、事件分发和生命周期。
支持自动扫描 plugins/ 目录下的插件。

用法：
    from app.plugins import plugin_registry

    # 注册插件
    plugin_registry.register(MyPlugin())

    # 触发事件
    plugin_registry.emit('test_completed', {'run_id': 1, 'status': 'success'})

    # 在应用初始化时加载所有插件
    plugin_registry.init_all(app)
"""
import os
import importlib
import inspect
from typing import List, Optional
from .base import PluginBase
from ..core.logging import get_logger

logger = get_logger(__name__)

# 通过环境变量控制禁用的插件列表（逗号分隔）
DISABLED_PLUGINS = set(
    p.strip() for p in os.environ.get('DISABLED_PLUGINS', '').split(',') if p.strip()
)


class PluginRegistry:
    """插件注册表"""

    def __init__(self):
        self._plugins: dict[str, PluginBase] = {}
        self._initialized = False

    def register(self, plugin: PluginBase):
        """
        注册插件

        Args:
            plugin: PluginBase 实例
        """
        if not isinstance(plugin, PluginBase):
            raise TypeError(f"插件必须继承 PluginBase: {type(plugin)}")

        if not plugin.name:
            raise ValueError("插件必须定义 name 属性")

        if plugin.name in DISABLED_PLUGINS:
            logger.info("插件已禁用（环境变量）", plugin_name=plugin.name)
            plugin.enabled = False

        self._plugins[plugin.name] = plugin
        logger.info("插件已注册", plugin_name=plugin.name,
                     plugin_version=plugin.version, enabled=plugin.enabled)

    def unregister(self, name: str):
        """注销插件"""
        if name in self._plugins:
            plugin = self._plugins.pop(name)
            plugin.on_destroy()
            logger.info("插件已注销", plugin_name=name)

    def get(self, name: str) -> Optional[PluginBase]:
        """获取插件实例"""
        return self._plugins.get(name)

    def get_all(self) -> List[PluginBase]:
        """获取所有已注册的插件"""
        return list(self._plugins.values())

    def get_enabled(self) -> List[PluginBase]:
        """获取所有已启用的插件"""
        return [p for p in self._plugins.values() if p.enabled]

    def init_all(self, app):
        """
        初始化所有已注册的插件

        Args:
            app: Flask 应用实例
        """
        for plugin in self.get_enabled():
            try:
                plugin.on_init(app)
                logger.info("插件已初始化", plugin_name=plugin.name)
            except Exception as exc:
                logger.error("插件初始化失败",
                             plugin_name=plugin.name, error=str(exc))

        # 注册插件路由
        for plugin in self.get_enabled():
            routes = plugin.get_routes()
            if routes:
                try:
                    app.register_blueprint(routes)
                    logger.info("插件路由已注册", plugin_name=plugin.name)
                except Exception as exc:
                    logger.error("插件路由注册失败",
                                 plugin_name=plugin.name, error=str(exc))

        self._initialized = True
        logger.info("所有插件已初始化", count=len(self.get_enabled()))

    def emit(self, event_name: str, data: dict = None):
        """
        触发事件，通知所有已启用的插件

        Args:
            event_name: 事件名称
            data: 事件数据
        """
        data = data or {}
        for plugin in self.get_enabled():
            try:
                plugin.on_event(event_name, data)
            except Exception as exc:
                logger.error("插件事件处理失败",
                             plugin_name=plugin.name,
                             event_name=event_name,
                             error=str(exc))

    def auto_discover(self, plugins_dir: str = None):
        """
        自动扫描并加载插件目录下的插件模块

        扫描 plugins_dir 下的所有 Python 模块，查找继承 PluginBase 的类并实例化注册。

        Args:
            plugins_dir: 插件目录路径（默认为当前包目录下的 custom/ 子目录）
        """
        if plugins_dir is None:
            plugins_dir = os.path.join(os.path.dirname(__file__), 'custom')

        if not os.path.isdir(plugins_dir):
            return

        for filename in os.listdir(plugins_dir):
            if filename.startswith('_') or not filename.endswith('.py'):
                continue

            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(
                    f'app.plugins.custom.{module_name}',
                    os.path.join(plugins_dir, filename),
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # 查找继承 PluginBase 的类
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, PluginBase) and obj is not PluginBase):
                            instance = obj()
                            self.register(instance)
            except Exception as exc:
                logger.error("插件加载失败",
                             module=module_name, error=str(exc))

    @property
    def initialized(self) -> bool:
        return self._initialized

    def __repr__(self):
        return f'<PluginRegistry plugins={len(self._plugins)}>'


# 全局插件注册表实例
plugin_registry = PluginRegistry()