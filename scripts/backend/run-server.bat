@echo off
REM 后端生产模式启动脚本

REM 设置项目根目录绝对路径
set "PROJECT_ROOT=d:\AutoTestingLearingProject\EasyTest-Web"
cd /d "%PROJECT_ROOT%\backend"

REM 设置工作目录
set "PYTHONPATH=%CD%"

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

"%PROJECT_ROOT%\backend\venv\Scripts\python.exe" app.py
