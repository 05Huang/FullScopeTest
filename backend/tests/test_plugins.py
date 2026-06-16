"""
插件系统测试

覆盖：插件基类、注册表、事件分发、自动发现、启用/禁用、
     生命周期、示例插件
"""
import os
import tempfile
from unittest.mock import MagicMock, patch

from app.plugins.base import PluginBase
from app.plugins.registry import PluginRegistry


# ══════════════════════════════════════════════════════════════════════════════
# 一、插件基类测试
# ══════════════════════════════════════════════════════════════════════════════

class ConcretePlugin(PluginBase):
    """用于测试的具体插件实现"""
    name = 'test_plugin'
    version = '1.0.0'
    description = 'Test plugin'

    def __init__(self):
        self.events = []

    def on_event(self, event_name: str, data: dict):
        self.events.append((event_name, data))


class TestPluginBase:
    """PluginBase 测试"""

    def test_plugin_attributes(self):
        plugin = ConcretePlugin()
        assert plugin.name == 'test_plugin'
        assert plugin.version == '1.0.0'
        assert plugin.enabled is True

    def test_plugin_on_event(self):
        plugin = ConcretePlugin()
        plugin.on_event('test_completed', {'run_id': 1})
        assert len(plugin.events) == 1
        assert plugin.events[0] == ('test_completed', {'run_id': 1})

    def test_plugin_get_routes_returns_none(self):
        plugin = ConcretePlugin()
        assert plugin.get_routes() is None

    def test_plugin_on_init_no_error(self):
        plugin = ConcretePlugin()
        plugin.on_init(None)  # 不应抛异常

    def test_plugin_on_destroy_no_error(self):
        plugin = ConcretePlugin()
        plugin.on_destroy()  # 不应抛异常

    def test_plugin_repr(self):
        plugin = ConcretePlugin()
        assert 'test_plugin' in repr(plugin)
        assert '1.0.0' in repr(plugin)

    def test_plugin_log(self):
        plugin = ConcretePlugin()
        plugin.log('info', 'Test message')  # 不应抛异常

    def test_cannot_instantiate_abstract(self):
        import pytest
        with pytest.raises(TypeError):
            PluginBase()  # 抽象类不能直接实例化


# ══════════════════════════════════════════════════════════════════════════════
# 二、插件注册表测试
# ══════════════════════════════════════════════════════════════════════════════

class TestPluginRegistry:
    """PluginRegistry 测试"""

    def test_register_plugin(self):
        registry = PluginRegistry()
        plugin = ConcretePlugin()
        registry.register(plugin)
        assert registry.get('test_plugin') is plugin

    def test_register_non_plugin_raises(self):
        registry = PluginRegistry()
        import pytest
        with pytest.raises(TypeError):
            registry.register("not a plugin")

    def test_register_no_name_raises(self):
        registry = PluginRegistry()
        import pytest

        class NoNamePlugin(PluginBase):
            name = ''
            def on_event(self, event_name, data): pass

        with pytest.raises(ValueError, match="name"):
            registry.register(NoNamePlugin())

    def test_unregister_plugin(self):
        registry = PluginRegistry()
        plugin = ConcretePlugin()
        registry.register(plugin)
        registry.unregister('test_plugin')
        assert registry.get('test_plugin') is None

    def test_get_nonexistent_returns_none(self):
        registry = PluginRegistry()
        assert registry.get('nonexistent') is None

    def test_get_all(self):
        registry = PluginRegistry()
        p1 = ConcretePlugin()

        class Plugin2(PluginBase):
            name = 'plugin2'
            def on_event(self, event_name, data): pass

        registry.register(p1)
        registry.register(Plugin2())
        assert len(registry.get_all()) == 2

    def test_get_enabled(self):
        registry = PluginRegistry()
        p1 = ConcretePlugin()

        class DisabledPlugin(PluginBase):
            name = 'disabled'
            enabled = False
            def on_event(self, event_name, data): pass

        registry.register(p1)
        registry.register(DisabledPlugin())
        assert len(registry.get_enabled()) == 1

    def test_emit_calls_enabled_plugins(self):
        registry = PluginRegistry()
        p1 = ConcretePlugin()
        registry.register(p1)

        registry.emit('test_completed', {'run_id': 1})
        assert len(p1.events) == 1
        assert p1.events[0][0] == 'test_completed'

    def test_emit_skips_disabled_plugins(self):
        registry = PluginRegistry()

        class DisabledPlugin(PluginBase):
            name = 'disabled'
            enabled = False
            def on_event(self, event_name, data):
                raise AssertionError("Should not be called")

        registry.register(DisabledPlugin())
        registry.emit('test_completed', {})  # 不应抛异常

    def test_emit_handles_plugin_error(self):
        registry = PluginRegistry()

        class ErrorPlugin(PluginBase):
            name = 'error_plugin'
            def on_event(self, event_name, data):
                raise RuntimeError("Plugin error")

        p1 = ConcretePlugin()
        registry.register(ErrorPlugin())
        registry.register(p1)

        # 即使 error_plugin 抛异常，p1 仍应收到事件
        registry.emit('test_completed', {})
        assert len(p1.events) == 1

    def test_init_all_calls_on_init(self):
        registry = PluginRegistry()
        p1 = ConcretePlugin()
        p1.on_init = MagicMock()
        registry.register(p1)

        registry.init_all(None)
        p1.on_init.assert_called_once_with(None)

    def test_disabled_plugin_via_env(self):
        with patch.dict(os.environ, {'DISABLED_PLUGINS': 'env_disabled'}):
            # 重新加载 DISABLED_PLUGINS
            from app.plugins.registry import DISABLED_PLUGINS
            DISABLED_PLUGINS.add('env_disabled')

            registry = PluginRegistry()

            class EnvDisabledPlugin(PluginBase):
                name = 'env_disabled'
                def on_event(self, event_name, data): pass

            registry.register(EnvDisabledPlugin())
            assert registry.get('env_disabled').enabled is False


# ══════════════════════════════════════════════════════════════════════════════
# 三、自动发现测试
# ══════════════════════════════════════════════════════════════════════════════

class TestAutoDiscover:
    """自动发现测试"""

    def test_auto_discover_nonexistent_dir(self):
        registry = PluginRegistry()
        registry.auto_discover('/nonexistent/path')  # 不应抛异常
        assert len(registry.get_all()) == 0

    def test_auto_discover_with_plugin_file(self):
        registry = PluginRegistry()

        # 创建临时插件文件
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_code = '''
from app.plugins.base import PluginBase

class TempPlugin(PluginBase):
    name = 'temp_plugin'
    version = '0.1.0'
    def on_event(self, event_name, data):
        pass
'''
            with open(os.path.join(tmpdir, 'temp_plugin.py'), 'w') as f:
                f.write(plugin_code)

            registry.auto_discover(tmpdir)
            assert registry.get('temp_plugin') is not None

    def test_auto_discover_ignores_init_file(self):
        registry = PluginRegistry()

        with tempfile.TemporaryDirectory() as tmpdir:
            # __init__.py 应被忽略
            with open(os.path.join(tmpdir, '__init__.py'), 'w') as f:
                f.write('# init')

            registry.auto_discover(tmpdir)
            assert len(registry.get_all()) == 0


# ══════════════════════════════════════════════════════════════════════════════
# 四、Slack 示例插件测试
# ══════════════════════════════════════════════════════════════════════════════

class TestSlackPlugin:
    """Slack 通知插件测试"""

    def test_plugin_attributes(self):
        from app.plugins.custom.slack_notify import SlackNotifyPlugin
        plugin = SlackNotifyPlugin()
        assert plugin.name == 'slack_notify'
        assert plugin.version == '1.0.0'

    def test_plugin_on_init_no_webhook(self):
        from app.plugins.custom.slack_notify import SlackNotifyPlugin
        plugin = SlackNotifyPlugin()
        plugin.on_init(None)  # 不应抛异常

    @patch.dict(os.environ, {'SLACK_WEBHOOK_URL': 'https://hooks.slack.com/test'})
    @patch('requests.post')
    def test_plugin_sends_notification(self, mock_post):
        from app.plugins.custom.slack_notify import SlackNotifyPlugin
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        plugin = SlackNotifyPlugin()
        plugin.on_event('test_completed', {'run_id': 1, 'test_name': 'Login Test'})
        mock_post.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_plugin_no_webhook_skips(self):
        from app.plugins.custom.slack_notify import SlackNotifyPlugin
        os.environ.pop('SLACK_WEBHOOK_URL', None)
        plugin = SlackNotifyPlugin()
        plugin.on_event('test_completed', {'run_id': 1})  # 不应抛异常


# ══════════════════════════════════════════════════════════════════════════════
# 五、全局注册表测试
# ══════════════════════════════════════════════════════════════════════════════

class TestGlobalRegistry:
    """全局插件注册表测试"""

    def test_global_registry_exists(self):
        from app.plugins.registry import plugin_registry
        assert plugin_registry is not None
        assert isinstance(plugin_registry, PluginRegistry)