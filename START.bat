@echo off
REM EasyTest 一键启动（简化版）
REM 调用完整启动脚本

REM 获取脚本所在目录作为项目根目录
set "PROJECT_ROOT=%~dp0"

REM 去除路径末尾的反斜杠
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM 调用启动脚本
call "%PROJECT_ROOT%\scripts\start\start-all.bat"
