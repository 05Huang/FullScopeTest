#!/usr/bin/env python3
"""
配置安全性检查脚本

用法:
    cd backend
    python ../scripts/check_config.py [--env production]

检查清单:
    - SECRET_KEY 非空
    - JWT_SECRET_KEY 非空
    - DEBUG 为 False
    - SQLALCHEMY_ECHO 为 False
    - CORS_ORIGINS 不包含 *
    - COOKIE_SECURE 为 True
    - SESSION_COOKIE_HTTPONLY 为 True
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


def check_config(env: str) -> list:
    """检查配置安全性，返回问题列表"""
    from app import create_app
    app = create_app(env)
    issues = []

    with app.app_context():
        cfg = app.config

        # SECRET_KEY
        if not cfg.get('SECRET_KEY'):
            issues.append(('CRITICAL', 'SECRET_KEY 未设置'))

        # JWT_SECRET_KEY
        if not cfg.get('JWT_SECRET_KEY'):
            issues.append(('CRITICAL', 'JWT_SECRET_KEY 未设置'))

        # DEBUG
        if cfg.get('DEBUG'):
            issues.append(('WARNING', 'DEBUG 为 True（生产环境应为 False）'))

        # SQLALCHEMY_ECHO
        if cfg.get('SQLALCHEMY_ECHO'):
            issues.append(('WARNING', 'SQLALCHEMY_ECHO 为 True（生产环境应为 False）'))

        # CORS_ORIGINS
        cors = cfg.get('CORS_ORIGINS', [])
        if '*' in cors:
            issues.append(('CRITICAL', 'CORS_ORIGINS 包含 *（生产环境禁止）'))

        # COOKIE_SECURE
        if env == 'production' and not cfg.get('COOKIE_SECURE'):
            issues.append(('WARNING', 'COOKIE_SECURE 未启用'))

        # JWT_COOKIE_HTTP_ONLY
        if not cfg.get('JWT_COOKIE_HTTP_ONLY'):
            issues.append(('WARNING', 'JWT_COOKIE_HTTP_ONLY 未启用'))

        # SESSION_COOKIE_HTTPONLY (Flask built-in)
        if not cfg.get('SESSION_COOKIE_HTTPONLY', True):
            issues.append(('WARNING', 'SESSION_COOKIE_HTTPONLY 未启用'))

        # DATABASE_URL
        if env == 'production' and not cfg.get('SQLALCHEMY_DATABASE_URI'):
            issues.append(('CRITICAL', 'DATABASE_URL 未设置'))

    return issues


def main():
    parser = argparse.ArgumentParser(description='配置安全性检查')
    parser.add_argument('--env', default='production', help='环境名称')
    args = parser.parse_args()

    print(f'\n检查 {args.env} 环境配置安全性...\n')

    try:
        issues = check_config(args.env)
    except Exception as e:
        print(f'错误: 无法加载配置 - {e}')
        sys.exit(1)

    if not issues:
        print('所有检查通过!')
        sys.exit(0)

    critical = [i for i in issues if i[0] == 'CRITICAL']
    warnings = [i for i in issues if i[0] == 'WARNING']

    if critical:
        print('严重问题:')
        for _, msg in critical:
            print(f'  [CRITICAL] {msg}')

    if warnings:
        print('警告:')
        for _, msg in warnings:
            print(f'  [WARNING] {msg}')

    print(f'\n共 {len(critical)} 个严重问题, {len(warnings)} 个警告')

    if critical:
        sys.exit(1)


if __name__ == '__main__':
    main()
