"""add AI invocation log and prompt version models

Revision ID: e1f2a3b4c5d6
Revises: d4e5f6a7b8c9
Create Date: 2026-05-30

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1f2a3b4c5d6'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 Prompt 版本表（先创建，因为 AIInvocationLog 依赖它）
    op.create_table('prompt_versions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feature', sa.String(length=50), nullable=False, comment='功能模块: copilot/script_gen/swagger_gen/dedup/其他'),
    sa.Column('name', sa.String(length=255), nullable=False, comment='版本名称/标签'),
    sa.Column('version', sa.Integer(), nullable=False, comment='版本号'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='是否为当前激活版本'),
    sa.Column('system_prompt', sa.Text(), nullable=False, comment='系统提示词内容'),
    sa.Column('user_prompt_template', sa.Text(), nullable=True, comment='用户提示词模板'),
    sa.Column('temperature', sa.Float(), nullable=True, comment='默认 temperature 参数'),
    sa.Column('model_name', sa.String(length=100), nullable=True, comment='指定使用的模型'),
    sa.Column('total_invocations', sa.Integer(), nullable=True, comment='总调用次数'),
    sa.Column('success_count', sa.Integer(), nullable=True, comment='成功调用次数'),
    sa.Column('failure_count', sa.Integer(), nullable=True, comment='失败调用次数'),
    sa.Column('avg_latency_ms', sa.Float(), nullable=True, comment='平均延迟'),
    sa.Column('avg_tokens', sa.Float(), nullable=True, comment='平均 token 用量'),
    sa.Column('avg_cost', sa.Float(), nullable=True, comment='平均调用成本'),
    sa.Column('traffic_weight', sa.Float(), nullable=True, comment='流量权重'),
    sa.Column('change_notes', sa.Text(), nullable=True, comment='变更说明'),
    sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True, comment='创建者用户 ID'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.Column('deactivated_at', sa.DateTime(), nullable=True, comment='停用时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_prompt_versions_feature', 'prompt_versions', ['feature'], unique=False)
    op.create_index('idx_prompt_versions_is_active', 'prompt_versions', ['is_active'], unique=False)
    op.create_index('idx_prompt_versions_version', 'prompt_versions', ['version'], unique=False)

    # 创建 AI 调用日志表
    op.create_table('ai_invocation_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True, comment='调用用户 ID'),
    sa.Column('feature', sa.String(length=50), nullable=False, comment='功能模块'),
    sa.Column('prompt_version_id', sa.Integer(), sa.ForeignKey('prompt_versions.id'), nullable=True, comment='关联的 Prompt 版本 ID'),
    sa.Column('prompt', sa.Text(), nullable=False, comment='发送给 LLM 的完整 prompt'),
    sa.Column('model_name', sa.String(length=100), nullable=False, comment='使用的模型名称'),
    sa.Column('temperature', sa.Float(), nullable=True, comment='temperature 参数'),
    sa.Column('response', sa.Text(), nullable=True, comment='LLM 返回的完整响应'),
    sa.Column('success', sa.Boolean(), nullable=False, comment='调用是否成功'),
    sa.Column('error_message', sa.Text(), nullable=True, comment='失败时的错误信息'),
    sa.Column('error_type', sa.String(length=50), nullable=True, comment='错误类型'),
    sa.Column('latency_ms', sa.Integer(), nullable=True, comment='总延迟（毫秒）'),
    sa.Column('first_token_latency_ms', sa.Integer(), nullable=True, comment='首 token 延迟'),
    sa.Column('prompt_tokens', sa.Integer(), nullable=True, comment='输入 token 数'),
    sa.Column('completion_tokens', sa.Integer(), nullable=True, comment='输出 token 数'),
    sa.Column('total_tokens', sa.Integer(), nullable=True, comment='总 token 数'),
    sa.Column('cost_estimate', sa.Float(), nullable=True, comment='估算的调用成本'),
    sa.Column('metadata_json', sa.JSON(), nullable=True, comment='额外元数据'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='调用时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_invocation_user_id', 'ai_invocation_logs', ['user_id'], unique=False)
    op.create_index('idx_ai_invocation_feature', 'ai_invocation_logs', ['feature'], unique=False)
    op.create_index('idx_ai_invocation_success', 'ai_invocation_logs', ['success'], unique=False)
    op.create_index('idx_ai_invocation_created_at', 'ai_invocation_logs', ['created_at'], unique=False)
    op.create_index('idx_ai_invocation_prompt_version_id', 'ai_invocation_logs', ['prompt_version_id'], unique=False)


def downgrade():
    op.drop_index('idx_ai_invocation_prompt_version_id', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_created_at', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_success', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_feature', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_user_id', table_name='ai_invocation_logs')
    op.drop_table('ai_invocation_logs')
    op.drop_index('idx_prompt_versions_version', table_name='prompt_versions')
    op.drop_index('idx_prompt_versions_is_active', table_name='prompt_versions')
    op.drop_index('idx_prompt_versions_feature', table_name='prompt_versions')
    op.drop_table('prompt_versions')
