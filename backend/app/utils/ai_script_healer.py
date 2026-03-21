"""
AI error analyzer and healer for test scripts.
"""

import json
import logging
import os
import requests
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

def analyze_test_error(
    script_content: str,
    error_log: str,
    test_type: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Analyze test error and return analysis and potential fix.
    Returns: {"analysis": str, "fixed_script": str}
    """
    if not error_log:
        raise ValueError("error_log is required")

    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    timeout_val = os.environ.get("AI_ASSISTANT_TIMEOUT") or config.get("AI_ASSISTANT_TIMEOUT") or 30
    timeout = int(timeout_val)
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()

    if not api_key:
        raise ValueError("AI_ASSISTANT_API_KEY is not configured")

    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are an expert QA engineer and debugging assistant. "
        "The user will provide a test script and the error log it produced when executed. "
        "Your task is to:\n"
        "1. Analyze the root cause of the error in plain Chinese (大白话).\n"
        "2. Provide a fixed version of the script if possible.\n"
        "You MUST return the result EXACTLY as a JSON object with two keys: 'analysis' and 'fixed_script'.\n"
        "For 'fixed_script', provide the FULL updated python code. If no fix is possible, return null for 'fixed_script'.\n"
        "Do NOT return markdown blocks outside the JSON. The response must be parseable by json.loads()."
    )

    user_content = f"Test Type: {test_type}\n\n=== Script Content ===\n{script_content}\n\n=== Error Log ===\n{error_log}"

    payload = {
        "model": model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
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
        logger.error("LLM request failed: %s", resp.text)
        raise RuntimeError(f"LLM request failed: HTTP {resp.status_code}")

    data = resp.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("LLM response is empty")

    content = ((choices[0] or {}).get("message") or {}).get("content", "")
    
    try:
        result = json.loads(content)
        return {
            "analysis": result.get("analysis", "No analysis provided."),
            "fixed_script": result.get("fixed_script")
        }
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON from LLM: %s", content)
        return {
            "analysis": "AI response was not valid JSON. Raw output: " + content,
            "fixed_script": None
        }
