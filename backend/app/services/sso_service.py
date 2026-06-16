"""
SSO 单点登录服务

提供 SSO 服务基类、OIDC 和 LDAP Provider 实现。
支持环境变量配置，自动创建/关联本地用户。
"""
import os
import json
import time
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlencode

import requests
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models.user import User
from ..core.logging import get_logger

logger = get_logger(__name__)


class SSOProvider(ABC):
    """SSO Provider 抽象基类"""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供商标识"""
        ...

    @abstractmethod
    def get_login_url(self, redirect_uri: str, state: str) -> str:
        """获取登录跳转 URL"""
        ...

    @abstractmethod
    def handle_callback(self, code: str, redirect_uri: str) -> Optional[dict]:
        """
        处理回调，返回用户信息字典

        返回:
            {
                'sso_id': str,         # 提供商中的用户唯一标识
                'username': str,        # 用户名
                'email': str,           # 邮箱
                'display_name': str,    # 显示名
                'avatar': str,          # 头像 URL
                'metadata': dict,       # 额外元数据
            }
        """
        ...

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return True


class OIDCProvider(SSOProvider):
    """
    OIDC (OpenID Connect) Provider

    环境变量:
        OIDC_ISSUER_URL: OIDC Provider 的 Issuer URL
        OIDC_CLIENT_ID: Client ID
        OIDC_CLIENT_SECRET: Client Secret
        OIDC_SCOPES: 请求的 Scopes（默认 'openid email profile'）
    """

    provider_name = 'oidc'

    def __init__(self):
        self.issuer_url = os.environ.get('OIDC_ISSUER_URL', '').rstrip('/')
        self.client_id = os.environ.get('OIDC_CLIENT_ID', '')
        self.client_secret = os.environ.get('OIDC_CLIENT_SECRET', '')
        self.scopes = os.environ.get('OIDC_SCOPES', 'openid email profile')

    def is_configured(self) -> bool:
        return bool(self.issuer_url and self.client_id and self.client_secret)

    def _get_discovery_document(self) -> dict:
        """获取 OIDC 发现文档"""
        url = f'{self.issuer_url}/.well-known/openid-configuration'
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_login_url(self, redirect_uri: str, state: str) -> str:
        doc = self._get_discovery_document()
        auth_endpoint = doc['authorization_endpoint']
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': self.scopes,
            'state': state,
        }
        return f'{auth_endpoint}?{urlencode(params)}'

    def handle_callback(self, code: str, redirect_uri: str) -> Optional[dict]:
        try:
            doc = self._get_discovery_document()
            token_endpoint = doc['token_endpoint']
            userinfo_endpoint = doc['userinfo_endpoint']

            # 用授权码换取 Token
            token_resp = requests.post(token_endpoint, data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }, timeout=10)
            token_resp.raise_for_status()
            token_data = token_resp.json()
            access_token = token_data.get('access_token')

            if not access_token:
                logger.error("OIDC 回调: 未获取到 access_token")
                return None

            # 获取用户信息
            userinfo_resp = requests.get(userinfo_endpoint, headers={
                'Authorization': f'Bearer {access_token}',
            }, timeout=10)
            userinfo_resp.raise_for_status()
            userinfo = userinfo_resp.json()

            sso_id = userinfo.get('sub', '')
            email = userinfo.get('email', '')
            username = userinfo.get('preferred_username', email.split('@')[0] if email else sso_id)
            display_name = userinfo.get('name', username)
            avatar = userinfo.get('picture', '')

            if not sso_id or not email:
                logger.error("OIDC 回调: 用户信息不完整", userinfo=userinfo)
                return None

            return {
                'sso_id': sso_id,
                'username': username,
                'email': email,
                'display_name': display_name,
                'avatar': avatar,
                'metadata': userinfo,
            }
        except Exception as exc:
            logger.error("OIDC 回调处理失败", error=str(exc))
            return None


class LDAPProvider(SSOProvider):
    """
    LDAP Provider

    环境变量:
        LDAP_SERVER_URL: LDAP 服务器地址 (如 ldap://ldap.example.com:389)
        LDAP_BASE_DN: 搜索基准 DN
        LDAP_BIND_DN: 绑定 DN（可选，用于匿名搜索则留空）
        LDAP_BIND_PASSWORD: 绑定密码
        LDAP_USER_SEARCH_FILTER: 用户搜索过滤器 (默认 '(uid={username})')
        LDAP_USER_ATTR_MAP: 属性映射 JSON (默认 '{}')
    """

    provider_name = 'ldap'

    def __init__(self):
        self.server_url = os.environ.get('LDAP_SERVER_URL', '')
        self.base_dn = os.environ.get('LDAP_BASE_DN', '')
        self.bind_dn = os.environ.get('LDAP_BIND_DN', '')
        self.bind_password = os.environ.get('LDAP_BIND_PASSWORD', '')
        self.search_filter = os.environ.get('LDAP_USER_SEARCH_FILTER', '(uid={username})')
        self.attr_map = {}
        try:
            raw = os.environ.get('LDAP_USER_ATTR_MAP', '{}')
            self.attr_map = json.loads(raw)
        except json.JSONDecodeError:
            pass

    def is_configured(self) -> bool:
        return bool(self.server_url and self.base_dn)

    def get_login_url(self, redirect_uri: str, state: str) -> str:
        # LDAP 通过用户名密码直接认证，不使用跳转 URL
        # 返回一个提示 URL，前端会显示 LDAP 登录表单
        return ''

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """
        LDAP 认证

        使用 python-ldap 或 ldap3 库进行认证。
        如果 ldap3 未安装，记录日志并返回 None。
        """
        try:
            from ldap3 import Server, Connection, ALL
        except ImportError:
            logger.warning("ldap3 未安装，LDAP 认证不可用。请执行: pip install ldap3")
            return None

        try:
            server = Server(self.server_url, get_info=ALL)
            # 先用 bind_dn 搜索用户 DN
            if self.bind_dn:
                conn = Connection(server, user=self.bind_dn, password=self.bind_password, auto_bind=True)
            else:
                conn = Connection(server, auto_bind=True)

            search_dn = self.search_filter.format(username=username)
            conn.search(self.base_dn, search_dn, attributes=['*'])

            if not conn.entries:
                logger.info("LDAP 搜索: 用户未找到", username=username)
                return None

            user_entry = conn.entries[0]
            user_dn = user_entry.entry_dn

            # 用用户 DN + 密码验证
            user_conn = Connection(server, user=user_dn, password=password, auto_bind=True)
            if not user_conn.bound:
                return None

            # 提取用户信息
            email_attr = self.attr_map.get('email', 'mail')
            username_attr = self.attr_map.get('username', 'uid')
            name_attr = self.attr_map.get('display_name', 'cn')

            email = str(user_entry[email_attr]) if email_attr in user_entry else f'{username}@ldap.local'
            display_name = str(user_entry[name_attr]) if name_attr in user_entry else username

            return {
                'sso_id': user_dn,
                'username': username,
                'email': email,
                'display_name': display_name,
                'avatar': '',
                'metadata': {'dn': user_dn},
            }
        except Exception as exc:
            logger.error("LDAP 认证失败", error=str(exc))
            return None

    def handle_callback(self, code: str, redirect_uri: str) -> Optional[dict]:
        # LDAP 不使用 OAuth 回调流程
        return None


# ── 全局 Provider 实例 ──────────────────────────────────────────────────────

oidc_provider = OIDCProvider()
ldap_provider = LDAPProvider()


def get_available_providers() -> list[dict]:
    """获取已配置的 SSO 提供商列表"""
    providers = []
    if oidc_provider.is_configured():
        providers.append({
            'name': 'oidc',
            'display_name': 'OIDC / OAuth2',
            'login_url': None,  # 需要 redirect_uri 参数
        })
    if ldap_provider.is_configured():
        providers.append({
            'name': 'ldap',
            'display_name': 'LDAP',
            'login_url': None,
        })
    return providers


def find_or_create_sso_user(sso_info: dict, provider: str) -> User:
    """
    根据 SSO 信息查找或创建本地用户

    查找顺序:
    1. 按 sso_provider + sso_id 查找
    2. 按 email 查找（关联已有账号）
    3. 创建新用户
    """
    sso_id = sso_info['sso_id']
    email = sso_info.get('email', '').lower()
    username = sso_info.get('username', '')

    # 1. 按 SSO 标识查找
    user = User.query.filter_by(sso_provider=provider, sso_id=sso_id).first()
    if user:
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user

    # 2. 按邮箱关联已有账号
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            user.sso_provider = provider
            user.sso_id = sso_id
            user.sso_metadata = sso_info.get('metadata')
            user.last_login = datetime.utcnow()
            db.session.commit()
            logger.info("SSO 关联已有用户", user_id=user.id, provider=provider)
            return user

    # 3. 创建新用户
    # 确保用户名唯一
    base_username = username or email.split('@')[0] if email else f'sso_{sso_id[:8]}'
    final_username = base_username
    counter = 1
    while User.query.filter_by(username=final_username).first():
        final_username = f'{base_username}_{counter}'
        counter += 1

    # 生成随机密码（SSO 用户不需要本地密码）
    random_password = secrets.token_urlsafe(32)

    user = User(
        username=final_username,
        email=email or f'{final_username}@sso.local',
        password_hash=generate_password_hash(random_password),
        sso_provider=provider,
        sso_id=sso_id,
        sso_metadata=sso_info.get('metadata'),
        avatar=sso_info.get('avatar', ''),
        role='member',
    )
    db.session.add(user)
    db.session.commit()
    logger.info("SSO 自动创建用户", user_id=user.id, provider=provider, username=final_username)
    return user


import secrets
from datetime import datetime
