@echo off
cd /d "%~dp0"
set PYTHONPATH=%CD%

echo 启动 EasyTest 后端服务器...
echo 地址: http://127.0.0.1:5211

REM 使用虚拟环境的 Python
.\.venv\Scripts\python.exe -u run_dev.py

pause
