# FullScopeTest 商业化改进计划（完整版）

> 每条任务完成后标记 `- [x]`，并附上 commit hash。
> 已有 commit 的任务来自之前的迭代，新增任务来自商业化差距分析。

---

## P0：安全与数据一致性（阻塞商业化）

### P0-1: SSRF 防护 — URL 目标地址校验

**问题**：接口测试、Web 测试的执行引擎会向用户指定的 URL 发起 HTTP 请求，缺乏 SSRF 防护。多租户 SaaS 场景下攻击者可借此探测内网服务。

**修改范围**：
- 新增 `backend/app/utils/url_safety.py`
- 修改 `backend/app/api/api_test.py` — 执行接口测试前校验 URL
- 修改 `backend/app/api/perf_test.py` — 执行性能测试前校验 URL
- 修改 `backend/app/api/web_test.py` — Web 测试的目标 URL 校验
- 新增 `backend/tests/test_url_safety.py`

**实现要求**：
- 创建 `is_safe_url(url: str) -> tuple[bool, str]` 工具函数
- 黑名单：`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`, `fc00::/7`, `metadata.google.internal`
- 使用 `ipaddress` 标准库解析 URL 中的 host，拒绝解析为内网 IP 的请求
- 支持通过环境变量 `SSRF_ALLOWLIST_HOSTS` 配置白名单（如 `localhost` 用于开发环境）
- 在所有发起外部 HTTP 请求的 API 入口处调用此校验
- 提供清晰的错误信息：`"目标地址不允许访问内网资源"`

- [x] 已完成 — 51684a4

---

### P0-2: 脚本执行沙箱隔离

**问题**：`tasks.py` 中使用 `subprocess` 执行 Playwright/Locust 脚本，用户输入的脚本内容直接传入，存在命令注入风险。

**修改范围**：
- 修改 `backend/app/tasks.py` — `run_web_test_task` 和 `run_perf_test_task` 的 subprocess 调用
- 新增 `backend/app/utils/sandbox.py` — 沙箱执行工具
- 新增 `backend/tests/test_sandbox.py`

**实现要求**：
- 脚本内容写入临时文件后通过 `subprocess.run([sys.executable, script_path], ...)` 执行，**禁止** `shell=True`
- 执行时设置 `timeout`（默认 300 秒）
- 执行时限制工作目录为临时目录，不暴露项目路径
- 在非 Docker 环境下，至少实现：禁止 `os.system`, `subprocess.call(shell=True)`, `__import__('os')` 等常见注入向量（通过脚本预处理或 AST 检查）
- 提供环境变量 `SANDBOX_MODE`（`subprocess`/`docker`），为后续 Docker 沙箱预留扩展点
- 记录所有脚本执行的审计日志（user_id, script_hash, 执行时间, 结果）

- [x] 已完成 — 282cca3

---

### P0-3: JWT Token 存储安全

**问题**：前端将 JWT Token 存储在 Zustand persist（localStorage），XSS 攻击者可直接窃取 Token。

**修改范围**：
- 修改 `web/src/stores/authStore.ts` — Token 存储策略
- 修改 `web/src/services/api.ts` — 请求拦截器适配
- 修改 `backend/app/api/auth.py` — 登录/注册接口返回 httpOnly cookie
- 修改 `backend/app/__init__.py` — Cookie 安全配置

**实现要求**：
- 后端登录成功后设置 httpOnly + Secure + SameSite=Lax 的 cookie 存储 access_token
- refresh_token 同样使用 httpOnly cookie
- 前端 authStore 不再在 localStorage 中存储 token 明文
- 前端 axios 请求配置 `withCredentials: true`
- 提供环境变量 `COOKIE_SECURE` 控制 Secure 标志（开发环境可关闭）
- 保持现有 API Token（Authorization header）机制不变，仅影响用户登录态

- [x] 已完成 — 4f01c64

---

### P0-4: 运行状态外部化 — 从进程内存迁移到 Redis

**问题**：`web_test.py` 中 `recording_processes = {}` 和 `live_view_sessions = {}` 直接存在 Python 进程内存，多实例部署不共享，进程重启丢失状态。

**修改范围**：
- 修改 `backend/app/api/web_test.py` — 录制进程和会话状态管理
- 新增 `backend/app/services/session_store.py` — 基于 Redis 的会话状态存储
- 新增 `backend/tests/test_session_store.py`

**实现要求**：
- 抽象 `SessionStore` 接口，提供 `get/set/delete/exists/expire` 方法
- 生产实现使用 Redis（通过 `REDIS_URL` 配置），开发/测试回退到内存 dict
- `recording_processes` 迁移为 Redis hash，key 格式 `recording:{session_id}`
- `live_view_sessions` 迁移为 Redis hash，key 格式 `live_view:{session_id}`
- 设置 TTL（录制会话 1 小时，live view 会话 30 分钟），防止泄漏
- 进程对象（如 subprocess）本身无法序列化，记录 PID + 元数据到 Redis，进程管理仍在本地（但状态可查询）

- [x] 已完成 — e11bd7e

---

### P0-5: 安全响应头与 CSP 策略

**问题**：缺少 Content-Security-Policy、X-Content-Type-Options、X-Frame-Options、Strict-Transport-Security 等安全响应头。

**修改范围**：
- 修改 `backend/app/__init__.py` — 注册安全头中间件
- 新增 `backend/app/middleware/security_headers.py`
- 修改 `web/index.html` — 添加 meta CSP（开发阶段宽松策略）

**实现要求**：
- 生产环境安全头：
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 0`（现代浏览器靠 CSP）
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`（生产）
  - `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self'`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- 通过环境变量 `SECURITY_HEADERS_ENABLED`（默认 true）控制开关
- 开发环境自动放宽 CSP（允许 eval 以支持 Vite HMR）

- [x] 已完成 — 394fba1

---
## P1：架构与测试（支撑规模化）

### P1-1: 统一后端框架 — Flask 到 FastAPI 迁移规划

**问题**：Flask v1 API 和 FastAPI v2 API 共存，维护两套中间件、错误处理、测试基础设施。

**修改范围**：
- 新增 `backend/REFACTOR_FRAMEWORK.md` — 迁移路线图文档

**实现要求**：
- 编写迁移路线图文档，列出每个 v1 模块迁移到 v2 的顺序和依赖关系
- 迁移顺序建议：auth → projects → api_test → web_test → perf_test → 其他
- 每个模块迁移后保持 v1 路由兼容（deprecated 标记），至少保留一个版本周期

> 注意：本任务只输出迁移规划文档，不执行实际迁移代码。

- [x] 已完成 — e057d4e

---

### P1-2: 补充后端集成测试

**问题**：42 个测试文件覆盖 26 个 API 模块，部分核心模块测试缺失或仅有单元测试。

**修改范围**：
- 新增 `backend/tests/test_web_test_api.py` — Web 测试模块 API 集成测试
- 新增 `backend/tests/test_perf_test_api.py` — 性能测试模块 API 集成测试
- 新增 `backend/tests/test_reports_api.py` — 报告模块 API 集成测试
- 新增 `backend/tests/test_visual_api.py` — 视觉回归模块 API 集成测试
- 新增 `backend/tests/test_rate_limit.py` — 限流中间件测试

**实现要求**：
- 使用现有的 `conftest.py` 中的 `client` fixture
- 每个模块测试覆盖：CRUD 完整流程 + 权限校验 + 边界条件 + 错误处理
- 测试命名规范：`test_{action}_{scenario}_{expected_result}`
- 至少补充 100+ 个测试用例
- 确保所有新增测试在 SQLite 模式下可运行（CI 环境）

- [x] 已完成 — 0510a52

---

### P1-3: 补充前端单元测试

**问题**：36 个页面组件仅有 17 个测试文件，覆盖率约 34%。

**修改范围**：
- 新增 `web/src/services/__tests__/api.test.ts`
- 新增 `web/src/services/__tests__/authService.test.ts`
- 新增 `web/src/services/__tests__/apiTestService.test.ts`
- 新增 `web/src/components/__tests__/GlobalSearch.test.tsx`
- 新增 `web/src/components/__tests__/NotificationPopover.test.tsx`
- 新增 `web/src/pages/__tests__/Login.test.tsx`
- 新增 `web/src/pages/__tests__/Register.test.tsx`

**实现要求**：
- 使用 Vitest + @testing-library/react（已有配置）
- mock axios 请求（使用 vi.mock）
- 测试核心交互：表单提交、错误提示、路由跳转、认证状态变更
- 每个文件至少 5 个测试用例

- [x] 已完成 — f6a7de0

---

### P1-4: E2E 测试框架搭建

**问题**：测试平台自身没有端到端测试。

**修改范围**：
- 新增 `e2e/` 目录（项目根目录）
- 新增 `e2e/playwright.config.ts`
- 新增 `e2e/tests/auth.spec.ts` — 登录/注册/登出流程
- 新增 `e2e/tests/api-test.spec.ts` — 接口测试核心流程
- 修改 `package.json` — 添加 e2e 脚本

**实现要求**：
- 使用 Playwright（项目已有依赖）
- 覆盖 3 个核心用户流程：认证、接口测试创建与执行、报告查看
- 测试数据通过 API seed，不依赖手动操作
- 配置 GitHub Actions 运行（可选，CI 阶段暂不强制）
- 提供 `npm run e2e` 和 `npm run e2e:ui` 命令

- [x] 已完成 — 319a53b

---

## P2：性能与可运维性（生产环境保障）

### P2-1: 多级缓存策略

**问题**：高频读取接口（Dashboard 统计、项目列表、环境列表）没有缓存，每次都查数据库。

**修改范围**：
- 新增 `backend/app/services/cache_service.py` — 缓存抽象层
- 修改 `backend/app/api/projects.py` — 项目列表缓存
- 修改 `backend/app/api/environments.py` — 环境列表缓存
- 修改 `backend/app/api/reports.py` — 报告统计缓存

**实现要求**：
- `CacheService` 提供 `get/set/delete/invalidate_pattern` 方法
- 生产使用 Redis，开发回退到 `cachetools.TTLCache`（内存）
- 项目列表 TTL 5 分钟，环境列表 TTL 2 分钟，Dashboard 统计 TTL 1 分钟
- 写操作后自动失效相关缓存（cache invalidation）
- 提供 `CACHE_ENABLED` 环境变量控制开关

- [x] 已完成 — 41ab2ef

---

### P2-2: 数据归档与清理策略

**问题**：测试执行产生大量数据（日志、截图、压测指标样本），缺乏生命周期管理。

**修改范围**：
- 新增 `backend/app/services/data_retention_service.py`
- 修改 `backend/app/scheduler.py` — 注册定时清理任务
- 新增 `backend/tests/test_data_retention.py`

**实现要求**：
- 可配置的保留策略（环境变量）：
  - 原始测试结果：保留 90 天（`RETENTION_RAW_DAYS=90`）
  - 截图/附件：保留 30 天（`RETENTION_ATTACHMENTS_DAYS=30`）
  - 汇总统计数据：保留 365 天（`RETENTION_SUMMARY_DAYS=365`）
- 定时任务每天凌晨 3:00 执行
- 删除前记录审计日志
- 支持手动触发清理（管理员 API）

- [x] 已完成 — 07523ae

---

### P2-3: Prometheus 告警规则

**问题**：有指标采集和 Grafana Dashboard，但没有告警规则。

**修改范围**：
- 新增 `infra/monitoring/alerts/alert_rules.yml`
- 新增 `infra/monitoring/alerts/alertmanager.yml`
- 修改 `docker-compose.prod.yml` — 添加 AlertManager 服务

**实现要求**：
- 核心告警规则：
  - API 5xx 错误率 > 5%（持续 5 分钟）
  - API P99 延迟 > 5 秒（持续 5 分钟）
  - Celery 任务失败率 > 10%（持续 10 分钟）
  - 数据库连接池耗尽
  - Redis 连接失败
  - 磁盘使用率 > 85%
- AlertManager 配置 Webhook 通知（预留钉钉/Slack/邮件模板）
- 提供文档说明如何配置通知渠道

- [x] 已完成 — dd4ab30

---

### P2-4: 前端大组件拆分

**问题**：核心页面组件过大，影响可维护性。

**修改范围**：
- 重构 `web/src/pages/api-test/ApiTestWorkspace.tsx`（2603 行）
- 重构 `web/src/pages/web-test/WebTestScripts.tsx`（1808 行）

**实现要求**：
- `ApiTestWorkspace.tsx` 拆分为：
  - `ApiTestWorkspace.tsx`（主容器，< 300 行）
  - `RequestEditor.tsx`（请求编辑区）
  - `ResponseViewer.tsx`（响应展示区）
  - `TestRunner.tsx`（测试执行与结果）
  - `EnvironmentSelector.tsx`（环境选择器）
- `WebTestScripts.tsx` 拆分为：
  - `WebTestScripts.tsx`（主容器，< 300 行）
  - `ScriptList.tsx`（脚本列表）
  - `ScriptEditor.tsx`（脚本编辑区）
  - `ScriptRunner.tsx`（脚本执行与日志）
- 拆分后功能不变，现有测试通过

- [x] 已完成 — c49b32f

---

## P3：产品功能完善（商业化能力）

### P3-1: 多租户资源配额

**问题**：缺乏租户级资源配额控制。

**修改范围**：
- 新增 `backend/app/models/quota.py`
- 修改 `backend/app/middleware/tenant.py`
- 新增 `backend/app/services/quota_service.py`
- 新增 `backend/tests/test_quota.py`

**实现要求**：
- `Quota` 模型：organization_id, resource_type, limit, used
- 资源类型：`projects`, `test_cases`, `parallel_executions`, `ai_calls_monthly`, `storage_mb`
- 默认配额（可按组织覆盖）：
  - 免费版：5 项目，100 用例，1 并行，100 AI 调用/月，500MB 存储
  - 专业版：50 项目，1000 用例，5 并行，5000 AI 调用/月，5GB 存储
  - 企业版：不限
- 在创建项目、执行测试、AI 调用前检查配额
- 提供管理员 API 查看/修改配额

- [x] 已完成 — ce146f0

---

### P3-2: 第三方集成 — Webhook 通知

**问题**：缺乏测试执行完成后的通知机制。

**修改范围**：
- 新增 `backend/app/services/notification_service.py`
- 修改 `backend/app/tasks.py` — 测试完成后触发通知
- 新增 `backend/app/models/notification_config.py`
- 新增 `backend/tests/test_notification.py`

**实现要求**：
- 支持的通知渠道：Webhook URL（通用）、钉钉、飞书、Slack
- 通知事件：测试执行完成、测试失败、告警触发
- 通知模板可配置（JSON 格式）
- 重试机制（3 次，指数退避）
- 通知日志记录

- [x] 已完成 — 11192bc

---

### P3-3: 无障碍访问改进（A11y）

**问题**：前端 ARIA 标记严重不足，不符合 WCAG 2.1 AA 标准。

**修改范围**：
- 修改 `web/src/layouts/MainLayout.tsx`
- 修改 `web/src/pages/Login.tsx`
- 修改 `web/src/pages/Dashboard.tsx`
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx`

**实现要求**：
- 主导航添加 `role="navigation"` 和 `aria-label`
- 表单元素关联 `<label>` 或 `aria-label`
- 按钮添加 `aria-label`（特别是图标按钮）
- 模态框添加 `role="dialog"` 和 `aria-modal="true"`
- 状态变更添加 `aria-live` 区域
- 键盘导航支持（Tab 顺序、Esc 关闭模态框）

- [x] 已完成 — 870f343

---

## P4：权限与认证体系（企业级必备）

### P4-1: RBAC 权限体系 — 角色与权限矩阵

**问题**：当前只有 owner/member 两种角色，无法满足企业客户对细粒度权限的需求。

**修改范围**：
- 新增 `backend/app/models/role.py` — Role 和 Permission 模型
- 修改 `backend/app/models/organization.py` — OrganizationMember 关联 Role
- 新增 `backend/app/services/permission_service.py` — 权限检查服务
- 新增 `backend/app/middleware/permission.py` — 权限校验装饰器
- 修改 `backend/app/api/organizations.py` — 角色管理 API
- 新增 `backend/tests/test_rbac.py`
- 新增 `web/src/hooks/usePermissions.ts` — 前端权限 Hook

**实现要求**：
- 定义角色：admin、manager、tester、viewer
- 定义权限资源：project、test_case、test_run、environment、report、ai_feature
- 定义权限操作：create、read、update、delete、execute、manage
- 角色-权限映射表（admin 全权限，viewer 只读）
- 提供 `@require_permission('project', 'create')` 装饰器
- API 查询时自动注入当前用户角色和权限
- 前端根据权限控制按钮可见性

- [x] 已完成

---

### P4-2: API Token 细粒度权限

**问题**：API Token 只有 read-only/read-write 粗粒度控制，CI/CD 场景需要限制到特定项目。

**修改范围**：
- 修改 `backend/app/models/api_token.py` — 扩展 permissions 和 scope 字段
- 新增 `backend/app/services/token_service.py` — Token 校验逻辑
- 修改 `backend/app/api/tokens.py` — Token 创建时支持项目绑定
- 新增 `backend/tests/test_token_scoped.py`

**实现要求**：
- Token 权限格式：`{"actions": ["read", "execute"], "project_ids": [1, 2]}`
- 空 project_ids 表示不限制项目
- Token 创建时必须指定权限范围
- 校验时检查 Token 是否有权操作目标项目

- [x] 已完成 — cdd2ec8

---

### P4-3: 登录失败锁定与密码策略

**问题**：缺乏暴力破解防护和密码复杂度要求。

**修改范围**：
- 修改 `backend/app/api/auth.py` — 登录失败计数、锁定逻辑
- 修改 `backend/app/models/user.py` — 添加 password_changed_at 字段
- 新增 `backend/app/services/password_policy.py` — 密码策略校验
- 新增 `backend/tests/test_login_lockout.py`

**实现要求**：
- 连续 5 次登录失败后锁定账户 15 分钟
- 密码策略：最少 8 位，至少包含大小写字母和数字
- 记录登录失败日志（IP、用户名、时间）
- 锁定状态下返回 423 状态码和锁定剩余时间

- [x] 已完成 — b12f7c5

---

## P5：测试管理能力（核心产品价值）

### P5-1: 测试计划 — 计划→轮次→执行

**问题**：只有单次执行，缺乏测试计划管理（回归测试、迭代测试等场景）。

**修改范围**：
- 新增 `backend/app/models/test_plan.py` — TestPlan、TestPlanRun、TestPlanCaseResult 模型
- 新增 `backend/app/services/plan_service.py` — 测试计划服务
- 新增 `backend/app/api/test_plans.py` — 测试计划 API（12 个端点）
- 修改 `backend/app/api/__init__.py` — 注册蓝图
- 修改 `backend/app/models/__init__.py` — 注册模型
- 新增 `backend/tests/test_test_plans.py`

**实现要求**：
- TestPlan：name、description、project_id、include_cases (JSON array of case IDs)、tags
- TestPlanRun：plan_id、status（pending/running/completed）、started_at、finished_at、pass_rate
- 支持从测试计划创建执行轮次
- 执行轮次中记录每个用例的执行结果
- 支持按轮次查看通过率趋势

- [x] 已完成 — 0033473

---

### P5-2: 缺陷管理联动 — Jira/飞书集成

**问题**：测试失败后无法自动创建缺陷，需要人工切换工具。

**修改范围**：
- 新增 `backend/app/services/issue_tracker_service.py` — 缺陷跟踪集成
- 新增 `backend/app/models/issue_link.py` — 缺陷关联模型
- 修改 `backend/app/models/__init__.py` — 注册模型
- 新增 `backend/tests/test_issue_tracker.py`

**实现要求**：
- 集成 Jira REST API（创建 Issue、关联 TestRun）
- 集成飞书项目（创建任务）
- 通过环境变量配置集成参数
- 支持手动和自动两种创建模式
- 在测试报告中展示关联的缺陷状态

- [x] 已完成 — c9c8fa6

---

### P5-3: 批量操作 — CSV/Excel 导入导出

**问题**：缺乏批量导入用例和导出报告的能力。

**修改范围**：
- 新增 `backend/app/services/import_export_service.py` — 导入导出服务
- 修改 `backend/app/api/api_test.py` — 添加 3 个导入端点
- 修改 `backend/app/api/reports.py` — 2 个报告导出端点
- 新增 `backend/tests/test_import_export.py`

**实现要求**：
- 支持 Postman Collection JSON 导入
- 支持 CSV 格式批量导入用例（name, method, url, headers, body, expected_status）
- 支持 Excel 格式导出测试报告
- 导入时校验格式、去重、返回导入结果统计
- 使用 openpyxl 处理 Excel，csv 标准库处理 CSV

- [x] 已完成 — ea484d1

---

### P5-4: 用例版本历史与变更追踪

**问题**：用例修改后无法查看历史版本和变更 diff。

**修改范围**：
- 新增 `backend/app/models/test_case_version.py` — 版本快照模型
- 修改 `backend/app/services/api_case_service.py` — 保存时创建版本
- 修改 `backend/app/api/api_test.py` — 版本历史 API（3 个端点）
- 新增 `backend/tests/test_case_versions.py`

**实现要求**：
- 每次修改用例时自动保存版本快照（前一版本）
- 版本记录：content (JSON)、created_by、created_at、change_summary
- API 支持查看用例版本列表和指定版本详情
- 支持两个版本之间的 diff 对比
- 最多保留最近 50 个版本（可配置）

- [x] 已完成 — 8508d00

---

## P6：报告与度量（决策支撑）

### P6-1: 质量趋势分析 — 按周/月的通过率趋势

**问题**：Dashboard 只有当前统计，缺乏历史趋势。

**修改范围**：
- 修改 `backend/app/api/reports.py` — 2 个趋势 API 端点
- 新增 `backend/app/services/trend_service.py` — 趋势计算服务
- 新增 `backend/tests/test_trend_service.py`
- 修改 `web/src/pages/Dashboard.tsx` — 趋势图表

**实现要求**：
- 按周/月聚合测试通过率趋势
- 按测试类型（API/Web/APP/Perf）分组统计
- 支持时间范围选择（最近 7 天/30 天/90 天）
- 前端使用 ECharts 折线图展示趋势
- API 返回格式：`[{date: "2026-01-01", api: 95.5, web: 88.2, perf: 92.0}]`

- [x] 已完成 — 3a6fc63

---

### P6-2: 报告导出 — PDF/Excel 格式

**问题**：无法导出测试报告为可分享的文件格式。

**修改范围**：
- 新增 `backend/app/services/export_service.py` — 导出服务（PDF + 增强 Excel）
- 修改 `backend/app/api/reports.py` — 2 个导出端点
- 新增 `backend/tests/test_export_service.py`

**实现要求**：
- PDF 报告：使用 ReportLab 生成
- 包含：项目信息、执行摘要、通过率、失败用例详情、执行时间
- Excel 报告：使用 openpyxl，包含多个 sheet（汇总、用例详情、性能指标）
- 支持自定义报告范围（按时间/按项目/按测试类型）

- [x] 已完成 — f8e34d4

---

### P6-3: 团队效能度量

**问题**：缺乏团队维度的效能分析。

**修改范围**：
- 新增 `backend/app/services/team_metrics_service.py` — 团队效能服务
- 修改 `backend/app/api/reports.py` — 团队效能 API
- 新增 `backend/tests/test_team_metrics.py`
- 新增 `web/src/pages/TeamMetrics.tsx` — 团队效能页面

**实现要求**：
- 指标：人均用例数、用例编写效率（个/周）、缺陷发现率、回归效率
- 按团队成员分组统计
- 时间范围可选
- 前端使用柱状图 + 表格展示

- [x] 已完成 — cc3128f

---

## P7：协作与工作流（团队协作）

### P7-1: 评论与讨论系统

**问题**：用例和执行结果缺乏评论讨论功能。

**修改范围**：
- 新增 `backend/app/models/comment.py` — Comment 模型
- 新增 `backend/app/services/comment_service.py` — 评论服务
- 新增 `backend/app/api/comments.py` — 评论 API（5 个端点）
- 修改 `backend/app/api/__init__.py` — 注册蓝图
- 修改 `backend/app/models/__init__.py` — 注册模型
- 新增 `backend/tests/test_comments.py`
- 新增前端组件 `web/src/components/CommentSection.tsx`

**实现要求**：
- 支持在用例、执行结果上添加评论
- 支持 @提及用户（发送通知）
- 评论支持 Markdown 格式
- 评论编辑和删除（仅限作者和管理员）
- 评论按时间排序，支持分页

- [x] 已完成 — 31bc5d5

---

### P7-2: 操作审计日志完善

**问题**：有 AuditLog 模型但未广泛接入，无法追溯谁在什么时间做了什么。

**修改范围**：
- 新增 `backend/app/middleware/audit.py` — @audit_action 装饰器
- 增强 `backend/app/api/audit_logs.py` — 查询/详情/统计 API
- 修改 `backend/app/api/__init__.py` — 注册蓝图
- 新增 `backend/tests/test_audit_logs.py`

**实现要求**：
- 记录：user_id、action（create/update/delete/execute）、resource_type、resource_id、changes (JSON diff)
- 自动记录所有写操作（通过装饰器）
- 审计日志不可修改/删除
- 提供查询 API（按用户、时间、资源类型筛选）
- 保留期 365 天

- [x] 已完成 — 2303714

---

## P8：平台化能力（扩展性）

### P8-1: 插件/扩展体系基础架构

**问题**：所有功能硬编码，无法扩展第三方集成。

**修改范围**：
- 新增 `backend/app/plugins/__init__.py` — 插件模块入口
- 新增 `backend/app/plugins/base.py` — PluginBase 抽象基类
- 新增 `backend/app/plugins/registry.py` — PluginRegistry 注册表
- 新增 `backend/app/plugins/custom/` — 自定义插件目录
- 新增 `backend/app/plugins/custom/slack_notify.py` — Slack 示例插件
- 修改 `backend/app/__init__.py` — 插件系统初始化
- 新增 `backend/tests/test_plugins.py`

**实现要求**：
- PluginBase 接口：name、version、on_event()、get_routes()
- 插件注册表：自动扫描 plugins/ 目录下的插件
- 事件系统：test_completed、test_failed、user_created 等事件钩子
- 插件可通过配置启用/禁用
- 示例插件：Slack 通知插件

- [x] 已完成 — e12cdf1

---

### P8-2: OpenAPI 文档自动生成

**问题**：API 文档不完整，缺乏交互式文档。

**修改范围**：
- 新增 `backend/app/schemas/common.py` — 通用 Pydantic Schema
- 增强 `backend/app/api/v2/openapi_docs.py` — 认证说明 + Schema 增强
- 新增 `backend/tests/test_openapi_docs.py`

**实现要求**：
- 所有 v2 端点都有 Pydantic 请求/响应 schema
- 自动生成 OpenAPI 3.0 文档
- 提供 /docs (Swagger UI) 和 /redoc 端点
- 包含认证说明（JWT Bearer + API Token）
- 包含请求/响应示例

- [x] 已完成 — 3300e9c

---

### P8-3: Python SDK

**问题**：缺乏 SDK，CI/CD 集成只能手动调用 API。

**修改范围**：
- 新增 `sdk/python/fullscopetest/__init__.py`
- 新增 `sdk/python/fullscopetest/client.py` — FullScopeTestClient API 客户端
- 新增 `sdk/python/fullscopetest/cli.py` — fst CLI 命令
- 新增 `sdk/python/setup.py` — 打包配置
- 新增 `sdk/python/tests/test_client.py`

**实现要求**：
- 提供 FullScopeTestClient 类
- 支持：创建测试运行、查询结果、创建用例、管理项目
- 支持 API Token 和 JWT 两种认证方式
- 自动重试和超时处理
- 提供 CLI 命令：`fst run --project-id 1 --type api`

- [x] 已完成 — b8e5930

---

## P9：运维与可靠性（生产保障）

### P9-1: 数据备份策略

**问题**：缺乏自动备份和恢复机制。

**修改范围**：
- 新增 `scripts/backup.sh` — 备份脚本（PostgreSQL + Redis + 文件存储）
- 新增 `docs/BACKUP.md` — 备份恢复完整指南
- 新增 `backend/tests/test_backup.py`

**实现要求**：
- PostgreSQL：每日 pg_dump 全量备份，保留 7 天
- Redis：每日 RDB 快照备份
- 文件存储（uploads/、reports/）：rsync 到备份目录
- 备份文件压缩和日期命名
- 提供一键恢复脚本
- 通过 cron 或 Celery Beat 调度

- [x] 已完成 — 8e45a34

---

### P9-2: 健康检查增强

**问题**：健康检查只有基础端点，缺乏依赖检查。

**修改范围**：
- 修改 `backend/app/core/health.py` — 增强健康检查（K8s 兼容）
- 修改 `backend/tests/test_health.py` — 增强测试

**实现要求**：
- `/health/live` — 存活探针（返回 200）
- `/health/ready` — 就绪探针（检查 DB、Redis、Celery 连接）
- 返回各组件状态：`{status: "ok", checks: {database: "ok", redis: "ok", celery: "degraded"}}`
- 任一关键组件失败返回 503
- 支持 Kubernetes liveness/readiness probe 格式

- [x] 已完成 — d6e8d87

---

## 进度跟踪

| 任务 | 状态 | Commit |
|------|------|--------|
| P0-1 SSRF 防护 | 已完成 | 51684a4 |
| P0-2 脚本沙箱隔离 | 已完成 | 282cca3 |
| P0-3 JWT Token 安全 | 已完成 | 4f01c64 |
| P0-4 运行状态外部化 | 已完成 | e11bd7e |
| P0-5 安全响应头 | 已完成 | 394fba1 |
| P1-1 框架迁移规划 | 已完成 | e057d4e |
| P1-2 后端集成测试 | 已完成 | 0510a52 |
| P1-3 前端单元测试 | 已完成 | f6a7de0 |
| P1-4 E2E 测试框架 | 已完成 | 319a53b |
| P2-1 多级缓存 | 已完成 | 41ab2ef |
| P2-2 数据归档 | 已完成 | 07523ae |
| P2-3 告警规则 | 已完成 | dd4ab30 |
| P2-4 大组件拆分 | 已完成 | c49b32f |
| P3-1 多租户配额 | 已完成 | ce146f0 |
| P3-2 Webhook 通知 | 已完成 | 11192bc |
| P3-3 A11y 改进 | 已完成 | 870f343 |
| P4-1 RBAC 权限体系 | 已完成 | 262a3c6 |
| P4-2 API Token 细粒度权限 | 已完成 | cdd2ec8 |
| P4-3 登录失败锁定与密码策略 | 已完成 | b12f7c5 |
| P5-1 测试计划 | 已完成 | 0033473 |
| P5-2 缺陷管理联动 | 已完成 | c9c8fa6 |
| P5-3 批量操作导入导出 | 已完成 | ea484d1 |
| P5-4 用例版本历史 | 已完成 | 8508d00 |
| P6-1 质量趋势分析 | 已完成 | 3a6fc63 |
| P6-2 报告导出 PDF/Excel | 已完成 | f8e34d4 |
| P6-3 团队效能度量 | 已完成 | cc3128f |
| P7-1 评论与讨论系统 | 已完成 | 31bc5d5 |
| P7-2 操作审计日志完善 | 已完成 | 2303714 |
| P8-1 插件扩展体系 | 已完成 | e12cdf1 |
| P8-2 OpenAPI 文档自动生成 | 已完成 | 3300e9c |
| P8-3 Python SDK | 已完成 | b8e5930 |
| P9-1 数据备份策略 | 已完成 | 8e45a34 |
| P9-2 健康检查增强 | 已完成 | d6e8d87 |

---

---

# 第二阶段：前端覆盖补全 + 商业化就绪

> 以下任务源自「后端功能 vs 前端实现」深度 Gap 分析。
> 核心发现：后端 159 个 API 端点中，前端仅消费 67 个（42%），58% 的后端能力在前端不可见。
> 后端 37 个服务中 14 个（38%）在前端完全未被使用；34 个数据模型中 13 个（38%）无前端管理界面。

---

## ⚠️ 全局设计规范（所有 P10/P11/P12 前端任务必须遵守）

> 本规范适用于第二阶段所有涉及前端开发的任务。新增页面/组件必须与现有页面保持视觉一致，不得引入与现有设计语言冲突的元素。

### 1. 色彩系统 — 严格使用已有 CSS 变量

**现有主题色板（`main.tsx` + `index.css`）**：

| 变量 | 色值 | 用途 |
|------|------|------|
| `--fst-primary` | `#2D6A64` | 主色调（深青绿） |
| `--fst-primary-light` | `#4A9E96` | 主色调亮色 |
| `--fst-primary-dark` | `#1A4A45` | 主色调暗色 |
| `--fst-primary-container` | `#D4EDE8` | 主色容器背景 |
| `--fst-secondary` | `#629B95` | 次要色（中青绿） |
| `--fst-tertiary` | `#D4B483` | 第三色（暖金） |
| `--fst-tertiary-light` | `#F0DFC4` | 第三色亮色 |
| `--fst-success` | `#2D6A64` | 成功 |
| `--fst-warning` | `#D4B483` | 警告 |
| `--fst-error` | `#C75450` | 错误 |
| `--fst-info` | `#5B8FB9` | 信息 |
| Ant Design `colorPrimary` | `#3D6E66` | Ant 组件主色 |
| Ant Design `colorSuccess` | `#2F8F6B` | Ant 成功色 |
| Ant Design `colorWarning` | `#D7B56D` | Ant 警告色 |
| Ant Design `colorError` | `#D24C3F` | Ant 错误色 |

**硬性禁止**：
- ❌ 禁止使用蓝紫色系（`#722ed1`, `#9254de`, `#b37feb`, `#667eea`, `#764ba2`, `#6366f1`, `#8b5cf6`, `#a78bfa` 等一切紫/靛/蓝紫渐变色）
- ❌ 禁止使用霓虹色/荧光色（`#00f5ff`, `#ff00ff`, `#00ff00` 等）
- ❌ 禁止使用 AI 产品常见的渐变色方案（如 OpenAI 的渐变紫、Claude 的渐变橙棕、Midjourney 的渐变蓝紫）
- ❌ 禁止在按钮、卡片、背景上使用 `linear-gradient` 渐变，除非现有页面已有相同用法（如登录页背景）
- ✅ 所有颜色必须引用 `--fst-*` CSS 变量或 Ant Design 主题 token
- ✅ 图表配色统一使用：`#2D6A64`（主）、`#629B95`（次）、`#D4B483`（三）、`#5B8FB9`（信息）、`#C75450`（错误）
- ✅ 如需额外颜色，仅可从上述色板中派生（调整透明度/明度），不得引入全新色相

### 2. 文案风格 — 禁止 AI 味道的 Emoji 和话术

**硬性禁止**：
- ❌ 禁止在页面标题、按钮文案、提示文字中使用 Emoji 表情（如 🤖🚀💡✨🎯🔥⚡🧠💬🎨🔍📊📋🛠🔧🎉💻🌟⭐ 等）
- ❌ 禁止使用 AI 产品常见话术：
  - "智能为您..."、"AI 赋能..."、"一键生成..."
  - "正在思考中..."、"让我来帮您..."
  - "✨ 已为您生成..."、"🎯 精准匹配..."
  - "🚀 快速开始..."、"💡 智能推荐..."
- ✅ 使用朴素、专业的中文表达：
  - "生成测试用例" 而非 "✨ 智能生成测试用例 🤖"
  - "分析中..." 而非 "🧠 AI 正在深度分析..."
  - "已完成" 而非 "🎉 太棒了！已完成 ✨"
  - "建议保留此用例" 而非 "💡 智能推荐保留此用例"
- ✅ Loading/状态文案简洁：使用 "加载中..."、"提交中..."、"执行中..."
- ✅ 按钮文案直接描述动作：使用 "创建"、"编辑"、"删除"、"运行"、"导出"

### 3. 图标使用 — 保持 Ant Design Icons 一致性

- ✅ 统一使用 `@ant-design/icons` 图标库
- ❌ 禁止引入其他图标库（如 Font Awesome、Material Icons、Lucide 等）
- ❌ 禁止使用自定义 SVG 图标（除非现有页面已有相同用法，如 Logo）
- ✅ 功能图标参考现有用法：
  - 创建/新增：`PlusOutlined`
  - 编辑：`EditOutlined`
  - 删除：`DeleteOutlined`
  - 设置：`SettingOutlined`
  - 搜索：`SearchOutlined`
  - 刷新：`ReloadOutlined`
  - 导出：`ExportOutlined`
  - 导入：`ImportOutlined`
  - 运行/执行：`PlayCircleOutlined` 或 `ThunderboltOutlined`
  - 查看：`EyeOutlined`
  - 成功：`CheckCircleOutlined`
  - 失败：`CloseCircleOutlined`
  - 警告：`ExclamationCircleOutlined`
  - 信息：`InfoCircleOutlined`

### 4. 布局与间距 — 遵循现有页面结构

- ✅ 页面容器使用 `padding: 24px`（与 Dashboard、Reports 等页面一致）
- ✅ 卡片间距使用 `margin-bottom: 16px` 或 `gap: 16px`
- ✅ 页面标题使用 `Typography.Title level={4}` 或 `h4`，不使用过大标题
- ✅ 表格使用 Ant Design `Table` 组件，配置与现有页面一致（分页、排序、筛选）
- ✅ 表单使用 Ant Design `Form` 组件，`labelCol={{ span: 6 }}` / `wrapperCol={{ span: 18 }}` 布局
- ✅ 弹窗使用 Ant Design `Modal` 组件，宽度参考现有弹窗（480px-720px）
- ✅ 按钮样式：主按钮使用 `type="primary"`，危险操作使用 `danger`，禁用自定义按钮样式
- ✅ 卡片使用 Ant Design `Card` 组件，圆角 `borderRadius: 12px`（与 `--fst-radius-md` 一致）

### 5. 状态与反馈 — 保持现有交互模式

- ✅ 操作成功：`message.success()`，文案简洁（"创建成功"、"删除成功"）
- ✅ 操作失败：`message.error()`，展示后端返回的错误信息
- ✅ 二次确认：使用 `Popconfirm` 或 `Modal.confirm`，文案格式："确定要删除 xxx 吗？此操作不可恢复。"
- ✅ Loading 状态：使用 `Spin` 组件包裹内容区，或按钮 `loading` 属性
- ✅ 空状态：使用 Ant Design `Empty` 组件，配合引导文案

### 6. 代码实现要求

- ✅ 优先使用现有组件和工具函数，避免重复造轮子
- ✅ 样式优先使用 CSS 变量和 Ant Design token，减少内联 style
- ✅ 如需自定义样式，使用 CSS Modules 或 `index.css` 中的 BEM 命名（`fst-*` 前缀）
- ✅ 图表组件统一使用 `echarts-for-react`，配色遵循上述色板
- ✅ 服务层调用使用现有的 `api` 实例（`web/src/services/api.ts`），保持请求/响应处理一致

---

## P10：前端覆盖补全 — 后端已有能力的 UI 落地（零后端开发）

> 本阶段所有任务**仅涉及前端开发**，后端 API 已全部就绪，目标是将后端 58% 的"隐形能力"变为用户可见功能。

### P10-1: 组织/多租户管理页面

**问题**：后端已实现 10 个组织管理 API（组织 CRUD、成员管理、角色管理、权限分配、角色 CRUD），前端仅在 `usePermissions.ts` 中调用了 1 个权限查询接口，多租户功能完全不可用。

**修改范围**：
- 新增 `web/src/pages/organizations/OrganizationList.tsx` — 组织列表页
- 新增 `web/src/pages/organizations/OrganizationDetail.tsx` — 组织详情页（成员 + 角色 Tab）
- 新增 `web/src/pages/organizations/MemberManagement.tsx` — 成员管理组件
- 新增 `web/src/pages/organizations/RoleManagement.tsx` — 角色管理组件
- 新增 `web/src/pages/organizations/PermissionConfig.tsx` — 权限配置组件
- 新增 `web/src/services/organizationService.ts` — 组织服务层
- 修改 `web/src/App.tsx` — 注册组织管理路由
- 修改 `web/src/layouts/MainLayout.tsx` — 侧边栏添加组织管理入口
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 组织列表：展示组织名称、成员数、创建时间，支持创建/编辑/删除
- 成员管理：邀请成员（输入用户名/邮箱）、移除成员、修改角色
- 角色管理：角色列表（admin/manager/tester/viewer）、每个角色的权限矩阵展示
- 权限配置：资源类型 × 操作类型的权限矩阵表格，支持自定义角色
- 对接后端 API：
  - `GET/POST /organizations` — 组织 CRUD
  - `GET/POST/PUT/DELETE /organizations/:id/members/:uid` — 成员管理
  - `GET/POST/PUT/DELETE /organizations/:id/roles/:rid` — 角色管理
  - `GET /organizations/:id/my-permissions` — 当前用户权限
- 组织切换器集成到顶栏（类似 GitHub 的组织切换下拉）
- 权限不足时显示无权限提示，隐藏操作按钮

- [x] 已完成 — 7ef4cf8

---

### P10-2: 审计日志页面

**问题**：后端已实现 3 个审计日志 API（日志列表查询、日志详情、日志统计），前端完全未调用，企业合规性功能缺失。

**修改范围**：
- 新增 `web/src/pages/AuditLogs.tsx` — 审计日志页面
- 新增 `web/src/services/auditLogService.ts` — 审计日志服务层
- 修改 `web/src/App.tsx` — 注册审计日志路由
- 修改 `web/src/layouts/MainLayout.tsx` — 侧边栏添加审计日志入口（仅 admin 可见）
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 日志列表：表格展示操作人、操作类型、资源类型、资源 ID、时间、IP 地址
- 筛选条件：操作类型（create/update/delete/execute）、资源类型、操作人、时间范围
- 日志详情弹窗：展示完整变更内容（JSON diff 格式高亮新增/修改/删除字段）
- 统计图表：按操作类型饼图 + 按天操作趋势折线图（调用 `/audit-logs/stats`）
- 日志只读，不可编辑/删除
- 对接后端 API：
  - `GET /audit-logs` — 日志列表（支持筛选/分页）
  - `GET /audit-logs/:id` — 日志详情
  - `GET /audit-logs/stats` — 日志统计
- 默认按时间倒序排列，支持分页

- [x] 已完成 — eaf71ca

---

### P10-3: API Token 管理页面

**问题**：后端已实现 3 个 API Token 管理 API（创建/删除/验证），前端无管理界面，CI/CD 集成的 Token 无法通过 UI 管理。

**修改范围**：
- 新增 `web/src/pages/ApiTokens.tsx` — Token 管理页面
- 新增 `web/src/services/tokenService.ts` — Token 服务层
- 修改 `web/src/App.tsx` — 注册 Token 管理路由
- 修改 `web/src/layouts/MainLayout.tsx` — 侧边栏或设置页添加入口
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- Token 列表：表格展示 Token 名称、权限范围、创建时间、最后使用时间、状态
- 创建 Token 弹窗：
  - 名称输入
  - 权限选择（read-only / read-write）
  - 项目绑定（可选，多选项目列表）
  - 创建后显示一次性 Token 值（带复制按钮，关闭后不再显示）
- 删除 Token：二次确认弹窗
- 对接后端 API：
  - `GET /tokens` — Token 列表
  - `POST /tokens` — 创建 Token
  - `DELETE /tokens/:id` — 删除 Token
  - `POST /tokens/validate` — 验证 Token
- 安全提示：Token 创建后仅显示一次，请妥善保存

- [x] 已完成 — f46a69e

---

### P10-4: 测试计划管理页面

**问题**：后端已实现 7 个测试计划 API（计划 CRUD、运行管理、运行结果、趋势），前端完全未调用，无法组织和编排测试套件。

**修改范围**：
- 新增 `web/src/pages/TestPlans.tsx` — 测试计划列表页
- 新增 `web/src/pages/TestPlanDetail.tsx` — 计划详情页（运行历史 + 用例列表）
- 新增 `web/src/pages/TestPlanRunDetail.tsx` — 运行详情页
- 新增 `web/src/services/testPlanService.ts` — 测试计划服务层
- 修改 `web/src/App.tsx` — 注册测试计划路由
- 修改 `web/src/layouts/MainLayout.tsx` — 侧边栏添加测试计划入口
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 计划列表：卡片或表格展示计划名称、关联用例数、最近运行状态、通过率
- 创建/编辑计划：
  - 计划名称、描述
  - 用例选择器（从用例集中勾选用例，支持全选/搜索/按标签筛选）
  - 标签管理
- 计划详情：
  - 用例列表 Tab（展示包含的用例）
  - 运行历史 Tab（展示每次运行的状态、通过率、耗时）
  - 趋势图 Tab（通过率折线图，调用 `/test-plans/:id/trend`）
- 创建运行：点击"运行"按钮，创建新的 TestPlanRun
- 运行详情：展示每个用例的执行结果（通过/失败/跳过）
- 对接后端 API：
  - `GET/POST /test-plans` — 计划 CRUD
  - `GET/PUT/DELETE /test-plans/:id` — 计划详情/编辑/删除
  - `POST /test-plans/:id/runs` — 创建运行
  - `GET /test-plans/:id/runs` — 运行列表
  - `GET /test-plan-runs/:id` — 运行详情
  - `GET /test-plan-runs/:id/case-results` — 用例结果
  - `GET /test-plans/:id/trend` — 趋势数据

- [x] 已完成 — 89211a6

---

### P10-5: 质量门禁管理页面

**问题**：后端已实现 4 个质量门禁 API（门禁 CRUD、评估触发、评估历史），前端完全未调用，无法配置自动化质量标准。

**修改范围**：
- 新增 `web/src/pages/QualityGates.tsx` — 质量门禁管理页面
- 新增 `web/src/services/qualityGateService.ts` — 质量门禁服务层
- 修改 `web/src/App.tsx` — 注册质量门禁路由
- 修改 `web/src/layouts/MainLayout.tsx` — 侧边栏添加入口
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 门禁列表：表格展示门禁名称、规则条件、最近评估结果、状态
- 创建/编辑门禁：
  - 门禁名称
  - 规则条件配置（通过率 ≥ X%、失败用例数 ≤ N、P95 响应时间 ≤ Yms 等）
  - 关联项目/测试计划
- 评估历史：展示每次评估的时间、结果（通过/不通过）、各项指标详情
- 手动触发评估按钮（调用 `/quality-gates/:id/evaluate`）
- 对接后端 API：
  - `GET/POST /quality-gates` — 门禁 CRUD
  - `GET/PUT/DELETE /quality-gates/:id` — 门禁详情/编辑/删除
  - `POST /quality-gates/:id/evaluate` — 触发评估
  - `GET /quality-gates/:id/evaluations` — 评估历史
- 评估结果用绿色（通过）/红色（不通过）Tag 展示

- [ ] 未开始

---

### P10-6: GitHub 集成管理页面

**问题**：后端已实现 8 个 GitHub 集成 API（OAuth 授权/回调/配置/状态/解绑 + Check Run 创建/更新/完成），前端完全未调用，CI/CD 联动能力被埋没。

**修改范围**：
- 新增 `web/src/pages/Integrations.tsx` — 集成管理页面（可扩展其他集成）
- 新增 `web/src/services/integrationService.ts` — 集成服务层
- 修改 `web/src/App.tsx` — 注册集成管理路由
- 修改 `web/src/layouts/MainLayout.tsx` — 设置页添加集成管理入口
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 集成卡片列表：GitHub、GitLab（预留）、Jira（预留）
- GitHub 集成卡片：
  - 未授权状态：显示"连接 GitHub"按钮，点击跳转 OAuth 授权页
  - 已授权状态：显示绑定的 GitHub 用户名、仓库信息、"断开连接"按钮
  - Check Run 配置：启用/禁用 PR 状态回写
- 对接后端 API：
  - `GET /integrations/github/status` — 获取集成状态
  - `GET /integrations/github/auth` — 获取授权 URL
  - `GET /integrations/github/callback` — 处理回调
  - `GET /integrations/github/config` — 获取配置
  - `POST /integrations/github/unbind` — 断开连接
- OAuth 回调处理：授权成功后刷新页面状态

- [ ] 未开始

---

### P10-7: 评论系统组件

**问题**：后端已实现 3 个评论 API（评论 CRUD，支持多资源类型），前端完全未调用，团队协作功能缺失。

**修改范围**：
- 新增 `web/src/components/CommentSection.tsx` — 评论区组件
- 新增 `web/src/services/commentService.ts` — 评论服务层
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 用例详情中嵌入评论区
- 修改 `web/src/pages/Reports.tsx` — 测试报告中嵌入评论区
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 评论区组件：可复用，接收 `resourceType` 和 `resourceId` 两个 props
- 评论列表：按时间倒序展示，显示用户头像、用户名、评论时间、评论内容
- 评论输入：Markdown 编辑器（简单版本，支持基本语法），发送按钮
- 评论操作：编辑（仅作者）、删除（仅作者和管理员），二次确认删除
- 支持 @提及用户（输入 @ 弹出用户列表）
- 对接后端 API：
  - `GET /comments/:resourceType/:resourceId` — 获取评论列表
  - `POST /comments` — 发表评论
  - `PUT /comments/:id` — 编辑评论
  - `DELETE /comments/:id` — 删除评论
- 分页加载（每页 20 条，滚动加载更多）

- [ ] 未开始

---

### P10-8: API 导入功能 UI

**问题**：后端已实现 Postman 导入、CSV 导入、模板下载 3 个 API，前端无导入 UI，用户无法从其他工具迁移数据。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 添加导入按钮和弹窗
- 新增 `web/src/pages/api-test/components/ImportModal.tsx` — 导入弹窗组件
- 修改 `web/src/services/apiTestService.ts` — 添加导入相关 API 调用
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 导入按钮位置：用例集管理页面顶部工具栏
- 导入弹窗：
  - 导入类型选择：Postman Collection (JSON) / CSV 文件
  - 文件上传区域（拖拽上传 + 点击选择）
  - CSV 模板下载链接（调用 `/api-test/import/template`）
  - 导入预览：解析后展示将导入的用例数量和列表
  - 目标用例集选择（导入到现有集合或新建集合）
- 导入结果：成功数量、失败数量、失败原因列表
- 对接后端 API：
  - `POST /api-test/import/postman` — Postman 导入
  - `POST /api-test/import/csv` — CSV 导入
  - `GET /api-test/import/template` — 下载 CSV 模板
- 文件大小限制提示（建议 < 10MB）

- [ ] 未开始

---

### P10-9: API Mock 服务配置 UI

**问题**：后端已实现 Mock 服务 API（支持响应码/Body/Header/延迟配置），前端类型定义中已有 mock 相关字段但无配置 UI。

**修改范围**：
- 修改 `web/src/pages/api-test/RequestEditor.tsx` — 添加 Mock 配置面板
- 修改 `web/src/pages/api-test/components/SaveCaseModal.tsx` — 保存用例时包含 Mock 配置
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- Mock 配置面板位置：请求编辑器的 Tab 页（与 Headers、Body、断言等同级）
- 配置项：
  - 启用/禁用 Mock 开关
  - Mock 响应状态码（下拉选择 200/201/400/401/403/404/500 等）
  - Mock 响应 Headers（Key-Value 编辑器）
  - Mock 响应 Body（JSON 编辑器，Monaco Editor）
  - Mock 延迟（毫秒输入框，模拟网络延迟）
- 保存时将 Mock 配置一起提交
- Mock 状态标识：用例列表中显示 Mock 标签（绿色 "Mock" Tag）

- [ ] 未开始

---

### P10-10: 用例版本管理与 Diff 视图

**问题**：后端已实现 3 个版本管理 API（版本列表、版本详情、版本 diff），前端无版本管理 UI，无法查看用例变更历史。

**修改范围**：
- 新增 `web/src/pages/api-test/components/VersionHistoryDrawer.tsx` — 版本历史抽屉
- 新增 `web/src/pages/api-test/components/VersionDiffView.tsx` — 版本 Diff 视图组件
- 修改 `web/src/pages/api-test/RequestEditor.tsx` — 添加版本历史入口按钮
- 修改 `web/src/services/apiTestService.ts` — 添加版本相关 API 调用
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 版本历史入口：用例编辑器工具栏的"历史"按钮
- 版本历史抽屉：
  - 版本列表（按时间倒序，显示版本号、修改人、修改时间、变更摘要）
  - 点击版本查看详情
  - 选择两个版本进行 Diff 对比
- Diff 视图：
  - 左右分屏展示两个版本
  - JSON Diff 高亮（新增绿色、删除红色、修改黄色）
  - 支持折叠未变更的字段
- 对接后端 API：
  - `GET /api-test/cases/:id/versions` — 版本列表
  - `GET /api-test/versions/:id` — 版本详情
  - `GET /api-test/versions/diff?v1=xx&v2=xx` — 版本 Diff

- [ ] 未开始

---

### P10-11: 报告多格式导出按钮

**问题**：后端支持 Excel/PDF/CSV/HTML 四种格式导出，前端仅有 JSON 导出，用户无法下载离线报告。

**修改范围**：
- 修改 `web/src/pages/Reports.tsx` — 添加导出下拉菜单
- 修改 `web/src/pages/test-reports` 相关页面 — 添加导出按钮
- 修改 `web/src/services/reportService.ts` — 添加多格式导出 API 调用
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 导出按钮位置：报告页面右上角，下拉菜单形式
- 导出格式选项：
  - PDF 报告（调用 `/reports/:id/export`）
  - Excel 报告（调用 `/reports/export/excel`）
  - CSV 数据（调用 `/test-runs/:id/export/csv`）
- 导出时显示 Loading 状态
- 文件下载后自动命名（格式：`报告名称_日期.扩展名`）
- 对接后端 API：
  - `GET /reports/:id/export` — 导出报告（JSON/HTML）
  - `GET /reports/export/excel` — 导出 Excel
  - `GET /test-runs/:id/export/csv` — 导出 CSV
  - `GET /test-runs/:id/export/excel` — 导出 Excel
  - `GET /test-runs/:id/export/pdf` — 导出 PDF

- [x] 已完成 — 1beb473

---

### P10-12: 视觉回归基线管理 UI

**问题**：后端已实现基线列表、删除基线、历史趋势 API，前端仅有历史页面和差异查看组件，缺少独立的基线管理入口。

**修改范围**：
- 修改 `web/src/pages/VisualRegressionHistory.tsx` — 增强基线管理功能
- 新增 `web/src/pages/VisualRegressionBaselines.tsx` — 基线管理页面（可选，或合并到历史页）
- 修改 `web/src/services/webTestService.ts` — 补充基线管理 API 调用
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 基线管理功能：
  - 基线列表（按用例分组，展示基准截图缩略图、创建时间、状态）
  - 删除基线按钮（二次确认）
  - 批准新基线（从差异对比页面跳转）
- 历史趋势增强：
  - 差异百分比折线图（已有）
  - 版本截图缩略图时间线
- 对接后端 API：
  - `GET /visual/baselines/:test_case_id` — 获取基线列表
  - `DELETE /visual/baselines/:id` — 删除基线
  - `POST /visual/baselines/:id/approve` — 批准基线
  - `GET /visual/history/:test_case_id` — 历史趋势
  - `GET /visual/diffs/:test_run_id` — 差异列表

- [ ] 未开始

---

### P10-13: 触发规则配置页面

**问题**：后端已实现 3 个触发规则 API（规则 CRUD + 触发执行），前端完全未调用，事件驱动测试无法配置。

**修改范围**：
- 新增 `web/src/pages/TriggerRules.tsx` — 触发规则管理页面
- 新增 `web/src/services/triggerRuleService.ts` — 触发规则服务层
- 修改 `web/src/App.tsx` — 注册路由
- 修改 `web/src/layouts/MainLayout.tsx` — 添加入口（可合并到 CI/CD 页面 Tab）
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 触发规则列表：规则名称、触发条件、关联测试目标、状态（启用/禁用）、最近触发时间
- 创建/编辑规则：
  - 规则名称
  - 触发条件（Webhook 接收 / 定时 Cron / 代码推送）
  - 关联测试目标（API 用例集 / Web 脚本 / 性能场景）
- 启用/禁用开关
- 对接后端 API：
  - `GET/POST /trigger-rules` — 规则 CRUD
  - `GET/PUT/DELETE /trigger-rules/:id` — 规则详情/编辑/删除
  - `POST /triggers/:token` — 触发执行

- [ ] 未开始

---

### P10-14: 通知渠道配置页面

**问题**：后端已有 NotificationConfig 模型和通知服务，前端无配置 UI，告警通知渠道无法配置。

**修改范围**：
- 新增 `web/src/pages/NotificationSettings.tsx` — 通知配置页面
- 新增 `web/src/services/notificationService.ts` — 通知服务层
- 修改 `web/src/pages/Settings.tsx` — 添加通知配置 Tab
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 通知渠道列表：渠道名称、类型（Webhook/钉钉/飞书/Slack/邮件）、状态
- 创建/编辑渠道：
  - 渠道类型选择
  - Webhook URL 输入
  - 测试发送按钮（验证配置是否正确）
- 通知事件配置：
  - 测试执行完成 → 选择通知渠道
  - 测试失败 → 选择通知渠道
  - 告警触发 → 选择通知渠道
- 对接后端 API：
  - 通知配置 CRUD（复用后端 notification 相关 API）
  - 测试通知发送

- [ ] 未开始

---

### P10-15: 团队效能指标页面

**问题**：后端已实现团队指标 API，前端完全未调用，无法度量团队测试效能。

**修改范围**：
- 新增 `web/src/pages/TeamMetrics.tsx` — 团队效能指标页面
- 新增 `web/src/services/teamMetricsService.ts` — 团队指标服务层
- 修改 `web/src/App.tsx` — 注册路由
- 修改 `web/src/layouts/MainLayout.tsx` — 报告模块下添加入口
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 指标概览卡片：人均用例数、用例编写效率（个/周）、缺陷发现率、回归效率
- 成员排行表格：按用例编写量、执行量、发现缺陷数排序
- 趋势图表：按周/月的团队效能趋势折线图
- 时间范围选择器：最近 7 天/30 天/90 天
- 对接后端 API：
  - `GET /reports/team-metrics` — 团队效能指标
- 使用 ECharts 柱状图 + 表格展示

- [ ] 未开始

---

### P10-16: 语义去重入口

**问题**：后端已实现 AI 语义去重服务（`/ai/find-duplicates`），前端仅在 AI 统计看板中作为统计维度提到，无独立操作入口。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 添加"智能去重"按钮
- 新增 `web/src/pages/api-test/components/DedupResultModal.tsx` — 去重结果弹窗
- 修改 `web/src/services/apiTestService.ts` — 添加去重 API 调用
- 修改 `web/src/i18n/locales/zh.json` + `en.json` — 国际化文案

**实现要求**：
- 入口位置：用例集管理页面工具栏，"智能去重"按钮
- 去重结果弹窗：
  - 重复用例分组列表（每组展示相似用例，相似度百分比）
  - 每组推荐保留的用例（高亮标记）
  - 批量选择要删除的重复用例
  - 一键删除选中的重复用例
- 对接后端 API：
  - `POST /ai/find-duplicates` — 执行语义去重
- Loading 状态：AI 分析中，请稍候...

- [ ] 未开始

---

## P11：商业化就绪 — 企业客户硬性需求

> 本阶段任务涉及前后端开发，解决企业采购的硬性门槛问题。

### P11-1: SSO/OIDC 单点登录

**问题**：仅有本地用户名密码登录，企业客户需要 LDAP/AD/OIDC 等统一认证方式。

**修改范围**：
- 新增 `backend/app/services/sso_service.py` — SSO 服务基类
- 新增 `backend/app/services/oidc_provider.py` — OIDC Provider 实现
- 新增 `backend/app/services/ldap_provider.py` — LDAP Provider 实现
- 修改 `backend/app/api/auth.py` — 添加 SSO 登录端点
- 修改 `backend/app/models/user.py` — 添加 sso_provider、sso_id 字段
- 修改 `web/src/pages/Login.tsx` — 添加 SSO 登录按钮
- 新增 `web/src/pages/SSOCallback.tsx` — SSO 回调处理页
- 修改 `web/src/pages/Settings.tsx` — SSO 配置管理（管理员）
- 新增 `backend/tests/test_sso.py`

**实现要求**：
- OIDC 集成：
  - 支持配置 OIDC Provider URL、Client ID、Client Secret
  - 授权码流程登录
  - 自动创建/关联本地用户
- LDAP 集成：
  - 支持配置 LDAP Server URL、Base DN、Bind DN/Password
  - 用户认证 + 属性映射
- 登录页展示 SSO 登录按钮（根据配置动态显示）
- 管理员可在设置页配置 SSO 参数
- 本地登录仍保留（作为备用）

- [x] 已完成 — 242a0a9

---

### P11-2: WebSocket 实时数据推送

**问题**：后端已有 WebSocket 支持但前端未接入，性能测试实时数据、告警推送依赖轮询，体验差。

**修改范围**：
- 新增 `web/src/services/websocketService.ts` — WebSocket 客户端服务
- 修改 `web/src/pages/perf-test/PerfTestMonitor.tsx` — 接入 WebSocket 实时数据
- 修改 `web/src/pages/perf-test/PerfTestScenarios.tsx` — 运行状态实时更新
- 修改 `web/src/pages/web-test/WebTestScripts.tsx` — 脚本执行日志实时推送
- 修改 `web/src/layouts/MainLayout.tsx` — 告警通知实时推送（Toast）
- 修改 `backend/app/api/v2/perf_tests.py` — 确认 WebSocket 端点
- 新增 `backend/tests/test_websocket.py`

**实现要求**：
- WebSocket 服务：
  - 自动连接/重连机制（指数退避）
  - 心跳保活（30 秒间隔）
  - 消息类型分发（performance_metrics / test_status / alert / log）
  - 连接状态指示器（顶栏小圆点：绿色=已连接、红色=断开）
- 性能测试监控：
  - 实时 RPS、响应时间、错误率折线图（替代轮询）
  - 实时并发用户数
- 测试执行状态：
  - 用例执行状态实时更新（pending → running → passed/failed）
  - 执行日志实时滚动
- 告警推送：
  - 右上角 Toast 通知
  - 告警计数 Badge

- [ ] 未开始

---

### P11-3: 暗色模式

**问题**：现代 UI 标配功能缺失，长时间使用的测试工程师需要暗色主题。

**修改范围**：
- 修改 `web/src/styles/` — 添加暗色主题变量
- 修改 `web/src/layouts/MainLayout.tsx` — 主题切换按钮
- 新增 `web/src/stores/themeStore.ts` — 主题状态管理
- 修改 `web/src/App.tsx` — 主题 Provider
- 修改全局 CSS 变量 — 支持 dark mode

**实现要求**：
- 主题切换：顶栏添加太阳/月亮图标按钮
- 主题持久化：localStorage 记住用户选择
- 跟随系统：默认跟随系统主题设置
- Ant Design 暗色主题：使用 `ConfigProvider` 的 `theme.algorithm` 切换
- ECharts 图表适配：暗色模式下图表配色自适应
- Monaco Editor 适配：暗色模式下切换编辑器主题

- [ ] 未开始

---

### P11-4: 移动端响应式适配

**问题**：无移动端适配，管理人员无法在手机上查看测试报告。

**修改范围**：
- 修改 `web/src/layouts/MainLayout.tsx` — 响应式布局
- 修改 `web/src/pages/Dashboard.tsx` — 移动端适配
- 修改 `web/src/pages/Reports.tsx` — 移动端适配
- 修改 `web/src/pages/Login.tsx` — 移动端适配
- 修改全局样式 — 响应式断点

**实现要求**：
- 响应式断点：mobile (< 768px)、tablet (768-1024px)、desktop (> 1024px)
- 移动端布局：
  - 侧边栏折叠为汉堡菜单
  - 表格改为卡片列表
  - 图表自适应宽度
  - 按钮/操作区域放大（触摸友好）
- 优先适配页面：登录、仪表盘、报告、测试结果详情
- 移动端导航：底部 Tab 栏（仪表盘、测试、报告、我的）

- [ ] 未开始

---

### P11-5: 批量操作增强

**问题**：部分页面缺乏批量操作能力，大量用例管理效率低。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 用例批量操作
- 修改 `web/src/pages/web-test/ScriptList.tsx` — 脚本批量操作
- 修改 `web/src/pages/perf-test/PerfTestScenarios.tsx` — 场景批量操作
- 新增 `web/src/components/BatchActionBar.tsx` — 通用批量操作栏组件

**实现要求**：
- 通用批量操作栏组件：
  - 全选/反选 Checkbox
  - 已选数量显示
  - 批量操作按钮（删除、移动、执行、导出、打标签）
- 用例列表：
  - Checkbox 列
  - 批量删除（二次确认）
  - 批量移动到其他用例集
  - 批量执行
  - 批量打标签/移除标签
- 脚本列表：批量删除、批量执行
- 操作完成后刷新列表

- [ ] 未开始

---

### P11-6: 快捷键支持

**问题**：缺乏快捷键支持，效率用户体验不佳。

**修改范围**：
- 新增 `web/src/hooks/useKeyboardShortcut.ts` — 快捷键 Hook
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx` — 添加快捷键
- 修改 `web/src/layouts/MainLayout.tsx` — 全局快捷键
- 新增 `web/src/components/ShortcutHelpModal.tsx` — 快捷键帮助弹窗

**实现要求**：
- 全局快捷键：
  - `Ctrl/Cmd + K` — 全局搜索
  - `Ctrl/Cmd + /` — 快捷键帮助
  - `Ctrl/Cmd + B` — 切换侧边栏
- API 测试工作台：
  - `Ctrl/Cmd + Enter` — 发送请求
  - `Ctrl/Cmd + S` — 保存用例
  - `Ctrl/Cmd + L` — 清空响应
  - `Ctrl/Cmd + D` — 复制用例
- 快捷键帮助弹窗：展示所有可用快捷键列表
- 输入框/编辑器内不触发全局快捷键

- [ ] 未开始

---

### P11-7: 用户手册与文档中心

**问题**：缺乏用户手册，新用户上手困难。

**修改范围**：
- 新增 `docs/user-manual/` — 用户手册目录
- 新增 `docs/user-manual/getting-started.md` — 快速开始
- 新增 `docs/user-manual/api-test-guide.md` — API 测试指南
- 新增 `docs/user-manual/web-test-guide.md` — Web 自动化指南
- 新增 `docs/user-manual/perf-test-guide.md` — 性能测试指南
- 新增 `docs/user-manual/ai-features-guide.md` — AI 功能指南
- 新增 `docs/user-manual/cicd-integration.md` — CI/CD 集成指南
- 修改 `web/src/pages/Documents.tsx` — 内置帮助文档入口

**实现要求**：
- 文档结构清晰，按功能模块组织
- 每篇文档包含：概述、操作步骤（带截图）、常见问题
- 支持中英双语
- 在平台内嵌入帮助入口（页面右上角 "?" 图标）
- 快速开始指南：5 分钟内完成第一次 API 测试

- [ ] 未开始

---

## P12：代码质量与工程化提升

### P12-1: CI 流水线强制化

**问题**：CI 配置中多处 `continue-on-error: true`，Lint/Type check/测试失败不阻塞合并。

**修改范围**：
- 修改 `.github/workflows/ci-backend.yml` — 移除关键步骤的 continue-on-error
- 修改 `.github/workflows/ci-frontend.yml` — 移除关键步骤的 continue-on-error
- 修复现有 Lint/Type 错误

**实现要求**：
- 后端 CI：`ruff check` 失败应阻塞合并（移除 continue-on-error）
- 前端 CI：`eslint` 和 `tsc --noEmit` 失败应阻塞合并
- 前端 CI：`vitest` 测试失败应阻塞合并
- 修复现有代码中的 Lint 和 Type 错误
- 仅 `npm run build` 保持 continue-on-error（构建失败已在其他步骤检测）

- [x] 已完成 — 0849166

---

### P12-2: 代码覆盖率报告集成

**问题**：缺乏代码覆盖率报告，无法量化测试覆盖情况。

**修改范围**：
- 修改 `backend/requirements-test.txt` — 添加 coverage 依赖
- 修改 `.github/workflows/ci-backend.yml` — 添加覆盖率步骤
- 修改 `web/package.json` — 添加覆盖率配置
- 修改 `.github/workflows/ci-frontend.yml` — 添加覆盖率步骤
- 新增 `backend/setup.cfg` — coverage 配置

**实现要求**：
- 后端：使用 `pytest --cov=app --cov-report=xml` 生成覆盖率报告
- 前端：使用 `vitest run --coverage` 生成覆盖率报告
- CI 中上传覆盖率报告为 Artifact
- 设置覆盖率阈值：后端 ≥ 60%，前端 ≥ 40%（当前基线）
- 覆盖率低于阈值时 CI 标记为警告（暂不阻塞）

- [ ] 未开始

---

### P12-3: 前端测试覆盖率提升

**问题**：前端测试覆盖率约 20%（24/119 文件），远低于后端。

**修改范围**：
- 新增 `web/src/pages/api-test/__tests__/ApiTestWorkspace.test.tsx`
- 新增 `web/src/pages/web-test/__tests__/WebTestScripts.test.tsx`
- 新增 `web/src/pages/perf-test/__tests__/PerfTestScenarios.test.tsx`
- 新增 `web/src/pages/perf-test/__tests__/PerfTestMonitor.test.tsx`
- 新增 `web/src/components/__tests__/VisualDiffViewer.test.tsx`
- 新增 `web/src/services/__tests__/webTestService.test.ts`
- 新增 `web/src/services/__tests__/perfTestService.test.ts`
- 新增 `web/src/services/__tests__/cicdService.test.ts`

**实现要求**：
- 优先覆盖核心页面和高频使用的组件
- 每个文件至少 8 个测试用例
- 测试覆盖：组件渲染、用户交互、API 调用、错误处理、Loading 状态
- Mock 所有 API 调用（vi.mock）
- 目标：测试文件从 24 个提升到 35+ 个，覆盖率从 20% 提升到 35%+

- [ ] 未开始

---

### P12-4: E2E 测试用例扩充

**问题**：E2E 测试仅 245 行代码，覆盖场景有限。

**修改范围**：
- 修改 `e2e/tests/auth.spec.ts` — 补充认证流程测试
- 新增 `e2e/tests/web-test.spec.ts` — Web 自动化流程测试
- 新增 `e2e/tests/perf-test.spec.ts` — 性能测试流程测试
- 新增 `e2e/tests/report.spec.ts` — 报告查看流程测试
- 新增 `e2e/tests/settings.spec.ts` — 设置页面测试

**实现要求**：
- 核心用户流程覆盖：
  - 登录 → 创建项目 → 创建 API 用例 → 执行 → 查看报告
  - 登录 → 创建 Web 脚本 → 录制 → 执行 → 查看截图
  - 登录 → 创建性能场景 → 运行 → 查看实时监控 → 查看结果
- 每个 spec 文件至少 5 个测试用例
- 使用 Page Object 模式组织代码
- 测试数据通过 API seed，不依赖手动操作
- 目标：E2E 用例从当前水平提升到 30+ 个

- [ ] 未开始

---

### P12-5: conftest.py 按模块拆分

**问题**：仅 1 个 conftest.py，所有测试共享同一套 fixtures，不利于模块化管理。

**修改范围**：
- 修改 `backend/tests/conftest.py` — 保留全局 fixtures
- 新增 `backend/tests/api_test/conftest.py` — API 测试模块 fixtures
- 新增 `backend/tests/web_test/conftest.py` — Web 测试模块 fixtures
- 新增 `backend/tests/perf_test/conftest.py` — 性能测试模块 fixtures
- 新增 `backend/tests/auth/conftest.py` — 认证模块 fixtures

**实现要求**：
- 全局 conftest.py：client fixture、db session fixture、通用 mock
- 模块 conftest.py：模块特定的测试数据（用例、集合、场景等）
- Fixtures 使用 `@pytest.fixture(scope="module")` 优化性能
- 提供 `authenticated_client` fixture（带 JWT Token 的 client）
- 提供 `sample_project`、`sample_collection`、`sample_case` 等常用 fixtures

- [ ] 未开始

---

### P12-6: .env 文件安全检查

**问题**：部分 `.env` 文件可能包含敏感信息提交到仓库。

**修改范围**：
- 审查 `backend/.env` — 检查是否有真实密钥
- 审查 `.env` — 检查是否有真实密钥
- 修改 `.gitignore` — 确保 .env 文件不被提交
- 修改 `.env.example` — 确保示例文件中无真实值

**实现要求**：
- 检查所有 .env 文件中是否包含真实 API Key、数据库密码、JWT Secret
- 真实密钥替换为占位符
- 确认 `.gitignore` 包含 `.env` 规则
- 提供 `scripts/check-env.sh` 脚本检查 .env 是否被 git 追踪
- CI 中添加 secret scanning 步骤（可选）

- [x] 已完成 — d11003a

---

## 进度跟踪（第二阶段）

| 任务 | 优先级 | 状态 | Commit |
|------|--------|------|--------|
| P10-1 组织/多租户管理页面 | 🔴 P0 | 已完成 | 7ef4cf8 |
| P10-2 审计日志页面 | 🔴 P0 | 已完成 | eaf71ca |
| P10-3 API Token 管理页面 | 🔴 P0 | 已完成 | f46a69e |
| P10-4 测试计划管理页面 | 🔴 P0 | 已完成 | 89211a6 |
| P10-5 质量门禁管理页面 | 🟡 P1 | 未开始 | |
| P10-6 GitHub 集成管理页面 | 🟡 P1 | 未开始 | |
| P10-7 评论系统组件 | 🟡 P1 | 未开始 | |
| P10-8 API 导入功能 UI | 🟡 P1 | 未开始 | |
| P10-9 API Mock 配置 UI | 🟡 P1 | 未开始 | |
| P10-10 用例版本管理与 Diff | 🟡 P1 | 未开始 | |
| P10-11 报告多格式导出按钮 | 🔴 P0 | 已完成 | 1beb473 |
| P10-12 视觉回归基线管理 UI | 🟡 P1 | 未开始 | |
| P10-13 触发规则配置页面 | 🟢 P2 | 未开始 | |
| P10-14 通知渠道配置页面 | 🟢 P2 | 未开始 | |
| P10-15 团队效能指标页面 | 🟢 P2 | 未开始 | |
| P10-16 语义去重入口 | 🟢 P2 | 未开始 | |
| P11-1 SSO/OIDC 单点登录 | 🔴 P0 | 已完成 | 242a0a9 |
| P11-2 WebSocket 实时推送 | 🟡 P1 | 未开始 | |
| P11-3 暗色模式 | 🟡 P1 | 未开始 | |
| P11-4 移动端响应式适配 | 🟡 P1 | 未开始 | |
| P11-5 批量操作增强 | 🟡 P1 | 未开始 | |
| P11-6 快捷键支持 | 🟢 P2 | 未开始 | |
| P11-7 用户手册与文档中心 | 🟡 P1 | 未开始 | |
| P12-1 CI 流水线强制化 | 🔴 P0 | 已完成 | 0849166 |
| P12-2 代码覆盖率报告 | 🟡 P1 | 未开始 | |
| P12-3 前端测试覆盖率提升 | 🟡 P1 | 未开始 | |
| P12-4 E2E 测试用例扩充 | 🟡 P1 | 未开始 | |
| P12-5 conftest.py 按模块拆分 | 🟢 P2 | 未开始 | |
| P12-6 .env 文件安全检查 | 🔴 P0 | 已完成 | d11003a |

---

## 任务总数统计

| 阶段 | 总数 | 已完成 | 未完成 |
|------|------|--------|--------|
| 第一阶段（P0-P9） | 34 | 34 | 0 |
| 第二阶段（P10-P12） | 29 | 8 | 21 |
| **总计** | **63** | **42** | **21** |

---

## 第二阶段工作量估算

| 优先级 | 任务数 | 预估工作量 | 说明 |
|--------|--------|-----------|------|
| 🔴 P0（必须） | 7 项 | 12-17 天 | 组织管理、审计日志、Token、测试计划、报告导出、SSO、CI 强制化、.env 安全 |
| 🟡 P1（重要） | 15 项 | 20-28 天 | 质量门禁、GitHub 集成、评论、导入、Mock、版本管理、视觉回归、WebSocket、暗色模式、移动端、批量操作、文档、测试覆盖率 |
| 🟢 P2（锦上添花） | 7 项 | 5-8 天 | 触发规则、通知、团队指标、语义去重、快捷键、conftest 拆分 |
| **总计** | **29 项** | **37-53 天** | |
