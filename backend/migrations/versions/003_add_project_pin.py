"""
项目置顶功能

为 projects 表添加 is_pinned 和 pinned_at 字段
"""
from alembic import op
import sqlalchemy as sa

revision = '003_add_project_pin'
down_revision = '002_add_indexes'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('projects', sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='false', comment='是否置顶'))
    op.add_column('projects', sa.Column('pinned_at', sa.DateTime(), nullable=True, comment='置顶时间'))


def downgrade():
    op.drop_column('projects', 'pinned_at')
    op.drop_column('projects', 'is_pinned')
