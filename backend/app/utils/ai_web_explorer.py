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
from typing import Dict, Any, List, Optional, Callable
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


def _select_input_target(elements: List[Dict[str, Any]]) -> Optional[str]:
    preferred_input_types = {"search", "text", "url", "email", "tel", ""}
    for element in elements:
        if element.get("tag") != "input":
            continue
        input_type = str(element.get("type") or "").lower()
        if input_type in preferred_input_types:
            return str(element.get("id") or "")
    for element in elements:
        if element.get("tag") == "textarea":
            return str(element.get("id") or "")
    return None


def _build_input_text(objective: str) -> str:
    candidate = " ".join(str(objective or "").split())
    if not candidate:
        return "探索测试"
    return candidate[:24]


def _classify_error_level(error_type: str, text: str = "", status: Optional[int] = None, request_url: str = "") -> Dict[str, str]:
    text_lower = str(text or "").lower()
    request_url_lower = str(request_url or "").lower()
    if error_type == "network_error":
        if status is not None and status >= 500:
            return {"severity": "critical", "category": "server"}
        if "captcha" in request_url_lower or "wappass.baidu.com" in request_url_lower:
            return {"severity": "warning", "category": "anti_bot"}
        if request_url_lower.endswith(".svg") or request_url_lower.endswith(".png") or request_url_lower.endswith(".jpg"):
            return {"severity": "info", "category": "asset"}
        return {"severity": "warning", "category": "network"}
    if error_type == "page_error":
        if "hydration failed" in text_lower or "react error #418" in text_lower:
            return {"severity": "warning", "category": "hydration"}
        return {"severity": "critical", "category": "runtime"}
    if error_type == "console_error":
        if "cors policy" in text_lower:
            return {"severity": "warning", "category": "cors"}
        if "failed to load resource" in text_lower:
            return {"severity": "info", "category": "asset"}
        if "failed to fetch rsc payload" in text_lower:
            return {"severity": "warning", "category": "rsc"}
        return {"severity": "warning", "category": "console"}
    if error_type == "step_collect_error":
        return {"severity": "warning", "category": "navigation"}
    return {"severity": "warning", "category": "unknown"}


def _append_error(report: Dict[str, Any], error_item: Dict[str, Any]) -> None:
    report["errors_found"].append(error_item)
    summary = report.get("error_summary")
    if not isinstance(summary, dict):
        return
    severity = str(error_item.get("severity") or "warning")
    if severity not in summary:
        summary[severity] = 0
    summary[severity] += 1

def run_exploration_task(
    start_url: str,
    max_steps: int,
    objective: str,
    config: Dict[str, Any],
    log_callback: Optional[Callable[[str], None]] = None,
    progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """
    Run an autonomous web exploration task.
    """
    from playwright.sync_api import sync_playwright
    
    def _emit_log(message: str) -> None:
        logger.info(message)
        if log_callback:
            try:
                log_callback(message)
            except Exception:
                logger.exception("Failed to emit exploration log callback")

    def _emit_progress(payload: Dict[str, Any]) -> None:
        if progress_callback:
            try:
                progress_callback(payload)
            except Exception:
                logger.exception("Failed to emit exploration progress callback")

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
        "error_summary": {
            "critical": 0,
            "warning": 0,
            "info": 0
        },
        "actions_taken": [],
        "status": "completed"
    }

    def _capture_preview_data_url(target_page: Any) -> str:
        try:
            screenshot_bytes = target_page.screenshot(type="jpeg", quality=55, full_page=False)
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            return f"data:image/jpeg;base64,{screenshot_base64}"
        except Exception:
            return ""

    try:
        with sync_playwright() as p:
            _emit_log(f"启动浏览器并打开页面: {start_url}")
            browser = _launch_chromium_with_fallback(p)
            context = browser.new_context(viewport={'width': 1280, 'height': 720})
            page = context.new_page()
            
            def bind_page_listeners(bound_page: Any) -> None:
                def handle_console(msg):
                    if msg.type == 'error':
                        level = _classify_error_level("console_error", text=msg.text)
                        error_item = {
                            "type": "console_error",
                            "url": bound_page.url,
                            "text": msg.text,
                            "severity": level["severity"],
                            "category": level["category"],
                            "time": time.time()
                        }
                        _append_error(report, error_item)
                        _emit_log(f"页面控制台错误: {msg.text}")
                bound_page.on("console", handle_console)

                def handle_page_error(exc):
                    level = _classify_error_level("page_error", text=str(exc))
                    error_item = {
                        "type": "page_error",
                        "url": bound_page.url,
                        "text": str(exc),
                        "severity": level["severity"],
                        "category": level["category"],
                        "time": time.time()
                    }
                    _append_error(report, error_item)
                    _emit_log(f"页面运行时错误: {str(exc)}")
                bound_page.on("pageerror", handle_page_error)

                def handle_response(response):
                    if response.status >= 400:
                        level = _classify_error_level(
                            "network_error",
                            status=response.status,
                            request_url=response.url
                        )
                        error_item = {
                            "type": "network_error",
                            "url": bound_page.url,
                            "request_url": response.url,
                            "status": response.status,
                            "severity": level["severity"],
                            "category": level["category"],
                            "time": time.time()
                        }
                        _append_error(report, error_item)
                        _emit_log(f"网络错误: {response.status} {response.url}")
                bound_page.on("response", handle_response)

            bind_page_listeners(page)

            _emit_log(f"开始探索: {start_url}")
            page.goto(start_url, wait_until="networkidle")
            report["visited_urls"].append(page.url)
            _emit_log(f"已进入页面: {page.url}")
            _emit_progress({
                "phase": "started",
                "step": 0,
                "max_steps": max_steps,
                "current_url": page.url,
                "action": "goto",
                "status": "running",
                "screenshot": _capture_preview_data_url(page),
            })

            for step in range(max_steps):
                report["total_steps_executed"] += 1
                current_url = page.url
                _emit_log(f"执行步骤 {step + 1}/{max_steps}，当前页面: {current_url}")
                _emit_progress({
                    "phase": "step_start",
                    "step": step + 1,
                    "max_steps": max_steps,
                    "current_url": current_url,
                    "action": "analyze",
                    "status": "running",
                    "screenshot": _capture_preview_data_url(page),
                })
                
                # 提取页面交互元素简化版 (提取带 a, button, input 标签)
                elements: List[Dict[str, Any]] = []
                element_collect_error = None
                for collect_attempt in range(2):
                    try:
                        elements = page.evaluate('''() => {
                            const interactables = [];
                            const nodes = document.querySelectorAll('a, button, input, textarea, [role="button"], [onclick], [tabindex]');
                            nodes.forEach((node, index) => {
                                const rect = node.getBoundingClientRect();
                                if (rect.width > 0 && rect.height > 0) {
                                    let text = node.innerText || node.value || node.placeholder || node.name || '';
                                    text = text.trim().substring(0, 50);
                                    if (text || node.tagName === 'INPUT') {
                                        node.setAttribute('data-ai-id', `ai-elem-${index}`);
                                        interactables.push({
                                            id: `ai-elem-${index}`,
                                            tag: node.tagName.toLowerCase(),
                                            type: node.type || '',
                                            text: text,
                                            href: node.href || ''
                                        });
                                    }
                                }
                            });
                            return interactables;
                        }''')
                        element_collect_error = None
                        break
                    except Exception as collect_error:
                        element_collect_error = collect_error
                        collect_error_text = str(collect_error)
                        recoverable = (
                            "Execution context was destroyed" in collect_error_text
                            or "Cannot find context" in collect_error_text
                        )
                        if recoverable and collect_attempt == 0:
                            _emit_log("检测到页面跳转导致上下文失效，等待页面稳定后重试元素采集")
                            try:
                                page.wait_for_load_state("domcontentloaded", timeout=5000)
                            except Exception:
                                pass
                            continue
                        break
                if element_collect_error:
                    error_text = str(element_collect_error)
                    level = _classify_error_level("step_collect_error", text=error_text)
                    _emit_log(f"步骤 {step + 1} 元素采集失败，跳过当前步: {error_text}")
                    _append_error(report, {
                        "type": "step_collect_error",
                        "url": page.url,
                        "text": error_text,
                        "severity": level["severity"],
                        "category": level["category"],
                        "time": time.time()
                    })
                    report["actions_taken"].append({
                        "step": step,
                        "url": current_url,
                        "type": "skip",
                        "reason": "页面跳转中导致元素采集失败，已跳过当前步",
                        "error": error_text,
                        "provider": "runtime",
                        "decision_latency_ms": None
                    })
                    time.sleep(0.5)
                    continue
                _emit_log(f"识别到可交互元素: {len(elements)} 个")
                
                # 请求 LLM 决定下一步
                screenshot_base64 = ""
                try:
                    screenshot_bytes = page.screenshot(type="jpeg", quality=65, full_page=False)
                    screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
                except Exception as screenshot_error:
                    logger.warning(f"Failed to capture screenshot on step {step}: {screenshot_error}")

                action: Dict[str, Any]
                recent_same_url_clicks = [
                    item for item in report["actions_taken"][-3:]
                    if item.get("url") == current_url and item.get("type") == "click" and not item.get("error")
                ]
                forced_target = None
                if len(recent_same_url_clicks) >= 2:
                    forced_target = _select_input_target(elements)
                if forced_target:
                    action = {
                        "action": "input",
                        "target_id": forced_target,
                        "input_value": _build_input_text(objective),
                        "reason": "检测到同页连续点击，切换为输入路径",
                        "_provider": "rule_engine",
                        "_latency_ms": 0,
                    }
                    _emit_log(f"触发反循环策略，改为输入动作: target={forced_target}")
                else:
                    action = _decide_next_action(
                        current_url,
                        elements,
                        objective,
                        report["actions_taken"][-5:],
                        screenshot_base64,
                        api_key,
                        base_url,
                        model,
                        vision_api_key,
                        vision_base_url,
                        vision_model,
                        decision_log_callback=_emit_log,
                    )
                
                if not action or action.get("action") == "stop":
                    _emit_log(f"Agent 决定停止探索: {action.get('reason', 'Goal achieved or stuck') if action else 'No action returned'}")
                    report["actions_taken"].append({
                        "step": step,
                        "url": current_url,
                        "action": "stop",
                        "reason": action.get("reason", "Goal achieved or stuck"),
                        "provider": action.get("_provider", "unknown"),
                        "decision_latency_ms": action.get("_latency_ms")
                    })
                    break

                act_type = action.get("action")
                target_id = action.get("target_id")
                input_value = action.get("input_value", "")
                decision_provider = action.get("_provider", "unknown")
                decision_latency_ms = action.get("_latency_ms")
                target_meta = next((item for item in elements if item.get("id") == target_id), None) if target_id else None
                target_tag = (target_meta or {}).get("tag", "")
                target_text = (target_meta or {}).get("text", "")
                target_type = (target_meta or {}).get("type", "")
                target_href = (target_meta or {}).get("href", "")
                target_desc = f"id={target_id or '-'}, tag={target_tag or '-'}, type={target_type or '-'}, text={target_text or '-'}, href={target_href or '-'}"
                
                action_record = {
                    "step": step,
                    "url": current_url,
                    "type": act_type,
                    "target_id": target_id,
                    "target_tag": target_tag,
                    "target_type": target_type,
                    "target_text": target_text,
                    "reason": action.get("reason", ""),
                    "provider": decision_provider,
                    "decision_latency_ms": decision_latency_ms
                }
                _emit_log(f"步骤 {step + 1} 动作决策: {act_type} -> {target_desc}，provider={decision_provider}，latency={decision_latency_ms}ms")

                try:
                    if act_type == "click" and target_id:
                        selector = f"[data-ai-id='{target_id}']"
                        before_click_url = page.url
                        page_count_before = len(context.pages)
                        page.wait_for_selector(selector, timeout=3000)
                        page.click(selector)
                        switched_to_new_tab = False
                        try:
                            page.wait_for_load_state("networkidle", timeout=5000)
                        except Exception:
                            pass
                        if len(context.pages) > page_count_before:
                            new_page = context.pages[-1]
                            if new_page != page:
                                page = new_page
                                bind_page_listeners(page)
                                switched_to_new_tab = True
                                try:
                                    page.wait_for_load_state("networkidle", timeout=5000)
                                except Exception:
                                    pass
                                _emit_log(f"步骤 {step + 1} 检测到新标签页并切换，当前页面: {page.url}")
                        if page.url == before_click_url and not switched_to_new_tab:
                            _emit_log(f"步骤 {step + 1} 点击后 URL 未变化，可能是站点拦截、前端拦截或同页异步行为")
                            if target_href and str(target_href).startswith(("http://", "https://")):
                                _emit_log(f"步骤 {step + 1} 尝试按 href 直达: {target_href}")
                                try:
                                    page.goto(str(target_href), wait_until="networkidle", timeout=8000)
                                    _emit_log(f"步骤 {step + 1} href 直达成功，当前页面: {page.url}")
                                except Exception as nav_error:
                                    _emit_log(f"步骤 {step + 1} href 直达失败: {str(nav_error)}")
                        _emit_log(f"步骤 {step + 1} 点击目标详情: {target_desc}")
                    elif act_type == "input" and target_id:
                        selector = f"[data-ai-id='{target_id}']"
                        page.wait_for_selector(selector, timeout=3000)
                        page.fill(selector, input_value)
                        page.press(selector, "Enter")
                        try:
                            page.wait_for_load_state("networkidle", timeout=5000)
                        except Exception:
                            pass
                        action_record["input_value"] = input_value
                        _emit_log(f"步骤 {step + 1} 输入目标详情: {target_desc}，input={input_value}")
                    
                    if page.url not in report["visited_urls"]:
                        report["visited_urls"].append(page.url)
                    _emit_log(f"步骤 {step + 1} 动作执行完成，当前页面: {page.url}")
                    _emit_progress({
                        "phase": "step_done",
                        "step": step + 1,
                        "max_steps": max_steps,
                        "current_url": page.url,
                        "action": act_type,
                        "target_id": target_id,
                        "reason": action.get("reason", ""),
                        "status": "running",
                        "screenshot": _capture_preview_data_url(page),
                    })
                    if "wappass.baidu.com/static/captcha" in str(page.url):
                        action_record["warning"] = "captcha_blocked"
                        _emit_log("检测到验证码挑战页，提前结束探索以避免无效循环")
                        report["actions_taken"].append(action_record)
                        report["status"] = "blocked_by_captcha"
                        break
                        
                except Exception as e:
                    logger.warning(f"Failed to execute action {act_type} on {target_id}: {e}")
                    action_record["error"] = str(e)
                    _emit_log(f"步骤 {step + 1} 动作执行失败: {str(e)}")
                    _emit_progress({
                        "phase": "step_error",
                        "step": step + 1,
                        "max_steps": max_steps,
                        "current_url": page.url,
                        "action": act_type,
                        "target_id": target_id,
                        "status": "running",
                        "error": str(e),
                        "screenshot": _capture_preview_data_url(page),
                    })
                
                if action_record not in report["actions_taken"]:
                    report["actions_taken"].append(action_record)
                time.sleep(1) # 短暂等待页面稳定

            browser.close()
            _emit_log("浏览器会话结束")
    except Exception as e:
        logger.error(f"Exploration failed: {e}")
        report["status"] = "failed"
        report["error_message"] = str(e)
        _emit_log(f"探索任务失败: {str(e)}")

    report["has_critical_errors"] = report.get("error_summary", {}).get("critical", 0) > 0
    _emit_log(f"探索任务完成，状态: {report.get('status')}, 执行步数: {report.get('total_steps_executed')}, 错误数: {len(report.get('errors_found', []))}")
    _emit_progress({
        "phase": "completed",
        "step": report.get("total_steps_executed", 0),
        "max_steps": max_steps,
        "current_url": report.get("visited_urls", [])[-1] if report.get("visited_urls") else start_url,
        "status": report.get("status"),
    })

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
    decision_log_callback: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    import requests

    def _emit_decision_log(message: str) -> None:
        if decision_log_callback:
            try:
                decision_log_callback(message)
            except Exception:
                logger.exception("Failed to emit decision log callback")
        else:
            logger.info(message)
    
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

    def _compact_response_text(text: str, limit: int = 240) -> str:
        compact = str(text or "").replace("\r", " ").replace("\n", " ").strip()
        if len(compact) <= limit:
            return compact
        return compact[:limit] + "..."

    def _parse_action_response(resp: Any, provider: str) -> Dict[str, Any]:
        if resp.status_code != 200:
            _emit_decision_log(f"{provider} 决策接口返回非 200: {resp.status_code}，响应摘要: {_compact_response_text(resp.text)}")
            return {}
        try:
            payload = resp.json()
        except Exception as parse_error:
            _emit_decision_log(f"{provider} 决策响应 JSON 解析失败: {str(parse_error)}，响应摘要: {_compact_response_text(resp.text)}")
            return {}
        content = payload.get("choices", [{}])[0].get("message", {}).get("content", "")
        if isinstance(content, dict):
            _emit_decision_log(f"{provider} 决策成功（dict 内容）")
            return content
        if not isinstance(content, str):
            _emit_decision_log(f"{provider} 决策响应 content 类型异常: {type(content).__name__}")
            return {}
        content_text = content.strip()
        if not content_text:
            _emit_decision_log(f"{provider} 决策响应 content 为空")
            return {}
        try:
            action_obj = json.loads(content_text)
            _emit_decision_log(f"{provider} 决策成功（text JSON）")
            return action_obj
        except Exception as parse_error:
            _emit_decision_log(f"{provider} 决策 content 解析失败: {str(parse_error)}，content 摘要: {_compact_response_text(content_text)}")
            return {}

    def _attach_meta(action: Dict[str, Any], provider: str, latency_ms: int) -> Dict[str, Any]:
        wrapped = dict(action)
        wrapped["_provider"] = provider
        wrapped["_latency_ms"] = latency_ms
        return wrapped

    try:
        _emit_decision_log(f"开始请求视觉模型决策: model={vision_model}, base_url={vision_base_url}")
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
        vision_started_at = time.time()
        vision_resp = requests.post(
            f"{vision_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {vision_api_key}",
                "Content-Type": "application/json",
            },
            json=vision_payload,
            timeout=20,
        )
        vision_latency_ms = int((time.time() - vision_started_at) * 1000)
        vision_action = _parse_action_response(vision_resp, "视觉模型")
        if vision_action:
            return _attach_meta(vision_action, "vision", vision_latency_ms)
        logger.warning(
            "Vision action decision failed with status %s, falling back to text model.",
            vision_resp.status_code,
        )
        _emit_decision_log(f"视觉模型未返回可用动作，耗时 {vision_latency_ms}ms，回退文本模型: model={model}, base_url={base_url}")
    except Exception as e:
        logger.error(f"Vision LLM decision failed: {e}")
        _emit_decision_log(f"视觉模型请求异常，回退文本模型: {str(e)}")

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
        _emit_decision_log(f"开始请求文本模型回退决策: model={model}, base_url={base_url}")
        fallback_started_at = time.time()
        fallback_resp = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=fallback_payload,
            timeout=15,
        )
        fallback_latency_ms = int((time.time() - fallback_started_at) * 1000)
        fallback_action = _parse_action_response(fallback_resp, "文本模型")
        if fallback_action:
            return _attach_meta(fallback_action, "text_fallback", fallback_latency_ms)
        logger.warning("Text fallback decision failed with status %s.", fallback_resp.status_code)
        _emit_decision_log(f"文本模型回退也未返回可用动作，耗时 {fallback_latency_ms}ms，结束探索")
    except Exception as e:
        logger.error(f"Text LLM decision failed: {e}")
        _emit_decision_log(f"文本模型回退请求异常: {str(e)}")
    
    return {
        "action": "stop",
        "reason": "Failed to get LLM decision",
        "_provider": "none",
        "_latency_ms": None
    }
