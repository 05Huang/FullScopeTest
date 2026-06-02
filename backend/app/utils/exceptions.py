"""
自定义异常模块

提供统一的异常类型，用于替代散落的 raise Exception 和 except Exception: pass
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


class NotFoundError(AppError):
    """资源不存在异常"""
    def __init__(self, resource: str, resource_id=None):
        message = f"{resource}不存在"
        if resource_id:
            message = f"{resource} (id={resource_id}) 不存在"
        super().__init__(message=message, code=404)


class PermissionError(AppError):
    """权限不足异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message=message, code=403)


class ConflictError(AppError):
    """资源冲突异常（如重复创建）"""
    def __init__(self, message: str):
        super().__init__(message=message, code=409)


class ExternalServiceError(AppError):
    """外部服务调用异常（AI、OSS 等）"""
    def __init__(self, service: str, message: str, original_error=None):
        self.service = service
        self.original_error = original_error
        super().__init__(message=f"{service}服务调用失败: {message}", code=502)
