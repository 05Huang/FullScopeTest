"""add test report features

Revision ID: add_test_report_features
Revises: 5ca026f04416
Create Date: 2025-12-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_test_report_features'
down_revision = '5ca026f04416'
branch_labels = None
depends_on = None


def _table_exists(table_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return table_name in inspector.get_table_names()


def _column_exists(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return column_name in {col['name'] for col in inspector.get_columns(table_name)}


def upgrade():
    if not _table_exists('test_reports'):
        op.create_table(
            'test_reports',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('test_run_id', sa.Integer(), nullable=False, comment='娴嬭瘯鎵ц璁板綍ID'),
            sa.Column('project_id', sa.Integer(), nullable=False, comment='椤圭洰ID'),
            sa.Column('test_type', sa.String(length=20), nullable=False, comment='娴嬭瘯绫诲瀷: api/web/performance'),
            sa.Column('title', sa.String(length=255), nullable=False, comment='鎶ュ憡鏍囬'),
            sa.Column('summary', sa.JSON(), nullable=True, comment='鎶ュ憡鎽樿'),
            sa.Column('report_data', sa.JSON(), nullable=True, comment='璇︾粏鎶ュ憡鏁版嵁'),
            sa.Column('report_html', sa.Text(), nullable=True, comment='HTML鎶ュ憡鍐呭'),
            sa.Column('status', sa.String(length=20), nullable=True, comment='鎶ュ憡鐘舵€?'),
            sa.Column('created_at', sa.DateTime(), nullable=True, comment='鍒涘缓鏃堕棿'),
            sa.Column('updated_at', sa.DateTime(), nullable=True, comment='鏇存柊鏃堕棿'),
            sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
            sa.ForeignKeyConstraint(['test_run_id'], ['test_runs.id']),
            sa.PrimaryKeyConstraint('id'),
            comment='娴嬭瘯鎶ュ憡琛?'
        )

    if not _column_exists('test_runs', 'report_id'):
        op.add_column(
            'test_runs',
            sa.Column('report_id', sa.Integer(), nullable=True, comment='鍏宠仈鎶ュ憡ID')
        )


def downgrade():
    if _column_exists('test_runs', 'report_id'):
        op.drop_column('test_runs', 'report_id')
    if _table_exists('test_reports'):
        op.drop_table('test_reports')
