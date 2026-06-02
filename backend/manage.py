"""
Flask CLI 管理命令

提供数据库初始化等管理命令
"""

import click
from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash


def create_cli_app():
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    """FullScopeTest 管理命令"""
    pass


@cli.command()
def init_db():
    """初始化数据库表"""
    db.create_all()
    click.echo('✅ 数据库表创建成功！')


@cli.command()
@click.option('--username', prompt='用户名', help='管理员用户名')
@click.option('--email', prompt='邮箱', help='管理员邮箱')
@click.option('--password', prompt='密码', hide_input=True, confirmation_prompt=True, help='管理员密码')
def create_admin(username, email, password):
    """创建管理员账号"""
    # 检查是否已存在
    if User.query.filter_by(username=username).first():
        click.echo('❌ 用户名已存在！')
        return
    
    if User.query.filter_by(email=email).first():
        click.echo('❌ 邮箱已被使用！')
        return
    
    # 创建用户
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    
    click.echo(f'✅ 管理员账号 {username} 创建成功！')


@cli.command()
def drop_db():
    """删除所有数据库表（危险操作）"""
    if click.confirm('⚠️ 确定要删除所有数据库表吗？此操作不可逆！'):
        db.drop_all()
        click.echo('✅ 所有数据库表已删除！')


@cli.command()
def seed():
    """初始化默认数据（Prompt 版本等）"""
    from sqlalchemy import inspect as sa_inspect
    from app.models.prompt_version import PromptVersion
    from app.services.ai.script_generator import (
        DEFAULT_WEB_SYSTEM_PROMPT,
        DEFAULT_PERF_SYSTEM_PROMPT,
    )

    # 检查表是否存在
    try:
        inspector = sa_inspect(db.engine)
        if not inspector.has_table("prompt_versions"):
            click.echo('❌ prompt_versions 表不存在，请先运行 init_db')
            return
    except Exception as e:
        click.echo(f'❌ 数据库连接失败: {e}')
        return

    defaults = [
        ('script_gen_web', 'baseline', DEFAULT_WEB_SYSTEM_PROMPT),
        ('script_gen_perf', 'baseline', DEFAULT_PERF_SYSTEM_PROMPT),
    ]

    seeded_count = 0
    for feature, name, system_prompt in defaults:
        existing = PromptVersion.query.filter_by(feature=feature, version=1).first()
        if not existing:
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
            seeded_count += 1
            click.echo(f'  ✅ 创建 {feature} baseline prompt')

    if seeded_count > 0:
        db.session.commit()
        click.echo(f'✅ 成功初始化 {seeded_count} 个默认 Prompt 版本')
    else:
        click.echo('ℹ️ 所有默认 Prompt 版本已存在，无需初始化')


if __name__ == '__main__':
    cli()
