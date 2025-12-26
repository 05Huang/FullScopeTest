@echo off
REM 安装核心 Python 依赖（跳过需要编译的包）

echo ========================================
echo   安装核心依赖
echo ========================================
echo.

cd /d "%~dp0..\..\backend"

echo 正在升级 pip...
venv\Scripts\python.exe -m pip install --upgrade pip
echo.

echo 正在安装核心依赖包（跳过需要编译的包）...
echo.

REM 只安装核心依赖，不安装需要编译的包
echo [1/6] 安装 Flask 相关...
venv\Scripts\python.exe -m pip install Flask Flask-CORS Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended
echo.

echo [2/6] 安装数据库驱动...
venv\Scripts\python.exe -m pip install psycopg2-binary SQLAlchemy
echo.

echo [3/6] 安装 Celery 和 Redis...
venv\Scripts\python.exe -m pip install celery redis
echo.

echo [4/6] 安装 HTTP 库...
venv\Scripts\python.exe -m pip install requests httpx
echo.

echo [5/6] 安装工具库...
venv\Scripts\python.exe -m pip install python-dotenv PyYAML Werkzeug
echo.

echo [6/6] 安装测试框架...
venv\Scripts\python.exe -m pip install pytest pytest-asyncio
echo.

echo ========================================
echo   核心依赖安装完成！
echo ========================================
echo.
echo 正在检查关键依赖...
echo.

venv\Scripts\python.exe -c "import flask" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flask 已安装
) else (
    echo [错误] Flask 未安装
)

venv\Scripts\python.exe -c "import celery" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Celery 已安装
) else (
    echo [错误] Celery 未安装
)

venv\Scripts\python.exe -c "import redis" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Redis 客户端已安装
) else (
    echo [错误] Redis 客户端未安装
)

echo.
echo 注意：以下功能需要额外安装
echo   - Playwright (Web 自动化): 运行 venv\Scripts\pip install playwright
echo   - Locust (性能测试): 可能需要安装 C++ 编译器
echo.

pause
