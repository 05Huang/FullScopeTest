"""
Prompt 模板市场服务

提供 Prompt 模板的管理和复用能力。
"""

import re
from typing import Dict, Any, List, Optional
from ...extensions import db
from ...models.prompt_version import PromptVersion
from ...core.logging import get_logger

logger = get_logger(__name__)

BUILTIN_TEMPLATES = [
    {
        "feature": "api_test_gen",
        "name": "API 测试用例生成 (REST)",
        "system_prompt": "你是 API 测试用例生成专家。根据接口定义生成完整的测试用例。",
        "user_prompt_template": "为以下 API 生成测试用例：\\nURL: {{api_url}}\\n方法: {{method}}",
        "variables": ["api_url", "method"],
    },
    {
        "feature": "perf_script_gen",
        "name": "性能测试脚本生成 (Locust)",
        "system_prompt": "你是 Locust 性能测试脚本专家。根据需求生成 Python Locust 脚本。",
        "user_prompt_template": "为以下场景生成 Locust 脚本：\\n目标 URL: {{target_url}}\\n并发用户: {{users}}",
        "variables": ["target_url", "users"],
    },
    {
        "feature": "playwright_gen",
        "name": "Playwright Web 自动化脚本生成",
        "system_prompt": "你是 Playwright 自动化测试专家。根据页面描述生成测试脚本。",
        "user_prompt_template": "为以下页面生成 Playwright 测试：\\nURL: {{page_url}}\\n场景: {{scenario}}",
        "variables": ["page_url", "scenario"],
    },
    {
        "feature": "test_data_gen",
        "name": "测试数据生成",
        "system_prompt": "你是测试数据生成专家。根据数据模型生成符合约束的测试数据。",
        "user_prompt_template": "为以下模型生成 {{count}} 条数据：\\n{{model}}",
        "variables": ["count", "model"],
    },
    {
        "feature": "failure_analysis",
        "name": "失败分析与根因归类",
        "system_prompt": "你是测试失败分析专家。分析失败用例，归类原因并给出修复建议。",
        "user_prompt_template": "分析以下失败：\\n用例: {{case_name}}\\n状态码: {{status_code}}\\n错误: {{error_message}}",
        "variables": ["case_name", "status_code", "error_message"],
    },
]


class PromptMarketplace:
    """Prompt 模板市场服务"""

    def get_builtin_templates(self) -> List[Dict[str, Any]]:
        """获取内置模板列表"""
        return BUILTIN_TEMPLATES

    def list_templates(self, feature: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出可用模板（内置 + 用户自定义）"""
        templates = []
        for bt in BUILTIN_TEMPLATES:
            if feature and bt["feature"] != feature:
                continue
            templates.append({**bt, "source": "builtin", "version": 1, "usage_count": 0})

        query = PromptVersion.query
        if feature:
            query = query.filter_by(feature=feature)
        for pt in query.order_by(PromptVersion.created_at.desc()).limit(100).all():
            variables = self._extract_variables(pt.user_prompt_template or "")
            templates.append({
                "id": pt.id, "feature": pt.feature, "name": pt.name,
                "system_prompt": pt.system_prompt, "user_prompt_template": pt.user_prompt_template,
                "variables": variables, "source": "custom", "version": pt.version,
                "is_active": pt.is_active, "usage_count": pt.total_invocations,
                "success_rate": round(pt.success_count / max(pt.total_invocations, 1) * 100, 1),
                "created_at": pt.created_at.isoformat() if pt.created_at else None,
            })
        return templates

    def create_template(self, feature: str, name: str, system_prompt: str,
                        user_prompt_template: str, user_id: int,
                        temperature: float = 0.3) -> Dict[str, Any]:
        """创建自定义 Prompt 模板"""
        from sqlalchemy import func
        max_ver = db.session.query(func.max(PromptVersion.version)).filter_by(feature=feature).scalar() or 0
        template = PromptVersion(
            feature=feature, name=name, version=max_ver + 1, is_active=False,
            system_prompt=system_prompt, user_prompt_template=user_prompt_template,
            temperature=temperature, change_notes="初始创建", created_by=user_id,
        )
        db.session.add(template)
        db.session.commit()
        logger.info("Prompt 模板创建成功", feature=feature, name=name, version=template.version)
        return template.to_dict()

    def render_template(self, template_id: int, variables: Dict[str, str]) -> Dict[str, str]:
        """渲染模板（替换变量占位符）"""
        template = PromptVersion.query.get(template_id)
        if not template:
            raise ValueError(f"模板 {template_id} 不存在")
        user_prompt = template.user_prompt_template or ""
        for key, value in variables.items():
            user_prompt = user_prompt.replace("{{" + key + "}}", str(value))
        return {
            "system_prompt": template.system_prompt,
            "user_prompt": user_prompt,
            "template_id": template.id,
        }

    def rollback_template(self, feature: str, target_version: int, user_id: int) -> Dict[str, Any]:
        """回滚到指定版本"""
        target = PromptVersion.query.filter_by(feature=feature, version=target_version).first()
        if not target:
            raise ValueError(f"版本 {target_version} 不存在")
        from sqlalchemy import func
        max_ver = db.session.query(func.max(PromptVersion.version)).filter_by(feature=feature).scalar() or 0
        new = PromptVersion(
            feature=feature, name=f"回滚到 v{target_version}", version=max_ver + 1,
            is_active=True, system_prompt=target.system_prompt,
            user_prompt_template=target.user_prompt_template,
            temperature=target.temperature, change_notes=f"回滚到版本 {target_version}",
            created_by=user_id,
        )
        db.session.add(new)
        db.session.commit()
        return new.to_dict()

    def _extract_variables(self, template: str) -> List[str]:
        """从模板中提取变量占位符"""
        return list(set(re.findall(r"\{\{(\w+)\}\}", template)))


_instance = None


def get_prompt_marketplace() -> PromptMarketplace:
    global _instance
    if _instance is None:
        _instance = PromptMarketplace()
    return _instance