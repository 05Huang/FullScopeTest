# EasyTest 文档总览

> 这份文档是当前项目的统一入口，摘要关键运行方式、模块与目录。更详细说明仍保留在 `document/` 目录。

## 1. 快速开始

- Windows 一键启动：`START.bat`
- Docker（开发）：`docker-compose up -d`
- Docker（生产）：`docker-compose -f docker-compose.prod.yml up -d`

## 2. 手动启动（开发/排障）

1. 启动 Redis
2. （可选）启动 Celery Worker（启用异步任务时）
3. 启动后端
4. 构建前端
5. 启动 Nginx

### Windows 示例

```powershell
# 1) Redis
redis-server

# 2) Celery Worker
cd backend
.\run_celery.bat

# 3) Backend
cd backend
.\run_server.bat

# 4) Frontend
cd web
npm run build

# 5) Nginx
cd nginx
.\start-nginx.bat
```

### Linux/macOS 示例

```bash
# 1) Redis
redis-server

# 2) Celery Worker
cd backend
celery -A app.extensions:celery worker --loglevel=info

# 3) Backend
cd backend
python app.py

# 4) Frontend
cd web
npm run build

# 5) Nginx
cd nginx
./start-nginx.sh
```

## 3. 关键配置

- 后端配置文件：`backend/.env`
- API 前缀：`/api/v1`
- 数据库：开发可用 SQLite，生产推荐 PostgreSQL
- 异步任务：Redis + Celery（未启用时可只启动后端）

## 4. 功能模块（以当前代码为准）

- 接口测试：用例/集合管理、环境变量、前置/后置脚本
- Web 自动化：脚本管理、录制（本地环境）、脚本执行
- 性能测试：场景管理、执行、监控、结果分析
- 报告中心：执行记录、统计与导出
- 文档管理：文档 CRUD 与模板列表

> 说明：Web 录制依赖本地 Playwright 环境，远程服务器通常无法直接使用录制功能。

## 5. 服务端口

| 服务 | 端口 | 地址 |
|------|------|------|
| 前端 (Nginx) | 8080 | http://localhost:8080 |
| 后端 API | 5211 | http://127.0.0.1:5211 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |

## 6. 关键目录

- `backend/`：Flask 后端与 API
- `web/`：React 前端
- `document/`：历史文档（保留作补充）
- `scripts/`：本地脚本
- `docker/`、`nginx/`：部署相关配置

## 7. 延伸阅读

- `document/STARTUP.md`：完整安装与启动
- `document/API.md`：接口说明
- `document/DEVELOPMENT.md`：开发说明与架构
- `document/SCRIPT_GUIDE.md`：脚本编写说明
- `backend/README.md`：后端说明
