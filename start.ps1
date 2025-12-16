# EasyTest 一键启动脚本
# 同时启动前端和后端服务

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   EasyTest 自动化测试平台启动中..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# 检查 Python 是否安装
Write-Host "[检查] Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 错误: 未找到 Python，请先安装 Python 3.10+" -ForegroundColor Red
    Write-Host "按任意键退出..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# 检查 Node.js 是否安装
Write-Host "[检查] Node.js 环境..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js 已安装: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 错误: 未找到 Node.js，请先安装 Node.js 18+" -ForegroundColor Red
    Write-Host "按任意键退出..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   正在启动服务..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 启动后端服务
Write-Host "[后端] 正在启动 Flask 服务..." -ForegroundColor Yellow
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    Set-Location '$scriptPath\backend'
    Write-Host '=====================================' -ForegroundColor Cyan
    Write-Host '   后端服务 (Flask)' -ForegroundColor Cyan
    Write-Host '=====================================' -ForegroundColor Cyan
    Write-Host ''
    Write-Host '启动后端服务在 http://localhost:5211' -ForegroundColor Green
    Write-Host ''
    
    # 检查虚拟环境
    if (Test-Path 'venv\Scripts\Activate.ps1') {
        Write-Host '[激活] Python 虚拟环境...' -ForegroundColor Yellow
        .\venv\Scripts\Activate.ps1
    } else {
        Write-Host '[警告] 未找到虚拟环境，使用全局 Python' -ForegroundColor Yellow
    }
    
    # 运行后端
    python app.py
"@ -PassThru

Start-Sleep -Seconds 2

# 启动前端服务
Write-Host "[前端] 正在启动 Vite 开发服务器..." -ForegroundColor Yellow
$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    Set-Location '$scriptPath\web'
    Write-Host '=====================================' -ForegroundColor Cyan
    Write-Host '   前端服务 (Vite)' -ForegroundColor Cyan
    Write-Host '=====================================' -ForegroundColor Cyan
    Write-Host ''
    Write-Host '启动前端服务...' -ForegroundColor Green
    Write-Host ''
    
    # 检查 node_modules
    if (-not (Test-Path 'node_modules')) {
        Write-Host '[安装] 检测到首次运行，正在安装依赖...' -ForegroundColor Yellow
        npm install
        Write-Host ''
    }
    
    # 运行前端
    npm run dev
"@ -PassThru

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "   ✓ 服务启动成功！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "后端地址: " -NoNewline
Write-Host "http://localhost:5211" -ForegroundColor Cyan
Write-Host "前端地址: " -NoNewline
Write-Host "http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示: 关闭此窗口不会停止服务，请分别关闭前后端窗口来停止服务" -ForegroundColor Yellow
Write-Host ""
Write-Host "按任意键退出此窗口（服务将继续运行）..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
