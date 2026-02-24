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


def upgrade():
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

    with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('collection_id', sa.Integer(), nullable=True, comment='Collection ID'))
        batch_op.create_foreign_key(
            'fk_web_test_scripts_collection_id',
            'web_test_collections',
            ['collection_id'],
            ['id'],
        )


def downgrade():
    with op.batch_alter_table('web_test_scripts', schema=None) as batch_op:
        batch_op.drop_constraint('fk_web_test_scripts_collection_id', type_='foreignkey')
        batch_op.drop_column('collection_id')

    op.drop_table('web_test_collections')
