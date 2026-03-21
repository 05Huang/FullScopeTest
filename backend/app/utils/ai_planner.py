"""
AI planner for API test workspace.

This module only generates operation plans. The actual execution is delegated
to existing backend APIs/functions by the caller to keep behavior consistent.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

ALLOWED_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
ALLOWED_OPERATION_TYPES = {
    "create_environment",
    "update_environment",
    "create_collection",
    "create_case",
    "run_collection",
    "run_case",
}


def generate_api_test_plan(
    prompt: str,
    context: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate an operation plan from natural language.

    Returns:
        {
            "summary": str,
            "operations": List[dict],
            "source": "llm" | "fallback"
        }
    """
    text = (prompt or "").strip()
    if not text:
        raise ValueError("prompt is required")

    if not config.get("AI_ASSISTANT_ENABLED", True):
        raise ValueError("AI assistant is disabled")

    api_key = str(config.get("AI_ASSISTANT_API_KEY") or "").strip()
    if api_key:
        try:
            return _generate_via_llm(text, context, config)
        except Exception as exc:
            logger.warning("LLM planning failed, fallback will be used: %s", exc)

    return _generate_fallback_plan(text, context)


def _generate_via_llm(
    prompt: str,
    context: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    base_url = str(config.get("AI_ASSISTANT_BASE_URL") or "").rstrip("/")
    if not base_url:
        raise ValueError("AI_ASSISTANT_BASE_URL is empty")

    model = str(config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    timeout = int(config.get("AI_ASSISTANT_TIMEOUT", 30))
    api_key = str(config.get("AI_ASSISTANT_API_KEY") or "").strip()

    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are an API test planning assistant. "
        "Return a single JSON object only. No markdown. "
        "Schema: "
        "{"
        '"summary":"string (在summary中用中文简要描述你计划执行的操作)",'
        '"operations":[{"type":"..."}]'
        "}. "
        "Allowed operation types: create_environment, update_environment, "
        "create_collection, create_case, run_collection, run_case. "
        "For create_case include at least name, method, url. "
        "Use existing IDs/names from context whenever possible. "
        "IMPORTANT: The 'summary' field MUST be in Chinese (简体中文)."
    )

    user_payload = {
        "prompt": prompt,
        "context": context,
    }

    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
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
        raise RuntimeError(f"LLM request failed: HTTP {resp.status_code}")

    data = resp.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("LLM response is empty")

    content = ((choices[0] or {}).get("message") or {}).get("content", "")
    raw_plan = _parse_json_content(content)
    if not isinstance(raw_plan, dict):
        raise RuntimeError("LLM plan is not a JSON object")

    normalized = _normalize_plan(raw_plan, context)
    normalized["source"] = "llm"
    return normalized


def _parse_json_content(content: Any) -> Any:
    if isinstance(content, dict):
        return content

    text = str(content or "").strip()
    if not text:
        return {}

    # Direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # JSON in markdown fences
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        pass

    # Best effort: locate first JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return {}
    return {}


def _normalize_plan(raw_plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    operations = raw_plan.get("operations") or []
    normalized_ops: List[Dict[str, Any]] = []

    if isinstance(operations, list):
        for op in operations:
            normalized = _normalize_operation(op, context)
            if normalized:
                normalized_ops.append(normalized)

    summary = str(raw_plan.get("summary") or "").strip()
    if not summary:
        summary = "AI generated operation plan"

    return {
        "summary": summary[:300],
        "operations": normalized_ops,
    }


def _normalize_operation(op: Any, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not isinstance(op, dict):
        return None

    op_type = str(op.get("type") or "").strip()
    if op_type not in ALLOWED_OPERATION_TYPES:
        return None

    selected_collection_id = _to_int(context.get("selected_collection_id"))
    selected_env_id = _to_int(context.get("selected_env_id"))

    if op_type == "create_environment":
        name = str(op.get("name") or "").strip() or _default_name("AI Environment")
        base_url = str(op.get("base_url") or "").strip() or "http://127.0.0.1:5211/api/v1"
        return {
            "type": op_type,
            "name": name,
            "base_url": base_url,
            "description": str(op.get("description") or "").strip(),
            "variables": _normalize_obj(op.get("variables")),
            "headers": _normalize_obj(op.get("headers")),
            "project_id": _to_int(op.get("project_id")),
        }

    if op_type == "update_environment":
        return {
            "type": op_type,
            "environment_id": _to_int(op.get("environment_id")),
            "environment_name": str(op.get("environment_name") or "").strip(),
            "name": str(op.get("name") or "").strip(),
            "base_url": str(op.get("base_url") or "").strip(),
            "variables": _normalize_obj(op.get("variables")),
            "headers": _normalize_obj(op.get("headers")),
        }

    if op_type == "create_collection":
        name = str(op.get("name") or "").strip() or _default_name("AI Collection")
        return {
            "type": op_type,
            "name": name,
            "description": str(op.get("description") or "").strip(),
            "project_id": _to_int(op.get("project_id")),
        }

    if op_type == "create_case":
        method = str(op.get("method") or "GET").upper()
        if method not in ALLOWED_METHODS:
            method = "GET"

        url = str(op.get("url") or "").strip() or "{{base_url}}/api-test/health"
        body = op.get("body")
        body_type = str(op.get("body_type") or "").strip()
        if not body_type:
            body_type = "json" if isinstance(body, (dict, list)) else "raw"

        return {
            "type": op_type,
            "name": str(op.get("name") or _default_name("AI Case")).strip(),
            "description": str(op.get("description") or "").strip(),
            "method": method,
            "url": url,
            "headers": _normalize_obj(op.get("headers")),
            "params": _normalize_obj(op.get("params")),
            "body": body,
            "body_type": body_type,
            "pre_script": str(op.get("pre_script") or ""),
            "post_script": str(op.get("post_script") or ""),
            "assertions": op.get("assertions") if isinstance(op.get("assertions"), list) else [],
            "collection_id": _to_int(op.get("collection_id")) or selected_collection_id,
            "collection_name": str(op.get("collection_name") or "").strip(),
            "project_id": _to_int(op.get("project_id")),
            "environment_id": _to_int(op.get("environment_id")) or selected_env_id,
            "environment_name": str(op.get("environment_name") or "").strip(),
        }

    if op_type == "run_collection":
        return {
            "type": op_type,
            "collection_id": _to_int(op.get("collection_id")) or selected_collection_id,
            "collection_name": str(op.get("collection_name") or "").strip(),
            "environment_id": _to_int(op.get("environment_id")) or selected_env_id,
            "environment_name": str(op.get("environment_name") or "").strip(),
        }

    if op_type == "run_case":
        return {
            "type": op_type,
            "case_id": _to_int(op.get("case_id")) or _to_int(context.get("selected_case_id")),
            "case_name": str(op.get("case_name") or "").strip(),
            "environment_id": _to_int(op.get("environment_id")) or selected_env_id,
            "environment_name": str(op.get("environment_name") or "").strip(),
        }

    return None


def _generate_fallback_plan(prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
    text = prompt.lower()
    selected_collection_id = _to_int(context.get("selected_collection_id"))

    operations: List[Dict[str, Any]] = []

    wants_env = any(k in text for k in ["environment", "env", "环境"])
    wants_run = any(k in text for k in ["run", "execute", "执行"])

    collection_name = _default_name("AI Collection")
    if wants_env:
        operations.append(
            {
                "type": "create_environment",
                "name": _default_name("AI Env"),
                "base_url": "http://127.0.0.1:5211/api/v1",
                "description": "Generated by fallback planner",
                "variables": {"base_url": "http://127.0.0.1:5211/api/v1"},
                "headers": {},
            }
        )

    if selected_collection_id:
        target_collection_id = selected_collection_id
    else:
        operations.append(
            {
                "type": "create_collection",
                "name": collection_name,
                "description": "Generated by fallback planner",
            }
        )
        target_collection_id = None

    operations.append(
        {
            "type": "create_case",
            "name": "Health Check",
            "description": "Verify API test module is healthy",
            "method": "GET",
            "url": "{{base_url}}/api-test/health",
            "headers": {},
            "params": {},
            "body": None,
            "body_type": "json",
            "pre_script": "",
            "post_script": (
                "pm.test('status is 200', function() {"
                "  pm.response.to.have.status(200);"
                "});"
            ),
            "collection_id": target_collection_id,
            "collection_name": "" if target_collection_id else collection_name,
        }
    )

    if wants_run:
        operations.append(
            {
                "type": "run_collection",
                "collection_id": target_collection_id,
                "collection_name": "" if target_collection_id else collection_name,
            }
        )

    return {
        "summary": "Fallback plan generated because external LLM is unavailable",
        "operations": operations,
        "source": "fallback",
    }


def _normalize_obj(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _to_int(value: Any) -> Optional[int]:
    try:
        if value is None or value == "":
            return None
        return int(value)
    except Exception:
        return None


def _default_name(prefix: str) -> str:
    ts = datetime.utcnow().strftime("%m%d-%H%M%S")
    return f"{prefix} {ts}"

