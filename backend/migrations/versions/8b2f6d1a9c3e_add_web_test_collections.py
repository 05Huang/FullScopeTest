"""add web test collections

Revision ID: 8b2f6d1a9c3e
Revises: add_test_report_features
Create Date: 2026-03-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b2f6d1a9c3e'
down_revision = 'add_test_report_features'
branch_labels = None
depends_on = None


def _table_exists(table_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return table_name in inspector.get_table_names()


def _column_exists(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return column_name in {col['name'] for col in inspector.get_columns(table_name)}


def _fk_exists(table_name: str, fk_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return fk_name in {fk['name'] for fk in inspector.get_foreign_keys(table_name)}


def upgrade():
    if not _table_exists('web_test_collections'):
        op.create_table(
            'web_test_collections',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('project_id', sa.Integer(), nullable=True, comment='Project ID'),
            sa.Column('user_id', sa.Integer(), nullable=False, comment='User ID'),
            sa.Column('name', sa.String(length=100), nullable=False, comment='Collection name'),
            sa.Column('description', sa.Text(), nullable=True, comment='Collection description'),
            sa.Column('sort_order', sa.Integer(), nullable=True, comment='Sort order'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
            sa.ForeignKeyConstraint(['user_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id'),
        )

    if not _column_exists('web_test_scripts', 'collection_id'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('collection_id', sa.Integer(), nullable=True, comment='Collection ID')
            )

    if not _fk_exists('web_test_scripts', 'fk_web_test_scripts_collection_id'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.create_foreign_key(
                'fk_web_test_scripts_collection_id',
                'web_test_collections',
                ['collection_id'],
                ['id'],
            )


def downgrade():
    if _fk_exists('web_test_scripts', 'fk_web_test_scripts_collection_id'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.drop_constraint('fk_web_test_scripts_collection_id', type_='foreignkey')

    if _column_exists('web_test_scripts', 'collection_id'):
        with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
            batch_op.drop_column('collection_id')

    if _table_exists('web_test_collections'):
        op.drop_table('web_test_collections')
