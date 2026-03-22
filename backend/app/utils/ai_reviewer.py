"""
AI reviewer for API test collections.
Reviews existing API test cases and suggests missing boundary, exception, or security cases.
"""

import json
import logging
import os
import requests
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def review_api_collection(
    collection_name: str,
    cases: List[Dict[str, Any]],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Review a collection of API test cases and suggest new ones.
    Returns a dict with 'review_summary' and 'suggested_cases'.
    """
    if not cases:
        raise ValueError("cases list cannot be empty")

    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    timeout_val = os.environ.get("AI_ASSISTANT_TIMEOUT") or config.get("AI_ASSISTANT_TIMEOUT") or 60
    timeout = int(timeout_val)
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()

    if not api_key:
        raise ValueError("AI_ASSISTANT_API_KEY is not configured")

    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are an expert API testing and security engineer. "
        "The user will provide the name of an API collection and a list of existing test cases in JSON format. "
        "Your task is to review the current coverage and identify missing test scenarios, such as:\n"
        "- Boundary conditions (e.g., extremely large numbers, long strings)\n"
        "- Exception scenarios (e.g., missing required fields, invalid types)\n"
        "- Security vulnerabilities (e.g., SQL injection, XSS, unauthorized access attempts)\n\n"
        "You MUST return the result EXACTLY as a JSON object with two keys:\n"
        "1. 'review_summary': A detailed string explaining what is missing in plain Chinese (大白话).\n"
        "2. 'suggested_cases': A list of suggested test cases to fill the gaps. Each case must have:\n"
        "   - name (string)\n"
        "   - method (string, e.g. GET, POST)\n"
        "   - url (string)\n"
        "   - headers (object)\n"
        "   - params (object)\n"
        "   - body (object or string)\n"
        "   - body_type (string, e.g. json, form, raw)\n"
        "   - description (string explaining the purpose of this case)\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. Do NOT return markdown blocks outside the JSON. The response must be parseable by json.loads().\n"
        "2. ONLY use valid JSON syntax. DO NOT use JavaScript expressions or functions like `\"a\".repeat(1000)`. If you need a long string, write a literal string like `\"aaaa...\"` (but keep it reasonable, e.g. 50 characters) or explain it in the description."
    )

    user_content = json.dumps({
        "collection_name": collection_name,
        "existing_cases": cases
    }, ensure_ascii=False)

    payload = {
        "model": model,
        "temperature": 0.3,
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
    
    # Clean up markdown code blocks if the LLM still returns them
    cleaned_content = content.strip()
    if cleaned_content.startswith("```json"):
        cleaned_content = cleaned_content[7:]
    elif cleaned_content.startswith("```"):
        cleaned_content = cleaned_content[3:]
    if cleaned_content.endswith("```"):
        cleaned_content = cleaned_content[:-3]
    cleaned_content = cleaned_content.strip()

    try:
        result = json.loads(cleaned_content)
        return {
            "review_summary": result.get("review_summary", "无评审总结"),
            "suggested_cases": result.get("suggested_cases", [])
        }
    except json.JSONDecodeError:
        # Fallback: try to find a JSON object in the string using regex or simple search
        import re
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            try:
                # If there's invalid JS like .repeat(), let's just do a naive replace
                # This is a hacky fix for common LLM mistakes like "a".repeat(1000)
                json_str = match.group(0)
                json_str = re.sub(r'"([^"]*)"\.repeat\(\d+\)', r'"\1\1\1\1\1"', json_str)
                result = json.loads(json_str)
                return {
                    "review_summary": result.get("review_summary", "无评审总结"),
                    "suggested_cases": result.get("suggested_cases", [])
                }
            except json.JSONDecodeError:
                pass
                
        logger.error("Failed to parse JSON from LLM: %s", content)
        return {
            "review_summary": "AI 返回的数据格式无法解析。请重试，或检查其是否返回了非标准 JSON 格式（如 JavaScript 代码）。\n\n原始返回内容：\n" + content,
            "suggested_cases": []
        }
