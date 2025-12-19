@echo off
REM EasyTest Nginx 停止脚本

set NGINX_PATH=D:\nginx

echo 正在停止 Nginx...
cd /d "%NGINX_PATH%"
nginx.exe -s stop

echo Nginx 已停止
pause
