# 数据备份与恢复指南

## 概述

FullScopeTest 提供自动化的数据备份方案，支持 PostgreSQL 数据库、Redis 缓存和文件存储的备份与恢复。

## 备份策略

| 数据类型 | 备份方式 | 保留策略 | 频率 |
|---------|---------|---------|------|
| PostgreSQL | pg_dump 全量备份 | 7 天 | 每日凌晨 3:00 |
| Redis | RDB 快照 | 7 天 | 每日凌晨 3:00 |
| 文件存储 | tar 压缩归档 | 7 天 | 每日凌晨 3:00 |

## 快速开始

### 执行备份

```bash
# 手动执行备份
./scripts/backup.sh

# 自定义备份目录和保留天数
BACKUP_DIR=/data/backups BACKUP_RETENTION=14 ./scripts/backup.sh
```

### 恢复备份

```bash
# 恢复最近一次备份
./scripts/backup.sh --restore
```

### 自动备份（Cron）

```bash
# 添加到 crontab（每天凌晨 3:00）
0 3 * * * cd /opt/fullscopetest && ./scripts/backup.sh >> /var/log/fullscopetest-backup.log 2>&1
```

### Docker Compose 自动备份

在 `docker-compose.prod.yml` 中添加备份服务：

```yaml
services:
  backup:
    image: postgres:15
    volumes:
      - ./scripts/backup.sh:/backup.sh
      - ./backups:/backups
      - /var/run/docker.sock:/var/run/docker.sock
    entrypoint: /bin/sh -c "echo '0 3 * * * /backup.sh' | crontab - && crond -f"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fullscopetest
      - BACKUP_DIR=/backups
      - BACKUP_RETENTION=7
    depends_on:
      - db
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BACKUP_DIR` | 备份输出目录 | `./backups` |
| `BACKUP_RETENTION` | 保留天数 | `7` |
| `DATABASE_URL` | PostgreSQL 连接 URL | 无（使用默认连接） |
| `REDIS_URL` | Redis 连接 URL | 无（使用默认连接） |

## 备份文件结构

```
backups/
├── 20260616_030000/
│   ├── postgres_20260616_030000.sql.gz
│   ├── redis_20260616_030000.rdb.gz
│   └── files_20260616_030000.tar.gz
├── 20260615_030000/
│   └── ...
└── 20260614_030000/
    └── ...
```

## 恢复流程

1. **停止应用服务**（避免数据不一致）
2. **执行恢复**：`./scripts/backup.sh --restore`
3. **验证数据**：检查数据库和文件是否完整
4. **重启应用服务**

### 手动恢复 PostgreSQL

```bash
# 解压备份
gunzip backups/20260616_030000/postgres_20260616_030000.sql.gz

# 恢复到数据库
psql -h localhost -U postgres -d fullscopetest < backups/20260616_030000/postgres_20260616_030000.sql
```

### 手动恢复 Redis

```bash
# 停止 Redis
redis-cli SHUTDOWN NOSAVE

# 替换 RDB 文件
cp backups/20260616_030000/redis_20260616_030000.rdb /var/lib/redis/dump.rdb

# 启动 Redis
redis-server
```

## 监控

备份脚本的执行日志可通过以下方式监控：

```bash
# 查看备份日志
tail -f /var/log/fullscopetest-backup.log

# 检查最近备份
ls -la backups/ | tail -5
```

建议配合 Prometheus 告警规则监控备份文件的生成时间，确保备份正常执行。