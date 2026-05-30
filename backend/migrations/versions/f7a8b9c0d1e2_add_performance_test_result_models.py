"""Add performance test result and metric sample models

Revision ID: f7a8b9c0d1e2
Revises: b1f4c9a7d2e1
Create Date: 2026-05-30 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7a8b9c0d1e2'
down_revision = 'b1f4c9a7d2e1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('performance_test_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scenario_id', sa.Integer(), sa.ForeignKey('perf_test_scenarios.id'), nullable=False, comment='关联的性能测试场景 ID'),
    sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True, comment='项目 ID'),
    sa.Column('user_count', sa.Integer(), nullable=False, comment='并发用户数'),
    sa.Column('spawn_rate', sa.Integer(), nullable=False, comment='用户生成速率'),
    sa.Column('duration', sa.Integer(), nullable=False, comment='持续时间（秒）'),
    sa.Column('target_url', sa.String(length=500), nullable=True, comment='目标 URL'),
    sa.Column('status', sa.String(length=20), server_default='running', nullable=True, comment='状态: running/completed/failed/stopped'),
    sa.Column('started_at', sa.DateTime(), nullable=True, comment='开始时间'),
    sa.Column('finished_at', sa.DateTime(), nullable=True, comment='结束时间'),
    sa.Column('total_requests', sa.Integer(), server_default='0', nullable=True, comment='总请求数'),
    sa.Column('total_failures', sa.Integer(), server_default='0', nullable=True, comment='失败请求数'),
    sa.Column('error_rate', sa.Float(), server_default='0', nullable=True, comment='错误率 (%)'),
    sa.Column('rps', sa.Float(), server_default='0', nullable=True, comment='最大 RPS'),
    sa.Column('avg_response_time', sa.Float(), nullable=True, comment='平均响应时间 (ms)'),
    sa.Column('min_response_time', sa.Float(), nullable=True, comment='最小响应时间 (ms)'),
    sa.Column('max_response_time', sa.Float(), nullable=True, comment='最大响应时间 (ms)'),
    sa.Column('p50_response_time', sa.Float(), nullable=True, comment='P50 响应时间 (ms)'),
    sa.Column('p75_response_time', sa.Float(), nullable=True, comment='P75 响应时间 (ms)'),
    sa.Column('p95_response_time', sa.Float(), nullable=True, comment='P95 响应时间 (ms)'),
    sa.Column('p99_response_time', sa.Float(), nullable=True, comment='P99 响应时间 (ms)'),
    sa.Column('raw_result', sa.JSON(), nullable=True, comment='原始结果 JSON'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_perf_results_scenario_id', 'performance_test_results', ['scenario_id'], unique=False)
    op.create_index('idx_perf_results_project_id', 'performance_test_results', ['project_id'], unique=False)
    op.create_index('idx_perf_results_created_at', 'performance_test_results', ['created_at'], unique=False)

    op.create_table('performance_metric_samples',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test_result_id', sa.Integer(), sa.ForeignKey('performance_test_results.id'), nullable=False, comment='关联的测试结果 ID'),
    sa.Column('timestamp', sa.DateTime(), nullable=False, comment='采样时间点'),
    sa.Column('elapsed_seconds', sa.Integer(), nullable=False, comment='自测试开始后的秒数'),
    sa.Column('rps', sa.Float(), server_default='0', nullable=True, comment='当前 RPS'),
    sa.Column('active_users', sa.Integer(), server_default='0', nullable=True, comment='当前活跃用户数'),
    sa.Column('avg_response_time', sa.Float(), nullable=True, comment='平均响应时间 (ms)'),
    sa.Column('min_response_time', sa.Float(), nullable=True, comment='最小响应时间 (ms)'),
    sa.Column('max_response_time', sa.Float(), nullable=True, comment='最大响应时间 (ms)'),
    sa.Column('p95_response_time', sa.Float(), nullable=True, comment='P95 响应时间 (ms)'),
    sa.Column('p99_response_time', sa.Float(), nullable=True, comment='P99 响应时间 (ms)'),
    sa.Column('request_count', sa.Integer(), server_default='0', nullable=True, comment='累计请求数'),
    sa.Column('failure_count', sa.Integer(), server_default='0', nullable=True, comment='累计失败数'),
    sa.Column('error_rate', sa.Float(), server_default='0', nullable=True, comment='当前错误率 (%)'),
    sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_perf_samples_result_id', 'performance_metric_samples', ['test_result_id'], unique=False)
    op.create_index('idx_perf_samples_timestamp', 'performance_metric_samples', ['timestamp'], unique=False)


def downgrade():
    op.drop_index('idx_perf_samples_timestamp', table_name='performance_metric_samples')
    op.drop_index('idx_perf_samples_result_id', table_name='performance_metric_samples')
    op.drop_table('performance_metric_samples')
    op.drop_index('idx_perf_results_created_at', table_name='performance_test_results')
    op.drop_index('idx_perf_results_project_id', table_name='performance_test_results')
    op.drop_index('idx_perf_results_scenario_id', table_name='performance_test_results')
    op.drop_table('performance_test_results')
