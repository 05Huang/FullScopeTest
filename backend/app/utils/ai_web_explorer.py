"""
AI Autonomous Web Explorer.
Uses Playwright to navigate a web application and LLM to decide actions.
"""

import base64
import json
import logging
import os
import subprocess
import sys
import time
from typing import Dict, Any, List
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


def _install_playwright_chromium() -> None:
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
        capture_output=True,
        text=True,
        timeout=600,
    )


def _launch_chromium_with_fallback(playwright_instance: Any):
    try:
        return playwright_instance.chromium.launch(headless=True)
    except Exception as launch_error:
        error_message = str(launch_error)
        if "Executable doesn't exist" not in error_message:
            raise
        logger.warning("Chromium executable missing, trying to auto install Playwright browser.")
        try:
            _install_playwright_chromium()
        except Exception as install_error:
            raise RuntimeError(
                "Playwright Chromium 浏览器未安装且自动安装失败，请手动执行: playwright install chromium"
            ) from install_error
        return playwright_instance.chromium.launch(headless=True)

def run_exploration_task(
    start_url: str,
    max_steps: int,
    objective: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Run an autonomous web exploration task.
    """
    from playwright.sync_api import sync_playwright
    
    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()
    vision_base_url = str(os.environ.get("AI_VISION_BASE_URL") or config.get("AI_VISION_BASE_URL") or base_url).rstrip("/")
    vision_model = str(os.environ.get("AI_VISION_MODEL") or config.get("AI_VISION_MODEL") or model)
    vision_api_key = str(os.environ.get("AI_VISION_API_KEY") or config.get("AI_VISION_API_KEY") or api_key).strip()

    if not api_key:
        raise ValueError("AI_ASSISTANT_API_KEY is not configured")

    report = {
        "start_url": start_url,
        "objective": objective,
        "total_steps_executed": 0,
        "visited_urls": [],
        "errors_found": [],
        "actions_taken": [],
        "status": "completed"
    }

    try:
        with sync_playwright() as p:
            browser = _launch_chromium_with_fallback(p)
            context = browser.new_context(viewport={'width': 1280, 'height': 720})
            page = context.new_page()
            
            # 捕获控制台错误
            def handle_console(msg):
                if msg.type == 'error':
                    report["errors_found"].append({
                        "type": "console_error",
                        "url": page.url,
                        "text": msg.text,
                        "time": time.time()
                    })
            page.on("console", handle_console)
            
            # 捕获页面错误
            def handle_page_error(exc):
                report["errors_found"].append({
                    "type": "page_error",
                    "url": page.url,
                    "text": str(exc),
                    "time": time.time()
                })
            page.on("pageerror", handle_page_error)
            
            # 捕获请求失败 (如 404, 500)
            def handle_response(response):
                if response.status >= 400:
                    report["errors_found"].append({
                        "type": "network_error",
                        "url": page.url,
                        "request_url": response.url,
                        "status": response.status,
                        "time": time.time()
                    })
            page.on("response", handle_response)

            logger.info(f"Starting exploration at {start_url}")
            page.goto(start_url, wait_until="networkidle")
            report["visited_urls"].append(page.url)

            for step in range(max_steps):
                report["total_steps_executed"] += 1
                current_url = page.url
                
                # 提取页面交互元素简化版 (提取带 a, button, input 标签)
                elements = page.evaluate('''() => {
                    const interactables = [];
                    const nodes = document.querySelectorAll('a, button, input');
                    nodes.forEach((node, index) => {
                        const rect = node.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            let text = node.innerText || node.value || node.placeholder || node.name || '';
                            text = text.trim().substring(0, 50);
                            if (text || node.tagName === 'INPUT') {
                                // 为元素添加临时属性以便后续点击
                                node.setAttribute('data-ai-id', `ai-elem-${index}`);
                                interactables.push({
                                    id: `ai-elem-${index}`,
                                    tag: node.tagName.toLowerCase(),
                                    type: node.type || '',
                                    text: text
                                });
                            }
                        }
                    });
                    return interactables;
                }''')
                
                # 请求 LLM 决定下一步
                screenshot_base64 = ""
                try:
                    screenshot_bytes = page.screenshot(type="jpeg", quality=65, full_page=False)
                    screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
                except Exception as screenshot_error:
                    logger.warning(f"Failed to capture screenshot on step {step}: {screenshot_error}")

                action = _decide_next_action(
                    current_url, 
                    elements, 
                    objective, 
                    report["actions_taken"][-5:], # 提供最近5步历史防止循环
                    screenshot_base64,
                    api_key, 
                    base_url, 
                    model,
                    vision_api_key,
                    vision_base_url,
                    vision_model,
                )
                
                if not action or action.get("action") == "stop":
                    logger.info("AI decided to stop exploration.")
                    report["actions_taken"].append({"step": step, "url": current_url, "action": "stop", "reason": action.get("reason", "Goal achieved or stuck")})
                    break

                act_type = action.get("action")
                target_id = action.get("target_id")
                input_value = action.get("input_value", "")
                
                action_record = {
                    "step": step,
                    "url": current_url,
                    "type": act_type,
                    "target_id": target_id,
                    "reason": action.get("reason", "")
                }

                try:
                    if act_type == "click" and target_id:
                        selector = f"[data-ai-id='{target_id}']"
                        page.wait_for_selector(selector, timeout=3000)
                        page.click(selector)
                        page.wait_for_load_state("networkidle", timeout=5000)
                    elif act_type == "input" and target_id:
                        selector = f"[data-ai-id='{target_id}']"
                        page.wait_for_selector(selector, timeout=3000)
                        page.fill(selector, input_value)
                        action_record["input_value"] = input_value
                    
                    if page.url not in report["visited_urls"]:
                        report["visited_urls"].append(page.url)
                        
                except Exception as e:
                    logger.warning(f"Failed to execute action {act_type} on {target_id}: {e}")
                    action_record["error"] = str(e)
                
                report["actions_taken"].append(action_record)
                time.sleep(1) # 短暂等待页面稳定

            browser.close()
    except Exception as e:
        logger.error(f"Exploration failed: {e}")
        report["status"] = "failed"
        report["error_message"] = str(e)

    return report

def _decide_next_action(
    current_url: str,
    elements: List[Dict],
    objective: str,
    history: List[Dict],
    screenshot_base64: str,
    api_key: str,
    base_url: str,
    model: str,
    vision_api_key: str,
    vision_base_url: str,
    vision_model: str,
) -> Dict[str, Any]:
    import requests
    
    system_prompt = (
        "You are an Autonomous Web Explorer Agent. "
        "Your task is to navigate a web page to achieve the user's objective, or just explore to find errors. "
        "You will be given the current URL, recent action history, and a list of interactable elements on the page. "
        "You must choose ONE action to perform.\n\n"
        "Available actions:\n"
        "1. click: Click an element. Requires 'target_id'.\n"
        "2. input: Type text into an input field. Requires 'target_id' and 'input_value'.\n"
        "3. stop: Stop exploration if objective is met or you are stuck in a loop.\n\n"
        "You MUST return ONLY a JSON object with the following structure:\n"
        "{\n"
        "  'action': 'click' | 'input' | 'stop',\n"
        "  'target_id': 'string (id of the element to interact with, e.g., ai-elem-5)',\n"
        "  'input_value': 'string (only if action is input)',\n"
        "  'reason': 'string (请用中文简短解释为什么选择这个操作)'\n"
        "}"
    )
    
    # 限制元素数量以防止上下文超限
    elements_subset = elements[:50]
    
    user_text_content = json.dumps({
        "objective": objective,
        "current_url": current_url,
        "recent_history": history,
        "interactable_elements": elements_subset
    }, indent=2)

    def _parse_action_response(resp: Any) -> Dict[str, Any]:
        if resp.status_code != 200:
            return {}
        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        if isinstance(content, dict):
            return content
        if not isinstance(content, str):
            return {}
        content_text = content.strip()
        if not content_text:
            return {}
        return json.loads(content_text)

    try:
        vision_user_content: Any = [{"type": "text", "text": user_text_content}]
        if screenshot_base64:
            vision_user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{screenshot_base64}"}
            })
        vision_payload = {
            "model": vision_model,
            "temperature": 0.5,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": vision_user_content},
            ],
        }
        vision_resp = requests.post(
            f"{vision_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {vision_api_key}",
                "Content-Type": "application/json",
            },
            json=vision_payload,
            timeout=20,
        )
        vision_action = _parse_action_response(vision_resp)
        if vision_action:
            return vision_action
        logger.warning(
            "Vision action decision failed with status %s, falling back to text model.",
            vision_resp.status_code,
        )
    except Exception as e:
        logger.error(f"Vision LLM decision failed: {e}")

    fallback_payload = {
        "model": model,
        "temperature": 0.5,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text_content},
        ],
    }

    try:
        fallback_resp = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=fallback_payload,
            timeout=15,
        )
        fallback_action = _parse_action_response(fallback_resp)
        if fallback_action:
            return fallback_action
        logger.warning("Text fallback decision failed with status %s.", fallback_resp.status_code)
    except Exception as e:
        logger.error(f"Text LLM decision failed: {e}")
    
    return {"action": "stop", "reason": "Failed to get LLM decision"}
