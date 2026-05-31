#!/bin/bash

# FullScopeTest 性能基准测试运行脚本
# 使用 Locust 对 Flask (v1) 和 FastAPI (v2) 接口进行性能对比测试

set -e

# 配置
HOST=${1:-"http://localhost:5000"}
USERS=${2:-10}
SPAWN_RATE=${3:-2}
DURATION=${4:-60}
REPORT_DIR="benchmark/reports/$(date +%Y%m%d_%H%M%S)"

# 创建报告目录
mkdir -p "$REPORT_DIR"

echo "=========================================="
echo "FullScopeTest 性能基准测试"
echo "=========================================="
echo "目标服务器: $HOST"
echo "并发用户数: $USERS"
echo "用户生成速率: $SPAWN_RATE 用户/秒"
echo "测试持续时间: $DURATION 秒"
echo "报告目录: $REPORT_DIR"
echo "=========================================="

# 检查 Locust 是否安装
if ! command -v locust &> /dev/null; then
    echo "错误: Locust 未安装"
    echo "请运行: pip install locust"
    exit 1
fi

# 运行 Flask (v1) 基准测试
echo ""
echo ">>> 运行 Flask (v1) 基准测试..."
locust -f benchmark/locustfile.py \
    --host="$HOST" \
    --users="$USERS" \
    --spawn-rate="$SPAWN_RATE" \
    --run-time="${DURATION}s" \
    --headless \
    --csv="$REPORT_DIR/flask_v1" \
    --html="$REPORT_DIR/flask_v1_report.html" \
    --only-summary

# 运行 FastAPI (v2) 基准测试
echo ""
echo ">>> 运行 FastAPI (v2) 基准测试..."
locust -f benchmark/locustfile.py \
    --host="$HOST" \
    --users="$USERS" \
    --spawn-rate="$SPAWN_RATE" \
    --run-time="${DURATION}s" \
    --headless \
    --csv="$REPORT_DIR/fastapi_v2" \
    --html="$REPORT_DIR/fastapi_v2_report.html" \
    --only-summary

# 运行混合负载测试
echo ""
echo ">>> 运行混合负载测试..."
locust -f benchmark/locustfile.py \
    --host="$HOST" \
    --users="$USERS" \
    --spawn-rate="$SPAWN_RATE" \
    --run-time="${DURATION}s" \
    --headless \
    --csv="$REPORT_DIR/mixed" \
    --html="$REPORT_DIR/mixed_report.html" \
    --only-summary

echo ""
echo "=========================================="
echo "基准测试完成!"
echo "报告已保存到: $REPORT_DIR"
echo "=========================================="
echo ""
echo "生成的文件:"
echo "  - Flask v1 CSV: $REPORT_DIR/flask_v1_stats.csv"
echo "  - Flask v1 HTML: $REPORT_DIR/flask_v1_report.html"
echo "  - FastAPI v2 CSV: $REPORT_DIR/fastapi_v2_stats.csv"
echo "  - FastAPI v2 HTML: $REPORT_DIR/fastapi_v2_report.html"
echo "  - 混合负载 CSV: $REPORT_DIR/mixed_stats.csv"
echo "  - 混合负载 HTML: $REPORT_DIR/mixed_report.html"
