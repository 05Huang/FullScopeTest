"""
P19 生产运维服务测试（Feature Flag / Config 热更新）
"""

import pytest
import os


class TestFeatureFlagService:
    """Feature Flag 服务测试"""

    def test_register_flag(self, app):
        """注册功能开关"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            flag = svc.register_flag("dark_mode", enabled=True, description="暗色模式")
            assert flag.name == "dark_mode"
            assert flag.enabled is True

    def test_is_enabled_boolean(self, app):
        """布尔类型开关"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            svc.register_flag("feature_a", enabled=True)
            assert svc.is_enabled("feature_a") is True
            svc.register_flag("feature_b", enabled=False)
            assert svc.is_enabled("feature_b") is False

    def test_is_enabled_percentage(self, app):
        """百分比灰度开关"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            svc.register_flag("new_ui", enabled=True, flag_type="percentage", percentage=50)
            # 同一用户应始终得到相同结果
            result1 = svc.is_enabled("new_ui", user_id=123)
            result2 = svc.is_enabled("new_ui", user_id=123)
            assert result1 == result2

    def test_is_enabled_user_list(self, app):
        """用户白名单开关"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            svc.register_flag("beta", enabled=True, flag_type="user_list", user_list=[1, 2, 3])
            assert svc.is_enabled("beta", user_id=1) is True
            assert svc.is_enabled("beta", user_id=99) is False

    def test_default_behavior_disabled(self, app):
        """未注册的开关默认关闭"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            assert svc.is_enabled("nonexistent") is False

    def test_toggle_flag(self, app):
        """切换开关状态"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            svc.register_flag("test", enabled=False)
            assert svc.is_enabled("test") is False
            svc.toggle_flag("test", True)
            assert svc.is_enabled("test") is True

    def test_list_flags(self, app):
        """列出所有开关"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            svc.register_flag("a", enabled=True)
            svc.register_flag("b", enabled=False)
            flags = svc.list_flags()
            assert len(flags) == 2

    def test_env_override(self, app):
        """环境变量覆盖"""
        with app.app_context():
            from app.services.feature_flag_service import FeatureFlagService
            svc = FeatureFlagService()
            os.environ["FEATURE_NEW_API"] = "true"
            assert svc.is_enabled("new_api") is True
            del os.environ["FEATURE_NEW_API"]
            assert svc.is_enabled("new_api") is False


class TestConfigService:
    """配置热更新服务测试"""

    def test_get_default(self, app):
        """获取默认值"""
        with app.app_context():
            from app.services.config_service import ConfigService
            svc = ConfigService()
            assert svc.get("NONEXISTENT_KEY", "default") == "default"

    def test_set_reloadable(self, app):
        """设置可热更新配置"""
        with app.app_context():
            from app.services.config_service import ConfigService
            svc = ConfigService()
            result = svc.set("PARALLEL_WORKERS", "10")
            assert result["success"] is True
            assert svc.get("PARALLEL_WORKERS") == "10"

    def test_set_requires_restart(self, app):
        """设置需重启的配置应失败"""
        with app.app_context():
            from app.services.config_service import ConfigService
            svc = ConfigService()
            result = svc.set("DATABASE_URL", "sqlite:///new.db")
            assert result["success"] is False
            assert "重启" in result["message"]

    def test_rollback(self, app):
        """回滚配置"""
        with app.app_context():
            from app.services.config_service import ConfigService
            svc = ConfigService()
            svc.set("PARALLEL_WORKERS", "5")
            svc.set("PARALLEL_WORKERS", "10")
            assert svc.get("PARALLEL_WORKERS") == "10"
            svc.rollback("PARALLEL_WORKERS")
            assert svc.get("PARALLEL_WORKERS") == "5"

    def test_history(self, app):
        """变更历史应被记录"""
        with app.app_context():
            from app.services.config_service import ConfigService
            svc = ConfigService()
            svc.set("PARALLEL_WORKERS", "5")
            svc.set("PARALLEL_WORKERS", "10")
            history = svc.get_history()
            assert len(history) == 2

    def test_is_reloadable(self, app):
        """检查配置是否可热更新"""
        with app.app_context():
            from app.services.config_service import ConfigService
            svc = ConfigService()
            assert svc.is_reloadable("PARALLEL_WORKERS") is True
            assert svc.is_reloadable("DATABASE_URL") is False
