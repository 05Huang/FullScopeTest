"""
访客统计 API 接口模块

提供访客数据的采集、查询和统计功能。
"""

import hashlib
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func as sa_func, text

from . import api_bp
from ..extensions import db
from ..models.visitor_stat import VisitorStat
from ..utils.response import success_response, error_response
from ..core.logging import get_logger

logger = get_logger(__name__)

# ip-api.com 免费 API（每分钟 45 次限制）
IP_API_URL = 'http://ip-api.com/json/{ip}?fields=status,country,countryCode,city,isp,org,query'

# 上海时区
SHANGHAI_TZ = timezone(timedelta(hours=8))


def _get_client_ip():
    """获取客户端真实 IP"""
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    xri = request.headers.get('X-Real-IP', '')
    if xri:
        return xri.strip()
    return request.remote_addr or '127.0.0.1'


def _hash_ip(ip: str) -> str:
    """对 IP 进行哈希处理（保护隐私）"""
    return hashlib.sha256(ip.encode()).hexdigest()[:64]


def _detect_geo(ip: str) -> dict:
    """调用 ip-api.com 检测 IP 归属地"""
    # 跳过本地/内网 IP
    if ip in ('127.0.0.1', '::1', 'localhost') or ip.startswith(('192.168.', '10.', '172.')):
        return {'country': 'Local', 'city': 'Local', 'isp': 'Local'}

    try:
        url = IP_API_URL.format(ip=ip)
        req = urllib.request.Request(url, headers={'User-Agent': 'FullScopeTest/1.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', ''),
                    'city': data.get('city', ''),
                    'isp': data.get('org', '') or data.get('isp', ''),
                }
    except Exception as e:
        logger.warning('Geo detection failed', ip=ip[:10], error=str(e))
    return {}


def _parse_user_agent(ua: str) -> dict:
    """解析 User-Agent 获取设备信息"""
    device_type = 'desktop'
    browser = 'Unknown'
    browser_version = ''
    os = 'Unknown'
    os_version = ''

    ua_lower = ua.lower()

    # 检测设备类型
    if any(x in ua_lower for x in ['mobile', 'android', 'iphone', 'ipad', 'tablet']):
        if 'ipad' in ua_lower or 'tablet' in ua_lower:
            device_type = 'tablet'
        else:
            device_type = 'mobile'

    # 检测浏览器
    if 'edg/' in ua_lower or 'edge/' in ua_lower:
        browser = 'Edge'
        browser_version = ua.split('Edg/')[-1].split('.')[0] if 'Edg/' in ua else ''
    elif 'chrome/' in ua_lower and 'safari/' in ua_lower:
        browser = 'Chrome'
        browser_version = ua.split('Chrome/')[-1].split('.')[0] if 'Chrome/' in ua else ''
    elif 'firefox/' in ua_lower:
        browser = 'Firefox'
        browser_version = ua.split('Firefox/')[-1].split('.')[0] if 'Firefox/' in ua else ''
    elif 'safari/' in ua_lower and 'chrome/' not in ua_lower:
        browser = 'Safari'
        browser_version = ua.split('Version/')[-1].split('.')[0] if 'Version/' in ua else ''
    elif 'msie' in ua_lower or 'trident/' in ua_lower:
        browser = 'IE'
    elif 'opera' in ua_lower or 'opr/' in ua_lower:
        browser = 'Opera'

    # 检测操作系统
    if 'windows nt 10' in ua_lower:
        os = 'Windows'
        os_version = '10/11'
    elif 'windows nt' in ua_lower:
        os = 'Windows'
        os_version = 'Older'
    elif 'mac os x' in ua_lower:
        os = 'macOS'
        version = ua.split('Mac OS X ')[-1].split(')')[0].replace('_', '.') if 'Mac OS X ' in ua else ''
        os_version = version.split('.')[0] if version else ''
    elif 'android' in ua_lower:
        os = 'Android'
        version = ua.split('Android ')[-1].split(';')[0].strip() if 'Android ' in ua else ''
        os_version = version
    elif 'iphone' in ua_lower or 'ipad' in ua_lower:
        os = 'iOS'
        version = ua.split('OS ')[-1].split(' ')[0].replace('_', '.') if 'OS ' in ua else ''
        os_version = version
    elif 'linux' in ua_lower:
        os = 'Linux'

    return {
        'device_type': device_type,
        'browser': browser,
        'browser_version': browser_version,
        'os': os,
        'os_version': os_version,
    }


@api_bp.route('/visitor/track', methods=['POST'])
def track_visitor():
    """
    记录访客数据

    请求体:
    {
        "session_id": "xxx",
        "page_views": 5,
        "total_duration": 120,
        "current_page": "/dashboard",
        "page_duration": 30,
        "screen_width": 1920,
        "screen_height": 1080,
        "referrer": "https://google.com",
    }
    """
    try:
        data = request.get_json() or {}
    except Exception:
        return error_response(400, '无效的 JSON 数据')

    session_id = data.get('session_id')
    if not session_id:
        return error_response(400, '缺少 session_id')

    client_ip = _get_client_ip()
    user_agent = request.headers.get('User-Agent', '')
    geo = _detect_geo(client_ip)
    device_info = _parse_user_agent(user_agent)

    # 查找或创建访客记录
    visitor = VisitorStat.query.filter_by(session_id=session_id).first()

    if visitor:
        # 更新现有记录
        visitor.last_active = datetime.now(SHANGHAI_TZ)
        visitor.total_duration = (visitor.total_duration or 0) + data.get('page_duration', 0)
        visitor.page_views = (visitor.page_views or 0) + 1

        # 更新访问页面详情
        visited_pages = visitor.visited_pages or []
        current_page = data.get('current_page', '')
        page_duration = data.get('page_duration', 0)

        # 合并相同页面的停留时间
        found = False
        for page in visited_pages:
            if page.get('path') == current_page:
                page['duration'] = page.get('duration', 0) + page_duration
                page['visits'] = page.get('visits', 1) + 1
                found = True
                break

        if not found and current_page:
            visited_pages.append({
                'path': current_page,
                'duration': page_duration,
                'visits': 1,
            })

        visitor.visited_pages = visited_pages[-50:]  # 最多保留 50 条记录
    else:
        # 创建新访客记录
        visitor = VisitorStat(
            session_id=session_id,
            ip_hash=_hash_ip(client_ip),
            ip_country=geo.get('country', ''),
            ip_city=geo.get('city', ''),
            ip_isp=geo.get('isp', ''),
            device_type=device_info['device_type'],
            browser=device_info['browser'],
            browser_version=device_info['browser_version'],
            os=device_info['os'],
            os_version=device_info['os_version'],
            screen_width=data.get('screen_width'),
            screen_height=data.get('screen_height'),
            referrer=data.get('referrer', ''),
            entry_page=data.get('current_page', ''),
            page_views=1,
            total_duration=data.get('page_duration', 0),
            visited_pages=[{
                'path': data.get('current_page', ''),
                'duration': data.get('page_duration', 0),
                'visits': 1,
            }],
        )
        db.session.add(visitor)

    db.session.commit()
    return success_response(data={'tracked': True})


@api_bp.route('/visitor/stats', methods=['GET'])
def get_visitor_stats():
    """
    获取访客统计概览

    查询参数:
        days: 统计天数（默认 7）
    """
    days = request.args.get('days', 7, type=int)

    # 使用上海时区计算日期
    now_shanghai = datetime.now(SHANGHAI_TZ)
    today_start_shanghai = now_shanghai.replace(hour=0, minute=0, second=0, microsecond=0)
    since_shanghai = today_start_shanghai - timedelta(days=days - 1)

    # 转换为 UTC 时间戳用于数据库查询
    since_utc = since_shanghai.astimezone(timezone.utc).replace(tzinfo=None)
    today_start_utc = today_start_shanghai.astimezone(timezone.utc).replace(tzinfo=None)

    # 总访客数（最近 N 天）
    total_visitors = VisitorStat.query.filter(
        VisitorStat.first_visit >= since_utc
    ).count()

    # 今日访客数（上海时区当天）
    today_visitors = VisitorStat.query.filter(
        VisitorStat.first_visit >= today_start_utc
    ).count()

    # 当前在线人数（最近 5 分钟内有活动）
    online_threshold = datetime.now(SHANGHAI_TZ) - timedelta(minutes=5)
    online_visitors = VisitorStat.query.filter(
        VisitorStat.last_active >= online_threshold
    ).count()

    # 平均停留时长
    avg_duration = db.session.query(
        sa_func.avg(VisitorStat.total_duration)
    ).filter(VisitorStat.first_visit >= since_utc).scalar() or 0

    # 总页面浏览数
    total_page_views = db.session.query(
        sa_func.sum(VisitorStat.page_views)
    ).filter(VisitorStat.first_visit >= since_utc).scalar() or 0

    # 按设备类型统计
    device_stats = db.session.query(
        VisitorStat.device_type,
        sa_func.count(VisitorStat.id).label('count'),
    ).filter(VisitorStat.first_visit >= since_utc).group_by(VisitorStat.device_type).all()

    # 按浏览器统计
    browser_stats = db.session.query(
        VisitorStat.browser,
        sa_func.count(VisitorStat.id).label('count'),
    ).filter(VisitorStat.first_visit >= since_utc).group_by(VisitorStat.browser).all()

    # 按国家统计
    country_stats = db.session.query(
        VisitorStat.ip_country,
        sa_func.count(VisitorStat.id).label('count'),
    ).filter(VisitorStat.first_visit >= since_utc, VisitorStat.ip_country != '').group_by(VisitorStat.ip_country).all()

    # 最近 N 天趋势（使用上海时区日期）
    daily_stats = []
    for i in range(days):
        # 计算上海时区的日期边界
        day_date = (today_start_shanghai - timedelta(days=days - 1 - i)).date()
        day_start = datetime.combine(day_date, datetime.min.time()).replace(tzinfo=SHANGHAI_TZ)
        day_end = day_start + timedelta(days=1)

        # 转换为 UTC 用于查询
        day_start_utc = day_start.astimezone(timezone.utc).replace(tzinfo=None)
        day_end_utc = day_end.astimezone(timezone.utc).replace(tzinfo=None)

        day_visitors = VisitorStat.query.filter(
            VisitorStat.first_visit >= day_start_utc,
            VisitorStat.first_visit < day_end_utc,
        ).count()
        day_page_views = db.session.query(
            sa_func.sum(VisitorStat.page_views)
        ).filter(
            VisitorStat.first_visit >= day_start_utc,
            VisitorStat.first_visit < day_end_utc,
        ).scalar() or 0

        daily_stats.append({
            'date': day_date.strftime('%Y-%m-%d'),
            'visitors': day_visitors,
            'page_views': day_page_views,
        })

    return success_response(data={
        'period_days': days,
        'total_visitors': total_visitors,
        'today_visitors': today_visitors,
        'online_visitors': online_visitors,
        'avg_duration': int(avg_duration),
        'total_page_views': total_page_views,
        'by_device': {row.device_type or 'Unknown': row.count for row in device_stats},
        'by_browser': {row.browser or 'Unknown': row.count for row in browser_stats},
        'by_country': {row.ip_country or 'Unknown': row.count for row in country_stats},
        'daily_trend': daily_stats,
    })


@api_bp.route('/visitor/list', methods=['GET'])
@jwt_required()
def get_visitor_list():
    """
    获取访客列表（需管理员权限）

    查询参数:
        page: 页码（默认 1）
        per_page: 每页数量（默认 20）
        device_type: 按设备类型筛选
        country: 按国家筛选
    """
    current_user_id = get_jwt_identity()
    from ..models.user import User
    user = db.session.get(User, current_user_id)
    if not user or user.role != 'admin':
        return error_response(403, '需要管理员权限')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    device_type = request.args.get('device_type', '').strip()
    country = request.args.get('country', '').strip()

    query = VisitorStat.query

    if device_type:
        query = query.filter(VisitorStat.device_type == device_type)
    if country:
        query = query.filter(VisitorStat.ip_country == country)

    total = query.count()
    visitors = query.order_by(VisitorStat.last_active.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return success_response(data={
        'items': [v.to_dict() for v in visitors],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
    })


@api_bp.route('/visitor/<int:visitor_id>', methods=['GET'])
@jwt_required()
def get_visitor_detail(visitor_id):
    """获取访客详情"""
    current_user_id = get_jwt_identity()
    from ..models.user import User
    user = db.session.get(User, current_user_id)
    if not user or user.role != 'admin':
        return error_response(403, '需要管理员权限')

    visitor = VisitorStat.query.get(visitor_id)
    if not visitor:
        return error_response(404, '访客不存在')

    return success_response(data=visitor.to_dict())


@api_bp.route('/visitor/top-pages', methods=['GET'])
@jwt_required()
def get_top_pages():
    """获取最受欢迎的页面排行"""
    current_user_id = get_jwt_identity()
    from ..models.user import User
    user = db.session.get(User, current_user_id)
    if not user or user.role != 'admin':
        return error_response(403, '需要管理员权限')

    days = request.args.get('days', 7, type=int)
    limit = request.args.get('limit', 10, type=int)

    # 使用上海时区计算
    now_shanghai = datetime.now(SHANGHAI_TZ)
    today_start_shanghai = now_shanghai.replace(hour=0, minute=0, second=0, microsecond=0)
    since_shanghai = today_start_shanghai - timedelta(days=days - 1)
    since_utc = since_shanghai.astimezone(timezone.utc).replace(tzinfo=None)

    # 从 visited_pages 聚合页面访问统计
    visitors = VisitorStat.query.filter(VisitorStat.first_visit >= since_utc).all()

    page_stats = {}
    for visitor in visitors:
        for page in (visitor.visited_pages or []):
            path = page.get('path', '')
            if path:
                if path not in page_stats:
                    page_stats[path] = {'views': 0, 'duration': 0}
                page_stats[path]['views'] += page.get('visits', 1)
                page_stats[path]['duration'] += page.get('duration', 0)

    # 排序并返回 top N
    sorted_pages = sorted(page_stats.items(), key=lambda x: x[1]['views'], reverse=True)[:limit]

    return success_response(data=[
        {'path': path, 'views': stats['views'], 'avg_duration': stats['duration'] // stats['views'] if stats['views'] else 0}
        for path, stats in sorted_pages
    ])


@api_bp.route('/visitor/cleanup', methods=['POST'])
@jwt_required()
def cleanup_old_visitors():
    """清理旧访客数据（保留 90 天）"""
    current_user_id = get_jwt_identity()
    from ..models.user import User
    user = db.session.get(User, current_user_id)
    if not user or user.role != 'admin':
        return error_response(403, '需要管理员权限')

    days = request.args.get('days', 90, type=int)

    # 使用上海时区计算
    now_shanghai = datetime.now(SHANGHAI_TZ)
    today_start_shanghai = now_shanghai.replace(hour=0, minute=0, second=0, microsecond=0)
    threshold_shanghai = today_start_shanghai - timedelta(days=days)
    threshold_utc = threshold_shanghai.astimezone(timezone.utc).replace(tzinfo=None)

    deleted = VisitorStat.query.filter(VisitorStat.first_visit < threshold_utc).delete()
    db.session.commit()

    return success_response(data={'deleted': deleted})
