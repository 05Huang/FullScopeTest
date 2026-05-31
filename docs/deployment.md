# FullScopeTest 部署文档

> 本文档涵盖 FullScopeTest 的完整部署流程，包括本地开发环境、测试环境和生产环境。

---

## 目录

- [1. 环境要求](#1-环境要求)
- [2. 本地开发环境部署](#2-本地开发环境部署)
- [3. 测试环境部署](#3-测试环境部署)
- [4. 生产环境部署](#4-生产环境部署)
- [5. 环境变量完整说明](#5-环境变量完整说明)
- [6. 数据库管理](#6-数据库管理)
- [7. 监控与告警](#7-监控与告警)
- [8. 备份与恢复](#8-备份与恢复)
- [9. 升级与回滚](#9-升级与回滚)
- [10. 常见问题排查](#10-常见问题排查)

---

## 1. 环境要求

### 1.1 最低配置

| 资源 | 开发/测试环境 | 生产环境 |
|------|---------------|----------|
| CPU | 2 核 | 4 核（推荐 8 核） |
| 内存 | 4 GB | 8 GB（推荐 16 GB） |
| 磁盘 | 20 GB | 100 GB SSD |
| 操作系统 | Linux / macOS / Windows (WSL2) | Ubuntu 20.04+ / Debian 11+ |

### 1.2 软件依赖

| 软件 | 版本要求 | 说明 |
|------|----------|------|
| Docker | 20.10+ | 容器运行时 |
| Docker Compose | v2.0+ | 多容器编排 |
| Git | 2.30+ | 代码管理 |
| OpenSSL | 3.0+ | SSL 证书生成（可选） |

> **注意**：生产环境**不需要**在主机上安装 Python、Node.js 或 Playwright，所有运行时都在容器内。

### 1.3 可选工具

| 工具 | 用途 |
|------|------|
| [1Panel](https://1panel.cn/) | Web 管理面板 + OpenResty 反向代理 |
| [Certbot](https://certbot.eff.org/) | Let's Encrypt 免费 SSL 证书 |
| [cURL](https://curl.se/) | API 健康检查 |

---

## 2. 本地开发环境部署

### 2.1 快速启动

```bash
git clone https://github.com/05Huang/FullScopeTest.git
cd FullScopeTest
cp .env.example .env
docker compose up -d
docker compose ps
```

### 2.2 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Flask 后端 | 5000 | 主 API 端口 |
| PostgreSQL | 5432 | 数据库 |
| Redis | 6379 | 缓存/消息队列 |
| Prometheus | 9090 | 指标监控 |
| Grafana | 3001 | 监控面板 |

### 2.3 访问地址

- **前端应用**：http://localhost:5000
- **API 健康检查**：http://localhost:5000/api/v1/api-test/health
- **Grafana**：http://localhost:3001（默认账号 admin/admin）
- **Prometheus**：http://localhost:9090

### 2.4 热重载

```bash
docker compose logs -f backend
```

### 2.5 停止服务

```bash
docker compose down
docker compose down -v  # 删除数据卷
```

---

## 3. 测试环境部署

### 3.1 使用 pytest 运行测试

```bash
docker run --rm --network host \n  -e "TEST_DATABASE_URL=postgresql://fullscopetest:password@127.0.0.1:5432/fullscopetest_test" \n  -v "$(pwd)/backend:/app" -w /app python:3.11-slim \n  sh -c "pip install -r requirements.txt -r requirements-test.txt && pytest -q tests"
docker compose exec backend pytest -q tests
```

---

## 4. 生产环境部署

### 4.1 方案一：Docker Compose + Nginx（推荐）

适用于中小规模部署（少于 100 并发用户）。

#### 步骤 1：服务器准备

```bash
apt update && apt upgrade -y
apt install -y git curl ufw
ufw allow OpenSSH && ufw allow 80 && ufw allow 443
ufw enable
```

#### 步骤 2：安装 Docker

```bash
curl -fsSL https://get.docker.com | sh
apt install -y docker-compose-plugin
```

#### 步骤 3：克隆仓库

```bash
mkdir -p /opt/apps/fullscopetest/{repo,data,logs}
cd /opt/apps/fullscopetest/repo
git clone https://github.com/05Huang/FullScopeTest.git .
```

#### 步骤 4：配置环境变量

```bash
cp .env.example .env
vi .env  # 填入密钥和配置
```

关键变量：

```bash
DATABASE_URL=postgresql://fullscopetest:YOUR_PASSWORD@postgres:5432/fullscopetest_prod
REDIS_URL=redis://redis:6379/0
SECRET_KEY=GENERATED_SECRET_KEY
JWT_SECRET_KEY=GENERATED_JWT_KEY
FLASK_ENV=production
GRAFANA_ADMIN_PASSWORD=YOUR_GRAFANA_PASSWORD
```

#### 步骤 5：配置 PostgreSQL

**方案 A：宿主机 PostgreSQL（推荐）**

```bash
docker run -d --name postgres-shared \n  -e POSTGRES_USER=fullscopetest -e POSTGRES_PASSWORD=YOUR_PASSWORD \n  -p 127.0.0.1:5432:5432 -v /opt/apps/postgres/data:/var/lib/postgresql/data \n  postgres:15-alpine
docker exec -it postgres-shared psql -U fullscopetest -c "CREATE DATABASE fullscopetest_prod;"
docker exec -it postgres-shared psql -U fullscopetest -c "CREATE DATABASE fullscopetest_test;"
```

DATABASE_URL: `postgresql://fullscopetest:YOUR_PASSWORD@host.docker.internal:5432/fullscopetest_prod`

> **注意**：生产环境 Redis 无密码，REDIS_URL 不能包含密码。

**方案 B**：编辑 docker-compose.prod.yml 取消注释 PostgreSQL 服务。

#### 步骤 6：首次部署

```bash
chmod +x deploy.sh && ./deploy.sh
```

deploy.sh 自动执行：拉取代码、构建前端、运行测试、启动容器、数据库迁移、健康检查。

#### 步骤 7：配置 Nginx

**1Panel（推荐）**：
1. 安装 1Panel：`curl -sSL https://resource.fit2cloud.com/1panel/package/quick_start.sh | bash`
2. 访问 `http://<server-ip>:21887`
3. 创建静态网站，根路径：`/opt/apps/fullscopetest/repo/web/dist`
4. 反向代理：`/api/` 指向 `127.0.0.1:8000`

**手动 Nginx**：参考 `docker/nginx/nginx.conf`。

#### 步骤 8：配置 SSL

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d YOUR_DOMAIN -d www.YOUR_DOMAIN
```

#### 步骤 9：验证

```bash
docker compose -p fullscopetest -f docker-compose.prod.yml ps
curl -fsS http://127.0.0.1:8000/api/v1/api-test/health
curl -I http://YOUR_DOMAIN
```

### 4.2 方案二：Jenkins 自动部署

1. 创建 Credentials（GitHub PAT + SSH 私钥）
2. 创建 Pipeline Job，脚本路径 Jenkinsfile
3. 配置 DEPLOY_HOST、DEPLOY_USER、DEPLOY_PATH、SSH_CREDENTIALS_ID
4. 启用 GitHub Webhook 自动触发

---

## 5. 环境变量完整说明

### 5.1 必须配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| SECRET_KEY | Flask 应用密钥 | 无（必填） |
| JWT_SECRET_KEY | JWT 签名密钥 | 无（必填） |
| DATABASE_URL | 数据库连接 URL | 无（生产必填） |
| REDIS_URL | Redis 连接 URL | redis://redis:6379/0 |

### 5.2 数据库配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| POSTGRES_USER | PostgreSQL 用户名 | fullscopetest |
| POSTGRES_PASSWORD | PostgreSQL 密码 | 无（必填） |
| POSTGRES_DB | 数据库名 | fullscopetest_dev |
| TEST_DATABASE_URL | 测试数据库 URL | 无 |

### 5.3 Flask 配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| FLASK_ENV | 运行环境 | development |
| FLASK_PORT | 监听端口 | 5000 |

### 5.4 AI 助手配置（可选）

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| AI_ASSISTANT_ENABLED | 启用 AI 助手 | false |
| AI_ASSISTANT_BASE_URL | LLM API 地址 | 空 |
| AI_ASSISTANT_API_KEY | LLM API 密钥 | 空 |
| AI_ASSISTANT_MODEL | LLM 模型名称 | 空 |
| AI_VISION_BASE_URL | 视觉模型 API | 空 |
| AI_VISION_MODEL | 视觉模型名称 | 空 |
| AI_VISION_API_KEY | 视觉模型密钥 | 空 |

### 5.5 Playwright 配置（可选）

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| AI_EXPLORE_LIVE_VIEW_ALLOCATOR_URL | 浏览器分配器 URL | 空 |
| AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TOKEN | 分配器 Token | 空 |
| AI_EXPLORE_LIVE_VIEW_ALLOCATOR_TIMEOUT | 超时（秒） | 15 |
| AI_EXPLORE_BROWSER_HEADLESS | 无头模式 | true |
| AI_EXPLORE_BROWSER_SLOW_MO | 操作延迟（ms） | 0 |

### 5.6 Aliyun OSS（可选）

| 变量名 | 说明 |
|--------|------|
| OSS_ENDPOINT | OSS 端点 |
| OSS_ACCESS_KEY_ID | Access Key ID |
| OSS_ACCESS_KEY_SECRET | Access Key Secret |
| OSS_BUCKET_NAME | Bucket 名称 |
| OSS_DOMAIN | 自定义域名 |

### 5.7 监控配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| GRAFANA_ADMIN_USER | Grafana 用户名 | admin |
| GRAFANA_ADMIN_PASSWORD | Grafana 密码 | admin |
| GRAFANA_ROOT_URL | Grafana URL | 空 |

### 5.8 部署脚本变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| BRANCH | 部署分支 | main |
| PROJECT_NAME | Compose 项目名 | fullscopetest |
| DATA_DIR | 数据目录 | 自动推导 |
| COMPOSE_FILE | Compose 文件 | docker-compose.prod.yml |
| SKIP_WEB_BUILD | 跳过前端构建 | 0 |
| SKIP_DB_MIGRATE | 跳过数据库迁移 | 0 |

---

## 6. 数据库管理

### 6.1 迁移

```bash
docker compose -p fullscopetest -f docker-compose.prod.yml exec backend flask --app wsgi:app db upgrade heads
docker compose exec backend flask --app wsgi:app db current
docker compose exec backend flask --app wsgi:app db history
docker compose exec backend flask --app wsgi:app db downgrade -1
```

### 6.2 备份

```bash
docker exec postgres-shared pg_dump -U fullscopetest fullscopetest_prod > backup.sql
cat backup.sql | docker exec -i postgres-shared psql -U fullscopetest fullscopetest_prod
```

---

## 7. 监控与告警

### 7.1 Prometheus

- **访问**：http://<server-ip>:9090（生产仅本地）
- **保留**：生产 90 天，开发 30 天
- **指标**：/metrics 端点

核心指标：api_requests_total、task_execution_duration_seconds、active_websocket_connections

### 7.2 Grafana

- **访问**：http://<server-ip>:3001
- **账号**：admin / GRAFANA_ADMIN_PASSWORD

### 7.3 健康检查端点

| 端点 | 说明 | 鉴权 |
|------|------|------|
| GET /health | 存活检查 | 无 |
| GET /health/ready | 就绪检查 | 无 |
| GET /api/v1/api-test/health | 后端健康 | 无 |
| GET /metrics | Prometheus 指标 | 无 |

---

## 8. 备份与恢复

### 8.1 备份内容

| 内容 | 位置 | 方式 |
|------|------|------|
| 数据库 | PostgreSQL | pg_dump |
| 上传文件 | backend_uploads Volume | 文件复制 |
| 测试报告 | backend_reports Volume | 文件复制 |
| Grafana | grafana_data Volume | 文件复制 |
| 配置 | .env | 文件复制 |

### 8.2 完整备份脚本

```bash
#!/bin/bash
set -euo pipefail
BACKUP_DIR="/opt/apps/fullscopetest/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
docker exec postgres-shared pg_dump -U fullscopetest fullscopetest_prod | gzip > "$BACKUP_DIR/database.sql.gz"
docker run --rm -v fullscopetest_backend_uploads:/data -v "$BACKUP_DIR":/backup alpine tar czf /backup/uploads.tar.gz -C /data .
docker run --rm -v fullscopetest_backend_reports:/data -v "$BACKUP_DIR":/backup alpine tar czf /backup/reports.tar.gz -C /data .
cp .env "$BACKUP_DIR/env.bak"
echo "Backup completed: $BACKUP_DIR"
```

### 8.3 恢复

```bash
docker compose -p fullscopetest -f docker-compose.prod.yml down
cat backup.sql.gz | gunzip | docker exec -i postgres-shared psql -U fullscopetest fullscopetest_prod
docker compose -p fullscopetest -f docker-compose.prod.yml up -d
```

---

## 9. 升级与回滚

### 9.1 升级

```bash
cd /opt/apps/fullscopetest/repo && ./deploy.sh
curl -fsS http://127.0.0.1:8000/api/v1/api-test/health
```

### 9.2 回滚

```bash
git reset --hard <commit-hash> && ./deploy.sh
docker compose exec backend flask --app wsgi:app db downgrade -1
```

---

## 10. 常见问题排查

### Q1: docker compose up 报错 version is obsolete
忽略警告或删除 `version: '3.8'` 行。

### Q2: psycopg2.OperationalError
```bash
docker compose ps postgres && docker compose logs postgres
docker compose exec backend env | grep DATABASE_URL
```

### Q3: 数据库迁移失败
```bash
docker compose logs backend | tail -50
docker compose exec backend flask --app wsgi:app db current
```

### Q4: Nginx 502 Bad Gateway
确保 upstream 指向 127.0.0.1:8000，后端容器正常运行。

### Q5: Grafana 连不上 Prometheus
prometheus.yml 中 targets 使用容器名（如 backend:5000）。

### Q6: Celery Worker 不处理任务
```bash
docker compose logs celery | tail -30
docker compose exec redis redis-cli ping
```

### Q7: SSL 证书过期
```bash
certbot renew --nginx && nginx -s reload
```

### Q8: 前端空白或 404
```bash
ls -la /opt/apps/fullscopetest/repo/web/dist/
docker run --rm -v "$(pwd)/web:/app" -w /app node:18-alpine sh -c "npm ci && npm run build"
```

### Q9: WebSocket 连接失败
Nginx 添加 proxy_set_header Upgrade 和 Connection upgrade 配置。

### Q10: 磁盘空间不足
```bash
docker system df && docker system prune -f
```

### Q11: Playwright 浏览器无法启动
```bash
docker compose exec backend playwright install --with-deps chromium
```

### Q12: Volume does not match configuration
```bash
docker compose -p fullscopetest -f docker-compose.prod.yml down
docker volume rm fullscopetest_redis_data fullscopetest_backend_uploads
./deploy.sh
```

---

## 附录

### A. 端口汇总

| 端口 | 开发 | 生产 | 说明 |
|------|------|------|------|
| 5000 | 是 | 否 | Flask 后端（开发） |
| 8000 | 否 | 是 | Flask 后端（生产） |
| 5432 | 是 | 是 | PostgreSQL |
| 6379 | 是 | 是 | Redis |
| 9090 | 是 | 仅本地 | Prometheus |
| 3001 | 是 | 仅本地 | Grafana |
| 80/443 | 否 | 是 | HTTP/HTTPS |

### B. Docker Volume

| Volume | 路径 | 用途 |
|--------|------|------|
| postgres_data | /var/lib/postgresql/data | PostgreSQL |
| redis_data | /data | Redis |
| backend_uploads | /app/uploads | 上传文件 |
| backend_reports | /app/reports | 测试报告 |
| prometheus_data | /prometheus | 时序数据 |
| grafana_data | /var/lib/grafana | Grafana |

### C. 安全清单

- 密钥从 .env 配置，未硬编码
- PostgreSQL/Redis/Grafana/Prometheus 只绑定 127.0.0.1
- SSL 已配置（生产）
- Nginx 安全头已启用
- 防火墙已启用
- .env 权限 600

### D. 部署目录结构

```
/opt/apps/fullscopetest/
  repo/                          # Git 仓库
    backend/                     # 后端代码
    web/dist/                    # 前端构建产物
    docker-compose.prod.yml      # 生产 Compose
    deploy.sh                    # 部署脚本
    .env                         # 环境变量
  data/                          # 数据目录
  logs/                          # 日志目录
  backups/                       # 备份目录
```
