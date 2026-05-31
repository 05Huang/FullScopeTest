"""
Flask 扩展实例

集中管理所有 Flask 扩展，避免循环导入
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery

# 数据库 ORM
db = SQLAlchemy()

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
