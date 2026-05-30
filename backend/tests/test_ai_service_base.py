"""
AI 服务基类测试

测试 AIServiceBase 的核心功能：
- chat_completion 基本调用
- AIInvocationLog 自动记录
- 重试机制（exponential backoff）
- 超时处理
- 降级策略
- 错误分类
"""

import os
import pytest
import json
from unittest.mock import patch, MagicMock


class TestAIServiceBaseInit:
    """测试 AIServiceBase 初始化"""

    def test_default_config(self):
        """测试默认配置值"""
        from app.services.ai.base import AIServiceBase

        svc = AIServiceBase(api_key='test-key')
        # base_url 可能被环境变量覆盖，只验证非空
        assert svc.base_url.startswith('http')
        assert svc.api_key == 'test-key'
        # model 可能被环境变量覆盖
        assert svc.model  # 非空
        assert svc.timeout > 0
        assert svc.max_retries == 3

    def test_custom_config(self):
        """测试自定义配置"""
        from app.services.ai.base import AIServiceBase

        svc = AIServiceBase(
            base_url='http://localhost:8080/v1',
            api_key='custom-key',
            model='custom-model',
            timeout=60,
            max_retries=5,
        )
        assert svc.base_url == 'http://localhost:8080/v1'
        assert svc.api_key == 'custom-key'
        assert svc.model == 'custom-model'
        assert svc.timeout == 60
        assert svc.max_retries == 5

    def test_config_dict_fallback(self):
        """测试通过 config dict 传入配置"""
        from app.services.ai.base import AIServiceBase

        config = {
            'AI_ASSISTANT_BASE_URL': 'http://config-url.com/v1',
            'AI_ASSISTANT_API_KEY': 'config-key',
            'AI_ASSISTANT_MODEL': 'config-model',
            'AI_ASSISTANT_TIMEOUT': '45',
        }
        svc = AIServiceBase(config=config)
        assert svc.base_url == 'http://config-url.com/v1'
        assert svc.api_key == 'config-key'
        assert svc.model == 'config-model'
        assert svc.timeout == 45

    def test_base_url_trailing_slash_stripped(self):
        """测试 base_url 末尾斜杠被移除"""
        from app.services.ai.base import AIServiceBase

        svc = AIServiceBase(base_url='http://example.com/v1/', api_key='key')
        assert svc.base_url == 'http://example.com/v1'


class TestChatCompletion:
    """测试 chat_completion 方法"""

    def test_successful_call(self, app):
        """测试成功调用 LLM"""
        from app.services.ai.base import AIServiceBase

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'Hello!'}}],
            'usage': {'prompt_tokens': 10, 'completion_tokens': 5, 'total_tokens': 15},
        }

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', model='gpt-4')
            with patch('app.services.ai.base.requests.post', return_value=mock_response) as mock_post:
                result = svc.chat_completion(
                    [{'role': 'user', 'content': 'hi'}],
                    feature='test_feature',
                )

                assert result['role'] == 'assistant'
                assert result['content'] == 'Hello!'
                mock_post.assert_called_once()

    def test_records_invocation_log_on_success(self, app):
        """测试成功调用时记录 AIInvocationLog"""
        from app.services.ai.base import AIServiceBase
        from app.models.ai_invocation_log import AIInvocationLog
        from app.extensions import db

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'OK'}}],
            'usage': {'prompt_tokens': 20, 'completion_tokens': 10, 'total_tokens': 30},
        }

        with app.app_context():
            # 清理可能的残留数据
            AIInvocationLog.query.filter_by(feature='script_gen').delete()
            db.session.commit()

            svc = AIServiceBase(api_key='test-key', model='gpt-4')
            with patch('app.services.ai.base.requests.post', return_value=mock_response):
                svc.chat_completion(
                    [{'role': 'user', 'content': 'test'}],
                    feature='script_gen',
                    user_id=1,
                )

            log = AIInvocationLog.query.filter_by(feature='script_gen').first()
            assert log is not None
            assert log.success is True
            assert log.model_name == 'gpt-4'
            assert log.prompt_tokens == 20
            assert log.completion_tokens == 10
            assert log.total_tokens == 30
            assert log.user_id == 1
            assert log.latency_ms is not None
            assert log.latency_ms >= 0

    def test_records_invocation_log_on_failure(self, app):
        """测试失败调用时记录 AIInvocationLog"""
        from app.services.ai.base import AIServiceBase
        from app.models.ai_invocation_log import AIInvocationLog
        from app.extensions import db

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'

        with app.app_context():
            # 清理可能的残留数据
            AIInvocationLog.query.filter_by(feature='copilot').delete()
            db.session.commit()

            svc = AIServiceBase(api_key='test-key', max_retries=1)
            with patch('app.services.ai.base.requests.post', return_value=mock_response):
                with patch('app.services.ai.base.time.sleep'):
                    with pytest.raises(RuntimeError):
                        svc.chat_completion(
                            [{'role': 'user', 'content': 'test'}],
                            feature='copilot',
                        )

            log = AIInvocationLog.query.filter_by(feature='copilot').first()
            assert log is not None
            assert log.success is False
            assert log.error_type == 'server_error'
            assert '500' in (log.error_message or '')


class TestRetryMechanism:
    """测试重试机制"""

    def test_retries_on_429(self, app):
        """测试 429 rate limit 时重试"""
        from app.services.ai.base import AIServiceBase

        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429
        rate_limit_response.text = 'Rate limited'

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'OK'}}],
            'usage': {},
        }

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=3)
            with patch('app.services.ai.base.requests.post', side_effect=[rate_limit_response, success_response]) as mock_post:
                with patch('app.services.ai.base.time.sleep') as mock_sleep:
                    result = svc.chat_completion(
                        [{'role': 'user', 'content': 'test'}],
                        feature='test',
                    )

                    assert result['content'] == 'OK'
                    assert mock_post.call_count == 2
                    assert mock_sleep.call_count == 1  # Slept once before retry

    def test_retries_on_500(self, app):
        """测试 500 服务端错误时重试"""
        from app.services.ai.base import AIServiceBase

        error_response = MagicMock()
        error_response.status_code = 500
        error_response.text = 'Server Error'

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'recovered'}}],
            'usage': {},
        }

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=2)
            with patch('app.services.ai.base.requests.post', side_effect=[error_response, success_response]):
                with patch('app.services.ai.base.time.sleep'):
                    result = svc.chat_completion(
                        [{'role': 'user', 'content': 'test'}],
                        feature='test',
                    )
                    assert result['content'] == 'recovered'

    def test_no_retry_on_400(self, app):
        """测试 400 客户端错误不重试"""
        from app.services.ai.base import AIServiceBase

        error_response = MagicMock()
        error_response.status_code = 400
        error_response.text = 'Bad Request'

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=3)
            with patch('app.services.ai.base.requests.post', return_value=error_response) as mock_post:
                with patch('app.services.ai.base.time.sleep') as mock_sleep:
                    # 无 fallback 时抛出 RuntimeError
                    with pytest.raises(RuntimeError):
                        svc.chat_completion(
                            [{'role': 'user', 'content': 'test'}],
                            feature='test',
                        )
                    assert mock_post.call_count == 1
                    mock_sleep.assert_not_called()

    def test_exhausted_retries(self, app):
        """测试重试耗尽后降级"""
        from app.services.ai.base import AIServiceBase

        error_response = MagicMock()
        error_response.status_code = 500
        error_response.text = 'Server Error'

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=2)
            with patch('app.services.ai.base.requests.post', return_value=error_response):
                with patch('app.services.ai.base.time.sleep'):
                    result = svc.chat_completion(
                        [{'role': 'user', 'content': 'test'}],
                        feature='test',
                        fallback_response='Sorry, AI is unavailable.',
                    )
                    assert result['content'] == 'Sorry, AI is unavailable.'


class TestFallbackStrategy:
    """测试降级策略"""

    def test_fallback_on_error(self, app):
        """测试有 fallback_response 时返回降级结果"""
        from app.services.ai.base import AIServiceBase

        error_response = MagicMock()
        error_response.status_code = 500
        error_response.text = 'Error'

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=1)
            with patch('app.services.ai.base.requests.post', return_value=error_response):
                with patch('app.services.ai.base.time.sleep'):
                    result = svc.chat_completion(
                        [{'role': 'user', 'content': 'test'}],
                        feature='test',
                        fallback_response='fallback data',
                    )
                    assert result['content'] == 'fallback data'
                    assert result['role'] == 'assistant'

    def test_no_fallback_raises_exception(self, app):
        """测试无 fallback_response 时抛出异常"""
        from app.services.ai.base import AIServiceBase

        error_response = MagicMock()
        error_response.status_code = 500
        error_response.text = 'Error'

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=1)
            with patch('app.services.ai.base.requests.post', return_value=error_response):
                with patch('app.services.ai.base.time.sleep'):
                    with pytest.raises(RuntimeError):
                        svc.chat_completion(
                            [{'role': 'user', 'content': 'test'}],
                            feature='test',
                        )

    def test_fallback_on_timeout(self, app):
        """测试超时时返回 fallback"""
        from app.services.ai.base import AIServiceBase
        import requests as req_lib

        with app.app_context():
            svc = AIServiceBase(api_key='test-key', max_retries=1, timeout=1)
            with patch('app.services.ai.base.requests.post', side_effect=req_lib.exceptions.Timeout()):
                with patch('app.services.ai.base.time.sleep'):
                    result = svc.chat_completion(
                        [{'role': 'user', 'content': 'test'}],
                        feature='test',
                        fallback_response='timeout fallback',
                    )
                    assert result['content'] == 'timeout fallback'

    def test_fallback_on_no_api_key(self, app):
        """测试无 API Key 时返回 fallback"""
        from app.services.ai.base import AIServiceBase

        with app.app_context():
            with patch.dict(os.environ, {'AI_ASSISTANT_API_KEY': ''}, clear=False):
                svc = AIServiceBase(api_key='')
                result = svc.chat_completion(
                    [{'role': 'user', 'content': 'test'}],
                    feature='test',
                    fallback_response='no key fallback',
                )
                assert result['content'] == 'no key fallback'


class TestSimpleChat:
    """测试 simple_chat 简化接口"""

    def test_simple_chat_injects_system_prompt(self, app):
        """测试自动注入 system prompt"""
        from app.services.ai.base import AIServiceBase

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'Hi!'}}],
            'usage': {},
        }

        with app.app_context():
            svc = AIServiceBase(api_key='test-key')
            with patch('app.services.ai.base.requests.post', return_value=mock_response) as mock_post:
                result = svc.simple_chat(
                    [{'role': 'user', 'content': 'hello'}],
                    feature='test',
                    system_prompt='You are a test assistant.',
                )

                # 验证 system prompt 被注入
                call_args = mock_post.call_args
                messages_sent = call_args[1]['json']['messages']
                assert messages_sent[0]['role'] == 'system'
                assert messages_sent[0]['content'] == 'You are a test assistant.'
                assert messages_sent[1]['role'] == 'user'
                assert messages_sent[1]['content'] == 'hello'

    def test_simple_chat_without_system_prompt(self, app):
        """测试不传 system prompt 时不注入"""
        from app.services.ai.base import AIServiceBase

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'Hi!'}}],
            'usage': {},
        }

        with app.app_context():
            svc = AIServiceBase(api_key='test-key')
            with patch('app.services.ai.base.requests.post', return_value=mock_response) as mock_post:
                svc.simple_chat(
                    [{'role': 'user', 'content': 'hello'}],
                    feature='test',
                )

                call_args = mock_post.call_args
                messages_sent = call_args[1]['json']['messages']
                assert len(messages_sent) == 1
                assert messages_sent[0]['role'] == 'user'


class TestHelperMethods:
    """测试辅助方法"""

    def test_classify_http_error(self):
        """测试 HTTP 错误分类"""
        from app.services.ai.base import AIServiceBase

        assert AIServiceBase._classify_http_error(401) == 'auth_error'
        assert AIServiceBase._classify_http_error(403) == 'auth_error'
        assert AIServiceBase._classify_http_error(429) == 'rate_limit'
        assert AIServiceBase._classify_http_error(500) == 'server_error'
        assert AIServiceBase._classify_http_error(503) == 'server_error'
        assert AIServiceBase._classify_http_error(400) == 'unknown'

    def test_estimate_cost(self):
        """测试成本估算"""
        from app.services.ai.base import AIServiceBase

        # 1000 input tokens + 500 output tokens
        cost = AIServiceBase._estimate_cost(1000, 500)
        # 1000 * 0.15/1M + 500 * 0.60/1M = 0.00015 + 0.0003 = 0.00045
        assert abs(cost - 0.00045) < 1e-8

    def test_calc_retry_delay(self):
        """测试重试延迟计算"""
        from app.services.ai.base import AIServiceBase

        # 尝试多次取平均值（因为有随机抖动）
        delays = [AIServiceBase._calc_retry_delay(1) for _ in range(100)]
        avg_delay_1 = sum(delays) / len(delays)
        assert 0.5 <= avg_delay_1 <= 2.5  # base=1, jitter up to 0.5

        delays = [AIServiceBase._calc_retry_delay(2) for _ in range(100)]
        avg_delay_2 = sum(delays) / len(delays)
        assert avg_delay_2 > avg_delay_1  # 指数退避

    def test_messages_to_prompt_text(self):
        """测试消息转文本"""
        from app.services.ai.base import AIServiceBase

        messages = [
            {'role': 'system', 'content': 'You are helpful.'},
            {'role': 'user', 'content': 'Hello!'},
        ]
        text = AIServiceBase._messages_to_prompt_text(messages)
        assert '[system]' in text
        assert '[user]' in text
        assert 'You are helpful.' in text
        assert 'Hello!' in text

    def test_get_content(self, app):
        """测试 get_content 辅助方法"""
        from app.services.ai.base import AIServiceBase

        svc = AIServiceBase(api_key='test')
        assert svc.get_content({'role': 'assistant', 'content': 'hello'}) == 'hello'
        assert svc.get_content({'role': 'assistant', 'content': ''}) == ''
        assert svc.get_content({'role': 'assistant'}) == ''


class TestAIServiceSubclass:
    """测试子类继承"""

    def test_subclass_inherits_chat(self, app):
        """测试子类可以继承并使用 chat_completion"""
        from app.services.ai.base import AIServiceBase

        class TestService(AIServiceBase):
            def do_chat(self, user_input):
                return self.simple_chat(
                    [{'role': 'user', 'content': user_input}],
                    feature='test_subclass',
                    system_prompt='You are a test.',
                )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'role': 'assistant', 'content': 'subclassed!'}}],
            'usage': {},
        }

        with app.app_context():
            svc = TestService(api_key='test-key')
            with patch('app.services.ai.base.requests.post', return_value=mock_response):
                result = svc.do_chat('hello')
                assert result['content'] == 'subclassed!'
