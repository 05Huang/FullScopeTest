"""
创建管理员账户脚本
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
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app('development')

with app.app_context():
    # 删除已存在的 admin 用户（如果有）
    existing = User.query.filter_by(username='admin').first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print(f'已删除旧的管理员账户: {existing.username}')

    # 创建管理员
    user = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123')
    )
    db.session.add(user)
    db.session.commit()

    print('✅ 管理员账户创建成功!')
    print('   用户名: admin')
    print('   密码: admin123')
    print('   邮箱: admin@example.com')
    print(f'   ID: {user.id}')