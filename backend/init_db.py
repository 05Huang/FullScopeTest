"""
数据库初始化脚本

直接创建所有表，用于开发环境快速初始化
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 先加载 backend 目录下的 .env，避免 config.py 提前读取到默认值
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

print("DATABASE_URL =", os.getenv("DATABASE_URL"))
print("CELERY_ENABLE =", os.getenv("CELERY_ENABLE"))

from app import create_app
from app.extensions import db

app = create_app('development')

with app.app_context():
    # 删除所有表并重建
    db.drop_all()
    db.create_all()
    print("数据库初始化完成！")