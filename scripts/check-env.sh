#!/usr/bin/env bash
# check-env.sh — 检查 .env 文件是否被 git 追踪
# 用法: bash scripts/check-env.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ERRORS=0

echo "=== .env 安全检查 ==="
echo ""

# 1. 检查 .env 文件是否被 git 追踪
echo "1. 检查 .env 文件是否被 git 追踪..."
TRACKED_ENV_FILES=$(git ls-files '*.env' '.env' 'backend/.env' 2>/dev/null || true)
if [ -n "$TRACKED_ENV_FILES" ]; then
    echo -e "${RED}✗ 以下 .env 文件已被 git 追踪:${NC}"
    echo "$TRACKED_ENV_FILES"
    echo "  请执行: git rm --cached <file>"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ 没有 .env 文件被 git 追踪${NC}"
fi
echo ""

# 2. 检查 .gitignore 是否包含 .env 规则
echo "2. 检查 .gitignore 规则..."
if grep -qE '^\s*\.env\s*$' .gitignore 2>/dev/null; then
    echo -e "${GREEN}✓ .gitignore 包含 .env 规则${NC}"
else
    echo -e "${RED}✗ .gitignore 缺少 .env 规则${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. 检查 .env 文件中是否有明显的真实密钥
echo "3. 检查 .env 文件中的可疑密钥..."
for env_file in .env backend/.env; do
    if [ -f "$env_file" ]; then
        # 检查是否包含看起来像真实 API Key 的值
        SUSPICIOUS=$(grep -nE '(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|[a-f0-9]{32,})' "$env_file" 2>/dev/null || true)
        if [ -n "$SUSPICIOUS" ]; then
            echo -e "${YELLOW}⚠ $env_file 中可能包含真实密钥:${NC}"
            echo "$SUSPICIOUS"
            echo "  建议替换为占位符（如 <your-api-key>）"
        else
            echo -e "${GREEN}✓ $env_file 未发现可疑密钥${NC}"
        fi
    fi
done
echo ""

# 4. 检查 .env.example 是否存在
echo "4. 检查 .env.example 文件..."
for example_file in .env.example backend/.env.example; do
    if [ -f "$example_file" ]; then
        echo -e "${GREEN}✓ $example_file 存在${NC}"
    else
        echo -e "${YELLOW}⚠ $example_file 不存在${NC}"
    fi
done
echo ""

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}发现 $ERRORS 个问题，请修复后重试。${NC}"
    exit 1
else
    echo -e "${GREEN}所有检查通过。${NC}"
    exit 0
fi
