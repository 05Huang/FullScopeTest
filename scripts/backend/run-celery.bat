@echo off
REM Celery Worker 启动脚本 (Windows)

echo Starting Celery Worker...

REM 设置项目根目录绝对路径
set "PROJECT_ROOT=d:\AutoTestingLearingProject\EasyTest-Web"
cd /d "%PROJECT_ROOT%\backend"

REM 设置 Python 路径
set PYTHONPATH=%cd%

REM 设置 Celery broker 为 Redis
set CELERY_BROKER_URL=redis://localhost:6379/0
set CELERY_RESULT_BACKEND=redis://localhost:6379/0

REM 使用 solo 池（Windows 兼容）
"%PROJECT_ROOT%\backend\venv\Scripts\python.exe" -m celery -A app.extensions:celery -b redis://localhost:6379/0 worker --loglevel=info --pool=solo

pause
