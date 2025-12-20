# EasyTest - 简单易用的自动化测试平台

<div align="center">

![EasyTest Logo](docs/logo.png)

**专为个人开发者打造的一站式自动化测试平台**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.3-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)

</div>

## ✨ 特性

- 🚀 **简单高效** - 开箱即用，无需复杂配置
- 🔧 **接口测试** - 类似 Postman 的接口测试体验，支持环境变量、断言脚本、cURL 导出
- 🌐 **Web 自动化** - 基于 Playwright 的 Web UI 自动化测试，支持录制和元素库
- ⚡ **性能测试** - 集成 Locust，支持实时监控和结果分析
- 📊 **可视化报告** - 完整的测试报告和趋势分析
- 📝 **测试文档** - Markdown 编辑器，方便管理测试文档

## 📅 更新日志

### v1.2.0 (2025-12-28)

#### 🚀 重大更新
- **异步任务系统** - 集成 Celery + Redis 分布式任务队列
  - Web 测试和性能测试异步执行，不阻塞主线程
  - 任务状态实时追踪和管理
  - 支持任务撤销和超时控制
  - Redis 消息队列，支持分布式 Worker
  - 任务持久化，进程重启不丢失

#### 📦 新增依赖
- `celery==5.3.4` - 分布式任务队列
- `redis==5.0.1` - 消息代理和结果存储

#### 📝 新增文档
- [CELERY_INTEGRATION.md](CELERY_INTEGRATION.md) - Celery 集成详细指南

### v1.1.0 (2025-12-24)

#### 🆕 新增功能
- **Web 测试录制器（增强）** - 支持从 Web 界面直接启动 Playwright Inspector
  - 点击按钮即可启动录制，无需手动命令行
  - 自动管理录制进程
  - 实时状态检查
  - 支持多浏览器选择（Chromium、Firefox、WebKit）
- **元素库管理** - 统一管理页面元素，支持 CSS/XPath/ID 等定位方式
- **性能测试实时监控** - 实时查看运行中测试的响应时间、吞吐量、错误率
- **性能测试结果分析** - 详细的响应时间分布、请求统计、历史对比

#### 🔧 功能完善
- **API 测试工作台**
  - 从数据库加载测试用例和集合
  - 支持复制为 cURL 命令
  - 支持保存请求为用例
  - 参数/请求头表格添加删除功能
- **用例管理**
  - 编辑用例功能
  - 复制用例功能
  - 批量删除功能
  - 搜索过滤功能
- **脚本管理**
  - 编辑脚本功能
  - 批量执行和删除
  - 搜索过滤功能
- **场景管理**
  - 编辑场景功能
  - 批量删除功能
  - 搜索过滤功能
- **报告管理**
  - 批量删除和下载
  - 搜索过滤功能
- **文档管理**
  - 搜索过滤功能

#### 🐛 Bug 修复
- 修复请求头变量命名冲突问题
- 修复编译警告（未使用变量）

## 📦 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+ (生产环境推荐，开发可用 SQLite)
- Redis 5.0+ (异步任务队列)

### 安装与启动

#### 1. 克隆项目

```bash
git clone https://github.com/Asukadaisiki/easytest.git
cd EasyTest-Web
```

#### 2. 后端设置

```bash
cd backend

# 创建虚拟环境 (可选)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动 Redis 服务器 (新窗口)
# Windows: 下载并启动 Redis for Windows
# Linux/Mac: redis-server

# 启动 Celery Worker (新窗口)
celery -A app.extensions:celery worker --loglevel=info --pool=solo  # Windows
# 或使用快捷脚本: .\run_celery.bat

# 启动开发服务器
python app.py
```

后端运行地址：http://127.0.0.1:5211

#### 3. 前端设置

```bash
cd web

# 安装依赖
npm install

# 构建前端
npm run build
```

#### 4. 启动 Nginx

```bash
cd nginx

# 启动 Nginx
.\start-nginx.bat
```

#### 5. 访问应用

打开浏览器访问 http://localhost:8080

**默认测试账号：**
- 用户名：`admin`
- 密码：`admin123`

### Docker 快速启动

```bash
# 启动所有服务 (需要安装 Docker 和 Docker Compose)
docker-compose up -d

# 访问应用
# 前端: http://localhost:80
# 后端 API: http://localhost:5211/api/v1
```

详见 [STARTUP_GUIDE.md](STARTUP_GUIDE.md) 了解更多启动选项。

## 🏗️ 项目结构

```
EasyTest-Web/
├── backend/                              # 后端 Flask 应用
│   ├── app/
│   │   ├── api/                         # API 路由模块
│   │   │   ├── auth.py                  # 认证接口 (登录、注册、JWT)
│   │   │   ├── api_test.py              # 接口测试相关接口
│   │   │   ├── web_test.py              # Web 自动化测试接口
│   │   │   ├── perf_test.py             # 性能测试接口
│   │   │   ├── projects.py              # 项目管理接口
│   │   │   ├── environments.py          # 测试环境管理接口
│   │   │   ├── reports.py               # 测试报告接口
│   │   │   └── docs.py                  # 文档管理接口
│   │   ├── models/                      # 数据库模型
│   │   │   ├── user.py                  # 用户模型
│   │   │   ├── project.py               # 项目模型
│   │   │   ├── api_test_case.py         # API 测试用例和集合模型
│   │   │   ├── web_test_script.py       # Web 测试脚本模型
│   │   │   ├── perf_test_scenario.py    # 性能测试场景模型
│   │   │   ├── environment.py           # 测试环境模型
│   │   │   ├── test_run.py              # 测试运行记录模型
│   │   │   └── test_document.py         # 测试文档模型
│   │   ├── utils/                       # 工具函数
│   │   │   ├── response.py              # 响应格式化工具
│   │   │   └── validators.py            # 数据验证工具
│   │   ├── config.py                    # Flask 应用配置
│   │   ├── extensions.py                # Flask 扩展初始化 (db, jwt等)
│   │   └── __init__.py                  # 应用工厂
│   ├── migrations/                      # 数据库迁移记录 (Alembic)
│   ├── app.py                           # Flask 应用主入口
│   ├── wsgi.py                          # WSGI 应用入口 (生产部署)
│   ├── manage.py                        # Flask CLI 管理命令
│   ├── init_db.py                       # 数据库初始化脚本
│   ├── run_server.bat                   # Windows 后端启动脚本
│   ├── run_celery.bat                   # Windows Celery Worker 启动脚本
│   ├── celery_worker.py                 # Celery Worker 启动文件
│   ├── requirements.txt                 # Python 依赖清单
│   ├── .env.example                     # 环境变量示例
│   └── README.md                        # 后端开发文档
├── web/                                 # 前端 React + TypeScript 应用
│   ├── src/
│   │   ├── pages/                       # 页面级组件
│   │   │   ├── Login.tsx                # 登录页面
│   │   │   ├── Register.tsx             # 注册页面
│   │   │   ├── Dashboard.tsx            # 仪表板首页
│   │   │   ├── Documents.tsx            # 文档管理页面
│   │   │   ├── Reports.tsx              # 报告页面
│   │   │   ├── api-test/                # API 测试模块
│   │   │   │   ├── ApiTestWorkspace.tsx # API 测试工作台
│   │   │   │   ├── ApiTestCollections.tsx # 用例集合管理
│   │   │   │   └── ApiTestEnvironments.tsx # 环境变量管理
│   │   │   ├── web-test/                # Web 自动化测试模块
│   │   │   │   ├── WebTestElements.tsx  # 元素库管理
│   │   │   │   └── ...                  # 其他测试相关页面
│   │   │   └── perf-test/               # 性能测试模块
│   │   │       ├── PerfTestScenarios.tsx # 场景管理
│   │   │       ├── PerfTestMonitor.tsx  # 实时监控
│   │   │       └── PerfTestResults.tsx  # 结果分析
│   │   ├── services/                    # API 服务层
│   │   │   ├── api.ts                   # 基础 HTTP 请求配置
│   │   │   ├── authService.ts           # 认证服务
│   │   │   ├── apiTestService.ts        # API 测试服务
│   │   │   ├── webTestService.ts        # Web 测试服务
│   │   │   ├── perfTestService.ts       # 性能测试服务
│   │   │   ├── projectService.ts        # 项目服务
│   │   │   ├── reportService.ts         # 报告服务
│   │   │   ├── environmentService.ts    # 环境服务
│   │   │   └── documentService.ts       # 文档服务
│   │   ├── stores/                      # 状态管理 (Zustand)
│   │   │   └── authStore.ts             # 认证状态管理
│   │   ├── layouts/                     # 布局组件
│   │   │   └── MainLayout.tsx           # 主布局
│   │   ├── styles/                      # 全局样式
│   │   │   └── index.css                # 全局 CSS
│   │   ├── App.tsx                      # 根组件
│   │   └── main.tsx                     # React 应用入口
│   ├── public/                          # 静态资源
│   ├── index.html                       # HTML 入口文件
│   ├── package.json                     # 项目依赖和脚本
│   ├── tsconfig.json                    # TypeScript 配置
│   ├── tsconfig.node.json               # TypeScript Node 配置
│   └── README.md                        # 前端开发文档
├── document/                            # 项目文档目录
│   └── DEVELOPMENT.md                   # 开发指南
├── docker/                              # Docker 配置
│   ├── Dockerfile.backend               # 后端 Docker 镜像
│   ├── Dockerfile.backend.dev           # 后端开发 Docker 镜像
│   ├── init.sql                         # 数据库初始化 SQL
│   └── nginx/                           # Nginx 反向代理配置
│       ├── nginx.conf                   # Nginx 主配置
│       └── ssl/                         # SSL 证书目录
├── docker-compose.yml                   # Docker Compose 开发配置
├── docker-compose.prod.yml              # Docker Compose 生产配置
├── IMPORTANT_FILES.md                   # 📌 重要文件清单 (推荐首先阅读)
├── README.md                            # 项目介绍与快速开始
├── STARTUP_GUIDE.md                     # 项目启动详细指南
├── POSTGRESQL_SETUP.md                  # PostgreSQL 安装与配置教程
├── MIGRATION_SUCCESS.md                 # 数据库迁移完成记录
├── USER_MANUAL.md                       # 用户使用手册
├── REFACTORING_PLAN.md                  # 项目架构与开发计划
├── RECORDING_QUICKSTART.md              # Playwright 录制快速指南
├── PLAYWRIGHT_RECORDING_GUIDE.md        # 录制功能详细指南
├── CELERY_INTEGRATION.md                # Celery 异步任务集成指南
├── .gitignore                           # Git 忽略规则
└── .git/                                # Git 版本控制
```

## 📚 功能模块

### 接口测试 (API Test)

- ✅ 支持 GET、POST、PUT、DELETE、PATCH 等 HTTP 方法
- ✅ 请求参数、Headers、Body 配置
- ✅ 环境变量管理和动态参数替换
- ✅ 前置/后置脚本执行
- ✅ 断言验证
- ✅ 用例和集合管理
- ✅ cURL 导出功能
- ✅ 测试结果历史记录

### Web 自动化测试 (Web Test)

- ✅ 基于 Playwright 的浏览器自动化
- ✅ 支持 Chromium、Firefox、WebKit 三种浏览器
- ✅ 脚本录制功能 (直观的 Inspector)
- ✅ 元素库管理
- ✅ 截图和视频录制
- ✅ 脚本编辑执行
- ✅ 批量执行

### 性能测试 (Performance Test)

- ✅ 基于 Locust 的分布式性能测试
- ✅ 并发用户模拟
- ✅ 实时性能监控面板
- ✅ 响应时间统计分析
- ✅ 吞吐量和错误率分析
- ✅ 性能报告生成
- ✅ 历史对比分析

### 项目管理

- ✅ 创建和管理多个测试项目
- ✅ 项目级别的测试环境配置
- ✅ 用户权限管理

### 测试文档

- ✅ Markdown 编辑器
- ✅ 文档搜索和分类
- ✅ 版本管理

### 测试报告

- ✅ 可视化测试报告
- ✅ 报告导出功能
- ✅ 历史报告查看

## 🔧 配置

### 环境变量

```bash
# backend/.env 示例
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 数据库配置 (选择一个)
# 选项 1: SQLite (开发用)
DATABASE_URL=sqlite:///easytest.db

# 选项 2: PostgreSQL (生产推荐)
DATABASE_URL=postgresql://user:password@localhost:5432/easytest_db

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
```

详见 [.env.example](backend/.env.example) 和 [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)

### 数据库配置

**SQLite (默认，用于开发)**
- 无需额外配置
- 数据存储在 `easytest_dev.db`

**PostgreSQL (生产推荐)**
- 详见 [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)
- 连接字符串示例：`postgresql://easytest:password@localhost:5432/easytest_db`

## 🐳 Docker 部署

### 开发环境

```bash
# 启动所有开发服务 (PostgreSQL + 后端 + 前端)
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 生产环境

```bash
# 启动生产配置
docker-compose -f docker-compose.prod.yml up -d

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 停止服务
docker-compose -f docker-compose.prod.yml down
```

详见 [docker-compose.yml](docker-compose.yml) 和 [docker-compose.prod.yml](docker-compose.prod.yml)

## 📖 文档

### 重要文件

推荐按以下顺序阅读：

1. **[IMPORTANT_FILES.md](IMPORTANT_FILES.md)** - 📌 项目重要文件清单 (概览)
2. **[STARTUP_GUIDE.md](STARTUP_GUIDE.md)** - 启动指南 (详细步骤)
3. **[USER_MANUAL.md](USER_MANUAL.md)** - 用户使用手册
4. **[POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)** - PostgreSQL 安装配置 (可选)
5. **[REFACTORING_PLAN.md](REFACTORING_PLAN.md)** - 项目架构设计文档

### API 文档

启动后端服务后，访问以下地址查看 API 文档：

- **RESTful API Docs**: http://localhost:5211/api/v1/docs (自定义)
- **项目文档**: [backend/README.md](backend/README.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<div align="center">
Made with ❤️ by EasyTest Team
</div>
