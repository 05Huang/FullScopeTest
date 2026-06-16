"""
自定义异常模块

提供统一的异常类型，用于替代散落的 raise Exception 和 except Exception: pass

异常类层级：
- AppError（基类，code=500）
  - ValidationError（400）
  - AuthenticationError（401）
  - PermissionError（403）
  - NotFoundError（404）
  - ConflictError（409）
  - RateLimitError（429）
  - ExternalServiceError（502）
"""


class AppError(Exception):
    """应用基础异常"""
    def __init__(self, message: str, code: int = 500, errors=None):
        self.message = message
        self.code = code
        self.errors = errors
        super().__init__(message)


class ValidationError(AppError):
    """参数校验异常"""
    def __init__(self, message: str, errors=None):
        super().__init__(message=message, code=400, errors=errors)


class AuthenticationError(AppError):
    """认证异常（未登录或 Token 无效）"""
    def __init__(self, message: str = "未认证或认证已过期"):
        super().__init__(message=message, code=401)


class PermissionError(AppError):
    """权限不足异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message=message, code=403)


class NotFoundError(AppError):
    """资源不存在异常"""
    def __init__(self, resource: str, resource_id=None):
        message = f"{resource}不存在"
        if resource_id:
            message = f"{resource} (id={resource_id}) 不存在"
        super().__init__(message=message, code=404)


class ConflictError(AppError):
    """资源冲突异常（如重复创建）"""
    def __init__(self, message: str):
        super().__init__(message=message, code=409)


class RateLimitError(AppError):
    """请求频率限制异常"""
    def __init__(self, message: str = "请求过于频繁，请稍后重试"):
        super().__init__(message=message, code=429)


class ExternalServiceError(AppError):
    """外部服务调用异常（AI、OSS 等）"""
    def __init__(self, service: str, message: str, original_error=None):
        self.service = service
        self.original_error = original_error
        super().__init__(message=f"{service}服务调用失败: {message}", code=502)
