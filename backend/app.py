"""
Flask 应用入口文件
"""

# 必须在任何导入之前强制设置环境变量（不依赖外部批处理）
import os

# 强制启用 Celery（覆盖任何外部设置）
os.environ['CELERY_ENABLE'] = 'true'

from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5211, debug=True, use_reloader=False)
