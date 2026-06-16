"""
FullScopeTest 后端应用工厂

创建和配置 Flask 应用实例
"""

import os
from dotenv import load_dotenv

# Ensure .env is loaded before evaluating config
# override=False: Docker/compose env vars take precedence over .env file values
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path, override=False)
else:
    load_dotenv(override=False)

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

from .extensions import db, migrate, jwt, celery
from .config import config
from .celery_app import init_celery
from .scheduler import init_scheduler
from .core.logging import configure_structlog, set_trace_id, clear_trace_id, get_logger

# 初始化限流器
limiter = Limiter(key_func=get_remote_address)

# 初始化 CSRF 保护
csrf = CSRFProtect()

# 全局 logger
logger = get_logger(__name__)


def create_app(config_name='development'):
    """
    应用工厂函数

    Args:
        config_name: 配置环境名称 (development/testing/production)

    Returns:
        Flask: 配置好的 Flask 应用实例
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 生产环境密钥校验
    if config_name == 'production':
        _validate_production_secrets(app)

    # 初始化结构化日志
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    json_format = config_name in ('production', 'staging')
    configure_structlog(log_level=log_level, json_format=json_format)

    # 注入 trace_id 到每个请求上下文
    @app.before_request
    def _inject_trace_id():
        from flask import g
        g.trace_id = set_trace_id()

    @app.teardown_appcontext
    def _clear_trace_id(exc=None):
        clear_trace_id()

    # 初始化扩展
    init_extensions(app)

    # 初始化 Celery（可选）
    if app.config.get('CELERY_ENABLE', False):
        try:
            init_celery(celery, app)
            logger.info('Celery initialized successfully')
        except Exception as e:
            logger.warning('Celery initialization failed, running without async tasks', error=str(e))
    else:
        logger.info('Celery is disabled. Running without async tasks.')

    # 注册蓝图
    register_blueprints(app)

    # 注册全局错误处理器
    register_error_handlers(app)

    # 初始化定时任务
    init_scheduler(app)

    # 可选：启动时自动 seed 默认数据（通过环境变量控制）
    if os.environ.get('AUTO_SEED', '').lower() == 'true':
        _seed_default_prompt_versions(app)

    # 初始化 Prometheus 指标采集
    try:
        from .core.metrics import init_metrics
        init_metrics(app)
        logger.info("Prometheus metrics initialized successfully")
    except Exception as e:
        logger.warning("Prometheus metrics initialization failed", error=str(e))

    # 初始化租户中间件
    from .middleware.tenant import setup_tenant_hooks
    setup_tenant_hooks(app)

    # 初始化限流中间件
    from .middleware.rate_limit import rate_limit_middleware
    rate_limit_middleware(app)

    # 初始化安全响应头中间件
    from .middleware.security_headers import security_headers_middleware
    security_headers_middleware(app)

    # 初始化 RBAC 权限注入中间件
    from .middleware.permission import inject_user_permissions
    inject_user_permissions(app)

    # 初始化插件系统
    _init_plugins(app)

    # 应用启动时自动 seed 系统角色（幂等）
    if os.environ.get('AUTO_SEED', '').lower() == 'true' or os.environ.get('SEED_RBAC', '').lower() == 'true':
        _seed_system_roles(app)

    return app


def _validate_production_secrets(app):
    """校验生产环境必需的密钥"""
    required_secrets = ['SECRET_KEY', 'JWT_SECRET_KEY']
    missing = [key for key in required_secrets if not app.config.get(key)]
    if missing:
        raise RuntimeError(f"生产环境缺少必需配置: {', '.join(missing)}。请在环境变量中设置这些值。")


def _seed_default_prompt_versions(app):
    """在应用启动时确保默认 PromptVersion 存在"""
    try:
        with app.app_context():
            from .extensions import db
            from sqlalchemy import inspect as sa_inspect
            # 检查表是否存在，数据库未初始化时跳过
            try:
                inspector = sa_inspect(db.engine)
                if not inspector.has_table("prompt_versions"):
                    return
            except Exception:
                return

            from .models.prompt_version import PromptVersion
            from .services.ai.script_generator import (
                DEFAULT_WEB_SYSTEM_PROMPT,
                DEFAULT_PERF_SYSTEM_PROMPT,
            )

            defaults = [
                ('script_gen_web', 'baseline', DEFAULT_WEB_SYSTEM_PROMPT),
                ('script_gen_perf', 'baseline', DEFAULT_PERF_SYSTEM_PROMPT),
            ]

            for feature, name, system_prompt in defaults:
                existing = PromptVersion.query.filter_by(
                    feature=feature, version=1
                ).first()
                if not existing:
                    pv = PromptVersion(
                        feature=feature,
                        name=name,
                        version=1,
                        is_active=True,
                        system_prompt=system_prompt,
                        temperature=0.2,
                        traffic_weight=1.0,
                        change_notes='Initial baseline prompt',
                    )
                    db.session.add(pv)
                    logger.info('Seeded default PromptVersion', feature=feature)

            db.session.commit()
    except Exception as exc:
        logger.warning('Failed to seed default PromptVersions', error=str(exc))


def _init_plugins(app):
    """初始化插件系统：自动发现并加载插件"""
    try:
        from .plugins.registry import plugin_registry
        # 自动扫描 custom/ 目录下的插件
        plugin_registry.auto_discover()
        # 注册内置插件（如有）
        _register_builtin_plugins(plugin_registry)
        # 初始化所有插件
        plugin_registry.init_all(app)
    except Exception as exc:
        logger.warning("插件系统初始化失败", error=str(exc))


def _register_builtin_plugins(registry):
    """注册内置插件"""
    try:
        from .plugins.custom.slack_notify import SlackNotifyPlugin
        registry.register(SlackNotifyPlugin())
    except Exception:
        pass  # 内置插件加载失败不影响启动


def _seed_system_roles(app):
    """在应用启动时自动创建系统角色（幂等操作）"""
    try:
        with app.app_context():
            from .extensions import db
            from sqlalchemy import inspect as sa_inspect
            try:
                inspector = sa_inspect(db.engine)
                if not inspector.has_table("roles"):
                    return
            except Exception:
                return

            from .services.permission_service import seed_system_roles
            seed_system_roles()
            logger.info("System roles seeded successfully")
    except Exception as exc:
        logger.warning("Failed to seed system roles", error=str(exc))


def init_extensions(app):
    """初始化 Flask 扩展"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS - 使用配置中的允许源列表
    cors_origins = app.config.get('CORS_ORIGINS', ['http://localhost:3000'])
    CORS(app, resources={r"/api/*": {"origins": cors_origins}}, supports_credentials=True)

    # 限流
    limiter.init_app(app)

    # CSRF 保护（API 通常禁用，因为使用 JWT）
    # 仅对浏览器表单提交启用，API 请求通过 JWT 验证
    if app.config.get('WTF_CSRF_ENABLED', False):
        csrf.init_app(app)

    # 数据库会话生命周期管理（替代 Flask-SQLAlchemy 的自动管理）
    # 会话在首次访问 db.session 时自动创建（scoped_session）
    # 请求结束时提交或回滚，然后释放会话
    @app.teardown_appcontext
    def _db_session_teardown(exc=None):
        try:
            if exc is None:
                db.session.commit()
            else:
                db.session.rollback()
        except Exception:
            db.session.rollback()
        finally:
            db.session.remove()


def register_blueprints(app):
    """注册 API 蓝图"""
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # 健康检查端点（无需认证）
    from .core.health import health_bp
    app.register_blueprint(health_bp)

    # 豁免 API 蓝图的 CSRF 保护（使用 JWT 认证）
    if app.config.get('WTF_CSRF_ENABLED', False):
        csrf.exempt(api_bp)


def register_error_handlers(app):
    """注册全局错误处理器"""
    from .utils.response import error_response
    from .utils.exceptions import AppError

    @app.errorhandler(AppError)
    def handle_app_error(e):
        """统一处理自定义异常"""
        return error_response(e.code, e.message, errors=e.errors)

    @app.errorhandler(400)
    def bad_request(e):
        return error_response(400, '请求参数错误')

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response(401, '未授权访问')

    @app.errorhandler(404)
    def not_found(e):
        return error_response(404, '资源不存在')

    @app.errorhandler(500)
    def internal_error(e):
        return error_response(500, '服务器内部错误')
