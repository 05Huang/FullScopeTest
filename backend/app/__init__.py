"""
EasyTest 后端应用工厂

创建和配置 Flask 应用实例
"""

from flask import Flask
from flask_cors import CORS

from .extensions import db, migrate, jwt, celery
from .config import config
from .celery_app import init_celery


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
    
    # 初始化扩展
    init_extensions(app)
    
    # 初始化 Celery（可选）
    if app.config.get('CELERY_ENABLE', False):
        try:
            init_celery(celery, app)
            app.logger.info('Celery initialized successfully')
        except Exception as e:
            app.logger.warning(f'Celery initialization failed: {e}. Running without async tasks.')
    else:
        app.logger.info('Celery is disabled. Running without async tasks.')
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app


def init_extensions(app):
    """初始化 Flask 扩展"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


def register_blueprints(app):
    """注册 API 蓝图"""
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')


def register_error_handlers(app):
    """注册全局错误处理器"""
    from .utils.response import error_response
    
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
