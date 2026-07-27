<p align="center"><img src="images/fullscopetest_logo.png" alt="FullScopeTest" width="400" /></p>
<h2 align="center" style="font-weight: 600; font-size: 1.5rem;">AI-Native 全链路自动化测试平台</h2>
<p align="center">
  <strong>AI 编排 · API 测试 · Web 自动化 · APP 测试 · 性能压测 · 智能报告</strong>
</p>
<p align="center">
  <a href="README.md">中文</a> | <a href="README_EN.md">English</a>
</p>
<p align="center">
  <a href="https://github.com/05Huang/FullScopeTest/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.typescriptlang.org/"><img src="https://img.shields.io/badge/typescript-5.x-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript"></a>
  <a href="https://reactjs.org/"><img src="https://img.shields.io/badge/react-18-61DAFB?style=flat&logo=react&logoColor=black" alt="React"></a>
  <a href="https://vitejs.dev/"><img src="https://img.shields.io/badge/vite-5-646CFF?style=flat&logo=vite&logoColor=white" alt="Vite"></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/flask-3.0-000000?style=flat&logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://www.sqlalchemy.org/"><img src="https://img.shields.io/badge/sqlalchemy-ORM-D71F00?style=flat&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"></a>
  <a href="https://ant.design/"><img src="https://img.shields.io/badge/ant--design-5-0170FE?style=flat&logo=antdesign&logoColor=white" alt="Ant Design"></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/playwright-e2e-2EAD33?style=flat&logo=playwright" alt="Playwright"></a>
  <a href="https://docs.celeryq.dev/"><img src="https://img.shields.io/badge/celery-task--queue-37814A?style=flat&logo=celery&logoColor=white" alt="Celery"></a>
  <a href="https://redis.io/"><img src="https://img.shields.io/badge/redis-broker-DC382D?style=flat&logo=redis&logoColor=white" alt="Redis"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/postgresql-15-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/docker-compose-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://vitest.dev/"><img src="https://img.shields.io/badge/vitest-testing-6E9F18?style=flat&logo=vitest" alt="Vitest"></a>
</p>
<p align="center" style="font-size: 1.4rem; font-weight: 700; color: #ff4500; margin: 16px 0;">
  <strong>🔥 在线演示环境: <a href="http://test.huangxuan.chat" style="text-decoration: none; color: #ff4500;">test.huangxuan.chat</a> 🔥</strong>
</p>
<hr />

## 📖 项目简介

**FullScopeTest** 是一个 AI 驱动的全链路自动化测试平台，覆盖 API 接口测试、Web UI 自动化、APP 移动端测试和性能压测四大领域。平台以 **AI-Native** 为核心设计理念，提供自然语言编排、脚本自动生成、智能错误分析与自愈等能力，降低测试编写与维护门槛。

### 核心能力

- **AI 赋能**：内置 AI Copilot，支持自然语言编排、脚本自动生成、智能错误分析与自愈、Prompt 版本管理与 A/B 测试、语义去重
- **接口测试**：完整的 HTTP/REST API 测试工作台，支持环境变量、前置/后置脚本、断言、cURL 导入导出、Mock Server
- **Web 自动化**：基于 Playwright，支持在线编写、视觉回归测试、VNC Live View 实时预览（录制功能需本地 GUI 环境，远程服务器请使用 `playwright codegen` 本地录制后上传脚本）
- **性能压测**：基于 Locust，支持分布式压测、实时监控大盘、历史对比、告警引擎
- **APP 测试**：Appium 脚本管理（支持 Android / iOS 脚本编写与存储，需配合外部 Appium Server 或设备农场执行）
- **测试报告**：聚合四类测试结果，提供可视化指标与多格式导出

### 企业级特性

- **多租户隔离**：组织级数据隔离，项目/用例/脚本/报告按组织过滤
- **用户管理**：管理员后台，支持角色切换、启用/禁用、密码重置
- **RBAC 权限**：admin / member / viewer 三级角色控制
- **组织邀请码**：通过邀请码直接加入团队，无需手动分配
- **审计日志**：全操作审计追踪，支持按用户/模块/时间筛选
- **国际化**：中英文双语支持，演示系统根据 IP 智能提示切换语言
- **暗色模式**：完整的深色主题适配，支持系统偏好自动切换
- **无障碍访问**：WCAG 2.1 AA 级别，键盘导航、屏幕阅读器支持、跳过导航链接

---

## 🖥 UI 展示

<table style="border-collapse: collapse; border: 1px solid black;">
  <tr>
    <td colspan="2" style="padding: 5px;background-color:#fff;text-align:center;">
      <img src="images/ui演示/ui-01.webp" alt="登录页" />
    </td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-02.webp" alt="工作台" /></td>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-03.webp" alt="用例集管理" /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-04.webp" alt="环境管理" /></td>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-05.webp" alt="Web自动化" /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-06.webp" alt="APP测试" /></td>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-07.webp" alt="性能测试" /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-08.webp" alt="测试报告" /></td>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-09.webp" alt="AI统计看板" /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-10.webp" alt="CI/CD" /></td>
    <td style="padding: 5px;background-color:#fff;"><img src="images/ui演示/ui-11.webp" alt="测试文档" /></td>
  </tr>
</table>


---

## 🏆 为什么选择 FullScopeTest？— 与 MeterSphere V3 对比

FullScopeTest 专为需要**全方位测试覆盖**的团队打造。我们不仅实现了传统测试平台的所有核心功能，更在以下关键维度**超越 MeterSphere V3**：

| 维度 | MeterSphere V3 | FullScopeTest | 说明 |
|------|---------------|---------------|------|
| **UI 自动化** | ❌ 已移除 | ✅ Playwright + 视觉回归 | MeterSphere V3 主动放弃了 UI 自动化，我们做得更深更好 |
| **性能测试** | ⚠️ 基础支持 | ✅ Locust + 实时大盘 + 告警 | 时间序列数据、分位数统计、历史对比、告警引擎 |
| **AI 能力** | ⚠️ 简单 Prompt 包装 | ✅ 可观测/可版本化/语义分析 | AI 调用日志、Prompt A/B 测试、智能去重、自愈修复 |
| **CI/CD 集成** | ⚠️ 基础 Webhook | ✅ GitHub Action + Quality Gate + 变更感知 | PR 自动触发、质量门禁、Check Run 回写 |
| **多租户** | ✅ 支持 | ✅ 支持 + 审计日志 | 组织级数据隔离、操作审计 |
| **部署方式** | Docker Compose | Docker Compose + K8s | 同时支持两种部署方式 |
| **后端性能** | Java (Spring Boot) | Flask 3.0 + FastAPI v2（渐进迁移中） | Python 生态 + 异步高性能 |
| **视觉回归** | ❌ 不支持 | ✅ 自动截图 + 像素级对比 | 独家功能，自动检测 UI 视觉变化 |
| **AI 用例生成** | ❌ 不支持 | ✅ Swagger → 语义分析 → 自动生成 | 智能理解接口业务含义 |
| **语义去重** | ❌ 不支持 | ✅ 向量化 + 余弦相似度 | 自动发现重复测试用例 |

### 核心差异化优势

#### 1. UI 自动化 — MeterSphere V3 主动放弃的领域

MeterSphere V3 在 2024 年正式移除了 Web 自动化测试模块（原基于 Selenium），转而推荐使用外部工具。FullScopeTest 选择 **Playwright** 作为自动化引擎，带来：

- **更快的执行速度**：Playwright 基于 Chromium 内核，比 Selenium 快 2-3 倍
- **更强的稳定性**：自动等待机制、网络拦截、多标签页支持
- **视觉回归测试**：每步自动截图 → 智能对比 → 差异高亮 → 一键批准
- **实时预览**：通过 VNC Live View 实时观察测试执行过程

#### 2. AI 能力真正工程化 — 不是 Prompt 包装

| 特性 | 常见 AI 测试工具 | FullScopeTest |
|------|-----------------|---------------|
| AI 调用监控 | ❌ 黑盒 | ✅ 每次调用记录 prompt/response/latency/tokens/cost |
| Prompt 管理 | ❌ 硬编码 | ✅ 数据库版本化 + A/B 测试 |
| 失败处理 | ❌ 直接报错 | ✅ 降级策略 + fallback 结果 |
| 语义分析 | ❌ 关键词匹配 | ✅ sentence-transformers 向量化 |

#### 3. CI/CD 集成 — 开发者优先

```yaml
# 一行集成到 GitHub Actions
- uses: FullScopeTest/fullscope-test/.github/actions/fullscope-test@main
  with:
    server-url: ${{ secrets.FULLSCOPETEST_URL }}
    api-token: ${{ secrets.FULLSCOPETEST_TOKEN }}
    test-suite-id: ${{ secrets.TEST_SUITE_ID }}
    quality-gate-id: ${{ secrets.QUALITY_GATE_ID }}
```

- **变更感知触发**：`/api/**` 路径变更时只运行接口测试，节省 CI 资源
- **Quality Gate**：可配置通过率阈值、P95 响应时间上限、视觉差异上限
- **Check Run 回写**：实时更新测试状态到 PR，失败用例一目了然

---

## 🏛 系统架构概览

### 整体架构

```mermaid
graph LR
    subgraph 客户端
        Browser["浏览器"]
    end

    subgraph Nginx_OpenResty
        Static["静态资源<br/>(React SPA)"]
        Proxy["反向代理<br/>/api → :5000(Dev)<br/>/api → :8000(Prod)"]
        WS["WebSocket<br/>(Live View)"]
    end

    subgraph Flask_Backend
        API["API 蓝图层<br/>25 个模块"]
        Auth["JWT 认证<br/>+ RBAC 权限"]
        ORM["SQLAlchemy ORM<br/>31 个数据模型"]
    end

    subgraph Async_Workers
        Celery["Celery Worker<br/>(Web / Perf 测试)"]
        Scheduler["APScheduler<br/>(定时任务)"]
    end

    subgraph AI_Layer
        Copilot["AI Copilot"]
        Agent["AI Agent<br/>(编排 / 脚本生成)"]
    end

    subgraph Data_Stores
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
| **Web 自动化** | Playwright | Chromium 内核，在线编写 + 视觉回归 + VNC 预览（录制需 GUI 环境） |
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

所有 API 路由挂载在统一的 `api_bp` 蓝图下（前缀 `/api/v1`），按功能域划分为 30+ 个模块：

| 模块 | 路由前缀 | 核心功能 |
|------|---------|---------|
| `auth` | `/auth` | 注册（支持邀请码）、登录、Token 刷新、SSO、用户信息 |
| `admin` | `/admin` | 用户管理：列表/角色切换/启用禁用/密码重置（仅管理员） |
| `organizations` | `/organizations` | 组织 CRUD、邀请码管理、成员管理 |
| `projects` | `/projects` | 项目 CRUD、成员管理、RBAC 权限 |
| `environments` | `/environments` | 环境变量管理、变量替换引擎 |
| `api_test` | `/api-test` | 集合/用例 CRUD、Mock Server、cURL 导入导出 |
| `web_test` | `/web-test` | Web 脚本管理、Playwright 执行、录制回放 |
| `app_test` | `/app-test` | APP 脚本管理、Appium 设备连接 |
| `perf_test` | `/perf-test` | 性能场景配置、Locust 分布式压测 |
| `reports` | `/test-reports` | 测试报告聚合、历史趋势分析 |
| `docs` | `/docs` | 测试文档管理、Markdown 编辑 |
| `ai_copilot` | `/ai` | AI 对话、用例生成、错误分析、脚本生成 |
| `ai_stats` | `/ai/stats` | AI 调用统计、Token 消耗、成本分析 |
| `prompt_versions` | `/ai/prompts` | Prompt 版本管理、A/B 测试、流量分配 |
| `triggers` | `/triggers` | Webhook 触发器、定时任务调度 |
| `global_search` | `/ai/global-search` | 全局搜索（跨模块模糊查询） |
| `quality_gates` | `/quality-gates` | 质量门禁配置、通过率/P95/视觉差异阈值 |
| `test_plans` | `/test-plans` | 测试计划管理、执行跟踪 |
| `audit_logs` | `/audit-logs` | 操作审计日志、按用户/模块/时间筛选 |
| `notifications` | `/notifications` | 通知配置、Webhook/邮件通知 |
| `tokens` | `/tokens` | API Token 管理、权限范围控制 |
| `geo` | `/geo` | 地理位置检测（演示系统语言切换） |
| `github_integration` | `/github` | GitHub OAuth、PR 自动触发、Check Run 回写 |
| `github_checks` | `/github/checks` | GitHub Checks API 集成 |

### 数据模型 ER 图

```mermaid
erDiagram
    Organization ||--o{ OrganizationMember : "has members"
    Organization ||--o{ Project : "owns"
    User ||--o{ OrganizationMember : "belongs to"
    User ||--o{ Project : "owns"
    User ||--o{ WebTestScript : "creates"
    User ||--o{ TestRun : "triggers"
    User ||--o{ ScheduledTask : "schedules"
    User ||--o{ AuditLog : "generates"

    Project ||--o{ Environment : "has"
    Project ||--o{ ApiTestCollection : "contains"
    Project ||--o{ WebTestCollection : "contains"
    Project ||--o{ AppTestCollection : "contains"
    Project ||--o{ PerfTestScenario : "contains"
    Project ||--o{ QualityGate : "enforces"
    Project ||--o{ TestPlan : "plans"

    ApiTestCollection ||--o{ ApiTestCase : "contains"
    WebTestCollection ||--o{ WebTestScript : "contains"
    AppTestCollection ||--o{ AppTestScript : "contains"

    TestRun ||--o| TestReport : "generates"
    Project ||--o{ TestRun : "tracks"
    Project ||--o{ TestReport : "aggregates"
    Project ||--o{ TestDocument : "documents"

    WebhookToken }o--|| Project : "belongs to"

    Organization {
        int id PK
        string name
        string invite_code UK
        boolean is_active
    }
    User {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role "admin | member | viewer"
        boolean is_active
    }
    OrganizationMember {
        int id PK
        int organization_id FK
        int user_id FK
        string role "owner | admin | member | viewer"
        boolean is_active
    }
    Project {
        int id PK
        string name
        int owner_id FK
        int organization_id FK
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
    AuditLog {
        int id PK
        int user_id FK
        string action
        string module
        json details
        datetime created_at
    }
    QualityGate {
        int id PK
        string name
        float min_pass_rate
        int max_p95_ms
        int project_id FK
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
    App["App.tsx<br/>路由入口 + 语言检测"] --> Layout["MainLayout<br/>侧边栏 + 顶栏 + 内容区"]
    Layout --> Suspense["React.Suspense<br/>懒加载边界"]
    Suspense --> Pages["页面组件"]
    Pages --> Dashboard["Dashboard"]
    Pages --> APITest["API 测试工作台"]
    Pages --> WebTest["Web 自动化"]
    Pages --> AppTest["APP 测试"]
    Pages --> PerfTest["性能测试"]
    Pages --> Reports["报告中心"]
    Pages --> Settings["系统设置<br/>5 个 Tab"]
    Pages --> Admin["用户管理<br/>(管理员)"]
    Pages --> Orgs["组织管理"]
    Pages --> AuditLogs["审计日志"]
    Pages --> TestPlans["测试计划"]
    Pages --> QualityGates["质量门禁"]
    Pages --> CICD["CI/CD 集成"]
    Pages --> Integ["第三方集成<br/>GitHub OAuth"]
    Pages --> Tokens["API Token 管理"]

    APITest --> Components["业务组件"]
    Components --> RequestEditor["请求编辑器"]
    Components --> EnvManager["环境管理器"]
    Components --> MockServer["Mock 面板"]

    Layout --> Global["全局组件"]
    Global --> Copilot["GlobalCopilot<br/>AI 助手浮窗"]
    Global --> Search["GlobalSearch<br/>全局搜索"]
    Global --> GeoPrompt["LanguageSwitchPrompt<br/>智能语言切换提示"]
    Global --> TourGuide["TourGuide<br/>新手引导"]
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
| `authService.ts` | auth | login, register, refreshToken, getProfile, ssoLogin |
| `adminService.ts` | admin | getUsers, updateUserRole, toggleUserStatus, resetPassword |
| `organizationService.ts` | organizations | getOrganizations, createOrganization, regenerateInviteCode |
| `projectService.ts` | projects | getProjects, createProject, updateProject |
| `environmentService.ts` | environments | getEnvironments, createEnvironment |
| `apiTestService.ts` | api_test | getCollections, createCase, runCase, curlImport |
| `webTestService.ts` | web_test | getScripts, createScript, runScript |
| `appTestService.ts` | app_test | getScripts, createScript, runScript |
| `perfTestService.ts` | perf_test | getScenarios, createScenario, runScenario |
| `reportService.ts` | reports | getReports, getReportDetail |
| `qualityGateService.ts` | quality_gates | getGates, createGate, evaluateGate |
| `testPlanService.ts` | test_plans | getPlans, createPlan, executePlan |
| `auditLogService.ts` | audit_logs | getLogs, filterByUser, filterByModule |
| `notificationService.ts` | notifications | getSettings, updateSettings |
| `tokenService.ts` | tokens | getTokens, createToken, revokeToken |
| `aiCopilotService.ts` | ai_copilot | chat, generateCases, analyzeError |
| `aiStatsService.ts` | ai_stats | getStats, getCostAnalysis |
| `documentService.ts` | docs | getDocuments, createDocument |
| `triggerService.ts` | triggers | getTriggers, createTrigger |
| `geoService.ts` | geo | detectRegion |
| `integrationService.ts` | github_integration | connectGitHub, getPRStatus |

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
| **API Token** | 独立 Token 管理 | 支持细粒度权限范围、可随时吊销 |
| **审计日志** | 全操作记录 | 登录/CRUD/配置变更全部可追溯 |
| **租户隔离** | organization_id 过滤 | 数据库级别组织隔离，防止跨租户访问 |
| **SSO 集成** | OIDC 协议 | 支持企业单点登录（Beta — 需配置 OIDC Provider 环境变量） |

---

## 📚 文档导读

### 完整文档（docs/ 目录）

| 文档 | 说明 |
|------|------|
| [部署文档](docs/deployment.md) | Docker Compose 部署（开发/生产）、环境变量说明、Troubleshooting |
| [Kubernetes 部署指南](docs/kubernetes-deployment.md) | Helm Chart 部署、TLS 配置、生产环境建议 |
| [API 参考文档](docs/api-reference.md) | 所有 v1 + v2 接口请求/响应示例、认证说明、错误码一览 |
| [GitHub Actions 集成指南](docs/github-actions-integration.md) | 从零到一集成步骤、PR 自动触发、定时回归、手动触发 |
| [GitLab CI 模板](docs/gitlab-ci-template.yml) | GitLab CI/CD YAML 模板示例 |
| [性能基准测试](docs/performance-benchmark.md) | Flask v1 vs FastAPI v2 压测对比、P95 响应时间分析 |
| [功能路线图](docs/ROADMAP.md) | 按季度规划的功能开发计划 |
| [功能完整性审计](docs/feature-audit.md) | 14 项功能实现状态审计报告 |
| [v1.0.0-rc1 发布说明](releases/v1.0.0-rc1.md) | 首个正式发布候选版本完整 Release Notes |

### 快速文档入口

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

### 初始管理员配置

生产环境通过环境变量配置初始管理员（首次启动自动创建）：

```bash
# backend/.env
INIT_ADMIN_USERNAME=admin
INIT_ADMIN_EMAIL=admin@example.com
INIT_ADMIN_PASSWORD=your_secure_password
```

> 不设置这些变量则不自动创建管理员，需通过 `python create_admin.py` 手动创建。

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

# ================= 初始管理员 (首次启动自动创建) =================
INIT_ADMIN_USERNAME=admin
INIT_ADMIN_EMAIL=admin@example.com
INIT_ADMIN_PASSWORD=<安全密码>

# ================= AI 助手配置 (可选) =================
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=your_api_key_here

# ================= 文件存储 (可选) =================
OSS_ENDPOINT=https://your-oss-endpoint
OSS_ACCESS_KEY_ID=your_key
OSS_ACCESS_KEY_SECRET=your_secret
OSS_BUCKET_NAME=your_bucket
OSS_DOMAIN=https://your-domain.com
```

### 生产环境部署（Docker Compose）

```bash
# 1. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 填入生产配置

# 2. 启动所有服务
docker compose -f docker-compose.prod.yml up -d

# 3. 查看日志
docker compose -f docker-compose.prod.yml logs -f backend

# 4. 构建前端并部署到 Nginx
cd web && npm install && npm run build
cp -r dist/* /var/www/test.huangxuan.chat/index/
```

生产环境包含的服务：

| 服务 | 端口 | 说明 |
|------|------|------|
| backend | 8000 | Flask API + Gunicorn (4 workers) |
| celery | - | 异步任务 Worker |
| redis | 6379 | 消息队列 + 缓存 |
| prometheus | 9090 | 指标采集 |
| grafana | 3001 | 监控可视化 |
| alertmanager | 9093 | 告警管理 |

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
│   │   ├── api/                # API 路由层 (30+ 个功能模块)
│   │   │   ├── auth.py         # 认证：注册/登录/SSO/邀请码
│   │   │   ├── admin.py        # 管理员：用户管理/角色/密码重置
│   │   │   ├── geo.py          # 地理位置检测（语言切换）
│   │   │   ├── organizations.py # 组织管理/邀请码
│   │   │   ├── audit_logs.py   # 审计日志
│   │   │   └── ...
│   │   ├── models/             # SQLAlchemy 数据模型 (35+ 个模型)
│   │   │   ├── organization.py # 组织模型（含邀请码）
│   │   │   ├── user.py         # 用户模型（含角色/组织关联）
│   │   │   ├── audit_log.py    # 审计日志模型
│   │   │   └── ...
│   │   ├── middleware/          # 中间件层
│   │   │   ├── tenant.py       # 租户隔离中间件
│   │   │   ├── permission.py   # RBAC 权限注入
│   │   │   ├── rate_limit.py   # 限流中间件
│   │   │   ├── security_headers.py # 安全响应头
│   │   │   └── ...
│   │   ├── utils/
│   │   │   └── org_filter.py   # 组织级数据过滤工具
│   │   ├── plugins/            # 插件系统
│   │   ├── tasks/              # Celery 异步任务
│   │   ├── services/           # 业务服务层 (AI/权限/配额等)
│   │   ├── __init__.py         # 应用工厂 create_app()
│   │   ├── config.py           # 多环境配置 (Dev / Test / Prod)
│   │   └── extensions.py       # 扩展初始化 (db, jwt, celery, migrate)
│   ├── migrations/             # Alembic 数据库迁移脚本
│   ├── scripts/                # 数据脚本 (seed_data.py)
│   ├── tests/                  # Pytest 自动化测试 (470+ 用例)
│   ├── app.py                  # 后端启动入口
│   ├── init_db.py              # 数据库初始化
│   └── requirements.txt        # Python 依赖
├── web/                        # React + TypeScript 前端
│   ├── src/
│   │   ├── pages/              # 页面组件 (按模块组织)
│   │   │   ├── admin/          # 管理员页面 (UserManagement)
│   │   │   ├── organizations/  # 组织管理页面
│   │   │   ├── api-test/       # API 测试工作台
│   │   │   ├── web-test/       # Web 自动化
│   │   │   ├── app-test/       # APP 测试
│   │   │   ├── perf-test/      # 性能测试
│   │   │   └── ...
│   │   ├── components/         # 共享组件
│   │   │   ├── GlobalCopilot.tsx    # AI 助手浮窗
│   │   │   ├── LanguageSwitchPrompt.tsx # 智能语言切换
│   │   │   └── ...
│   │   ├── services/           # API 服务层 (25+ 个 Service)
│   │   ├── hooks/              # 自定义 Hooks
│   │   │   ├── useRole.ts      # 角色权限 Hook
│   │   │   └── useGeoLanguage.ts # 地理语言检测 Hook
│   │   ├── stores/             # Zustand 状态管理
│   │   ├── i18n/               # 国际化 (中英文)
│   │   ├── styles/             # 样式系统
│   │   │   ├── index.css       # 主样式 (iOS 设计系统)
│   │   │   ├── dark-theme.css  # 暗色主题
│   │   │   └── responsive.css  # 响应式适配
│   │   └── layouts/            # 布局组件 (MainLayout)
│   ├── .env.production         # 生产环境变量
│   ├── vite.config.ts          # Vite 构建配置 + API 代理
│   └── tsconfig.json           # TypeScript 严格模式配置
├── infra/                      # 基础设施配置
│   └── monitoring/             # Prometheus + Grafana 监控
├── document/                   # 项目文档
├── docker/                     # Dockerfile
├── docker-compose.yml          # 开发环境 Docker Compose
├── docker-compose.prod.yml     # 生产环境 Docker Compose
└── deploy.sh                   # 一键部署脚本
```

---

## 🌟 新增功能详解

### 多租户与组织管理

- **组织（Organization）**：顶层租户单元，所有数据按组织隔离
- **邀请码**：每个组织有唯一邀请码，注册时输入即可直接加入团队
- **个人空间**：注册时不填邀请码自动创建个人空间组织
- **数据隔离**：项目、用例、脚本、报告等所有资源按 `organization_id` 过滤

### 用户管理（管理员后台）

管理员可以：
- 查看所有用户列表（支持搜索）
- 切换用户角色（admin / member / viewer）
- 启用/禁用用户账号
- 重置用户密码

### 国际化与智能语言切换

- **中英文双语**：完整的 i18n 支持，覆盖所有页面和组件
- **智能检测**：演示系统根据用户 IP 地理位置自动提示切换英文
- **用户偏好**：语言选择保存在 localStorage，下次访问自动应用

### 暗色模式

- 完整的深色主题适配，覆盖所有组件和页面
- 支持系统偏好自动切换（`prefers-color-scheme: dark`）
- 手动切换保存在 localStorage

### 无障碍访问（Accessibility）

- WCAG 2.1 AA 级别合规
- 键盘导航支持（Tab 切换、Enter 确认）
- 屏幕阅读器友好（ARIA 标签、role 属性）
- 跳过导航链接（Skip Navigation）
- 减少动画模式（`prefers-reduced-motion`）
- 颜色对比度达标

### 设置页面（5 个 Tab）

| Tab | 功能 |
|-----|------|
| 通用 | 基础设置、语言切换 |
| 外观 | 主题切换、暗色模式 |
| AI | AI 模型配置、API Key |
| 安全 | 密码修改、API Token |
| 集成 | GitHub OAuth、Webhook 配置 |

### 新手引导（Tour Guide）（计划中）

- 首次登录自动触发 7 步引导
- 覆盖侧边栏导航、AI 助手、项目创建等核心功能
- 引导状态保存在 localStorage，不重复显示
- **注意**：此功能尚在开发中，预计 Q3 2026 上线

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

<details>
<summary><strong>如何配置初始管理员？</strong></summary>

生产环境通过环境变量配置（推荐）：

```bash
# backend/.env
INIT_ADMIN_USERNAME=admin
INIT_ADMIN_EMAIL=admin@example.com
INIT_ADMIN_PASSWORD=your_secure_password
```

首次启动时自动创建。已有用户则跳过。

开发环境手动创建：

```bash
cd backend
python create_admin.py
# 默认账号：admin / admin123
```
</details>

<details>
<summary><strong>如何启用多租户隔离？</strong></summary>

多租户功能已内置，默认启用。所有 API 请求通过 `X-Organization-ID` 头标识当前组织。

注册流程：
1. 用户注册时输入组织邀请码 → 自动加入对应组织
2. 不填邀请码 → 自动创建个人空间组织

管理员可以通过 `/api/v1/admin/users` 管理用户角色和状态。
</details>

<details>
<summary><strong>演示系统语言切换不生效？</strong></summary>

1. 确认 `web/.env.production` 中设置了 `VITE_DEPLOY_ENV=demo`
2. 清除浏览器 localStorage 中的 `fst-language` 和 `fst-geo-dismiss` 键
3. 刷新页面，F12 Console 查看 `[GeoLanguage]` 调试输出
4. 如果显示 `is_china: true`，说明你的 IP 被识别为中国（在国内访问不会弹提示）
</details>

<details>
<summary><strong>生产环境部署后前端文件未更新？</strong></summary>

前端构建文件在 `web/dist/`，但 Nginx 可能从其他目录读取。部署时需同步：

```bash
# 构建前端
cd web && npm run build

# 同步到 Nginx 根目录（根据实际配置调整路径）
cp -r dist/* /opt/1panel/www/sites/test.huangxuan.chat/index/

# 重载 Nginx
docker exec openresty openresty -s reload
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

jobs
  test:
    runs-on: ubuntu-latest
    steps
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
 
jobs
  test:
    runs-on: ubuntu-latest
    steps
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
    <img src="images/docs/wechat-qr.webp" alt="微信二维码" width="150px" />
    <p><em>扫码添加作者微信</em></p>
  </div>

---
 
## 🛠 技术栈
 
- **前端**: [React 18](https://reactjs.org/) + [TypeScript](https://www.typescriptlang.org/) + [Vite](https://vitejs.dev/) + [Ant Design 5](https://ant.design/)
- **后端**: [Flask 3.0](https://flask.palletsprojects.com/) + [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- **数据库**: [PostgreSQL 15](https://www.postgresql.org/) + [Redis 7](https://redis.io/)
- **测试引擎**: [Playwright](https://playwright.dev/) (Web) + [Locust](https://locust.io/) (性能) + [Appium](https://appium.io/) (APP)
- **异步任务**: [Celery](https://docs.celeryq.dev/) + [APScheduler](https://apscheduler.readthedocs.io/)
- **国际化**: [i18next](https://www.i18next.com/) + [react-i18next](https://react.i18next.com/) (中英文双语)
- **状态管理**: [Zustand](https://github.com/pmndrs/zustand) (轻量级 Store + persist 持久化)
- **监控**: [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/) (指标采集 + 可视化)
- **基础设施**: [Docker Compose](https://www.docker.com/) + [OpenResty](https://openresty.org/) (Nginx + Lua)
 
---
 
## 📄 许可证
 
本项目采用 [MIT License](LICENSE) 协议开源。
 
<div align="center">
  <sub>Built with ❤️ by FullScopeTest Team</sub>
</div>
