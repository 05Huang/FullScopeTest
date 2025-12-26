@echo off
REM 安装后端 Python 依赖

echo ========================================
echo   安装后端依赖
echo ========================================
echo.

cd /d "%~dp0..\..\backend"

echo 正在升级 pip...
venv\Scripts\python.exe -m pip install --upgrade pip
echo.

echo 正在安装 Python 依赖包...
echo 这可能需要几分钟，请耐心等待...
echo.

REM 使用 --no-build-isolation 和 --only-binary :all: 跳过需要编译的包
REM 如果失败，再尝试正常安装
echo [1/2] 尝试安装预编译包（跳过需要编译的包）...
venv\Scripts\python.exe -m pip install --only-binary :all: -r requirements.txt 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [注意] 某些包没有预编译版本，尝试完整安装...
    echo [2/2] 完整安装（可能需要编译某些包）...
    venv\Scripts\python.exe -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [警告] 部分包安装失败，但核心功能可能仍可正常使用
        echo 失败的包通常是：gevent, greenlet 等需要编译的包
        echo 这些包在 Windows 上不是必需的
        echo.
    )
)

echo.
echo ========================================
echo   依赖安装完成！
echo ========================================
echo.
echo 正在检查关键依赖...
echo.

REM 检查关键依赖
venv\Scripts\python.exe -c "import flask" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flask 已安装
) else (
    echo [错误] Flask 未安装，请检查网络连接
)

venv\Scripts\python.exe -c "import celery" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Celery 已安装
) else (
    echo [警告] Celery 未安装，异步任务功能将不可用
)

venv\Scripts\python.exe -c "import redis" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Redis 已安装
) else (
    echo [警告] Redis 未安装，缓存功能将不可用
)

venv\Scripts\python.exe -c "import playwright" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Playwright 已安装
) else (
    echo [警告] Playwright 未安装，Web 自动化测试功能将不可用
)

echo.
echo 现在可以启动后端服务了。
echo.

pause
