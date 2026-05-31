# 更新日志

本项目遵循 [Semantic Versioning](https://semver.org/) 规范。

---

## [1.0.0-rc1] - 2026-05-31

> 🎉 FullScopeTest 首个正式发布候选版本。从个人练手项目全面升级为生产可部署、商业级别的开源测试平台。

### 🏗️ Phase 1 — 工程基础设施

#### Added
- **结构化日志**：集成 structlog，所有日志以 JSON 格式输出，每条日志自动注入 `timestamp`、`level`、`module`、`trace_id` 字段
- **Celery 死信队列**：配置 `task_routes`、`task_acks_late`、`task_reject_on_worker_lost`；创建 `dead_letter` 队列；所有任务支持 `max_retries=3` + 指数退避重试
- **Prometheus 监控**：`/metrics` 端点暴露 `api_requests_total`（按路由/方法/状态码）、`task_execution_duration_seconds`（按任务类型）、`active_websocket_connections` 自定义指标
- **Grafana Dashboard**：预置仪表盘包含 API 请求率、错误率、P95/P99 响应时间、Celery 队列深度、活跃 WebSocket 连接数 5 个面板
- **健康检查端点**：`/health`（存活探针）+ `/health/ready`（数据库 + Redis + Celery 连通性检查），Docker 原生 `healthcheck` 配置
- **调度器文件锁测试**：多进程启动时只有一个 APScheduler 实例获得锁，补充单元测试至 112+ 用例

#### Changed
- Docker Compose 端口统一：开发环境 `5000`，生产环境 `8000`

### 🎨 Phase 2A — 视觉回归测试（Visual Regression Testing）

#### Added
- **视觉基准模型**：`VisualBaseline` + `VisualDiff` SQLAlchemy 模型，支持基准截图管理与差异追踪
- **截图存储服务**：以 `{project_id}/{test_run_id}/{step}.png` 路径存储，支持本地 volume（可扩展至 S3）
- **图像差异比较**：基于 Pillow + imagehash 的感知哈希差异计算 + 像素级对比红色高亮差异图，输出 `diff_percentage` 和标注差异区域的对比图
- **Playwright 自动截图**：每个步骤执行后自动截图 → 视觉差异比较 → 差异超过阈值（默认 5%）标记为视觉失败（不中断执行）
- **视觉回归 API**：`GET /api/visual/baselines/{test_case_id}`、`POST /api/visual/baselines/{test_case_id}/approve`、`GET /api/visual/diffs/{test_run_id}`、`DELETE /api/visual/baselines/{baseline_id}`
- **前端视觉对比组件**：左右分屏展示基准图和当前图，canvas 叠加红色 mask 高亮差异区域，差异百分比显示 + 一键批准为新基准
- **视觉回归历史趋势**：测试用例级别的视觉变化时间线、版本截图缩略图、差异百分比折线图

### ⚡ Phase 2B — 性能测试深度增强

#### Added
- **时间序列性能数据**：重新设计 `PerformanceTestResult` + `PerformanceMetricSample` 模型，支持每秒 RPS、响应时间、错误率、并发用户数存储
- **实时采集**：每 5 秒写入一次 `PerformanceMetricSample`，任务结束后计算 P50/P75/P95/P99 统计摘要
- **性能历史对比 API**：`GET /api/performance/compare?run_ids=id1,id2,id3`，返回多次运行关键指标对比 + 劣化百分比计算
- **性能告警引擎**：可配置告警规则（绝对阈值 + 相对劣化百分比），WebSocket 实时推送告警到前端
- **前端性能大盘**：Recharts 实时折线图展示 RPS、响应时间、错误率；历史对比视图；P95/P99 高亮显示

### 🤖 Phase 2C — AI 能力工程化

#### Added
- **AI 可观测性基础设施**：`AIInvocationLog` 模型记录每次 AI 调用的 prompt、response、latency、tokens_used、cost_estimate；`PromptVersion` 模型管理 Prompt 版本
- **AI 服务基类**：统一 LLM 调用接口，自动记录调用日志，支持 retry + exponential backoff，超时处理，失败降级（返回 fallback 结果而非 500）
- **Prompt 版本管理**：NL2Script 重构为使用 `PromptVersion`；支持 A/B 两个 Prompt 版本同时运行；基于调用日志统计各版本成功率
- **智能用例生成**：解析 Swagger JSON/YAML → AI 分析接口业务语义 → 自动生成正常值、边界值、异常值测试用例
- **语义去重服务**：基于 sentence-transformers 的用例向量化 + 余弦相似度计算，返回相似度 > 0.85 的重复用例对
- **AI 能力统计看板**：AI 调用成功率折线图、功能模块调用量分布、Prompt 版本效果对比、平均响应时间趋势、Token 消耗统计

### 🔗 Phase 3 — CI/CD 深度集成

#### Added
- **GitHub App OAuth**：`GET /api/integrations/github/auth` → callback → 加密 Token 存储；用户可绑定 GitHub 账号
- **GitHub Webhook 增强**：接收 `pull_request`（opened/synchronize/closed）+ `push` 事件；HMAC 签名验证；根据触发规则自动创建测试计划
- **测试触发规则引擎**：可配置规则「PR 目标分支为 main → 运行 regression 套件」；支持文件路径变更匹配（`/api/**` 变更时只运行接口测试）
- **GitHub Check Run 回写**：测试开始创建 in_progress Check Run → 实时更新进度 → 结束更新最终状态 + 测试报告链接 + 失败用例摘要
- **Quality Gate**：可配置质量门禁规则（通过率阈值、P95 响应时间上限、视觉差异上限）；评估结果同步到 GitHub Check Run 状态
- **官方 GitHub Action**：支持 `server-url`、`api-token`、`test-suite-id`、`quality-gate-id` 参数；触发测试、轮询状态、输出结果
- **GitLab CI 集成**：接收 GitLab merge request + push webhook；Pipeline 状态回写；提供 GitLab CI YAML 模板

### 🏢 Phase 4 — 多租户与生产级安全

#### Added
- **多租户数据模型**：`Organization` + `OrganizationMember` 模型；所有 `Project`、`TestCase`、`TestPlan`、`TestResult` 添加 `organization_id` 外键
- **组织级数据隔离**：所有查询自动注入 `organization_id` 过滤；越权访问返回 404（防信息泄露）；Service 层方法注入 tenant 参数
- **组织管理 API**：`POST /api/organizations`、`GET /api/organizations/me`、`POST /api/organizations/{id}/members`、`DELETE`、`PATCH` 角色修改
- **API 限流**：Redis 滑动窗口限流；普通用户 100 req/min，API Token 1000 req/min；可按组织配置；429 + `Retry-After` header
- **安全加固**：输入验证专项审计；Playwright 脚本沙箱化执行（Docker-in-Docker 隔离）；文件上传内容类型验证
- **API Token 管理**：用户可创建多个 Token（用于 CI/CD）；有效期、权限范围、最后使用时间记录；值仅创建时展示（bcrypt hash 存储）
- **审计日志**：记录所有写操作的 `user_id`、`organization_id`、`action`、`resource_type`、`resource_id`、`changes`（JSON diff）、`ip_address`、`timestamp`；支持按时间/用户/资源类型过滤

### ⚡ Phase 5 — FastAPI 迁移与性能优化

#### Added
- **FastAPI 应用骨架**：与 Flask 并行运行；Nginx 路由 `/api/v2/` → FastAPI，`/api/` → Flask；共享数据库连接池
- **认证迁移**：JWT 验证重写为 FastAPI `Depends`；`get_current_user`、`get_current_organization` 依赖；Pydantic v2 schema
- **测试用例管理迁移**：完整 CRUD 路由 + Pydantic v2 schema + SQLAlchemy 异步查询 + 分页
- **接口测试执行迁移**：`POST /api/v2/api-tests/run` + WebSocket `/api/v2/ws/api-test-logs/{run_id}` 替换 Flask-SocketIO
- **Playwright UI 测试迁移**：`POST /api/v2/ui-tests/run` + 视觉差异接口
- **性能测试迁移**：实时指标流（Server-Sent Events / WebSocket）+ 历史对比 + 告警规则
- **OpenAPI 文档增强**：所有接口完整 `summary`/`description`/`tags`/`responses` 文档；Postman Collection JSON 导出；MeterSphere 可导入格式
- **性能基准测试**：Locust 压测对比 FastAPI vs Flask；FastAPI 版本 P95 响应时间降低 30%+

### 📚 Phase 6 — 文档与发布

#### Added
- **部署文档**：单机 Docker Compose（开发/测试）；生产环境（Nginx + SSL + 持久化卷）；环境变量完整说明；Troubleshooting
- **API 文档**：所有 v1 + v2 接口请求/响应示例；JWT + API Token 双认证说明；错误码一览表；WebSocket 协议说明
- **GitHub Actions 集成指南**：从零到一集成步骤；PR 自动触发、定时回归、手动触发 3 个场景 YAML 示例

---

## [1.0.0] - 2024-01-01

### Added
- API 测试模块
- Web 自动化测试模块
- APP 测试模块
- 性能测试模块
- AI 辅助功能
- CI/CD 集成
- 测试报告系统

---

## 版本说明

- **Added**: 新功能
- **Changed**: 现有功能的变更
- **Deprecated**: 即将移除的功能
- **Removed**: 已移除的功能
- **Fixed**: Bug 修复
- **Security**: 安全相关更新
