@echo off
REM 后端开发模式启动脚本

set "PROJECT_ROOT=%~dp0..\.."
cd /d "%PROJECT_ROOT%\backend"
set PYTHONPATH=%CD%

echo 启动 EasyTest 后端开发服务器...
echo 地址: http://127.0.0.1:5211

REM 使用虚拟环境的 Python
.\.venv\Scripts\python.exe -u run_dev.py

pause
