@echo off
REM 启动后端服务器

setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

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

cd backend
backend\.venv\Scripts\python.exe app.py
