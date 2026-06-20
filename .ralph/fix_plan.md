# FullScopeTest 代码质量修复计划

> 生成日期：2026-06-21
> 本文档汇总所有可通过代码修改解决的问题，按优先级和模块分类。
> 共计 9 大类、40+ 项具体任务，涉及约 80 个需修改/新增的文件。

---

## 一、前端工程质量

### 1.1 超大文件拆分（13 个文件）

| 文件 | 当前行数 | 目标 | 拆分方案 |
|------|---------|------|---------|
| `web/src/pages/api-test/ApiTestWorkspace.tsx` | 2163 | ≤300 | 拆分为 CollectionTree、RequestPanel、ResponsePanel、EnvironmentPanel、AiPanel、useApiTestWorkspace hook |
| `web/src/pages/web-test/WebTestScripts.tsx` | 1743 | ≤300 | 拆分为 ScriptList、ScriptEditor、ExecutionPanel、useWebTestScripts hook |
| `web/src/pages/Settings.tsx` | 1100 | ≤300 | 每个 Tab 独立组件：GeneralTab、AppearanceTab、AiTab、SecurityTab、IntegrationTab |
| `web/src/layouts/MainLayout.tsx` | 1097 | ≤300 | 拆分为 Sidebar、TopBar、UserMenu、ProjectSelector、ThemeToggle |
| `web/src/pages/perf-test/PerfTestScenarios.tsx` | 1068 | ≤300 | 拆分为 ScenarioList、ScenarioEditor、StepEditor |
| `web/src/pages/perf-test/PerformanceDashboard.tsx` | 983 | ≤300 | 拆分为 MetricCards、ChartPanel、AlertPanel |
| `web/src/components/GlobalCopilot.tsx` | 663 | ≤300 | 拆分为 ChatPanel、MessageList、InputArea、useCopilot hook |
| `web/src/pages/app-test/AppTestScripts.tsx` | 641 | ≤300 | 拆分为 ScriptList、ScriptEditor、DevicePanel |
| `web/src/pages/Reports.tsx` | 636 | ≤300 | 拆分为 ReportList、ReportDetail、ExportPanel |
| `web/src/pages/web-test/WebTestRecorder.tsx` | 630 | ≤300 | 拆分为 RecorderControls、PreviewPanel、ScriptOutput |
| `web/src/pages/Login.tsx` | 612 | ≤300 | 拆分为 LoginForm、RegisterForm、SsoSection、LanguagePrompt |
| `web/src/pages/api-test/ApiTestEnvironments.tsx` | 602 | ≤300 | 拆分为 EnvList、EnvEditor、VariableTable |
| `web/src/pages/api-test/ApiTestCollections.tsx` | 574 | ≤300 | 拆分为 CollectionTree、CaseList、CaseDetail |

### 1.2 消除 `any` 类型（10 个高优先文件）

| 文件 | `any` 数量 | 修复方案 |
|------|-----------|---------|
| `web/src/pages/api-test/ApiTestWorkspace.tsx` | 41 | 定义 RequestConfig、ResponseData、TestCase 等接口 |
| `web/src/services/apiTestService.ts` | 21 | 定义所有 API 响应类型（ApiResponse\<T\> 泛型） |
| `web/src/pages/web-test/WebTestScripts.tsx` | 20 | 定义 WebScript、ExecutionResult 等接口 |
| `web/src/pages/perf-test/PerfTestScenarios.tsx` | 18 | 定义 PerfScenario、PerfMetric 等接口 |
| `web/src/pages/CICD.tsx` | 18 | 定义 Pipeline、CiConfig 等接口 |
| `web/src/pages/api-test/RequestEditor.tsx` | 9 | 定义 RequestHeader、RequestBody 类型 |
| `web/src/pages/Dashboard.tsx` | 9 | 定义 DashboardStats、ChartData 类型 |
| `web/src/pages/perf-test/PerformanceDashboard.tsx` | 8 | 定义 MetricSnapshot、ChartPoint 类型 |
| `web/src/pages/web-test/components/AiExploreModal.tsx` | 7 | 定义 AiSuggestion 类型 |
| `web/src/pages/perf-test/ScenarioStepEditor.tsx` | 7 | 定义 StepConfig 类型 |

**操作步骤**：
1. 在 `web/src/types/` 目录下建立统一类型定义文件
2. 按模块建立：`api-test.ts`、`web-test.ts`、`perf-test.ts`、`common.ts`
3. 在 `tsconfig.json` 中启用 `noImplicitAny: true`
4. 逐步替换，每次 PR 改一个文件

### 1.3 前端测试补充

当前状态：仅 10 个测试文件，全部是浅层冒烟测试（仅验证渲染不崩溃）。

**目标**：核心模块测试覆盖率 ≥ 60%

| 优先级 | 测试目标 | 测试类型 | 文件位置 |
|--------|---------|---------|---------|
| P0 | Zustand stores（authStore、projectStore） | 单元测试 | `web/src/stores/__tests__/` |
| P0 | API 服务层（apiTestService、authService） | 单元测试 + Mock | `web/src/services/__tests__/` |
| P0 | Axios 拦截器（Token 注入、401 刷新） | 单元测试 | `web/src/utils/__tests__/` |
| P1 | 权限 Hook（useRole） | Hook 测试 | `web/src/hooks/__tests__/` |
| P1 | 业务 Hook（useAiAssistant） | Hook 测试 | `web/src/pages/api-test/hooks/__tests__/` |
| P1 | 核心组件（RequestEditor、ResponseViewer） | 组件测试 | 对应目录 `__tests__/` |
| P2 | 路由守卫和权限页面渲染 | 集成测试 | `web/src/__tests__/integration/` |
| P2 | 主题切换、语言切换逻辑 | 单元测试 | `web/src/stores/__tests__/` |

### 1.4 状态管理重构

**问题**：ApiTestWorkspace 等文件内有 20+ 个 `useState`，状态碎片化，难以追踪和调试。

**方案**：
- 为复杂页面创建专用 Zustand store（如 `useApiTestStore`）
- 将相关状态聚合为对象，减少 useState 数量
- 将副作用逻辑抽取到自定义 hooks

| 页面文件 | 需创建的 Store |
|---------|---------------|
| `web/src/pages/api-test/ApiTestWorkspace.tsx` | `web/src/stores/apiTestWorkspaceStore.ts` |
| `web/src/pages/web-test/WebTestScripts.tsx` | `web/src/stores/webTestStore.ts` |
| `web/src/pages/perf-test/PerfTestScenarios.tsx` | `web/src/stores/perfTestStore.ts` |

### 1.5 样式方案统一

**当前问题**：全局 CSS + 内联 style + Ant Design 样式三种方案混用。

**方案**：
- 建立 CSS Modules 规范（`*.module.css`）
- 逐步将内联 style 迁移到 CSS Modules
- 全局样式只保留 reset 和 CSS 变量定义
- 暗色主题通过 CSS 变量实现，替代独立的 `dark-theme.css`

| 当前文件 | 改造方向 |
|---------|---------|
| `web/src/styles/index.css` | 拆分为 CSS 变量文件 + 各组件 module.css |
| `web/src/styles/dark-theme.css` | 合并为 CSS 变量的 dark 主题覆盖 |
| `web/src/styles/responsive.css` | 合并到各组件的 module.css 中 |

### 1.6 前端性能监控

**需新增文件**：
- `web/src/utils/webVitals.ts` — 采集 LCP/FID/CLS 等 Web Vitals 指标
- `web/src/utils/errorReporter.ts` — 统一错误上报（对接 Sentry 或自建）

**需修改文件**：
- `web/vite.config.ts` — 添加 `rollup-plugin-visualizer` 进行 Bundle 体积分析

---

## 二、后端工程质量

### 2.1 后端大文件拆分（4 个文件）

| 文件 | 当前行数 | 目标 | 拆分方案 |
|------|---------|------|---------|
| `backend/app/api/api_test.py` | 1556 | ≤300 | 拆分为 routes/api_test.py、services/api_test_service.py、utils/api_test_utils.py |
| `backend/app/api/web_test.py` | 871 | ≤300 | 拆分为 routes、services、executor |
| `backend/app/api/perf_test.py` | 813 | ≤300 | 拆分为 routes、services、runner |
| `backend/app/api/reports.py` | 763 | ≤300 | 拆分为 routes、services |

### 2.2 建立 Service 层架构

**需新增目录和文件**：
```
backend/app/services/
├── __init__.py
├── base.py              # ServiceBase 基类（统一事务管理、日志）
├── api_test_service.py  # API 测试业务逻辑
├── web_test_service.py  # Web 测试业务逻辑
├── perf_test_service.py # 性能测试业务逻辑
├── report_service.py    # 报告业务逻辑
├── auth_service.py      # 认证业务逻辑
└── ai_service.py        # AI 相关业务逻辑
```

**ServiceBase 基类设计**：
```python
class ServiceBase:
    def __init__(self, db_session):
        self.db = db_session

    def commit(self):
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def add_and_commit(self, obj):
        self.db.add(obj)
        self.commit()
        return obj
```

### 2.3 统一异常处理

**需新增文件**：`backend/app/utils/exceptions.py`

```python
class AppError(Exception):
    status_code = 400
    def __init__(self, message, code=None):
        self.message = message
        self.code = code

class NotFoundError(AppError):
    status_code = 404

class ForbiddenError(AppError):
    status_code = 403

class ValidationError(AppError):
    status_code = 422
```

**需修改文件**：
- `backend/app/__init__.py` — 注册全局异常处理器
- 所有 `api/*.py` — 将 `except Exception` 替换为具体异常类型
- 移除所有 `except Exception: pass` 模式

### 2.4 数据库事务管理统一

**需修改文件**：
- 所有 `backend/app/api/*.py` — 移除直接的 `db.session.commit()`，改为调用 Service 层
- `backend/app/config.py` — 添加 `SQLALCHEMY_ENGINE_OPTIONS` 配置连接池参数

### 2.5 修复重构计划虚假声明

**需修改文件**：`REFACTOR_PLAN.md`

将 P0/P1/P2 进度如实更新为实际完成状态（当前文件声称 100% 完成，但 1.1 和 2.1 中的大文件均未拆分），重新标记未完成项。

### 2.6 Alembic 迁移工作流规范化

**需修改文件**：
- `backend/init_db.py` — 添加安全警告，生产环境禁止执行
- `backend/app/__init__.py` — 启动时自动运行 `alembic upgrade head`
- `README.md` — 将"运行 init_db.py"改为"运行 alembic upgrade"

**需新增文件**：
- `backend/scripts/migrate.sh` — 一键迁移脚本（含备份提示）

### 2.7 依赖版本精确锁定

**需修改文件**：
- `backend/requirements.txt` — 将 `>=` 改为 `==` 精确锁定，确保构建可重现
- `web/package.json` — 确认 package-lock.json 存在且最新

**需新增文件**：
- `backend/requirements-lock.txt` — `pip freeze` 输出的精确版本
- `.github/dependabot.yml` — 自动依赖更新配置（见 CI/CD 章节）

### 2.8 Access Token 有效期调整

**需修改文件**：
- `backend/app/config.py` — `JWT_ACCESS_TOKEN_EXPIRES` 从 24h 改为 1h（安全最佳实践）
- `backend/app/config.py` — `JWT_REFRESH_TOKEN_EXPIRES` 保持 30d
- `web/src/utils/api.ts` — 确认 401 自动刷新逻辑正确处理短 Token 场景

### 2.9 移除明文默认密码

**需修改文件**：
- `backend/.env.example` — 将 `INIT_ADMIN_PASSWORD=admin123` 改为 `INIT_ADMIN_PASSWORD=<CHANGE_ME>`
- `README.md` — 移除所有默认密码明文（admin123）
- `backend/create_admin.py` — 添加交互式密码输入或随机密码生成

---

## 三、CI/CD 工程化

### 3.1 建立 GitHub Actions 工作流

**需新增目录和文件**：
```
.github/
├── workflows/
│   ├── ci.yml               # 主 CI 流水线（push/PR 触发）
│   ├── release.yml          # 自动发布（Tag 触发）
│   └── docker-publish.yml   # Docker 镜像发布
├── ISSUE_TEMPLATE/
│   ├── bug_report.md        # Bug 报告模板
│   └── feature_request.md   # 功能请求模板
├── PULL_REQUEST_TEMPLATE.md # PR 模板
└── dependabot.yml           # 自动依赖更新
```

**ci.yml 核心 Job**：
- `lint-backend`: `flake8` + `mypy`
- `lint-frontend`: `npm run lint` + `npx tsc --noEmit`
- `test-backend`: `pytest --cov`
- `test-frontend`: `npm run test`
- `build`: `npm run build` + Docker 构建验证
- `security`: `pip-audit` + `npm audit`

**release.yml 核心逻辑**：
- 基于 `v*` Git Tag 触发
- 自动生成 Release Notes（基于 Conventional Commits）
- 构建并推送 Docker 镜像到 GHCR

### 3.2 建立 Semantic Versioning

**需修改文件**：
- `CHANGELOG.md` — 采用 [Keep a Changelog](https://keepachangelog.com/) 格式，按版本记录变更
- `README.md` — 添加版本徽章和最新版本号

**需新增文件**：
- `.release-please-manifest.json` — release-please 配置

### 3.3 Docker 镜像发布

**需新增文件**：
- `.github/workflows/docker-publish.yml`

**需修改文件**：
- `docker/Dockerfile.backend` — 优化多阶段构建，减小镜像体积
- `docker/Dockerfile.frontend` — 使用 Nginx Alpine 基础镜像

### 3.4 ESLint / Prettier / Black 配置强化

**需新增/修改文件**：
- `web/.eslintrc.cjs` — 强化规则，特别是 `@typescript-eslint/no-explicit-any: error`
- `web/.prettierrc` — 统一格式化规则（printWidth、singleQuote、trailingComma）
- `backend/pyproject.toml` — 添加 `[tool.black]` 和 `[tool.ruff]` 配置
- `backend/setup.cfg` — 添加 `[flake8]` 配置（max-line-length、ignore 列表）

### 3.5 建立 Issue/PR 模板

**需新增文件**：
- `.github/ISSUE_TEMPLATE/bug_report.md` — 包含复现步骤、期望行为、环境信息
- `.github/ISSUE_TEMPLATE/feature_request.md` — 包含用例描述、期望 API
- `.github/PULL_REQUEST_TEMPLATE.md` — 包含变更说明、测试确认、Checklist

---

## 四、文档工程化

### 4.1 精简 README

**需修改文件**：`README.md`（当前 1350+ 行）

**目标**：精简至 300 行以内。

**保留内容**：项目简介、核心特性列表、快速开始（最简步骤）、文档导航链接、贡献指南链接、许可证。

**迁移出 README 的内容**：

| 当前 README 章节 | 迁移目标文件 |
|-----------------|-------------|
| 系统架构详解（含 Mermaid 图） | `docs/architecture.md` |
| 后端架构详解 | `docs/backend-architecture.md` |
| 前端架构详解 | `docs/frontend-architecture.md` |
| 安全架构 | `docs/security.md` |
| GitHub Actions 集成 | `docs/github-actions-integration.md`（已有，移除 README 中重复） |
| 完整 FAQ（13 个问答） | `docs/faq.md` |
| 生产环境部署 | `docs/deployment.md`（已有，移除 README 中重复） |
| 与 MeterSphere 对比表 | `docs/comparison.md` |

### 4.2 同步 README_EN

**需修改文件**：`README_EN.md`

同步中文 README 的结构变更，确保英文版完整且准确。

### 4.3 补充 OpenAPI/Swagger 自动文档

**需新增文件**：
- `backend/app/utils/swagger.py` — Flask-RESTX 或 apispec 集成
- `docs/api/openapi.yaml` — 自动生成的 OpenAPI 规范

**需修改文件**：
- `backend/app/__init__.py` — 注册 Swagger UI 路由（`/api/docs`）
- `backend/requirements.txt` — 添加 `flask-restx` 或 `apispec` 依赖

### 4.4 补充架构决策记录（ADR）

**需新增目录和文件**：
```
docs/adr/
├── 001-flask-over-fastapi.md    # 为什么选 Flask
├── 002-zustand-over-redux.md    # 为什么选 Zustand
├── 003-playwright-over-selenium.md  # 为什么选 Playwright
├── 004-celery-for-async-tasks.md    # 为什么选 Celery
└── template.md                  # ADR 模板
```

### 4.5 完善 CONTRIBUTING.md

**需修改文件**：`CONTRIBUTING.md`

补充以下缺失内容：
- 开发环境搭建的完整步骤（含 IDE 推荐配置）
- 分支策略说明（main/develop/feature-*/hotfix-*）
- Commit 规范（Conventional Commits 格式）
- PR 流程和 Code Review 要求
- 代码风格指南链接（ESLint/Black 配置）

---

## 五、功能代码完善

### 5.1 i18n 自动化检测

**需新增文件**：
- `web/scripts/check-i18n.ts` — 扫描代码中 `t()` 调用的 key，与 locale JSON 对比，输出缺失/多余 key

**需修改文件**：
- `web/package.json` — 添加 `"check-i18n"` 脚本
- `.github/workflows/ci.yml` — 集成 i18n 检查到 CI 流水线

### 5.2 国际化语言扩展

**需新增文件**：
- `web/src/i18n/locales/ja.json` — 日语
- `web/src/i18n/locales/ko.json` — 韩语
- `web/src/i18n/locales/es.json` — 西班牙语

**需修改文件**：
- `web/src/i18n/index.ts` — 注册新语言资源
- `web/src/components/LanguageSwitchPrompt.tsx` — 支持更多语言选项

### 5.3 前端错误监控集成

**需新增文件**：
- `web/src/utils/sentry.ts` — Sentry SDK 初始化（含 DSN、环境、采样率配置）
- `web/src/utils/errorBoundary.tsx` — 增强 ErrorBoundary，自动上报到 Sentry

**需修改文件**：
- `web/src/main.tsx` — 在应用入口引入 Sentry 初始化
- `web/package.json` — 添加 `@sentry/react` 依赖
- `web/.env.production` — 添加 `VITE_SENTRY_DSN` 环境变量

### 5.4 Bundle 分析与优化

**需新增文件**：
- `web/scripts/analyze-bundle.ts` — Bundle 体积分析脚本

**需修改文件**：
- `web/vite.config.ts` — 添加 `rollup-plugin-visualizer`，配置 manualChunks 代码分割策略
- `web/package.json` — 添加 `"analyze"` 脚本命令

### 5.5 前端日志工具规范化

**需修改文件**：
- `web/src/utils/logger.ts` — 确认生产环境禁用 `console.log`，仅保留 `error`/`warn`
- 所有使用 `console.log` 的源文件 — 替换为 `logger.debug/info/warn/error`

---

## 六、安全加固

### 6.1 移除仓库中的敏感信息

**需检查并修改的文件**：
- `backend/.env.example` — 移除真实密码值，改为占位符 `<CHANGE_ME>`
- `README.md` — 移除所有默认密码明文（`admin123`）
- `Jenkinsfile` — 检查是否有硬编码凭据

### 6.2 安全响应头完善

**需修改文件**：
- `backend/app/middleware/security_headers.py` — 确认包含以下响应头：
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security: max-age=31536000`
  - `Content-Security-Policy`（基础策略）

### 6.3 输入校验强化

**需新增文件**：
- `backend/app/utils/validators.py` — 统一输入校验工具函数（长度、类型、格式）

**需修改文件**：
- 所有 `backend/app/api/*.py` — 对用户输入进行长度、类型、格式校验
- 审计所有 raw SQL 执行点，确认已参数化（防 SQL 注入）

---

## 七、后端测试补充

### 7.1 当前状态

已有 606 个测试文件，但缺少以下关键覆盖。

### 7.2 需补充的测试

| 优先级 | 测试目标 | 文件位置 |
|--------|---------|---------|
| P0 | Service 层单元测试（2.2 新建后） | `backend/tests/services/` |
| P0 | 中间件测试（tenant、rate_limit、security_headers） | `backend/tests/middleware/` |
| P1 | Alembic 迁移脚本正确性测试 | `backend/tests/migrations/` |
| P1 | Celery 异步任务测试 | `backend/tests/tasks/` |
| P2 | 端到端集成测试（完整请求链路） | `backend/tests/integration/` |

### 7.3 测试覆盖率门槛

**需修改文件**：
- `backend/pyproject.toml` — 添加 `[tool.pytest.ini_options]` 配置 `--cov-fail-under=60`
- `.github/workflows/ci.yml` — CI 中添加覆盖率报告上传和门槛检查

---

## 八、基础设施优化

### 8.1 Docker 镜像优化

**需修改文件**：
- `docker/Dockerfile.backend` — 多阶段构建（builder + runtime），减小镜像体积
- `docker/Dockerfile.frontend` — 使用 `nginx:alpine` 基础镜像
- `docker-compose.prod.yml` — 添加 `healthcheck`、内存/CPU 资源限制

### 8.2 Prometheus 指标暴露

**需新增文件**：
- `backend/app/middleware/metrics.py` — Flask Prometheus 中间件（请求计数、延迟直方图、活跃连接数）

**需修改文件**：
- `backend/app/__init__.py` — 注册 `/metrics` 端点
- `backend/requirements.txt` — 添加 `prometheus-client` 依赖
- `infra/monitoring/prometheus/prometheus.yml` — 添加自身后端的 scrape target

---

## 九、Git 仓库清理

### 9.1 清理临时/调试文件

**需从仓库删除的文件**（不应存在于版本控制中）：
- `chinese_final.txt` — 翻译临时文件
- `chinese_remaining.txt` — 翻译临时文件
- `chinese_text_report.txt` — 翻译临时文件
- `chinese_to_translate.txt` — 翻译临时文件
- `remaining_chinese.txt` — 翻译临时文件
- `tree.txt` — 目录树临时输出
- `cloc.txt` — 代码行数临时输出
- `commit_p0.bat` — 临时提交脚本
- `start_redis.bat` — 本地启动脚本
- `START.bat` — 本地启动脚本
- `test_locust.py` — 临时测试脚本

### 9.2 更新 .gitignore

**需修改文件**：`.gitignore`

补充忽略规则：
- `*.bat`（Windows 本地启动脚本）
- `*.txt`（临时分析输出文件，排除 README 等）
- 已确认：`.env`、`node_modules/`、`__pycache__/` 已在忽略列表中

---

## 十、执行顺序建议

```
Phase 1 — 基础设施（第1-2周）
├── 1.1 建立 GitHub Actions CI 工作流（ci.yml）
├── 1.2 建立 ESLint/Prettier/Black 配置并强化规则
├── 1.3 建立 Issue/PR 模板
├── 1.4 清理仓库临时文件（9.1）
└── 1.5 修复 REFACTOR_PLAN.md 虚假进度声明（2.5）

Phase 2 — 代码质量（第3-6周）
├── 2.1 建立前端统一类型定义（web/src/types/ 目录）
├── 2.2 消除前端 any 类型（按文件逐步推进，每次 PR 改一个文件）
├── 2.3 拆分前端超大文件（优先级：ApiTestWorkspace → WebTestScripts → 其余）
├── 2.4 建立后端 Service 层架构（backend/app/services/）
├── 2.5 拆分后端大文件（api_test.py → routes + services + utils）
└── 2.6 统一异常处理（exceptions.py + 全局处理器）

Phase 3 — 测试覆盖（第7-10周）
├── 3.1 补充 Zustand Store 单元测试
├── 3.2 补充后端 Service 层单元测试
├── 3.3 补充前端 Hook 测试
├── 3.4 补充核心组件测试
└── 3.5 建立覆盖率门槛（≥60%，CI 强制检查）

Phase 4 — 文档与发布（第11-12周）
├── 4.1 精简 README 至 300 行以内
├── 4.2 补充 OpenAPI/Swagger 自动文档
├── 4.3 建立 Semantic Versioning + CHANGELOG
├── 4.4 发布 Docker 镜像到 GHCR
└── 4.5 补充 ADR 架构决策文档

Phase 5 — 增强功能（持续迭代）
├── 5.1 i18n 自动化检测脚本 + CI 集成
├── 5.2 前端错误监控（Sentry 集成）
├── 5.3 Bundle 分析与体积优化
├── 5.4 国际化语言扩展（日/韩/西）
└── 5.5 安全加固（响应头、输入校验、密码策略）
```

---

> **注意**：每项修改应作为独立 PR 提交，便于 Review 和回滚。每个 PR 需通过 CI 全部检查后方可合并。
