#!/usr/bin/env bash
# FullScopeTest 数据备份脚本
#
# 功能：
#   - PostgreSQL 全量备份（pg_dump），保留 7 天
#   - Redis RDB 快照备份
#   - 文件存储（uploads/、reports/）备份
#   - 备份文件压缩和日期命名
#
# 用法：
#   ./scripts/backup.sh              # 执行备份
#   ./scripts/backup.sh --restore    # 恢复最近一次备份
#
# 环境变量：
#   BACKUP_DIR        — 备份输出目录（默认 ./backups）
#   BACKUP_RETENTION  — 保留天数（默认 7）
#   DATABASE_URL      — PostgreSQL 连接 URL
#   REDIS_URL         — Redis 连接 URL（可选）

set -euo pipefail

# ── 配置 ──────────────────────────────────────────────────────────────────────

BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_RETENTION="${BACKUP_RETENTION:-7}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/${DATE}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ── 创建备份目录 ──────────────────────────────────────────────────────────────

mkdir -p "${BACKUP_PATH}"
log_info "备份目录: ${BACKUP_PATH}"

# ── PostgreSQL 备份 ───────────────────────────────────────────────────────────

backup_postgres() {
    log_info "开始 PostgreSQL 备份..."

    local pg_dump_file="${BACKUP_PATH}/postgres_${DATE}.sql.gz"

    if command -v pg_dump &> /dev/null; then
        # 使用 pg_dump
        if [ -n "${DATABASE_URL:-}" ]; then
            pg_dump "${DATABASE_URL}" | gzip > "${pg_dump_file}"
        else
            pg_dump -h localhost -U postgres fullscopetest | gzip > "${pg_dump_file}"
        fi
        log_info "PostgreSQL 备份完成: ${pg_dump_file} ($(du -h "${pg_dump_file}" | cut -f1))"
    else
        # Docker 环境：通过 docker exec 执行
        local pg_container
        pg_container=$(docker ps --filter "ancestor=postgres" --format "{{.Names}}" | head -1)
        if [ -n "${pg_container}" ]; then
            docker exec "${pg_container}" pg_dump -U postgres fullscopetest | gzip > "${pg_dump_file}"
            log_info "PostgreSQL 备份完成（通过 Docker）: ${pg_dump_file}"
        else
            log_error "pg_dump 不可用且未找到 PostgreSQL 容器"
            return 1
        fi
    fi
}

# ── Redis 备份 ────────────────────────────────────────────────────────────────

backup_redis() {
    log_info "开始 Redis 备份..."

    local redis_dump_file="${BACKUP_PATH}/redis_${DATE}.rdb"

    if command -v redis-cli &> /dev/null; then
        # 触发 BGSAVE 并等待完成
        redis-cli BGSAVE > /dev/null 2>&1 || true
        sleep 2

        # 复制 RDB 文件
        local rdb_path
        rdb_path=$(redis-cli CONFIG GET dir | tail -1)/dump.rdb
        if [ -f "${rdb_path}" ]; then
            cp "${rdb_path}" "${redis_dump_file}"
            gzip "${redis_dump_file}"
            log_info "Redis 备份完成: ${redis_dump_file}.gz"
        else
            log_warn "未找到 Redis RDB 文件: ${rdb_path}"
        fi
    else
        # Docker 环境
        local redis_container
        redis_container=$(docker ps --filter "ancestor=redis" --format "{{.Names}}" | head -1)
        if [ -n "${redis_container}" ]; then
            docker exec "${redis_container}" redis-cli BGSAVE > /dev/null 2>&1 || true
            sleep 2
            docker cp "${redis_container}:/data/dump.rdb" "${redis_dump_file}"
            gzip "${redis_dump_file}"
            log_info "Redis 备份完成（通过 Docker）: ${redis_dump_file}.gz"
        else
            log_warn "redis-cli 不可用且未找到 Redis 容器，跳过 Redis 备份"
        fi
    fi
}

# ── 文件存储备份 ──────────────────────────────────────────────────────────────

backup_files() {
    log_info "开始文件存储备份..."

    local files_archive="${BACKUP_PATH}/files_${DATE}.tar.gz"
    local dirs_to_backup=""

    # 检查需要备份的目录
    for dir in uploads reports; do
        if [ -d "./${dir}" ]; then
            dirs_to_backup="${dirs_to_backup} ./${dir}"
        fi
    done

    if [ -n "${dirs_to_backup}" ]; then
        tar -czf "${files_archive}" ${dirs_to_backup}
        log_info "文件备份完成: ${files_archive} ($(du -h "${files_archive}" | cut -f1))"
    else
        log_warn "未找到需要备份的文件目录（uploads/、reports/）"
    fi
}

# ── 清理旧备份 ────────────────────────────────────────────────────────────────

cleanup_old_backups() {
    log_info "清理 ${BACKUP_RETENTION} 天前的旧备份..."

    local count=0
    while IFS= read -r old_dir; do
        if [ -d "${old_dir}" ]; then
            rm -rf "${old_dir}"
            count=$((count + 1))
        fi
    done < <(find "${BACKUP_DIR}" -maxdepth 1 -type d -mtime +${BACKUP_RETENTION} 2>/dev/null | sort)

    if [ ${count} -gt 0 ]; then
        log_info "已清理 ${count} 个旧备份"
    else
        log_info "无旧备份需要清理"
    fi
}

# ── 恢复功能 ──────────────────────────────────────────────────────────────────

restore_latest() {
    local latest_dir
    latest_dir=$(find "${BACKUP_DIR}" -maxdepth 1 -type d -name "20*" | sort -r | head -1)

    if [ -z "${latest_dir}" ]; then
        log_error "未找到备份目录"
        exit 1
    fi

    log_info "恢复备份: ${latest_dir}"

    # 恢复 PostgreSQL
    local pg_file
    pg_file=$(find "${latest_dir}" -name "postgres_*.sql.gz" | head -1)
    if [ -n "${pg_file}" ]; then
        log_info "恢复 PostgreSQL: ${pg_file}"
        gunzip -c "${pg_file}" | psql "${DATABASE_URL:-fullscopetest}" || log_error "PostgreSQL 恢复失败"
    fi

    # 恢复 Redis
    local redis_file
    redis_file=$(find "${latest_dir}" -name "redis_*.rdb.gz" | head -1)
    if [ -n "${redis_file}" ]; then
        log_info "恢复 Redis: ${redis_file}"
        gunzip -c "${redis_file}" > /var/lib/redis/dump.rdb || log_warn "Redis 恢复失败（可能需要手动操作）"
    fi

    # 恢复文件
    local files_archive
    files_archive=$(find "${latest_dir}" -name "files_*.tar.gz" | head -1)
    if [ -n "${files_archive}" ]; then
        log_info "恢复文件: ${files_archive}"
        tar -xzf "${files_archive}" -C / || log_warn "文件恢复失败"
    fi

    log_info "恢复完成"
}

# ── 主流程 ────────────────────────────────────────────────────────────────────

main() {
    if [ "${1:-}" = "--restore" ]; then
        restore_latest
        exit 0
    fi

    log_info "========================================="
    log_info "FullScopeTest 数据备份开始"
    log_info "时间: $(date)"
    log_info "========================================="

    backup_postgres || log_warn "PostgreSQL 备份失败（非致命）"
    backup_redis    || log_warn "Redis 备份失败（非致命）"
    backup_files    || log_warn "文件备份失败（非致命）"
    cleanup_old_backups

    log_info "========================================="
    log_info "备份完成: ${BACKUP_PATH}"
    log_info "========================================="
}

main "$@"