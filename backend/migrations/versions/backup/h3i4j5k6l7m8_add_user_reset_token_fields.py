"""add user reset token fields for password reset

Revision ID: h3i4j5k6l7m8
Revises: g2h3i4j5k6l7
Create Date: 2026-05-31 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'h3i4j5k6l7m8'
down_revision = 'g2h3i4j5k6l7'
branch_labels = None
depends_on = None


def upgrade():
    # 添加密码重置 Token 字段
    op.add_column('users', sa.Column('reset_token', sa.String(255), nullable=True, comment='密码重置 Token'))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(), nullable=True, comment='重置 Token 过期时间'))


def downgrade():
    # 移除密码重置 Token 字段
    op.drop_column('users', 'reset_token_expires')
    op.drop_column('users', 'reset_token')
