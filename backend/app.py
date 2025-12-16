"""
Flask 应用入口文件
"""
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5211, debug=True)
