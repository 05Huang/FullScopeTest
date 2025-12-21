@echo off
REM EasyTest Nginx 启动脚本
REM 请修改 NGINX_PATH 为你的 Nginx 安装路径

set NGINX_PATH=D:\nginx

echo ================================
echo EasyTest Nginx 启动脚本
echo ================================

REM 检查 Nginx 是否存在
if not exist "%NGINX_PATH%\nginx.exe" (
    echo [错误] 未找到 Nginx，请检查路径: %NGINX_PATH%
    echo 请从 https://nginx.org/en/download.html 下载安装
    pause
    exit /b 1
)

REM 复制配置文件
echo [1/3] 复制配置文件...
copy /Y "%~dp0..\..\nginx\nginx.conf" "%NGINX_PATH%\conf\nginx.conf" >nul
if %errorlevel% neq 0 (
    echo [错误] 配置文件复制失败
    pause
    exit /b 1
)

REM 测试配置
echo [2/3] 测试配置文件...
cd /d "%NGINX_PATH%"
nginx.exe -t
if %errorlevel% neq 0 (
    echo [错误] 配置文件有误，请检查
    pause
    exit /b 1
)

REM 启动或重载 Nginx
echo [3/3] 启动 Nginx...
tasklist /FI "IMAGENAME eq nginx.exe" 2>NUL | find /I /N "nginx.exe" >NUL
if %errorlevel% equ 0 (
    echo Nginx 已在运行，执行重载...
    nginx.exe -s reload
) else (
    echo 启动 Nginx...
    start /B nginx.exe
)

echo.
echo ================================
echo Nginx 已启动！
echo 开发环境: http://localhost
echo 生产环境: http://localhost:8080
echo ================================
echo.
echo 常用命令:
echo   停止: nginx.exe -s stop
echo   重载: nginx.exe -s reload
echo ================================

pause
