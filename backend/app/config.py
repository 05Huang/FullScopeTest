"""
应用配置模块

包含不同环境的配置类
"""

import os
from datetime import timedelta


class BaseConfig:
    """基础配置"""

    # 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fullscopetest-secret-key-change-in-production')

    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers', 'query_string']
    JWT_QUERY_STRING_NAME = 'token'

    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

    # 报告存储路径
    REPORT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

    # Performance test limits
    PERF_TEST_LIMITS = {
        'min_users': int(os.environ.get('PERF_TEST_MIN_USERS', '1')),
        'max_users': int(os.environ.get('PERF_TEST_MAX_USERS', '2000')),
        'min_spawn_rate': int(os.environ.get('PERF_TEST_MIN_SPAWN_RATE', '1')),
        'max_spawn_rate': int(os.environ.get('PERF_TEST_MAX_SPAWN_RATE', '50')),
        'min_duration': int(os.environ.get('PERF_TEST_MIN_DURATION', '10')),
        'max_duration': int(os.environ.get('PERF_TEST_MAX_DURATION', '3600')),
    }

    # Celery 配置（优先读取显式 Celery 配置，其次回退到 REDIS_URL）
    _redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', _redis_url)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', _redis_url)
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 分钟超时
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ENABLE = os.environ.get('CELERY_ENABLE', 'false').strip().lower() == 'true'  # strip() 去除空格

    # AI Assistant (API test workspace)
    AI_ASSISTANT_ENABLED = os.environ.get('AI_ASSISTANT_ENABLED', 'true').strip().lower() == 'true'
    AI_ASSISTANT_BASE_URL = os.environ.get('AI_ASSISTANT_BASE_URL', 'https://api.openai.com/v1')
    AI_ASSISTANT_API_KEY = os.environ.get('AI_ASSISTANT_API_KEY', '')
    AI_ASSISTANT_MODEL = os.environ.get('AI_ASSISTANT_MODEL', 'gpt-4o-mini')
    AI_ASSISTANT_TIMEOUT = int(os.environ.get('AI_ASSISTANT_TIMEOUT', '30'))
    AI_VISION_BASE_URL = os.environ.get('AI_VISION_BASE_URL', AI_ASSISTANT_BASE_URL)
    AI_VISION_API_KEY = os.environ.get('AI_VISION_API_KEY', AI_ASSISTANT_API_KEY)
    AI_VISION_MODEL = os.environ.get('AI_VISION_MODEL', 'gpt-4o-mini')
    AI_EXPLORE_LIVE_VIEW_ALLOCATOR_URL = os.environ.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_URL', '')
    AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TOKEN = os.environ.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TOKEN', '')
    AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TIMEOUT = int(os.environ.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TIMEOUT', '15'))
    AI_EXPLORE_LIVE_VIEW_INTERNAL_URL_TEMPLATE = os.environ.get('AI_EXPLORE_LIVE_VIEW_INTERNAL_URL_TEMPLATE', '')
    AI_EXPLORE_LIVE_VIEW_URL_TEMPLATE = os.environ.get('AI_EXPLORE_LIVE_VIEW_URL_TEMPLATE', '')
    AI_EXPLORE_LIVE_VIEW_RELEASE_URL = os.environ.get('AI_EXPLORE_LIVE_VIEW_RELEASE_URL', '')
    AI_EXPLORE_LIVE_VIEW_RELEASE_TIMEOUT = int(os.environ.get('AI_EXPLORE_LIVE_VIEW_RELEASE_TIMEOUT', '6'))
    AI_EXPLORE_BROWSER_HEADLESS = os.environ.get('AI_EXPLORE_BROWSER_HEADLESS', 'true')
    AI_EXPLORE_BROWSER_SLOW_MO = int(os.environ.get('AI_EXPLORE_BROWSER_SLOW_MO', '0'))

    # Aliyun OSS configuration
    OSS_ENDPOINT = os.environ.get('OSS_ENDPOINT', '')
    OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET', '')
    OSS_BUCKET_NAME = os.environ.get('OSS_BUCKET_NAME', '')
    OSS_DOMAIN = os.environ.get('OSS_DOMAIN', '')  # Custom domain if available


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    
    DEBUG = True
    # 使用 PostgreSQL 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://admin:123456@localhost:5432/fullscopetest_dev'
    )
    SQLALCHEMY_ECHO = True  # 开发时打印 SQL


class TestingConfig(BaseConfig):
    """测试环境配置"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://admin:123456@localhost:5432/fullscopetest_test'
    )


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # 生产环境必须设置密钥
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
