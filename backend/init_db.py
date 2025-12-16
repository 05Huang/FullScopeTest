"""
数据库初始化脚本

直接创建所有表，用于开发环境快速初始化
"""

from app import create_app
from app.extensions import db

app = create_app('development')

with app.app_context():
    # 删除所有表并重建
    db.drop_all()
    db.create_all()
    print("数据库初始化完成！")
