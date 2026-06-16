"""
AI 测试数据工厂服务测试
"""

import pytest


class TestDataFactoryService:
    """DataFactoryService 测试"""

    def test_get_templates(self, app):
        """获取模板列表"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            templates = svc.get_templates()
            assert len(templates) >= 3
            names = [t["name"] for t in templates]
            assert "user" in names
            assert "order" in names
            assert "product" in names

    def test_generate_user(self, app):
        """生成用户数据"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            result = svc.generate("user", count=5, seed=42)
            assert result["count"] == 5
            assert len(result["data"]) == 5
            for user in result["data"]:
                assert "username" in user
                assert "email" in user
                assert "phone" in user
                assert "id" in user

    def test_generate_order(self, app):
        """生成订单数据"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            result = svc.generate("order", count=3, seed=42)
            assert result["count"] == 3
            for order in result["data"]:
                assert "order_no" in order
                assert "amount" in order
                assert 10.0 <= order["amount"] <= 10000.0

    def test_generate_with_custom_rules(self, app):
        """自定义规则生成"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            result = svc.generate("user", count=1, custom_rules={"age": {"min": 20, "max": 30}}, seed=42)
            user = result["data"][0]
            assert 20 <= user["age"] <= 30

    def test_generate_invalid_template(self, app):
        """无效模板应抛出异常"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            with pytest.raises(ValueError):
                svc.generate("nonexistent")

    def test_generate_invalid_count(self, app):
        """无效数量应抛出异常"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            with pytest.raises(ValueError):
                svc.generate("user", count=0)
            with pytest.raises(ValueError):
                svc.generate("user", count=20000)

    def test_cleanup(self, app):
        """清理数据"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            svc.generate("user", count=10, seed=42)
            result = svc.cleanup("user")
            assert result["cleaned"] == 10

    def test_cleanup_all(self, app):
        """清理所有数据"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc = DataFactoryService()
            svc.generate("user", count=5, seed=42)
            svc.generate("order", count=3, seed=42)
            result = svc.cleanup()
            assert result["cleaned"] == 8

    def test_seeded_reproducible(self, app):
        """相同种子应生成相同数据"""
        with app.app_context():
            from app.services.ai.data_factory_service import DataFactoryService
            svc1 = DataFactoryService()
            result1 = svc1.generate("user", count=3, seed=123)
            svc2 = DataFactoryService()
            result2 = svc2.generate("user", count=3, seed=123)
            assert result1["data"] == result2["data"]
