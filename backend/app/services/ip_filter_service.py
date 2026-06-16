"""
IP 白名单过滤服务

提供组织级和 Token 级 IP 白名单控制。
"""

import ipaddress
from typing import List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)


class IPFilterService:
    """IP 白名单过滤服务"""

    def is_ip_allowed(self, client_ip: str, whitelist: List[str]) -> bool:
        """
        检查 IP 是否在白名单中

        Args:
            client_ip: 客户端 IP
            whitelist: 白名单列表（支持 IP 和 CIDR）

        Returns:
            bool: 是否允许
        """
        if not whitelist:
            return True  # 空白名单不限制

        try:
            addr = ipaddress.ip_address(client_ip)
        except ValueError:
            logger.warning("无效的 IP 地址", ip=client_ip)
            return False

        for entry in whitelist:
            try:
                if "/" in entry:
                    network = ipaddress.ip_network(entry, strict=False)
                    if addr in network:
                        return True
                else:
                    if addr == ipaddress.ip_address(entry):
                        return True
            except ValueError:
                logger.warning("无效的白名单条目", entry=entry)
                continue
        return False

    def validate_whitelist(self, whitelist: List[str]) -> List[str]:
        """验证白名单格式，返回无效条目"""
        invalid = []
        for entry in whitelist:
            try:
                if "/" in entry:
                    ipaddress.ip_network(entry, strict=False)
                else:
                    ipaddress.ip_address(entry)
            except ValueError:
                invalid.append(entry)
        return invalid


_instance = None


def get_ip_filter_service():
    global _instance
    if _instance is None: _instance = IPFilterService()
    return _instance
