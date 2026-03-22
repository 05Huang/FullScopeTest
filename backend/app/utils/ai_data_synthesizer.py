"""
AI data synthesizer for API testing.
Generates boundary cases, invalid inputs, and security payloads based on a base API request.
"""

import json
import logging
import os
import requests
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def synthesize_test_cases(
    base_request: Dict[str, Any],
    count: int,
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Generate mutated test cases based on a base API request.
    Returns a list of dicts, each representing a test case.
    """
    if not base_request:
        raise ValueError("base_request is required")

    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    timeout_val = os.environ.get("AI_ASSISTANT_TIMEOUT") or config.get("AI_ASSISTANT_TIMEOUT") or 30
    timeout = int(timeout_val)
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()

    if not api_key:
        raise ValueError("AI_ASSISTANT_API_KEY is not configured")

    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are an expert API testing engineer. "
        "The user will provide a base API request (method, url, headers, params, body). "
        f"Your task is to generate {count} new, mutated test cases to thoroughly test the API's robustness. "
        "Include boundary values, empty values, missing fields, type mismatches, and potential security injections (e.g., SQLi, XSS) where applicable in the params or body.\n\n"
        "You MUST return the result EXACTLY as a JSON object containing a 'cases' array. "
        "Each case in the array should have the following structure:\n"
        "{\n"
        "  'name': 'string, brief description of the test case intent IN CHINESE (必须使用中文描述)',\n"
        "  'method': 'string, e.g., GET, POST',\n"
        "  'url': 'string, the request URL',\n"
        "  'headers': { ... },\n"
        "  'params': { ... },\n"
        "  'body': { ... },\n"
        "  'body_type': 'string, usually json or form'\n"
        "}\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. Do NOT return markdown blocks outside the JSON. The response must be parseable by json.loads().\n"
        "2. ONLY use valid JSON syntax. DO NOT use JavaScript expressions or functions like `\"a\".repeat(1000)`. If you need a long string, write a literal string."
    )

    user_content = json.dumps(base_request, ensure_ascii=False, indent=2)

    payload = {
        "model": model,
        "temperature": 0.7,
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
    
    # Clean up markdown code blocks
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
        cases = result.get("cases", [])
        if not isinstance(cases, list):
            return []
        return cases
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            try:
                json_str = match.group(0)
                json_str = re.sub(r'"([^"]*)"\.repeat\(\d+\)', r'"\1\1\1\1\1"', json_str)
                result = json.loads(json_str)
                cases = result.get("cases", [])
                if not isinstance(cases, list):
                    return []
                return cases
            except json.JSONDecodeError:
                pass
        logger.error("Failed to parse JSON from LLM in data synthesizer: %s", content)
        return []
