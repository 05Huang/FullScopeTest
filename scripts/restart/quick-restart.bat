@echo off
setlocal enabledelayedexpansion

REM ========================================
REM 快速重启脚本
REM 功能：构建前端 + 重启后端
REM ========================================

echo.
echo ========================================
echo   EasyTest 快速重启
echo ========================================
echo.

REM 获取项目根目录
set "PROJECT_ROOT=%~dp0..\.."
cd /d "%PROJECT_ROOT%"

REM ========================================
REM 1. 停止后端进程
REM ========================================
echo [1/3] 停止现有后端进程...

REM 停止所有 python.exe 进程
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "python.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
)

echo 已停止后端进程
timeout /t 1 /nobreak >nul
echo.

REM ========================================
REM 2. 构建前端
REM ========================================
echo [2/3] 构建前端...

cd "%PROJECT_ROOT%web"

echo 正在构建前端...
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 前端构建失败！
    pause
    exit /b 1
)

echo.
echo 前端构建完成！
echo.

cd "%PROJECT_ROOT%"

REM ========================================
REM 3. 启动后端服务
REM ========================================
echo [3/3] 启动后端服务...

cd "%PROJECT_ROOT%"

echo.
echo ========================================
echo   后端服务启动中...
echo ========================================
echo.
echo 服务器地址: http://127.0.0.1:5211
echo.
echo 测试用户:
echo   用户名: admin
echo   密码: admin123
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

call scripts\backend\run-server.bat

endlocal
