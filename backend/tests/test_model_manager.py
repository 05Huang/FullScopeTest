"""
AI 模型管理服务测试
"""

import pytest


class TestModelManager:
    """ModelManager 测试"""

    def test_get_model_for_feature(self, app):
        """应返回功能对应的模型"""
        with app.app_context():
            from app.services.ai.model_manager import ModelManager
            mgr = ModelManager()
            model = mgr.get_model_for_feature("copilot")
            assert isinstance(model, str)
            assert len(model) > 0

    def test_get_model_unknown_feature(self, app):
        """未知功能应返回默认模型"""
        with app.app_context():
            from app.services.ai.model_manager import ModelManager
            mgr = ModelManager()
            model = mgr.get_model_for_feature("unknown_feature")
            assert model == "gpt-4o-mini"

    def test_check_budget(self, app):
        """预算检查应返回正确结构"""
        with app.app_context():
            from app.services.ai.model_manager import ModelManager
            mgr = ModelManager()
            result = mgr.check_budget()
            assert "used" in result
            assert "budget" in result
            assert "remaining" in result
            assert "percentage" in result
            assert "exceeded" in result

    def test_usage_stats_structure(self, app):
        """用量统计应返回正确结构"""
        with app.app_context():
            from app.services.ai.model_manager import ModelManager
            mgr = ModelManager()
            result = mgr.get_usage_stats(days=7)
            assert "total_calls" in result
            assert "total_tokens" in result
            assert "total_cost" in result
            assert "by_feature" in result
            assert "by_day" in result

    def test_model_status(self, app):
        """模型状态应返回列表"""
        with app.app_context():
            from app.services.ai.model_manager import ModelManager
            mgr = ModelManager()
            result = mgr.get_model_status()
            assert isinstance(result, list)
            assert len(result) > 0
            assert "name" in result[0]
            assert "pricing" in result[0]

    def test_budget_not_exceeded(self, app):
        """新环境预算不应超支"""
        with app.app_context():
            from app.services.ai.model_manager import ModelManager
            mgr = ModelManager()
            result = mgr.check_budget()
            assert result["exceeded"] is False
