"""
创建测试用户脚本
"""

from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app('development')

with app.app_context():
    # 检查用户是否已存在
    existing_user = User.query.filter_by(username='admin').first()
    if existing_user:
        print("测试用户已存在！")
        print(f"用户名: {existing_user.username}")
        print(f"邮箱: {existing_user.email}")
    else:
        # 创建测试用户
        test_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_active=True
        )
        db.session.add(test_user)
        db.session.commit()
        print("测试用户创建成功！")
        print("用户名: admin")
        print("密码: admin123")
        print("邮箱: admin@example.com")
