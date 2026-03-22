"""
AI Global Search Utility
Extracts intent from natural language query and searches the database.
"""

import json
import logging
import os
import requests
from typing import Dict, Any, List
from ..extensions import db
from ..models.api_test_case import ApiTestCase
from ..models.web_test_script import WebTestScript
from ..models.perf_test_scenario import PerfTestScenario
from ..models.environment import Environment

logger = logging.getLogger(__name__)

def execute_global_search(
    query: str,
    user_id: int,
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Parse search intent using AI and perform database search.
    """
    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    timeout_val = os.environ.get("AI_ASSISTANT_TIMEOUT") or config.get("AI_ASSISTANT_TIMEOUT") or 30
    timeout = int(timeout_val)
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()

    if not api_key:
        raise ValueError("AI_ASSISTANT_API_KEY is not configured")

    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are an AI assistant that extracts search intents. "
        "The user will provide a natural language search query. "
        "Your task is to extract the keywords and target asset types from the query.\n\n"
        "Valid asset types are: 'api_case', 'web_script', 'perf_scenario', 'environment'.\n"
        "If the query implies searching all assets, return all valid types.\n\n"
        "You MUST return EXACTLY a JSON object with:\n"
        "- 'keywords': A list of strings (the core search terms, do not include words like '查找', '所有', '关于').\n"
        "- 'asset_types': A list of strings (the valid asset types inferred).\n"
        "Do NOT return markdown blocks outside the JSON."
    )

    payload = {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    }

    try:
        resp = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        intent = json.loads(content)
        keywords = intent.get("keywords", [])
        asset_types = intent.get("asset_types", ["api_case", "web_script", "perf_scenario", "environment"])
    except Exception as e:
        logger.error(f"AI search intent extraction failed: {e}")
        # Fallback: simple keyword split
        keywords = query.split()
        asset_types = ["api_case", "web_script", "perf_scenario", "environment"]

    if not keywords:
        keywords = [query]
        
    results = []

    # Helper function to construct LIKE filters
    def build_like_filters(model_class, fields, kws):
        from sqlalchemy import or_, and_
        conditions = []
        for kw in kws:
            kw_condition = or_(*[getattr(model_class, field).ilike(f"%{kw}%") for field in fields])
            conditions.append(kw_condition)
        return and_(*conditions)

    if "api_case" in asset_types:
        try:
            filters = build_like_filters(ApiTestCase, ['name', 'description', 'url'], keywords)
            cases = ApiTestCase.query.filter_by(user_id=user_id).filter(filters).limit(20).all()
            for c in cases:
                results.append({
                    "id": c.id,
                    "type": "api_case",
                    "title": c.name,
                    "description": c.description or c.url,
                    "url": f"/api-test"
                })
        except Exception as e:
            logger.error(f"Error searching api_case: {e}")

    if "web_script" in asset_types:
        try:
            filters = build_like_filters(WebTestScript, ['name', 'description', 'script_content'], keywords)
            scripts = WebTestScript.query.filter_by(user_id=user_id).filter(filters).limit(20).all()
            for s in scripts:
                results.append({
                    "id": s.id,
                    "type": "web_script",
                    "title": s.name,
                    "description": s.description or "Web自动化脚本",
                    "url": f"/web-test"
                })
        except Exception as e:
            logger.error(f"Error searching web_script: {e}")

    if "perf_scenario" in asset_types:
        try:
            filters = build_like_filters(PerfTestScenario, ['name', 'description', 'target_url'], keywords)
            scenarios = PerfTestScenario.query.filter_by(user_id=user_id).filter(filters).limit(20).all()
            for s in scenarios:
                results.append({
                    "id": s.id,
                    "type": "perf_scenario",
                    "title": s.name,
                    "description": s.description or s.target_url,
                    "url": f"/perf-test"
                })
        except Exception as e:
            logger.error(f"Error searching perf_scenario: {e}")

    if "environment" in asset_types:
        try:
            # Environment doesn't have user_id directly, but we can query by projects owned by user.
            # However, for simplicity, we can join Project.
            from ..models.project import Project
            filters = build_like_filters(Environment, ['name', 'base_url', 'description'], keywords)
            envs = db.session.query(Environment).join(Project).filter(Project.owner_id == user_id).filter(filters).limit(20).all()
            for e in envs:
                results.append({
                    "id": e.id,
                    "type": "environment",
                    "title": e.name,
                    "description": e.description or e.base_url,
                    "url": f"/settings/environments"
                })
        except Exception as e:
            logger.error(f"Error searching environment: {e}")

    return results
