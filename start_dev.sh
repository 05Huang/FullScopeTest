#!/bin/bash
echo "========================================"
echo "FullScopeTest 开发环境启动脚本"
echo "========================================"
echo

# 支持两种模式：Docker 一键启动 或 本地进程启动
# 使用 --docker 参数启用 Docker 模式
if [ "$1" = "--docker" ]; then
    echo "[Docker] 一键启动所有服务..."
    docker-compose -f docker-compose.dev.yml up --build
    exit 0
fi

echo "[1/3] 启动数据库服务 (Redis)..."
docker-compose -f docker-compose.dev.yml up -d redis
sleep 3

echo "[2/3] 启动后端服务 (Flask)..."
cd backend
if [ -d "venv" ]; then
    source venv/Scripts/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
fi
flask run --host=0.0.0.0 --port=5000 --reload &
BACKEND_PID=$!
cd ..

echo "[3/3] 启动前端服务 (React/Vite)..."
cd web
npm run dev &
FRONTEND_PID=$!
cd ..

echo
echo "========================================"
echo "服务启动完成！"
echo "========================================"
echo
echo "访问地址:"
echo "  前端: http://localhost:3001"
echo "  后端: http://localhost:5000"
echo "  健康检查: http://localhost:5000/health"
echo
echo "Docker 一键启动: ./start_dev.sh --docker"
echo "清理 Docker 环境: docker-compose -f docker-compose.dev.yml down -v"
echo
echo "按 Ctrl+C 停止所有服务"
echo

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait
