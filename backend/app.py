"""
Flask 应用入口文件（带自动重启功能）
"""
import os
import subprocess
import sys
import time

# 强制启用 Celery
os.environ['CELERY_ENABLE'] = 'true'

# 配置项
PORT = 5211
HOST = '0.0.0.0'

def kill_process_on_port(port):
    """终止占用指定端口的进程（Windows）"""
    try:
        # 查找占用端口的PID
        result = subprocess.check_output(
            f'netstat -ano | findstr :{port}',
            shell=True,
            encoding='gbk'  # Windows默认编码
        )
        # 提取PID（取最后一列数字）
        lines = result.strip().split('\n')
        for line in lines:
            if 'LISTENING' in line:
                pid = line.strip().split()[-1]
                # 终止进程
                subprocess.run(f'taskkill /F /PID {pid}', shell=True)
                print(f"已终止占用{port}端口的进程（PID: {pid}）")
                time.sleep(1)  # 等待进程退出
                break
    except subprocess.CalledProcessError:
        # 端口未被占用，无需处理
        print(f"{port}端口未被占用，无需终止进程")
    except Exception as e:
        print(f"终止进程时出错：{e}")

# 第一步：终止旧进程
kill_process_on_port(PORT)

# 第二步：加载环境变量
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)
else:
    load_dotenv(override=True)

# 第三步：启动Flask应用
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print(f"启动Flask服务：{HOST}:{PORT}")
    app.run(
        host=HOST,
        port=PORT,
        debug=True,
        use_reloader=False
    )