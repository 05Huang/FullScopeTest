@echo off
REM EasyTest 一键启动脚本（Windows）
REM 此脚本会在不同的终端中启动所有必需的服务

chcp 65001 >nul

REM 设置项目根目录绝对路径
set "PROJECT_ROOT=d:\AutoTestingLearingProject\EasyTest-Web"
cd /d "%PROJECT_ROOT%"

echo.
echo ========================================
echo     EasyTest 一键启动脚本
echo ========================================
echo.
echo 本脚本将在多个终端中启动以下服务：
echo   1. Celery Worker
echo   2. Flask 后端服务
echo   3. Nginx 反向代理
echo.
echo 注意：请确保已安装所有依赖
echo   - Python 3.10+
echo   - Node.js 18+
echo   - Redis (需手动启动: D:\redis-windows\redis-server.exe redis.windows.conf)
echo   - 已运行 pip install -r requirements.txt
echo   - 已运行 npm install 和 npm run build
echo.

REM 检查 Python 依赖是否已安装
echo 检查 Python 依赖...
"%PROJECT_ROOT%\backend\venv\Scripts\python.exe" -c "import celery" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [警告] Celery 模块未安装！
    echo 正在运行核心依赖安装脚本...
    call "%PROJECT_ROOT%\scripts\backend\install-core-deps.bat"
    echo.
)
echo [OK] Python 依赖检查完成
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

echo 按任意键继续启动... (Press any key to continue...)
pause

echo.
echo [注意] 请确保 Redis 已手动启动
echo   运行: D:\redis-windows\redis-server.exe redis.windows.conf
echo.

REM 在新窗口中启动后端服务（先启动后端，以便 Celery 连接成功）
echo [1/3] 启动后端服务...
start "EasyTest - Flask Backend" cmd /k %PROJECT_ROOT%\scripts\backend\run-server.bat
timeout /t 3 /nobreak

REM 在新窗口中启动 Celery Worker（如果 Redis 已就绪更有可能连接成功）
echo [2/3] 启动 Celery Worker...
start "EasyTest - Celery Worker" cmd /k %PROJECT_ROOT%\scripts\backend\run-celery.bat
timeout /t 3 /nobreak

REM 在新窗口中启动 Nginx
echo [3/3] 启动 Nginx 反向代理...
start "EasyTest - Nginx" cmd /k %PROJECT_ROOT%\scripts\start\start-nginx.bat
timeout /t 2 /nobreak

echo.
echo ========================================
echo     启动完成！
echo ========================================
echo.
echo 服务访问地址：
echo   - Web 应用: http://localhost:8080
echo   - 后端 API: http://127.0.0.1:5211/api/v1
echo.
echo 默认登录信息：
echo   - 用户名: admin
echo   - 密码: admin123
echo.
echo 请在浏览器中访问 http://localhost:8080 开始使用
echo.
echo 停止所有服务：
echo   1. 在各个终端窗口中按 Ctrl+C
echo   2. 或运行 scripts\stop\stop-all.bat
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
        echo [OK] 后端服务已启动 (端口 5211)
    ) else (
        echo [!] 后端服务未启动 (端口 5211)
    )
)

REM 检查 Nginx
for /f %%A in ('netstat -ano ^| findstr "8080" ^| findstr LISTENING ^| find /c /v ""') do (
    if %%A gtr 0 (
        echo [OK] Nginx 已启动 (端口 8080)
    ) else (
        echo [!] Nginx 未启动 (端口 8080)
    )
)

echo.
echo ========================================
echo 启动检查已完成 — 父窗口保持打开以便查看日志 (Startup check complete - parent window will remain open for logs)
echo ========================================

echo 子窗口（后端 / Celery / Nginx）应在各自窗口运行。 (Child windows for services should be running separately)
echo 注意：Redis 需要手动启动 (Redis needs to be started manually)
echo 输入 'quit' 并回车以关闭此脚本并退出父窗口；输入其它内容会显示服务状态。 (Type 'quit' then Enter to exit; press Enter or any other key to show status)

:WAIT_CMD
set /p USER_CMD=命令 (quit 退出, 回车或任意键显示状态):
if /i "%USER_CMD%"=="quit" goto FINISH

echo.
echo 正在检查服务状态...

REM 检查后端
for /f %%A in ('netstat -ano ^| findstr "127.0.0.1:5211" ^| findstr LISTENING ^| find /c /v ""') do (
    if %%A gtr 0 (
        echo [OK] 后端服务已启动 (端口 5211)
    ) else (
        echo [!] 后端服务未启动 (端口 5211)
    )
)

REM 检查 Nginx
for /f %%A in ('netstat -ano ^| findstr "8080" ^| findstr LISTENING ^| find /c /v ""') do (
    if %%A gtr 0 (
        echo [OK] Nginx 已启动 (端口 8080)
    ) else (
        echo [!] Nginx 未启动 (端口 8080)
    )
)

echo.
goto WAIT_CMD

:FINISH
