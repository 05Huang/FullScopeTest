@echo off
setlocal enabledelayedexpansion

REM ========================================
REM 停止所有服务
REM ========================================

echo.
echo ========================================
echo   停止所有 EasyTest 服务
echo ========================================
echo.

set "COUNT=0"

REM 停止 Python 后端进程
echo 停止 Python 后端进程...
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "python.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
    set /a COUNT+=1
)
echo 已停止 !COUNT! 个 Python 进程
echo.

REM 停止 Celery 进程
set "COUNT=0"
echo 停止 Celery Worker...
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "celery.exe"') do (
    taskkill /F /PID %%i >nul 2>&1
    set /a COUNT+=1
)
echo 已停止 !COUNT! 个 Celery 进程
echo.

REM 停止 Redis（如果作为服务运行）
echo 尝试停止 Redis 服务...
net stop Redis >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Redis 服务已停止
) else (
    echo Redis 服务未运行或未安装
)
echo.

REM 停止 Nginx
echo 停止 Nginx...
taskkill /F /IM nginx.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Nginx 已停止
) else (
    echo Nginx 未运行
)
echo.

echo ========================================
echo   所有服务已停止
echo ========================================
echo.

endlocal
pause
