"""
Prompt 模板市场服务测试
"""

import pytest


class TestPromptMarketplace:
    """PromptMarketplace 测试"""

    def test_get_builtin_templates(self, app):
        """应返回内置模板列表"""
        with app.app_context():
            from app.services.ai.prompt_marketplace import PromptMarketplace
            svc = PromptMarketplace()
            templates = svc.get_builtin_templates()
            assert len(templates) >= 5
            assert all("feature" in t for t in templates)

    def test_list_templates(self, app):
        """列出模板应包含内置模板"""
        with app.app_context():
            from app.services.ai.prompt_marketplace import PromptMarketplace
            svc = PromptMarketplace()
            templates = svc.list_templates()
            builtin = [t for t in templates if t.get("source") == "builtin"]
            assert len(builtin) >= 5

    def test_list_templates_by_feature(self, app):
        """按功能过滤应返回正确结果"""
        with app.app_context():
            from app.services.ai.prompt_marketplace import PromptMarketplace
            svc = PromptMarketplace()
            templates = svc.list_templates(feature="api_test_gen")
            assert all(t["feature"] == "api_test_gen" for t in templates)

    def test_create_template(self, app, client):
        """创建模板应成功"""
        with app.app_context():
            from app.services.ai.prompt_marketplace import PromptMarketplace
            svc = PromptMarketplace()
            result = svc.create_template(
                feature="test_feature",
                name="测试模板",
                system_prompt="你是测试专家",
                user_prompt_template="测试 {{url}}",
                user_id=1,
            )
            assert result["feature"] == "test_feature"
            assert result["version"] >= 1

    def test_render_template(self, app, client):
        """渲染模板应替换变量"""
        with app.app_context():
            from app.services.ai.prompt_marketplace import PromptMarketplace
            svc = PromptMarketplace()
            # 先创建模板
            created = svc.create_template(
                feature="render_test",
                name="渲染测试",
                system_prompt="系统提示",
                user_prompt_template="请求 {{url}} 的 {{method}} 方法",
                user_id=1,
            )
            # 渲染
            result = svc.render_template(created["id"], {"url": "/api/test", "method": "GET"})
            assert "/api/test" in result["user_prompt"]
            assert "GET" in result["user_prompt"]

    def test_extract_variables(self, app):
        """应正确提取变量"""
        with app.app_context():
            from app.services.ai.prompt_marketplace import PromptMarketplace
            svc = PromptMarketplace()
            variables = svc._extract_variables("{{name}} 和 {{url}} 的测试")
            assert "name" in variables
            assert "url" in variables
