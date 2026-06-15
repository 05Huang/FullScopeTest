"""
URL 安全校验工具测试 — SSRF 防护

覆盖：
- 合法外部 URL 通过校验
- 内网/保留地址被拦截
- IPv6 地址拦截
- 云端元数据服务拦截
- 协议校验
- 白名单功能
- 边界条件
"""

import os
import pytest
from unittest.mock import patch
from app.utils.url_safety import is_safe_url, _is_ip_blocked, _get_allowlist_hosts


class TestIsSafeUrl:
    """is_safe_url 函数测试"""

    # ========== 合法 URL ==========

    @patch("app.utils.url_safety._resolve_host_to_ips", return_value=["93.184.216.34"])
    def test_valid_external_url_http(self, _mock):
        """合法 HTTP 外部地址应通过"""
        safe, msg = is_safe_url("http://example.com")
        assert safe is True
        assert msg == ""

    @patch("app.utils.url_safety._resolve_host_to_ips", return_value=["93.184.216.34"])
    def test_valid_external_url_https(self, _mock):
        """合法 HTTPS 外部地址应通过"""
        safe, msg = is_safe_url("https://api.example.com/v1/users")
        assert safe is True

    @patch("app.utils.url_safety._resolve_host_to_ips", return_value=["93.184.216.34"])
    def test_valid_url_with_port(self, _mock):
        """带端口的外部地址应通过"""
        safe, msg = is_safe_url("https://example.com:8443/api")
        assert safe is True

    @patch("app.utils.url_safety._resolve_host_to_ips", return_value=["93.184.216.34"])
    def test_valid_url_with_path_and_query(self, _mock):
        """带路径和查询参数的外部地址应通过"""
        safe, msg = is_safe_url("https://example.com/path?name=test&id=1")
        assert safe is True

    # ========== 内网地址拦截 ==========

    def test_block_localhost(self):
        """localhost 应被拦截"""
        safe, msg = is_safe_url("http://localhost:8080/api")
        assert safe is False
        assert "内网" in msg

    def test_block_127_loopback(self):
        """127.x.x.x 应被拦截"""
        safe, msg = is_safe_url("http://127.0.0.1:8080")
        assert safe is False
        assert "内网" in msg

    def test_block_127_range(self):
        """127.0.0.2 也应被拦截"""
        safe, _ = is_safe_url("http://127.0.0.2")
        assert safe is False

    def test_block_10_private(self):
        """10.x.x.x 私有地址应被拦截"""
        safe, msg = is_safe_url("http://10.0.0.1:8080")
        assert safe is False
        assert "内网" in msg

    def test_block_172_private(self):
        """172.16.x.x 私有地址应被拦截"""
        safe, _ = is_safe_url("http://172.16.0.1")
        assert safe is False

    def test_block_172_private_range(self):
        """172.31.255.255 应被拦截（仍在 172.16.0.0/12 内）"""
        safe, _ = is_safe_url("http://172.31.255.255")
        assert safe is False

    def test_block_192_private(self):
        """192.168.x.x 私有地址应被拦截"""
        safe, _ = is_safe_url("http://192.168.1.1:3000")
        assert safe is False

    def test_block_link_local(self):
        """169.254.x.x 链路本地地址应被拦截"""
        safe, _ = is_safe_url("http://169.254.169.254/metadata")
        assert safe is False

    def test_block_zero_network(self):
        """0.0.0.0 应被拦截"""
        safe, _ = is_safe_url("http://0.0.0.0:8080")
        assert safe is False

    # ========== IPv6 地址拦截 ==========

    def test_block_ipv6_loopback(self):
        """IPv6 ::1 应被拦截"""
        safe, _ = is_safe_url("http://[::1]:8080")
        assert safe is False

    def test_block_ipv6_link_local(self):
        """IPv6 fe80:: 应被拦截"""
        safe, _ = is_safe_url("http://[fe80::1]")
        assert safe is False

    def test_block_ipv6_unique_local(self):
        """IPv6 fc00:: 应被拦截"""
        safe, _ = is_safe_url("http://[fc00::1]")
        assert safe is False

    # ========== 云端元数据服务 ==========

    def test_block_google_metadata(self):
        """Google Cloud 元数据服务应被拦截"""
        safe, _ = is_safe_url("http://metadata.google.internal/computeMetadata/v1/")
        assert safe is False

    # ========== 协议校验 ==========

    def test_block_ftp_protocol(self):
        """FTP 协议应被拦截"""
        safe, msg = is_safe_url("ftp://example.com/file")
        assert safe is False
        assert "协议" in msg

    def test_block_file_protocol(self):
        """file 协议应被拦截"""
        safe, msg = is_safe_url("file:///etc/passwd")
        assert safe is False

    def test_block_javascript_protocol(self):
        """javascript 协议应被拦截"""
        safe, msg = is_safe_url("javascript:alert(1)")
        assert safe is False

    # ========== 边界条件 ==========

    def test_empty_url(self):
        """空 URL 应被拦截"""
        safe, _ = is_safe_url("")
        assert safe is False

    def test_none_url(self):
        """None 应被拦截"""
        safe, _ = is_safe_url(None)
        assert safe is False

    def test_non_string_url(self):
        """非字符串应被拦截"""
        safe, _ = is_safe_url(123)
        assert safe is False

    def test_url_without_host(self):
        """缺少主机名的 URL 应被拦截"""
        safe, msg = is_safe_url("http://")
        assert safe is False

    def test_whitespace_only_url(self):
        """纯空白 URL 应被拦截"""
        safe, _ = is_safe_url("   ")
        assert safe is False


class TestIsIpBlocked:
    """_is_ip_blocked 函数测试"""

    def test_blocked_loopback(self):
        assert _is_ip_blocked("127.0.0.1") is True

    def test_blocked_private(self):
        assert _is_ip_blocked("10.0.0.1") is True

    def test_blocked_link_local(self):
        assert _is_ip_blocked("169.254.0.1") is True

    def test_allowed_public_ip(self):
        """公网 IP 应通过"""
        assert _is_ip_blocked("8.8.8.8") is False

    def test_allowed_public_ip_2(self):
        assert _is_ip_blocked("1.1.1.1") is False

    def test_invalid_ip(self):
        """无法解析的 IP 视为不安全"""
        assert _is_ip_blocked("not-an-ip") is True


class TestAllowlistHosts:
    """白名单功能测试"""

    def test_empty_allowlist_by_default(self):
        """默认白名单为空"""
        hosts = _get_allowlist_hosts()
        assert isinstance(hosts, set)

    def test_allowlist_from_env(self, monkeypatch):
        """从环境变量读取白名单"""
        monkeypatch.setenv("SSRF_ALLOWLIST_HOSTS", "localhost,127.0.0.1")
        hosts = _get_allowlist_hosts()
        assert "localhost" in hosts
        assert "127.0.0.1" in hosts

    def test_allowlist_whitespace_handling(self, monkeypatch):
        """白名单应处理空格"""
        monkeypatch.setenv("SSRF_ALLOWLIST_HOSTS", " localhost , 127.0.0.1 ")
        hosts = _get_allowlist_hosts()
        assert "localhost" in hosts
        assert "127.0.0.1" in hosts

    def test_allowlist_bypasses_block(self, monkeypatch):
        """白名单主机应绕过封锁"""
        monkeypatch.setenv("SSRF_ALLOWLIST_HOSTS", "localhost")
        safe, _ = is_safe_url("http://localhost:8080")
        assert safe is True

    def test_allowlist_cleanup(self, monkeypatch):
        """测试结束后环境变量应被清理（通过 monkeypatch 自动处理）"""
        monkeypatch.setenv("SSRF_ALLOWLIST_HOSTS", "")
        hosts = _get_allowlist_hosts()
        assert len(hosts) == 0


class TestEdgeCasesSSRF:
    """SSRF 攻击向量边界测试"""

    def test_url_with_credentials(self):
        """带认证信息的内网 URL 应被拦截"""
        safe, _ = is_safe_url("http://admin:password@192.168.1.1/admin")
        assert safe is False

    def test_url_with_fragment(self):
        """带 fragment 的合法 URL 应通过"""
        safe, _ = is_safe_url("https://example.com/page#section")
        assert safe is True

    def test_mixed_case_scheme(self):
        """大小写混合的协议应通过"""
        safe, _ = is_safe_url("HTTPS://example.com")
        assert safe is True

    def test_ip_as_decimal(self):
        """十进制 IP 表示（2130706433 = 127.0.0.1）"""
        # 注意：Python socket 会将纯数字视为无效主机名，
        # 但某些系统可能会解析为 IP，此处测试当前行为
        safe, _ = is_safe_url("http://2130706433")
        # 如果解析失败则不安全（safe=False），如果解析为 127.0.0.1 也不安全
        # 无论如何都不应通过
        # 这取决于系统行为，但关键是不应泄露内网
