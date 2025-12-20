# EasyTest - 简单易用的自动化测试平台

<div align="center">

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

## 📦 技术栈

### 后端
- **Flask 3.0.0** - 轻量级 Web 框架
- **Flask-SQLAlchemy 3.1.1** - ORM 和数据库抽象层
- **Flask-JWT-Extended 4.6.0** - JWT 身份验证
- **PostgreSQL 15+** - 生产数据库（开发可用 SQLite）
- **Celery 5.3.4** - 分布式异步任务队列
- **Redis 5.0.1** - 消息代理和任务结果存储
- **Locust** - 性能测试框架
- **Playwright** - Web 自动化测试框架

### 前端
- **React 18.3** - UI 框架
- **TypeScript** - 类型安全的 JavaScript
- **Ant Design 5** - 企业级 UI 组件库
- **Zustand** - 状态管理
- **React Router 6** - 路由管理
- **Vite** - 现代化构建工具

### 基础设施
- **Nginx** - 反向代理和静态文件服务
- **Docker & Docker Compose** - 容器化部署

## 🏗️ 项目架构

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     Nginx 反向代理                           │
│                  (静态资源 + API 转发)                        │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
┌────────────▼────────────┐    ┌──────────────▼───────────────┐
│   前端 (React + Vite)    │    │   后端 (Flask + Gunicorn)    │
│                          │    │ + Celery Worker             │
│  • React 18              │    │                              │
│  • TypeScript            │    │  • Flask 3.0                 │
│  • Ant Design 5          │    │  • Flask-SQLAlchemy          │
│  • Zustand               │    │  • Flask-JWT-Extended        │
│  • React Router 6        │    │  • Celery + Redis            │
└──────────────────────────┘    └──────────────┬───────────────┘
                                               │
                                ┌──────────────▼───────────────┐
                                │         数据库层              │
                                │                              │
                                │  • PostgreSQL (生产)         │
                                │  • SQLite (开发)             │
                                │  • Redis (消息队列)          │
                                └──────────────────────────────┘
```

### 项目目录结构

```
EasyTest-Web/
├── backend/                              # 后端 Flask 应用
│   ├── app/
│   │   ├── api/                         # API 路由模块
│   │   │   ├── auth.py                  # 认证接口
│   │   │   ├── api_test.py              # 接口测试接口
│   │   │   ├── web_test.py              # Web 自动化测试接口
│   │   │   ├── perf_test.py             # 性能测试接口
│   │   │   ├── projects.py              # 项目管理接口
│   │   │   ├── environments.py          # 环境管理接口
│   │   │   ├── reports.py               # 报告接口
│   │   │   └── docs.py                  # 文档管理接口
│   │   ├── models/                      # 数据库模型
│   │   │   ├── user.py                  # 用户模型
│   │   │   ├── project.py               # 项目模型
│   │   │   ├── api_test_case.py         # API 测试用例模型
│   │   │   ├── web_test_script.py       # Web 测试脚本模型
│   │   │   ├── perf_test_scenario.py    # 性能测试场景模型
│   │   │   ├── environment.py           # 测试环境模型
│   │   │   ├── test_run.py              # 测试运行记录模型
│   │   │   └── test_document.py         # 测试文档模型
│   │   ├── utils/                       # 工具函数
│   │   │   ├── response.py              # 响应格式化
│   │   │   └── validators.py            # 数据验证
│   │   ├── celery_app.py                # Celery 配置
│   │   ├── tasks.py                     # 异步任务定义
│   │   ├── config.py                    # Flask 配置
│   │   ├── extensions.py                # Flask 扩展初始化
│   │   └── __init__.py                  # 应用工厂
│   ├── migrations/                      # 数据库迁移
│   ├── app.py                           # Flask 应用主入口
│   ├── wsgi.py                          # WSGI 应用入口
│   ├── manage.py                        # CLI 管理命令
│   ├── init_db.py                       # 数据库初始化脚本
│   ├── requirements.txt                 # Python 依赖
│   ├── run_server.bat                   # 启动脚本
│   └── run_celery.bat                   # Celery Worker 启动脚本
├── web/                                 # 前端 React 应用
│   ├── src/
│   │   ├── pages/                       # 页面级组件
│   │   │   ├── Login.tsx                # 登录页面
│   │   │   ├── Register.tsx             # 注册页面
│   │   │   ├── Dashboard.tsx            # 仪表板
│   │   │   ├── Documents.tsx            # 文档管理
│   │   │   ├── Reports.tsx              # 报告页面
│   │   │   ├── api-test/                # API 测试模块
│   │   │   ├── web-test/                # Web 测试模块
│   │   │   └── perf-test/               # 性能测试模块
│   │   ├── services/                    # API 服务层
│   │   │   ├── api.ts                   # HTTP 请求配置
│   │   │   ├── authService.ts           # 认证服务
│   │   │   ├── apiTestService.ts        # API 测试服务
│   │   │   ├── webTestService.ts        # Web 测试服务
│   │   │   ├── perfTestService.ts       # 性能测试服务
│   │   │   └── ...其他服务
│   │   ├── stores/                      # 状态管理
│   │   ├── layouts/                     # 布局组件
│   │   ├── styles/                      # 全局样式
│   │   ├── App.tsx                      # 根组件
│   │   └── main.tsx                     # 应用入口
│   ├── package.json                     # 依赖管理
│   ├── tsconfig.json                    # TypeScript 配置
│   └── vite.config.ts                   # Vite 配置
├── document/                            # 项目文档
│   ├── README.md                        # 项目介绍（本文档）
│   ├── STARTUP.md                       # 详细启动指南
│   ├── API.md                           # API 接口文档
│   └── DEVELOPMENT.md                   # 开发文档
├── docker/                              # Docker 配置
│   ├── Dockerfile.backend               # 后端镜像
│   ├── Dockerfile.backend.dev           # 后端开发镜像
│   └── nginx/                           # Nginx 配置
├── nginx/                               # Nginx 反向代理
│   ├── nginx.conf                       # 配置文件
│   ├── start-nginx.bat                  # 启动脚本
│   └── stop-nginx.bat                   # 停止脚本
├── docker-compose.yml                   # 开发配置
├── docker-compose.prod.yml              # 生产配置
└── .gitignore                           # Git 忽略规则
```

## 📋 需求

### 必需
- **Python 3.10+** - 后端运行环境
- **Node.js 18+** - 前端构建工具
- **PostgreSQL 15+** - 生产数据库（开发可用 SQLite）
- **Redis 5.0+** - 异步任务队列

### 可选
- **Docker & Docker Compose** - 容器化部署
- **Nginx** - 反向代理

## 🚀 快速开始

详见 [STARTUP.md](STARTUP.md) 获取完整的安装和启动步骤。

### 简要步骤

```bash
# 1. 克隆项目
git clone https://github.com/Asukadaisiki/easytest.git
cd EasyTest-Web

# 2. 启动后端
cd backend
pip install -r requirements.txt
python init_db.py
python app.py

# 3. 启动前端（新终端）
cd web
npm install
npm run build

# 4. 启动 Nginx（新终端）
cd nginx
.\start-nginx.bat

# 5. 访问应用
# 打开浏览器访问: http://localhost:8080
# 默认账号: admin / admin123
```

## 📚 文档导览

### 核心文档

| 文档 | 描述 |
|------|------|
| [STARTUP.md](STARTUP.md) | 📖 详细的项目启动指南，包含所有依赖安装和配置步骤 |
| [API.md](API.md) | 📑 完整的 API 接口文档，支持接口测试、性能测试、Web 自动化 |
| [DEVELOPMENT.md](DEVELOPMENT.md) | 🔧 开发人员指南，包含项目架构、开发规范和部署说明 |

### 推荐阅读顺序

1. **本文档（README.md）** - 了解项目概览
2. **[STARTUP.md](STARTUP.md)** - 按步骤启动项目
3. **[API.md](API.md)** - 了解可用接口，进行测试
4. **[DEVELOPMENT.md](DEVELOPMENT.md)** - 深入开发

## 🎯 使用场景

### 作为测试平台使用
1. 创建项目
2. 配置测试环境（base_url、环境变量等）
3. 创建测试用例或脚本
4. 执行测试并查看报告

### 作为学习项目使用
本项目可以作为自己的测试目标：
1. 使用接口测试功能测试该项目本身的 API
2. 使用性能测试功能对该项目进行压力测试
3. 使用 Web 自动化功能测试该项目的前端界面

## 🔐 默认账号

| 字段 | 值 |
|------|-----|
| 用户名 | admin |
| 密码 | admin123 |
| 邮箱 | admin@example.com |

## 📊 功能模块

### 接口测试 (API Test)
- ✅ 支持所有 HTTP 方法（GET、POST、PUT、DELETE、PATCH）
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
- ✅ 脚本录制功能
- ✅ 元素库管理
- ✅ 截图和视频录制
- ✅ 脚本编辑执行
- ✅ 批量执行

### 性能测试 (Performance Test)
- ✅ 基于 Locust 的分布式性能测试
- ✅ 并发用户模拟
- ✅ 实时性能监控
- ✅ 响应时间统计分析
- ✅ 吞吐量和错误率分析
- ✅ 性能报告生成

### 其他功能
- ✅ 项目管理 - 创建和管理多个测试项目
- ✅ 环境管理 - 项目级别的测试环境配置
- ✅ 测试文档 - Markdown 编辑器
- ✅ 测试报告 - 可视化报告和历史对比

## 🔧 配置

### 环境变量

后端环境变量配置示例（`backend/.env`）：

```bash
# Flask 配置
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 数据库配置（选择一个）
# 开发环境使用 SQLite
DATABASE_URL=sqlite:///easytest_dev.db

# 生产环境使用 PostgreSQL
# DATABASE_URL=postgresql://easytest:password@localhost:5432/easytest_db

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=86400
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# Celery 配置
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

## 🌐 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Nginx 反向代理 | 8080 | 前端和 API 入口 |
| Flask 后端 | 5211 | API 服务 |
| PostgreSQL 数据库 | 5432 | 数据库服务 |
| Redis | 6379 | 消息队列和缓存 |

## 🐳 Docker 快速启动

```bash
# 启动所有服务（开发环境）
docker-compose up -d

# 启动所有服务（生产环境）
docker-compose -f docker-compose.prod.yml up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📝 版本日志

### v1.2.0 (2025-12-28)
- ✨ 集成 Celery + Redis 异步任务系统
- ✨ Web 测试和性能测试支持异步执行
- 📝 新增完整 API 文档

### v1.1.0 (2025-12-24)
- ✨ 增强 Web 测试录制功能
- 🐛 修复多项 bug

## 🤝 开发

### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 前端开发
```bash
cd web
npm install
npm run dev
```

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📮 联系方式

- 提交 Issue 反馈 bug 或建议
- 提交 Pull Request 贡献代码

---

<div align="center">
Made with ❤️ by EasyTest Team
</div>
