#!/bin/bash

echo "======================================"
echo "  接口测试平台 - Web 版"
echo "======================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.7+"
    exit 1
fi

echo "[信息] 检测到 Python✓"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "[信息] 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "[信息] 安装依赖包..."
pip install -r requirements.txt

# 启动应用
echo ""
echo "======================================"
echo "  应用启动中..."
echo "======================================"
echo ""
echo "📍 访问地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python app.py

deactivate
