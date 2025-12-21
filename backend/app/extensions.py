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

# Celery 实例 - 配置稍后从 Flask 配置加载
celery = Celery(
    __name__,
    include=['app.tasks']  # 自动导入任务模块
)
