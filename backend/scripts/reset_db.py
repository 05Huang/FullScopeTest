#!/usr/bin/env python
"""
数据库重置脚本

用途：开发环境数据库重置，从零开始运行迁移并填充种子数据。

使用方法：
    cd backend
    python scripts/reset_db.py --seed

可选参数：
    --seed    填充种子数据（默认用户、角色、Prompt 版本等）
    --force   跳过确认提示

注意：仅限开发环境使用，生产环境禁止运行！
"""

import os
import sys
import argparse

# 确保 backend 目录在 Python path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def metadata_sorted_tables(db):
    """获取按依赖排序的表名列表"""
    from app.models import *  # noqa: F401,F403 — 确保所有模型导入
    return [t.name for t in db.metadata.sorted_tables]


def _seed_data(app, db, logger):
    """填充种子数据"""
    try:
        from app.models.user import User
        from app.services.permission_service import seed_system_roles

        # 创建默认管理员
        admin = User(
            username='admin',
            email='admin@fullscopetest.local',
            role='admin',
            is_active=True,
        )
        admin.set_password('Admin@123456')
        db.session.add(admin)
        db.session.commit()
        print("  创建管理员: admin / Admin@123456")

        # 创建系统角色
        seed_system_roles()
        print("  系统角色已创建")

        # 创建默认 Prompt 版本
        _seed_prompt_versions(app, db, logger)

    except Exception as exc:
        logger.warning("种子数据填充失败", error=str(exc))
        print(f"  [WARN] 种子数据填充失败: {exc}")


def _seed_prompt_versions(app, db, logger):
    """创建默认 Prompt 版本"""
    try:
        from app.models.prompt_version import PromptVersion
        from app.services.ai.script_generator import (
            DEFAULT_WEB_SYSTEM_PROMPT,
            DEFAULT_PERF_SYSTEM_PROMPT,
        )

        defaults = [
            ('script_gen_web', 'baseline', DEFAULT_WEB_SYSTEM_PROMPT),
            ('script_gen_perf', 'baseline', DEFAULT_PERF_SYSTEM_PROMPT),
        ]

        for feature, name, system_prompt in defaults:
            pv = PromptVersion(
                feature=feature,
                name=name,
                version=1,
                is_active=True,
                system_prompt=system_prompt,
                temperature=0.2,
                traffic_weight=1.0,
                change_notes='Initial baseline prompt',
            )
            db.session.add(pv)

        db.session.commit()
        print("  默认 Prompt 版本已创建")
    except Exception as exc:
        logger.warning("Prompt 版本种子失败", error=str(exc))


def _verify_database(db, insp):
    """验证数据库完整性"""
    tables = insp.get_table_names()
    expected_count = 40  # 不含 alembic_version
    actual = len([t for t in tables if t != 'alembic_version'])

    if actual >= expected_count:
        print(f"  [OK] 表数量: {actual}（预期 {expected_count}+）")
    else:
        print(f"  [WARN] 表数量: {actual}（预期 {expected_count}+），可能有遗漏")

    # 检查关键表
    critical = ['users', 'projects', 'api_test_cases', 'test_runs', 'organizations']
    for table in critical:
        if table in tables:
            cols = [c['name'] for c in insp.get_columns(table)]
            print(f"  [OK] {table}: {len(cols)} 列")
        else:
            print(f"  [FAIL] {table}: 表不存在！")


def reset_database(seed=False, force=False):
    """
    重置数据库

    流程：删除数据库 → 创建数据库 → 运行迁移 → 填充种子数据
    """
    from app import create_app

    app = create_app('development')

    with app.app_context():
        from app.extensions import db
        from app.core.logging import get_logger
        from sqlalchemy import inspect, text

        logger = get_logger(__name__)

        insp = inspect(db.engine)
        db_url = str(db.engine.url)

        # 安全检查：仅允许 SQLite 或开发数据库
        if 'fullscopetest.db' not in db_url and 'sqlite' not in db_url:
            print(f"[ERROR] 安全拒绝：当前数据库 URL 为 {db_url}")
            print("[ERROR] 此脚本仅允许操作 SQLite 或开发数据库")
            sys.exit(1)

        # 确认提示
        if not force:
            tables = insp.get_table_names()
            print(f"[WARNING] 即将重置数据库（{len(tables)} 张表）")
            print(f"[WARNING] 数据库: {db_url}")
            confirm = input("确认重置？输入 'yes' 继续: ")
            if confirm.lower() != 'yes':
                print("[INFO] 操作已取消")
                sys.exit(0)

        # Step 1: 删除所有表
        print("[1/4] 删除所有表...")
        if 'sqlite' in db_url:
            db.session.execute(text("PRAGMA foreign_keys = OFF"))
        for table in reversed(metadata_sorted_tables(db)):
            try:
                db.session.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
            except Exception as e:
                print(f"  [WARN] 删除表 {table} 失败: {e}")
        # 删除 alembic_version
        try:
            db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))
        except Exception:
            pass
        db.session.commit()
        print("  删除完成")

        # Step 2: 运行迁移
        print("[2/4] 运行迁移...")
        from alembic import command
        from alembic.config import Config as AlembicConfig

        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alembic_cfg = AlembicConfig(
            os.path.join(backend_dir, 'migrations', 'alembic.ini')
        )
        alembic_cfg.set_main_option(
            'script_location',
            os.path.join(backend_dir, 'migrations')
        )
        command.upgrade(alembic_cfg, 'head')

        tables = insp.get_table_names()
        print(f"  迁移完成，共 {len(tables)} 张表（含 alembic_version）")

        # Step 3: 种子数据（可选）
        if seed:
            print("[3/4] 填充种子数据...")
            _seed_data(app, db, logger)
            print("  种子数据填充完成")
        else:
            print("[3/4] 跳过种子数据（使用 --seed 启用）")

        # Step 4: 验证
        print("[4/4] 验证数据库...")
        _verify_database(db, insp)

        print("\n[DONE] 数据库重置完成！")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FullScopeTest 数据库重置脚本（开发环境）')
    parser.add_argument('--seed', action='store_true', help='填充种子数据')
    parser.add_argument('--force', action='store_true', help='跳过确认提示')
    args = parser.parse_args()

    reset_database(seed=args.seed, force=args.force)
