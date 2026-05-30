# FullScopeTest —— AI一站式自动化测试平台

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69bfd011e4b01ee6a7b76b33.png" alt="FullScopeTest Banner" width="100%" />


  <br />

  **AI-Native 全链路自动化测试平台**
  <br />
  AI 编排 · API 测试 · Web 自动化 · APP 测试 · 性能压测 · 智能报告

  <a href="README.md">中文</a> | <a href="README_EN.md">English</a>

  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
  [![TypeScript](https://img.shields.io/badge/typescript-5.x-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
  [![React](https://img.shields.io/badge/react-18-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
  [![Vite](https://img.shields.io/badge/vite-6-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
  [![Flask](https://img.shields.io/badge/flask-3.0-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-ORM-D71F00?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
  [![Ant Design](https://img.shields.io/badge/ant--design-5-0170FE?style=flat&logo=antdesign&logoColor=white)](https://ant.design/)
  [![Playwright](https://img.shields.io/badge/playwright-e2e-2EAD33?style=flat&logo=playwright)](https://playwright.dev/)
  [![Celery](https://img.shields.io/badge/celery-task--queue-37814A?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
  [![Redis](https://img.shields.io/badge/redis-broker-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
  [![PostgreSQL](https://img.shields.io/badge/postgresql-15-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Docker](https://img.shields.io/badge/docker-compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
  [![Vitest](https://img.shields.io/badge/vitest-testing-6E9F18?style=flat&logo=vitest&logoColor=white)](https://vitest.dev/)

  <h2>🔥 在线演示地址: <a href="http://test.huangxuan.chat">test.huangxuan.chat</a> 🔥</h2>
</div>

## 📖 项目简介

**FullScopeTest** 是一个 AI 驱动的全链路自动化测试平台，覆盖 API 接口测试、Web UI 自动化、APP 移动端测试和性能压测四大领域。平台以 **AI-Native** 为核心设计理念，提供自然语言编排、脚本自动生成、智能错误分析与自愈等能力，降低测试编写与维护门槛。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c01107e4b01ee6a7b76b3a.png" alt="Dashboard 预览" width="80%" />
  <p><em>平台总览控制台</em></p>
</div>


---

## ✨ 核心特性

### AI 能力 (AI-Native)

#### 1. AI 自动编排

输入自然语言测试目标，AI 自动解析意图并生成结构化执行计划（Plan），随后调用平台 API 自动创建环境、集合、用例并执行。前端面板支持运行时动态配置 `base_url` / `model` / `api_key`，兼容 OpenAI、DeepSeek 等主流 LLM。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c01159e4b01ee6a7b76b3b.png" alt="AI 自动编排 — 输入测试目标" width="45%" />
  <img src="https://res.huangxuan.chat/thrivex/album/69c01159e4b01ee6a7b76b3c.png" alt="AI 自动编排 — 自动生成并执行" width="45%" />
  <p><em>自然语言 → 结构化计划 → 自动执行</em></p>
</div>

#### 2. NL2Script — 自然语言生成测试脚本

输入自然语言描述（如"登录系统，进入控制台，创建用户，验证成功提示"），AI Agent 将其转换为可执行的 Playwright Web 测试脚本或 Locust 性能测试脚本。生成结果在 Monaco Editor 中高亮展示，支持在线编辑与审查。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ae4b01ee6a7b76b41.png" alt="NL2Script — 自然语言生成测试脚本" width="80%" />
</div>

#### 3. 智能错误分析与自愈

测试失败时自动触发 AI 诊断：分析错误日志、API 响应体或 DOM 结构，定位根因（如选择器变更、字段缺失）。支持一键修复 — AI 自动修正断言或选择器后重新执行，降低用例维护成本。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ae4b01ee6a7b76b42.png" alt="智能错误分析" width="45%" />
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144be4b01ee6a7b76b43.png" alt="一键自愈修复" width="45%" />
  <p><em>错误定位 → AI 诊断 → 一键修复</em></p>
</div>

#### 4. 智能测试数据生成与用例裂变

基于 API 定义或已有用例，AI 自动推断字段语义，批量生成边界值、空值、注入攻击等异常测试数据，将单条用例裂变为覆盖多种场景的测试集，提升测试覆盖率。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144be4b01ee6a7b76b44.png" alt="AI 数据生成" width="45%" />
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144be4b01ee6a7b76b45.png" alt="用例裂变" width="45%" />
  <p><em>单条用例 → AI 裂变 → 多场景覆盖</em></p>
</div>

#### 5. 探索性测试 Agent

给定起始 URL 和测试目标，AI Agent 自主遍历页面 — 解析 DOM、点击按钮、填写表单、记录异常。结合 Vision 模型进行视觉验证，最终输出探索测试报告（JS 错误、404 死链、安全风险）。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ce4b01ee6a7b76b46.png" alt="探索性测试 Agent" width="80%" />
</div>

#### 6. 全局 Copilot

统一的 AI 对话入口，支持通过自然语言指令操作平台："创建性能测试场景，并发 100 持续 5 分钟"、"查询昨日失败的 Web 测试"。后端通过 Function Calling 解析意图，直接调用平台 API 执行操作。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ce4b01ee6a7b76b47.png" alt="全局 Copilot" width="80%" />
</div>

---

### 测试工作台 (Core Workspace)

#### API 接口测试

完整的 HTTP/REST API 测试工作台，支持环境变量 `{variable}` 替换、前置/后置脚本引擎、变量提取与断言、一键 cURL 导入导出。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c011b3e4b01ee6a7b76b3d.png" alt="API 接口测试工作台" width="80%" />
</div>

#### Web 自动化测试 (Playwright)

内置 Playwright 引擎，支持在线编写、编辑、执行 Python 测试脚本。可通过 `playwright codegen` 录制交互操作自动生成脚本。任务通过 Celery 异步执行，支持实时状态跟踪与错误定位。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c011e4e4b01ee6a7b76b3e.png" alt="Web 自动化测试" width="80%" />
</div>

#### 性能测试 (Locust)

基于 Locust 的分布式压测，支持并发用户数配置与阶梯加压（Step load）。实时采集并可视化响应时间、吞吐量 (RPS)、错误率等核心指标。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69bfd012e4b01ee6a7b76b35.png" alt="性能测试看板" width="80%" />
</div>

#### APP 移动端测试 (Appium)

基于 Appium 的移动应用自动化测试，支持 Android / iOS 双平台。通过配置 package/activity（Android）或 bundle_id（iOS）连接真机或模拟器，在线编写 Appium Python 脚本并通过 Celery 异步执行。

#### 测试报告中心

聚合 API、Web、APP、性能四类测试的执行结果，提供按类型统计、每日趋势、成功率等可视化指标。支持 HTML 和 JSON 格式导出，Dashboard 首页展示全局测试概览。

#### 环境变量管理

独立的环境管理模块，支持创建多套环境（开发/测试/预发/生产），每套环境包含自定义变量与请求头。API 测试中通过 `{variable}` 语法自动替换，支持设置默认环境。

#### 测试文档管理

内置测试文档管理，支持 Markdown 编辑、分类检索与关键词搜索。提供测试计划、测试用例、API 文档等内置模板，支持导出为 Markdown / HTML。

#### Mock Server

API 用例级别 Mock，启用后直接返回预设响应（状态码、响应体、响应头、延迟时间），无需依赖真实后端服务，便于前端并行开发与联调。

#### Webhook 触发器与定时任务

支持创建 Webhook 触发器（HMAC-SHA256 签名验证），通过 HTTP 请求触发测试集合执行。定时任务支持 Cron 表达式调度，基于 APScheduler 实现，文件锁保证多进程安全。

---

## 🏛 系统架构概览

### 整体架构

```mermaid
graph LR
    subgraph 客户端
        Browser["浏览器"]
    end

    subgraph Nginx / OpenResty
        Static["静态资源<br/>(React SPA)"]
        Proxy["反向代理<br/>/api → :5000(Dev)<br/>/api → :8000(Prod)"]
        WS["WebSocket<br/>(Live View)"]
    end

    subgraph Flask Backend :5000(Dev) / :8000(Prod)
        API["API 蓝图层<br/>12 个模块"]
        Auth["JWT 认证<br/>+ RBAC 权限"]
        ORM["SQLAlchemy ORM<br/>15 个数据模型"]
    end

    subgraph Async Workers
        Celery["Celery Worker<br/>(Web / Perf 测试)"]
        Scheduler["APScheduler<br/>(定时任务)"]
    end

    subgraph AI Layer
        Copilot["AI Copilot"]
        Agent["AI Agent<br/>(编排 / 脚本生成)"]
    end

    subgraph Data Stores
        PG["PostgreSQL"]
        Redis["Redis<br/>(消息队列 + 缓存)"]
    end

    Browser --> Static
    Browser --> Proxy
    Proxy --> API
    API --> Auth
    Auth --> ORM
    ORM --> PG
    API --> Celery
    Celery --> Redis
    Scheduler --> Celery
    API --> Copilot
    Copilot --> Agent
    Agent -->|OpenAI / DeepSeek 等| LLM["LLM API"]
    WS -->|VNC Live View| VNC["x11vnc + websockify"]
    Celery -->|Playwright| VNC
```

### 请求处理流程

```mermaid
sequenceDiagram
    participant U as 用户浏览器
    participant N as Nginx / OpenResty
    participant F as Flask API
    participant DB as PostgreSQL
    participant R as Redis
    participant C as Celery Worker
    participant AI as LLM API

    U->>N: HTTPS 请求
    N->>F: 反向代理 /api/*
    F->>F: JWT 鉴权 + RBAC 校验
    F->>DB: 读写业务数据
    F-->>U: 同步响应 (JSON)

    Note over U,F: 异步任务场景 (Web/Perf 测试)
    F->>R: 发送 Celery 任务
    F-->>U: 返回 task_id
    R->>C: 消费任务
    C->>DB: 写入测试结果
    C->>R: 更新任务状态
    U->>F: 轮询任务状态
    F->>R: 查询 Celery 状态
    F-->>U: 返回进度与结果

    Note over F,AI: AI 辅助场景
    F->>AI: 发送 Prompt (含上下文)
    AI-->>F: 返回结构化结果
    F-->>U: AI 生成的用例 / 脚本 / 分析
```

### 技术栈总览

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **前端框架** | React 18 + TypeScript | 组件化 SPA，严格类型检查 |
| **构建工具** | Vite 6 | 极速 HMR，开箱即用的 TS/JSX 支持 |
| **UI 组件库** | Ant Design 5 | 企业级 UI，ProComponents 扩展 |
| **代码编辑器** | Monaco Editor | VS Code 同源编辑器，支持语法高亮与自动补全 |
| **状态管理** | Zustand | 轻量级 Store，支持 persist 持久化 + devtools |
| **HTTP 客户端** | Axios | 拦截器统一注入 JWT，自动 Token 刷新 |
| **前端测试** | Vitest + Testing Library | jsdom 环境，组件级单元测试 |
| **后端框架** | Flask 3.0 | 应用工厂模式 + Blueprint 模块化 |
| **ORM** | SQLAlchemy + Alembic | 声明式模型 + 数据库版本迁移 |
| **认证鉴权** | Flask-JWT-Extended | 双 Token 机制 (access + refresh) |
| **任务队列** | Celery + Redis | 异步执行 Web/性能测试任务 |
| **定时调度** | APScheduler | 文件锁单例，支持多进程安全 |
| **Web 自动化** | Playwright | Chromium 内核，支持录制与 Headless 执行 |
| **性能压测** | Locust | Python 编写压测脚本，支持分布式 |
| **数据库** | PostgreSQL (生产) / SQLite (开发) | 生产推荐 PostgreSQL，开发零配置 |
| **缓存/消息** | Redis | Celery Broker + Result Backend |
| **反向代理** | Nginx / OpenResty | 静态资源托管 + API 代理 + SSL |
| **容器化** | Docker Compose | 一键部署编排，开发/生产双配置 |
| **CI/CD** | GitHub Actions | CodeQL 安全扫描 + pytest + npm test + Docker 构建 |

---

## 🔧 后端架构详解

### 应用工厂模式

后端采用 Flask 标准的 **Application Factory** 模式，通过 `create_app(config_name)` 创建应用实例，便于测试与多环境配置：

```mermaid
graph TD
    Entry["app.py / wsgi.py"] --> Factory["create_app()"]
    Factory --> Config["加载配置<br/>(Development / Testing / Production)"]
    Factory --> Ext["初始化扩展<br/>(db, jwt, celery, migrate)"]
    Factory --> BP["注册蓝图<br/>api_bp → /api/v1"]
    Factory --> CORS["配置 CORS"]
    Factory --> ErrorH["注册全局错误处理"]
    Factory --> Scheduler["启动 APScheduler"]
```

### API 模块划分

所有 API 路由挂载在统一的 `api_bp` 蓝图下（前缀 `/api/v1`），按功能域划分为 12 个模块：

| 模块 | 路由前缀 | 核心功能 |
|------|---------|---------|
| `auth` | `/auth` | 注册、登录、Token 刷新、用户信息 |
| `projects` | `/projects` | 项目 CRUD、成员管理、RBAC 权限 |
| `environments` | `/environments` | 环境变量管理、变量替换引擎 |
| `api_test` | `/api-test` | 集合/用例 CRUD、Mock Server、cURL 导入导出 |
| `web_test` | `/web-test` | Web 脚本管理、Playwright 执行、录制回放 |
| `app_test` | `/app-test` | APP 脚本管理、Appium 设备连接 |
| `perf_test` | `/perf-test` | 性能场景配置、Locust 分布式压测 |
| `reports` | `/test-reports` | 测试报告聚合、历史趋势分析 |
| `docs` | `/docs` | 测试文档管理、Markdown 编辑 |
| `ai_copilot` | `/ai` | AI 对话、用例生成、错误分析、脚本生成 |
| `triggers` | `/triggers` | Webhook 触发器、定时任务调度 |
| `global_search` | `/ai/global-search` | 全局搜索（跨模块模糊查询） |

### 数据模型 ER 图

```mermaid
erDiagram
    User ||--o{ Project : "owns"
    User ||--o{ WebTestScript : "creates"
    User ||--o{ TestRun : "triggers"
    User ||--o{ ScheduledTask : "schedules"

    Project ||--o{ Environment : "has"
    Project ||--o{ ApiTestCollection : "contains"
    Project ||--o{ WebTestCollection : "contains"
    Project ||--o{ AppTestCollection : "contains"
    Project ||--o{ PerfTestScenario : "contains"

    ApiTestCollection ||--o{ ApiTestCase : "contains"
    WebTestCollection ||--o{ WebTestScript : "contains"
    AppTestCollection ||--o{ AppTestScript : "contains"

    TestRun ||--o| TestReport : "generates"
    Project ||--o{ TestRun : "tracks"
    Project ||--o{ TestReport : "aggregates"
    Project ||--o{ TestDocument : "documents"

    WebhookToken }o--|| Project : "belongs to"

    User {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role "admin | member | viewer"
    }
    Project {
        int id PK
        string name
        int owner_id FK
    }
    Environment {
        int id PK
        string name
        json variables
        int project_id FK
    }
    ApiTestCase {
        int id PK
        string name
        string method
        string url
        int collection_id FK
    }
    TestRun {
        int id PK
        string test_type "api | web | app | perf"
        string status "pending | running | success | failed"
        int total_cases
        int passed
        int failed
    }
    TestReport {
        int id PK
        string test_type
        json summary
        int test_run_id FK
    }
```

### 认证与权限机制

```mermaid
graph LR
    subgraph 认证流程
        Login["登录请求"] --> Validate["校验用户名密码"]
        Validate --> GenToken["生成双 Token"]
        GenToken --> Access["Access Token<br/>有效期 24h"]
        GenToken --> Refresh["Refresh Token<br/>有效期 30d"]
        Access --> Header["放入 Authorization Header"]
    end

    subgraph 权限控制
        Request["API 请求"] --> JWT["JWT 解析<br/>提取 user_id + role"]
        JWT --> RBAC{"角色校验"}
        RBAC -->|admin| Admin["全部权限"]
        RBAC -->|member| Member["读写权限"]
        RBAC -->|viewer| Viewer["只读权限"]
    end
```

- **Access Token**：短期有效（24 小时），用于 API 请求鉴权
- **Refresh Token**：长期有效（30 天），用于无感刷新 Access Token
- **前端自动刷新**：Axios 拦截器捕获 401 响应，自动调用 refresh 接口并重试原请求
- **RBAC 三角色**：`admin`（管理员）、`member`（成员，默认）、`viewer`（只读）

### 异步任务架构

Web 测试和性能测试通过 Celery 异步执行，避免阻塞 API 请求：

```mermaid
graph LR
    API["Flask API"] -->|send_task| Broker["Redis Broker"]
    Broker -->|consume| Worker["Celery Worker"]
    Worker -->|Playwright| WebTest["执行 Web 测试"]
    Worker -->|Locust| PerfTest["执行性能压测"]
    Worker -->|update_state| Backend["Redis Backend"]
    API -->|AsyncResult| Backend
    API -->|查询状态| Client["前端轮询"]
```

- **Web 测试**：Celery Worker 调用 `subprocess.run()` 执行 Playwright Python 脚本，支持 VNC Live View 实时预览
- **性能测试**：Celery Worker 启动 Locust 进程，实时采集 RPS、响应时间、错误率等指标
- **定时任务**：APScheduler 基于文件锁实现单例调度，支持 Cron 表达式与一次性触发

---

## 🎨 前端架构详解

### 组件层次结构

```mermaid
graph TD
    App["App.tsx<br/>路由入口"] --> Layout["MainLayout<br/>侧边栏 + 顶栏 + 内容区"]
    Layout --> Suspense["React.Suspense<br/>懒加载边界"]
    Suspense --> Pages["页面组件"]
    Pages --> Dashboard["Dashboard"]
    Pages --> APITest["API 测试工作台"]
    Pages --> WebTest["Web 自动化"]
    Pages --> AppTest["APP 测试"]
    Pages --> PerfTest["性能测试"]
    Pages --> Reports["报告中心"]
    Pages --> Settings["系统设置"]

    APITest --> Components["业务组件"]
    Components --> RequestEditor["请求编辑器"]
    Components --> EnvManager["环境管理器"]
    Components --> MockServer["Mock 面板"]

    Layout --> Global["全局组件"]
    Global --> Copilot["GlobalCopilot<br/>AI 助手浮窗"]
    Global --> Search["GlobalSearch<br/>全局搜索"]
    Global --> EnvHint["EnvironmentVariableHint<br/>变量自动补全"]
```

### 状态管理 (Zustand)

```mermaid
graph LR
    subgraph Stores
        AuthStore["authStore<br/>用户认证状态<br/>(persist → localStorage)"]
        ProjectStore["projectStore<br/>当前项目<br/>(persist → localStorage)"]
        APITestStore["apiTestStore<br/>集合/用例/Mock"]
        WebTestStore["webTestStore<br/>脚本/执行状态"]
        PerfTestStore["perfTestStore<br/>场景/实时指标"]
    end

    subgraph 中间件
        Persist["persist<br/>持久化到 localStorage"]
        Devtools["devtools<br/>Redux DevTools 调试"]
    end

    AuthStore --> Persist
    ProjectStore --> Persist
    APITestStore --> Devtools
    WebTestStore --> Devtools
    PerfTestStore --> Devtools
```

### 服务层模式

前端通过统一的 **Service 层** 封装所有 API 调用，职责分离清晰：

| 服务文件 | 对应后端模块 | 核心方法 |
|---------|-------------|---------|
| `authService.ts` | auth | login, register, refreshToken, getProfile |
| `projectService.ts` | projects | getProjects, createProject, updateProject |
| `environmentService.ts` | environments | getEnvironments, createEnvironment |
| `apiTestService.ts` | api_test | getCollections, createCase, runCase, curlImport |
| `webTestService.ts` | web_test | getScripts, createScript, runScript |
| `appTestService.ts` | app_test | getScripts, createScript, runScript |
| `perfTestService.ts` | perf_test | getScenarios, createScenario, runScenario |
| `reportService.ts` | reports | getReports, getReportDetail |
| `aiCopilotService.ts` | ai_copilot | chat, generateCases, analyzeError |
| `documentService.ts` | docs | getDocuments, createDocument |
| `triggerService.ts` | triggers | getTriggers, createTrigger |

**Axios 拦截器链**：
1. **请求拦截器**：自动注入 `Authorization: Bearer <token>` 头
2. **响应拦截器**：捕获 401 → 自动 refresh Token → 重试原请求
3. **错误拦截器**：统一处理网络错误、业务错误，弹出 antd notification 提示

### 路由与懒加载

```typescript
// React Router v6 + lazy() 按需加载
const Dashboard = lazy(() => import('./pages/Dashboard'))
const APITestWorkspace = lazy(() => import('./pages/api-test/APITestWorkspace'))
const WebTestWorkspace = lazy(() => import('./pages/web-test/WebTestWorkspace'))
// ...

<Suspense fallback={<Spin />}>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/api-test/*" element={<APITestWorkspace />} />
    {/* ... */}
  </Routes>
</Suspense>
```

非首屏页面全部使用 `lazy()` 动态导入，结合 `<Suspense>` 实现路由级代码分割，显著减小首屏加载体积。

---

## 🔒 安全架构

```mermaid
graph TD
    subgraph 认证层
        JWT["JWT 双 Token<br/>Access: 24h / Refresh: 30d"]
        Header["Authorization Header<br/>Bearer <token>"]
    end

    subgraph 权限层
        RBAC["RBAC 角色控制<br/>admin / member / viewer"]
        Decorator["@require_role 装饰器<br/>路由级权限守卫"]
    end

    subgraph 传输层
        HTTPS["HTTPS (SSL/TLS)"]
        CORS["CORS 白名单"]
    end

    subgraph 数据层
        Hash["密码哈希<br/>(bcrypt / werkzeug)"]
        EnvVars["环境变量<br/>敏感信息不入代码库"]
        Webhook["Webhook 签名<br/>HMAC-SHA256"]
    end

    Header --> JWT --> RBAC --> Decorator
    HTTPS --> CORS
    Hash --> EnvVars --> Webhook
```

| 安全机制 | 实现方式 | 作用 |
|---------|---------|------|
| **身份认证** | JWT (Flask-JWT-Extended) | 无状态认证，支持 Token 自动刷新 |
| **权限控制** | RBAC 三角色 + 装饰器 | admin/member/viewer 细粒度权限 |
| **密码存储** | werkzeug 安全哈希 | 不可逆加密，防止数据泄露 |
| **Webhook 安全** | HMAC-SHA256 签名验证 | 防止伪造触发请求 |
| **传输安全** | HTTPS + CORS 白名单 | 加密传输 + 跨域限制 |
| **敏感信息** | `.env` 文件 + `.gitignore` | API Key、密码等不进入代码仓库 |
| **安全扫描** | GitHub CodeQL | CI 自动检测 OWASP Top 10 漏洞 |
| **依赖审计** | npm audit + pip-audit | CI 自动检测已知漏洞依赖 |

---

## 📚 文档导读

- 统一入口：`document/overview.md`
- 启动指南：`document/STARTUP.md`
- API 文档：`document/API.md`
- 开发文档：`document/DEVELOPMENT.md`
- 脚本指南：`document/SCRIPT_GUIDE.md`

---

## 🚀 快速开始（本地开发部署推荐）

项目采用前后端分离架构：后端 Flask + SQLAlchemy，前端 React + TypeScript。

提供两种启动方式：**方式 A** 手动启动（推荐开发调试），**方式 B** Docker Compose 一键启动。

### 前置要求

| 组件 | 版本建议 | 说明 |
|------|---------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建/开发服务器 |
| Redis | 5.0+ | **必需** — Celery 消息队列（`app.py` 会自动开启 Celery） |

> **数据库说明**：本地开发默认使用 **SQLite**（零配置），无需安装 PostgreSQL。生产环境推荐 PostgreSQL。

### 方式 A：手动启动（推荐）

#### 1) 启动 Redis

```bash
# 确认 Redis 已启动
redis-cli ping
# 应返回 PONG，否则请先启动 Redis 服务
```

#### 2) 启动后端

```bash
cd backend
python -m venv venv

# Windows 激活虚拟环境
.\venv\Scripts\activate

# Linux/macOS 激活虚拟环境
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 可选：安装 Playwright 浏览器（启用 Web 自动化/录制时需要）
python -m playwright install chromium

# 准备配置文件（从模板复制，多数变量已有默认值）
cp .env.example .env
# 编辑 .env，至少确认以下配置：
#   DATABASE_URL=sqlite:///fullscopetest_dev.db   # SQLite 本地开发
#   SECRET_KEY=任意随机字符串
#   JWT_SECRET_KEY=另一个随机字符串

# 初始化数据库（⚠️ 会清空现有数据，仅限开发环境）
python init_db.py

# 创建管理员账号
python create_admin.py
# 默认账号：admin / admin123

# 启动后端 API 服务
python app.py
```

> 后端默认运行地址：`http://127.0.0.1:5211/api/v1`（手动开发模式）
>
> **端口说明**：
> - **手动开发**：后端运行在 `5211` 端口，Vite 代理配置已对接
> - **Docker Compose 开发**：后端运行在 `5000` 端口
> - **Docker Compose 生产**：后端运行在 `8000` 端口
>
> **注意**：`app.py` 会自动设置 `CELERY_ENABLE=true`，因此必须先确保 Redis 已启动，否则启动时会报连接错误。如果不需要异步任务功能，可在 `.env` 中设置 `CELERY_ENABLE=false`。

#### 3) 启动 Celery Worker（新终端窗口）

```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
celery -A app.extensions:celery worker --loglevel=info --pool=solo  # Windows 需加 --pool=solo
```

> Celery Worker 负责执行 Web 自动化测试和性能压测等异步任务。如果只使用 API 测试功能，可以不启动。

#### 4) 启动前端（开发模式）

```bash
cd web
npm install
npm run dev
```

> 前端开发服务器默认运行在：`http://localhost:3000`（已配置代理，将 `/api/*` 转发到 `http://localhost:5211`）

启动完成后访问 `http://localhost:3000`，使用 `admin / admin123` 登录即可。

### 方式 B：Docker Compose 一键启动

```bash
# 开发环境（含 PostgreSQL + Redis + Backend + Celery）
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

> Docker Compose 启动的后端运行在 `http://localhost:5000`（与手动启动的 5211 端口不同）。
> 前端仍需手动启动：`cd web && npm install && npm run dev`，或构建后由 Nginx 托管。
>
> **端口汇总**：
>
> | 部署方式 | 后端端口 | 说明 |
> |---------|---------|------|
> | 手动开发 | `5211` | `python app.py`，Vite 代理已对接 |
> | Docker 开发 | `5000` | `docker-compose up -d` |
> | Docker 生产 | `8000` | `docker-compose -f docker-compose.prod.yml up -d` |

---

## 🛠 构建与部署（生产/预发布环境）

### 前端构建

```bash
cd web
npm install
npm run build
```

前端构建产物位于 `web/dist`，可由 Nginx/OpenResty 托管，并反向代理后端到 `http://127.0.0.1:8000`。配置示例可参考 `nginx/` 目录。

### 生产环境部署

#### Docker Compose 部署（推荐）

```bash
# 生产环境启动（PostgreSQL + Redis + Backend + Celery）
docker-compose -f docker-compose.prod.yml up -d
```

#### 手动部署

```bash
# 1. 构建前端
cd web && npm install && npm run build

# 2. 部署后端（使用 Gunicorn 替代 Flask 开发服务器）
cd ../backend
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"

# 3. 启动 Celery Worker
celery -A app.extensions:celery worker --loglevel=info

# 4. 配置 Nginx 反向代理（参考 nginx/ 目录配置）
```

#### 一键部署脚本

```bash
# 部署到远程服务器（需提前配置 SSH 免密登录）
bash deploy.sh
```

### 关键配置项 (`backend/.env`)

完整配置项可参考 `backend/.env.example`，以下是生产环境必须关注的配置：

```bash
# ================= 数据库配置 =================
# PostgreSQL (生产推荐)
DATABASE_URL=postgresql://user:password@localhost:5432/fullscopetest
# SQLite (仅限本地开发)
# DATABASE_URL=sqlite:///fullscopetest_dev.db

# ================= 异步任务配置 =================
REDIS_URL=redis://localhost:6379/0
CELERY_ENABLE=true

# ================= 安全配置 (生产务必修改!) =================
SECRET_KEY=<随机长字符串>
JWT_SECRET_KEY=<另一个随机长字符串>

# ================= AI 助手配置 (可选) =================
# 也可由前端界面按请求动态覆盖
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=your_api_key_here
```

> **注意：**
> - 生产环境务必修改 `SECRET_KEY` 和 `JWT_SECRET_KEY`，切勿使用默认值。
> - Web 录制功能通过启动本机 `playwright codegen` 实现，远程服务器环境通常无法使用本地录制器。
> - Windows 环境下 Celery 需加 `--pool=solo` 参数（不支持 prefork）。

---

## 🏗 项目结构

```text
FullScopeTest/
├── backend/                    # Flask 后端核心服务
│   ├── app/
│   │   ├── api/                # API 路由层 (12 个功能模块)
│   │   ├── models/             # SQLAlchemy 数据模型 (15 个模型)
│   │   ├── tasks/              # Celery 异步任务
│   │   ├── utils/              # 工具类 (响应格式化、校验器、安全)
│   │   ├── __init__.py         # 应用工厂 create_app()
│   │   ├── config.py           # 多环境配置 (Dev / Test / Prod)
│   │   └── extensions.py       # 扩展初始化 (db, jwt, celery, migrate)
│   ├── migrations/             # Alembic 数据库迁移脚本
│   ├── tests/                  # Pytest 自动化测试 (112+ 用例)
│   ├── app.py                  # 后端启动入口
│   ├── init_db.py              # 数据库初始化 (含 admin 账号)
│   └── requirements.txt        # Python 依赖
├── web/                        # React + TypeScript 前端
│   ├── src/
│   │   ├── pages/              # 页面组件 (按模块组织)
│   │   ├── components/         # 共享组件 (GlobalCopilot, GlobalSearch 等)
│   │   ├── services/           # API 服务层 (11 个 Service)
│   │   ├── stores/             # Zustand 状态管理 (5 个 Store)
│   │   ├── hooks/              # 自定义 Hooks
│   │   ├── layouts/            # 布局组件 (MainLayout)
│   │   └── test/               # Vitest 测试配置与用例
│   ├── vite.config.ts          # Vite 构建配置 + API 代理
│   └── tsconfig.json           # TypeScript 严格模式配置
├── document/                   # 项目文档 (STARTUP / API / DEVELOPMENT 等)
├── nginx/                      # Nginx 部署配置示例
├── docker/                     # Dockerfile + 容器编排
├── scripts/                    # 辅助运维/构建脚本
├── docker-compose.yml          # 开发环境 Docker Compose
├── docker-compose.prod.yml     # 生产环境 Docker Compose
└── deploy.sh                   # 一键部署脚本
```

---

## ❓ 常见问题 (FAQ)

<details>
<summary><strong>启动后端时报 Redis 连接失败？</strong></summary>

`app.py` 会自动设置 `CELERY_ENABLE=true`，启动时会尝试连接 Redis。如果不需要异步任务功能，在 `backend/.env` 中添加：

```bash
CELERY_ENABLE=false
```

如果需要 Celery 功能，请先确保 Redis 已启动：

```bash
redis-cli ping  # 应返回 PONG
```

Windows 用户可从 [Redis for Windows](https://github.com/tporadowski/redis/releases) 下载，或使用 WSL/Docker 运行。
</details>

<details>
<summary><strong>SQLite 初始化后表不存在 / 数据库报错？</strong></summary>

确认已执行初始化脚本：

```bash
cd backend
python init_db.py
```

> **注意**：`init_db.py` 会**清空并重建**所有表，仅限开发环境使用。生产环境请使用迁移脚本：`python manage.py db upgrade`。
</details>

<details>
<summary><strong>前端启动后页面空白 / API 请求 404？</strong></summary>

1. 确认后端已启动并运行在 `http://127.0.0.1:5211`（手动模式）或 `http://localhost:5000`（Docker 开发）
2. 确认前端开发服务器运行在 `http://localhost:3000`（Vite 会自动代理 `/api` 到后端）
3. 如果使用 Docker Compose，后端端口是 **5000** 而非 5211，需修改 `web/vite.config.ts` 中的代理目标
4. 如果使用 Docker Compose 生产模式，后端端口是 **8000**，需配置 Nginx 反向代理
5. 尝试清除浏览器缓存后硬刷新（`Ctrl + Shift + R`）
</details>

<details>
<summary><strong>Web 自动化录制器启动失败？</strong></summary>

Web 录制依赖于 Playwright 本机环境，请确认已执行：

```bash
pip install playwright
python -m playwright install chromium
```

> **注意**：录制功能（`playwright codegen`）需要图形界面环境，远程服务器/无头环境无法使用。可改为在本地编写脚本后上传到平台执行。
</details>

<details>
<summary><strong>Celery Worker 启动后任务不执行？</strong></summary>

1. 确认 Redis 已启动且可连接
2. Windows 用户必须加 `--pool=solo` 参数：
   ```bash
   celery -A app.extensions:celery worker --loglevel=info --pool=solo
   ```
3. 确认 Worker 终端无报错信息，检查是否成功连接到 Redis Broker
</details>

<details>
<summary><strong>Windows 下 Celery 报 NotImplementedError？</strong></summary>

Celery 4+ 在 Windows 上不支持 `prefork` 进程池，必须使用 `solo` 模式：

```bash
celery -A app.extensions:celery worker --loglevel=info --pool=solo
```

或者考虑在 WSL2 / Docker 中运行 Celery Worker。
</details>

<details>
<summary><strong>AI 助手功能不工作？</strong></summary>

AI 助手需要配置大语言模型 API。在 `backend/.env` 中配置：

```bash
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1  # 或其他兼容 OpenAI 的 API 地址
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=your_api_key_here
```

也可以在前端界面的 AI Copilot 面板中动态配置，无需重启后端。
</details>

<details>
<summary><strong>运行后端测试用例失败？</strong></summary>

后端测试使用 SQLite 内存数据库，无需额外配置。运行方式：

```bash
cd backend
pip install -r requirements-test.txt
pytest -q tests
```

如果遇到 `ModuleNotFoundError`，确认已安装所有依赖：`pip install -r requirements.txt`。
</details>

<details>
<summary><strong>前端构建报 TypeScript 类型错误？</strong></summary>

项目启用了严格模式 TypeScript 检查。常见修复：

```bash
# 查看所有类型错误
cd web && npx tsc --noEmit

# 常见原因：
# 1. 未使用的变量/参数 — 删除或加 _ 前缀
# 2. 类型断言缺失 — 添加适当的类型注解
# 3. API 返回值类型不匹配 — 检查 services/ 中的类型定义
```
</details>

<details>
<summary><strong>如何切换到 PostgreSQL 数据库？</strong></summary>

1. 安装 PostgreSQL 并创建数据库：
   ```bash
   createdb fullscopetest_dev
   ```

2. 修改 `backend/.env`：
   ```bash
   DATABASE_URL=postgresql://用户名:密码@localhost:5432/fullscopetest_dev
   ```

3. 重新初始化数据库：
   ```bash
   python init_db.py
   ```
</details>

---

## 🚀 GitHub Actions 集成

FullScopeTest 提供官方 GitHub Action，可在 CI/CD 流程中自动运行测试。

### 快速开始

在你的项目中创建 `.github/workflows/test.yml`：

```yaml
name: FullScopeTest CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: FullScopeTest/fullscope-test/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FULLSCOPETEST_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_TOKEN }}
          test-type: api
          environment: staging
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `server-url` | ✅ | - | FullScopeTest 服务器地址 |
| `api-token` | ✅ | - | API Token（在 Settings → Tokens 创建） |
| `test-suite-id` | ❌ | - | 指定测试套件 ID |
| `quality-gate-id` | ❌ | - | Quality Gate ID，用于评估质量门禁 |
| `environment` | ❌ | `staging` | 测试环境名称 |
| `test-type` | ❌ | `api` | 测试类型：`api`、`web` 或 `all` |

### 输出变量

| 变量 | 说明 |
|------|------|
| `test_run_id` | 创建的测试运行 ID |
| `test_status` | 最终状态：`success` / `failed` / `timeout` |
| `quality_gate_passed` | Quality Gate 是否通过 |

### 高级用法

**带 Quality Gate 的 CI 流程：**

```yaml
name: FullScopeTest CI with Quality Gate
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: FullScopeTest/fullscope-test/.github/actions/fullscope-test@main
        id: test
        with:
          server-url: ${{ secrets.FULLSCOPETEST_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_TOKEN }}
          test-suite-id: ${{ secrets.TEST_SUITE_ID }}
          quality-gate-id: ${{ secrets.QUALITY_GATE_ID }}
          environment: production
          test-type: all
      - name: Report status
        if: always()
        run: |
          echo "Test Status: ${{ steps.test.outputs.test_status }}"
          echo "Quality Gate: ${{ steps.test.outputs.quality_gate_passed }}"
```

---

## 🤝 参与贡献

我们非常欢迎您的参与！
- 发现 Bug 或有好的建议，欢迎提交 Issue。
- 想要贡献代码，请提交 Pull Request。
- 提交代码前建议进行本地自检：
  - 前端：`cd web && npm run lint`
  - 后端：`cd backend && pytest -q`

---

## 📞 联系作者

如果您在部署、使用过程中遇到问题，或者有商业合作、功能定制等需求，欢迎通过以下方式与我取得联系：

- **个人博客**：[huangxuan.chat](http://huangxuan.chat)
- **邮箱**：3441578327@qq.com or huangxuandev@126.com
- **电话**：(+86)188-5212-2635
- **微信**：
  
  <div align="left">
    <img src="https://res.huangxuan.chat/thrivex/album/69c008b2e4b01ee6a7b76b39.png" alt="微信二维码" width="150px" />
    <p><em>扫码添加作者微信</em></p>
  </div>

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 协议开源。

<div align="center">
  <sub>Built with ❤️ by FullScopeTest Team</sub>
</div>
