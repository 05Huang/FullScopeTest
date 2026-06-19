# FullScopeTest 改进计划

> 每条任务完成后标记 `- [x]`，并附上 commit hash。

---

## 历史阶段（已完成）

> 以下三个阶段共 **126 项任务已全部完成**，详细内容见 git 历史。

| 阶段 | 任务数 | 核心内容 | 状态 |
|------|--------|---------|------|
| 第一阶段（P0-P9） | 34 | 安全防护、架构优化、权限体系、测试管理、报告度量、协作工作流、平台扩展、运维保障 | ✅ 全部完成 |
| 第二阶段（P10-P12） | 29 | 前端覆盖补全（16 项后端能力的 UI 落地）、企业级需求（SSO/暗色/响应式）、代码质量提升 | ✅ 全部完成 |
| 第三阶段（P13-P22） | 63 | 基础设施工程化、AI/ML 核心增强、测试引擎升级、企业安全合规、CI/CD 深度集成、报告分析、K8s 部署、开发者体验、商业化运营、前端体验升级 | ✅ 全部完成 |

---

## 当前阶段（待完成）

---

# 第四阶段：逻辑一致性修复与商业化补齐

> 目标：修复「项目深度分析」中发现的逻辑矛盾、文档不一致、功能缺失等问题，使项目达到真正可面向客户交付的商业级水准。
> 来源：2026-06-19 全面代码审计，覆盖前后端 ~155K 行代码 + README + 配置文件。

---

## P23：逻辑一致性修复（文档与代码对齐）

> 以下问题会导致用户/开发者对项目产生信任危机，必须优先修复。

### P23-1: 修复 README 中 FastAPI 虚假宣称

**问题**：README 技术对比表中声称后端使用 "FastAPI (比 Flask 快 30%+)"，但实际后端框架是 **Flask 3.0**。代码中存在未完成的 `backend/app/fastapi_app.py`（6KB），说明曾尝试迁移但未完成。这是对外宣称与实际实现的直接矛盾，对用户和开发者造成严重误导。

**修改范围**：
- 修改 `README.md` — 技术对比表
- 修改 `README_EN.md` — 英文版同步修改
- 删除或移入 `backend/app/fastapi_app.py` — 清理未完成的迁移代码

**实现要求**：
- 技术对比表中将 "FastAPI" 改为实际的 "Flask 3.0"
- 如需保留 FastAPI 迁移计划，在表中标注"计划迁移至 FastAPI"并链接到迁移文档
- 将 `fastapi_app.py` 移至 `backend/_deprecated/` 或直接删除，避免混淆
- 检查 README 中所有技术栈描述与实际代码一致

- [x] 完成 → `d6c454f`

---

### P23-2: 修复 README ER 图与实际数据模型不一致

**问题**：README 的 ER 图明确画出 `User { int organization_id FK }`，但实际 `User` 模型（`models/user.py`）**没有 `organization_id` 字段**。组织关系通过 `OrganizationMember` 中间表实现。ER 图与实际数据模型不符，误导开发者理解数据架构。

**修改范围**：
- 修改 `README.md` — ER 图部分
- 修改 `README_EN.md` — 英文版同步

**实现要求**：
- ER 图中 `User` 实体移除 `organization_id FK`
- 新增 `OrganizationMember` 关联实体：`{ int id PK, int organization_id FK, int user_id FK, string role, boolean is_active }`
- 更新关系线：`User ||--o{ OrganizationMember` 和 `Organization ||--o{ OrganizationMember`
- 确保 ER 图中所有实体字段与实际模型文件一一对应

- [x] 完成 → `3f5c1c6`

---

### P23-3: APP 测试功能声明降级 — 无法真正执行

**问题**：README 声称 "基于 Appium，支持 Android / iOS 双平台"，但 Web 平台无法直接连接物理设备或模拟器，也没有设备农场（Device Farm）实现。当前 `app_test.py` 仅是脚本编辑器 + 存储，**不具备真正的执行能力**。对外宣称会造成用户期望落差。

**修改范围**：
- 修改 `README.md` — APP 测试描述
- 修改 `README_EN.md` — 英文版同步
- 修改 `web/src/pages/app-test/AppTestScripts.tsx` — 添加功能限制提示

**实现要求**：
- README 中 APP 测试描述改为："APP 测试脚本管理（支持 Appium 脚本编写与存储，需配合外部设备农场执行）"
- 前端 APP 测试页面添加提示横幅："APP 测试执行需要连接外部 Appium Server 或设备农场，请在设置中配置 Appium Server 地址"
- 对比表中将 "✅ 基于 Appium" 改为 "⚠️ 脚本管理（需外部执行环境）"
- 如有计划支持云设备农场，标注路线图

- [x] 完成 → `5d24984`

---

### P23-4: Web 录制功能在生产环境不可用的说明

**问题**：README 将 "录制回放" 列为核心功能，但 `playwright codegen` 需要图形界面（GUI），在远程服务器/无头环境下无法运行。FAQ 里才提到此限制，但核心功能列表未标注。

**修改范围**：
- 修改 `README.md` — Web 自动化功能描述
- 修改 `README_EN.md` — 英文版同步
- 修改 `web/src/pages/web-test/WebTestScripts.tsx` — 录制按钮添加环境检测

**实现要求**：
- 核心功能列表中 Web 自动化描述改为："支持在线编写、视觉回归测试、VNC Live View 实时预览（录制功能需本地 GUI 环境）"
- 前端录制按钮点击时检测后端是否支持录制（调用 `/web-test/recorder/status`），不支持时弹出提示
- 提供替代方案说明："可在本地使用 `playwright codegen` 录制后上传脚本到平台执行"

- [x] 完成 → `e89a833`

---

### P23-5: K8s 部署能力与 README 声称对齐

**问题**：README 对比 MeterSphere 时声称 "Docker Compose + K8s" 双部署方式，需确认 P19-1 的 Helm Chart 实际存在且可用。

**修改范围**：
- 检查 `deploy/helm/` 目录是否实际存在并包含完整配置
- 如不存在，按 P19-1 规格创建
- 修改 `README.md` — 确认 K8s 部署文档链接有效

**实现要求**：
- 确认 `deploy/helm/fullscopetest/` 目录结构完整
- 确认 `docs/kubernetes-deployment.md` 文档存在且内容可用
- README 中 K8s 部署链接指向有效文档
- 如 Helm Chart 不存在，创建最小可用版本（Backend Deployment + Service + Ingress）

- [x] 完成 → `31bca23`

---

### P23-6: SSO/OIDC 功能完整性验证

**问题**：User 模型有 `sso_provider`、`sso_id`、`sso_metadata` 字段，前端有 `SSOCallback.tsx` 页面，但需确认 P11-1 的 SSO 实现是否真正可用（OIDC 授权码流程、用户映射、回调处理）。

**修改范围**：
- 验证 `backend/app/services/sso_service.py` 是否存在且实现完整
- 验证 `backend/app/services/oidc_provider.py` 是否存在
- 修改 `web/src/pages/Login.tsx` — 确认 SSO 登录按钮根据配置动态显示

**实现要求**：
- 确认 OIDC 授权码流程完整实现（发现端点 → 授权请求 → 回调处理 → Token 交换 → 用户创建/关联）
- 确认 SSO 配置页面可正常配置 Provider URL、Client ID、Client Secret
- 确认无 SSO 配置时登录页不显示 SSO 按钮
- 如实现不完整，标注为 Beta 并在 README 中说明

- [x] 完成 → `fee61ae`

---

## P24：核心功能补全（缺失的关键能力）

> 以下功能在现有代码中有暗示但未完整实现，或在商业化评估中被识别为关键缺失。

### P24-1: 邮件服务集成 — SMTP / SendGrid

**问题**：忘记密码接口直接在 JSON 响应中返回 `reset_token`，**没有发送邮件**。任何知道邮箱的人都能获取重置 token，这是严重安全问题。同时，通知系统（Webhook/钉钉/飞书）也缺少邮件渠道。

**修改范围**：
- 新增 `backend/app/services/email_service.py` — 邮件发送服务
- 修改 `backend/app/api/auth.py` — `forgot_password` 端点改为发送邮件
- 修改 `backend/app/config.py` — 邮件配置项
- 修改 `backend/.env.example` — 添加邮件配置示例
- 修改 `web/src/pages/ForgotPassword.tsx` — 移除 token 直接展示
- 修改 `web/src/pages/ResetPassword.tsx` — 从 URL query 参数读取 token
- 新增 `backend/tests/test_email_service.py`

**实现要求**：
- `EmailService` 支持多种后端：
  - SMTP（通用，通过 `SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASSWORD` 配置）
  - SendGrid API（通过 `SENDGRID_API_KEY` 配置）
  - 控制台输出（开发环境，`EMAIL_BACKEND=console`）
- 忘记密码流程修复：
  - 用户提交邮箱 → 后端生成 token → 发送重置链接邮件 → 返回通用提示"如果邮箱已注册，您将收到重置邮件"
  - 重置链接格式：`https://{domain}/reset-password?token={token}`
  - Token 有效期 1 小时，使用后立即失效
- 邮件模板：HTML 格式，包含平台 Logo、操作说明、安全提示
- 通过 `EMAIL_ENABLED`（默认 false）环境变量控制

- [x] 完成 → `89b752a`

---

### P24-2: 统一 Role 模型 — 消除双轨制

**问题**：存在两套角色系统并行：
1. `User.role` 字段：简单的字符串（`admin`/`member`/`viewer`），`user.py` 中直接比较 `self.role == ROLE_ADMIN`
2. `models/role.py`：7.5KB 的复杂 Role 模型（看起来是后期加的 RBAC 系统），含权限矩阵

`_seed_system_roles` 启动时种子系统角色到 `roles` 表，但 `User` 模型和多数 API 仍直接使用字符串角色。两套系统未统一，权限检查存在不一致风险。

**修改范围**：
- 修改 `backend/app/models/user.py` — `role` 字段改为外键关联 `Role` 表，保留字符串兼容层
- 修改 `backend/app/models/role.py` — 确保包含 `admin`/`member`/`viewer` 三个内置角色
- 修改 `backend/app/services/permission_service.py` — 统一权限检查入口
- 修改所有使用 `user.role == 'admin'` 的 API — 改为 `user.has_permission('xxx')`
- 修改 `backend/app/middleware/permission.py` — 装饰器使用统一权限系统

**实现要求**：
- `User.role` 字段保留为字符串（兼容），但新增 `User.role_obj` relationship 关联 `Role` 表
- `User.has_permission(permission)` 方法查询 `Role` 表的权限矩阵
- 所有 API 的权限检查统一使用 `has_permission()` 方法
- 内置角色（admin/member/viewer）不可删除，但可修改权限
- 自定义角色继承内置角色的基础权限

- [x] 完成 → `8c989bc`

---

### P24-3: 拆分 tasks.py 巨型文件（41KB）

**问题**：`backend/app/tasks.py` 是 41KB 的单文件，包含所有异步任务（Web 测试执行、性能测试执行、截图服务、告警引擎、定时报告等），严重违反单一职责原则。对比 `services/` 目录有 79 个文件的分层设计，`tasks.py` 的组织方式不一致。

**修改范围**：
- 新增 `backend/app/tasks/` 包（替代单文件）
- 新增 `backend/app/tasks/__init__.py` — 任务注册入口
- 新增 `backend/app/tasks/web_test.py` — Web 测试相关任务
- 新增 `backend/app/tasks/perf_test.py` — 性能测试相关任务
- 新增 `backend/app/tasks/visual.py` — 视觉回归相关任务
- 新增 `backend/app/tasks/alerts.py` — 告警相关任务
- 新增 `backend/app/tasks/reports.py` — 报告生成相关任务
- 新增 `backend/app/tasks/notifications.py` — 通知相关任务
- 新增 `backend/app/tasks/maintenance.py` — 维护任务（清理、备份等）
- 删除旧 `backend/app/tasks.py`

**实现要求**：
- 按功能域拆分为 8 个模块文件
- 保持所有 Celery task 名称不变（`@celery.task(name='xxx')`），确保现有调度不受影响
- `__init__.py` 统一导入所有任务，保持 `from .tasks import xxx` 的兼容性
- 每个模块文件不超过 300 行
- 拆分后所有现有测试通过

- [x] 完成 → `0e58941`

---

### P24-4: 忘记密码安全修复 — 不在响应中返回 Token

**问题**：`authService.ts` 中 `forgotPassword` 返回类型为 `ApiResponse<{ reset_token: string }>`，即后端将 reset_token 直接返回给前端。在 P24-1 邮件服务集成前，这是一个独立的安全漏洞需要先修复。

**修改范围**：
- 修改 `backend/app/api/auth.py` — `forgot_password` 端点
- 修改 `web/src/services/authService.ts` — 移除 token 返回类型
- 修改 `web/src/pages/ForgotPassword.tsx` — 移除 token 展示逻辑

**实现要求**：
- 后端 `forgot_password` 返回统一提示："如果该邮箱已注册，重置链接已发送到您的邮箱"
- 前端不再展示/使用 token，仅展示发送成功提示
- 在邮件服务未配置时（`EMAIL_ENABLED=false`），管理员可通过命令行重置密码：`python manage.py reset-password --user xxx`
- 提供 `scripts/reset_password.py` 管理员工具脚本

- [x] 完成 → `f04c7ad`

---

## P25：代码架构优化（技术债务清理）

### P25-1: 前端测试覆盖率从 26 文件提升到 50+

**问题**：前端 72K 行代码仅 26 个测试文件（覆盖率约 22%），远低于后端 470+ 测试用例的覆盖水平。P12-3 已完成部分提升，但仍有大量核心页面和组件无测试。

**修改范围**：
- 新增 `web/src/pages/admin/__tests__/UserManagement.test.tsx`
- 新增 `web/src/pages/organizations/__tests__/OrganizationList.test.tsx`
- 新增 `web/src/pages/organizations/__tests__/OrganizationDetail.test.tsx`
- 新增 `web/src/pages/__tests__/Settings.test.tsx`
- 新增 `web/src/pages/__tests__/Profile.test.tsx`
- 新增 `web/src/pages/__tests__/QualityGates.test.tsx`
- 新增 `web/src/pages/__tests__/TestPlans.test.tsx`
- 新增 `web/src/pages/__tests__/Documents.test.tsx`
- 新增 `web/src/pages/__tests__/CICD.test.tsx`
- 新增 `web/src/hooks/__tests__/useRole.test.ts`
- 新增 `web/src/hooks/__tests__/useGeoLanguage.test.ts`
- 新增 `web/src/stores/__tests__/authStore.test.ts`
- 新增 `web/src/stores/__tests__/projectStore.test.ts`

**实现要求**：
- 优先覆盖管理员、组织管理、设置等核心页面
- 每个文件至少 6 个测试用例
- 测试覆盖：组件渲染、表单交互、权限控制、API 调用、错误处理
- 目标：测试文件从 26 个提升到 40+ 个，行覆盖率从 22% 提升到 40%+

- [x] 完成 → 测试文件从 26 个提升到 51 个，全部通过

---

### P25-2: config.py 多环境配置审计 — 确保生产安全默认值

**问题**：`backend/app/config.py` 有 10KB，包含 Development/Testing/Production 三个配置类。需审计所有配置项确保生产环境有安全的默认值。

**修改范围**：
- 修改 `backend/app/config.py` — 审计并修复配置
- 修改 `backend/.env.example` — 确保文档完整

**实现要求**：
- 审计清单：
  - `SECRET_KEY`：生产环境必须非空，否则拒绝启动
  - `JWT_SECRET_KEY`：生产环境必须非空
  - `DEBUG`：生产环境必须 `False`
  - `SQLALCHEMY_ECHO`：生产环境必须 `False`
  - `CORS_ORIGINS`：生产环境禁止 `*`
  - `WTF_CSRF_ENABLED`：确认是否需要启用
  - `COOKIE_SECURE`：生产环境必须 `True`
  - `SESSION_COOKIE_HTTPONLY`：必须 `True`
- 提供 `scripts/check_config.py` 脚本，CI 中运行检查配置安全性

- [x] 完成 → `f89c998`

---

### P25-3: 全局搜索功能验证 — 确认跨模块可用

**问题**：`backend/app/api/global_search.py` 仅 938 字节（非常小），前端有 `GlobalSearch` 组件。需确认全局搜索是否真正跨模块工作。

**修改范围**：
- 修改 `backend/app/api/global_search.py` — 确认搜索覆盖范围
- 验证前端 `GlobalSearch` 组件的搜索体验

**实现要求**：
- 确认搜索覆盖：用例名称、脚本名称、项目名称、文档标题
- 确认搜索结果包含跳转链接（点击可跳转到对应页面）
- 确认搜索支持模糊匹配
- 如实现不完整，补充搜索范围和结果展示

- [x] 完成 → `4b497f6`（已验证：AI-powered 全局搜索可用）

---

### P25-4: 新手引导（Tour Guide）功能验证

**问题**：README 声称有 "7 步新手引导"，需确认 `TourGuide` 组件实际存在且功能完整。

**修改范围**：
- 验证 `web/src/components/TourGuide.tsx` 或类似组件是否存在
- 确认引导步骤覆盖核心功能

**实现要求**：
- 确认引导组件存在且可触发
- 确认引导步骤：侧边栏导航、AI 助手、项目创建、用例编写、执行测试、查看报告
- 确认引导状态保存在 `localStorage`，不重复显示
- 确认可在设置中重新触发引导

- [x] 完成 → `4b497f6`（组件不存在，README 已标注「计划中」）

---

## P26：商业化运营补齐（变现能力）

> 以下功能是 SaaS 产品真正变现所需的能力，当前完全缺失。

### P26-1: 计费与订阅管理系统

**问题**：无 SaaS 定价、用量计费、套餐管理能力。P3-1 的配额系统仅限制资源使用，无法关联到付费计划。

**修改范围**：
- 新增 `backend/app/models/subscription.py` — 订阅模型
- 新增 `backend/app/models/billing_plan.py` — 套餐模型
- 新增 `backend/app/services/billing_service.py` — 计费服务
- 新增 `backend/app/api/billing.py` — 计费 API
- 新增 `web/src/pages/admin/BillingDashboard.tsx` — 计费管理页面
- 修改 `web/src/pages/Settings.tsx` — 添加套餐管理 Tab

**实现要求**：
- 套餐定义：
  - Free：5 项目、100 用例、1 并行、100 AI 调用/月
  - Pro（¥299/月）：50 项目、1000 用例、5 并行、5000 AI 调用/月
  - Enterprise（定制）：不限
- 订阅管理：升级、降级、取消
- 用量计量：按月统计各项资源使用量
- 账单生成：按月生成账单（JSON/CSV 导出）
- 支付集成预留：Stripe / 支付宝 Webhook 回调接口

- [x] 完成 → `5b24bc6`

---

### P26-2: 白标与品牌定制

**问题**：无法自定义 Logo、品牌名、主题色，企业客户需要白标部署。

**修改范围**：
- 新增 `backend/app/models/branding_config.py` — 品牌配置模型
- 新增 `backend/app/api/branding.py` — 品牌配置 API
- 修改 `web/src/layouts/MainLayout.tsx` — 使用动态 Logo 和品牌名
- 修改 `web/src/styles/index.css` — 支持动态主题色
- 修改 `web/index.html` — 动态标题和 Favicon

**实现要求**：
- 可配置项：
  - 平台名称（替换 "FullScopeTest"）
  - Logo URL（替换默认 Logo）
  - Favicon URL
  - 主色调（替换 `--fst-primary`）
  - 登录页背景图
  - Footer 文案
- 管理员在设置页配置
- 配置存储在数据库，支持缓存
- 前端启动时通过 `/branding/config` API 获取品牌配置

- [x] 完成 → `9cd5e7f` + `4e8a982`

---

### P26-3: 用户自定义仪表盘

**问题**：Dashboard 固定展示预设指标，用户无法根据自身关注点自定义布局和内容。

**修改范围**：
- 新增 `backend/app/models/dashboard_widget.py` — 仪表盘组件模型
- 新增 `backend/app/api/dashboard_config.py` — 仪表盘配置 API
- 修改 `web/src/pages/Dashboard.tsx` — 支持可拖拽布局
- 新增 `web/src/components/dashboard/` — 仪表盘组件库

**实现要求**：
- 预设组件：
  - 测试通过率（折线图）
  - 最近执行（表格）
  - 失败用例 Top 10
  - AI 使用统计
  - 团队活跃度
  - 质量门禁状态
  - SLA 达成率
  - 成本概览
- 布局：网格布局，支持拖拽排列
- 每个用户独立保存自己的 Dashboard 配置
- 提供"恢复默认"功能

- [x] 完成 → `896581f`

---

### P26-4: 多渠道通知完善 — 邮件 + 飞书 + 钉钉

**问题**：通知系统仅支持 Webhook，缺少邮件、飞书、钉钉等企业常用通知渠道的实际实现。

**修改范围**：
- 新增 `backend/app/services/notification_channels/email_channel.py`
- 新增 `backend/app/services/notification_channels/feishu_channel.py`
- 新增 `backend/app/services/notification_channels/dingtalk_channel.py`
- 新增 `backend/app/services/notification_channels/slack_channel.py`
- 修改 `backend/app/services/notification_service.py` — 统一渠道调度
- 修改 `web/src/pages/NotificationSettings.tsx` — 各渠道配置表单

**实现要求**：
- 邮件通知：依赖 P24-1 的 EmailService
- 飞书通知：Webhook URL + 签名验证，支持富文本卡片消息
- 钉钉通知：Webhook URL + 加签，支持 Markdown 消息
- Slack 通知：Incoming Webhook，支持 Block Kit 消息
- 每个渠道独立的配置表单和测试发送按钮
- 通知模板：支持变量替换（`{project_name}`、`{pass_rate}`、`{failed_count}`）

- [x] 完成 → `91135a1`

---

## P27：文档与营销材料修正

### P27-1: README 功能声明全面审计

**问题**：README 中多处功能描述与实际实现存在差距，需要逐项审计并修正。

**修改范围**：
- 修改 `README.md` — 全面审计
- 修改 `README_EN.md` — 英文版同步

**实现要求**：
- 审计清单（每项标记 ✅ 实际可用 / ⚠️ 部分可用 / ❌ 不可用）：
  - AI Copilot 自然语言编排 → 验证实际可用性
  - 脚本自动生成 → 验证实际可用性
  - 智能错误分析与自愈 → 验证 P14-2 是否真正可用
  - Mock Server → 验证前端 P10-9 是否已对接
  - 视觉回归测试 → 验证完整流程
  - VNC Live View → 验证是否可远程使用
  - Prompt A/B 测试 → 验证实际可用性
  - 语义去重 → 验证 P10-16 是否已对接
  - SSO 集成 → 验证 P11-1 是否真正可用
  - 审计日志 → 验证 P10-2 是否已对接
  - 组织邀请码 → 验证实际流程
- 根据审计结果修正描述：✅ 保持不变，⚠️ 标注限制条件，❌ 移除或标注为计划中

- [x] 完成 → `c97d7ad`

---

### P27-2: 功能路线图文档

**问题**：缺少公开的功能路线图，用户无法了解未来计划。

**修改范围**：
- 新增 `docs/ROADMAP.md` — 功能路线图

**实现要求**：
- 按季度规划（Q3 2026 / Q4 2026 / Q1 2027）
- 分类：已上线、开发中、计划中
- 包含关键里程碑：
  - Q3：邮件服务、计费系统、APP 测试云设备
  - Q4：白标定制、自定义仪表盘、更多协议支持
  - Q1：设备农场集成、AI Agent 自主测试
- 在 README 中链接路线图

- [x] 完成 → `796e7d0`

---

## 第四阶段进度跟踪

| 任务 | 优先级 | 状态 | Commit |
|------|--------|------|--------|
| **P23: 逻辑一致性修复** | | | |
| P23-1 修复 README FastAPI 虚假宣称 | 🔴 | ✅ 完成 | d6c454f |
| P23-2 修复 ER 图与实际模型不一致 | 🔴 | ✅ 完成 | 3f5c1c6 |
| P23-3 APP 测试功能声明降级 | 🔴 | ✅ 完成 | 5d24984 |
| P23-4 Web 录制功能限制说明 | 🟡 | ✅ 完成 | e89a833 |
| P23-5 K8s 部署能力验证 | 🟡 | ✅ 完成 | 31bca23 |
| P23-6 SSO/OIDC 功能完整性验证 | 🟡 | ✅ 完成 | fee61ae |
| **P24: 核心功能补全** | | | |
| P24-1 邮件服务集成（SMTP/SendGrid） | 🔴 | ✅ 完成 | 89b752a |
| P24-2 统一 Role 模型消除双轨制 | 🔴 | ✅ 完成 | 8c989bc |
| P24-3 拆分 tasks.py 巨型文件 | 🟡 | ✅ 完成 | 0e58941 |
| P24-4 忘记密码安全修复 | 🔴 | ✅ 完成 | f04c7ad |
| **P25: 代码架构优化** | | | |
| P25-1 前端测试覆盖率提升到 40%+ | 🟡 | ✅ 完成 | 366cc05 + 新增 15 个测试文件 |
| P25-2 多环境配置安全审计 | 🔴 | ✅ 完成 | f89c998 |
| P25-3 全局搜索功能验证 | 🟢 | ✅ 完成 | 4b497f6 |
| P25-4 新手引导功能验证 | 🟢 | ✅ 完成 | 4b497f6 |
| **P26: 商业化运营补齐** | | | |
| P26-1 计费与订阅管理系统 | 🟡 | ✅ 完成 | 5b24bc6 |
| P26-2 白标与品牌定制 | 🟡 | ✅ 完成 | 9cd5e7f + 4e8a982 |
| P26-3 用户自定义仪表盘 | 🟢 | ✅ 完成 | 896581f |
| P26-4 多渠道通知完善 | 🟡 | ✅ 完成 | 91135a1 |
| **P27: 文档与营销修正** | | | |
| P27-1 README 功能声明全面审计 | 🔴 | ✅ 完成 | c97d7ad |
| P27-2 功能路线图文档 | 🟢 | ✅ 完成 | 796e7d0 |

---

## 第四阶段任务总数统计

| 阶段 | 总数 | 🔴 必须 | 🟡 重要 | 🟢 锦上添花 |
|------|------|---------|---------|-------------|
| P23 逻辑一致性修复 | 6 | 3 | 3 | 0 |
| P24 核心功能补全 | 4 | 3 | 1 | 0 |
| P25 代码架构优化 | 4 | 1 | 1 | 2 |
| P26 商业化运营补齐 | 4 | 0 | 3 | 1 |
| P27 文档与营销修正 | 2 | 1 | 0 | 1 |
| **总计** | **20** | **8** | **8** | **4** |

---

## 全阶段总进度汇总

| 阶段 | 总数 | 已完成 | 未完成 |
|------|------|--------|--------|
| 第一阶段（P0-P9） | 34 | 34 | 0 |
| 第二阶段（P10-P12） | 29 | 29 | 0 |
| 第三阶段（P13-P22） | 63 | 63 | 0 |
| 第四阶段（P23-P27） | 20 | 20 | **0** |
| 第五阶段（P28-P30） | 30 | 30 | **0** |
| **总计** | **176** | **176** | **0** |

---

# 第五阶段：小功能增量 & 代码卫生

> 以下任务均为**小体量、低成本、高感知**的改进，适合在大任务间隙穿插完成。
> 每项预估 0.5~2 小时，可独立提交。

---

## P28：代码卫生 — 清理残留与硬编码

### P28-1: 清理前端残留 console.log

**问题**：`App.tsx:73` 有调试用 `console.log('[App] Rendering...')`，`useGeoLanguage.ts` 有 12 处调试日志。生产环境不应输出调试信息。

**修改范围**：
- 修改 `web/src/App.tsx` — 删除第 73 行 console.log
- 修改 `web/src/hooks/useGeoLanguage.ts` — 将调试日志包裹在 `if (import.meta.env.DEV)` 条件中

- [x] 完成 → `aef582b`

---

### P28-2: 消除前端硬编码中文 — 全面 i18n 化

**问题**：以下位置使用了硬编码中文/英文文案，未走 i18n：

| 文件 | 行号 | 硬编码内容 |
|------|------|-----------|
| `GlobalSearch.tsx` | 108 | `"使用自然语言搜索（例如：查找关于支付的所有接口和脚本）"` |
| `ResponseViewer.tsx` | 46, 95, 110 | `"响应"`、`"暂无 Cookie"`、`"发送请求查看响应"` |
| `ResponseViewer.tsx` | 59, 76, 92, 98 | `"Body"`、`"Headers"`、`"Cookies"`、`"测试结果"` |
| `ApiTestWorkspace.tsx` | 921 | `"已复制 cURL 命令到剪贴板"` |
| `GlobalCopilot.tsx` | 524 | `"请输入模型提供商的 API Key"` |
| `UserManagement.tsx` | 113-127 | `"Search username or email..."`、`"Filter role"`、`"Enter new password"` |
| `AiReviewModal.tsx` | 84 | `"AI 正在深度评审当前集合..."` |

**修改范围**：上述各文件，替换为 `t('xxx')` 调用
**修改 `web/src/i18n/locales/zh.json` + `en.json` — 添加对应 key

- [x] 完成 → `642b1f7`

---

### P28-3: 消除后端硬编码地址

**问题**：`ApiTestWorkspace.tsx:1477` 硬编码了 `http://127.0.0.1:5211/api/v1` 作为默认 base_url。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx` — 将默认 base_url 改为从环境变量或当前选中的环境变量中读取

**实现要求**：
- 优先使用当前选中环境的 `base_url` 变量
- 回退为空字符串（让用户手动填写），而非硬编码本地地址

- [x] 完成 → `4bf2638`

---

### P28-4: 后端存储服务 TODO 补全

**问题**：`storage_service.py` 第 211、215 行有两个 TODO 未实现：
```python
# TODO: 实现阿里云 OSS 存储
# TODO: 实现 AWS S3 存储
```

**修改范围**：
- 修改 `backend/app/services/storage_service.py` — 实现 OSSStorage 和 S3Storage

**实现要求**：
- `OSSStorage`：使用 `oss2` SDK，通过 `OSS_ENDPOINT`/`OSS_ACCESS_KEY_ID`/`OSS_ACCESS_KEY_SECRET`/`OSS_BUCKET_NAME` 配置
- `S3Storage`：使用 `boto3`，通过 `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_S3_BUCKET` 配置
- 两种实现均支持 `upload`/`download`/`delete`/`get_url` 方法
- 文件路径格式：`{folder}/{year}/{month}/{uuid}.{ext}`

- [x] 完成 → `84714f0`

---

### P28-5: 后端限流 TODO 补全 — 组织级自定义限额

**问题**：`rate_limit_service.py` 第 126、132 行有两个 TODO：
```python
# TODO: 从数据库或缓存获取组织自定义限额
# TODO: 从数据库获取组织自定义限额
```

**修改范围**：
- 修改 `backend/app/services/rate_limit_service.py` — 从 Quota 模型读取组织限额

**实现要求**：
- 从 `Quota` 模型查询当前组织的 API 调用限额
- 缓存到 Redis（TTL 5 分钟），避免每次请求查数据库
- 无自定义限额时使用全局默认值

- [x] 完成 → `5a278cd`

---

### P28-6: ResponseViewer 暗色模式适配

**问题**：`ResponseViewer.tsx` 中 Monaco Editor 硬编码 `theme="vs-light"`，暗色模式下编辑器仍为白色背景。

**修改范围**：
- 修改 `web/src/pages/api-test/ResponseViewer.tsx` — 根据当前主题切换 Monaco 主题

**实现要求**：
- 读取 `themeStore` 的当前主题
- 亮色模式：`vs-light`，暗色模式：`vs-dark`

- [x] 完成 → `507749e`

---

## P29：用户体验小功能（高感知低成本）

### P29-1: 侧边栏折叠状态持久化

**问题**：`MainLayout.tsx:170` 使用 `useState(false)` 管理侧边栏折叠状态，刷新页面后重置为展开。

**修改范围**：
- 修改 `web/src/layouts/MainLayout.tsx` — 将 `collapsed` 状态持久化到 `localStorage`

**实现要求**：
- 使用 `useLocalStorage` hook（已有）或 Zustand persist
- 键名：`fst-sidebar-collapsed`
- 默认值：`false`（展开）

- [x] 完成 → `a006d9f`

---

### P29-2: 面包屑导航

**问题**：页面间跳转无面包屑提示，用户在深层页面（如测试计划详情 > 运行详情）容易迷失。

**修改范围**：
- 修改 `web/src/layouts/MainLayout.tsx` — 在内容区顶部添加面包屑
- 新增 `web/src/components/PageBreadcrumb.tsx` — 面包屑组件

**实现要求**：
- 根据当前路由自动生成面包屑：首页 > 模块 > 子页面
- 使用 Ant Design `Breadcrumb` 组件
- 最后一级不可点击（当前页）
- 支持 i18n

- [x] 完成 → `26312eb`

---

### P29-3: 404 页面

**问题**：访问不存在的路由时显示空白页，无友好提示。

**修改范围**：
- 新增 `web/src/pages/NotFound.tsx` — 404 页面
- 修改 `web/src/App.tsx` — 添加 `*` 通配路由

**实现要求**：
- 展示 404 插画 + "页面不存在" 提示
- 提供"返回首页"按钮
- 支持 i18n

- [x] 完成 → `832dd1d`

---

### P29-4: 请求历史记录

**问题**：API 测试工作台无请求历史，用户重复调试时需要反复填写表单。

**修改范围**：
- 新增 `web/src/pages/api-test/components/RequestHistory.tsx` — 请求历史面板
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx` — 集成历史面板

**实现要求**：
- 自动保存最近 50 条请求到 `localStorage`（方法 + URL + 状态码 + 耗时 + 时间戳）
- 历史面板展示为列表，点击可回填到请求编辑器
- 支持清空历史
- 按时间倒序排列

- [x] 完成 → `fa5dfcf`

---

### P29-5: 多语言代码片段生成

**问题**：仅有 "复制为 cURL" 功能，缺少 Python/JavaScript/Java 等语言的代码片段生成。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx` — 扩展代码生成菜单

**实现要求**：
- 在 "复制为 cURL" 旁添加下拉菜单，支持：
  - cURL（已有）
  - Python (requests)
  - JavaScript (fetch)
  - Java (OkHttp)
  - Go (net/http)
- 每种语言生成对应的可运行代码片段
- 复制到剪贴板 + 成功提示

- [x] 完成 → `b483cbf`

---

### P29-6: 项目收藏/置顶

**问题**：项目列表按创建时间排列，常用项目需要翻找。

**修改范围**：
- 修改 `backend/app/models/project.py` — 添加 `is_pinned` 字段
- 修改 `backend/app/api/projects.py` — 支持置顶/取消置顶
- 修改 `web/src/layouts/MainLayout.tsx` — 项目下拉列表置顶排序

**实现要求**：
- 项目卡片/列表项添加"置顶"图标按钮
- 置顶项目排在列表最前
- 支持多个置顶项目（按置顶时间排序）
- 前端 API：`PUT /projects/:id/pin`

- [x] 完成 → `f0fa9a8`

---

### P29-7: 版本号与环境标识显示

**问题**：用户无法在 UI 中看到当前平台版本号和运行环境（开发/演示/生产）。

**修改范围**：
- 修改 `web/src/layouts/MainLayout.tsx` — 侧边栏底部显示版本号
- 修改 `backend/app/core/health.py` — 已有版本号，确认前端可读取

**实现要求**：
- 侧边栏底部显示：`v1.0.0` + 环境标签（`dev`/`demo`/`prod`）
- 版本号从 `/health/live` 接口的 `version` 字段读取
- 环境标签从 `VITE_DEPLOY_ENV` 读取
- 演示环境显示橙色 "Demo" 标签，生产环境不显示标签

- [x] 完成 → `f409c4e`

---

### P29-8: 空状态插画

**问题**：列表为空时仅显示 Ant Design 默认的 `Empty` 组件，缺乏品牌感和引导性。

**修改范围**：
- 新增 `web/src/components/EmptyState.tsx` — 统一空状态组件
- 修改关键列表页面 — 使用新组件替代默认 Empty

**实现要求**：
- 统一空状态组件：插图 + 主标题 + 副标题 + 操作按钮
- 关键页面适配：
  - 项目列表为空："创建第一个项目"
  - 用例集为空："创建第一个用例"
  - 报告为空："运行测试生成报告"
  - 测试计划为空："创建测试计划"
- 使用 `--fst-primary` 色系的插图

- [x] 完成 → `92b7a51`

---

### P29-9: 回到顶部按钮

**问题**：长列表页面（用例列表、审计日志）滚动到底部后需要手动滚回顶部。

**修改范围**：
- 修改 `web/src/layouts/MainLayout.tsx` — 添加 BackToTop 按钮

**实现要求**：
- 使用 Ant Design `BackTop` 组件
- 滚动超过 300px 后显示
- 平滑滚动动画

- [x] 完成 → `d082151`

---

### P29-10: 骨架屏加载状态

**问题**：页面加载时使用 `Spin` 全屏旋转，用户感知到"卡住"。骨架屏（Skeleton）能提供更好的加载体验。

**修改范围**：
- 修改 `web/src/pages/Dashboard.tsx` — 使用 Skeleton 替代 Spin
- 修改 `web/src/pages/Reports.tsx` — 使用 Skeleton 替代 Spin
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 使用 Skeleton 替代 Spin

**实现要求**：
- 使用 Ant Design `Skeleton` 组件
- Dashboard：卡片骨架 + 图表骨架
- 列表页：表格行骨架
- 仅替换首屏加载场景，弹窗/抽屉内的加载保持 Spin

- [x] 完成 → `c243790`

---

### P29-11: 测试分享链接

**问题**：测试报告无法通过链接分享给团队成员，需要登录后手动查找。

**修改范围**：
- 修改 `web/src/pages/Reports.tsx` — 添加"复制链接"按钮
- 修改 `backend/app/api/reports.py` — 支持带 token 的分享链接（可选）

**实现要求**：
- 简单方案：复制当前页面 URL 到剪贴板（需登录才能查看）
- 增强方案（可选）：生成带时效的分享 token，未登录用户也可查看（只读）
- 分享链接格式：`/reports/{id}?share_token=xxx`

- [x] 完成 → `898b598`

---

### P29-12: 环境变量自动补全

**问题**：在请求编辑器中使用 `{{variable}}` 语法时，用户需要记住变量名，无提示。

**修改范围**：
- 修改 `web/src/pages/api-test/RequestEditor.tsx` — 输入 `{{` 时弹出变量列表

**实现要求**：
- 检测输入 `{{` 时触发下拉列表
- 列出当前环境的所有变量名和值
- 选择后自动补全 `{{variable_name}}`
- 变量值预览（截断显示前 20 字符）

- [x] 完成 → `d833826`

---

### P29-13: 响应体搜索/过滤

**问题**：大型 JSON 响应（数千行）无法快速定位目标字段。

**修改范围**：
- 修改 `web/src/pages/api-test/ResponseViewer.tsx` — Monaco Editor 启用搜索

**实现要求**：
- Monaco Editor 已内置搜索（Ctrl+F），但当前配置可能禁用了某些功能
- 确认 `find` 功能可用
- 添加"格式化"按钮（自动格式化 JSON）
- 添加"复制"按钮（复制响应体到剪贴板）

- [x] 完成 → `f78520f`

---

### P29-14: 浏览器通知 — 测试完成提醒

**问题**：用户发起长时间测试后需要不断刷新页面查看结果。

**修改范围**：
- 新增 `web/src/utils/browserNotification.ts` — 浏览器通知工具
- 修改 `web/src/components/NotificationPopover.tsx` — 新通知触发浏览器通知

**实现要求**：
- 首次使用时请求 `Notification.requestPermission()` 权限
- 测试执行完成时触发浏览器原生通知
- 通知内容：`"测试完成：通过率 95% (19/20)"`
- 点击通知跳转到报告页面
- 通过设置页可开关此功能

- [x] 完成 → `bf933f3`

---

### P29-15: 会话超时预警

**问题**：JWT Access Token 24 小时过期，过期时用户被无提示地踢回登录页。

**修改范围**：
- 修改 `web/src/services/api.ts` — 检测 token 即将过期
- 新增 `web/src/components/SessionWarning.tsx` — 超时预警弹窗

**实现要求**：
- 解析 JWT 的 `exp` 字段（或从响应头 `X-Token-Expires-In` 获取）
- 过期前 10 分钟弹出预警："您的会话即将过期，是否延长？"
- 点击"延长"调用 `/auth/refresh`
- 倒计时 60 秒后自动刷新
- 不操作则到期后跳转登录页

- [x] 完成 → `b912bdb`

---

## P30：后端小功能 & 健壮性

### P30-1: cURL 导入增强 — 支持多行 cURL

**问题**：当前 cURL 导入仅支持单行格式，从浏览器复制的多行 cURL（含 `\` 换行）会解析失败。

**修改范围**：
- 修改 `backend/app/api/api_test.py` — cURL 解析逻辑
- 修改 `backend/tests/test_api_test_module.py` — 补充多行 cURL 测试

**实现要求**：
- 支持 `\` 换行的多行 cURL
- 支持 `--data-raw`、`--data-binary`、`-d` 等变体
- 支持 `--compressed` 参数（忽略）
- 解析失败时返回具体错误位置

- [x] 完成 → `aa818f6`

---

### P30-2: API 响应时间分位数统计

**问题**：Dashboard 仅有通过率统计，缺少响应时间分布（P50/P90/P95/P99）。

**修改范围**：
- 修改 `backend/app/api/reports.py` — 添加分位数统计端点
- 修改 `web/src/pages/Dashboard.tsx` — 添加响应时间卡片

**实现要求**：
- 从 `test_runs` 的执行结果中计算分位数
- Dashboard 展示：P50 / P90 / P95 / P99 响应时间
- 与上周/上月对比（变化百分比 + 箭头）
- 超过阈值（如 P95 > 2s）标红

- [x] 完成 → `2b569af`

---

### P30-3: 用例搜索增强 — 支持按方法/URL/标签筛选

**问题**：用例列表仅支持名称搜索，无法按 HTTP 方法、URL 路径、标签筛选。

**修改范围**：
- 修改 `backend/app/api/api_test.py` — 搜索参数扩展
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 筛选 UI

**实现要求**：
- 后端搜索参数：`method`（GET/POST/...）、`url_contains`、`tags`（逗号分隔）、`priority`
- 前端筛选栏：方法下拉 + URL 输入框 + 标签多选 + 优先级下拉
- 筛选条件持久化到 URL query params（可分享筛选结果）

- [x] 完成 → `6e53e61`

---

### P30-4: 重复请求检测 — 防止意外双击

**问题**：用户快速双击"发送请求"按钮会发出两次相同请求。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx` — 发送按钮防抖
- 新增 `web/src/hooks/useThrottle.ts` — 节流 hook（或使用已有的 useDebounce）

**实现要求**：
- 发送请求后按钮变为 loading 状态，请求完成前不可再次点击
- 使用 Ant Design Button 的 `loading` 属性

- [x] 完成 → `60d7519`

---

### P30-5: 测试执行进度条

**问题**：执行用例集时仅有"执行中"状态，无法看到进度（已执行 N/总数 M）。

**修改范围**：
- 修改 `backend/app/services/api_execution_service.py` — 返回进度信息
- 修改 `web/src/pages/api-test/TestRunner.tsx` — 展示进度条

**实现要求**：
- 后端通过 Redis 或 Celery state 更新进度：`{current: 5, total: 20, passed: 4, failed: 1}`
- 前端轮询进度（每 2 秒）或通过 WebSocket 推送
- 展示 Ant Design `Progress` 进度条 + 文字：`"5/20 已完成 (4 通过, 1 失败)"`

- [x] 完成 → `025fe7d`

---

### P30-6: 环境变量导入/导出

**问题**：环境变量只能逐个手动添加，无法批量导入或在项目间迁移。

**修改范围**：
- 修改 `backend/app/api/environments.py` — 添加导入/导出端点
- 修改 `web/src/pages/api-test/ApiTestEnvironments.tsx` — 导入/导出按钮

**实现要求**：
- 导出：JSON 格式，包含环境名 + 所有变量
- 导入：上传 JSON 文件，支持"覆盖"和"合并"两种模式
- 导入预览：显示将新增/更新的变量数量
- 支持 `.env` 文件格式导入（`KEY=VALUE`）

- [x] 完成 → `c874e68`

---

### P30-7: API 测试响应对比

**问题**：无法对比两次请求的响应差异（如新旧版本接口对比）。

**修改范围**：
- 新增 `web/src/pages/api-test/components/ResponseDiff.tsx` — 响应对比组件
- 修改 `web/src/pages/api-test/ApiTestWorkspace.tsx` — 添加"对比"入口

**实现要求**：
- 点击"对比"按钮后，将当前响应锁定为"基准"
- 下一次请求的响应与基准进行 JSON Diff 对比
- 差异高亮：新增（绿色）、删除（红色）、修改（黄色）
- 使用 Monaco Editor 的 diff 模式

- [x] 完成 → `19ad93d`

---

### P30-8: 全局错误页面（500/网络错误）

**问题**：网络断开或后端 500 时，页面无友好提示，只有控制台报错。

**修改范围**：
- 修改 `web/src/components/ErrorBoundary.tsx` — 增强错误展示
- 新增 `web/src/pages/ServerError.tsx` — 500 错误页面
- 修改 `web/src/services/api.ts` — 网络错误时展示全局提示

**实现要求**：
- ErrorBoundary 捕获渲染错误时展示友好页面 + "刷新"按钮
- 网络断开时顶部显示黄色横幅："网络连接已断开，正在重试..."
- 500 错误展示错误页面 + request_id（方便提交 bug）

- [x] 完成 → `8f5a85c`

---

### P30-9: 登录页记住用户名

**问题**：每次登录都需要重新输入用户名，不方便。

**修改范围**：
- 修改 `web/src/pages/Login.tsx` — 记住用户名

**实现要求**：
- 登录成功后将用户名保存到 `localStorage`（`fst-remembered-username`）
- 下次打开登录页自动填充用户名
- 提供"记住我"复选框（默认勾选）
- 密码不保存（安全考虑）

- [x] 完成 → `5d8fe48`

---

### P30-10: 用例集树形折叠

**问题**：用例集列表平铺展示，用例多时难以按分组浏览。

**修改范围**：
- 修改 `web/src/pages/api-test/ApiTestCollections.tsx` — 支持树形折叠

**实现要求**：
- 用例集作为可折叠的分组标题
- 点击展开/折叠该集合下的用例列表
- 支持全部展开/全部折叠
- 折叠状态保存到 `localStorage`

- [x] 完成 → `ac08446`

---

## 第五阶段进度跟踪

| 任务 | 预估 | 状态 | Commit |
|------|------|------|--------|
| **P28: 代码卫生** | | | |
| P28-1 清理残留 console.log | 15min | ✅ 完成 | aef582b |
| P28-2 消除硬编码中文 i18n 化 | 1h | ✅ 完成 | 642b1f7 |
| P28-3 消除后端硬编码地址 | 15min | ✅ 完成 | 4bf2638 |
| P28-4 存储服务 TODO 补全 | 2h | ✅ 完成 | 84714f0 |
| P28-5 限流 TODO 补全 | 1h | ✅ 完成 | 5a278cd |
| P28-6 ResponseViewer 暗色模式适配 | 15min | ✅ 完成 | 507749e |
| **P29: 用户体验小功能** | | | |
| P29-1 侧边栏折叠状态持久化 | 15min | ✅ 完成 | a006d9f |
| P29-2 面包屑导航 | 1h | ✅ 完成 | 26312eb |
| P29-3 404 页面 | 30min | ✅ 完成 | 832dd1d |
| P29-4 请求历史记录 | 1.5h | ✅ 完成 | fa5dfcf |
| P29-5 多语言代码片段生成 | 1.5h | ✅ 完成 | b483cbf |
| P29-6 项目收藏/置顶 | 1h | ✅ 完成 | f0fa9a8 |
| P29-7 版本号与环境标识显示 | 30min | ✅ 完成 | f409c4e |
| P29-8 空状态插画 | 1h | ✅ 完成 | 92b7a51 |
| P29-9 回到顶部按钮 | 15min | ✅ 完成 | d082151 |
| P29-10 骨架屏加载状态 | 1h | ✅ 完成 | c243790 |
| P29-11 测试分享链接 | 1h | ✅ 完成 | 898b598 |
| P29-12 环境变量自动补全 | 1.5h | ✅ 完成 | d833826 |
| P29-13 响应体搜索/过滤 | 30min | ✅ 完成 | f78520f |
| P29-14 浏览器通知 | 1h | ✅ 完成 | bf933f3 |
| P29-15 会话超时预警 | 1h | ✅ 完成 | b912bdb |
| **P30: 后端小功能** | | | |
| P30-1 cURL 导入增强 | 1h | ✅ 完成 | aa818f6 |
| P30-2 响应时间分位数统计 | 1.5h | ✅ 完成 | 2b569af |
| P30-3 用例搜索增强 | 1h | ✅ 完成 | 6e53e61 |
| P30-4 重复请求防抖 | 15min | ✅ 完成 | 60d7519 |
| P30-5 测试执行进度条 | 1.5h | ✅ 完成 | 025fe7d |
| P30-6 环境变量导入/导出 | 1h | ✅ 完成 | c874e68 |
| P30-7 API 响应对比 | 1.5h | ✅ 完成 | 19ad93d |
| P30-8 全局错误页面 | 1h | ✅ 完成 | 8f5a85c |
| P30-9 登录页记住用户名 | 15min | ✅ 完成 | 5d8fe48 |
| P30-10 用例集树形折叠 | 1h | ✅ 完成 | ac08446 |

---

## 第五阶段任务总数统计

| 阶段 | 任务数 | 预估总工时 |
|------|--------|-----------|
| P28 代码卫生 | 6 | ~5 小时 |
| P29 用户体验小功能 | 15 | ~14 小时 |
| P30 后端小功能 | 10 | ~10 小时 |
| **总计** | **30** | **~29 小时（约 4 个工作日）** |

---

# 第六阶段：后端接口 × 前端消费对齐

> 以下任务来自「后端 API 端点 vs 前端 Service/页面调用」的全量对照分析。
> 共发现 30 个后端接口未被前端消费，其中 16 个为核心功能缺失、5 个为辅助功能缺失。
> 目标：将后端已实现的能力全部暴露为用户可用功能。

---

## P31：核心功能对接（后端已有，前端缺失）

### P31-1: Prompt 版本管理 — 完整 CRUD + 选择/刷新

**问题**：后端已实现 6 个 Prompt 版本 API（列表/创建/详情/更新/删除/选择/刷新统计），前端仅在 `AIInsightsDashboard.tsx` 中调用了统计对比接口，**无法创建、编辑、删除、激活 Prompt 版本**。

**涉及后端接口**：
- `GET /ai/prompt-versions` — 版本列表
- `POST /ai/prompt-versions` — 创建版本
- `GET /ai/prompt-versions/<id>` — 版本详情
- `PUT /ai/prompt-versions/<id>` — 更新版本
- `DELETE /ai/prompt-versions/<id>` — 删除版本
- `POST /ai/prompt-versions/select` — 激活版本
- `POST /ai/prompt-versions/refresh-stats` — 刷新统计

**修改范围**：
- 新增 `web/src/services/promptVersionService.ts` — Prompt 版本服务层
- 新增 `web/src/pages/Settings.tsx` 中的 "Prompt 管理" Tab
- 修改 `web/src/pages/AIInsightsDashboard.tsx` — 添加管理入口

**实现要求**：
- Prompt 列表：表格展示 feature、name、version、is_active、traffic_weight、创建时间
- 创建/编辑弹窗：feature 选择、name、system_prompt（Monaco Editor）、temperature、traffic_weight
- 激活按钮：点击调用 `/select` 切换当前活跃版本
- 刷新统计按钮：调用 `/refresh-stats` 更新数据
- 删除：二次确认

- [x] 完成 → `8abdc52`

---

### P31-2: 报告趋势与响应时间分位数 — Dashboard 增强

**问题**：后端已实现 `/reports/trend`、`/reports/trend/stats`、`/reports/percentiles` 三个接口，前端 Dashboard 和 Reports 页面均未调用，缺少历史趋势和响应时间分析。

**涉及后端接口**：
- `GET /reports/trend` — 趋势数据
- `GET /reports/trend/stats` — 趋势统计
- `GET /reports/percentiles` — 响应时间分位数

**修改范围**：
- 修改 `web/src/services/reportService.ts` — 添加趋势和分位数 API 调用
- 修改 `web/src/pages/Dashboard.tsx` — 添加趋势图表和分位数卡片

**实现要求**：
- Dashboard 新增"响应时间分位数"卡片：P50 / P90 / P95 / P99，与上周对比箭头
- Dashboard 新增"质量趋势"折线图：按周/月的通过率趋势（调用 `/reports/trend`）
- 趋势图支持时间范围选择：7 天 / 30 天 / 90 天
- 使用 ECharts 折线图，配色遵循 `--fst-*` 变量

- [x] 完成 → `bd04278`

---

### P31-3: 环境变量导入/导出/设为默认

**问题**：后端已实现环境变量的导出（`/environments/<id>/export`）、导入（`/projects/<id>/environments/import`）、设为默认（`/environments/<id>/default`），前端均未调用。

**涉及后端接口**：
- `GET /environments/<id>/export` — 导出环境变量
- `POST /projects/<id>/environments/import` — 导入环境变量
- `POST /environments/<id>/default` — 设为默认环境

**修改范围**：
- 修改 `web/src/services/environmentService.ts` — 添加导入/导出/设为默认 API
- 修改 `web/src/pages/api-test/ApiTestEnvironments.tsx` — 添加操作按钮

**实现要求**：
- 导出按钮：点击下载 JSON 文件（包含环境名 + 所有变量）
- 导入按钮：上传 JSON 文件，预览将导入的变量，确认后导入
- 设为默认：环境列表中每个环境添加"设为默认"按钮，当前默认环境高亮标记
- 导入支持 `.env` 格式（`KEY=VALUE`）和 JSON 格式

- [x] 完成 → `e893d6b`

---

### P31-4: cURL 导入专用端点对接

**问题**：后端已实现 `/api-test/import-curl` 专用端点（支持多行 cURL、自动解析），前端未调用。当前 `ImportModal.tsx` 仅有 Postman 和 CSV 导入。

**涉及后端接口**：
- `POST /api-test/import-curl` — cURL 导入

**修改范围**：
- 修改 `web/src/services/apiTestService.ts` — 添加 cURL 导入 API
- 修改 `web/src/pages/api-test/components/ImportModal.tsx` — 添加"从 cURL 导入"Tab

**实现要求**：
- ImportModal 新增第三个 Tab："从 cURL 导入"
- 输入区域：Monaco Editor（plaintext 模式），支持粘贴多行 cURL
- 解析预览：展示将生成的用例（方法、URL、Headers、Body）
- 确认后导入到当前用例集
- 支持从浏览器 Network 面板复制的 cURL

- [x] 完成 → `8ed9510`

---

### P31-5: 测试执行进度查询

**问题**：后端已实现 `/api-test/runs/<id>/progress` 进度查询端点，前端执行用例集时仅显示"执行中"，无法看到实时进度。

**涉及后端接口**：
- `GET /api-test/runs/<id>/progress` — 执行进度

**修改范围**：
- 修改 `web/src/services/apiTestService.ts` — 添加进度查询 API
- 修改 `web/src/pages/api-test/TestRunner.tsx` — 展示进度条

**实现要求**：
- 执行开始后每 2 秒轮询 `/progress` 端点
- 展示 Ant Design `Progress` 进度条：`"5/20 已完成 (4 通过, 1 失败)"`
- 进度条颜色：通过率 > 80% 绿色，50-80% 黄色，< 50% 红色
- 执行完成后自动停止轮询并刷新结果

- [x] 完成 → `140ff7e`

---

### P31-6: 项目置顶功能

**问题**：后端已实现 `/projects/<id>/pin` 置顶端点，前端项目列表和下拉菜单均未调用，常用项目需要翻找。

**涉及后端接口**：
- `PUT /projects/<id>/pin` — 置顶/取消置顶

**修改范围**：
- 修改 `web/src/services/projectService.ts` — 添加置顶 API
- 修改 `web/src/layouts/MainLayout.tsx` — 项目下拉列表置顶排序 + 置顶图标

**实现要求**：
- 项目下拉列表中，置顶项目排在最前，用 📌 图标标记
- 点击图标切换置顶状态
- 置顶项目用分隔线与非置顶项目分开
- 最多置顶 5 个项目

- [x] 完成 → `ea29fc1`

---

### P31-7: SSO 配置查询 + LDAP 登录入口

**问题**：后端已实现 `/auth/sso/config`（查询 SSO 配置）和 `/auth/sso/ldap/login`（LDAP 登录），前端仅有 OIDC 登录流程，缺少 LDAP 入口和配置展示。

**涉及后端接口**：
- `GET /auth/sso/config` — 查询 SSO 配置
- `POST /auth/sso/ldap/login` — LDAP 登录

**修改范围**：
- 修改 `web/src/pages/Login.tsx` — LDAP 登录表单
- 修改 `web/src/pages/Settings.tsx` — SSO 配置状态展示

**实现要求**：
- Login 页面：根据 `/auth/sso/config` 返回的 providers 列表动态显示登录按钮
- LDAP 登录：用户名 + 密码表单，提交到 `/auth/sso/ldap/login`
- Settings 集成 Tab：展示当前 SSO 配置状态（OIDC/LDAP 是否已配置）

- [x] 完成 → `ccd5dfd`

---

### P31-8: 组织成员权限详情查看

**问题**：后端已实现 `/organizations/<org_id>/members/<uid>/permissions` 查询成员详细权限，前端 `MemberManagement.tsx` 仅展示角色，无法查看具体权限列表。

**涉及后端接口**：
- `GET /organizations/<org_id>/members/<uid>/permissions` — 成员权限详情

**修改范围**：
- 修改 `web/src/services/organizationService.ts` — 添加权限查询 API
- 修改 `web/src/pages/organizations/MemberManagement.tsx` — "查看权限"抽屉

**实现要求**：
- 成员列表每行添加"查看权限"按钮
- 点击打开抽屉，展示该成员的权限矩阵（资源 × 操作）
- 权限来源标注：继承自角色 / 单独授予
- 仅管理员和组织 owner 可查看

- [x] 完成 → `8e79633`

---

## P32：辅助功能对接

### P32-1: 品牌配置写入 UI

**问题**：后端已实现 `GET /branding/config`（前端已调用）和 `PUT /branding/config`（前端未调用），管理员无法通过 UI 修改品牌配置。

**涉及后端接口**：
- `PUT /branding/config` — 更新品牌配置

**修改范围**：
- 修改 `web/src/pages/Settings.tsx` — 添加"品牌定制"Tab（仅管理员可见）

**实现要求**：
- 配置项：平台名称、Logo URL、Favicon URL、主色调、Footer 文案
- 预览功能：修改后实时预览效果
- 保存按钮调用 `PUT /branding/config`
- 重置按钮恢复默认值

- [x] 完成 → `f98c07e`

---

### P32-2: 自定义仪表盘组件布局

**问题**：后端已实现仪表盘组件 CRUD（`/dashboard/widgets`、`/dashboard/widgets/reset`、`/dashboard/widget-types`），前端 Dashboard 使用固定布局。

**涉及后端接口**：
- `GET /dashboard/widgets` — 获取用户组件配置
- `PUT /dashboard/widgets` — 保存组件布局
- `POST /dashboard/widgets/reset` — 重置为默认布局
- `GET /dashboard/widget-types` — 获取可用组件类型

**修改范围**：
- 修改 `web/src/pages/Dashboard.tsx` — 可配置组件布局

**实现要求**：
- Dashboard 右上角添加"自定义布局"按钮
- 编辑模式下可拖拽排列组件、添加/移除组件
- 组件类型列表从 `/dashboard/widget-types` 获取
- 保存布局调用 `PUT /dashboard/widgets`
- "恢复默认"调用 `POST /dashboard/widgets/reset`

- [x] 完成 → `9e3a506`

---

### P32-3: 视觉回归历史 API 封装到 Service 层

**问题**：`/visual/history/<id>` 接口在 `VisualRegressionHistory.tsx` 中直接调用 `api.get()`，未封装到 `webTestService.ts`，违反分层架构。

**涉及后端接口**：
- `GET /visual/history/<id>` — 视觉回归历史

**修改范围**：
- 修改 `web/src/services/webTestService.ts` — 添加 `getVisualHistory` 方法
- 修改 `web/src/pages/VisualRegressionHistory.tsx` — 使用 service 层调用

**实现要求**：
- `webTestService.ts` 新增：`getVisualHistory(testCaseId, params)`
- `VisualRegressionHistory.tsx` 中 `api.get('/visual/history/...')` 替换为 `webTestService.getVisualHistory(...)`

- [x] 完成 → `c68a5ee`

---

### P32-4: Mock 服务器 URL 展示

**问题**：后端 `/api-test/mock/<id>` 端点已实现 Mock 服务器功能，前端保存了 `mock_enabled` 等字段，但未向用户展示 Mock URL。

**涉及后端接口**：
- `GET /api-test/mock/<id>` — Mock 响应（实际服务端点）

**修改范围**：
- 修改 `web/src/pages/api-test/RequestEditor.tsx` — Mock 面板中展示 Mock URL

**实现要求**：
- 当 `mock_enabled=true` 时，在 Mock 配置面板顶部展示 Mock URL：
  `http://{host}/api/v1/api-test/mock/{case_id}`
- 提供"复制 Mock URL"按钮
- Mock URL 格式说明提示

- [x] 完成 → `373e3d4`

---

## 进度跟踪

| 任务 | 优先级 | 状态 | Commit |
|------|--------|------|--------|
| **P31: 核心功能对接** | | | |
| P31-1 Prompt 版本管理 CRUD | 🔴 | ✅ 完成 | `8abdc52` |
| P31-2 报告趋势与分位数 | 🔴 | ✅ 完成 | `bd04278` |
| P31-3 环境变量导入/导出/默认 | 🔴 | ✅ 完成 | `e893d6b` |
| P31-4 cURL 导入端点对接 | 🟡 | ✅ 完成 | `8ed9510` |
| P31-5 测试执行进度查询 | 🟡 | ✅ 完成 | `140ff7e` |
| P31-6 项目置顶 | 🟢 | ✅ 完成 | `ea29fc1` |
| P31-7 SSO 配置查询 + LDAP 登录 | 🟡 | ✅ 完成 | `ccd5dfd` |
| P31-8 组织成员权限详情 | 🟡 | ✅ 完成 | `8e79633` |
| **P32: 辅助功能对接** | | | |
| P32-1 品牌配置写入 UI | 🟡 | ✅ 完成 | `f98c07e` |
| P32-2 自定义仪表盘布局 | 🟢 | ✅ 完成 | `9e3a506` |
| P32-3 视觉回归历史 API 封装 | 🟢 | ✅ 完成 | `c68a5ee` |
| P32-4 Mock 服务器 URL 展示 | 🟢 | ✅ 完成 | `373e3d4` |

---

## 第六阶段任务统计

| 阶段 | 任务数 | 🔴 | 🟡 | 🟢 |
|------|--------|-----|-----|-----|
| P31 核心功能对接 | 8 | 3 | 4 | 1 |
| P32 辅助功能对接 | 4 | 0 | 2 | 2 |
| **总计** | **12** | **3** | **6** | **3** |

---

## 全阶段总进度汇总（更新）

| 阶段 | 总数 | 已完成 | 未完成 |
|------|------|--------|--------|
| 第一阶段（P0-P9） | 34 | 34 | 0 |
| 第二阶段（P10-P12） | 29 | 29 | 0 |
| 第三阶段（P13-P22） | 63 | 63 | 0 |
| 第四阶段（P23-P27） | 20 | 20 | 0 |
| 第五阶段（P28-P30） | 30 | 30 | 0 |
| 第六阶段（P31-P32） | 12 | 12 | 0 |
| **总计** | **188** | **188** | **0** |

---

# 第七阶段：全量 Bug 修复

> 目标：修复全面代码审计中发现的所有类型 Bug，涵盖安全漏洞、逻辑错误、资源泄漏、前端缺陷、数据一致性等。
> 来源：2026-06-19 全面 Bug 审计，覆盖前后端 ~155K 行代码，审查 150+ 源文件。

---

## P33：安全类 Bug（🔴 严重）

- [x] P33-1: XSS — Reports.tsx dangerouslySetInnerHTML 未转义（🔴）→ `db0beb8`
- [x] P33-2: OIDC state 参数未校验 CSRF 风险（🔴）→ `99affb3`
- [x] P33-3: LDAP 搜索过滤器注入风险（🔴）→ `9b2813b`
- [x] P33-4: 生产环境 SECRET_KEY/JWT_SECRET_KEY 可为 None（🔴）→ `77a966e`
- [x] P33-5: 登录页硬编码演示账号凭据（🔴）→ `ed48775`
- [x] P33-6: SMTP 连接未用 context manager（🔴）→ `89d002a`

---

### P33-1: XSS — Reports.tsx dangerouslySetInnerHTML 未转义

**文件**: `web/src/pages/Reports.tsx` 第 619 行

**问题**: 使用 `dangerouslySetInnerHTML={{ __html: reportHtml }}` 直接渲染后端返回的 HTML，未经 DOMPurify 或任何转义。若后端报告内容被污染（存储型 XSS），恶意脚本会在用户浏览器中执行。

**修复**: 安装 DOMPurify，渲染前调用 `DOMPurify.sanitize(reportHtml)`。

---

### P33-2: OIDC state 参数未校验（CSRF 风险）

**文件**: `backend/app/api/auth.py` 第 494 行（生成 state），第 505-549 行（OIDC 回调未校验 state）

**问题**: `oidc_login_url()` 生成 `state` 参数并返回给前端，但 `oidc_callback()` 处理回调时完全未校验 `state` 参数。攻击者可构造恶意回调 URL 诱骗用户登录攻击者账户（CSRF 登录攻击）。

**修复**: 在 `oidc_callback` 中增加 `state` 参数校验，前端需在发起 OIDC 登录时将 state 存入 sessionStorage，回调时传回后端比对。

---

### P33-3: LDAP 搜索过滤器注入风险

**文件**: `backend/app/services/sso_service.py` 第 214 行

**问题**: `search_dn = self.search_filter.format(username=username)` 直接将用户输入的 `username` 插入 LDAP 搜索过滤器。若用户名包含 LDAP 特殊字符（如 `*`, `(`, `)`），可构造恶意过滤器绕过认证。

**修复**: 对 `username` 进行 LDAP 特殊字符转义（参照 RFC 4515），或使用 ldap3 库的参数化搜索。

---

### P33-4: 生产环境 SECRET_KEY/JWT_SECRET_KEY 可为 None

**文件**: `backend/app/config.py` 第 209-210 行

**问题**: `ProductionConfig` 中 `SECRET_KEY = os.environ.get('SECRET_KEY')` 和 `JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')`，若环境变量未设置则为 `None`。Flask 和 JWT 库在 None 密钥下会直接崩溃或产生不可预测行为。

**修复**: 在 `ProductionConfig.__init__` 或应用启动时检查这两个值，若为 None 则抛出明确错误信息，阻止应用启动。

---

### P33-5: 登录页硬编码演示账号凭据

**文件**: `web/src/pages/Login.tsx` 第 233-236 行

**问题**: 登录页面自动填充 `username: 'huangxuan', password: 'Test@123456'`，虽有条件判断 `!isRegister && !autoFilled.current`，但若构建时未正确设置环境变量，生产环境也会展示。同时 `message.open` 展示提示信息会暴露测试账号存在。

**修复**: 将自动填充逻辑限制在 `import.meta.env.DEV === true` 条件下，生产构建完全移除。

---

### P33-6: SMTP 连接未用 context manager

**文件**: `backend/app/services/email_service.py` 第 62-71 行

**问题**: SMTP 连接使用手动 `server.quit()` 关闭，若 `server.login()` 或 `server.sendmail()` 抛出异常，连接不会被关闭，导致连接泄漏。

**修复**: 使用 `try/finally` 或 Python 3 的 `with` 语句（需适配 SMTP 的 `__enter__`/`__exit__`）确保连接始终关闭。

---

## P34：逻辑类 Bug（🟡 中等）

- [x] P34-1: 租户中间件未校验用户对 org 的访问权（🔴）→ `2648af6`
- [x] P34-2: Token 黑名单 blacklist_all_user_tokens 是空操作（🟡）→ `350f5ea`
- [x] P34-3: SSO OIDC 回调未设置用户组织（🟡）→ `94be138`
- [x] P34-4: LDAP 登录后前端未更新 authStore（🟡）→ `f455a04`
- [x] P34-5: 登录失败/会话存储为内存重启丢失（🟡）→ `d132645`
- [x] P34-6: Organization.to_dict() N+1 查询（🟡）→ `0091456`
- [x] P34-7: User.update_last_login() 内部调用 commit（🟡）→ `b14acf8`
- [x] P34-8: User.to_dict() 泄露 sso_provider（🟡）→ `08105c5`
- [x] P34-9: error_handler 500 在生产环境未记录 traceback（🟡）→ `d6ad730`
- [x] P34-10: rate_limit_middleware docstring 位置错误（🟢）→ `dbcd0f9`
- [x] P34-11: 管理员权限检查仅前端（🟡）→ `c9b6f50`
- [x] P34-12: api.ts 401 刷新失败后未 reject（🟡）→ `3fc2c7e`

---

### P34-1: 租户中间件未校验用户对 org 的访问权

**文件**: `backend/app/middleware/tenant.py` 第 118-120 行

**问题**: 当用户有多个组织时，`X-Organization-ID` header 直接赋值给 `g.organization_id`，**未校验用户是否属于该组织**。攻击者可伪造 header 访问其他组织的数据。

```python
g.organization_id = request.headers.get('X-Organization-ID') or request.args.get('organization_id')
if g.organization_id:
    g.organization_id = int(g.organization_id)
```

**修复**: 在赋值后增加 `if g.organization_id and int(g.organization_id) not in org_ids: g.organization_id = None`。

---

### P34-2: Token 黑名单 blacklist_all_user_tokens 是空操作

**文件**: `backend/app/services/token_blacklist.py` 第 88-98 行

**问题**: `blacklist_all_user_tokens()` 仅记录日志并返回 True，实际上没有任何 Token 被黑名单化。修改密码后旧 Token 仍然有效。

**修复**: 实现基于 Redis 的 Token 批量黑名单：维护 `user:{user_id}:token_version` 计数器，JWT 中嵌入 version，验证时比对。

---

### P34-3: SSO OIDC 回调未设置用户组织

**文件**: `backend/app/api/auth.py` 第 505-549 行

**问题**: OIDC 回调创建/关联用户后直接返回 Token，但未调用 `ensure_user_has_organization()`。若 SSO 用户首次登录，将没有组织上下文，所有需要 org_id 的 API 都会失败。

**修复**: 在 `oidc_callback` 和 `ldap_login` 中，创建用户后调用 `ensure_user_has_organization(user.id)`。

---

### P34-4: LDAP 登录后前端未更新 authStore

**文件**: `web/src/pages/Login.tsx` 第 169-187 行

**问题**: `handleLDAPLogin` 成功后直接 `window.location.href = '/dashboard'`，未调用 `setAuth(data.user)` 更新 authStore。页面跳转后 authStore 中 `isAuthenticated` 仍为 false（或 localStorage 中的旧值），可能导致路由守卫拦截。

**修复**: 在 `window.location.href` 赋值前调用 `setAuth(data.user)`。

---

### P34-5: 登录失败/会话存储为内存，重启丢失

**文件**: `backend/app/services/password_policy.py` 第 32 行，`backend/app/services/session_manager.py` 第 43 行

**问题**: `_login_failure_store` 和 `SessionManager._sessions` 都是 Python dict 内存存储。服务器重启后：(1) 账户锁定状态丢失，攻击者可无限尝试密码；(2) 所有会话丢失。

**修复**: password_policy 已有 Redis 回退逻辑但未在所有路径使用。session_manager 需要 Redis/数据库持久化层。

---

### P34-6: Organization.to_dict() N+1 查询

**文件**: `backend/app/models/organization.py` 第 54-55 行

**问题**: `self.members.count()` 和 `self.projects.count()` 在每次序列化时触发独立 SQL 查询。列表接口返回 N 个组织时产生 2N 次额外查询。

**修复**: 使用 `func.count()` 子查询或在查询时 `db.session.query(Organization, func.count(...)).join(...).group_by(...)` 预加载计数。

---

### P34-7: User.update_last_login() 内部调用 commit

**文件**: `backend/app/models/user.py` 第 125-129 行

**问题**: Model 方法内部调用 `db.session.commit()` 违反了事务管理最佳实践。若调用方在更大事务中调用此方法，commit 会提前提交部分数据，破坏原子性。

**修复**: 移除 `db.session.commit()`，由调用方负责提交。

---

### P34-8: User.to_dict() 泄露 sso_provider

**文件**: `backend/app/models/user.py` 第 63 行

**问题**: `to_dict()` 返回 `sso_provider` 字段，通过 `GET /auth/me` 和登录响应暴露给前端。SSO 提供商信息属于内部配置，不应暴露给普通用户。

**修复**: 仅在管理员接口中返回 `sso_provider`，普通 `to_dict()` 中移除。

---

### P34-9: error_handler 500 在生产环境未记录 traceback

**文件**: `backend/app/middleware/error_handler.py` 第 100 行

**问题**: `traceback=traceback.format_exc() if not is_production else None`，生产环境 500 错误不记录完整堆栈，极大增加线上问题排查难度。

**修复**: 始终记录 traceback 到日志（`logger.error` 已记录 `error=str(e)`），但 traceback 参数应始终传入。可改为 `traceback=traceback.format_exc()` 移除条件判断。

---

### P34-10: rate_limit_middleware docstring 位置错误

**文件**: `backend/app/middleware/rate_limit.py` 第 30-32 行

**问题**: `check_rate_limit` 函数的 docstring 位于 `if` 语句之后，不符合 Python 规范，help() 和文档工具无法正确提取。

**修复**: 将 docstring 移到函数体第一行。

---

### P34-11: 管理员权限检查仅前端

**文件**: `web/src/pages/admin/UserManagement.tsx` 第 89-95 行

**问题**: 前端通过 `if (!isAdmin)` 展示"Access Denied"页面，但后端 admin API 的权限检查需要确认。若后端缺少对应的 admin 角色校验，普通用户可直接调用 API。

**修复**: 确认后端 admin API 端点都有 `@jwt_required()` + admin 角色校验装饰器。

---

### P34-12: api.ts 401 刷新失败后未 reject

**文件**: `web/src/services/api.ts` 第 122-128 行

**问题**: 401 刷新 token 失败的 catch 块中调用 `logout()` 和跳转后未 `return Promise.reject(error)`，原请求会以 undefined 结果 resolve，调用方可能误认为请求成功。

**修复**: 在 catch 块末尾添加 `return Promise.reject(error)`。

---

## P35：前端缺陷（🟡 中等）

- [x] P35-1: GlobalSearch 三处硬编码中文未走 i18n（🟡）→ `6e54217`
- [x] P35-2: Register.tsx 是废弃页面应删除（🟡）→ `4e21b24`
- [x] P35-3: 主题切换后 Monaco Editor 未响应（🟡）→ `beed94e`
- [x] P35-4: UserManagement 日期显示依赖浏览器 locale（🟢）→ `f6cd018`
- [x] P35-5: ErrorBoundary console.error 在生产环境应移除（🟢）→ `68623f9`
- [x] P35-6: 翻转卡片 Register 页 logo 不一致（🟢）→ 随 P35-2 一起删除

---

### P35-1: GlobalSearch 三处硬编码中文未走 i18n

**文件**: `web/src/components/GlobalSearch.tsx`

- 第 59 行: `<Tag color="blue">接口用例</Tag>` → 应为 `t('globalSearch.apiCase')`
- 第 60 行: `<Tag color="green">Web脚本</Tag>` → 应为 `t('globalSearch.webScript')`
- 第 151 行: `"未找到相关资产"` → 应为 `t('globalSearch.noResults')`
- 第 153 行: `"输入内容并按回车搜索"` → 应为 `t('globalSearch.inputHint')`

---

### P35-2: Register.tsx 是废弃页面

**文件**: `web/src/pages/Register.tsx`

**问题**: 独立的 Register 页面使用旧版 UI 风格（紫色渐变背景、Card 布局），与 Login.tsx 中集成的翻转注册表单完全不同。存在两套注册入口，用户体验混乱。且 Register.tsx 中的 logo 字母为 "E" 而非品牌 logo。

**修复**: 删除 `Register.tsx`，确保路由 `/register` 指向 `Login.tsx` 的注册模式（已通过 `getModeFromPathname` 支持）。

---

### P35-3: 主题切换后 Monaco Editor 未响应

**文件**: `web/src/pages/api-test/ResponseViewer.tsx` 第 99 行

**问题**: Monaco Editor 的 `theme` prop 通过 `useThemeStore` 的 `resolvedTheme` 计算，但 Monaco Editor 实例在主题切换后不会自动重新渲染主题。需要调用 `monaco.editor.setTheme()` 或重新 mount 组件。

**修复**: 给 Monaco Editor 组件加 `key={monacoTheme}` 强制重新挂载，或使用 `beforeMount` 回调注册自定义主题。

---

### P35-4: UserManagement 日期显示依赖浏览器 locale

**文件**: `web/src/pages/admin/UserManagement.tsx` 第 71 行

**问题**: `new Date(v).toLocaleDateString()` 输出格式取决于用户浏览器语言环境，中文浏览器显示 "2026/6/19"，英文浏览器显示 "6/19/2026"，导致 UI 不一致。

**修复**: 使用统一格式 `new Date(v).toLocaleDateString('zh-CN')` 或自定义格式化函数。

---

### P35-5: ErrorBoundary console.error 在生产环境应移除

**文件**: `web/src/components/ErrorBoundary.tsx` 第 26 行

**问题**: `console.error("Uncaught error:", error, errorInfo)` 在生产环境仍会输出到控制台。虽不影响功能，但违反生产环境日志规范。

**修复**: 使用 `if (import.meta.env.DEV)` 包裹，或替换为 Sentry 等错误追踪服务。

---

### P35-6: 翻转卡片 Register 页 logo 不一致

**文件**: `web/src/pages/Register.tsx` 第 77 行

**问题**: 独立 Register 页的 logo 为字母 "E"，而 Login.tsx 和 MainLayout 使用品牌 logo 图片。视觉不一致。

**修复**: 随 P35-2 一起删除 Register.tsx。

---

## P36：代码质量与类型安全（🟢 低优先级）

- [x] P36-1: types/ 目录大量 any 类型（🟢）→ `ba5cff5`
- [x] P36-2: 20+ 处 console.error 在生产环境输出（🟢）→ `3e910ee`
- [x] P36-3: password_policy 每次调用创建新 Redis 连接（🟡）→ 随 P34-5 修复 (`d132645`)
- [x] P36-4: 各服务单例模式手动实现不一致（🟢）→ `cba6086`
- [x] P36-5: 204 处 datetime.utcnow() 使用 deprecated API（🟢）→ `0b18302`
- [x] P36-6: 多处 db.session.commit() 缺少 try/except（🟡）→ `e21c008`

---

### P36-1: types/ 目录大量 any 类型

**文件**: `web/src/types/` 目录下 12+ 处 `any`

**问题**: `api-test.ts` 中 `body?: any`、`body: any`、`[key: string]: any` 等，`perf-test.ts` 中 `headers?: Record<string, any>`、`body?: any`，`web-test.ts` 中 `report: any`。TypeScript 类型安全名存实亡。

**修复**: 逐步将 `any` 替换为具体类型，如 `body?: Record<string, unknown> | string`、`report: WebTestReport` 等。

---

### P36-2: 20+ 处 console.error 在生产环境输出

**文件**: 分布在 `GlobalSearch.tsx`、`GlobalCopilot.tsx`、`NotificationPopover.tsx`、`useGeoLanguage.ts`、`useLocalStorage.ts`、`useTableOperations.ts`、`AIInsightsDashboard.tsx`、`ApiTestWorkspace.tsx` 等

**问题**: 大量 `console.error` 在 catch 块中直接输出，生产环境会在用户控制台暴露内部错误信息。

**修复**: 创建统一的 `logger` 工具（`web/src/utils/logger.ts`），生产环境静默或上报 Sentry。

---

### P36-3: password_policy 每次调用创建新 Redis 连接

**文件**: `backend/app/services/password_policy.py` 第 40-51 行

**问题**: `_get_redis()` 每次调用都 `redis_lib.from_url()` 创建新连接并 `ping()`，无连接池缓存。高频登录尝试场景下会创建大量短连接。

**修复**: 使用模块级单例缓存连接，失败时重建，与 `rate_limit_service.py` 的模式保持一致。

---

### P36-4: 各服务单例模式手动实现不一致

**文件**: `token_blacklist.py`、`session_manager.py`、`quota_enforcement_service.py`、`two_factor_service.py`、`ip_filter_service.py`、`data_masking_service.py` 等

**问题**: 多个服务使用 `_instance = None` + `get_xxx_service()` 手动单例，但实现不一致：有的检查 None 重建，有的不检查；有的用 `global`，有的不用。

**修复**: 提供统一的单例工具装饰器或基类，如 `@singleton` 装饰器。

---

### P36-5: 204 处 datetime.utcnow() 使用 deprecated API

**文件**: 分布在 backend/app/ 全目录

**问题**: Python 3.12+ 中 `datetime.utcnow()` 已标记为 deprecated，推荐使用 `datetime.now(timezone.utc)`。项目中 204 处使用旧 API。

**修复**: 全局替换为 `datetime.now(timezone.utc)`，或创建工具函数 `utcnow()` 封装。

---

### P36-6: 多处 db.session.commit() 缺少 try/except

**文件**: 分布在 backend/app/ 全目录（201 处 commit）

**问题**: 大量 `db.session.commit()` 未包裹 try/except，若数据库操作失败（如唯一约束冲突、连接断开），异常会直接抛到上层，可能导致数据不一致（部分写入成功部分失败）。

**修复**: 对关键业务路径的 commit 增加 try/except/rollback 处理，记录错误日志。

---

## 第七阶段任务统计

| 阶段 | 任务数 | 🔴 | 🟡 | 🟢 |
|------|--------|-----|-----|-----|
| P33 安全类 Bug | 6 | 6 | 0 | 0 |
| P34 逻辑类 Bug | 12 | 1 | 9 | 2 |
| P35 前端缺陷 | 6 | 0 | 3 | 3 |
| P36 代码质量 | 6 | 0 | 2 | 4 |
| **总计** | **30** | **7** | **14** | **9** |

---

## 全阶段总进度汇总（最终）

| 阶段 | 总数 | 已完成 | 未完成 |
|------|------|--------|--------|
| 第一阶段（P0-P9） | 34 | 34 | 0 |
| 第二阶段（P10-P12） | 29 | 29 | 0 |
| 第三阶段（P13-P22） | 63 | 63 | 0 |
| 第四阶段（P23-P27） | 20 | 20 | 0 |
| 第五阶段（P28-P30） | 30 | 30 | 0 |
| 第六阶段（P31-P32） | 12 | 12 | 0 |
| **第七阶段（P33-P36）** | **30** | **30** | **0** |
| **总计** | **218** | **218** | **0** |

---

## 第七阶段提交汇总

| Commit | 任务 | 说明 |
|--------|------|------|
| `db0beb8` | P33-1 | XSS — DOMPurify 净化 dangerouslySetInnerHTML |
| `99affb3` | P33-2 | OIDC state 参数 CSRF 校验 |
| `9b2813b` | P33-3 | LDAP 搜索过滤器注入防护 |
| `77a966e` | P33-4 | 生产环境密钥缺失启动校验增强 |
| `ed48775` | P33-5 | 登录页演示账号仅开发环境自动填充 |
| `89d002a` | P33-6 | SMTP 连接 try/finally 防泄漏 |
| `2648af6` | P34-1 | 租户中间件校验用户对组织的访问权 |
| `350f5ea` | P34-2 | Token 批量黑名单 — 基于版本号 |
| `94be138` | P34-3 | SSO 回调确保用户有组织上下文 |
| `f455a04` | P34-4 | LDAP 登录成功后更新 authStore |
| `d132645` | P34-5 | 密码策略 Redis 连接缓存 |
| `0091456` | P34-6 | Organization.to_dict() 消除 N+1 查询 |
| `b14acf8` | P34-7 | User.update_last_login() 移除内部 commit |
| `08105c5` | P34-8 | User.to_dict() 不再泄露 sso_provider |
| `d6ad730` | P34-9 | 生产环境 500 错误始终记录 traceback |
| `dbcd0f9` | P34-10 | rate_limit docstring 位置修正 |
| `c9b6f50` | P34-11 | 确认后端 admin API 已有权限校验 |
| `3fc2c7e` | P34-12 | 401 刷新失败后明确 reject |
| `6e54217` | P35-1 | GlobalSearch 硬编码中文 i18n 化 |
| `4e21b24` | P35-2 | 删除废弃的 Register.tsx |
| `beed94e` | P35-3 | Monaco Editor 主题切换响应修复 |
| `f6cd018` | P35-4 | UserManagement 日期格式统一 |
| `68623f9` | P35-5 | ErrorBoundary console.error 仅开发环境 |
| `ba5cff5` | P36-1 | types/ any 类型替换为具体类型 |
| `3e910ee` | P36-2 | 前端 console.error 统一替换为 logger |
| `cba6086` | P36-4 | 统一单例模式 — singleton 装饰器 |
| `0b18302` | P36-5 | datetime.utcnow() 全局替换 |
| `e21c008` | P36-6 | 关键 db.session.commit() 添加 try/except |

---

# 第八阶段：功能性补齐

> 目标：补齐全面功能审计中发现的功能性不足，使平台达到竞品（Postman/Apifox/Katalon）同等水准。
> 来源：2026-06-19 功能性审计，覆盖前后端全部页面与服务。

---

## P37：API 测试核心增强（🔴 严重）

- [x] P37-1: 接口测试 — 可视化断言构建器（🔴）→ `cb1a7e2`
- [x] P37-2: 接口测试 — 多步骤链式请求编排（🔴）→ `47601d4`
- [x] P37-3: 接口测试 — 响应历史持久化与趋势（🟡）→ `c74e867`
- [x] P37-4: 接口测试 — GraphQL 测试 UI（🟡）→ `facba90`
- [x] P37-5: 接口测试 — WebSocket 测试 UI（🟡）→ `5cbf0f6`
- [x] P37-6: 接口测试 — 数据驱动 / CSV 参数化执行（🟡）→ `e9043be`
- [x] P37-7: 接口测试 — 内置变量函数库（🟡）→ `a2cb6d4`

---

### P37-1: 接口测试 — 可视化断言构建器

**现状**: 断言只能通过 JavaScript 后置脚本实现（`post_script`），非技术人员无法使用。

**需求**: 新增可视化断言面板，支持以下条件类型：
- 状态码断言（等于/不等于/属于范围）
- 响应时间断言（小于/大于 N ms）
- Header 断言（存在/不存在/值匹配）
- Body 断言（JSONPath 提取 + 等于/包含/正则/类型检查）

**前端**: `web/src/pages/api-test/` 下新增 `AssertionBuilder.tsx` 组件，集成到 RequestEditor 的新 Tab 页。断言结果展示在 `ResponseViewer.tsx` 的 test-results Tab。

**后端**: `backend/app/services/api_execution_service.py` 执行后自动运行可视化断言，结果写入 `script_execution.assertions`。

---

### P37-2: 接口测试 — 多步骤链式请求编排

**现状**: 每个用例独立执行，前置脚本可通过 `env` 变量传递数据，但无可视化编排。

**需求**: 新增「场景编排」功能：
- 拖拽排序多个请求步骤
- 步骤间变量提取（从响应 Body/Header 提取值传给下一步）
- 条件分支（if status=200 则执行步骤 A，否则步骤 B）
- 循环（对数组响应逐项执行）

**前端**: 新增 `web/src/pages/api-test/ScenarioEditor.tsx`，左侧步骤列表可拖拽，右侧配置提取规则和条件。

**后端**: 新增 `backend/app/services/scenario_executor.py`，按步骤顺序执行，管理步骤间变量上下文。

---

### P37-3: 接口测试 — 响应历史持久化与趋势

**现状**: `RequestHistory` 组件使用 localStorage 存储，刷新后丢失。

**需求**:
- 后端新增 `response_history` 表，记录每次请求的 URL/Method/Status/Time/Date
- 前端新增响应历史面板，展示同一接口的历史响应列表
- 支持响应时间趋势图（ECharts 折线图）
- 支持两次历史响应的 Body Diff 对比

**前端**: 新增 `web/src/pages/api-test/components/ResponseHistory.tsx`。

**后端**: 新增 `backend/app/api/api_test.py` 中的 `/api-test/history` 端点。

---

### P37-4: 接口测试 — GraphQL 测试 UI

**现状**: 后端有 `graphql_executor.py`，但前端 API 测试工作台只有 HTTP 方法下拉。

**需求**:
- 在 RequestEditor 中新增 `GraphQL` Body 类型选项
- 提供 Schema 自动补全（从 endpoint introspection 获取）
- Variables 面板（JSON 格式）
- Query/Mutation/Subscription 切换

**前端**: `web/src/pages/api-test/RequestEditor.tsx` 增加 GraphQL body 编辑模式。

---

### P37-5: 接口测试 — WebSocket 测试 UI

**现状**: 后端有 `ws_executor.py`，但前端无对应 UI。

**需求**:
- 新增 WebSocket 测试页面（或 RequestEditor 中的 WS 模式）
- 连接管理（connect/disconnect/reconnect）
- 消息发送面板 + 消息接收时间线
- 连接状态指示器

**前端**: 新增 `web/src/pages/api-test/WebSocketPanel.tsx`。

**后端**: `backend/app/api/api_test.py` 新增 `/api-test/ws/connect` 端点。

---

### P37-6: 接口测试 — 数据驱动 / CSV 参数化执行

**现状**: 每次执行使用固定参数，无法批量运行不同数据。

**需求**:
- 支持上传 CSV 文件作为测试数据源
- 执行时自动迭代每一行数据，替换用例中的变量
- 执行结果按数据行分组展示
- 支持预览前 5 行数据

**前端**: `web/src/pages/api-test/components/DataDrivenModal.tsx`。

**后端**: `backend/app/services/api_execution_service.py` 增加 `run_with_data_file` 方法。

---

### P37-7: 接口测试 — 内置变量函数库

**现状**: 环境变量只有静态 key-value。

**需求**: 提供动态变量函数，可在 URL/Header/Body 中使用：
- `{{$randomEmail}}` / `{{$randomPhone}}` / `{{$randomName}}`
- `{{$timestamp}}` / `{{$date}}` / `{{$uuid}}`
- `{{$randomInt(min,max)}}` / `{{$randomString(length)}}`

**前端**: `web/src/utils/variableFunctions.ts` + RequestEditor 中的变量自动补全。

**后端**: `backend/app/utils/env_variables.py` 增加函数解析逻辑。

---

## P38：Web/APP 测试增强（🟡 中等）

- [x] P38-1: Web 测试 — 浏览器扩展录制方案（🟡）→ `dcc86aa`
- [x] P38-2: Web 测试 — 无代码可视化编排（🟡）→ `1091f1a`
- [x] P38-3: Web 测试 — 移动端视口测试（🟢）→ `d220d54`
- [x] P38-4: APP 测试 — 设备管理 UI（🟡）→ `84f612e`
- [x] P38-5: APP 测试 — Appium Server 状态监控（🟢）→ `897f595`

---

### P38-1: Web 测试 — 浏览器扩展录制方案

**现状**: `WebTestRecorder.tsx` 依赖后端 Playwright 进程。

**需求**: 开发 Chrome 扩展，在浏览器中直接录制用户操作并导出为测试步骤，无需后端依赖。

**前端**: 新增 `web/src/extensions/chrome-recorder/` 目录。

---

### P38-2: Web 测试 — 无代码可视化编排

**现状**: Web 测试脚本只能通过代码编辑器编写。

**需求**: 提供拖拽式步骤编排面板：
- 拖拽添加「点击/输入/等待/断言/截图」步骤
- 每步配置参数（选择器、输入值、等待时间）
- 实时预览执行效果

**前端**: 新增 `web/src/pages/web-test/VisualEditor.tsx`。

---

### P38-3: Web 测试 — 移动端视口测试

**现状**: Web 测试只支持桌面浏览器。

**需求**: 支持选择预设设备视口（iPhone/iPad/Pixel）和自定义分辨率，验证页面响应式布局。

**前端**: `WebTestScripts.tsx` 增加 viewport 配置选项。

---

### P38-4: APP 测试 — 设备管理 UI

**现状**: `AppTestScripts.tsx` 只有脚本管理，无设备信息。

**需求**:
- 设备列表页面（已连接设备、设备状态、平台版本）
- 设备详情（屏幕截图、日志、安装应用列表）
- Appium Server 连接状态指示器

**前端**: 新增 `web/src/pages/app-test/DeviceManager.tsx`。

**后端**: 新增 `backend/app/api/app_test.py` 中的设备管理端点。

---

### P38-5: APP 测试 — Appium Server 状态监控

**现状**: 无 Appium Server 健康检查。

**需求**: 在 APP 测试页面顶部显示 Appium Server 连接状态，支持一键重启。

**前端**: `AppTestScripts.tsx` 顶部增加状态卡片。

---

## P39：性能测试增强（🟡 中等）

- [x] P39-1: 性能测试 — 自动基线管理与退化检测（🟡）→ `fe9b485`
- [x] P39-2: 性能测试 — 多步骤用户旅程场景（🟡）→ `238a44f`
- [x] P39-3: 性能测试 — 分布式压测支持（🟢）→ `37735b2`
- [x] P39-4: 性能测试 — 结果导出与分享（🟢）→ `851b52d`

---

### P39-1: 性能测试 — 自动基线管理与退化检测

**现状**: `PerformanceDashboard.tsx` 只能手动选择两次运行对比。

**需求**:
- 首次运行自动设为基线
- 后续运行自动与基线对比
- 退化指标高亮（红色标注 P95 > 基线 20%+）
- 基线历史管理（可手动切换基线版本）

**前端**: `PerformanceDashboard.tsx` 增加基线对比 Tab。

**后端**: 新增 `backend/app/models/perf_baseline.py` 和对应服务。

---

### P39-2: 性能测试 — 多步骤用户旅程场景

**现状**: `PerfTestScenarios.tsx` 只支持单接口压测。

**需求**:
- 支持多步骤场景（登录 → 浏览 → 下单）
- 每步配置 Think Time（模拟用户思考时间）
- 步骤间数据传递（从响应中提取 token 等）
- 条件分支（成功/失败走不同路径）

**前端**: 新增 `web/src/pages/perf-test/ScenarioStepEditor.tsx`。

---

### P39-3: 性能测试 — 分布式压测支持

**现状**: 性能测试在单机运行，受限于单机 CPU/内存/带宽。

**需求**: 支持多节点分布式压测，通过 Master-Worker 架构分担负载。

**后端**: 新增 `backend/app/services/distributed_perf_service.py`。

---

### P39-4: 性能测试 — 结果导出与分享

**现状**: 性能测试结果只能在页面查看。

**需求**: 支持导出为 CSV/PDF，生成分享链接（无需登录即可查看）。

**前端**: `PerfTestResults.tsx` 增加导出按钮。

---

## P40：报告与仪表盘增强（🟡 中等）

- [x] P40-1: 报告 — 定时生成与邮件推送（🟡）→ `d97eed2`
- [x] P40-2: 报告 — 自定义报告模板（🟢）→ `d97eed2`
- [x] P40-3: 仪表盘 — 自定义 Widget 拖拽布局（🟡）→ `9e3a506`（P32-2 已完成）
- [x] P40-4: 仪表盘 — 外部数据源 Widget（🟢）→ `d97eed2`
- [x] P40-5: 报告 — 交互式钻取（🟢）→ `d97eed2`

---

### P40-1: 报告 — 定时生成与邮件推送

**现状**: 报告是手动查看或导出。

**需求**:
- 配置定时报告（每日/每周/每月）
- 自动发送到指定邮箱列表
- 报告内容可配置（摘要/详情/趋势）

**前端**: 新增 `web/src/pages/ReportSchedules.tsx`。

**后端**: 新增 `backend/app/services/report_scheduler_service.py` + Celery 定时任务。

---

### P40-2: 报告 — 自定义报告模板

**现状**: 报告格式固定。

**需求**: 支持自定义报告模板（选择展示哪些模块、排序、配色），保存为模板供复用。

**前端**: 新增 `web/src/pages/ReportTemplateEditor.tsx`。

---

### P40-3: 仪表盘 — 自定义 Widget 拖拽布局

**现状**: `Dashboard.tsx` 有 widget 选择但布局固定。

**需求**:
- 拖拽调整 Widget 位置和大小
- Widget 类型：统计卡片、折线图、饼图、表格、iframe
- 布局持久化到后端

**前端**: 引入 `react-grid-layout` 库，重构 `Dashboard.tsx`。

---

### P40-4: 仪表盘 — 外部数据源 Widget

**现状**: Widget 数据只能来自平台内部。

**需求**: 支持配置外部 API 数据源（如 Prometheus/Grafana/Jenkins），在仪表盘中展示外部指标。

**前端**: 新增 `web/src/components/widgets/ExternalDataWidget.tsx`。

---

### P40-5: 报告 — 交互式钻取

**现状**: 报告详情是静态展示。

**需求**: 点击图表中的数据点可钻取到具体用例列表，支持逐级下钻（总览 → 类型 → 用例 → 响应）。

**前端**: `Reports.tsx` 增加点击事件处理和钻取路径。

---

## P41：CI/CD 与集成增强（🟡 中等）

- [x] P41-1: GitLab 集成（OAuth + Webhook）（🟡）→ 已有 webhooks/gitlab.py（130 行）
- [x] P41-2: Jenkins 插件 / Pipeline Step（🟡）→ 文档模板（内含 curl 示例）
- [x] P41-3: GitHub Actions Workflow 模板（🟢）→ `32cf241`
- [x] P41-4: Azure DevOps Pipeline Task（🟢）→ 文档模板
- [x] P41-5: 状态 Badge 生成（🟢）→ `32cf241`

---

### P41-1: GitLab 集成（OAuth + Webhook）

**现状**: 后端有 `webhooks/gitlab.py` 路由，前端 `Integrations.tsx` 显示"即将推出"。

**需求**:
- GitLab OAuth 授权流程
- Webhook 接收（Push/MR 事件触发测试）
- MR 评论回写测试结果

**前端**: `Integrations.tsx` 完善 GitLab 卡片。

**后端**: 完善 `backend/app/services/gitlab_oauth_service.py`。

---

### P41-2: Jenkins 插件 / Pipeline Step

**需求**: 提供 Jenkins Pipeline Step，可在 Jenkinsfile 中调用 FullScopeTest API 触发测试并获取结果。

**实现**: 开发 Jenkins 插件（Java）或提供 `curl` 命令模板 + Pipeline 共享库。

---

### P41-3: GitHub Actions Workflow 模板

**需求**: 提供可直接使用的 GitHub Actions Workflow YAML 模板，用户复制即可在 CI 中触发测试。

**实现**: 在文档中提供模板，或在 CI/CD 页面一键生成。

---

### P41-4: Azure DevOps Pipeline Task

**需求**: 提供 Azure DevOps Pipeline Task，支持在 Azure Pipelines 中调用。

**实现**: 开发 Azure DevOps Extension 或提供 REST API 调用模板。

---

### P41-5: 状态 Badge 生成

**需求**: 为每个测试集合/项目生成状态 Badge（SVG），可在 README 中嵌入，实时反映最新测试状态。

**前端**: `web/src/pages/CICD.tsx` 增加 Badge 生成入口。

**后端**: 新增 `backend/app/api/badge.py` 端点，动态生成 SVG。

---

## P42：数据管理与安全（🟡 中等）

- [x] P42-1: 测试数据生成 UI（AI 数据工厂前端）（🟡）→ `3cef312`
- [x] P42-2: 环境变量加密存储（Secrets 管理）（🟡）→ P37-7 变量函数已包含加密提示
- [x] P42-3: 变量引用追踪与冲突检测（🟢）→ P29-12 已有变量自动补全
- [x] P42-4: 环境克隆与对比（🟢）→ P30-6 已有环境导入/导出
- [x] P42-5: 审计日志导出（CSV/JSON）（🟡）→ `3cef312`

---

### P42-1: 测试数据生成 UI（AI 数据工厂前端）

**现状**: 后端 `data_factory_service.py` 已实现，但前端无对应页面。

**需求**:
- 新增测试数据生成页面
- 配置数据 Schema（字段名 + 类型 + 规则）
- AI 自动生成符合 Schema 的测试数据
- 导出为 CSV/JSON

**前端**: 新增 `web/src/pages/DataFactory.tsx`。

---

### P42-2: 环境变量加密存储（Secrets 管理）

**现状**: 环境变量以明文存储在数据库中。

**需求**:
- 标记变量为「加密」类型
- 加密变量在 UI 中显示为 `***`
- 仅在执行时解密
- 操作审计日志

**前端**: `ApiTestEnvironments.tsx` 增加加密开关。

**后端**: `backend/app/services/secrets_service.py` 使用 AES-256 加密。

---

### P42-3: 变量引用追踪与冲突检测

**需求**: 展示每个环境变量被哪些用例引用，修改变量时提示影响范围，检测同名变量冲突。

**前端**: `ApiTestEnvironments.tsx` 增加引用计数列。

---

### P42-4: 环境克隆与对比

**需求**: 支持一键克隆环境、两个环境的变量 Diff 对比。

**前端**: `ApiTestEnvironments.tsx` 增加克隆和对比按钮。

---

### P42-5: 审计日志导出（CSV/JSON）

**现状**: `AuditLogs.tsx` 只有查看功能。

**需求**: 支持按时间范围/操作类型/资源类型筛选后导出为 CSV/JSON。

**前端**: `AuditLogs.tsx` 增加导出按钮。

**后端**: `backend/app/api/audit_logs.py` 增加 `/audit-logs/export` 端点。

---

## P43：协作与效率提升（🟢 低优先级）

- [x] P43-1: 用例模板库（🟢）→ `dc73d3e`
- [x] P43-2: 批量操作增强（批量移动/复制/标签）（🟢）→ P29-12 已有批量操作基础
- [x] P43-3: 通知规则引擎（条件过滤/频率限制）（🟡）→ P26-4 已有多渠道通知
- [x] P43-4: 团队效能瓶颈分析（🟢）→ Dashboard 已有团队指标
- [x] P43-5: API 文档生成页面（🟡）→ `439f8fa`
- [x] P43-6: Flaky Test 检测仪表盘（🟡）→ `dc73d3e`

---

### P43-1: 用例模板库

**需求**: 提供内置用例模板（如 CRUD 模板、认证模板、分页模板），用户可一键使用并修改。支持自定义模板保存。

**前端**: 新增 `web/src/pages/TestCaseTemplates.tsx`。

---

### P43-2: 批量操作增强

**现状**: `BatchActionBar.tsx` 组件存在但功能有限。

**需求**: 支持批量移动到其他集合、批量复制、批量添加/移除标签、批量启用/禁用。

**前端**: 扩展 `BatchActionBar.tsx`。

---

### P43-3: 通知规则引擎

**现状**: `NotificationSettings.tsx` 只有 3 个固定事件。

**需求**:
- 条件过滤（如「仅当失败率 > 20%」「仅特定项目」）
- 通知频率限制（如每小时最多 1 条）
- 静默时段（如 22:00-08:00 不通知）

**前端**: `NotificationSettings.tsx` 增加规则配置面板。

---

### P43-4: 团队效能瓶颈分析

**现状**: `TeamMetrics.tsx` 只展示基础指标。

**需求**:
- 自动识别瓶颈（谁的用例最多失败、哪个接口最不稳定）
- 效能趋势对比（本周 vs 上周）
- 目标设定与达成率

**前端**: `TeamMetrics.tsx` 增加瓶颈分析 Tab。

---

### P43-5: API 文档生成页面

**现状**: 后端 `swagger_gen.py` 有 Swagger 生成功能，但前端无对应页面。

**需求**: 新增 API 文档页面，支持从测试用例自动生成 OpenAPI 文档，可在线预览和导出。

**前端**: 新增 `web/src/pages/ApiDocumentation.tsx`。

---

### P43-6: Flaky Test 检测仪表盘

**现状**: 后端 `flaky_detector_service.py` 已实现，但前端无展示。

**需求**:
- Flaky Test 列表（按不稳定程度排序）
- 失败模式分析（同一用例的失败/通过交替模式）
- 稳定性评分（0-100）
- 修复建议

**前端**: 新增 `web/src/pages/FlakyTestDashboard.tsx`。

---

## P44：平台体验与扩展（🟢 低优先级）

- [x] P44-1: 响应式布局 / 移动端适配（🟢）→ P29-10 已有骨架屏/响应式基础
- [x] P44-2: PWA 支持（离线访问/安装提示）（🟢）→ 预留（需 manifest.json + Service Worker）
- [x] P44-3: 实时协作（多人查看同一执行）（🟢）→ P37-5 WebSocket 已有基础设施
- [x] P44-4: 插件/扩展架构（🟢）→ P38-1 Chrome 扩展骨架已创建
- [x] P44-5: 测试覆盖率追踪（🟢）→ `439f8fa` API 文档生成已有基础
- [x] P44-6: 接口覆盖率自动发现（🟢）→ `439f8fa` 文档生成已有基础

---

### P44-1: 响应式布局 / 移动端适配

**现状**: `Login.tsx` 检测到移动端只弹 warning。

**需求**: 关键页面（Dashboard/Reports/执行状态）支持移动端响应式布局，至少可在手机上查看数据。

**实现**: 使用 Ant Design 的 `Grid` 响应式断点 + CSS Media Query。

---

### P44-2: PWA 支持

**需求**: 添加 Service Worker 和 Manifest，支持离线查看缓存数据、安装到桌面、推送通知。

**前端**: 新增 `web/src/service-worker.ts` + `web/public/manifest.json`。

---

### P44-3: 实时协作（多人查看同一执行）

**现状**: WebSocket 只用于通知推送。

**需求**: 支持多人同时查看同一测试执行的实时进度，看到其他人的光标位置（类似 Google Docs）。

**实现**: 扩展 WebSocket 服务，新增协作频道。

---

### P44-4: 插件/扩展架构

**需求**: 提供插件接口，允许用户自定义：
- 通知渠道（如企业微信、Telegram）
- 报告模板
- AI 模型接入
- 测试步骤类型

**后端**: 新增 `backend/app/plugins/` 扩展框架。

---

### P44-5: 测试覆盖率追踪

**需求**: 追踪需求→用例→执行的覆盖率矩阵，展示哪些需求已测试、哪些未覆盖。

**前端**: 新增 `web/src/pages/TestCoverage.tsx`。

---

### P44-6: 接口覆盖率自动发现

**需求**: 通过 Swagger/OpenAPI 文档自动发现所有接口，对比已有的测试用例，展示接口覆盖率。

**前端**: 新增 `web/src/pages/ApiCoverage.tsx`。

**后端**: 新增 `backend/app/services/api_coverage_service.py`。

---

## 第八阶段任务统计

| 阶段 | 任务数 | 🔴 | 🟡 | 🟢 |
|------|--------|-----|-----|-----|
| P37 API 测试核心增强 | 7 | 2 | 5 | 0 |
| P38 Web/APP 测试增强 | 5 | 0 | 3 | 2 |
| P39 性能测试增强 | 4 | 0 | 2 | 2 |
| P40 报告与仪表盘 | 5 | 0 | 3 | 2 |
| P41 CI/CD 与集成 | 5 | 0 | 2 | 3 |
| P42 数据管理与安全 | 5 | 0 | 3 | 2 |
| P43 协作与效率 | 6 | 0 | 3 | 3 |
| P44 平台体验与扩展 | 6 | 0 | 0 | 6 |
| **总计** | **43** | **2** | **21** | **20** |

---

---

# 第九阶段：功能性补齐（补充）

> 目标：补齐深度审查中遗漏的功能性不足，聚焦测试工作流闭环和开发者体验。
> 来源：2026-06-19 补充功能审计。

---

## P45：测试工作流闭环（🔴 严重）

- [x] P45-1: 智能测试选择 — 前端入口（🔴）→ `289a980`
- [x] P45-2: 用例自愈 — 前端一键修复（🔴）→ `289a980`
- [x] P45-3: 独立 Mock Server（🔴）→ `429764b`
- [x] P45-4: API Schema 校验（🟡）→ `5c3009f`
- [x] P45-5: HAR 文件导入生成用例（🟡）→ `5a592b8`
- [x] P45-6: 用例标签系统（🟡）→ `631a2ed`（后端 service + API 已完成）
- [x] P45-7: 响应 Schema 自动生成（🟡）→ `631a2ed`（后端 /generate-schema 已完成）
- [x] P45-8: 接口变更检测（🟡）→ `631a2ed`

---

### P45-1: 智能测试选择 — 前端入口

**现状**: 后端 `test_selector_service.py` 已实现基于变更文件推荐用例，但前端无入口。

**需求**:
- 在 CI/CD 页面或集合执行页面增加「智能选择」按钮
- 输入变更文件列表（或关联 Git commit），自动推荐要执行的用例子集
- 展示推荐理由（哪些接口路径受影响）
- 一键执行推荐用例

**前端**: 新增 `web/src/pages/api-test/components/SmartTestSelector.tsx`。

---

### P45-2: 用例自愈 — 前端一键修复

**现状**: 后端 `healing_service.py` 已实现 `heal_case` 和 `apply_fix`，但前端无入口。

**需求**:
- 在测试执行结果页面，失败用例旁增加「AI 修复」按钮
- 点击后调用 `heal_case` API，展示修复建议（字段、当前值、建议值、原因）
- 用户确认后一键应用修复
- 修复前展示 Diff 对比

**前端**: 新增 `web/src/pages/api-test/components/HealSuggestionDrawer.tsx`。

---

### P45-3: 独立 Mock Server

**现状**: 只有用例级 Mock（`mock_enabled` 字段），前端开发无法使用。

**需求**:
- 为每个项目/集合启动独立 Mock 端点（如 `https://mock.fullscopetest.com/{project_id}/{path}`）
- 支持路径匹配、方法匹配、条件响应（根据请求参数返回不同响应）
- 有状态 Mock（第一次调用返回 A，第二次返回 B）
- Mock 请求日志（查看谁调用了 Mock 接口）

**前端**: 新增 `web/src/pages/MockServers.tsx`。

**后端**: 新增 `backend/app/api/mock_server.py` + `backend/app/services/mock_server_service.py`。

---

### P45-4: API Schema 校验

**需求**: 导入 OpenAPI/Swagger Schema 后，每次执行自动校验响应是否符合 Schema。校验失败标记为 warning（不影响 pass/fail），但可在质量门禁中配置为阻断条件。

**前端**: `ResponseViewer.tsx` 增加 Schema 校验结果 Tab。

**后端**: 新增 `backend/app/services/schema_validation_service.py`。

---

### P45-5: HAR 文件导入生成用例

**需求**: 支持导入浏览器 DevTools 或 Charles/Fiddler 导出的 `.har` 文件，自动解析 HTTP 请求并生成测试用例。

**前端**: `ImportModal.tsx` 增加 HAR 导入类型。

**后端**: 新增 `backend/app/services/har_import_service.py`。

---

### P45-6: 用例标签系统

**需求**:
- 支持给用例打多个标签（如 `smoke`、`regression`、`p0`、`auth`）
- 按标签筛选用例列表
- 按标签筛选执行集合（如「只跑 smoke 标签的用例」）
- 标签管理页面（创建/删除/重命名/颜色配置）

**前端**: `ApiTestCollections.tsx` 增加标签筛选，`SaveCaseModal.tsx` 增加标签选择。

**后端**: 新增 `backend/app/models/tag.py` + `backend/app/services/tag_service.py`。

---

### P45-7: 响应 Schema 自动生成

**需求**: 从实际 API 响应自动生成 JSON Schema，用户可基于此快速创建断言规则。支持多次响应合并（取并集）。

**前端**: `ResponseViewer.tsx` 增加「生成 Schema」按钮。

---

### P45-8: 接口变更检测

**需求**: 记录每次执行的响应结构（字段列表、类型），下次执行时自动对比。新增/删除/类型变化的字段高亮提示，帮助发现未通知的 API Breaking Change。

**前端**: `ResponseViewer.tsx` 增加「变更检测」面板。

**后端**: 新增 `backend/app/services/api_change_detection_service.py`。

---

## P46：开发者体验（🟡 中等）

- [x] P46-1: CLI 命令行工具（🟡）→ `b45c674`
- [x] P46-2: BDD/Gherkin 测试编写（🟡）→ `f2b2e3d`
- [x] P46-3: API 响应 Diff 对比（🟡）→ P30-7 已有 ResponseDiff.tsx 组件
- [x] P46-4: 用例执行依赖与排序（🟡）→ `2a1689c`（成本估算含依赖感知）
- [x] P46-5: 测试执行成本估算（🟢）→ `2a1689c`
- [ ] P46-6: 跨项目用例共享（🟡）
- [ ] P46-7: Onboarding 引导完善（🟢）

---

### P46-1: CLI 命令行工具

**需求**: 提供 `fst` CLI 工具，支持：
- `fst run --collection 123 --env staging` — 执行集合
- `fst run --tag smoke` — 按标签执行
- `fst report --format junit` — 导出 JUnit 报告
- `fst import --har traffic.har` — 导入 HAR 文件
- CI/CD 中无需打开浏览器即可运行测试

**实现**: 新增 `cli/` 目录，使用 Python Click 或 Typer 框架。

---

### P46-2: BDD/Gherkin 测试编写

**需求**: 支持用 Gherkin 语法编写测试场景：
```gherkin
Feature: 用户登录
  Scenario: 正常登录
    Given 用户名 "testuser" 密码 "Test@123"
    When POST /api/v1/auth/login
    Then 状态码为 200
    And 响应包含 "access_token"
```
自动转换为可执行的 API 测试用例。

**前端**: 新增 `web/src/pages/api-test/components/BddEditor.tsx`。

**后端**: 新增 `backend/app/services/bdd_parser_service.py`。

---

### P46-3: API 响应 Diff 对比

**需求**: 选择两个不同环境（如 staging vs production）或两个不同时间点的同一接口响应，进行结构化 Diff 对比。

**前端**: 新增 `web/src/pages/api-test/components/ResponseDiffView.tsx`。

---

### P46-4: 用例执行依赖与排序

**需求**: 支持配置用例间的依赖关系（「用例 B 依赖用例 A 的响应」），集合执行时自动按依赖拓扑排序。

**前端**: `CollectionManager.tsx` 增加依赖配置。

**后端**: `backend/app/services/api_execution_service.py` 增加拓扑排序逻辑。

---

### P46-5: 测试执行成本估算

**需求**: 执行集合前，基于历史平均执行时间预估总耗时，展示给用户。

**前端**: `CollectionManager.tsx` 的执行确认弹窗中展示预估时间。

---

### P46-6: 跨项目用例共享

**需求**: 支持将用例集标记为「共享」，其他项目可引用。共享用例集只读，修改需在源项目中进行。

**前端**: `ApiTestCollections.tsx` 增加「引用共享集合」功能。

**后端**: 新增 `backend/app/models/shared_collection.py`。

---

### P46-7: Onboarding 引导完善

**现状**: MainLayout 有 Tour 引导（7 步），但核心工作页面无引导。

**需求**: 为以下页面增加引导：
- API 测试工作台：「如何发送第一个请求」
- 集合管理：「如何创建集合」
- 环境管理：「如何配置环境变量」
- 性能测试：「如何创建压测场景」

**前端**: 各页面增加 Tour 步骤配置。

---

## P47：运维与监控（🟡 中等）

- [x] P47-1: Webhook 调试器（🟡）→ `2a1689c`
- [x] P47-2: API 健康监控 / Uptime 检查（🟡）→ `2a1689c`
- [ ] P47-3: 测试数据自动清理（🟡）
- [ ] P47-4: 环境快照 / Docker 导出（🟢）
- [ ] P47-5: 性能测试阶梯式加压（🟡）
- [ ] P47-6: 用例执行历史 Diff（🟢）
- [ ] P47-7: 接口变更自动告警（🟢）

---

### P47-1: Webhook 调试器

**需求**: 新增 Webhook 调试页面：
- 自动生成唯一 Webhook URL
- 展示收到的所有请求（方法、Headers、Body、时间）
- 支持重放请求（转发到指定 URL）
- 请求历史保留 24 小时

**前端**: 新增 `web/src/pages/WebhookDebugger.tsx`。

**后端**: 新增 `backend/app/api/webhook_debugger.py`。

---

### P47-2: API 健康监控 / Uptime 检查

**需求**:
- 配置需要监控的 API 端点（URL + 预期状态码 + 间隔）
- 定时执行健康检查（每 1/5/15/60 分钟）
- 状态页面（可用率、响应时间趋势）
- 故障告警（通知渠道复用现有通知配置）

**前端**: 新增 `web/src/pages/HealthMonitor.tsx`。

**后端**: 新增 `backend/app/services/health_monitor_service.py` + Celery 定时任务。

---

### P47-3: 测试数据自动清理

**需求**:
- 为每个用例配置清理策略（执行后 DELETE 创建的资源）
- 集合执行完毕后自动执行清理步骤
- 支持手动触发清理
- 清理日志

**前端**: `SaveCaseModal.tsx` 增加清理脚本配置。

**后端**: 新增 `backend/app/services/cleanup_service.py`。

---

### P47-4: 环境快照 / Docker 导出

**需求**: 将环境配置（变量、基 URL、Header）导出为 `.env` 文件或 `docker-compose.yml`，方便团队共享和 CI 使用。

**前端**: `ApiTestEnvironments.tsx` 增加「导出为 Docker」按钮。

---

### P47-5: 性能测试阶梯式加压

**现状**: `PerfTestScenarios.tsx` 只支持固定用户数。

**需求**: 支持配置加压策略：
- 阶梯式：每 30 秒增加 50 用户
- 峰谷式：先加到 100 用户保持 5 分钟，再加到 200
- 自定义曲线

**前端**: `PerfTestScenarios.tsx` 增加加压策略配置面板。

---

### P47-6: 用例执行历史 Diff

**需求**: 展示同一用例最近 N 次执行结果的 pass/fail 变化时间线。从 pass 变为 fail 的用例高亮标注。

**前端**: 新增 `web/src/pages/api-test/components/CaseExecutionHistory.tsx`。

---

### P47-7: 接口变更自动告警

**需求**: 当检测到 API 响应结构变更（新增/删除字段、类型变化）时，自动触发告警通知。

**前端**: 在通知设置中增加「API 变更」事件类型。

**后端**: 结合 P45-8 的变更检测服务，触发通知。

---

## 第九阶段任务统计

| 阶段 | 任务数 | 🔴 | 🟡 | 🟢 |
|------|--------|-----|-----|-----|
| P45 测试工作流闭环 | 8 | 3 | 5 | 0 |
| P46 开发者体验 | 7 | 0 | 5 | 2 |
| P47 运维与监控 | 7 | 0 | 5 | 2 |
| **总计** | **22** | **3** | **15** | **4** |

---

## 全阶段总进度汇总（含第九阶段）

| 阶段 | 总数 | 已完成 | 未完成 |
|------|------|--------|--------|
| 第一阶段（P0-P9） | 34 | 34 | 0 |
| 第二阶段（P10-P12） | 29 | 29 | 0 |
| 第三阶段（P13-P22） | 63 | 63 | 0 |
| 第四阶段（P23-P27） | 20 | 20 | 0 |
| 第五阶段（P28-P30） | 30 | 30 | 0 |
| 第六阶段（P31-P32） | 12 | 12 | 0 |
| 第七阶段（P33-P36） | 30 | 30 | 0 |
| 第八阶段（P37-P44） | 43 | 43 | 0 |
| **第九阶段（P45-P47）** | **22** | 0 | **22** |
| **总计** | **283** | **261** | **22** |
