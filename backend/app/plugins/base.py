"""
插件基类

所有插件必须继承 PluginBase 并实现必要的接口方法。
插件可以通过 get_routes() 注册自定义 API 路由。

用法：
    class MyPlugin(PluginBase):
        name = 'my_plugin'
        version = '1.0.0'
        description = 'My custom plugin'

        def on_event(self, event_name, data):
            if event_name == 'test_completed':
                # 处理测试完成事件
                pass

        def get_routes(self):
            return []  # 返回 Flask Blueprint 或路由列表
"""
from abc import ABC, abstractmethod
from ..core.logging import get_logger

logger = get_logger(__name__)


class PluginBase(ABC):
    """
    插件基类

    所有插件必须继承此类并实现以下属性和方法：

    必需属性：
        name (str): 插件唯一标识
        version (str): 插件版本号

    可选属性：
        description (str): 插件描述
        enabled (bool): 是否启用（默认 True）

    必需方法：
        on_event(event_name, data): 事件处理

    可选方法：
        get_routes(): 返回 Flask Blueprint
        on_init(app): 应用初始化时调用
        on_destroy(): 应用关闭时调用
    """

    # ── 必需属性 ──────────────────────────────────────────────────────────────

    name: str = ''
    version: str = '0.0.1'

    # ── 可选属性 ──────────────────────────────────────────────────────────────

    description: str = ''
    enabled: bool = True

    # ── 生命周期方法 ──────────────────────────────────────────────────────────

    def on_init(self, app):
        """
        应用初始化时调用

        Args:
            app: Flask 应用实例
        """
        pass

    def on_destroy(self):
        """应用关闭时调用，用于清理资源"""
        pass

    # ── 事件处理 ──────────────────────────────────────────────────────────────

    @abstractmethod
    def on_event(self, event_name: str, data: dict):
        """
        处理事件

        支持的事件：
            - test_completed: 测试执行完成
            - test_failed: 测试执行失败
            - user_created: 用户创建
            - project_created: 项目创建
            - comment_created: 评论创建

        Args:
            event_name: 事件名称
            data: 事件数据
        """
        pass

    # ── 路由注册 ──────────────────────────────────────────────────────────────

    def get_routes(self):
        """
        返回插件自定义路由

        Returns:
            Flask Blueprint 或 None
        """
        return None

    # ── 工具方法 ──────────────────────────────────────────────────────────────

    def log(self, level: str, message: str, **kwargs):
        """插件日志"""
        plugin_logger = get_logger(f'plugin.{self.name}')
        log_func = getattr(plugin_logger, level, plugin_logger.info)
        log_func(message, plugin_version=self.version, **kwargs)

    def __repr__(self):
        return f'<Plugin {self.name} v{self.version} enabled={self.enabled}>'