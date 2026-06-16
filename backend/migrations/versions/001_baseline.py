"""
基线迁移：全部模型定义

本迁移文件包含 FullScopeTest 项目所有数据库表的完整定义，
替代此前 19 个分散的迁移文件，提供干净的迁移起点。

适用于 SQLite 和 PostgreSQL。

备份位置：backend/migrations/versions/backup/
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_baseline'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # === 基线迁移：创建全部 40 张表 ===

    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('avatar', sa.String(255), nullable=True),
        sa.Column('role', sa.String(20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('reset_token', sa.String(255), nullable=True),
        sa.Column('reset_token_expires', sa.DateTime(), nullable=True),
        sa.Column('password_changed_at', sa.DateTime(), nullable=True),
        sa.Column('sso_provider', sa.String(50), nullable=True),
        sa.Column('sso_id', sa.String(255), nullable=True),
        sa.Column('sso_metadata', sa.JSON(), nullable=True)
    )

    op.create_table('api_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('token_hash', sa.String(256), nullable=False),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('project_ids', sa.JSON(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('comments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('mentions', sa.JSON(), nullable=True),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('comments.id'), nullable=True),
        sa.Column('is_edited', sa.Boolean(), nullable=True),
        sa.Column('edited_at', sa.DateTime(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('github_integrations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('github_user_id', sa.String(50), nullable=False),
        sa.Column('github_username', sa.String(100), nullable=False),
        sa.Column('github_email', sa.String(200), nullable=True),
        sa.Column('github_avatar', sa.String(500), nullable=True),
        sa.Column('access_token_encrypted', sa.Text(), nullable=False),
        sa.Column('token_type', sa.String(50), nullable=True),
        sa.Column('scope', sa.String(500), nullable=True),
        sa.Column('token_expires_at', sa.DateTime(), nullable=True),
        sa.Column('refresh_token_encrypted', sa.Text(), nullable=True),
        sa.Column('refresh_token_expires_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True)
    )

    op.create_table('notification_configs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('channel', sa.String(20), nullable=False),
        sa.Column('webhook_url', sa.String(500), nullable=False),
        sa.Column('token', sa.String(500), nullable=True),
        sa.Column('events', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('organizations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('avatar', sa.String(500), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('prompt_versions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('feature', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('system_prompt', sa.Text(), nullable=False),
        sa.Column('user_prompt_template', sa.Text(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('model_name', sa.String(100), nullable=True),
        sa.Column('total_invocations', sa.Integer(), nullable=True),
        sa.Column('success_count', sa.Integer(), nullable=True),
        sa.Column('failure_count', sa.Integer(), nullable=True),
        sa.Column('avg_latency_ms', sa.Float(), nullable=True),
        sa.Column('avg_tokens', sa.Float(), nullable=True),
        sa.Column('avg_cost', sa.Float(), nullable=True),
        sa.Column('traffic_weight', sa.Float(), nullable=True),
        sa.Column('change_notes', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deactivated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_case_versions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('case_type', sa.String(20), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('change_summary', sa.String(500), nullable=True),
        sa.Column('changed_fields', sa.JSON(), nullable=True),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('ai_invocation_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('feature', sa.String(50), nullable=False),
        sa.Column('prompt_version_id', sa.Integer(), sa.ForeignKey('prompt_versions.id'), nullable=True),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('model_name', sa.String(100), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('response', sa.Text(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('error_type', sa.String(50), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('first_token_latency_ms', sa.Integer(), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=True),
        sa.Column('completion_tokens', sa.Integer(), nullable=True),
        sa.Column('total_tokens', sa.Integer(), nullable=True),
        sa.Column('cost_estimate', sa.Float(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('changes', sa.JSON(), nullable=True),
        sa.Column('old_values', sa.JSON(), nullable=True),
        sa.Column('new_values', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('organization_members',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('role', sa.String(20), nullable=True),
        sa.Column('invited_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('projects',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('quotas',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('limit', sa.Integer(), nullable=False),
        sa.Column('used', sa.Integer(), nullable=False),
        sa.Column('plan', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('roles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('display_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True),
        sa.Column('is_system', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('permissions', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('api_test_collections',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('api_test_collections.id'), nullable=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('app_test_collections',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('environments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('base_url', sa.String(255), nullable=False),
        sa.Column('variables', sa.JSON(), nullable=True),
        sa.Column('headers', sa.JSON(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('perf_test_scenarios',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_url', sa.String(500), nullable=False),
        sa.Column('method', sa.String(10), nullable=True),
        sa.Column('headers', sa.JSON(), nullable=True),
        sa.Column('body', sa.JSON(), nullable=True),
        sa.Column('script_content', sa.Text(), nullable=True),
        sa.Column('user_count', sa.Integer(), nullable=True),
        sa.Column('spawn_rate', sa.Integer(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('ramp_up', sa.Integer(), nullable=True),
        sa.Column('step_load_enabled', sa.Boolean(), nullable=True),
        sa.Column('step_users', sa.Integer(), nullable=True),
        sa.Column('step_duration', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('last_result', sa.JSON(), nullable=True),
        sa.Column('avg_response_time', sa.Float(), nullable=True),
        sa.Column('max_response_time', sa.Float(), nullable=True),
        sa.Column('min_response_time', sa.Float(), nullable=True),
        sa.Column('throughput', sa.Float(), nullable=True),
        sa.Column('error_rate', sa.Float(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('quality_gates',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('min_pass_rate', sa.Float(), nullable=True),
        sa.Column('max_p95_response_time', sa.Float(), nullable=True),
        sa.Column('max_visual_diff_percentage', sa.Float(), nullable=True),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('scheduled_tasks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('cron_expression', sa.String(100), nullable=False),
        sa.Column('target_type', sa.String(50), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('notify_webhook', sa.String(500), nullable=True),
        sa.Column('notify_events', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_documents',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('version', sa.String(20), nullable=True),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_plans',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('include_cases', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('total_runs', sa.Integer(), nullable=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('last_pass_rate', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_runs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('test_type', sa.String(20), nullable=False),
        sa.Column('test_object_id', sa.Integer(), nullable=True),
        sa.Column('test_object_name', sa.String(255), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('total_cases', sa.Integer(), nullable=True),
        sa.Column('passed', sa.Integer(), nullable=True),
        sa.Column('failed', sa.Integer(), nullable=True),
        sa.Column('skipped', sa.Integer(), nullable=True),
        sa.Column('error', sa.Integer(), nullable=True),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('environment_id', sa.Integer(), nullable=True),
        sa.Column('environment_name', sa.String(50), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.Column('report_id', sa.Integer(), nullable=True),
        sa.Column('report_path', sa.String(500), nullable=True),
        sa.Column('allure_report_path', sa.String(500), nullable=True),
        sa.Column('triggered_by', sa.String(50), nullable=True),
        sa.Column('triggered_user_id', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('check_run_id', sa.Integer(), nullable=True),
        sa.Column('check_run_repo', sa.String(200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('trigger_rules',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('trigger_event', sa.String(50), nullable=False),
        sa.Column('target_branches', sa.JSON(), nullable=True),
        sa.Column('target_tags', sa.JSON(), nullable=True),
        sa.Column('include_paths', sa.JSON(), nullable=True),
        sa.Column('exclude_paths', sa.JSON(), nullable=True),
        sa.Column('test_types', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('target_type', sa.String(50), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('visual_baselines',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('test_case_id', sa.Integer(), nullable=False),
        sa.Column('test_type', sa.String(20), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('step_index', sa.Integer(), nullable=False),
        sa.Column('step_name', sa.String(255), nullable=True),
        sa.Column('baseline_image_path', sa.String(500), nullable=False),
        sa.Column('viewport_width', sa.Integer(), nullable=True),
        sa.Column('viewport_height', sa.Integer(), nullable=True),
        sa.Column('device_pixel_ratio', sa.Float(), nullable=True),
        sa.Column('full_page', sa.Boolean(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('web_test_collections',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('webhook_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('token', sa.String(100), nullable=False),
        sa.Column('target_type', sa.String(50), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('api_test_cases',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('collection_id', sa.Integer(), sa.ForeignKey('api_test_collections.id'), nullable=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('environment_id', sa.Integer(), sa.ForeignKey('environments.id'), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('method', sa.String(10), nullable=False),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('headers', sa.JSON(), nullable=True),
        sa.Column('params', sa.JSON(), nullable=True),
        sa.Column('body', sa.JSON(), nullable=True),
        sa.Column('body_type', sa.String(20), nullable=True),
        sa.Column('assertions', sa.JSON(), nullable=True),
        sa.Column('pre_script', sa.Text(), nullable=True),
        sa.Column('post_script', sa.Text(), nullable=True),
        sa.Column('variables', sa.JSON(), nullable=True),
        sa.Column('extract_variables', sa.JSON(), nullable=True),
        sa.Column('timeout', sa.Integer(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('last_status', sa.String(20), nullable=True),
        sa.Column('last_result', sa.JSON(), nullable=True),
        sa.Column('mock_enabled', sa.Boolean(), nullable=True),
        sa.Column('mock_response_code', sa.Integer(), nullable=True),
        sa.Column('mock_response_body', sa.Text(), nullable=True),
        sa.Column('mock_response_headers', sa.JSON(), nullable=True),
        sa.Column('mock_delay_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('app_test_scripts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('collection_id', sa.Integer(), sa.ForeignKey('app_test_collections.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('platform', sa.String(20), nullable=True),
        sa.Column('app_path', sa.String(500), nullable=True),
        sa.Column('app_package', sa.String(200), nullable=True),
        sa.Column('app_activity', sa.String(200), nullable=True),
        sa.Column('bundle_id', sa.String(200), nullable=True),
        sa.Column('device_name', sa.String(100), nullable=True),
        sa.Column('platform_version', sa.String(20), nullable=True),
        sa.Column('automation_name', sa.String(50), nullable=True),
        sa.Column('appium_server', sa.String(200), nullable=True),
        sa.Column('script_content', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('last_result', sa.JSON(), nullable=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('issue_links',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('test_run_id', sa.Integer(), sa.ForeignKey('test_runs.id'), nullable=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('tracker', sa.String(20), nullable=False),
        sa.Column('issue_key', sa.String(100), nullable=False),
        sa.Column('issue_url', sa.String(500), nullable=True),
        sa.Column('issue_title', sa.String(500), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('created_by', sa.String(20), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('extra', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('performance_alert_rules',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('scenario_id', sa.Integer(), sa.ForeignKey('perf_test_scenarios.id'), nullable=True),
        sa.Column('p95_threshold', sa.Float(), nullable=True),
        sa.Column('p99_threshold', sa.Float(), nullable=True),
        sa.Column('error_rate_threshold', sa.Float(), nullable=True),
        sa.Column('rps_min_threshold', sa.Float(), nullable=True),
        sa.Column('relative_p95_degradation', sa.Float(), nullable=True),
        sa.Column('relative_rps_degradation', sa.Float(), nullable=True),
        sa.Column('relative_error_rate_degradation', sa.Float(), nullable=True),
        sa.Column('notify_webhook', sa.String(500), nullable=True),
        sa.Column('notify_email', sa.Text(), nullable=True),
        sa.Column('enabled', sa.Boolean(), nullable=True),
        sa.Column('last_triggered_at', sa.DateTime(), nullable=True),
        sa.Column('trigger_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('performance_test_results',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('scenario_id', sa.Integer(), sa.ForeignKey('perf_test_scenarios.id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('user_count', sa.Integer(), nullable=False),
        sa.Column('spawn_rate', sa.Integer(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('target_url', sa.String(500), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('total_requests', sa.Integer(), nullable=True),
        sa.Column('total_failures', sa.Integer(), nullable=True),
        sa.Column('error_rate', sa.Float(), nullable=True),
        sa.Column('rps', sa.Float(), nullable=True),
        sa.Column('avg_response_time', sa.Float(), nullable=True),
        sa.Column('min_response_time', sa.Float(), nullable=True),
        sa.Column('max_response_time', sa.Float(), nullable=True),
        sa.Column('p50_response_time', sa.Float(), nullable=True),
        sa.Column('p75_response_time', sa.Float(), nullable=True),
        sa.Column('p95_response_time', sa.Float(), nullable=True),
        sa.Column('p99_response_time', sa.Float(), nullable=True),
        sa.Column('raw_result', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('quality_gate_evaluations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('quality_gate_id', sa.Integer(), sa.ForeignKey('quality_gates.id'), nullable=False),
        sa.Column('test_run_id', sa.Integer(), sa.ForeignKey('test_runs.id'), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('evaluation_details', sa.JSON(), nullable=True),
        sa.Column('github_check_run_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_plan_runs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('plan_id', sa.Integer(), sa.ForeignKey('test_plans.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('total_cases', sa.Integer(), nullable=True),
        sa.Column('passed', sa.Integer(), nullable=True),
        sa.Column('failed', sa.Integer(), nullable=True),
        sa.Column('skipped', sa.Integer(), nullable=True),
        sa.Column('error', sa.Integer(), nullable=True),
        sa.Column('pass_rate', sa.Float(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('environment_id', sa.Integer(), nullable=True),
        sa.Column('environment_name', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('triggered_by', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_reports',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('test_run_id', sa.Integer(), sa.ForeignKey('test_runs.id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('test_type', sa.String(20), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('summary', sa.JSON(), nullable=True),
        sa.Column('report_data', sa.JSON(), nullable=True),
        sa.Column('report_html', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('visual_diffs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('test_run_id', sa.Integer(), sa.ForeignKey('test_runs.id'), nullable=False),
        sa.Column('baseline_id', sa.Integer(), sa.ForeignKey('visual_baselines.id'), nullable=True),
        sa.Column('test_case_id', sa.Integer(), nullable=False),
        sa.Column('test_type', sa.String(20), nullable=False),
        sa.Column('step_index', sa.Integer(), nullable=False),
        sa.Column('step_name', sa.String(255), nullable=True),
        sa.Column('current_image_path', sa.String(500), nullable=False),
        sa.Column('diff_image_path', sa.String(500), nullable=True),
        sa.Column('diff_percentage', sa.Float(), nullable=False),
        sa.Column('diff_pixel_count', sa.Integer(), nullable=True),
        sa.Column('total_pixel_count', sa.Integer(), nullable=True),
        sa.Column('similarity_score', sa.Float(), nullable=True),
        sa.Column('viewport_width', sa.Integer(), nullable=True),
        sa.Column('viewport_height', sa.Integer(), nullable=True),
        sa.Column('threshold', sa.Float(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('is_baseline_current', sa.Boolean(), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('review_comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('web_test_scripts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('collection_id', sa.Integer(), sa.ForeignKey('web_test_collections.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('script_content', sa.Text(), nullable=False),
        sa.Column('script_type', sa.String(20), nullable=True),
        sa.Column('target_url', sa.String(500), nullable=True),
        sa.Column('browser', sa.String(20), nullable=True),
        sa.Column('headless', sa.Boolean(), nullable=True),
        sa.Column('timeout', sa.Integer(), nullable=True),
        sa.Column('viewport_width', sa.Integer(), nullable=True),
        sa.Column('viewport_height', sa.Integer(), nullable=True),
        sa.Column('config', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('last_status', sa.String(20), nullable=True),
        sa.Column('last_run_at', sa.DateTime(), nullable=True),
        sa.Column('last_run_duration', sa.Float(), nullable=True),
        sa.Column('last_result', sa.JSON(), nullable=True),
        sa.Column('step_count', sa.Integer(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )

    op.create_table('performance_alert_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('rule_id', sa.Integer(), sa.ForeignKey('performance_alert_rules.id'), nullable=False),
        sa.Column('result_id', sa.Integer(), sa.ForeignKey('performance_test_results.id'), nullable=False),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('metric_name', sa.String(50), nullable=False),
        sa.Column('threshold_value', sa.Float(), nullable=False),
        sa.Column('actual_value', sa.Float(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('notification_sent', sa.Boolean(), nullable=True),
        sa.Column('notification_error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('performance_metric_samples',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('test_result_id', sa.Integer(), sa.ForeignKey('performance_test_results.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('elapsed_seconds', sa.Integer(), nullable=False),
        sa.Column('rps', sa.Float(), nullable=True),
        sa.Column('active_users', sa.Integer(), nullable=True),
        sa.Column('avg_response_time', sa.Float(), nullable=True),
        sa.Column('min_response_time', sa.Float(), nullable=True),
        sa.Column('max_response_time', sa.Float(), nullable=True),
        sa.Column('p95_response_time', sa.Float(), nullable=True),
        sa.Column('p99_response_time', sa.Float(), nullable=True),
        sa.Column('request_count', sa.Integer(), nullable=True),
        sa.Column('failure_count', sa.Integer(), nullable=True),
        sa.Column('error_rate', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table('test_plan_case_results',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('run_id', sa.Integer(), sa.ForeignKey('test_plan_runs.id'), nullable=False),
        sa.Column('case_type', sa.String(20), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('case_name', sa.String(255), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('result_detail', sa.JSON(), nullable=True),
        sa.Column('test_run_id', sa.Integer(), nullable=True),
        sa.Column('executed_at', sa.DateTime(), nullable=True)
    )

    # === 索引 ===
    op.create_index('idx_users_role', 'users', ['role'])
    op.create_index('idx_api_tokens_user_id', 'api_tokens', ['user_id'])
    op.create_index('idx_comments_created_at', 'comments', ['created_at'])
    op.create_index('idx_comments_resource', 'comments', ['resource_type', 'resource_id'])
    op.create_index('idx_comments_user_id', 'comments', ['user_id'])
    op.create_index('idx_github_integrations_user_id', 'github_integrations', ['user_id'])
    op.create_index('idx_github_integrations_github_user_id', 'github_integrations', ['github_user_id'])
    op.create_index('idx_notif_config_user_id', 'notification_configs', ['user_id'])
    op.create_index('idx_organizations_owner_id', 'organizations', ['owner_id'])
    op.create_index('idx_prompt_versions_version', 'prompt_versions', ['version'])
    op.create_index('idx_prompt_versions_feature', 'prompt_versions', ['feature'])
    op.create_index('idx_prompt_versions_is_active', 'prompt_versions', ['is_active'])
    op.create_index('idx_tc_versions_case', 'test_case_versions', ['case_type', 'case_id'])
    op.create_index('idx_tc_versions_created', 'test_case_versions', ['created_at'])
    op.create_index('idx_ai_invocation_created_at', 'ai_invocation_logs', ['created_at'])
    op.create_index('idx_ai_invocation_user_id', 'ai_invocation_logs', ['user_id'])
    op.create_index('idx_ai_invocation_prompt_version_id', 'ai_invocation_logs', ['prompt_version_id'])
    op.create_index('idx_ai_invocation_feature', 'ai_invocation_logs', ['feature'])
    op.create_index('idx_ai_invocation_success', 'ai_invocation_logs', ['success'])
    op.create_index('idx_audit_logs_organization_id', 'audit_logs', ['organization_id'])
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_logs_resource_type', 'audit_logs', ['resource_type'])
    op.create_index('idx_audit_logs_created_at', 'audit_logs', ['created_at'])
    op.create_index('idx_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_org_members_org_id', 'organization_members', ['organization_id'])
    op.create_index('idx_org_members_user_id', 'organization_members', ['user_id'])
    op.create_index('idx_quotas_org_id', 'quotas', ['organization_id'])
    op.create_index('idx_roles_org_id', 'roles', ['organization_id'])
    op.create_index('idx_api_test_collections_user_id', 'api_test_collections', ['user_id'])
    op.create_index('idx_api_test_collections_parent_id', 'api_test_collections', ['parent_id'])
    op.create_index('idx_api_test_collections_project_id', 'api_test_collections', ['project_id'])
    op.create_index('idx_perf_test_scenarios_status', 'perf_test_scenarios', ['status'])
    op.create_index('idx_perf_test_scenarios_user_id', 'perf_test_scenarios', ['user_id'])
    op.create_index('idx_perf_test_scenarios_project_id', 'perf_test_scenarios', ['project_id'])
    op.create_index('idx_test_plans_project_id', 'test_plans', ['project_id'])
    op.create_index('idx_test_plans_user_id', 'test_plans', ['user_id'])
    op.create_index('idx_test_plans_status', 'test_plans', ['status'])
    op.create_index('idx_test_runs_project_id', 'test_runs', ['project_id'])
    op.create_index('idx_test_runs_created_at', 'test_runs', ['created_at'])
    op.create_index('idx_test_runs_project_type', 'test_runs', ['project_id', 'test_type'])
    op.create_index('idx_test_runs_status', 'test_runs', ['status'])
    op.create_index('idx_test_runs_test_type', 'test_runs', ['test_type'])
    op.create_index('idx_visual_baselines_project_id', 'visual_baselines', ['project_id'])
    op.create_index('idx_visual_baselines_test_case_id', 'visual_baselines', ['test_case_id'])
    op.create_index('idx_visual_baselines_step_index', 'visual_baselines', ['step_index'])
    op.create_index('idx_api_test_cases_user_id', 'api_test_cases', ['user_id'])
    op.create_index('idx_api_test_cases_project_id', 'api_test_cases', ['project_id'])
    op.create_index('idx_api_test_cases_collection_id', 'api_test_cases', ['collection_id'])
    op.create_index('idx_api_test_cases_method', 'api_test_cases', ['method'])
    op.create_index('idx_issue_links_status', 'issue_links', ['status'])
    op.create_index('idx_issue_links_test_run_id', 'issue_links', ['test_run_id'])
    op.create_index('idx_issue_links_tracker', 'issue_links', ['tracker'])
    op.create_index('idx_alert_rules_scenario_id', 'performance_alert_rules', ['scenario_id'])
    op.create_index('idx_alert_rules_enabled', 'performance_alert_rules', ['enabled'])
    op.create_index('idx_perf_results_scenario_id', 'performance_test_results', ['scenario_id'])
    op.create_index('idx_perf_results_project_id', 'performance_test_results', ['project_id'])
    op.create_index('idx_perf_results_created_at', 'performance_test_results', ['created_at'])
    op.create_index('idx_test_plan_runs_plan_id', 'test_plan_runs', ['plan_id'])
    op.create_index('idx_test_plan_runs_status', 'test_plan_runs', ['status'])
    op.create_index('idx_visual_diffs_test_run_id', 'visual_diffs', ['test_run_id'])
    op.create_index('idx_visual_diffs_baseline_id', 'visual_diffs', ['baseline_id'])
    op.create_index('idx_visual_diffs_test_case_id', 'visual_diffs', ['test_case_id'])
    op.create_index('idx_visual_diffs_status', 'visual_diffs', ['status'])
    op.create_index('idx_alert_logs_result_id', 'performance_alert_logs', ['result_id'])
    op.create_index('idx_alert_logs_created_at', 'performance_alert_logs', ['created_at'])
    op.create_index('idx_alert_logs_rule_id', 'performance_alert_logs', ['rule_id'])
    op.create_index('idx_perf_samples_result_id', 'performance_metric_samples', ['test_result_id'])
    op.create_index('idx_perf_samples_timestamp', 'performance_metric_samples', ['timestamp'])
    op.create_index('idx_tp_case_results_run_id', 'test_plan_case_results', ['run_id'])


def downgrade():
    # 删除全部表（按逆序）
    op.drop_index('idx_tp_case_results_run_id', table_name='test_plan_case_results')
    op.drop_index('idx_perf_samples_result_id', table_name='performance_metric_samples')
    op.drop_index('idx_perf_samples_timestamp', table_name='performance_metric_samples')
    op.drop_index('idx_alert_logs_result_id', table_name='performance_alert_logs')
    op.drop_index('idx_alert_logs_created_at', table_name='performance_alert_logs')
    op.drop_index('idx_alert_logs_rule_id', table_name='performance_alert_logs')
    op.drop_index('idx_visual_diffs_test_run_id', table_name='visual_diffs')
    op.drop_index('idx_visual_diffs_baseline_id', table_name='visual_diffs')
    op.drop_index('idx_visual_diffs_test_case_id', table_name='visual_diffs')
    op.drop_index('idx_visual_diffs_status', table_name='visual_diffs')
    op.drop_index('idx_test_plan_runs_plan_id', table_name='test_plan_runs')
    op.drop_index('idx_test_plan_runs_status', table_name='test_plan_runs')
    op.drop_index('idx_perf_results_scenario_id', table_name='performance_test_results')
    op.drop_index('idx_perf_results_project_id', table_name='performance_test_results')
    op.drop_index('idx_perf_results_created_at', table_name='performance_test_results')
    op.drop_index('idx_alert_rules_scenario_id', table_name='performance_alert_rules')
    op.drop_index('idx_alert_rules_enabled', table_name='performance_alert_rules')
    op.drop_index('idx_issue_links_status', table_name='issue_links')
    op.drop_index('idx_issue_links_test_run_id', table_name='issue_links')
    op.drop_index('idx_issue_links_tracker', table_name='issue_links')
    op.drop_index('idx_api_test_cases_user_id', table_name='api_test_cases')
    op.drop_index('idx_api_test_cases_project_id', table_name='api_test_cases')
    op.drop_index('idx_api_test_cases_collection_id', table_name='api_test_cases')
    op.drop_index('idx_api_test_cases_method', table_name='api_test_cases')
    op.drop_index('idx_visual_baselines_project_id', table_name='visual_baselines')
    op.drop_index('idx_visual_baselines_test_case_id', table_name='visual_baselines')
    op.drop_index('idx_visual_baselines_step_index', table_name='visual_baselines')
    op.drop_index('idx_test_runs_project_id', table_name='test_runs')
    op.drop_index('idx_test_runs_created_at', table_name='test_runs')
    op.drop_index('idx_test_runs_project_type', table_name='test_runs')
    op.drop_index('idx_test_runs_status', table_name='test_runs')
    op.drop_index('idx_test_runs_test_type', table_name='test_runs')
    op.drop_index('idx_test_plans_project_id', table_name='test_plans')
    op.drop_index('idx_test_plans_user_id', table_name='test_plans')
    op.drop_index('idx_test_plans_status', table_name='test_plans')
    op.drop_index('idx_perf_test_scenarios_status', table_name='perf_test_scenarios')
    op.drop_index('idx_perf_test_scenarios_user_id', table_name='perf_test_scenarios')
    op.drop_index('idx_perf_test_scenarios_project_id', table_name='perf_test_scenarios')
    op.drop_index('idx_api_test_collections_user_id', table_name='api_test_collections')
    op.drop_index('idx_api_test_collections_parent_id', table_name='api_test_collections')
    op.drop_index('idx_api_test_collections_project_id', table_name='api_test_collections')
    op.drop_index('idx_roles_org_id', table_name='roles')
    op.drop_index('idx_quotas_org_id', table_name='quotas')
    op.drop_index('idx_org_members_org_id', table_name='organization_members')
    op.drop_index('idx_org_members_user_id', table_name='organization_members')
    op.drop_index('idx_audit_logs_organization_id', table_name='audit_logs')
    op.drop_index('idx_audit_logs_action', table_name='audit_logs')
    op.drop_index('idx_audit_logs_resource_type', table_name='audit_logs')
    op.drop_index('idx_audit_logs_created_at', table_name='audit_logs')
    op.drop_index('idx_audit_logs_user_id', table_name='audit_logs')
    op.drop_index('idx_ai_invocation_created_at', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_user_id', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_prompt_version_id', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_feature', table_name='ai_invocation_logs')
    op.drop_index('idx_ai_invocation_success', table_name='ai_invocation_logs')
    op.drop_index('idx_tc_versions_case', table_name='test_case_versions')
    op.drop_index('idx_tc_versions_created', table_name='test_case_versions')
    op.drop_index('idx_prompt_versions_version', table_name='prompt_versions')
    op.drop_index('idx_prompt_versions_feature', table_name='prompt_versions')
    op.drop_index('idx_prompt_versions_is_active', table_name='prompt_versions')
    op.drop_index('idx_organizations_owner_id', table_name='organizations')
    op.drop_index('idx_notif_config_user_id', table_name='notification_configs')
    op.drop_index('idx_github_integrations_user_id', table_name='github_integrations')
    op.drop_index('idx_github_integrations_github_user_id', table_name='github_integrations')
    op.drop_index('idx_comments_created_at', table_name='comments')
    op.drop_index('idx_comments_resource', table_name='comments')
    op.drop_index('idx_comments_user_id', table_name='comments')
    op.drop_index('idx_api_tokens_user_id', table_name='api_tokens')
    op.drop_index('idx_users_role', table_name='users')
    op.drop_table('test_plan_case_results')
    op.drop_table('performance_metric_samples')
    op.drop_table('performance_alert_logs')
    op.drop_table('web_test_scripts')
    op.drop_table('visual_diffs')
    op.drop_table('test_reports')
    op.drop_table('test_plan_runs')
    op.drop_table('quality_gate_evaluations')
    op.drop_table('performance_test_results')
    op.drop_table('performance_alert_rules')
    op.drop_table('issue_links')
    op.drop_table('app_test_scripts')
    op.drop_table('api_test_cases')
    op.drop_table('webhook_tokens')
    op.drop_table('web_test_collections')
    op.drop_table('visual_baselines')
    op.drop_table('trigger_rules')
    op.drop_table('test_runs')
    op.drop_table('test_plans')
    op.drop_table('test_documents')
    op.drop_table('scheduled_tasks')
    op.drop_table('quality_gates')
    op.drop_table('perf_test_scenarios')
    op.drop_table('environments')
    op.drop_table('app_test_collections')
    op.drop_table('api_test_collections')
    op.drop_table('roles')
    op.drop_table('quotas')
    op.drop_table('projects')
    op.drop_table('organization_members')
    op.drop_table('audit_logs')
    op.drop_table('ai_invocation_logs')
    op.drop_table('test_case_versions')
    op.drop_table('prompt_versions')
    op.drop_table('organizations')
    op.drop_table('notification_configs')
    op.drop_table('github_integrations')
    op.drop_table('comments')
    op.drop_table('api_tokens')
    op.drop_table('users')
