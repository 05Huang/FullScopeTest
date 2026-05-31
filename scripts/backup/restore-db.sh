#!/bin/bash
# FullScopeTest 数据库恢复脚本
# 用法: ./restore-db.sh <backup_file>
# 例如: ./restore-db.sh /data/backups/fullscopetest/fullscopetest_20260531_020000.dump

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "用法: $0 <backup_file>"
    echo "例如: $0 /data/backups/fullscopetest/fullscopetest_20260531_020000.dump"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "错误: 备份文件不存在: ${BACKUP_FILE}"
    exit 1
fi

# 数据库连接信息
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-fullscopetest_prod}"
DB_USER="${POSTGRES_USER:-fullscopetest}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  警告: 此操作将覆盖当前数据库！"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 备份文件: ${BACKUP_FILE}"
read -p "确认恢复? (yes/no): " CONFIRM

if [ "${CONFIRM}" != "yes" ]; then
    echo "已取消恢复操作"
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始恢复数据库..."

# 先备份当前数据库
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 备份当前数据库..."
PRE_RESTORE_FILE="/tmp/fullscopetest_pre_restore_$(date +%Y%m%d_%H%M%S).dump"
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    --format=custom -f "${PRE_RESTORE_FILE}"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 当前数据库已备份到: ${PRE_RESTORE_FILE}"

# 恢复数据库
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 恢复中..."
pg_restore -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    --clean --if-exists "${BACKUP_FILE}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 数据库恢复完成"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 恢复前的备份保留在: ${PRE_RESTORE_FILE}"
