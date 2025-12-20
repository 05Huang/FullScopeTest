#!/usr/bin/env python
"""运行开发服务器的脚本"""
import sys
import os

# 确保当前目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == '__main__':
    app = create_app('development')
    print("Starting Flask development server...")
    print("Server will be available at http://127.0.0.1:5211")
    app.run(host='127.0.0.1', port=5211, debug=True, use_reloader=False)
