# EasyTest

<div align="center">

**一站式自动化测试平台**

API 接口测试 · Web 自动化 · 性能测试

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.3-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)

[![Star](https://img.shields.io/github/stars/Asukadaisiki/easytest?style=social)](https://github.com/Asukadaisiki/easytest)

</div>

---

## 项目简介

EasyTest 是一款专为个人开发者和小型团队设计的自动化测试平台，集成了三大测试模块：

- **接口测试** - 类似 Postman 的 HTTP 测试体验
- **Web 自动化** - 基于 Playwright 的浏览器自动化
- **性能测试** - 基于 Locust 的压力测试

采用前后端分离架构，后端使用 Flask，前端使用 React + TypeScript，支持环境变量管理、脚本录制、实时监控等功能。

---

## 文档总览

统一入口文档：`document/overview.md`（推荐先看这一份）。
其他历史说明保留在 `document/` 目录，作为补充参考。










## 核心功能

### 🔌 接口测试

| 功能 | 描述 |
|------|------|
| HTTP 方法 | 支持 GET、POST、PUT、DELETE、PATCH 等 |
| 环境变量 | 动态参数替换，`{variable}` 语法 |
| 前置/后置脚本 | JavaScript 脚本执行 |
| 断言验证 | 多种断言类型，JSON Path 提取 |
| cURL 导出 | 一键复制为 cURL 命令 |
| 用例管理 | 用例和集合组织 |

### 🌐 Web 自动化

| 功能 | 描述 |
|------|------|
| 多浏览器支持 | Chromium、Firefox、WebKit |
| 脚本录制 | 可视化录制器，一键启动 |
| 截图视频 | 自动保存执行过程 |
| 批量执行 | 支持脚本批量运行 |

### ⚡ 性能测试

| 功能 | 描述 |
|------|------|
| 并发模拟 | 配置并发用户数 |
| 实时监控 | 响应时间、吞吐量、错误率 |
| 结果分析 | 响应时间分布、统计图表 |
| 历史对比 | 多次测试结果对比 |

---

## 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 运行环境 |
| Flask | 3.0 | Web 框架 |
| SQLAlchemy | 2.0 | ORM |
| Celery | 5.3+ | 异步任务队列 |
| Redis | 5.0+ | 消息代理 |
| Playwright | - | Web 自动化 |
| Locust | - | 性能测试 |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| React | 18.3 | UI 框架 |
| TypeScript | 5.x | 类型系统 |
| Vite | 5.x | 构建工具 |
| Ant Design | 5.x | UI 组件库 |
| Zustand | 4.x | 状态管理 |
| Monaco Editor | - | 代码编辑器 |

---

## 快速开始

### 前置要求

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建工具 |
| PostgreSQL | 15+ | 生产数据库（开发可用 SQLite） |
| Redis | 5.0+ | 异步任务队列 |

### 一键启动（推荐）

```bash
# Windows 用户
START.bat
```

该脚本会自动启动所有服务：Redis → Celery → 后端 → Nginx

### 手动启动

```bash
# 1. 启动 Redis
redis-server

# 2. 启动 Celery Worker（新终端）
cd backend
.\run_celery.bat

# 3. 启动后端（新终端）
cd backend
.\run_server.bat

# 4. 构建前端（新终端）
cd web
npm run build

# 5. 启动 Nginx（新终端）
cd nginx
.\start-nginx.bat
```

### 访问应用

打开浏览器访问：**http://localhost:8080**

| 项目 | 值 |
|------|-----|
| 地址 | http://localhost:8080 |
| 用户名 | admin |
| 密码 | admin123 |

---

## 项目结构

```
EasyTest-Web/
├── backend/              # Flask 后端
│   ├── app/
│   │   ├── api/         # API 接口
│   │   ├── models/      # 数据模型
│   │   ├── utils/       # 工具函数
│   │   ├── config.py    # 配置管理
│   │   └── extensions.py # Flask 扩展
│   ├── migrations/      # 数据库迁移
│   ├── init_db.py       # 数据库初始化
│   ├── run_server.bat   # 后端启动脚本
│   ├── run_celery.bat   # Celery 启动脚本
│   └── requirements.txt
├── web/                  # React 前端
│   ├── src/
│   │   ├── pages/       # 页面组件
│   │   ├── services/    # API 服务层
│   │   ├── stores/      # Zustand 状态管理
│   │   └── layouts/     # 布局组件
│   └── package.json
├── document/             # 项目文档
│   ├── STARTUP.md       # 启动指南
│   ├── API.md           # API 文档
│   ├── DEVELOPMENT.md   # 开发指南
│   └── SCRIPT_GUIDE.md  # 脚本指南
├── scripts/              # 开发脚本
│   ├── start/           # 启动脚本
│   ├── backend/         # 后端脚本
│   └── build/           # 构建脚本
├── nginx/                # Nginx 配置
├── docker/               # Docker 配置
├── START.bat             # 一键启动脚本
├── CLAUDE.md             # AI 助手指南
└── README.md             # 本文件
```

---

## 文档导航

统一入口文档：`document/overview.md`




### 快速上手

| 文档 | 说明 |
|------|------|
| [document/STARTUP.md](document/STARTUP.md) | 详细安装和启动指南 |

### 开发文档

| 文档 | 说明 |
|------|------|
| [document/API.md](document/API.md) | API 接口文档 |
| [document/DEVELOPMENT.md](document/DEVELOPMENT.md) | 开发环境配置 |
| [backend/README.md](backend/README.md) | 后端开发文档 |

### 功能指南

| 文档 | 说明 |
|------|------|
| [document/SCRIPT_GUIDE.md](document/SCRIPT_GUIDE.md) | 脚本编写指南 |

---

## 服务端口

| 服务 | 端口 | 地址 |
|------|------|------|
| 前端 (Nginx) | 8080 | http://localhost:8080 |
| 后端 API | 5211 | http://127.0.0.1:5211 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |

---

## 常见问题

### 启动失败

**Q: Redis 连接失败？**

A: 确保 Redis 已启动：
```bash
redis-cli ping  # 应返回 PONG
```

**Q: Celery 任务不执行？**

A: 检查 Celery Worker 是否运行：
```bash
cd backend
.\run_celery.bat
```

**Q: 前端修改后不生效？**

A: 重新构建前端：
```bash
cd web
npm run build
```

### 数据库

**Q: 如何切换到 PostgreSQL？**

A: 修改 `backend/.env` 中的 `DATABASE_URL`：
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/easytest_db
```

**Q: 如何重置数据库？**

A: 删除数据库文件后重新初始化：
```bash
cd backend
del easytest_dev.db  # Windows
rm easytest_dev.db   # Linux/Mac
python init_db.py
```

---

## Docker 部署

```bash
# 开发环境
docker-compose up -d

# 生产环境
docker-compose -f docker-compose.prod.yml up -d
```

---

## 更新日志

### 2025-01-05

**测试报告模块重构**

- ✅ 整合测试报告功能到"执行记录"页面，删除独立的"测试报告"标签页
- ✅ 修复报告下载功能，支持 HTML 和 JSON 格式导出
- ✅ 优化删除逻辑：删除执行记录时自动级联删除关联报告
- ✅ 改进数据结构：列表请求使用 page/per_page 分页参数
- ✅ 增强错误处理：兼容多种后端返回格式
- ✅ 修复 TypeScript 类型错误

**技术改进：**
- 后端 API 路由规范化 (`/api/v1/test-reports`)
- axios 响应拦截器优化，支持 text/blob 响应类型
- 文件下载使用授权的 blob 下载方式，文件名格式为"运行名称-报告ID"

### 历史版本

- 集成 Celery + Redis 异步任务系统
- Web 测试可视化录制器
- 性能测试实时监控
- 环境变量自动补全

详见 [Git 提交历史](https://github.com/Asukadaisiki/easytest/commits/main/)。

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

[MIT](LICENSE)

---

<div align="center">

Made with ❤️ by EasyTest Team

</div>
Webhook trigger test update: 2026-02-08
CI trigger verification: 2026-02-13 webhook check
CI trigger verification: 2026-02-13 21:29:12
