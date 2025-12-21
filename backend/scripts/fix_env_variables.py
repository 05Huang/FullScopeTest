"""
修复环境变量数据类型问题

解决数据库中 variables 字段被存储为字符串而不是对象的问题
"""

import sys
import os
import json

# 切换到 backend 目录并添加到 Python 路径
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from app import create_app
from app.extensions import db
from app.models.environment import Environment


def fix_variables():
    """修复 variables 字段类型"""
    app = create_app()

    with app.app_context():
        envs = Environment.query.all()
        print("=" * 60)
        print("Fix Environment Variables Data Type")
        print("=" * 60)

        for env in envs:
            print(f"\n环境 {env.id} ({env.name}):")

            # 检查 variables 类型
            if isinstance(env.variables, str):
                print(f"  - Current type: str (needs fix)")
                print(f"  - Current value (first 100 chars): {env.variables[:100]}...")

                try:
                    # 尝试解析 JSON 字符串
                    parsed = json.loads(env.variables)
                    env.variables = parsed
                    db.session.commit()
                    print(f"  [OK] Fixed to dict type, variable count: {len(parsed)}")
                except json.JSONDecodeError as e:
                    print(f"  [ERROR] JSON parse failed: {e}")
                    print(f"  - Clearing variables due to parse error")
                    env.variables = {}
                    db.session.commit()
                    print(f"  [OK] Variables cleared")

            elif isinstance(env.variables, dict):
                var_count = len(env.variables)
                print(f"  - Current type: dict (OK)")
                print(f"  - Variable count: {var_count}")

                # 显示变量列表
                if var_count > 0:
                    print(f"  - Variable list (first 5):")
                    for i, (key, value) in enumerate(list(env.variables.items())[:5], 1):
                        value_preview = str(value)[:50]
                        if len(value_preview) >= 50:
                            value_preview += "..."
                        print(f"    {i}. {key} = {value_preview}")
                    if var_count > 5:
                        print(f"    ... and {var_count - 5} more variables")
            else:
                print(f"  - Current type: {type(env.variables).__name__} (ERROR)")
                print(f"  - Clearing variables")
                env.variables = {}
                db.session.commit()

        print(f"\n{'=' * 60}")
        print("Fix Completed!")
        print("=" * 60)


if __name__ == '__main__':
    fix_variables()
