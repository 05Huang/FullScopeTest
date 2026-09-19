"""访客统计数据收集

Revision ID: visitor_stats_v1
Revises:
Create Date: 2024-09-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'visitor_stats_v1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'visitor_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=64), nullable=False, comment='唯一会话标识'),
        sa.Column('ip_hash', sa.String(length=64), nullable=True, comment='IP 哈希值（隐私保护）'),
        sa.Column('ip_country', sa.String(length=50), nullable=True, comment='IP 国家'),
        sa.Column('ip_city', sa.String(length=100), nullable=True, comment='IP 城市'),
        sa.Column('ip_isp', sa.String(length=100), nullable=True, comment='ISP 运营商'),
        sa.Column('first_visit', sa.DateTime(), nullable=True, comment='首次访问时间'),
        sa.Column('last_active', sa.DateTime(), nullable=True, comment='最后活跃时间'),
        sa.Column('total_duration', sa.Integer(), nullable=True, comment='总停留时长（秒）'),
        sa.Column('page_views', sa.Integer(), nullable=True, comment='页面浏览数'),
        sa.Column('device_type', sa.String(length=20), nullable=True, comment='设备类型'),
        sa.Column('browser', sa.String(length=50), nullable=True, comment='浏览器'),
        sa.Column('browser_version', sa.String(length=30), nullable=True, comment='浏览器版本'),
        sa.Column('os', sa.String(length=50), nullable=True, comment='操作系统'),
        sa.Column('os_version', sa.String(length=30), nullable=True, comment='操作系统版本'),
        sa.Column('screen_width', sa.Integer(), nullable=True, comment='屏幕宽度'),
        sa.Column('screen_height', sa.Integer(), nullable=True, comment='屏幕高度'),
        sa.Column('referrer', sa.Text(), nullable=True, comment='来源页面'),
        sa.Column('entry_page', sa.String(length=255), nullable=True, comment='入口页面'),
        sa.Column('visited_pages', sa.JSON(), nullable=True, comment='访问页面详情'),
        sa.Column('created_at', sa.DateTime(), nullable=True, comment='创建时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )
    op.create_index('idx_visitor_session', 'visitor_stats', ['session_id'])
    op.create_index('idx_visitor_first_visit', 'visitor_stats', ['first_visit'])
    op.create_index('idx_visitor_last_active', 'visitor_stats', ['last_active'])
    op.create_index('idx_visitor_ip_hash', 'visitor_stats', ['ip_hash'])


def downgrade():
    op.drop_index('idx_visitor_ip_hash')
    op.drop_index('idx_visitor_last_active')
    op.drop_index('idx_visitor_first_visit')
    op.drop_index('idx_visitor_session')
    op.drop_table('visitor_stats')
