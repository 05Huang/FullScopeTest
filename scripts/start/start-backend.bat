@echo off
REM 启动后端服务器

setlocal enabledelayedexpansion

REM 设置项目根目录绝对路径
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..\..") do set "PROJECT_ROOT=%%~fI"
cd /d "%PROJECT_ROOT%"

echo ========================================
echo  EasyTest 后端服务器
echo ========================================
echo.
echo 启动中...
echo 服务器地址: http://127.0.0.1:5211
echo API 前缀: /api/v1
echo.
echo 测试用户:
echo   用户名: admin
echo   密码: admin123
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

cd "%PROJECT_ROOT%\backend"
set "PYTHON_EXE=%PROJECT_ROOT%\backend\venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"
"%PYTHON_EXE%" app.py
