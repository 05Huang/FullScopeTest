"""
应用配置模块

包含不同环境的配置类
"""

import os
from datetime import timedelta


def _env_int(key: str, default: int) -> int:
    raw = os.environ.get(key)
    if raw is None:
        return default
    value = str(raw).strip()
    if not value:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class BaseConfig:
    """基础配置"""

    # 密钥配置（不设默认弱密钥，必须通过环境变量设置）
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # CORS 配置 - 允许的源列表（逗号分隔）
    # 开发环境默认允许 localhost
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3001,http://localhost:3000,http://localhost:8080').split(',')
    # 允许的 HTTP 方法
    CORS_METHODS = os.environ.get('CORS_METHODS', 'GET,POST,PUT,DELETE,PATCH,OPTIONS').split(',')
    # 允许的请求头
    CORS_ALLOW_HEADERS = os.environ.get('CORS_ALLOW_HEADERS', 'Authorization,Content-Type,X-Request-ID').split(',')
    # 预检请求缓存时间（秒）
    CORS_MAX_AGE = int(os.environ.get('CORS_MAX_AGE', '3600'))

    # 并行测试执行配置
    PARALLEL_WORKERS = int(os.environ.get('PARALLEL_WORKERS', '5'))
    MAX_PARALLEL_WORKERS = int(os.environ.get('MAX_PARALLEL_WORKERS', '20'))

    # 限流配置
    RATELIMIT_DEFAULT = "200/minute"
    RATELIMIT_STORAGE_URI = os.environ.get('REDIS_URL', 'memory://')

    # CSRF 配置
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1小时

    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT 配置（不设默认弱密钥，必须通过环境变量设置）
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']

    # Cookie 安全配置
    # Secure 标志：生产环境默认开启，开发环境通过 COOKIE_SECURE 环境变量控制
    COOKIE_SECURE = os.environ.get('COOKIE_SECURE', '').lower() == 'true'
    COOKIE_SAMESITE = os.environ.get('COOKIE_SAMESITE', 'Lax')  # Lax / Strict / None
    COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN', '')  # 留空则不设置 domain

    # Flask-JWT-Extended Cookie 配置
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_COOKIE_SECURE = COOKIE_SECURE
    JWT_COOKIE_SAMESITE = COOKIE_SAMESITE
    JWT_COOKIE_HTTP_ONLY = True
    JWT_COOKIE_CSRF_PROTECT = False  # 使用 SameSite 替代 CSRF double-submit
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'

    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

    # 报告存储路径
    REPORT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

    # 截图存储路径（视觉回归测试）
    SCREENSHOT_STORAGE_PATH = os.environ.get(
        'SCREENSHOT_STORAGE_PATH',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'screenshots')
    )

    # Performance test limits
    PERF_TEST_LIMITS = {
        'min_users': _env_int('PERF_TEST_MIN_USERS', 1),
        'max_users': _env_int('PERF_TEST_MAX_USERS', 2000),
        'min_spawn_rate': _env_int('PERF_TEST_MIN_SPAWN_RATE', 1),
        'max_spawn_rate': _env_int('PERF_TEST_MAX_SPAWN_RATE', 50),
        'min_duration': _env_int('PERF_TEST_MIN_DURATION', 10),
        'max_duration': _env_int('PERF_TEST_MAX_DURATION', 3600),
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

    # Celery 可靠性：死信队列 + 任务重试
    CELERY_TASK_ACKS_LATE = True
    CELERY_TASK_REJECT_ON_WORKER_LOST = True
    CELERY_TASK_ROUTES = {
        'tasks.*': {'queue': 'default'},
    }
    CELERY_TASK_DEFAULT_RETRY_DELAY = 60  # 重试间隔 60 秒
    CELERY_TASK_MAX_RETRIES = 3

    # AI Assistant (API test workspace)
    AI_ASSISTANT_ENABLED = os.environ.get('AI_ASSISTANT_ENABLED', 'true').strip().lower() == 'true'
    AI_ASSISTANT_BASE_URL = os.environ.get('AI_ASSISTANT_BASE_URL', 'https://api.openai.com/v1')
    AI_ASSISTANT_API_KEY = os.environ.get('AI_ASSISTANT_API_KEY', '')
    AI_ASSISTANT_MODEL = os.environ.get('AI_ASSISTANT_MODEL', 'gpt-4o-mini')
    AI_ASSISTANT_TIMEOUT = _env_int('AI_ASSISTANT_TIMEOUT', 30)
    AI_VISION_BASE_URL = os.environ.get('AI_VISION_BASE_URL', AI_ASSISTANT_BASE_URL)
    AI_VISION_API_KEY = os.environ.get('AI_VISION_API_KEY', AI_ASSISTANT_API_KEY)
    AI_VISION_MODEL = os.environ.get('AI_VISION_MODEL', 'gpt-4o-mini')
    AI_EXPLORE_LIVE_VIEW_ALLOCATOR_URL = os.environ.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_URL', '')
    AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TOKEN = os.environ.get('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TOKEN', '')
    AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TIMEOUT = _env_int('AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TIMEOUT', 15)
    AI_EXPLORE_LIVE_VIEW_INTERNAL_URL_TEMPLATE = os.environ.get('AI_EXPLORE_LIVE_VIEW_INTERNAL_URL_TEMPLATE', '')
    AI_EXPLORE_LIVE_VIEW_URL_TEMPLATE = os.environ.get('AI_EXPLORE_LIVE_VIEW_URL_TEMPLATE', '')
    AI_EXPLORE_LIVE_VIEW_RELEASE_URL = os.environ.get('AI_EXPLORE_LIVE_VIEW_RELEASE_URL', '')
    AI_EXPLORE_LIVE_VIEW_RELEASE_TIMEOUT = _env_int('AI_EXPLORE_LIVE_VIEW_RELEASE_TIMEOUT', 6)
    AI_EXPLORE_BROWSER_HEADLESS = os.environ.get('AI_EXPLORE_BROWSER_HEADLESS', 'true')
    AI_EXPLORE_BROWSER_SLOW_MO = _env_int('AI_EXPLORE_BROWSER_SLOW_MO', 0)

    # Aliyun OSS configuration
    OSS_ENDPOINT = os.environ.get('OSS_ENDPOINT', '')
    OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET', '')
    OSS_BUCKET_NAME = os.environ.get('OSS_BUCKET_NAME', '')
    OSS_DOMAIN = os.environ.get('OSS_DOMAIN', '')  # Custom domain if available

    # Webhook 安全配置
    WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '')  # HMAC 签名密钥，为空则不验证

    # GitHub OAuth 配置
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
    GITHUB_REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI', 'http://localhost:5000/api/v1/integrations/github/callback')
    GITHUB_WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET', '')


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""

    DEBUG = True
    # 开发环境使用默认密钥（生产环境必须通过环境变量设置）
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')

    # 使用 PostgreSQL 数据库
    _raw_db_url = os.environ.get(
        'DATABASE_URL',
        'postgresql://localhost:5432/fullscopetest_dev'
    )
    # SQLite 相对路径需要基于项目根目录解析，避免被 Flask instance_path 二次拼接
    if _raw_db_url.startswith('sqlite:///') and not _raw_db_url.startswith('sqlite:////'):
        _rel_path = _raw_db_url[len('sqlite:///'):]
        _abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), _rel_path)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{_abs_path}'
    else:
        SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_ECHO = True  # 开发时打印 SQL
    # SQLite 不支持连接池，使用 NullPool 避免 "database is locked" 错误
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }


class TestingConfig(BaseConfig):
    """测试环境配置"""

    TESTING = True
    # 测试环境使用默认密钥
    SECRET_KEY = os.environ.get('SECRET_KEY', 'test-secret-key-for-testing-only-32bytes!')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'test-jwt-secret-key-for-testing-only-32bytes!')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://localhost:5432/fullscopetest_test'
    )
    # 测试环境禁用限流和 CSRF，启用 DEBUG
    RATELIMIT_ENABLED = False
    DEBUG = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """生产环境配置"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # 生产环境必须设置密钥
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    @staticmethod
    def init_app(app):
        """生产环境启动时校验关键配置项"""
        BaseConfig.init_app(app) if hasattr(BaseConfig, 'init_app') else None

        missing = []
        if not app.config.get('SECRET_KEY'):
            missing.append('SECRET_KEY')
        if not app.config.get('JWT_SECRET_KEY'):
            missing.append('JWT_SECRET_KEY')
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            missing.append('DATABASE_URL')

        if missing:
            raise RuntimeError(
                f"生产环境缺少必需的环境变量: {', '.join(missing)}。"
                f"请在 .env 或环境变量中设置后重启服务。"
            )

    # 生产环境 Cookie 默认启用 Secure
    COOKIE_SECURE = os.environ.get('COOKIE_SECURE', 'true').lower() == 'true'
    JWT_COOKIE_SECURE = COOKIE_SECURE

    # 生产环境 CORS 必须显式配置，不允许默认 localhost
    _cors_raw = os.environ.get('CORS_ORIGINS', '')
    CORS_ORIGINS = [o.strip() for o in _cors_raw.split(',') if o.strip()] if _cors_raw else []

    # 生产环境限流更严格
    RATELIMIT_DEFAULT = "100/minute"

    # SQLAlchemy 连接池优化
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': _env_int('DB_POOL_SIZE', 10),        # 连接池大小
        'max_overflow': _env_int('DB_MAX_OVERFLOW', 20),   # 超出池大小后最多额外创建的连接数
        'pool_timeout': _env_int('DB_POOL_TIMEOUT', 30),   # 获取连接超时（秒）
        'pool_recycle': _env_int('DB_POOL_RECYCLE', 1800), # 连接回收时间（秒），防止 MySQL 断连
        'pool_pre_ping': True,                              # 使用前检测连接是否有效
    }


# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
