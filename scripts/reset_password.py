#!/usr/bin/env python3
"""
管理员密码重置工具

用法:
    cd backend
    python ../scripts/reset_password.py --user admin --password NewP@ssw0rd

说明:
    此脚本用于在邮件服务未配置时，管理员通过命令行重置用户密码。
    仅限管理员或拥有服务器访问权限的人员使用。
"""
import argparse
import os
import sys

# 将 backend 目录加入 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


def main():
    parser = argparse.ArgumentParser(description='重置用户密码（管理员工具）')
    parser.add_argument('--user', '-u', required=True, help='用户名或邮箱')
    parser.add_argument('--password', '-p', required=True, help='新密码（至少8位）')
    parser.add_argument('--env', default='development', help='Flask 环境 (development/production)')
    args = parser.parse_args()

    if len(args.password) < 8:
        print('错误: 密码长度至少为 8 位')
        sys.exit(1)

    # 创建 Flask 应用
    from app import create_app
    app = create_app(args.env)

    with app.app_context():
        from app.extensions import db
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        from datetime import datetime, timezone

        # 按用户名或邮箱查找用户
        user = User.query.filter(
            (User.username == args.user) | (User.email == args.user)
        ).first()

        if not user:
            print(f'错误: 未找到用户 "{args.user}"')
            sys.exit(1)

        # 重置密码
        user.password_hash = generate_password_hash(args.password)
        user.password_changed_at = datetime.now(timezone.utc)
        # 清除可能存在的重置 token
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()

        print(f'成功: 用户 "{user.username}" (ID: {user.id}) 的密码已重置')
        print(f'密码修改时间: {user.password_changed_at.isoformat()}')


if __name__ == '__main__':
    main()
