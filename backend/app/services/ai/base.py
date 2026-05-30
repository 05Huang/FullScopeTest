"""
AI 服务基类

提供统一的 LLM 调用接口，具备以下能力：
- 自动记录 AIInvocationLog（prompt、response、latency、tokens、cost）
- Retry with exponential backoff
- 超时处理
- 降级策略（AI 失败时返回 fallback 结果而不是 500）
- 支持 OpenAI 兼容的 chat/completions API（OpenAI、Azure、本地模型等）
"""

import os
import time
import random
import requests
from typing import Dict, Any, Optional, List

from ...extensions import db
from ...models.ai_invocation_log import AIInvocationLog
from ...core.logging import get_logger

logger = get_logger(__name__)


class AIServiceBase:
    """
    AI 服务基类 —— 所有 AI 功能（copilot、script_gen、swagger_gen、dedup）的统一入口。

    子类只需调用 self.chat_completion() 或 self.simple_chat() 即可获得完整的
    调用日志记录、重试、超时、降级能力。

    Usage::

        class CopilotService(AIServiceBase):
            def chat(self, messages, **kwargs):
                return self.simple_chat(messages, feature='copilot', **kwargs)

        svc = CopilotService()
        result = svc.chat([{"role": "user", "content": "hello"}], user_id=1)
    """

    # ---- 默认配置（可通过构造函数或子类覆盖） ----

    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_BASE_DELAY = 1.0   # 首次重试延迟（秒）
    DEFAULT_RETRY_MAX_DELAY = 16.0   # 最大重试延迟（秒）
    DEFAULT_TIMEOUT = 30             # 请求超时（秒）

    # ---- 构造函数 ----

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化 AI 服务。

        参数优先级：显式传入 > config dict > 环境变量 > 默认值。

        Args:
            base_url: LLM API 基础 URL（如 https://api.openai.com/v1）
            api_key: API 密钥
            model: 模型名称
            timeout: 请求超时（秒）
            max_retries: 最大重试次数
            config: 可选的配置字典（如 Flask app.config）
        """
        cfg = config or {}

        self.base_url = (
            base_url
            or cfg.get('AI_ASSISTANT_BASE_URL')
            or os.environ.get('AI_ASSISTANT_BASE_URL')
            or 'https://api.openai.com/v1'
        ).rstrip('/')

        self.api_key = (
            api_key
            or cfg.get('AI_ASSISTANT_API_KEY')
            or os.environ.get('AI_ASSISTANT_API_KEY')
            or ''
        ).strip()

        self.model = (
            model
            or cfg.get('AI_ASSISTANT_MODEL')
            or os.environ.get('AI_ASSISTANT_MODEL')
            or 'gpt-4o-mini'
        )

        self.timeout = timeout or int(
            cfg.get('AI_ASSISTANT_TIMEOUT')
            or os.environ.get('AI_ASSISTANT_TIMEOUT')
            or self.DEFAULT_TIMEOUT
        )

        self.max_retries = max_retries or self.DEFAULT_MAX_RETRIES

    # ---- 公开接口 ----

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        *,
        feature: str = 'general',
        user_id: Optional[int] = None,
        prompt_version_id: Optional[int] = None,
        temperature: float = 0.3,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = 'auto',
        fallback_response: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        调用 LLM chat/completions 接口，自动记录日志、支持重试和降级。

        Args:
            messages: OpenAI 格式的消息列表 [{"role": "user", "content": "..."}]
            feature: 功能标识（copilot / script_gen / swagger_gen / dedup）
            user_id: 调用用户 ID
            prompt_version_id: 关联的 Prompt 版本 ID
            temperature: 温度参数
            tools: 可选的 function calling 工具定义
            tool_choice: 工具选择策略
            fallback_response: 降级响应（AI 失败时返回此内容而非抛异常）
            extra_metadata: 额外的元数据（会存入 metadata_json）

        Returns:
            dict: OpenAI 格式的响应 {"role": "assistant", "content": "...", ...}
        """
        if not self.api_key:
            return self._handle_no_api_key(feature, user_id, fallback_response)

        # 构造完整的 prompt 文本（用于日志记录）
        prompt_text = self._messages_to_prompt_text(messages)

        endpoint = f"{self.base_url}/chat/completions"
        payload: Dict[str, Any] = {
            'model': self.model,
            'temperature': temperature,
            'messages': messages,
        }
        if tools:
            payload['tools'] = tools
            payload['tool_choice'] = tool_choice

        # 重试循环
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            start_time = time.monotonic()
            try:
                resp = requests.post(
                    endpoint,
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json',
                    },
                    json=payload,
                    timeout=self.timeout,
                )
                latency_ms = int((time.monotonic() - start_time) * 1000)

                # HTTP 错误
                if resp.status_code >= 400:
                    error_type = self._classify_http_error(resp.status_code)
                    # 对 429 (rate limit) 和 5xx 进行重试
                    if error_type in ('rate_limit', 'server_error') and attempt < self.max_retries:
                        delay = self._calc_retry_delay(attempt)
                        logger.warning(
                            'AI call failed, retrying',
                            attempt=attempt,
                            max_retries=self.max_retries,
                            status_code=resp.status_code,
                            delay=delay,
                        )
                        time.sleep(delay)
                        continue

                    error_msg = f'LLM request failed: HTTP {resp.status_code} {resp.text[:500]}'
                    self._record_log(
                        feature=feature,
                        user_id=user_id,
                        prompt_version_id=prompt_version_id,
                        prompt=prompt_text,
                        response=None,
                        success=False,
                        error_message=error_msg,
                        error_type=error_type,
                        latency_ms=latency_ms,
                        temperature=temperature,
                        extra_metadata=extra_metadata,
                    )
                    try:
                        return self._apply_fallback(fallback_response, error_msg)
                    except RuntimeError:
                        raise

                # 解析响应
                data = resp.json()
                choices = data.get('choices') or []
                if not choices:
                    error_msg = 'LLM response is empty (no choices)'
                    self._record_log(
                        feature=feature,
                        user_id=user_id,
                        prompt_version_id=prompt_version_id,
                        prompt=prompt_text,
                        response=str(data)[:500],
                        success=False,
                        error_message=error_msg,
                        error_type='unknown',
                        latency_ms=latency_ms,
                        temperature=temperature,
                        extra_metadata=extra_metadata,
                    )
                    try:
                        return self._apply_fallback(fallback_response, error_msg)
                    except RuntimeError:
                        raise

                response_message = choices[0].get('message', {})
                content = response_message.get('content', '') or ''

                # 提取 token 用量
                usage = data.get('usage', {})
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
                total_tokens = usage.get('total_tokens', 0)
                cost = self._estimate_cost(prompt_tokens, completion_tokens)

                self._record_log(
                    feature=feature,
                    user_id=user_id,
                    prompt_version_id=prompt_version_id,
                    prompt=prompt_text,
                    response=content[:5000] if content else None,
                    success=True,
                    latency_ms=latency_ms,
                    temperature=temperature,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    cost_estimate=cost,
                    extra_metadata=extra_metadata,
                )

                return response_message

            except requests.exceptions.Timeout:
                latency_ms = int((time.monotonic() - start_time) * 1000)
                last_error = Exception(f'LLM request timed out after {self.timeout}s')
                if attempt < self.max_retries:
                    delay = self._calc_retry_delay(attempt)
                    logger.warning(
                        'AI call timed out, retrying',
                        attempt=attempt,
                        delay=delay,
                    )
                    time.sleep(delay)
                    continue

                self._record_log(
                    feature=feature,
                    user_id=user_id,
                    prompt_version_id=prompt_version_id,
                    prompt=prompt_text,
                    response=None,
                    success=False,
                    error_message=str(last_error),
                    error_type='timeout',
                    latency_ms=latency_ms,
                    temperature=temperature,
                    extra_metadata=extra_metadata,
                )
                return self._apply_fallback(fallback_response, str(last_error))

            except requests.exceptions.ConnectionError as exc:
                latency_ms = int((time.monotonic() - start_time) * 1000)
                last_error = exc
                if attempt < self.max_retries:
                    delay = self._calc_retry_delay(attempt)
                    logger.warning(
                        'AI call connection error, retrying',
                        attempt=attempt,
                        delay=delay,
                    )
                    time.sleep(delay)
                    continue

                error_msg = f'Connection error: {exc}'
                self._record_log(
                    feature=feature,
                    user_id=user_id,
                    prompt_version_id=prompt_version_id,
                    prompt=prompt_text,
                    response=None,
                    success=False,
                    error_message=error_msg,
                    error_type='server_error',
                    latency_ms=latency_ms,
                    temperature=temperature,
                    extra_metadata=extra_metadata,
                )
                return self._apply_fallback(fallback_response, error_msg)

            except (RuntimeError, ValueError):
                # _apply_fallback 已经处理过（记录日志 + 返回 fallback 或 raise）
                raise
            except Exception as exc:
                latency_ms = int((time.monotonic() - start_time) * 1000)
                error_msg = f'Unexpected error: {exc}'
                logger.error('AI call unexpected error', error=error_msg)
                self._record_log(
                    feature=feature,
                    user_id=user_id,
                    prompt_version_id=prompt_version_id,
                    prompt=prompt_text,
                    response=None,
                    success=False,
                    error_message=error_msg,
                    error_type='unknown',
                    latency_ms=latency_ms,
                    temperature=temperature,
                    extra_metadata=extra_metadata,
                )
                return self._apply_fallback(fallback_response, error_msg)

        # 理论上不会到这里，但作为安全网
        error_msg = f'All {self.max_retries} retries exhausted. Last error: {last_error}'
        self._record_log(
            feature=feature,
            user_id=user_id,
            prompt_version_id=prompt_version_id,
            prompt=prompt_text,
            response=None,
            success=False,
            error_message=error_msg,
            error_type='unknown',
            latency_ms=0,
            temperature=temperature,
            extra_metadata=extra_metadata,
        )
        return self._apply_fallback(fallback_response, error_msg)

    def simple_chat(
        self,
        messages: List[Dict[str, str]],
        *,
        feature: str = 'general',
        user_id: Optional[int] = None,
        prompt_version_id: Optional[int] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        fallback_response: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        简化版聊天接口 —— 自动注入 system prompt，返回 assistant content。

        Args:
            messages: 用户消息列表（不需要包含 system prompt）
            feature: 功能标识
            user_id: 用户 ID
            prompt_version_id: Prompt 版本 ID
            system_prompt: 系统提示词（可选，会自动插入消息列表首位）
            temperature: 温度
            fallback_response: 降级响应

        Returns:
            dict: {"role": "assistant", "content": "..."}
        """
        full_messages = list(messages)
        if system_prompt:
            full_messages.insert(0, {'role': 'system', 'content': system_prompt})

        return self.chat_completion(
            full_messages,
            feature=feature,
            user_id=user_id,
            prompt_version_id=prompt_version_id,
            temperature=temperature,
            fallback_response=fallback_response,
        )

    def get_content(self, response: Dict[str, Any]) -> str:
        """从 chat_completion 响应中提取纯文本内容"""
        return response.get('content', '') or ''

    # ---- 内部方法 ----

    def _record_log(
        self,
        *,
        feature: str,
        user_id: Optional[int],
        prompt_version_id: Optional[int],
        prompt: str,
        response: Optional[str],
        success: bool,
        latency_ms: int,
        temperature: float,
        error_message: Optional[str] = None,
        error_type: Optional[str] = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        cost_estimate: float = 0.0,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ):
        """将调用信息写入 AIInvocationLog"""
        try:
            log = AIInvocationLog(
                user_id=user_id,
                feature=feature,
                prompt_version_id=prompt_version_id,
                prompt=prompt[:10000] if prompt else '',  # 防止超大 prompt
                model_name=self.model,
                temperature=temperature,
                response=response[:5000] if response else None,
                success=success,
                error_message=error_message[:2000] if error_message else None,
                error_type=error_type,
                latency_ms=latency_ms,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost_estimate=cost_estimate,
                metadata_json=extra_metadata,
            )
            db.session.add(log)
            db.session.commit()
            logger.info(
                'AI invocation logged',
                feature=feature,
                success=success,
                latency_ms=latency_ms,
                total_tokens=total_tokens,
            )
        except Exception as exc:
            # 日志记录失败不应影响主流程
            db.session.rollback()
            logger.error('Failed to record AI invocation log', error=str(exc))

    def _apply_fallback(
        self,
        fallback_response: Optional[str],
        error_msg: str,
    ) -> Dict[str, Any]:
        """降级策略：返回 fallback 结果或抛出异常"""
        if fallback_response is not None:
            logger.warning(
                'AI call using fallback response',
                error=error_msg,
            )
            return {'role': 'assistant', 'content': fallback_response}
        raise RuntimeError(error_msg)

    def _handle_no_api_key(
        self,
        feature: str,
        user_id: Optional[int],
        fallback_response: Optional[str],
    ) -> Dict[str, Any]:
        """处理未配置 API Key 的情况"""
        error_msg = 'AI_ASSISTANT_API_KEY is not configured'
        self._record_log(
            feature=feature,
            user_id=user_id,
            prompt_version_id=None,
            prompt='',
            response=None,
            success=False,
            error_message=error_msg,
            error_type='auth_error',
            latency_ms=0,
            temperature=0.0,
        )
        return self._apply_fallback(fallback_response, error_msg)

    @staticmethod
    def _messages_to_prompt_text(messages: List[Dict[str, str]]) -> str:
        """将 messages 列表转为可记录的文本"""
        parts = []
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            parts.append(f'[{role}] {content}')
        return '\n'.join(parts)[:10000]

    @staticmethod
    def _calc_retry_delay(attempt: int, base: float = 1.0, max_delay: float = 16.0) -> float:
        """指数退避 + 随机抖动"""
        delay = min(base * (2 ** (attempt - 1)), max_delay)
        jitter = random.uniform(0, delay * 0.5)
        return delay + jitter

    @staticmethod
    def _classify_http_error(status_code: int) -> str:
        """分类 HTTP 错误类型"""
        if status_code == 401 or status_code == 403:
            return 'auth_error'
        if status_code == 429:
            return 'rate_limit'
        if status_code >= 500:
            return 'server_error'
        return 'unknown'

    @staticmethod
    def _estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
        """
        简单成本估算（基于 GPT-4o-mini 定价）。
        实际项目中可根据 model_name 使用不同的定价表。
        """
        # GPT-4o-mini: $0.15/1M input, $0.60/1M output
        input_cost = prompt_tokens * 0.15 / 1_000_000
        output_cost = completion_tokens * 0.60 / 1_000_000
        return round(input_cost + output_cost, 8)
