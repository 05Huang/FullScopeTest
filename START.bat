@echo off
REM EasyTest 一键启动脚本（Windows）
REM 此脚本会在不同的终端中启动所有必需的服务

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ========================================
echo     EasyTest 一键启动脚本
echo ========================================
echo.
echo 本脚本将在多个终端中启动以下服务：
echo   1. Redis 服务器
echo   2. Celery Worker
echo   3. Flask 后端服务
echo   4. Nginx 反向代理
echo.
echo 注意：请确保已安装所有依赖
echo   - Python 3.10+
echo   - Node.js 18+
echo   - Redis
echo   - 已运行 pip install -r requirements.txt
echo   - 已运行 npm install 和 npm run build
echo.

REM 检查必要的目录
if not exist "backend" (
    echo [错误] 找不到 backend 文件夹，请在项目根目录运行此脚本
    pause
    exit /b 1
)

if not exist "nginx" (
    echo [错误] 找不到 nginx 文件夹，请检查项目结构
    pause
    exit /b 1
)

echo 按任意键继续启动...
pause

REM 启动 Redis
echo.
echo [1/4] 启动 Redis 服务器...
echo 请使用 redis-cli ping 命令验证 Redis 是否运行
timeout /t 2 /nobreak

REM 在新窗口中启动 Celery Worker
echo [2/4] 启动 Celery Worker...
cd /d "%~dp0backend"
start "EasyTest - Celery Worker" cmd /k ".\run_celery.bat"
timeout /t 3 /nobreak

REM 在新窗口中启动后端服务
echo [3/4] 启动后端服务...
start "EasyTest - Flask Backend" cmd /k ".\run_server.bat"
timeout /t 3 /nobreak

REM 在新窗口中启动 Nginx
echo [4/4] 启动 Nginx 反向代理...
cd /d "%~dp0nginx"
start "EasyTest - Nginx" cmd /k ".\start-nginx.bat"
timeout /t 2 /nobreak

REM 返回根目录
cd /d "%~dp0"

echo.
echo ========================================
echo     启动完成！
echo ========================================
echo.
echo 服务访问地址：
echo   • Web 应用: http://localhost:8080
echo   • 后端 API: http://127.0.0.1:5211/api/v1
echo.
echo 默认登录信息：
echo   • 用户名: admin
echo   • 密码: admin123
echo.
echo 请在浏览器中访问 http://localhost:8080 开始使用
echo.
echo 停止所有服务：
echo   1. 在各个终端窗口中按 Ctrl+C
echo   2. 或运行 nginx\stop-nginx.bat 停止 Nginx
echo.
echo 详细的启动说明请参考 document\STARTUP.md
echo ========================================
echo.

REM 检查关键服务是否启动
timeout /t 5 /nobreak
echo 检查服务状态...

REM 检查后端
for /f %%A in ('netstat -ano ^| findstr "127.0.0.1:5211" ^| findstr LISTENING ^| find /c /v ""') do (
    if %%A gtr 0 (
        echo ✓ 后端服务已启动 (端口 5211)
    ) else (
        echo ✗ 后端服务未启动 (端口 5211)
    )
)

REM 检查 Nginx
for /f %%A in ('netstat -ano ^| findstr "8080" ^| findstr LISTENING ^| find /c /v ""') do (
    if %%A gtr 0 (
        echo ✓ Nginx 已启动 (端口 8080)
    ) else (
        echo ✗ Nginx 未启动 (端口 8080)
    )
)

REM 检查 Redis
redis-cli ping >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Redis 已启动 (端口 6379)
) else (
    echo ✗ Redis 未启动 (端口 6379) - 请手动启动
    echo   Windows: D:\redis\redis-server.exe 或 redis-server
)

echo.
echo 按任意键关闭此窗口...
pause

endlocal
