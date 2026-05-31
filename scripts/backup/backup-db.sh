#!/bin/bash
# FullScopeTest 数据库自动备份脚本
# 用法: ./backup-db.sh [backup_dir]
# 建议通过 cron 定期执行: 0 2 * * * /path/to/backup-db.sh /path/to/backups

set -euo pipefail

# 配置
BACKUP_DIR="${1:-/data/backups/fullscopetest}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/fullscopetest_${TIMESTAMP}.sql.gz"
KEEP_DAYS=30  # 保留最近 30 天的备份

# 数据库连接信息（从环境变量读取）
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-fullscopetest_prod}"
DB_USER="${POSTGRES_USER:-fullscopetest}"

# 创建备份目录
mkdir -p "${BACKUP_DIR}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始备份数据库..."

# 执行备份
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
  --format=custom --compress=9 \
  -f "${BACKUP_DIR}/fullscopetest_${TIMESTAMP}.dump"

# 同时生成 SQL 文本备份（便于手动恢复）
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
  | gzip > "${BACKUP_FILE}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 备份完成: ${BACKUP_FILE}"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 备份文件大小: $(du -h "${BACKUP_FILE}" | cut -f1)"

# 清理过期备份
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 清理 ${KEEP_DAYS} 天前的备份..."
find "${BACKUP_DIR}" -name "fullscopetest_*" -type f -mtime +${KEEP_DAYS} -delete
REMAINING=$(find "${BACKUP_DIR}" -name "fullscopetest_*" -type f | wc -l)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 清理完成，剩余 ${REMAINING} 个备份文件"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 数据库备份任务完成"
