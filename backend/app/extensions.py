"""
Flask 扩展实例

集中管理所有 Flask 扩展，避免循环导入
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# 数据库 ORM
db = SQLAlchemy()

# 数据库迁移
migrate = Migrate()

# JWT 认证
jwt = JWTManager()
