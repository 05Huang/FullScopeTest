"""
AI script generator for Web UI and Performance tests.
"""

import json
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

def generate_test_script(
    prompt: str,
    test_type: str,
    config: Dict[str, Any],
) -> str:
    """
    Generate test script from natural language.
    test_type: 'web' (Playwright) or 'perf' (Locust)
    """
    text = (prompt or "").strip()
    if not text:
        raise ValueError("prompt is required")

    if not config.get("AI_ASSISTANT_ENABLED", True):
        raise ValueError("AI assistant is disabled")

    api_key = str(config.get("AI_ASSISTANT_API_KEY") or "").strip()
    # Also fallback to environment variable directly in case Flask app config is out of sync
    import os
    if not api_key:
        api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or "").strip()
        
    if api_key:
        try:
            return _generate_via_llm(text, test_type, config)
        except Exception as exc:
            logger.warning("LLM generation failed: %s", exc)
            raise RuntimeError(f"Failed to generate script: {str(exc)}")
    
    raise ValueError("AI_ASSISTANT_API_KEY is not configured")


def _generate_via_llm(
    prompt: str,
    test_type: str,
    config: Dict[str, Any],
) -> str:
    import os
    
    # 获取基础 URL (优先环境变量 -> 其次配置 -> 默认值)
    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    if not base_url:
        raise ValueError("AI_ASSISTANT_BASE_URL is empty")

    # 获取模型
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    
    # 获取超时时间
    timeout_val = os.environ.get("AI_ASSISTANT_TIMEOUT") or config.get("AI_ASSISTANT_TIMEOUT") or 30
    timeout = int(timeout_val)
    
    # 获取 API Key
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()

    endpoint = f"{base_url}/chat/completions"

    if test_type == "web":
        system_prompt = (
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
    elif test_type == "perf":
        system_prompt = (
            "You are an expert QA engineer. "
            "Write a Python Locust script based on the user's natural language description. "
            "The script should define an `HttpUser` with appropriate tasks, wait_time, and requests. "
            "Return ONLY the python code, no markdown wrappers like ```python, no explanations."
        )
    else:
        raise ValueError(f"Unknown test_type: {test_type}")

    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    resp = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"LLM request failed: HTTP {resp.status_code} {resp.text}")

    data = resp.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("LLM response is empty")

    content = ((choices[0] or {}).get("message") or {}).get("content", "")
    
    # Clean up markdown code blocks if the LLM returned them anyway
    content = content.strip()
    if content.startswith("```python"):
        content = content[9:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
        
    return content.strip()
