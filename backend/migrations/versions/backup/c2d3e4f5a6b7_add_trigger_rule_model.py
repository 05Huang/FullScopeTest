"""add trigger rule model

Revision ID: c2d3e4f5a6b7
Revises: f1e2d3c4b5a6
Create Date: 2026-05-30 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d3e4f5a6b7'
down_revision = 'f1e2d3c4b5a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('trigger_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('trigger_event', sa.String(length=50), nullable=False),
    sa.Column('target_branches', sa.JSON(), nullable=True),
    sa.Column('target_tags', sa.JSON(), nullable=True),
    sa.Column('include_paths', sa.JSON(), nullable=True),
    sa.Column('exclude_paths', sa.JSON(), nullable=True),
    sa.Column('test_types', sa.JSON(), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=True),
    sa.Column('target_type', sa.String(length=50), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('trigger_rules')
