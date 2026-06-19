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

- [ ] P34-1: 租户中间件未校验用户对 org 的访问权（🔴）
- [ ] P34-2: Token 黑名单 blacklist_all_user_tokens 是空操作（🟡）
- [ ] P34-3: SSO OIDC 回调未设置用户组织（🟡）
- [ ] P34-4: LDAP 登录后前端未更新 authStore（🟡）
- [ ] P34-5: 登录失败/会话存储为内存重启丢失（🟡）
- [ ] P34-6: Organization.to_dict() N+1 查询（🟡）
- [ ] P34-7: User.update_last_login() 内部调用 commit（🟡）
- [ ] P34-8: User.to_dict() 泄露 sso_provider（🟡）
- [ ] P34-9: error_handler 500 在生产环境未记录 traceback（🟡）
- [ ] P34-10: rate_limit_middleware docstring 位置错误（🟢）
- [ ] P34-11: 管理员权限检查仅前端（🟡）
- [ ] P34-12: api.ts 401 刷新失败后未 reject（🟡）

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

- [ ] P35-1: GlobalSearch 三处硬编码中文未走 i18n（🟡）
- [ ] P35-2: Register.tsx 是废弃页面应删除（🟡）
- [ ] P35-3: 主题切换后 Monaco Editor 未响应（🟡）
- [ ] P35-4: UserManagement 日期显示依赖浏览器 locale（🟢）
- [ ] P35-5: ErrorBoundary console.error 在生产环境应移除（🟢）
- [ ] P35-6: 翻转卡片 Register 页 logo 不一致（🟢）

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

- [ ] P36-1: types/ 目录大量 any 类型（🟢）
- [ ] P36-2: 20+ 处 console.error 在生产环境输出（🟢）
- [ ] P36-3: password_policy 每次调用创建新 Redis 连接（🟡）
- [ ] P36-4: 各服务单例模式手动实现不一致（🟢）
- [ ] P36-5: 204 处 datetime.utcnow() 使用 deprecated API（🟢）
- [ ] P36-6: 多处 db.session.commit() 缺少 try/except（🟡）

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
| **第七阶段（P33-P36）** | **30** | 0 | **30** |
| **总计** | **218** | **188** | **30** |
