"""
URL 安全校验工具 — SSRF 防护

在向用户指定的 URL 发起 HTTP 请求前，校验目标地址是否属于内网/保留地址段，
防止多租户 SaaS 场景下的 SSRF 攻击。
"""

import ipaddress
import os
import socket
from urllib.parse import urlparse

from ..core.logging import get_logger

logger = get_logger(__name__)

# 内网/保留 IP 地址段（黑名单）
BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),       # Loopback
    ipaddress.ip_network("10.0.0.0/8"),         # Private Class A
    ipaddress.ip_network("172.16.0.0/12"),      # Private Class B
    ipaddress.ip_network("192.168.0.0/16"),     # Private Class C
    ipaddress.ip_network("169.254.0.0/16"),     # Link-local
    ipaddress.ip_network("0.0.0.0/8"),          # Current network
    ipaddress.ip_network("100.64.0.0/10"),      # Carrier-grade NAT
    ipaddress.ip_network("192.0.0.0/24"),       # IETF Protocol Assignments
    ipaddress.ip_network("192.0.2.0/24"),       # TEST-NET-1
    ipaddress.ip_network("198.51.100.0/24"),    # TEST-NET-2
    ipaddress.ip_network("203.0.113.0/24"),     # TEST-NET-3
    ipaddress.ip_network("224.0.0.0/4"),        # Multicast
    ipaddress.ip_network("240.0.0.0/4"),        # Reserved
    ipaddress.ip_network("255.255.255.255/32"), # Broadcast
    # IPv6
    ipaddress.ip_network("::1/128"),            # IPv6 Loopback
    ipaddress.ip_network("fc00::/7"),           # IPv6 Unique Local
    ipaddress.ip_network("fe80::/10"),          # IPv6 Link-local
    ipaddress.ip_network("ff00::/8"),           # IPv6 Multicast
    ipaddress.ip_network("::ffff:127.0.0.0/104"),  # IPv4-mapped IPv6 loopback
    ipaddress.ip_network("::ffff:10.0.0.0/104"),   # IPv4-mapped IPv6 private
    ipaddress.ip_network("::ffff:172.16.0.0/108"),  # IPv4-mapped IPv6 private
    ipaddress.ip_network("::ffff:192.168.0.0/112"), # IPv4-mapped IPv6 private
]

# 云端元数据服务地址
BLOCKED_HOSTS = {
    "metadata.google.internal",
    "metadata.goog",
    "instance-data",
    "169.254.169.254",
}


def _get_allowlist_hosts() -> set:
    """
    从环境变量获取白名单主机列表

    环境变量 SSRF_ALLOWLIST_HOSTS 格式：逗号分隔的主机名
    例如：SSRF_ALLOWLIST_HOSTS=localhost,127.0.0.1
    """
    raw = os.environ.get("SSRF_ALLOWLIST_HOSTS", "")
    if not raw:
        return set()
    return {h.strip().lower() for h in raw.split(",") if h.strip()}


def _resolve_host_to_ips(host: str) -> list:
    """
    将主机名解析为 IP 地址列表

    Args:
        host: 主机名或 IP 地址

    Returns:
        IP 地址字符串列表
    """
    try:
        # 先尝试直接解析为 IP 地址
        try:
            addr = ipaddress.ip_address(host)
            return [str(addr)]
        except ValueError:
            pass

        # DNS 解析
        results = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        ips = []
        seen = set()
        for family, _, _, _, sockaddr in results:
            ip_str = sockaddr[0]
            if ip_str not in seen:
                seen.add(ip_str)
                ips.append(ip_str)
        return ips
    except (socket.gaierror, OSError) as e:
        logger.warning("DNS 解析失败", host=host, error=str(e))
        return []


def _is_ip_blocked(ip_str: str) -> bool:
    """
    检查 IP 地址是否属于被封锁的网段

    Args:
        ip_str: IP 地址字符串

    Returns:
        True 表示应被封锁
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        for network in BLOCKED_NETWORKS:
            if ip in network:
                return True
        return False
    except ValueError:
        return True  # 无法解析的 IP 视为不安全


def is_safe_url(url: str) -> tuple:
    """
    校验 URL 是否安全（非 SSRF 目标）

    Args:
        url: 用户输入的完整 URL

    Returns:
        (is_safe, message):
            - (True, "") 表示安全
            - (False, "错误信息") 表示不安全
    """
    if not url or not isinstance(url, str):
        return False, "URL 不能为空"

    url = url.strip()

    # 解析 URL
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "URL 格式无效"

    # 仅允许 HTTP/HTTPS 协议
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        return False, f"不支持的协议: {scheme}，仅允许 http/https"

    host = parsed.hostname
    if not host:
        return False, "URL 缺少主机名"

    host_lower = host.lower()

    # 检查白名单
    allowlist = _get_allowlist_hosts()
    if host_lower in allowlist:
        logger.info("URL 通过白名单校验", host=host_lower)
        return True, ""

    # 检查明确封锁的主机名
    if host_lower in BLOCKED_HOSTS:
        logger.warning("SSRF 拦截：命中主机黑名单", host=host_lower, url=url)
        return False, "目标地址不允许访问内网资源"

    # 解析主机名对应的 IP 地址
    ips = _resolve_host_to_ips(host)
    if not ips:
        return False, f"无法解析主机名: {host}"

    # 逐一检查解析出的 IP
    for ip_str in ips:
        if _is_ip_blocked(ip_str):
            logger.warning(
                "SSRF 拦截：目标解析为内网地址",
                host=host, resolved_ip=ip_str, url=url
            )
            return False, "目标地址不允许访问内网资源"

    return True, ""
