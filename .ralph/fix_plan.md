# FullScopeTest — Production Upgrade Task List
# Ralph fix_plan.md — 自动循环任务清单

> Ralph 每次循环从此文件中找第一个 `[ ]` 任务执行。
> 完成后将 `[ ]` 改为 `[x]`。
> 不要修改任务描述，只修改 checkbox。

---

## 阶段一：工程基础设施（Phase 1 — Engineering Foundation）
> 目标：让现有功能在更稳固的地基上运行，不改变任何对外行为

- [x] **P1-01** 安装并配置 structlog，将所有现有 `print()` 和 `app.logger` 替换为结构化 JSON 日志，每条日志包含 `timestamp`、`level`、`module`、`trace_id` 字段；在 Flask app factory 中生成 `trace_id` 并注入 request context
- [x] **P1-02** 为 Celery 任务添加死信队列（Dead Letter Queue）：配置 `task_routes`、`task_acks_late=True`、`task_reject_on_worker_lost=True`；创建 `dead_letter` 队列；为所有现有 task 添加 `max_retries=3`、`retry_backoff=True`、失败时发送告警日志
- [x] **P1-03** 安装 `prometheus-flask-exporter`，暴露 `/metrics` 端点；添加自定义 metrics：`api_requests_total`（按路由、方法、状态码）、`task_execution_duration_seconds`（按任务类型）、`active_websocket_connections`；在 docker-compose 中添加 Prometheus + Grafana 服务
- [x] **P1-04** 创建 Grafana Dashboard JSON（`infra/monitoring/dashboards/fullscopetest.json`），包含：API 请求率、错误率、P95/P99 响应时间、Celery 任务队列深度、活跃 WebSocket 连接数 5 个面板
- [x] **P1-05** 统一 Docker Compose 端口：开发环境后端统一用 `5000`，生产环境用 `8000`；修复 `docker-compose.yml` 和 `docker-compose.prod.yml` 中的端口不一致问题；更新 `.env.example` 和 README 中的相关说明
- [x] **P1-06** 为 Celery Beat 调度器添加文件锁检查测试（`backend/tests/test_scheduler.py`）：验证多进程启动时只有一个实例获得锁；补充现有调度任务的单元测试，总覆盖率提升到与现有 112 个用例并列
- [x] **P1-07** 创建 `backend/app/core/health.py`：实现 `/health`（基础存活）和 `/health/ready`（数据库 + Redis + Celery 连通性检查）端点；在 docker-compose 中配置 `healthcheck`；添加对应测试用例

---

## 阶段二：差异化核心功能（Phase 2 — Differentiation Features）
> 目标：实现 MeterSphere V3 没有的独家功能，建立技术壁垒

### 2A：视觉回归测试（Visual Regression Testing）

- [x] **P2A-01** 设计并创建视觉回归测试数据模型：`VisualBaseline`（基准截图记录）、`VisualDiff`（差异记录）SQLAlchemy 模型；创建 Alembic 迁移；字段包括 `test_case_id`、`step_index`、`baseline_image_path`、`diff_image_path`、`diff_percentage`、`status`
- [x] **P2A-02** 实现截图存储服务（`backend/app/services/screenshot_service.py`）：截图以 `{project_id}/{test_run_id}/{step}.png` 路径存储到本地 volume（支持后续接入 S3）；实现基准截图的「首次运行自动设为基准」逻辑
- [x] **P2A-03** 实现图像差异比较服务（`backend/app/services/visual_diff_service.py`）：使用 `Pillow` + `imagehash` 计算感知哈希差异；使用像素级对比生成红色高亮差异图；输出 `diff_percentage`（差异百分比）和 `diff_image`（标注了差异区域的对比图）
- [x] **P2A-04** 修改现有 Playwright 执行器（Celery task）：每个步骤执行后自动截图；将截图传入视觉差异服务；若差异超过阈值（默认 5%）将该步骤标记为视觉失败，但不中断测试执行；将视觉结果写入 `VisualDiff` 表
- [x] **P2A-05** 创建视觉回归 API 路由（`backend/app/api/visual.py`）：`GET /api/visual/baselines/{test_case_id}`、`POST /api/visual/baselines/{test_case_id}/approve`（批准新截图为基准）、`GET /api/visual/diffs/{test_run_id}`、`DELETE /api/visual/baselines/{baseline_id}`
- [x] **P2A-06** 实现前端视觉对比组件（`frontend/src/components/VisualDiffViewer.tsx`）：左右分屏展示基准图和当前图；高亮展示差异区域（使用 canvas 叠加红色 mask）；差异百分比显示；「批准为新基准」按钮；集成到测试报告详情页
- [x] **P2A-07** 实现视觉回归历史趋势（`frontend/src/pages/VisualRegressionHistory.tsx`）：展示某个测试用例的视觉变化时间线；每个版本的截图缩略图；差异百分比折线图

### 2B：性能测试深度增强

- [x] **P2B-01** 重新设计性能测试结果数据模型（`PerformanceTestResult`、`PerformanceMetricSample`）：支持存储完整的时间序列数据（每秒的 RPS、响应时间、错误率、并发用户数）；创建 Alembic 迁移
- [x] **P2B-02** 修改 Locust 任务执行器：实时采集并每 5 秒写入一次 `PerformanceMetricSample`；任务结束后计算并存储统计摘要（P50/P75/P95/P99 响应时间、最大 RPS、错误率）
- [x] **P2B-03** 实现性能测试历史对比 API（`GET /api/performance/compare?run_ids=id1,id2,id3`）：返回多次测试运行的关键指标对比；计算性能劣化百分比（相对于基准运行）
- [x] **P2B-04** 实现性能告警规则引擎（`backend/app/services/performance_alert_service.py`）：可配置告警规则（如「P99 响应时间 > 2000ms 触发告警」）；支持「相比上次运行劣化超过 X%」的相对告警；告警通过 WebSocket 实时推送到前端
- [x] **P2B-05** 实现前端性能测试实时大盘（`frontend/src/pages/PerformanceDashboard.tsx`）：Recharts 折线图展示实时 RPS、响应时间、错误率；历史对比视图（多条曲线叠加）；P95/P99 分位数高亮显示

### 2C：AI 能力工程化

- [x] **P2C-01** 设计 AI 功能的可观测性基础设施：创建 `AIInvocationLog` 模型（存储每次 AI 调用的 prompt、response、latency、success/fail、tokens_used、cost_estimate）；创建 `PromptVersion` 模型（Prompt 版本管理）；创建 Alembic 迁移
- [x] **P2C-02** 创建 AI 服务基类（`backend/app/services/ai/base.py`）：统一的 LLM 调用接口；自动记录 `AIInvocationLog`；支持 retry with exponential backoff；超时处理；降级策略（AI 失败时返回 fallback 结果而不是 500）
- [x] **P2C-03** 将现有 NL2Script 功能重构为使用 `PromptVersion` 管理：提取 Prompt 到数据库；支持 A/B 两个版本的 Prompt 同时运行；基于 `AIInvocationLog` 统计每个版本的成功率；实现 `GET /api/ai/prompt-versions` 和 `POST /api/ai/prompt-versions` 接口
- [ ] **P2C-04** 实现基于 OpenAPI/Swagger 的智能用例生成服务（`backend/app/services/ai/swagger_case_generator.py`）：解析 Swagger JSON/YAML；AI 分析每个接口的业务语义；自动生成正常值、边界值、异常值测试用例；支持 `POST /api/ai/generate-cases-from-swagger`；生成的用例直接保存到现有用例管理模块
- [ ] **P2C-05** 实现测试用例语义去重服务（`backend/app/services/ai/semantic_dedup_service.py`）：将用例描述和步骤向量化（使用 `sentence-transformers` 或调 embedding API）；余弦相似度计算；返回相似度 > 0.85 的用例对；提供 `POST /api/ai/find-duplicates` 接口；前端展示去重建议面板
- [ ] **P2C-06** 实现 AI 能力统计看板（`frontend/src/pages/AIInsightsDashboard.tsx`）：AI 调用成功率折线图；各功能模块的 AI 调用量分布；Prompt 版本效果对比表格；平均响应时间趋势；token 消耗统计

---

## 阶段三：CI/CD 深度集成（Phase 3 — CI/CD Integration）
> 目标：让开发者团队能把 FullScopeTest 嵌入日常开发流程

- [ ] **P3-01** 实现 GitHub App OAuth 集成：`GET /api/integrations/github/auth`（OAuth 授权入口）、callback 处理、token 存储（加密存储到数据库）；用户可绑定 GitHub 账号；创建 `GitHubIntegration` 数据模型
- [ ] **P3-02** 实现 GitHub Webhook 接收器增强（`backend/app/api/webhooks/github.py`）：接收 `pull_request` 事件（opened/synchronize/closed）；接收 `push` 事件；HMAC 签名验证；根据触发规则（可配置）自动创建并启动测试计划
- [ ] **P3-03** 实现测试触发规则引擎（`backend/app/services/trigger_rule_service.py`）：可配置规则「当 PR 目标分支为 main 时，运行标签为 regression 的测试套件」；支持「文件路径变更匹配」（如 `/api/**` 变更时只运行接口测试）；规则配置 CRUD API
- [ ] **P3-04** 实现 GitHub Check Run 回写（`backend/app/services/github_check_service.py`）：测试开始时创建 Check Run（状态 in_progress）；实时更新进度（通过 Check Run 的 output.summary）；测试结束时更新最终状态（success/failure）；附上测试报告链接和失败用例摘要
- [ ] **P3-05** 实现 Quality Gate 功能：可配置质量门禁规则（通过率阈值、P95 响应时间上限、视觉差异上限）；`GET /api/quality-gates`、`POST /api/quality-gates`、`POST /api/quality-gates/{id}/evaluate`；Quality Gate 评估结果同步到 GitHub Check Run 状态
- [ ] **P3-06** 发布官方 GitHub Action（`.github/actions/fullscope-test/action.yml`）：支持 `with` 参数：`server-url`、`api-token`、`test-suite-id`、`quality-gate-id`；Action 触发测试、轮询状态、输出结果；在 `README.md` 中提供完整的 Action 使用示例
- [ ] **P3-07** 实现 GitLab CI 集成（`backend/app/api/webhooks/gitlab.py`）：接收 GitLab merge request 和 push webhook；逻辑与 GitHub 一致；生成 GitLab Pipeline 状态回写（通过 GitLab API 提交 commit status）；提供 GitLab CI YAML 模板示例

---

## 阶段四：多租户与生产级安全（Phase 4 — Multi-tenancy & Security）

- [ ] **P4-01** 设计多租户数据模型：创建 `Organization`（组织）、`OrganizationMember`（成员关系）模型；所有现有的 `Project`、`TestCase`、`TestPlan`、`TestResult` 模型添加 `organization_id` 外键；创建 Alembic 迁移（带数据迁移：将现有数据归入默认组织）
- [ ] **P4-02** 实现组织级数据隔离中间件（`backend/app/middleware/tenant.py`）：所有查询自动注入 `organization_id` 过滤条件；防止越权访问（A 组织用户访问 B 组织数据返回 404 而不是 403，避免泄露存在性）；为所有 Service 层方法添加 tenant 参数
- [ ] **P4-03** 实现组织管理 API：`POST /api/organizations`（创建组织）、`GET /api/organizations/me`（当前用户的组织列表）、`POST /api/organizations/{id}/members`（邀请成员）、`DELETE /api/organizations/{id}/members/{user_id}`、`PATCH /api/organizations/{id}/members/{user_id}/role`（修改角色）
- [ ] **P4-04** 实现 API 限流（Rate Limiting）：使用 Redis 实现滑动窗口限流；默认规则：普通用户 100 req/min，API token 1000 req/min；可按组织配置不同限额；触发限流返回 `429` 并附 `Retry-After` header；在 Prometheus 中记录限流触发次数
- [ ] **P4-05** 安全加固——输入验证专项：审查所有接受用户输入的端点；测试用例脚本内容存储时进行沙箱化处理（禁止存储可执行的服务端代码）；Playwright 脚本执行在独立容器中运行（Docker-in-Docker 或隔离 network）；文件上传增加内容类型验证（不仅依赖扩展名）
- [ ] **P4-06** 实现 API Token 管理系统：用户可创建多个 API Token（用于 CI/CD 集成）；Token 有效期、权限范围（read-only/read-write）、最后使用时间记录；Token 值只在创建时展示一次（存储 bcrypt hash）；`GET /api/tokens`、`POST /api/tokens`、`DELETE /api/tokens/{id}`
- [ ] **P4-07** 实现审计日志（Audit Log）：记录所有写操作（创建/修改/删除测试用例、执行测试、修改配置、成员变更）；`AuditLog` 模型包含 `user_id`、`organization_id`、`action`、`resource_type`、`resource_id`、`changes`（JSON diff）、`ip_address`、`timestamp`；`GET /api/audit-logs` 支持按时间、用户、资源类型过滤

---

## 阶段五：FastAPI 迁移与性能优化（Phase 5 — FastAPI Migration & Performance）
> 目标：将 Flask 逐步迁移到 FastAPI，保持 API 完全向后兼容

- [ ] **P5-01** 搭建 FastAPI 应用骨架（与 Flask 并行运行）：创建 `backend/app/fastapi_app.py`；配置 CORS、中间件、异常处理器、自动 OpenAPI 文档；通过 Nginx 路由：新接口走 FastAPI（`/api/v2/`），旧接口继续走 Flask（`/api/`）；确保两套应用共享同一个数据库连接池
- [ ] **P5-02** 迁移认证模块到 FastAPI：将 JWT 验证逻辑重写为 FastAPI `Depends`；实现 `get_current_user`、`get_current_organization` 依赖；Pydantic v2 schema 定义 token payload；在 FastAPI 应用上启用 `/api/v2/auth/` 路由
- [ ] **P5-03** 迁移测试用例管理到 FastAPI（`backend/app/api/v2/test_cases.py`）：完整的 CRUD 路由；Pydantic v2 request/response schema；SQLAlchemy 异步查询（`AsyncSession`）；分页参数（`limit`、`offset`、`total`）；保持与 v1 完全相同的响应结构
- [ ] **P5-04** 迁移接口测试执行模块到 FastAPI：`POST /api/v2/api-tests/run`、`GET /api/v2/api-tests/results/{run_id}`、WebSocket `/api/v2/ws/api-test-logs/{run_id}`；异步 WebSocket 日志推送（替换 Flask-SocketIO）
- [ ] **P5-05** 迁移 Playwright UI 测试模块到 FastAPI：`POST /api/v2/ui-tests/run`、`GET /api/v2/ui-tests/results/{run_id}`、`GET /api/v2/ui-tests/visual-diffs/{run_id}`
- [ ] **P5-06** 迁移性能测试模块到 FastAPI：包含实时指标流（Server-Sent Events 或 WebSocket）；历史对比接口；告警规则配置接口
- [ ] **P5-07** 实现 FastAPI 自动生成的 OpenAPI 文档增强：为所有接口添加完整的 `summary`、`description`、`tags`、`responses` 文档；生成 Postman Collection JSON（`GET /api/v2/openapi/postman`）；生成 MeterSphere 可导入格式（兼容其接口定义格式）
- [ ] **P5-08** 性能基准测试：使用 `locust` 对新的 FastAPI 接口做压测，与原 Flask 接口对比；目标：在相同并发下 FastAPI 版本 P95 响应时间比 Flask 版本低 30%；将基准测试结果写入 `docs/performance-benchmark.md`

---

## 阶段六：文档与发布（Phase 6 — Documentation & Release）

- [ ] **P6-01** 编写完整部署文档（`docs/deployment.md`）：单机 Docker Compose 部署（开发/测试环境）；生产环境 Docker Compose 部署（含 Nginx、SSL、持久化卷）；环境变量完整说明表；常见问题排查（Troubleshooting）
- [ ] **P6-02** 编写 API 文档（`docs/api-reference.md`）：所有 v1 + v2 接口的请求/响应示例；认证说明（JWT + API Token 两种方式）；错误码一览表；WebSocket 协议说明
- [ ] **P6-03** 编写 GitHub Actions 集成指南（`docs/github-actions-integration.md`）：完整的从零到一集成步骤；3 个真实场景的 YAML 示例（PR 自动触发、定时回归、手动触发）；Quality Gate 配置示例
- [ ] **P6-04** 创建第一个正式 Release（v1.0.0-rc1）：更新 `CHANGELOG.md`（按模块列出所有新功能）；创建 `docker-compose.release.yml`（固定所有镜像版本）；写 GitHub Release Notes；更新 README 的功能特性列表，突出与 MeterSphere V3 的差异化
- [ ] **P6-05** 编写与 MeterSphere 的功能对比文档（`docs/vs-metersphere.md`）：功能矩阵对比表（FullScopeTest vs MeterSphere V3 vs MeterSphere V2）；性能基准对比；架构差异说明；从 MeterSphere 迁移指南（数据导出/导入工具或格式说明）
- [ ] **P6-06** 完善前端国际化（i18n）：使用 `react-i18next`；实现中英文切换；至少完成以下页面的英文翻译：登录、测试用例列表、测试执行详情、仪表盘、AI 功能页；语言偏好存储在 localStorage

---

## 状态汇总

完成进度：22 / 48 个任务

**阶段进度：**
- Phase 1（基础设施）：7/7
- Phase 2A（视觉回归）：7/7
- Phase 2B（性能增强）：5/5
- Phase 2C（AI 工程化）：3/6
- Phase 3（CI/CD 集成）：0/7
- Phase 4（多租户安全）：0/7
- Phase 5（FastAPI 迁移）：0/8
- Phase 6（文档发布）：0/6

> **Ralph 提示**：每次循环完成一个任务后，在任务前的 `[ ]` 改为 `[x]`，并更新上方的「完成进度」计数。
