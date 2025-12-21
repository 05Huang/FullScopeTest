"""
环境变量数据检查脚本

用于检查数据库中环境配置的实际变量数据，
帮助诊断变量数量异常等问题。

使用方法：
    cd backend
    python scripts/check_env_variables.py           # 检查所有环境
    python scripts/check_env_variables.py --check    # 同上
    python scripts/check_env_variables.py --clean    # 清理异常数据
    python scripts/check_env_variables.py --clean --env-id 1  # 清理指定环境
"""

import sys
import os

# 切换到 backend 目录并添加到 Python 路径
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# 现在可以安全地导入 app 模块
from app import create_app
from app.extensions import db
from app.models.environment import Environment
from app.models.project import Project


def check_environments():
    """检查所有环境的变量数据"""
    app = create_app()
    total_vars = 0

    with app.app_context():
        envs = Environment.query.all()
        print("=" * 60)
        print("环境变量数据检查报告")
        print("=" * 60)
        print(f"\n总环境数: {len(envs)}")

        for env in envs:
            print(f"\n{'-' * 60}")
            print(f"环境 ID: {env.id}")
            print(f"环境名称: {env.name}")
            print(f"项目 ID: {env.project_id}")
            print(f"Base URL: {env.base_url}")

            # 检查 variables 字段
            print(f"\nvariables 字段信息:")
            print(f"  - 类型: {type(env.variables).__name__}")

            if env.variables is None:
                print(f"  - 值: None")
                var_count = 0
            elif isinstance(env.variables, dict):
                var_count = len(env.variables)
                total_vars += var_count
                print(f"  - 变量数量: {var_count}")

                if var_count > 0:
                    # 显示前10个变量
                    keys = list(env.variables.keys())
                    print(f"  - 变量列表 (前10个):")
                    for i, key in enumerate(keys[:10], 1):
                        value = env.variables[key]
                        value_preview = str(value)[:50]
                        if len(value_preview) >= 50:
                            value_preview += "..."
                        print(f"    {i}. {key} = {value_preview}")

                    if var_count > 10:
                        print(f"    ... 还有 {var_count - 10} 个变量")

                # 警告：变量数量过多
                if var_count > 100:
                    print(f"  ⚠️  警告: 变量数量过多 ({var_count} > 100)")

            elif isinstance(env.variables, list):
                var_count = len(env.variables)
                print(f"  - 数组长度: {var_count}")
                print(f"  - 前5项: {env.variables[:5]}")
                print(f"  ⚠️  警告: variables 是数组类型，应该是对象类型！")
            else:
                print(f"  - 值: {env.variables}")
                print(f"  ⚠️  警告: variables 类型异常！")

            # 检查 headers 字段
            print(f"\nheaders 字段信息:")
            if env.headers is None:
                print(f"  - 值: None")
            elif isinstance(env.headers, dict):
                print(f"  - Headers 数量: {len(env.headers)}")
            else:
                print(f"  - 类型: {type(env.headers).__name__}")

        print(f"\n{'=' * 60}")
        print("总结")
        print("=" * 60)
        print(f"总环境数: {len(envs)}")
        print(f"总变量数: {total_vars}")
        print(f"平均每环境变量数: {total_vars / len(envs) if envs else 0:.1f}")

        # 检查是否有异常数据
        print(f"\n异常检查:")
        has_issues = False
        for env in envs:
            issues = []

            if isinstance(env.variables, list):
                issues.append("variables 是数组类型")

            if isinstance(env.variables, dict) and len(env.variables) > 100:
                issues.append(f"变量数量过多 ({len(env.variables)})")

            if env.variables is None:
                issues.append("variables 为 None")

            if issues:
                has_issues = True
                print(f"  ⚠️  环境 {env.id} ({env.name}): {', '.join(issues)}")

        if not has_issues:
            print(f"  ✓ 未发现异常数据")

        print(f"\n{'=' * 60}")


def clean_environment_variables(env_id=None, max_vars=100):
    """
    清理环境变量数据

    Args:
        env_id: 环境 ID，如果不指定则清理所有环境
        max_vars: 保留的最大变量数量
    """
    app = create_app()

    with app.app_context():
        if env_id:
            envs = [Environment.query.get(env_id)]
            if not envs[0]:
                print(f"错误: 环境 ID {env_id} 不存在")
                return
        else:
            envs = Environment.query.all()

        print("=" * 60)
        print("清理环境变量数据")
        print("=" * 60)

        for env in envs:
            modified = False

            # 修复数组类型
            if isinstance(env.variables, list):
                print(f"\n环境 {env.id} ({env.name}):")
                print(f"  - 变量是数组类型，转换为空对象")
                env.variables = {}
                modified = True

            # 限制变量数量
            elif isinstance(env.variables, dict) and len(env.variables) > max_vars:
                original_count = len(env.variables)
                print(f"\n环境 {env.id} ({env.name}):")
                print(f"  - 变量从 {original_count} 个减少到 {max_vars} 个")
                keys = list(env.variables.keys())[:max_vars]
                env.variables = {k: env.variables[k] for k in keys}
                modified = True

            if modified:
                db.session.commit()
                print(f"  ✓ 已保存")
            else:
                print(f"\n环境 {env.id} ({env.name}): 无需修改")

        print(f"\n{'=' * 60}")
        print("清理完成！")
        print("=" * 60)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='环境变量数据检查和清理工具')
    parser.add_argument('--check', action='store_true', help='检查环境变量数据')
    parser.add_argument('--clean', action='store_true', help='清理异常数据')
    parser.add_argument('--env-id', type=int, help='指定环境 ID')
    parser.add_argument('--max-vars', type=int, default=100, help='最大变量数量 (默认: 100)')

    args = parser.parse_args()

    if args.check:
        check_environments()
    elif args.clean:
        clean_environment_variables(args.env_id, args.max_vars)
    else:
        # 默认执行检查
        print("提示: 使用 --clean 参数可以清理异常数据\n")
        check_environments()
