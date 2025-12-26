@echo off
REM EasyTest Nginx 启动脚本 (Windows)

chcp 65001 >nul

REM 设置项目根目录和 Nginx 路径
set "PROJECT_ROOT=d:\AutoTestingLearingProject\EasyTest-Web"
set "NGINX_HOME=D:\nginx"

cd /d "%PROJECT_ROOT%"

echo.
echo ========================================
echo     启动 Nginx 反向代理
echo ========================================
echo.

REM 检查 Nginx 是否已安装
if not exist "%NGINX_HOME%\nginx.exe" (
    echo [错误] 找不到 Nginx 可执行文件！
    echo 请确认 Nginx 已安装到: %NGINX_HOME%
    echo.
    echo 如需安装 Nginx：
    echo   1. 访问 https://nginx.org/en/download.html
    echo   2. 下载 Windows Stable 版本
    echo   3. 解压到 D:\nginx
    echo.
    pause
    exit /b 1
)

REM 检查是否已在运行
tasklist /FI "IMAGENAME eq nginx.exe" 2>nul | find /I /N "nginx.exe">nul
if "%ERRORLEVEL%"=="0" (
    echo [警告] Nginx 已在运行中！
    echo.
    echo 如需重启 Nginx，请先运行: %NGINX_HOME%\nginx.exe -s quit
    echo.
    pause
    exit /b 0
)

REM 检查前端是否已构建
if not exist "%PROJECT_ROOT%\web\dist" (
    echo [警告] 前端未构建！
    echo 正在构建前端...
    cd /d "%PROJECT_ROOT%\web"
    call npm run build
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] 前端构建失败！
        pause
        exit /b 1
    )
    echo [OK] 前端构建完成
    cd /d "%PROJECT_ROOT%"
)

echo Nginx 安装目录: %NGINX_HOME%
echo.

REM 备份原配置并复制项目配置
echo 配置 Nginx...
if exist "%NGINX_HOME%\conf\nginx.conf" (
    copy /Y "%NGINX_HOME%\conf\nginx.conf" "%NGINX_HOME%\conf\nginx.conf.bak" >nul
)
copy /Y "%PROJECT_ROOT%\nginx\nginx.conf" "%NGINX_HOME%\conf\nginx.conf" >nul
echo [OK] 配置文件已更新
echo.

REM 测试配置文件
echo 测试 Nginx 配置...
cd /d "%NGINX_HOME%"
nginx.exe -t
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Nginx 配置测试失败！
    echo 请检查 nginx.conf 配置是否正确
    pause
    exit /b 1
)
echo [OK] 配置测试通过
echo.

REM 启动 Nginx
echo 启动 Nginx 服务...
start "" nginx.exe

REM 等待启动
timeout /t 2 /nobreak >nul

REM 检查是否启动成功
tasklist /FI "IMAGENAME eq nginx.exe" 2>nul | find /I /N "nginx.exe">nul
if "%ERRORLEVEL%"=="0" (
    echo [OK] Nginx 启动成功！
    echo.
    echo ========================================
    echo   Nginx 服务信息
    echo ========================================
    echo   访问地址: http://localhost:8080
    echo   配置文件: %NGINX_HOME%\conf\nginx.conf
    echo   日志目录: %NGINX_HOME%\logs\
    echo.
    echo 常用命令:
    echo   停止: %NGINX_HOME%\nginx.exe -s quit
    echo   重载: %NGINX_HOME%\nginx.exe -s reload
    echo ========================================
    echo.
) else (
    echo [错误] Nginx 启动失败！
    echo 请查看日志: %NGINX_HOME%\logs\error.log
    pause
    exit /b 1
)

cd /d "%PROJECT_ROOT%"
