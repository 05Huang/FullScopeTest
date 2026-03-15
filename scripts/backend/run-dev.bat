@echo off
REM 后端开发模式启动脚本

4REM 设置项目根目录绝对路径
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..\..") do set "PROJECT_ROOT=%%~fI"
cd /d "%PROJECT_ROOT%\backend"
set PYTHONPATH=%CD%

echo 启动 EasyTest 后端开发服务器...
echo 地址: http://127.0.0.1:5211

REM 使用虚拟环境的 Python
set "PYTHON_EXE=%PROJECT_ROOT%\backend\venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"
"%PYTHON_EXE%" -u run_dev.py

pause
