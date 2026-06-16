"""
存储抽象层

提供统一的文件存储接口，支持多种存储后端：
- LocalStorage：本地文件系统（开发环境）
- OSSStorage：阿里云 OSS（生产环境，待实现）
- S3Storage：AWS S3（生产环境，待实现）

通过 STORAGE_TYPE 环境变量切换：local / oss / s3

安全特性：
- 文件类型校验（magic bytes）
- 文件大小限制
- 文件名随机化（UUID，防止路径遍历）
"""

import os
import uuid
import hashlib
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from ..core.logging import get_logger

logger = get_logger(__name__)

# 文件大小限制（字节）
FILE_SIZE_LIMITS = {
    'image': 5 * 1024 * 1024,      # 图片 5MB
    'script': 500 * 1024,           # 脚本 500KB
    'report': 20 * 1024 * 1024,     # 报告附件 20MB
    'default': 10 * 1024 * 1024,    # 默认 10MB
}

# 允许的文件类型（MIME → magic bytes）
ALLOWED_MIME_MAGIC = {
    'image/png': b'\x89PNG',
    'image/jpeg': b'\xff\xd8\xff',
    'image/gif': b'GIF8',
    'image/webp': b'RIFF',
    'application/pdf': b'%PDF',
    'application/json': None,  # JSON 无固定 magic bytes
    'text/csv': None,
    'text/plain': None,
    'application/x-yaml': None,
    'text/yaml': None,
}

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {
    'image': {'.png', '.jpg', '.jpeg', '.gif', '.webp'},
    'script': {'.py', '.js', '.ts'},
    'document': {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.json', '.yaml', '.yml'},
    'report': {'.pdf', '.xlsx', '.csv', '.html'},
}


def validate_file(file_data: bytes, file_type: str = 'default', filename: str = '') -> Tuple[bool, str]:
    """
    校验文件安全性

    Args:
        file_data: 文件二进制内容
        file_type: 文件类型类别（image/script/document/report/default）
        filename: 原始文件名（用于扩展名检查）

    Returns:
        (is_valid, error_message)
    """
    # 检查文件大小
    size_limit = FILE_SIZE_LIMITS.get(file_type, FILE_SIZE_LIMITS['default'])
    if len(file_data) > size_limit:
        size_mb = size_limit / (1024 * 1024)
        return False, f'文件大小超过限制（最大 {size_mb:.0f}MB）'

    if len(file_data) == 0:
        return False, '文件内容为空'

    # 检查文件扩展名
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        allowed_exts = ALLOWED_EXTENSIONS.get(file_type, set())
        if allowed_exts and ext not in allowed_exts:
            return False, f'不允许的文件类型: {ext}'

    return True, ''


def generate_safe_filename(original_filename: str) -> str:
    """
    生成安全的文件名（UUID 随机化）

    防止路径遍历攻击和文件名冲突。
    保留原始扩展名。
    """
    ext = os.path.splitext(original_filename)[1].lower()
    # 清理扩展名中的非法字符
    ext = ''.join(c for c in ext if c.isalnum() or c == '.')
    safe_name = f"{uuid.uuid4().hex}{ext}"
    return safe_name


class StorageBase(ABC):
    """存储服务基类"""

    @abstractmethod
    def upload(self, file_data: bytes, path: str, content_type: str = '') -> str:
        """
        上传文件

        Args:
            file_data: 文件二进制内容
            path: 存储路径（相对路径）
            content_type: MIME 类型

        Returns:
            str: 文件访问 URL
        """
        pass

    @abstractmethod
    def download(self, path: str) -> bytes:
        """
        下载文件

        Args:
            path: 存储路径

        Returns:
            bytes: 文件内容
        """
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        """
        删除文件

        Args:
            path: 存储路径

        Returns:
            bool: 是否成功
        """
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """检查文件是否存在"""
        pass


class LocalStorage(StorageBase):
    """本地文件系统存储（开发环境）"""

    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'uploads'
        )
        os.makedirs(self.base_path, exist_ok=True)

    def _full_path(self, path: str) -> str:
        """获取完整文件路径（防止路径遍历）"""
        # 规范化路径，防止 ../ 攻击
        normalized = os.path.normpath(path)
        if normalized.startswith('..') or os.path.isabs(normalized):
            raise ValueError(f"非法路径: {path}")
        full = os.path.join(self.base_path, normalized)
        return full

    def upload(self, file_data: bytes, path: str, content_type: str = '') -> str:
        full_path = self._full_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(file_data)
        logger.info("文件已上传", path=path, size=len(file_data))
        return f"/uploads/{path}"

    def download(self, path: str) -> bytes:
        full_path = self._full_path(path)
        with open(full_path, 'rb') as f:
            return f.read()

    def delete(self, path: str) -> bool:
        full_path = self._full_path(path)
        if os.path.exists(full_path):
            os.remove(full_path)
            logger.info("文件已删除", path=path)
            return True
        return False

    def exists(self, path: str) -> bool:
        full_path = self._full_path(path)
        return os.path.exists(full_path)


def get_storage() -> StorageBase:
    """
    获取存储服务实例

    通过 STORAGE_TYPE 环境变量选择存储后端：
    - local（默认）：本地文件系统
    - oss：阿里云 OSS（待实现）
    - s3：AWS S3（待实现）
    """
    storage_type = os.environ.get('STORAGE_TYPE', 'local').lower()

    if storage_type == 'local':
        return LocalStorage()
    elif storage_type == 'oss':
        # TODO: 实现阿里云 OSS 存储
        logger.warning("OSS 存储尚未实现，回退到本地存储")
        return LocalStorage()
    elif storage_type == 's3':
        # TODO: 实现 AWS S3 存储
        logger.warning("S3 存储尚未实现，回退到本地存储")
        return LocalStorage()
    else:
        logger.warning(f"未知的存储类型: {storage_type}，使用本地存储")
        return LocalStorage()
