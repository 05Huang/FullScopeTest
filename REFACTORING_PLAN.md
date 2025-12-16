# 🔄 自动化测试平台重构计划

**项目名称**：EasyTest - 简易自动化测试平台  
**版本**：v2.0  
**重构日期**：2025年12月19日  
**目标用户**：个人开发者、小型团队

---

## 📋 目录

1. [项目背景与目标](#1-项目背景与目标)
2. [技术选型](#2-技术选型)
3. [项目架构](#3-项目架构)
4. [目录结构](#4-目录结构)
5. [功能模块设计](#5-功能模块设计)
6. [数据库设计](#6-数据库设计)
7. [API 设计](#7-api-设计)
8. [前端设计规范](#8-前端设计规范)
9. [部署方案](#9-部署方案)
10. [开发计划](#10-开发计划)

---

## 1. 项目背景与目标

### 1.1 项目背景

市面上的测试工具（如 Postman、JMeter、LoadRunner 等）功能强大，但对于个人开发者存在以下痛点：

- **学习成本高**：功能繁杂，上手困难
- **付费限制**：高级功能需要付费订阅
- **资源占用**：桌面应用占用系统资源
- **协作困难**：测试数据和配置不易共享
- **报告简陋**：免费版报告功能受限

### 1.2 核心目标

打造一个**简单易用、功能实用、开箱即用**的 Web 测试平台：

| 目标 | 描述 |
|------|------|
| 🎯 **简单易用** | 零学习成本，5分钟上手 |
| 🚀 **快速测试** | 快速发送 HTTP 请求，实时查看响应 |
| 📊 **专业报告** | 生成美观的可视化测试报告 |
| 🔧 **多种测试** | 支持接口测试、性能测试、自动化测试 |
| 📝 **文档管理** | 支持测试文档编写和管理 |
| 🌐 **在线访问** | 部署到服务器，随时随地使用 |

### 1.3 目标用户画像

```
┌─────────────────────────────────────────────────────────────┐
│  🧑‍💻 个人开发者                                              │
│  ├── 需要快速测试自己开发的 API                               │
│  ├── 不想花时间学习复杂工具                                    │
│  └── 希望有简单的测试报告                                     │
├─────────────────────────────────────────────────────────────┤
│  👥 小型团队                                                 │
│  ├── 需要共享测试用例和环境配置                                │
│  ├── 希望有统一的测试平台                                     │
│  └── 预算有限，倾向开源方案                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 技术选型

### 2.1 后端技术栈

| 技术 | 版本 | 用途 | 选择理由 |
|------|------|------|----------|
| **Python** | 3.10+ | 后端语言 | 生态丰富，测试框架完善 |
| **Flask** | 3.0+ | Web 框架 | 轻量级、灵活、易于扩展 |
| **PostgreSQL** | 15+ | 数据库 | 稳定可靠，支持 JSON 字段，适合生产环境 |
| **SQLAlchemy** | 2.0+ | ORM | 数据库抽象层，便于迁移 |
| **Flask-Migrate** | 4.0+ | 数据库迁移 | 版本化管理数据库结构 |
| **Flask-JWT-Extended** | 4.5+ | 认证 | JWT Token 认证 |
| **Celery** | 5.3+ | 任务队列 | 异步执行测试任务 |
| **Redis** | 7.0+ | 缓存/消息队列 | 配合 Celery，缓存热点数据 |
| **pytest** | 7.4+ | 测试框架 | 自动化测试执行 |
| **locust** | 2.0+ | 性能测试 | 分布式压力测试 |
| **allure-pytest** | 2.13+ | 报告生成 | 美观的测试报告 |

### 2.2 前端技术栈

> **关于 React Native 的建议**：React Native 主要用于开发移动端应用（iOS/Android），对于 Web 平台，建议使用 **React.js** 或 **Vue.js**。

考虑到项目的**简洁性**和**开发效率**，我推荐以下方案：

| 方案 | 技术栈 | 优点 | 适用场景 |
|------|--------|------|----------|
| **方案 A（推荐）** | React 18 + TypeScript + Ant Design | 组件丰富、企业级、文档完善 | 功能丰富的管理平台 |
| **方案 B** | Vue 3 + TypeScript + Element Plus | 易学易用、中文生态好 | 快速开发、中小型项目 |

**最终选择：React 18 + TypeScript + Ant Design Pro**

选择理由：
1. **Ant Design Pro**：提供开箱即用的管理后台模板
2. **TypeScript**：类型安全，减少运行时错误
3. **组件丰富**：表格、表单、图表等组件齐全
4. **设计规范**：统一的设计语言，界面专业
5. **国际化**：支持多语言

### 2.3 基础设施

| 组件 | 技术 | 用途 |
|------|------|------|
| **Web 服务器** | Nginx | 反向代理、静态资源服务 |
| **WSGI 服务器** | Gunicorn | Python 应用服务器 |
| **容器化** | Docker + Docker Compose | 一键部署 |
| **进程管理** | Supervisor | 进程守护 |

---

## 3. 项目架构

### 3.1 整体架构图

```
┌────────────────────────────────────────────────────────────────────────────┐
│                              用户浏览器                                      │
└─────────────────────────────────┬──────────────────────────────────────────┘
                                  │ HTTPS
                                  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                           Nginx (反向代理)                                   │
│  ┌─────────────────────────┐  ┌──────────────────────────────────────────┐ │
│  │   静态资源 (React 构建)   │  │        API 代理 (/api/*)                  │ │
│  └─────────────────────────┘  └──────────────────────────────────────────┘ │
└─────────────────────────────────┬──────────────────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│   Flask API     │    │    Celery Worker    │    │    Redis        │
│   (Gunicorn)    │◄───│   (异步任务处理)     │◄───│  (消息队列/缓存) │
└────────┬────────┘    └──────────┬──────────┘    └─────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                          PostgreSQL 数据库                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │  用户表   │ │  项目表   │ │  测试用例 │ │  测试报告 │ │  测试文档 │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 模块架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EasyTest 平台                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  接口测试    │  │  性能测试    │  │  自动化测试  │  │  测试文档    │        │
│  │  模块       │  │  模块       │  │  模块       │  │  模块       │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  项目管理    │  │  环境管理    │  │  测试报告    │  │  用户管理    │        │
│  │  模块       │  │  模块       │  │  模块       │  │  模块       │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 目录结构

### 4.1 项目根目录

```
pt_project/
│
├── 📂 web/                      # 前端项目 (React + TypeScript)
│   ├── 📂 public/               # 静态资源
│   ├── 📂 src/                  # 源代码
│   │   ├── 📂 components/       # 公共组件
│   │   ├── 📂 pages/            # 页面组件
│   │   ├── 📂 services/         # API 服务层
│   │   ├── 📂 stores/           # 状态管理 (Zustand)
│   │   ├── 📂 hooks/            # 自定义 Hooks
│   │   ├── 📂 utils/            # 工具函数
│   │   ├── 📂 types/            # TypeScript 类型定义
│   │   ├── 📂 styles/           # 全局样式
│   │   └── 📄 App.tsx           # 应用入口
│   ├── 📄 package.json          # 依赖配置
│   ├── 📄 tsconfig.json         # TypeScript 配置
│   ├── 📄 vite.config.ts        # Vite 构建配置
│   └── 📄 README.md             # 前端说明文档
│
├── 📂 backend/                  # 后端项目 (Flask + PostgreSQL)
│   ├── 📂 app/                  # 应用核心
│   │   ├── 📂 api/              # API 路由
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth.py       # 认证接口
│   │   │   ├── 📄 projects.py   # 项目管理接口
│   │   │   ├── 📄 environments.py # 环境管理接口
│   │   │   ├── 📄 test_cases.py # 测试用例接口
│   │   │   ├── 📄 test_runs.py  # 测试执行接口
│   │   │   ├── 📄 reports.py    # 报告接口
│   │   │   ├── 📄 performance.py # 性能测试接口
│   │   │   └── 📄 docs.py       # 测试文档接口
│   │   ├── 📂 models/           # 数据模型
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 user.py       # 用户模型
│   │   │   ├── 📄 project.py    # 项目模型
│   │   │   ├── 📄 environment.py # 环境模型
│   │   │   ├── 📄 test_case.py  # 测试用例模型
│   │   │   ├── 📄 test_run.py   # 测试执行记录模型
│   │   │   ├── 📄 report.py     # 报告模型
│   │   │   └── 📄 document.py   # 文档模型
│   │   ├── 📂 services/         # 业务逻辑层
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 test_executor.py   # 测试执行服务
│   │   │   ├── 📄 report_generator.py # 报告生成服务
│   │   │   ├── 📄 performance_tester.py # 性能测试服务
│   │   │   └── 📄 http_client.py     # HTTP 客户端封装
│   │   ├── 📂 tasks/            # Celery 异步任务
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 test_tasks.py      # 测试任务
│   │   │   └── 📄 report_tasks.py    # 报告生成任务
│   │   ├── 📂 utils/            # 工具函数
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 validators.py      # 数据验证
│   │   │   ├── 📄 response.py        # 响应格式化
│   │   │   └── 📄 logger.py          # 日志工具
│   │   ├── 📄 __init__.py       # 应用工厂
│   │   ├── 📄 config.py         # 配置管理
│   │   └── 📄 extensions.py     # Flask 扩展初始化
│   ├── 📂 migrations/           # 数据库迁移文件
│   ├── 📂 tests/                # 单元测试
│   ├── 📄 requirements.txt      # Python 依赖
│   ├── 📄 celery_worker.py      # Celery 启动文件
│   ├── 📄 wsgi.py               # WSGI 入口
│   └── 📄 README.md             # 后端说明文档
│
├── 📂 document/                 # 项目文档
│   ├── 📄 README.md             # 项目总览
│   ├── 📄 ARCHITECTURE.md       # 架构设计
│   ├── 📄 API_REFERENCE.md      # API 文档
│   ├── 📄 DEPLOYMENT.md         # 部署指南
│   ├── 📄 DEVELOPMENT.md        # 开发指南
│   ├── 📄 CHANGELOG.md          # 更新日志
│   └── 📂 images/               # 文档图片
│
├── 📂 docker/                   # Docker 配置
│   ├── 📄 Dockerfile.frontend   # 前端 Docker 配置
│   ├── 📄 Dockerfile.backend    # 后端 Docker 配置
│   ├── 📄 docker-compose.yml    # 开发环境编排
│   ├── 📄 docker-compose.prod.yml # 生产环境编排
│   └── 📂 nginx/                # Nginx 配置
│       ├── 📄 nginx.conf        # Nginx 主配置
│       └── 📄 ssl/              # SSL 证书目录
│
├── 📂 scripts/                  # 脚本工具
│   ├── 📄 init_db.py            # 初始化数据库
│   ├── 📄 backup_db.sh          # 数据库备份脚本
│   └── 📄 deploy.sh             # 部署脚本
│
├── 📄 .env.example              # 环境变量模板
├── 📄 .gitignore                # Git 忽略文件
├── 📄 Makefile                  # 常用命令封装
└── 📄 README.md                 # 项目说明
```

---

## 5. 功能模块设计

### 5.1 核心功能模块

#### 📡 接口测试模块

```
功能特性：
├── 🔹 快速请求发送
│   ├── 支持 GET/POST/PUT/DELETE/PATCH 等方法
│   ├── 请求参数管理（Query/Headers/Body）
│   ├── 多种 Body 格式（JSON/Form/Raw/Binary）
│   └── 环境变量替换 {{variable}}
│
├── 🔹 响应查看
│   ├── 状态码、响应时间、大小显示
│   ├── JSON 格式化/高亮显示
│   ├── Headers 查看
│   └── 响应断言验证
│
├── 🔹 请求历史
│   ├── 自动保存请求记录
│   ├── 快速重发历史请求
│   └── 历史搜索和筛选
│
└── 🔹 批量测试
    ├── 集合批量执行
    ├── 数据驱动测试（CSV/JSON）
    └── 并发请求测试
```

#### 🚀 性能测试模块

```
功能特性：
├── 🔹 压力测试
│   ├── 配置并发用户数
│   ├── 配置请求持续时间
│   ├── 配置请求速率 (RPS)
│   └── 实时监控测试进度
│
├── 🔹 性能指标
│   ├── 响应时间（平均/P50/P90/P99）
│   ├── 吞吐量 (TPS)
│   ├── 错误率
│   └── 带宽使用
│
├── 🔹 可视化图表
│   ├── 响应时间趋势图
│   ├── 吞吐量曲线
│   ├── 错误分布图
│   └── 资源使用监控
│
└── 🔹 性能报告
    ├── HTML 格式报告
    ├── 测试结果对比
    └── 性能基线设置
```

#### 🤖 自动化测试模块

```
功能特性：
├── 🔹 测试用例管理
│   ├── 用例创建/编辑/删除
│   ├── 用例分组（按模块/功能）
│   ├── 用例标签管理
│   └── 用例优先级设置
│
├── 🔹 测试执行
│   ├── 单用例执行
│   ├── 批量执行
│   ├── 定时执行（Cron）
│   └── CI/CD 集成接口
│
├── 🔹 断言验证
│   ├── 状态码断言
│   ├── JSON 路径断言
│   ├── 响应时间断言
│   ├── 正则表达式匹配
│   └── 数据库断言（可选）
│
└── 🔹 数据管理
    ├── 测试数据模板
    ├── 数据参数化
    ├── 前置/后置操作
    └── 变量提取和传递
```

#### 📊 测试报告模块

```
功能特性：
├── 🔹 报告概览
│   ├── 测试执行统计（通过/失败/跳过）
│   ├── 执行时间统计
│   ├── 趋势分析图表
│   └── 模块覆盖率
│
├── 🔹 详细报告
│   ├── 每个用例的执行详情
│   ├── 请求/响应数据记录
│   ├── 错误堆栈信息
│   ├── 截图/日志附件
│   └── 失败原因分析
│
├── 🔹 报告导出
│   ├── HTML 格式
│   ├── PDF 格式
│   ├── Excel 格式
│   └── 邮件发送
│
└── 🔹 Allure 集成
    ├── Allure 报告生成
    ├── 历史趋势对比
    └── 报告在线预览
```

#### 📝 测试文档模块

```
功能特性：
├── 🔹 文档编辑
│   ├── Markdown 编辑器
│   ├── 富文本编辑器
│   ├── 实时预览
│   └── 图片/文件上传
│
├── 🔹 文档管理
│   ├── 文档分类/目录
│   ├── 文档搜索
│   ├── 版本管理
│   └── 文档模板
│
├── 🔹 自动生成
│   ├── 从测试用例生成文档
│   ├── API 文档生成
│   ├── 测试计划模板
│   └── 测试报告模板
│
└── 🔹 导出分享
    ├── Word 导出
    ├── PDF 导出
    ├── 在线分享链接
    └── 团队协作编辑
```

### 5.2 辅助功能模块

#### 🗂️ 项目管理

- 多项目支持
- 项目成员管理
- 项目配置（环境变量、全局 Headers）
- 项目导入/导出

#### 🌍 环境管理

- 多环境配置（开发/测试/生产）
- 环境变量管理
- 环境快速切换
- 环境复制

#### 👥 用户管理

- 用户注册/登录
- 角色权限管理
- 操作日志审计
- 个人设置

---

## 6. 数据库设计

### 6.1 ER 图

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │       │    projects     │       │  environments   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │───┐   │ id (PK)         │───┐   │ id (PK)         │
│ username        │   │   │ name            │   │   │ project_id (FK) │
│ email           │   │   │ description     │   │   │ name            │
│ password_hash   │   │   │ owner_id (FK)   │   │   │ base_url        │
│ avatar          │   │   │ created_at      │   │   │ variables       │
│ created_at      │   │   │ updated_at      │   │   │ headers         │
│ last_login      │   │   └────────┬────────┘   │   │ is_default      │
└─────────────────┘   │            │             │   │ created_at      │
                      │            │             │   └────────┬────────┘
                      └────────────┴─────────────┴────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   collections   │       │   test_cases    │       │   test_runs     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │───┐   │ id (PK)         │       │ id (PK)         │
│ project_id (FK) │   │   │ collection_id   │       │ project_id (FK) │
│ name            │   │   │ name            │       │ status          │
│ description     │   │   │ method          │       │ total_cases     │
│ parent_id       │   │   │ url             │       │ passed          │
│ sort_order      │   │   │ headers         │       │ failed          │
│ created_at      │   │   │ body            │       │ skipped         │
│ updated_at      │   │   │ assertions      │       │ duration        │
└────────┬────────┘   │   │ pre_script      │       │ report_path     │
         │            │   │ post_script     │       │ triggered_by    │
         │            │   │ created_at      │       │ created_at      │
         │            │   │ updated_at      │       └─────────────────┘
         │            │   └─────────────────┘
         │            │
         │            │   ┌─────────────────┐       ┌─────────────────┐
         │            │   │   test_docs     │       │  perf_tests     │
         │            │   ├─────────────────┤       ├─────────────────┤
         │            │   │ id (PK)         │       │ id (PK)         │
         │            │   │ project_id (FK) │       │ project_id (FK) │
         │            │   │ title           │       │ name            │
         │            │   │ content         │       │ config          │
         │            │   │ category        │       │ results         │
         │            │   │ version         │       │ status          │
         │            │   │ created_by      │       │ created_at      │
         │            │   │ created_at      │       └─────────────────┘
         │            │   │ updated_at      │
         │            │   └─────────────────┘
         │            │
         └────────────┘
```

### 6.2 核心表结构

#### users 用户表

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

#### projects 项目表

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### test_cases 测试用例表

```sql
CREATE TABLE test_cases (
    id SERIAL PRIMARY KEY,
    collection_id INTEGER REFERENCES collections(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL DEFAULT 'GET',
    url VARCHAR(500) NOT NULL,
    headers JSONB DEFAULT '{}',
    params JSONB DEFAULT '{}',
    body JSONB,
    assertions JSONB DEFAULT '[]',
    pre_script TEXT,
    post_script TEXT,
    variables JSONB DEFAULT '{}',
    tags VARCHAR(255)[],
    priority INTEGER DEFAULT 2,
    is_enabled BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. API 设计

### 7.1 API 规范

- RESTful 风格
- 统一响应格式
- JWT Token 认证
- API 版本控制

### 7.2 统一响应格式

```json
{
    "code": 200,
    "message": "success",
    "data": { ... },
    "timestamp": "2025-12-19T10:30:00Z"
}
```

### 7.3 核心 API 列表

| 模块 | 方法 | 路径 | 描述 |
|------|------|------|------|
| **认证** | POST | /api/v1/auth/login | 用户登录 |
| | POST | /api/v1/auth/register | 用户注册 |
| | POST | /api/v1/auth/logout | 退出登录 |
| | GET | /api/v1/auth/me | 获取当前用户 |
| **项目** | GET | /api/v1/projects | 获取项目列表 |
| | POST | /api/v1/projects | 创建项目 |
| | GET | /api/v1/projects/:id | 获取项目详情 |
| | PUT | /api/v1/projects/:id | 更新项目 |
| | DELETE | /api/v1/projects/:id | 删除项目 |
| **环境** | GET | /api/v1/projects/:id/environments | 获取环境列表 |
| | POST | /api/v1/projects/:id/environments | 创建环境 |
| | PUT | /api/v1/environments/:id | 更新环境 |
| | DELETE | /api/v1/environments/:id | 删除环境 |
| **测试用例** | GET | /api/v1/collections/:id/cases | 获取用例列表 |
| | POST | /api/v1/collections/:id/cases | 创建用例 |
| | PUT | /api/v1/cases/:id | 更新用例 |
| | DELETE | /api/v1/cases/:id | 删除用例 |
| | POST | /api/v1/cases/:id/run | 执行单个用例 |
| **测试执行** | POST | /api/v1/projects/:id/runs | 创建测试执行 |
| | GET | /api/v1/runs/:id | 获取执行详情 |
| | GET | /api/v1/runs/:id/report | 获取测试报告 |
| **性能测试** | POST | /api/v1/projects/:id/performance | 创建性能测试 |
| | GET | /api/v1/performance/:id | 获取测试结果 |
| | POST | /api/v1/performance/:id/stop | 停止测试 |
| **测试文档** | GET | /api/v1/projects/:id/docs | 获取文档列表 |
| | POST | /api/v1/projects/:id/docs | 创建文档 |
| | PUT | /api/v1/docs/:id | 更新文档 |
| | DELETE | /api/v1/docs/:id | 删除文档 |

---

## 8. 前端设计规范

### 8.1 设计原则

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           设计原则                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🎯 简洁清晰                                                             │
│     └── 界面简洁，功能直观，减少用户思考                                    │
│                                                                          │
│  🎨 风格统一                                                             │
│     └── 统一的色彩、字体、间距、组件样式                                    │
│                                                                          │
│  ⚡ 流畅高效                                                             │
│     └── 响应迅速，交互流畅，减少等待                                       │
│                                                                          │
│  📱 响应式设计                                                           │
│     └── 适配桌面、平板、移动设备                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 8.2 色彩规范

```
主色调：
├── Primary:    #1890ff (蓝色 - 主要操作)
├── Success:    #52c41a (绿色 - 成功状态)
├── Warning:    #faad14 (橙色 - 警告状态)
├── Error:      #f5222d (红色 - 错误状态)
└── Info:       #1890ff (蓝色 - 信息提示)

中性色：
├── Title:      #262626 (标题文字)
├── Text:       #595959 (正文文字)
├── Secondary:  #8c8c8c (辅助文字)
├── Border:     #d9d9d9 (边框颜色)
├── Divider:    #f0f0f0 (分割线)
└── Background: #f5f5f5 (背景色)
```

### 8.3 页面布局

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LOGO     📁 项目  📡 接口  🚀 性能  📊 报告  📝 文档     👤 用户      │  ← Header
├─────────┬───────────────────────────────────────────────────────────────┤
│         │                                                               │
│  侧边栏  │                      主内容区                                 │
│         │                                                               │
│  • 项目1 │   ┌─────────────────────────────────────────────────────┐    │
│  • 项目2 │   │                    面包屑导航                         │    │
│  • 项目3 │   ├─────────────────────────────────────────────────────┤    │
│         │   │                                                       │    │
│         │   │                    内容区域                            │    │
│         │   │                                                       │    │
│         │   │                                                       │    │
│         │   │                                                       │    │
│         │   └─────────────────────────────────────────────────────┘    │
│         │                                                               │
└─────────┴───────────────────────────────────────────────────────────────┘
```

---

## 9. 部署方案

### 9.1 本地开发环境

```bash
# 启动 PostgreSQL 和 Redis (Docker)
docker-compose -f docker/docker-compose.yml up -d postgres redis

# 启动后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask run --port=5000

# 启动前端
cd web
npm install
npm run dev
```

### 9.2 生产环境部署

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/ssl:/etc/nginx/ssl
      - ./web/dist:/usr/share/nginx/html
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/easytest
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  celery:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    command: celery -A celery_worker worker -l info
    depends_on:
      - redis
      - postgres

  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=easytest
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=easytest

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 9.3 域名配置

当您获得域名后，需要进行以下配置：

1. **DNS 解析**：将域名 A 记录指向服务器 IP
2. **SSL 证书**：使用 Let's Encrypt 免费证书
3. **Nginx 配置**：配置反向代理和 SSL

```nginx
# nginx.conf 示例
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # 前端静态资源
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 10. 开发计划

### 10.1 阶段划分

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           开发阶段规划                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  📦 阶段一：基础架构搭建 (预计 2-3 天)                                     │
│     ├── 创建项目目录结构                                                  │
│     ├── 后端 Flask 项目初始化                                            │
│     ├── 前端 React 项目初始化                                            │
│     ├── PostgreSQL 数据库配置                                            │
│     └── Docker 开发环境配置                                              │
│                                                                          │
│  🔐 阶段二：用户系统 (预计 1-2 天)                                        │
│     ├── 用户注册/登录接口                                                 │
│     ├── JWT Token 认证                                                   │
│     ├── 前端登录/注册页面                                                 │
│     └── 路由守卫实现                                                      │
│                                                                          │
│  📡 阶段三：接口测试模块 (预计 3-4 天)                                     │
│     ├── 项目/集合/用例 CRUD                                               │
│     ├── 请求编辑器组件                                                    │
│     ├── 请求发送和响应显示                                                 │
│     ├── 环境变量管理                                                      │
│     └── 请求历史记录                                                      │
│                                                                          │
│  🚀 阶段四：自动化测试 (预计 2-3 天)                                       │
│     ├── 测试用例批量执行                                                  │
│     ├── 断言验证系统                                                      │
│     ├── Celery 异步任务                                                  │
│     └── 数据驱动测试                                                      │
│                                                                          │
│  📊 阶段五：测试报告 (预计 2 天)                                          │
│     ├── 报告数据统计                                                      │
│     ├── 可视化图表                                                        │
│     ├── Allure 报告集成                                                  │
│     └── 报告导出功能                                                      │
│                                                                          │
│  ⚡ 阶段六：性能测试 (预计 2-3 天)                                         │
│     ├── Locust 集成                                                      │
│     ├── 性能测试配置界面                                                  │
│     ├── 实时监控展示                                                      │
│     └── 性能报告生成                                                      │
│                                                                          │
│  📝 阶段七：测试文档 (预计 1-2 天)                                         │
│     ├── Markdown 编辑器                                                  │
│     ├── 文档分类管理                                                      │
│     └── 文档导出功能                                                      │
│                                                                          │
│  🚀 阶段八：部署上线 (预计 1-2 天)                                         │
│     ├── 生产环境 Docker 配置                                              │
│     ├── Nginx 配置                                                       │
│     ├── SSL 证书配置                                                     │
│     └── 域名绑定                                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

总计预估时间：14-21 天
```

### 10.2 优先级排序

| 优先级 | 功能 | 重要性 | 难度 |
|--------|------|--------|------|
| P0 | 基础架构搭建 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| P0 | 接口测试核心功能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| P1 | 用户认证系统 | ⭐⭐⭐⭐ | ⭐⭐ |
| P1 | 测试报告展示 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| P2 | 自动化测试执行 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| P2 | 性能测试 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| P3 | 测试文档管理 | ⭐⭐⭐ | ⭐⭐ |

---

## 📋 确认清单

请确认以下内容后，我将开始执行重构：

- [ ] **技术选型确认**
  - 后端：Flask + PostgreSQL + Redis + Celery
  - 前端：React 18 + TypeScript + Ant Design
  
- [ ] **功能模块确认**
  - 接口测试（核心功能）
  - 性能测试（Locust 集成）
  - 自动化测试（批量执行、断言）
  - 测试报告（可视化、导出）
  - 测试文档（Markdown 编辑）

- [ ] **目录结构确认**
  - web/ (前端)
  - backend/ (后端)
  - document/ (文档)

- [ ] **部署方案确认**
  - 本机服务器
  - Docker 容器化部署
  - Nginx 反向代理

---

**请您确认上述计划，或提出修改意见后，我将开始执行重构工作！** 🚀
