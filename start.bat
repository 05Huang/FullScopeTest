@echo off
chcp 65001 >nul
REM EasyTest 一键启动脚本（批处理版本）

echo =====================================
echo    EasyTest 自动化测试平台启动中...
echo =====================================
echo.

REM 获取脚本所在目录
cd /d "%~dp0"

REM 检查 PowerShell 是否可用
where powershell >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [启动] 使用 PowerShell 脚本启动...
    powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"
) else (
    echo [警告] 未找到 PowerShell，使用基础启动模式...
    echo.
    
    REM 启动后端
    echo [后端] 正在启动 Flask 服务...
    start "EasyTest-Backend" cmd /k "cd /d %~dp0backend && if exist venv\Scripts\activate.bat (venv\Scripts\activate.bat) && python app.py"
    
    timeout /t 2 /nobreak >nul
    
    REM 启动前端
    echo [前端] 正在启动 Vite 开发服务器...
    start "EasyTest-Frontend" cmd /k "cd /d %~dp0web && npm run dev"
    
    echo.
    echo =====================================
    echo    ✓ 服务启动成功！
    echo =====================================
    echo.
    echo 后端地址: http://localhost:5211
    echo 前端地址: http://localhost:5173
    echo.
    echo 提示: 请分别关闭前后端窗口来停止服务
    echo.
)

pause
