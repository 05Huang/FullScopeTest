"""
AI 脚本生成服务

基于 PromptVersion 管理的 NL2Script 功能：
- 从数据库加载 Prompt（支持多版本 A/B 测试）
- 自动记录 AIInvocationLog
- 调用后更新 PromptVersion 统计
"""

import random
import re
from typing import Dict, Any, Optional, List

from ...extensions import db
from ...models.prompt_version import PromptVersion
from ...core.logging import get_logger
from .base import AIServiceBase

logger = get_logger(__name__)

# 默认系统提示词模板（用于初始化数据库中的 PromptVersion）
DEFAULT_WEB_SYSTEM_PROMPT = (
    "You are an expert QA engineer. "
    "Write a Python Playwright sync script based on the user's natural language description. "
    "The script should use `sync_playwright` and follow this structure:\n"
    "def run():\n"
    "    with sync_playwright() as p:\n"
    "        browser = p.chromium.launch(headless=True)\n"
    "        page = browser.new_page()\n"
    "        # your generated steps here\n"
    "        browser.close()\n"
    "        return {'status': 'success'}\n"
    "if __name__ == '__main__':\n"
    "    print(run())\n"
    "Return ONLY the python code, no markdown wrappers like ```python, no explanations."
)

DEFAULT_PERF_SYSTEM_PROMPT = (
    "You are an expert QA engineer. "
    "Write a Python Locust script based on the user's natural language description. "
    "The script should define an `HttpUser` with appropriate tasks, wait_time, and requests. "
    "Return ONLY the python code, no markdown wrappers like ```python, no explanations."
)

# feature -> 默认系统提示词映射
DEFAULT_PROMPTS = {
    'script_gen_web': DEFAULT_WEB_SYSTEM_PROMPT,
    'script_gen_perf': DEFAULT_PERF_SYSTEM_PROMPT,
}


class ScriptGeneratorService(AIServiceBase):
    """
    脚本生成服务 —— 基于 PromptVersion 的 NL2Script 引擎。

    支持 A/B 测试：同一 feature 下可有多个激活版本，按 traffic_weight 分配流量。
    每次调用后自动更新 PromptVersion 的统计指标。
    """

    FEATURE_WEB = 'script_gen_web'
    FEATURE_PERF = 'script_gen_perf'

    def generate_script(
        self,
        prompt: str,
        test_type: str,
        *,
        user_id: Optional[int] = None,
        prompt_version_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        生成测试脚本。

        Args:
            prompt: 用户的自然语言描述
            test_type: 'web' 或 'perf'
            user_id: 调用用户 ID
            prompt_version_id: 指定 Prompt 版本 ID（可选，不指定则自动选择）

        Returns:
            dict: {'script_content': str, 'prompt_version_id': int, 'prompt_version_name': str}
        """
        feature = self.FEATURE_WEB if test_type == 'web' else self.FEATURE_PERF
        if test_type not in ('web', 'perf'):
            raise ValueError(f'Unknown test_type: {test_type}')

        # 选择 Prompt 版本
        if prompt_version_id:
            pv = PromptVersion.query.get(prompt_version_id)
            if not pv or pv.feature != feature:
                raise ValueError(f'Prompt version {prompt_version_id} not found for feature {feature}')
            if not pv.is_active:
                raise ValueError(f'Prompt version {prompt_version_id} is not active')
        else:
            pv = self._select_version(feature)

        if not pv:
            raise ValueError(f'No active prompt version found for feature: {feature}')

        # 构建消息
        system_prompt = pv.system_prompt
        messages = [{'role': 'user', 'content': prompt}]

        # 调用 LLM（通过基类，自动记录日志）
        response = self.simple_chat(
            messages,
            feature=feature,
            user_id=user_id,
            prompt_version_id=pv.id,
            system_prompt=system_prompt,
            temperature=pv.temperature or 0.2,
        )

        content = self.get_content(response)

        # 清理 markdown 代码块
        content = self._clean_code_block(content)

        # 更新 PromptVersion 统计
        success = bool(content and content.strip())
        self._update_version_stats(pv, success, response)

        return {
            'script_content': content,
            'prompt_version_id': pv.id,
            'prompt_version_name': pv.name,
        }

    def _select_version(self, feature: str) -> Optional[PromptVersion]:
        """
        按 traffic_weight 加权随机选择一个激活的 PromptVersion。
        支持 A/B 测试：多个版本同时激活，按权重分配流量。
        """
        active_versions = PromptVersion.query.filter_by(
            feature=feature,
            is_active=True,
        ).all()

        if not active_versions:
            return None

        if len(active_versions) == 1:
            return active_versions[0]

        # 加权随机选择
        total_weight = sum(pv.traffic_weight or 1.0 for pv in active_versions)
        if total_weight <= 0:
            return active_versions[0]

        r = random.uniform(0, total_weight)
        cumulative = 0.0
        for pv in active_versions:
            cumulative += pv.traffic_weight or 1.0
            if r <= cumulative:
                return pv

        return active_versions[-1]

    def _update_version_stats(
        self,
        pv: PromptVersion,
        success: bool,
        response: Dict[str, Any],
    ):
        """更新 PromptVersion 的聚合统计"""
        try:
            pv.total_invocations = (pv.total_invocations or 0) + 1
            if success:
                pv.success_count = (pv.success_count or 0) + 1
            else:
                pv.failure_count = (pv.failure_count or 0) + 1

            # 更新平均延迟（滑动平均）
            latency = response.get('latency_ms', 0) or 0
            if latency > 0:
                n = pv.total_invocations
                pv.avg_latency_ms = ((pv.avg_latency_ms or 0) * (n - 1) + latency) / n

            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            logger.warning('Failed to update PromptVersion stats', error=str(exc))

    @staticmethod
    def _clean_code_block(content: str) -> str:
        """清理 LLM 返回的 markdown 代码块包装"""
        if not content:
            return ''
        content = content.strip()
        if content.startswith('```python'):
            content = content[9:]
        elif content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        return content.strip()


def ensure_default_prompt_versions():
    """
    确保默认的 PromptVersion 存在。
    在应用启动时调用，为 web 和 perf 生成各创建一个默认版本。
    """
    for feature, system_prompt in DEFAULT_PROMPTS.items():
        existing = PromptVersion.query.filter_by(feature=feature, version=1).first()
        if not existing:
            pv = PromptVersion(
                feature=feature,
                name='baseline',
                version=1,
                is_active=True,
                system_prompt=system_prompt,
                temperature=0.2,
                traffic_weight=1.0,
                change_notes='Initial baseline prompt',
            )
            db.session.add(pv)
            logger.info('Created default PromptVersion', feature=feature)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
