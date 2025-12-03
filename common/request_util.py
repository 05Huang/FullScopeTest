"""
HTTP 请求工具类
用于统一管理所有 HTTP 请求，包括日志记录、错误处理、SSL 配置等
"""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from common.logger_util import LoggerUtil

# 获取日志记录器
logger = LoggerUtil.get_logger("request_logger")

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestUtil:
    """
    HTTP 请求工具类
    
    功能：
    - 统一管理 HTTP 请求（GET, POST, PUT, DELETE 等）
    - 自动禁用 SSL 验证（用于测试环境）
    - 自动记录所有请求和响应日志
    - 统一的错误处理
    
    使用示例：
        response = RequestUtil.send(
            method='POST',
            url='https://api.example.com/users',
            headers={'Content-Type': 'application/json'},
            json={'name': 'John'},
            params={'page': 1}
        )
    """
    
    # 配置常量
    DEFAULT_TIMEOUT = 15  # 默认超时时间（秒）
    VERIFY_SSL = False    # 是否验证 SSL 证书（测试环境禁用）
    
    @staticmethod
    def send(method, url, headers=None, json=None, params=None, timeout=None, verify=None):
        """
        发送 HTTP 请求
        
        参数：
            method (str): HTTP 方法 (GET, POST, PUT, DELETE, PATCH 等)
            url (str): 完整的请求 URL
            headers (dict): 请求头，可选
            json (dict): JSON 请求体，可选
            params (dict): URL 查询参数，可选
            timeout (int): 超时时间（秒），默认 15 秒
            verify (bool): 是否验证 SSL 证书，默认 False（禁用）
        
        返回：
            requests.Response: 响应对象
        
        异常：
            RequestException: 网络错误
            Timeout: 超时错误
            其他异常会被记录并重新抛出
        """
        
        # 使用默认配置如果未提供
        if timeout is None:
            timeout = RequestUtil.DEFAULT_TIMEOUT
        if verify is None:
            verify = RequestUtil.VERIFY_SSL
        
        try:
            # 记录请求信息
            logger.info(f"{'='*60}")
            logger.info(f"📤 发送 {method.upper()} 请求")
            logger.info(f"   URL: {url}")
            if headers:
                logger.info(f"   Headers: {headers}")
            if json:
                logger.info(f"   Body: {json}")
            if params:
                logger.info(f"   Params: {params}")
            
            # 发送请求
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                params=params,
                timeout=timeout,
                verify=verify
            )
            
            # 记录响应信息
            logger.info(f"📥 收到响应 - 状态码: {response.status_code}")
            logger.info(f"   响应大小: {len(response.content)} 字节")
            if response.text:
                # 只记录前 500 个字符，避免日志过长
                body_preview = response.text[:500]
                if len(response.text) > 500:
                    body_preview += "...(已截断)"
                logger.info(f"   响应体: {body_preview}")
            logger.info(f"{'='*60}")
            
            return response
        
        except requests.exceptions.Timeout:
            logger.error(f"⏱️  请求超时: {url} (超时时间: {timeout}秒)")
            raise
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"🔌 连接错误: {url} - {str(e)}")
            raise
        
        except requests.exceptions.SSLError as e:
            logger.error(f"🔒 SSL 错误: {url} - {str(e)}")
            raise
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 请求错误: {url} - {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"❌ 未知错误: {url} - {type(e).__name__}: {str(e)}")
            raise
