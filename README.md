# FullScopeTest

<div align="center">

**一站式自动化测试平台**

AI 自动编排 · API 接口测试 · Web 自动化 · 性能测试 · 报告中心

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.3-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Star](https://img.shields.io/github/stars/Asukadaisiki/fullscopetest?style=social)](https://github.com/Asukadaisiki/fullscopetest)

<p>
  <img src="images/Snipaste_2026-03-20_18-05-42.png" alt="FullScopeTest 首页" width="100%" />
  <img src="images/Snipaste_2026-03-20_23-21-38.png" alt="FullScopeTest 首页" width="100%" />
</p>

</div>

---

## 项目简介

FullScopeTest 是一款面向个人开发者与小团队的自动化测试平台，覆盖接口测试、Web 自动化、性能测试与报告中心，并提供可落地执行的 AI 自动编排能力。

- AI 自动编排：自然语言生成执行计划，并复用既有平台 API 自动落地执行
- 接口测试：类似 Postman 的工作台体验（环境变量、脚本、断言、用例/集合管理）
- Web 自动化：Playwright 脚本管理与异步执行；支持本地录制（`playwright codegen`）
- 性能测试：基于 Locust 的压测场景、执行与监控
- 报告中心：执行记录与报告落库，支持检索与导出

项目采用前后端分离架构：后端 Flask + SQLAlchemy，前端 React + TypeScript。AI 模型提供方配置（`base_url` / `model` / `api_key`）支持在前端面板运行时填写，并按请求即时生效。

---

## 文档入口

- 统一入口：`document/overview.md`
- 启动指南：`document/STARTUP.md`
- API 文档：`document/API.md`
- 开发文档：`document/DEVELOPMENT.md`
- 脚本指南：`document/SCRIPT_GUIDE.md`

---

## 功能一览

### 🤖 AI 自动编排（API 测试工作台）

| 功能 | 说明 |
|------|------|
| 自然语言生成计划 | 输入目标后生成结构化操作步骤（plan） |
| 复用既有接口落地执行 | 按计划调用平台 API 创建/更新环境、集合、用例并运行 |
| 运行时模型配置 | 前端面板动态设置 `base_url` / `model` / `api_key` |

### 🔌 接口测试

| 功能 | 说明 |
|------|------|
| 多种 HTTP 方法 | GET / POST / PUT / DELETE / PATCH 等 |
| 环境变量与 Headers | 支持 `{variable}` 变量替换与默认请求头 |
| 前置/后置脚本 | 支持脚本执行与变量提取/断言 |
| 用例与集合管理 | 组织、批量运行与结果落库 |
| cURL 导出 | 一键复制为 cURL 命令 |

### 🌐 Web 自动化（Playwright）

| 功能 | 说明 |
|------|------|
| 脚本管理 | 创建、编辑、保存、归档 Playwright Python 脚本 |
| 异步执行 | 通过 Celery 后台运行，支持状态跟踪 |
| 本地录制 | 启动 `playwright codegen` 录制（需本机环境） |
| 报告落库 | 执行输出与报告持久化，便于检索追溯 |

### ⚡ 性能测试（Locust）

| 功能 | 说明 |
|------|------|
| 并发模拟 | 配置并发用户数与阶段（step load） |
| 实时监控 | 响应时间、吞吐量、错误率等 |
| 结果分析 | 指标统计与图表展示 |

---

## 快速开始（本地开发推荐）

### 前置要求

| 组件 | 版本建议 | 说明 |
|------|---------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建/开发服务器 |
| PostgreSQL | 15+ | 推荐数据库（默认配置更贴近 PostgreSQL） |
| Redis | 5.0+ | 异步任务（Celery）所需，未用异步可不启 |

### 1) 启动后端

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt

# 可选：安装 Playwright 浏览器（启用 Web 录制/执行时建议）
python -m playwright install chromium

# 准备 backend/.env（最少需要 DATABASE_URL / SECRET_KEY / JWT_SECRET_KEY）
# 示例（SQLite 快速启动）：
#   DATABASE_URL=sqlite:///fullscopetest_dev.db
#   SECRET_KEY=dev-secret
#   JWT_SECRET_KEY=dev-jwt-secret

# 初始化数据库（会 drop & create）
python init_db.py

# 创建管理员账号（可选）
python create_admin.py
# 默认账号：admin / admin123

# 启动后端 API
python app.py
```

后端默认地址：`http://127.0.0.1:5211/api/v1`

#### 可选：启动 Celery Worker（建议新终端）

```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
celery -A app.extensions:celery worker --loglevel=info
```

### 2) 启动前端（开发模式）

```bash
cd web
npm install
npm run dev
```

前端开发服务器：`http://localhost:3000`（已配置代理，将 `/api/*` 转发到 `http://localhost:5211`）

---

## 构建与部署（生产/预发布）

```bash
cd web
npm install
npm run build
```

构建产物位于 `web/dist`，可由 Nginx/OpenResty 托管，并反代后端到 `http://127.0.0.1:5211`。配置示例可参考 `nginx/` 目录与 `deploy.sh`。

---

## 关键配置

后端配置文件：`backend/.env`（由 `python-dotenv` 在启动时加载）。

```bash
# 数据库（二选一）
# PostgreSQL（推荐）
DATABASE_URL=postgresql://user:password@localhost:5432/fullscopetest_dev
# SQLite（本地快速启动）
# DATABASE_URL=sqlite:///fullscopetest_dev.db

# Redis / Celery
REDIS_URL=redis://localhost:6379/0
CELERY_ENABLE=true

# JWT（生产环境务必更换）
SECRET_KEY=change-me
JWT_SECRET_KEY=change-me

# AI Assistant（可选；也可由前端按请求覆盖）
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=
```

说明：
- Web 录制功能通过启动本机 `playwright codegen` 实现，远程服务器环境通常无法使用录制器。
- 后端入口 `backend/app.py` 会强制启用 Celery，建议同时启动 Redis + Celery Worker。

---

## 服务地址与端口

| 服务 | 默认端口 | 地址 |
|------|---------:|------|
| 前端（Vite dev） | 3000 | http://localhost:3000 |
| 后端 API | 5211 | http://127.0.0.1:5211/api/v1 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |

---

## 项目结构（核心）

```
FullScopeTest/
├── backend/              # Flask 后端
│   ├── app/              # API / models / tasks / utils
│   ├── migrations/       # 数据库迁移
│   ├── tests/            # Pytest
│   ├── app.py            # 后端启动入口
│   ├── init_db.py        # 开发环境快速初始化
│   └── create_admin.py   # 创建管理员账号
├── web/                  # React + TS 前端
├── document/             # 项目文档
├── nginx/                # Nginx 配置示例
├── docker/               # Dockerfile 等
└── scripts/              # 启动/构建脚本
```

---

## 常见问题

### Redis 连接失败？

确保 Redis 已启动：

```bash
redis-cli ping  # 应返回 PONG
```

### Web 录制器启动失败？

录制依赖 Playwright 本机环境，请确认：

```bash
pip install playwright
playwright install chromium
```

---

## 贡献

- 欢迎提交 Issue / Pull Request
- 提交前建议本地自检：`cd web && npm run lint`，`cd backend && pytest -q`

---

## 许可证

[MIT](LICENSE)

