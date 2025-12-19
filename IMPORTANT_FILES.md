# 📌 EasyTest 重要文件清单

## 🎯 核心配置文件

### 环境与依赖
- **[requirements.txt](backend/requirements.txt)** - Python 依赖管理文件，记录所有后端包
- **[package.json](web/package.json)** - Node.js 依赖管理，前端项目配置
- **[.env.example](backend/.env.example)** - 环境变量模板（参考配置）
- **[.gitignore](.gitignore)** - Git 忽略规则

### 数据库与ORM
- **[backend/app/models/](backend/app/models/)** - 数据库模型定义（核心数据结构）
  - `user.py` - 用户模型
  - `project.py` - 项目模型
  - `api_test_case.py` - API 测试用例模型
  - `web_test_script.py` - Web 测试脚本模型
  - `perf_test_scenario.py` - 性能测试场景模型
  - `environment.py` - 测试环境模型
  - `test_run.py` - 测试运行记录模型
  - `test_document.py` - 测试文档模型
- **[migrations/](backend/migrations/)** - 数据库迁移记录

---

## 🔧 后端核心代码

### 启动与初始化
- **[backend/app.py](backend/app.py)** - Flask 应用主入口
- **[backend/wsgi.py](backend/wsgi.py)** - WSGI 应用入口（生产部署）
- **[backend/manage.py](backend/manage.py)** - Flask CLI 管理命令（数据库初始化、创建管理员）
- **[backend/init_db.py](backend/init_db.py)** - 数据库初始化脚本
- **[backend/run_server.bat](backend/run_server.bat)** - Windows 启动脚本

### API 接口层
- **[backend/app/api/](backend/app/api/)** - API 路由定义
  - `auth.py` - 认证相关接口（登录、注册、JWT）
  - `api_test.py` - API 测试相关接口
  - `web_test.py` - Web 自动化测试接口
  - `perf_test.py` - 性能测试接口
  - `projects.py` - 项目管理接口
  - `environments.py` - 环境管理接口
  - `reports.py` - 测试报告接口
  - `docs.py` - 文档管理接口

### 应用配置
- **[backend/app/config.py](backend/app/config.py)** - Flask 应用配置（数据库、日志等）
- **[backend/app/extensions.py](backend/app/extensions.py)** - Flask 扩展初始化
- **[backend/app/__init__.py](backend/app/__init__.py)** - Flask 应用工厂

### 工具函数
- **[backend/app/utils/](backend/app/utils/)** - 通用工具
  - `response.py` - 响应格式化
  - `validators.py` - 数据验证

---

## 🎨 前端核心代码

### 启动与配置
- **[web/package.json](web/package.json)** - 项目配置和依赖
- **[web/tsconfig.json](web/tsconfig.json)** - TypeScript 配置
- **[web/index.html](web/index.html)** - HTML 入口文件

### 源代码结构
- **[web/src/main.tsx](web/src/main.tsx)** - React 应用入口
- **[web/src/App.tsx](web/src/App.tsx)** - 根组件

### 页面组件
- **[web/src/pages/](web/src/pages/)** - 页面级组件
  - `Login.tsx` - 登录页面
  - `Register.tsx` - 注册页面
  - `Dashboard.tsx` - 仪表板
  - `Documents.tsx` - 文档管理
  - `Reports.tsx` - 报告页面
  - `api-test/` - API 测试模块
  - `web-test/` - Web 自动化测试模块
  - `perf-test/` - 性能测试模块

### 服务层
- **[web/src/services/](web/src/services/)** - API 服务调用
  - `api.ts` - 基础 HTTP 请求配置
  - `authService.ts` - 认证服务
  - `apiTestService.ts` - API 测试服务
  - `webTestService.ts` - Web 测试服务
  - `perfTestService.ts` - 性能测试服务
  - `projectService.ts` - 项目服务
  - `reportService.ts` - 报告服务
  - `environmentService.ts` - 环境服务
  - `documentService.ts` - 文档服务

### 状态管理
- **[web/src/stores/authStore.ts](web/src/stores/authStore.ts)** - 认证状态管理（Zustand）

---

## 📚 文档文件（优先级）

### ⭐⭐⭐ 最重要
- **[README.md](README.md)** - 项目介绍、快速开始、功能特性
- **[MIGRATION_SUCCESS.md](MIGRATION_SUCCESS.md)** - 数据库迁移完成记录、连接信息
- **[POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)** - PostgreSQL 安装和配置教程

### ⭐⭐ 重要
- **[STARTUP_GUIDE.md](STARTUP_GUIDE.md)** - 项目启动步骤和环境配置
- **[USER_MANUAL.md](USER_MANUAL.md)** - 用户使用手册
- **[REFACTORING_PLAN.md](REFACTORING_PLAN.md)** - 项目架构和开发计划

### ⭐ 参考
- **[RECORDING_QUICKSTART.md](RECORDING_QUICKSTART.md)** - Playwright 录制快速指南
- **[PLAYWRIGHT_RECORDING_GUIDE.md](PLAYWRIGHT_RECORDING_GUIDE.md)** - 录制功能详细指南
- **[backend/README.md](backend/README.md)** - 后端开发文档

### 📄 部署
- **[docker-compose.yml](docker-compose.yml)** - Docker Compose 开发配置
- **[docker-compose.prod.yml](docker-compose.prod.yml)** - Docker Compose 生产配置
- **[docker/](docker/)** - Docker 构建文件

---

## 🗂️ 已删除的测试文件（不必要的开发临时文件）

✅ `backend/test_api.py` - API 测试脚本
✅ `backend/test_playwright.py` - Playwright 测试脚本
✅ `backend/create_test_user.py` - 临时创建用户脚本
✅ `backend/log.txt` - 日志文件
✅ `token.txt` - 临时 token 文件
✅ `backend/setup_database.sql` - 临时 SQL 文件

---

## 🚀 快速启动参考

### 后端启动
```bash
cd backend
python manage.py init_db  # 初始化数据库
python app.py             # 启动开发服务器
```

### 前端启动
```bash
cd web
npm install  # 首次安装依赖
npm run dev  # 启动开发服务器
```

### Docker 启动
```bash
docker-compose up -d
```

---

## 📊 项目统计

- **后端模型**: 8 个（User, Project, ApiTestCase, WebTestScript 等）
- **后端 API**: 8 个模块（auth, api_test, web_test, perf_test 等）
- **前端页面**: 3 + 3 + 3 个模块化页面
- **文档**: 8 个详细指南
- **部署方案**: Docker + Docker Compose

---

**最后更新**: 2025-12-25
**项目状态**: 生产就绪 ✅
