"""add test report features

Revision ID: add_test_report_features
Revises: 5ca026f04416
Create Date: 2025-12-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'add_test_report_features'
down_revision = '5ca026f04416'
branch_labels = None
depends_on = None


def upgrade():
    # 创建测试报告表
    op.create_table('test_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_run_id', sa.Integer(), nullable=False, comment='测试执行记录ID'),
        sa.Column('project_id', sa.Integer(), nullable=False, comment='项目ID'),
        sa.Column('test_type', sa.String(length=20), nullable=False, comment='测试类型: api/web/performance'),
        sa.Column('title', sa.String(length=255), nullable=False, comment='报告标题'),
        sa.Column('summary', sa.JSON(), nullable=True, comment='报告摘要'),
        sa.Column('report_data', sa.JSON(), nullable=True, comment='详细报告数据'),
        sa.Column('report_html', sa.Text(), nullable=True, comment='HTML报告内容'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='报告状态'),
        sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['test_run_id'], ['test_runs.id'], ),
        sa.PrimaryKeyConstraint('id'),
        comment='测试报告表'
    )
    
    # 为 test_runs 表添加 report_id 字段
    op.add_column('test_runs', sa.Column('report_id', sa.Integer(), nullable=True, comment='关联报告ID'))


def downgrade():
    op.drop_column('test_runs', 'report_id')
    op.drop_table('test_reports')
