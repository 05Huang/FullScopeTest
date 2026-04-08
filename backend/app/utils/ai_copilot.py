"""
Global AI Copilot using Function Calling to interact with the platform.
"""

import json
import logging
import os
import requests
from typing import Dict, Any, List
from ..extensions import db
from ..models.perf_test_scenario import PerfTestScenario
from ..models.web_test_script import WebTestScript

logger = logging.getLogger(__name__)

# 定义可供大模型调用的工具库
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_performance_test",
            "description": "Create a new performance test scenario. Use this when the user asks to create a performance test or load test.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the test scenario"
                    },
                    "target_url": {
                        "type": "string",
                        "description": "The URL to test. Default to 'http://example.com' if not provided."
                    },
                    "concurrent_users": {
                        "type": "integer",
                        "description": "Number of concurrent users (VUs)"
                    },
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Duration of the test in seconds (convert minutes to seconds if needed)"
                    }
                },
                "required": ["name", "concurrent_users", "duration_seconds"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_failed_web_tests",
            "description": "Query recent failed web UI test scripts. Use this when the user asks about failed web tests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of failed tests to return. Default is 5."
                    }
                }
            }
        }
    }
]

def execute_tool_call(tool_call: Dict[str, Any], user_id: int) -> str:
    """执行大模型请求调用的本地函数"""
    function_name = tool_call.get("function", {}).get("name")
    try:
        arguments = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
    except json.JSONDecodeError:
        arguments = {}

    logger.info(f"Copilot executing tool: {function_name} with args {arguments}")

    if function_name == "create_performance_test":
        try:
            name = arguments.get("name")
            target_url = arguments.get("target_url", "http://example.com")
            vus = arguments.get("concurrent_users", 10)
            duration = arguments.get("duration_seconds", 60)

            # 生成一个基础的 locust 脚本
            script_content = f"""from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_target(self):
        self.client.get("/")
"""
            test = PerfTestScenario(
                name=name,
                description=f"Copilot created: {vus} VUs for {duration}s",
                target_url=target_url,
                user_count=vus,
                duration=duration,
                script_content=script_content,
                status="pending",
                user_id=user_id
            )
            db.session.add(test)
            db.session.commit()
            return json.dumps({
                "status": "success", 
                "message": f"成功创建了名为 '{name}' 的性能测试场景 (并发: {vus}, 时长: {duration}秒)。你可以在性能测试模块查看它。"
            }, ensure_ascii=False)
        except Exception as e:
            db.session.rollback()
            return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)

    elif function_name == "query_failed_web_tests":
        limit = arguments.get("limit", 5)
        failed_tests = WebTestScript.query.filter_by(status='failed').order_by(WebTestScript.updated_at.desc()).limit(limit).all()
        
        if not failed_tests:
            return json.dumps({"status": "success", "message": "太棒了！最近没有任何失败的 Web 测试。"}, ensure_ascii=False)
            
        results = [{"id": t.id, "name": t.name, "time": str(t.updated_at)} for t in failed_tests]
        return json.dumps({"status": "success", "data": results}, ensure_ascii=False)

    return json.dumps({"status": "error", "message": f"Unknown tool {function_name}"})


def process_copilot_chat(
    messages: List[Dict[str, str]],
    user_id: int,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    处理全局 Copilot 的对话逻辑，支持 Function Calling。
    """
    base_url = str(os.environ.get("AI_ASSISTANT_BASE_URL") or config.get("AI_ASSISTANT_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    model = str(os.environ.get("AI_ASSISTANT_MODEL") or config.get("AI_ASSISTANT_MODEL") or "gpt-4o-mini")
    api_key = str(os.environ.get("AI_ASSISTANT_API_KEY") or config.get("AI_ASSISTANT_API_KEY") or "").strip()

    if not api_key:
        raise ValueError("AI_ASSISTANT_API_KEY is not configured")

    endpoint = f"{base_url}/chat/completions"

    system_message = {
        "role": "system", 
        "content": "You are a helpful AI Copilot for a Software Testing Platform. "
                   "You can help users create performance tests, query failed test results, and answer general testing questions. "
                   "Always use the provided tools if the user's request matches their capabilities. "
                   "Respond in Chinese."
    }
    
    # 确保系统提示词在最前面
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, system_message)

    payload = {
        "model": model,
        "temperature": 0.3,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto"
    }

    resp = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30
    )
    
    if resp.status_code >= 400:
        raise RuntimeError(f"LLM request failed: {resp.text}")

    data = resp.json()
    response_message = data["choices"][0]["message"]

    # 检查大模型是否决定调用工具
    if response_message.get("tool_calls"):
        messages.append(response_message)  # 把助手的回复加入历史
        
        # 执行所有请求的工具
        for tool_call in response_message["tool_calls"]:
            function_response = execute_tool_call(tool_call, user_id)
            
            # 把工具执行结果附加到消息列表中发回给大模型
            messages.append({
                "tool_call_id": tool_call["id"],
                "role": "tool",
                "name": tool_call["function"]["name"],
                "content": function_response,
            })
            
        # 第二次请求，让模型根据工具返回的数据生成自然语言回复
        second_payload = {
            "model": model,
            "messages": messages,
        }
        
        second_resp = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=second_payload,
            timeout=30
        )
        
        if second_resp.status_code >= 400:
            raise RuntimeError(f"LLM second request failed: {second_resp.text}")
            
        final_message = second_resp.json()["choices"][0]["message"]
        return {"role": "assistant", "content": final_message.get("content", "")}

    # 如果不需要调用工具，直接返回文本回复
    return {"role": "assistant", "content": response_message.get("content", "")}
