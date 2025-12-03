@echo off
REM Windows 启动脚本

echo ======================================
echo   接口测试平台 - Web 版
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [信息] 检测到 Python✓

REM 检查虚拟环境
if not exist "venv" (
    echo [信息] 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo [信息] 安装依赖包...
pip install -r requirements.txt

REM 启动应用
echo.
echo ======================================
echo   应用启动中...
echo ======================================
echo.
echo 📍 访问地址: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务
echo.

python app.py

pause
