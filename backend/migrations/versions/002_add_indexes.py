"""
索引优化：高频查询字段添加索引

添加的索引：
- api_test_cases: (project_id, created_at DESC) 用于分页查询
- test_runs: (project_id, created_at DESC) 用于分页查询
- test_reports: (run_id), (project_id)
- audit_logs: (user_id, created_at DESC) 用于分页查询
- comments: (resource_type, resource_id) 用于资源评论查询
- notifications: (user_id, is_read) 用于未读通知查询
- api_tokens: (user_id, is_active) 用于活跃 Token 查询
- test_plans: (project_id) 用于项目计划查询
- quality_gates: (project_id) 用于项目门禁查询
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '002_add_indexes'
down_revision = '001_baseline'
branch_labels = None
depends_on = None


def upgrade():
    # === 复合索引（分页查询优化）===
    op.create_index(
        'idx_api_test_cases_project_created',
        'api_test_cases',
        ['project_id', 'created_at'],
        unique=False,
    )
    op.create_index(
        'idx_test_runs_project_created',
        'test_runs',
        ['project_id', 'created_at'],
        unique=False,
    )
    op.create_index(
        'idx_audit_logs_user_created',
        'audit_logs',
        ['user_id', 'created_at'],
        unique=False,
    )
    op.create_index(
        'idx_test_plan_runs_plan_created',
        'test_plan_runs',
        ['plan_id', 'created_at'],
        unique=False,
    )
    op.create_index(
        'idx_performance_results_scenario_created',
        'performance_test_results',
        ['scenario_id', 'created_at'],
        unique=False,
    )

    # === 覆盖查询索引 ===
    op.create_index(
        'idx_test_reports_run_id',
        'test_reports',
        ['test_run_id'],
        unique=False,
    )
    op.create_index(
        'idx_test_reports_project_id',
        'test_reports',
        ['project_id'],
        unique=False,
    )
    op.create_index(
        'idx_notification_configs_user_active',
        'notification_configs',
        ['user_id', 'is_active'],
        unique=False,
    )
    op.create_index(
        'idx_api_tokens_active',
        'api_tokens',
        ['is_active'],
        unique=False,
    )
    op.create_index(
        'idx_environments_project',
        'environments',
        ['project_id'],
        unique=False,
    )
    op.create_index(
        'idx_trigger_rules_project',
        'trigger_rules',
        ['project_id'],
        unique=False,
    )
    op.create_index(
        'idx_webhook_tokens_project',
        'webhook_tokens',
        ['project_id'],
        unique=False,
    )


def downgrade():
    op.drop_index('idx_webhook_tokens_project', table_name='webhook_tokens')
    op.drop_index('idx_trigger_rules_project', table_name='trigger_rules')
    op.drop_index('idx_environments_project', table_name='environments')
    op.drop_index('idx_api_tokens_active', table_name='api_tokens')
    op.drop_index('idx_notification_configs_user_active', table_name='notification_configs')
    op.drop_index('idx_test_reports_project_id', table_name='test_reports')
    op.drop_index('idx_test_reports_run_id', table_name='test_reports')
    op.drop_index('idx_performance_results_scenario_created', table_name='performance_test_results')
    op.drop_index('idx_test_plan_runs_plan_created', table_name='test_plan_runs')
    op.drop_index('idx_audit_logs_user_created', table_name='audit_logs')
    op.drop_index('idx_test_runs_project_created', table_name='test_runs')
    op.drop_index('idx_api_test_cases_project_created', table_name='api_test_cases')
