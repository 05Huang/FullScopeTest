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
