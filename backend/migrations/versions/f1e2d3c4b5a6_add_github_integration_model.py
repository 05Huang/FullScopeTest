"""add github integration model

Revision ID: f1e2d3c4b5a6
Revises: e1f2a3b4c5d6
Create Date: 2026-05-30 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1e2d3c4b5a6'
down_revision = 'e1f2a3b4c5d6'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 GitHubIntegration 表
    op.create_table(
        'github_integrations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, comment='本地用户 ID'),
        sa.Column('github_user_id', sa.String(50), nullable=False, comment='GitHub 用户 ID'),
        sa.Column('github_username', sa.String(100), nullable=False, comment='GitHub 用户名'),
        sa.Column('github_email', sa.String(200), nullable=True, comment='GitHub 邮箱'),
        sa.Column('github_avatar', sa.String(500), nullable=True, comment='GitHub 头像 URL'),
        sa.Column('access_token_encrypted', sa.Text(), nullable=False, comment='加密的 Access Token'),
        sa.Column('token_type', sa.String(50), server_default='bearer', comment='Token 类型'),
        sa.Column('scope', sa.String(500), nullable=True, comment='授权的 scope'),
        sa.Column('token_expires_at', sa.DateTime(), nullable=True, comment='Token 过期时间'),
        sa.Column('refresh_token_encrypted', sa.Text(), nullable=True, comment='加密的 Refresh Token'),
        sa.Column('refresh_token_expires_at', sa.DateTime(), nullable=True, comment='Refresh Token 过期时间'),
        sa.Column('is_active', sa.Boolean(), server_default='1', comment='是否激活'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), comment='更新时间'),
        sa.Column('last_used_at', sa.DateTime(), nullable=True, comment='最后使用时间'),
    )

    # 创建索引
    op.create_index(
        'idx_github_integrations_user_id',
        'github_integrations',
        ['user_id'],
        unique=False
    )
    op.create_index(
        'idx_github_integrations_github_user_id',
        'github_integrations',
        ['github_user_id'],
        unique=False
    )


def downgrade():
    # 删除索引
    op.drop_index('idx_github_integrations_github_user_id', table_name='github_integrations')
    op.drop_index('idx_github_integrations_user_id', table_name='github_integrations')

    # 删除表
    op.drop_table('github_integrations')
