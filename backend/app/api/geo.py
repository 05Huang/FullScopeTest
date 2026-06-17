"""
地理位置检测 API

通过客户端 IP 检测用户所在地区，用于演示系统智能语言切换提示。
使用免费 ip-api.com 服务，无需 API Key。
"""

import urllib.request
import json
from flask import Blueprint, jsonify, request
from app.core.logging import get_logger

logger = get_logger(__name__)
geo_bp = Blueprint('geo', __name__)

# ip-api.com 免费 API（每分钟 45 次限制，演示系统够用）
IP_API_URL = 'http://ip-api.com/json/{ip}?fields=country,countryCode,timezone,status'


def _get_client_ip():
    """获取客户端真实 IP（支持反向代理）"""
    # 优先从 X-Forwarded-For 获取（OpenResty 反向代理）
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    # 其次从 X-Real-IP 获取
    xri = request.headers.get('X-Real-IP', '')
    if xri:
        return xri.strip()
    return request.remote_addr or '127.0.0.1'


def _detect_country(ip: str) -> dict:
    """调用 ip-api.com 检测 IP 所属国家"""
    try:
        url = IP_API_URL.format(ip=ip)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'FullScopeTest/1.0',
        })
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', ''),
                    'country_code': data.get('countryCode', ''),
                    'timezone': data.get('timezone', ''),
                }
    except Exception as e:
        logger.warning('Geo detection failed', ip=ip, error=str(e))
    return {}


@geo_bp.route('/api/v1/geo/detect', methods=['GET'])
def detect_region():
    """
    检测客户端所在地区

    返回格式:
    {
        "code": 200,
        "data": {
            "country": "United States",
            "country_code": "US",
            "timezone": "America/New_York",
            "is_china": false
        }
    }
    """
    client_ip = _get_client_ip()

    # 本地/内网 IP 直接返回中国
    if client_ip in ('127.0.0.1', '::1', 'localhost') or client_ip.startswith('192.168.') or client_ip.startswith('10.'):
        return jsonify({
            'code': 200,
            'data': {
                'country': 'China',
                'country_code': 'CN',
                'timezone': 'Asia/Shanghai',
                'is_china': True,
            }
        })

    geo = _detect_country(client_ip)
    is_china = geo.get('country_code') == 'CN' if geo else True

    return jsonify({
        'code': 200,
        'data': {
            **geo,
            'is_china': is_china,
        }
    })
