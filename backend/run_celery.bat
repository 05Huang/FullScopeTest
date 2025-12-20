@echo off
REM Celery Worker 启动脚本 (Windows)

echo Starting Celery Worker...

REM 切换到 backend 目录
cd /d %~dp0

REM 设置 Python 路径
set PYTHONPATH=%cd%

REM 使用 solo 池（Windows 兼容）
python -m celery -A app.extensions:celery worker --loglevel=info --pool=solo

pause
