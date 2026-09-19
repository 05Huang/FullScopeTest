"""
访客统计模型

记录网站访客的详细行为数据
"""

from datetime import datetime, timezone, timedelta
from ..extensions import db


class VisitorStat(db.Model):
    """访客统计表"""

    __tablename__ = 'visitor_stats'
    __table_args__ = (
        db.Index('idx_visitor_session', 'session_id'),
        db.Index('idx_visitor_first_visit', 'first_visit'),
        db.Index('idx_visitor_last_active', 'last_active'),
        db.Index('idx_visitor_ip_hash', 'ip_hash'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # 会话标识
    session_id = db.Column(db.String(64), unique=True, nullable=False, comment='唯一会话标识')

    # IP 信息
    ip_hash = db.Column(db.String(64), comment='IP 哈希值（隐私保护）')
    ip_address = db.Column(db.String(45), comment='IP 地址（仅管理员可见）')
    ip_country = db.Column(db.String(50), comment='IP 国家')
    ip_city = db.Column(db.String(100), comment='IP 城市')
    ip_isp = db.Column(db.String(100), comment='ISP 运营商')

    # 时间统计
    first_visit = db.Column(db.DateTime, default=datetime.utcnow, comment='首次访问时间')
    last_active = db.Column(db.DateTime, default=datetime.utcnow, comment='最后活跃时间')
    total_duration = db.Column(db.Integer, default=0, comment='总停留时长（秒）')

    # 页面统计
    page_views = db.Column(db.Integer, default=0, comment='页面浏览数')

    # 设备信息
    device_type = db.Column(db.String(20), comment='设备类型: desktop/mobile/tablet')
    browser = db.Column(db.String(50), comment='浏览器')
    browser_version = db.Column(db.String(30), comment='浏览器版本')
    os = db.Column(db.String(50), comment='操作系统')
    os_version = db.Column(db.String(30), comment='操作系统版本')

    # 屏幕信息
    screen_width = db.Column(db.Integer, comment='屏幕宽度')
    screen_height = db.Column(db.Integer, comment='屏幕高度')

    # 来源信息
    referrer = db.Column(db.Text, comment='来源页面')
    entry_page = db.Column(db.String(255), comment='入口页面')

    # 访问详情（JSON 存储每个页面的停留时间）
    visited_pages = db.Column(db.JSON, default=list, comment='访问页面详情 [{path, duration}]')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    def to_dict(self, include_ip=False):
        """转换为字典"""
        # 将 UTC 时间转换为带时区信息的 ISO 格式，前端可正确显示
        def format_datetime(dt):
            if dt is None:
                return None
            # 确保返回带 UTC 时区标记的 ISO 格式
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()

        result = {
            'id': self.id,
            'session_id': self.session_id,
            'ip_country': self.ip_country,
            'ip_city': self.ip_city,
            'ip_isp': self.ip_isp,
            'first_visit': format_datetime(self.first_visit),
            'last_active': format_datetime(self.last_active),
            'total_duration': self.total_duration,
            'page_views': self.page_views,
            'device_type': self.device_type,
            'browser': self.browser,
            'browser_version': self.browser_version,
            'os': self.os,
            'os_version': self.os_version,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'referrer': self.referrer,
            'entry_page': self.entry_page,
            'visited_pages': self.visited_pages or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        # 仅当明确请求时返回 IP 地址
        if include_ip:
            result['ip_address'] = self.ip_address
        return result

    def __repr__(self):
        return f'<VisitorStat {self.session_id[:8]}...>'
