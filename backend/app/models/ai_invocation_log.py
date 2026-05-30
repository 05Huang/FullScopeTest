"""
AI 调用日志模型

存储每次 AI 调用的完整可观测性数据：
prompt、response、延迟、成功/失败、token 用量、成本估算
"""

from datetime import datetime
from ..extensions import db


class AIInvocationLog(db.Model):
    """AI 调用日志表 - 记录每次 LLM 调用的详细信息"""

    __tablename__ = 'ai_invocation_logs'
    __table_args__ = (
        db.Index('idx_ai_invocation_user_id', 'user_id'),
        db.Index('idx_ai_invocation_feature', 'feature'),
        db.Index('idx_ai_invocation_success', 'success'),
        db.Index('idx_ai_invocation_created_at', 'created_at'),
        db.Index('idx_ai_invocation_prompt_version_id', 'prompt_version_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, comment='调用用户 ID')

    # 功能标识
    feature = db.Column(db.String(50), nullable=False, comment='功能模块: copilot/script_gen/swagger_gen/dedup/其他')

    # Prompt 版本（可选关联）
    prompt_version_id = db.Column(db.Integer, db.ForeignKey('prompt_versions.id'), nullable=True, comment='关联的 Prompt 版本 ID')

    # 输入
    prompt = db.Column(db.Text, nullable=False, comment='发送给 LLM 的完整 prompt 内容')
    model_name = db.Column(db.String(100), nullable=False, comment='使用的模型名称')
    temperature = db.Column(db.Float, comment='temperature 参数')

    # 输出
    response = db.Column(db.Text, comment='LLM 返回的完整响应内容')

    # 调用结果
    success = db.Column(db.Boolean, nullable=False, default=True, comment='调用是否成功')
    error_message = db.Column(db.Text, comment='失败时的错误信息')
    error_type = db.Column(db.String(50), comment='错误类型: timeout/rate_limit/auth_error/server_error/unknown')

    # 性能指标
    latency_ms = db.Column(db.Integer, comment='总延迟（毫秒）')
    first_token_latency_ms = db.Column(db.Integer, comment='首 token 延迟（毫秒）')

    # Token 用量
    prompt_tokens = db.Column(db.Integer, default=0, comment='输入 token 数')
    completion_tokens = db.Column(db.Integer, default=0, comment='输出 token 数')
    total_tokens = db.Column(db.Integer, default=0, comment='总 token 数')

    # 成本估算
    cost_estimate = db.Column(db.Float, default=0.0, comment='估算的调用成本（美元）')

    # 元数据
    metadata_json = db.Column(db.JSON, comment='额外元数据（如 tool_calls 结果、function_call 参数等）')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='调用时间')

    # 关联关系
    user = db.relationship('User', backref='ai_invocation_logs')
    prompt_version = db.relationship('PromptVersion', backref='invocation_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'feature': self.feature,
            'prompt_version_id': self.prompt_version_id,
            'prompt': self.prompt[:500] if self.prompt else None,  # 截断展示
            'model_name': self.model_name,
            'temperature': self.temperature,
            'response': self.response[:500] if self.response else None,  # 截断展示
            'success': self.success,
            'error_message': self.error_message,
            'error_type': self.error_type,
            'latency_ms': self.latency_ms,
            'first_token_latency_ms': self.first_token_latency_ms,
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
            'total_tokens': self.total_tokens,
            'cost_estimate': self.cost_estimate,
            'metadata_json': self.metadata_json,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def to_dict_full(self):
        """返回完整数据（不截断 prompt/response），用于详情查看"""
        d = self.to_dict()
        d['prompt'] = self.prompt
        d['response'] = self.response
        return d

    def __repr__(self):
        return f'<AIInvocationLog feature={self.feature} success={self.success} latency={self.latency_ms}ms>'
