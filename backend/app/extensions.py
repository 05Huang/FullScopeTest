"""
Flask 扩展实例

集中管理所有 Flask 扩展，避免循环导入

数据库模块已迁移到 database.py，支持 Flask 和 FastAPI 双框架。
"""

from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery

# 数据库 ORM（从独立模块导入，不再依赖 Flask-SQLAlchemy）
from .database import db

# 数据库迁移
migrate = Migrate()

# JWT 认证
jwt = JWTManager()


# JWT Token 黑名单检查
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """检查 JWT Token 是否已被注销"""
    from .services.token_blacklist import is_token_blacklisted
    jti = jwt_payload.get('jti')
    if not jti:
        return False
    return is_token_blacklisted(jti)


# Celery 实例 - 配置稍后从 Flask 配置加载
celery = Celery(
    __name__,
    include=['app.tasks']  # 自动导入任务模块
)
