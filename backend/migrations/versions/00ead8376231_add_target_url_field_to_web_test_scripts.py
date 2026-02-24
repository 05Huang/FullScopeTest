"""Add target_url field to web_test_scripts

Revision ID: 00ead8376231
Revises:
Create Date: 2025-12-24 20:04:09.345631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00ead8376231'
down_revision = None
branch_labels = None
depends_on = None


def _column_exists(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return column_name in {col['name'] for col in inspector.get_columns(table_name)}


def upgrade():
    if not _column_exists('web_test_scripts', 'target_url'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('target_url', sa.String(length=500), nullable=True, comment='鐩爣URL')
            )


def downgrade():
    if _column_exists('web_test_scripts', 'target_url'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.drop_column('target_url')
