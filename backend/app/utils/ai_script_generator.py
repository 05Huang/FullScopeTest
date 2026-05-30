"""
AI script generator for Web UI and Performance tests.

使用 AIServiceBase 和 PromptVersion 管理 Prompt，支持 A/B 测试和调用日志记录。
"""

import os
import re
from typing import Dict, Any, Optional

from ..core.logging import get_logger
from ..services.ai.base import AIServiceBase
from ..services.ai.prompt_version_service import prompt_version_service

logger = get_logger(__name__)

# ---- 默认系统 Prompt（当数据库中没有 PromptVersion 时使用） ----

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

DEFAULT_SYSTEM_PROMPTS = {
    'web': DEFAULT_WEB_SYSTEM_PROMPT,
    'perf': DEFAULT_PERF_SYSTEM_PROMPT,
}


def _clean_code_blocks(content: str) -> str:
    """清理 LLM 返回的 markdown 代码块"""
    content = content.strip()
    if content.startswith("```python"):
        content = content[9:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()


def _build_service(config: Dict[str, Any]) -> AIServiceBase:
    """从 Flask config 构建 AIServiceBase 实例"""
    return AIServiceBase(
        base_url=config.get('AI_ASSISTANT_BASE_URL'),
        api_key=config.get('AI_ASSISTANT_API_KEY'),
        model=config.get('AI_ASSISTANT_MODEL'),
        timeout=int(config.get('AI_ASSISTANT_TIMEOUT', 30)),
        config=config,
    )


def generate_test_script(
    prompt: str,
    test_type: str,
    config: Dict[str, Any],
    *,
    user_id: Optional[int] = None,
) -> str:
    """
    Generate test script from natural language.
    test_type: 'web' (Playwright) or 'perf' (Locust)

    使用 PromptVersion 管理 Prompt：
    1. 尝试通过 A/B 测试选择数据库中的 PromptVersion
    2. 如果没有激活版本，使用默认 Prompt
    3. 通过 AIServiceBase 调用 LLM，自动记录 AIInvocationLog
    """
    text = (prompt or "").strip()
    if not text:
        raise ValueError("prompt is required")

    if not config.get("AI_ASSISTANT_ENABLED", True):
        raise ValueError("AI assistant is disabled")

    # 通过 A/B 测试选择 Prompt 版本（web 和 perf 使用不同的 feature）
    feature = f'script_gen_{test_type}'
    pv = prompt_version_service.select_version_for_ab_test(feature)

    if pv:
        # 使用数据库中的 PromptVersion
        system_prompt = pv.system_prompt
        temperature = pv.temperature or 0.2
        prompt_version_id = pv.id
        model_override = pv.model_name  # 可能为 None，使用全局默认
        logger.info(
            'Using PromptVersion for script generation',
            version_id=pv.id,
            name=pv.name,
            version=pv.version,
        )
    else:
        # 使用默认 Prompt
        system_prompt = DEFAULT_SYSTEM_PROMPTS.get(test_type)
        if not system_prompt:
            raise ValueError(f"Unknown test_type: {test_type}")
        temperature = 0.2
        prompt_version_id = None
        model_override = None
        logger.info('No active PromptVersion found, using default prompt')

    # 构建服务
    svc_kwargs: Dict[str, Any] = {'config': config}
    if model_override:
        svc_kwargs['model'] = model_override

    service = _build_service(svc_kwargs)

    # 调用 LLM
    response = service.simple_chat(
        messages=[{'role': 'user', 'content': text}],
        feature='script_gen',
        user_id=user_id,
        prompt_version_id=prompt_version_id,
        system_prompt=system_prompt,
        temperature=temperature,
    )

    content = service.get_content(response)
    return _clean_code_blocks(content)

