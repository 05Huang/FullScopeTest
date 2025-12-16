"""
WSGI 入口文件

用于启动 Flask 应用
"""

import os
from app import create_app

# 从环境变量获取配置，默认为开发环境
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5211)
