"""Add last_result fields to web_test_scripts and perf_test_scenarios

Revision ID: 5ca026f04416
Revises: 00ead8376231
Create Date: 2025-12-24 20:17:57.723206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca026f04416'
down_revision = '00ead8376231'
branch_labels = None
depends_on = None


def _column_exists(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return column_name in {col['name'] for col in inspector.get_columns(table_name)}


def upgrade():
    if not _column_exists('perf_test_scenarios', 'last_result'):
        with op.batch_alter_table('perf_test_scenarios', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('last_result', sa.JSON(), nullable=True, comment='鏈€鍚庢墽琛岀粨鏋?')
            )

    if not _column_exists('web_test_scripts', 'last_result'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('last_result', sa.JSON(), nullable=True, comment='鏈€鍚庢墽琛岀粨鏋?')
            )


def downgrade():
    if _column_exists('web_test_scripts', 'last_result'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.drop_column('last_result')

    if _column_exists('perf_test_scenarios', 'last_result'):
        with op.batch_alter_table('perf_test_scenarios', schema=None) as batch_op:
            batch_op.drop_column('last_result')
