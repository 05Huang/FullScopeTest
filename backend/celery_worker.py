"""
Celery Worker 启动脚本

启动 Celery 工作进程来执行异步任务
"""

import sys
import os

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import celery

# 创建 Flask 应用
app = create_app('development')

# 导入任务模块（确保任务被注册）
import app.tasks

if __name__ == '__main__':
    # 启动 Celery worker
    # 使用方式: python celery_worker.py
    celery.start()
