"""add performance alert rule and log tables

Revision ID: d4e5f6a7b8c9
Revises: f7a8b9c0d1e2
Create Date: 2026-05-30

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e5f6a7b8c9'
down_revision = 'f7a8b9c0d1e2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('performance_alert_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False, comment='告警规则名称'),
    sa.Column('description', sa.Text(), nullable=True, comment='告警规则描述'),
    sa.Column('scenario_id', sa.Integer(), sa.ForeignKey('perf_test_scenarios.id'), nullable=True, comment='关联的性能测试场景 ID'),
    sa.Column('p95_threshold', sa.Float(), nullable=True, comment='P95 响应时间阈值 (ms)'),
    sa.Column('p99_threshold', sa.Float(), nullable=True, comment='P99 响应时间阈值 (ms)'),
    sa.Column('error_rate_threshold', sa.Float(), nullable=True, comment='错误率阈值 (%)'),
    sa.Column('rps_min_threshold', sa.Float(), nullable=True, comment='最小 RPS 阈值'),
    sa.Column('relative_p95_degradation', sa.Float(), nullable=True, comment='P95 劣化百分比阈值 (%)'),
    sa.Column('relative_rps_degradation', sa.Float(), nullable=True, comment='RPS 劣化百分比阈值 (%)'),
    sa.Column('relative_error_rate_degradation', sa.Float(), nullable=True, comment='错误率劣化百分比阈值 (%)'),
    sa.Column('notify_webhook', sa.String(length=500), nullable=True, comment='Webhook 通知 URL'),
    sa.Column('notify_email', sa.Text(), nullable=True, comment='邮件通知列表 (JSON 数组)'),
    sa.Column('enabled', sa.Boolean(), nullable=True, comment='是否启用'),
    sa.Column('last_triggered_at', sa.DateTime(), nullable=True, comment='最后触发时间'),
    sa.Column('trigger_count', sa.Integer(), nullable=True, comment='触发次数'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_alert_rules_scenario_id', 'performance_alert_rules', ['scenario_id'], unique=False)
    op.create_index('idx_alert_rules_enabled', 'performance_alert_rules', ['enabled'], unique=False)

    op.create_table('performance_alert_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rule_id', sa.Integer(), sa.ForeignKey('performance_alert_rules.id'), nullable=False, comment='关联的告警规则 ID'),
    sa.Column('result_id', sa.Integer(), sa.ForeignKey('performance_test_results.id'), nullable=False, comment='关联的性能测试结果 ID'),
    sa.Column('alert_type', sa.String(length=50), nullable=False, comment='告警类型: absolute/relative'),
    sa.Column('metric_name', sa.String(length=50), nullable=False, comment='触发告警的指标名称'),
    sa.Column('threshold_value', sa.Float(), nullable=False, comment='阈值'),
    sa.Column('actual_value', sa.Float(), nullable=False, comment='实际值'),
    sa.Column('message', sa.Text(), nullable=False, comment='告警消息'),
    sa.Column('notification_sent', sa.Boolean(), nullable=True, comment='是否已发送通知'),
    sa.Column('notification_error', sa.Text(), nullable=True, comment='通知发送失败的错误信息'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_alert_logs_rule_id', 'performance_alert_logs', ['rule_id'], unique=False)
    op.create_index('idx_alert_logs_result_id', 'performance_alert_logs', ['result_id'], unique=False)
    op.create_index('idx_alert_logs_created_at', 'performance_alert_logs', ['created_at'], unique=False)


def downgrade():
    op.drop_index('idx_alert_logs_created_at', table_name='performance_alert_logs')
    op.drop_index('idx_alert_logs_result_id', table_name='performance_alert_logs')
    op.drop_index('idx_alert_logs_rule_id', table_name='performance_alert_logs')
    op.drop_table('performance_alert_logs')
    op.drop_index('idx_alert_rules_enabled', table_name='performance_alert_rules')
    op.drop_index('idx_alert_rules_scenario_id', table_name='performance_alert_rules')
    op.drop_table('performance_alert_rules')
