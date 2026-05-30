"""
AI 可观测性模型测试

测试 AIInvocationLog 和 PromptVersion 模型的创建、关联和序列化
"""

import pytest
from datetime import datetime


class TestPromptVersionModel:
    """PromptVersion 模型测试"""

    def test_create_prompt_version(self, app):
        """测试创建 PromptVersion 记录"""
        from app.extensions import db
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            pv = PromptVersion(
                feature='copilot',
                name='baseline',
                version=1,
                is_active=True,
                system_prompt='You are a helpful AI assistant.',
                user_prompt_template='Help me with: {task}',
                temperature=0.3,
                model_name='gpt-4o-mini',
            )
            db.session.add(pv)
            db.session.commit()

            assert pv.id is not None
            assert pv.feature == 'copilot'
            assert pv.name == 'baseline'
            assert pv.version == 1
            assert pv.is_active is True
            assert pv.system_prompt == 'You are a helpful AI assistant.'
            assert pv.total_invocations == 0
            assert pv.success_count == 0
            assert pv.failure_count == 0

    def test_prompt_version_to_dict(self, app):
        """测试 PromptVersion.to_dict 序列化"""
        from app.extensions import db
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            pv = PromptVersion(
                feature='script_gen',
                name='v2-improved',
                version=2,
                is_active=True,
                system_prompt='You are an expert.',
                total_invocations=100,
                success_count=95,
                failure_count=5,
                avg_latency_ms=1500.0,
                avg_tokens=800.0,
                avg_cost=0.005,
            )
            db.session.add(pv)
            db.session.commit()

            d = pv.to_dict()
            assert d['feature'] == 'script_gen'
            assert d['name'] == 'v2-improved'
            assert d['version'] == 2
            assert d['total_invocations'] == 100
            assert d['success_count'] == 95
            assert d['success_rate'] == 95.0
            assert d['avg_latency_ms'] == 1500.0
            assert d['created_at'] is not None

    def test_prompt_version_success_rate_zero_invocations(self, app):
        """测试无调用时成功率计算为 0"""
        from app.extensions import db
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            pv = PromptVersion(
                feature='dedup',
                name='initial',
                version=1,
                system_prompt='Test prompt',
            )
            db.session.add(pv)
            db.session.commit()

            d = pv.to_dict()
            assert d['success_rate'] == 0.0

    def test_prompt_version_repr(self, app):
        """测试 PromptVersion __repr__"""
        from app.extensions import db
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            pv = PromptVersion(
                feature='copilot',
                name='v1',
                version=1,
                system_prompt='Test',
            )
            db.session.add(pv)
            db.session.commit()

            assert 'copilot' in repr(pv)
            assert 'v1' in repr(pv)

    def test_prompt_version_default_values(self, app):
        """测试 PromptVersion 默认值"""
        from app.extensions import db
        from app.models.prompt_version import PromptVersion

        with app.app_context():
            pv = PromptVersion(
                feature='swagger_gen',
                name='baseline',
                version=1,
                system_prompt='Test',
            )
            db.session.add(pv)
            db.session.commit()

            assert pv.is_active is False
            assert pv.temperature == 0.3
            assert pv.traffic_weight == 1.0
            assert pv.total_invocations == 0


class TestAIInvocationLogModel:
    """AIInvocationLog 模型测试"""

    def test_create_invocation_log(self, app):
        """测试创建 AIInvocationLog 记录"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            log = AIInvocationLog(
                user_id=1,
                feature='copilot',
                prompt='Hello, help me create a test',
                model_name='gpt-4o-mini',
                temperature=0.3,
                response='Sure! Here is a test script...',
                success=True,
                latency_ms=2500,
                first_token_latency_ms=800,
                prompt_tokens=50,
                completion_tokens=120,
                total_tokens=170,
                cost_estimate=0.0003,
            )
            db.session.add(log)
            db.session.commit()

            assert log.id is not None
            assert log.feature == 'copilot'
            assert log.success is True
            assert log.latency_ms == 2500
            assert log.total_tokens == 170

    def test_invocation_log_to_dict_truncates(self, app):
        """测试 to_dict 截断 prompt 和 response"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            long_prompt = 'x' * 1000
            long_response = 'y' * 1000

            log = AIInvocationLog(
                feature='script_gen',
                prompt=long_prompt,
                model_name='gpt-4',
                response=long_response,
                success=True,
                latency_ms=3000,
            )
            db.session.add(log)
            db.session.commit()

            d = log.to_dict()
            assert len(d['prompt']) <= 500
            assert len(d['response']) <= 500

    def test_invocation_log_to_dict_full(self, app):
        """测试 to_dict_full 返回完整数据"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            long_prompt = 'z' * 1000
            long_response = 'w' * 1000

            log = AIInvocationLog(
                feature='copilot',
                prompt=long_prompt,
                model_name='gpt-4',
                response=long_response,
                success=True,
                latency_ms=1500,
            )
            db.session.add(log)
            db.session.commit()

            d = log.to_dict_full()
            assert len(d['prompt']) == 1000
            assert len(d['response']) == 1000

    def test_invocation_log_failure(self, app):
        """测试失败调用记录"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            log = AIInvocationLog(
                feature='copilot',
                prompt='test prompt',
                model_name='gpt-4',
                success=False,
                error_message='Rate limit exceeded',
                error_type='rate_limit',
                latency_ms=500,
            )
            db.session.add(log)
            db.session.commit()

            d = log.to_dict()
            assert d['success'] is False
            assert d['error_message'] == 'Rate limit exceeded'
            assert d['error_type'] == 'rate_limit'

    def test_invocation_log_default_values(self, app):
        """测试默认值"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            log = AIInvocationLog(
                feature='dedup',
                prompt='test',
                model_name='gpt-4o-mini',
                success=True,
            )
            db.session.add(log)
            db.session.commit()

            assert log.prompt_tokens == 0
            assert log.completion_tokens == 0
            assert log.total_tokens == 0
            assert log.cost_estimate == 0.0

    def test_invocation_log_repr(self, app):
        """测试 __repr__"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            log = AIInvocationLog(
                feature='swagger_gen',
                prompt='test',
                model_name='gpt-4',
                success=True,
                latency_ms=1200,
            )
            db.session.add(log)
            db.session.commit()

            r = repr(log)
            assert 'swagger_gen' in r
            assert '1200' in r


class TestModelRelationships:
    """模型关联关系测试"""

    def test_prompt_version_invocation_logs_relationship(self, app):
        """测试 PromptVersion 与 AIInvocationLog 的一对多关系"""
        from app.extensions import db
        from app.models.prompt_version import PromptVersion
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            pv = PromptVersion(
                feature='copilot',
                name='v1',
                version=1,
                system_prompt='Test',
            )
            db.session.add(pv)
            db.session.flush()

            log1 = AIInvocationLog(
                prompt_version_id=pv.id,
                feature='copilot',
                prompt='test 1',
                model_name='gpt-4',
                success=True,
            )
            log2 = AIInvocationLog(
                prompt_version_id=pv.id,
                feature='copilot',
                prompt='test 2',
                model_name='gpt-4',
                success=True,
            )
            db.session.add_all([log1, log2])
            db.session.commit()

            assert len(pv.invocation_logs) == 2
            assert pv.invocation_logs[0].prompt_version_id == pv.id

    def test_invocation_log_with_metadata(self, app):
        """测试 metadata_json 字段存储"""
        from app.extensions import db
        from app.models.ai_invocation_log import AIInvocationLog

        with app.app_context():
            meta = {
                'tool_calls': [{'function': 'create_test'}],
                'conversation_id': 'abc-123',
            }
            log = AIInvocationLog(
                feature='copilot',
                prompt='test',
                model_name='gpt-4',
                success=True,
                metadata_json=meta,
            )
            db.session.add(log)
            db.session.commit()

            d = log.to_dict()
            assert d['metadata_json']['tool_calls'][0]['function'] == 'create_test'
            assert d['metadata_json']['conversation_id'] == 'abc-123'
