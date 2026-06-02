"""add multi-tenant organization models

Revision ID: g2h3i4j5k6l7
Revises: f1e2d3c4b5a6
Create Date: 2026-05-30 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'g2h3i4j5k6l7'
down_revision = 'f1e2d3c4b5a6'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 organizations 表
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, comment='组织名称'),
        sa.Column('slug', sa.String(100), nullable=False, unique=True, comment='组织 slug'),
        sa.Column('description', sa.Text(), nullable=True, comment='组织描述'),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, comment='创建者 ID'),
        sa.Column('avatar', sa.String(500), nullable=True, comment='组织头像 URL'),
        sa.Column('settings', sa.JSON(), server_default='{}', comment='组织设置'),
        sa.Column('is_active', sa.Boolean(), server_default='true', comment='是否激活'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), comment='更新时间'),
    )

    op.create_index('idx_organizations_owner_id', 'organizations', ['owner_id'], unique=False)

    # 创建 organization_members 表
    op.create_table(
        'organization_members',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False, comment='组织 ID'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, comment='用户 ID'),
        sa.Column('role', sa.String(20), server_default='member', comment='角色: owner/admin/member/viewer'),
        sa.Column('invited_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True, comment='邀请人 ID'),
        sa.Column('is_active', sa.Boolean(), server_default='true', comment='是否激活'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), comment='加入时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), comment='更新时间'),
        sa.UniqueConstraint('organization_id', 'user_id', name='uq_org_member'),
    )

    op.create_index('idx_org_members_org_id', 'organization_members', ['organization_id'], unique=False)
    op.create_index('idx_org_members_user_id', 'organization_members', ['user_id'], unique=False)

    # 为 projects 表添加 organization_id 外键
    op.add_column('projects', sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True, comment='组织 ID'))
    op.create_index('idx_projects_organization_id', 'projects', ['organization_id'], unique=False)

    # 创建默认组织（数据迁移）
    op.execute(
        "INSERT INTO organizations (name, slug, description, owner_id, is_active, created_at, updated_at) "
        "VALUES ('Default Organization', 'default', '系统默认组织', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    )

    # 将现有项目绑定到默认组织
    op.execute(
        "UPDATE projects SET organization_id = (SELECT id FROM organizations WHERE slug = 'default' LIMIT 1) "
        "WHERE organization_id IS NULL"
    )


def downgrade():
    # 删除 projects 表的 organization_id 字段
    op.drop_index('idx_projects_organization_id', table_name='projects')
    op.drop_column('projects', 'organization_id')

    # 删除 organization_members 表
    op.drop_index('idx_org_members_user_id', table_name='organization_members')
    op.drop_index('idx_org_members_org_id', table_name='organization_members')
    op.drop_table('organization_members')

    # 删除 organizations 表
    op.drop_index('idx_organizations_owner_id', table_name='organizations')
    op.drop_table('organizations')
