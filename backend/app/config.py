"""
应用配置模块

包含不同环境的配置类
"""

import os
from datetime import timedelta


class BaseConfig:
    """基础配置"""

    # 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'easytest-secret-key-change-in-production')

    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

    # 报告存储路径
    REPORT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

    # Performance test limits
    PERF_TEST_LIMITS = {
        'min_users': int(os.environ.get('PERF_TEST_MIN_USERS', '1')),
        'max_users': int(os.environ.get('PERF_TEST_MAX_USERS', '200')),
        'min_spawn_rate': int(os.environ.get('PERF_TEST_MIN_SPAWN_RATE', '1')),
        'max_spawn_rate': int(os.environ.get('PERF_TEST_MAX_SPAWN_RATE', '50')),
        'min_duration': int(os.environ.get('PERF_TEST_MIN_DURATION', '10')),
        'max_duration': int(os.environ.get('PERF_TEST_MAX_DURATION', '3600')),
    }

    # Celery 配置（可选，如果Redis不可用则不使用异步任务）
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 分钟超时
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ENABLE = os.environ.get('CELERY_ENABLE', 'false').strip().lower() == 'true'  # strip() 去除空格


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    
    DEBUG = True
    # 使用 PostgreSQL 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://easytest:easytest123@localhost:5432/easytest_dev'
    )
    SQLALCHEMY_ECHO = True  # 开发时打印 SQL


class TestingConfig(BaseConfig):
    """测试环境配置"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://easytest:easytest123@localhost:5432/easytest_test'
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
