@echo off
setlocal enabledelayedexpansion

REM ========================================
REM EasyTest 一键重启脚本
REM 功能：构建前端 + 重启后端服务
REM ========================================

echo.
echo ========================================
echo   EasyTest 一键重启
echo ========================================
echo.

REM 获取项目根目录
set "PROJECT_ROOT=%~dp0..\.."
cd /d "%PROJECT_ROOT%"

REM ========================================
REM 1. 停止现有服务
REM ========================================
echo [1/5] 停止现有服务...

REM 停止 Python 后端进程
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "python.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
)

REM 停止 Celery 进程
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "celery.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
)

REM 尝试停止 Redis（如果作为 Windows 服务运行）
net stop Redis >nul 2>&1

echo 已停止现有服务
echo.

REM ========================================
REM 2. 启动 Redis
REM ========================================
echo [2/5] 启动 Redis...

REM 检查 Redis 是否已安装
where redis-server >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [警告] Redis 未找到，请手动启动 Redis
    echo 如果使用 Redis for Windows，请运行：redis-server.exe
    echo.
) else (
    REM 在后台启动 Redis
    start /B redis-server >nul 2>&1
    echo Redis 已启动
)

timeout /t 2 /nobreak >nul
echo.

REM ========================================
REM 3. 构建前端
REM ========================================
echo [3/5] 构建前端...

cd "%PROJECT_ROOT%web"

if not exist "node_modules" (
    echo 首次运行，正在安装依赖...
    call npm install
)

echo 正在构建前端...
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 前端构建失败！
    pause
    exit /b 1
)

echo 前端构建完成
echo.

cd "%PROJECT_ROOT%"

REM ========================================
REM 4. 启动 Celery Worker
REM ========================================
echo [4/5] 启动 Celery Worker...

REM 在新窗口启动 Celery
start "Celery Worker" cmd /k "cd /d "%PROJECT_ROOT%" && call scripts\backend\run-celery.bat"

echo Celery Worker 已启动（新窗口）
echo.

REM ========================================
REM 5. 启动后端服务
REM ========================================
echo [5/5] 启动后端服务...

REM 在当前窗口启动后端
echo.
echo ========================================
echo   后端服务启动中...
echo ========================================
echo.
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

REM 启动后端
call scripts\backend\run-server.bat

endlocal
