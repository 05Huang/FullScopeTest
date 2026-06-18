# FullScopeTest 功能路线图

> 最后更新：2026-06-19

## 已上线 ✅

### 2025-2026 H1
- ✅ API 接口测试工作台（环境变量/脚本/断言/cURL/Mock）
- ✅ Web UI 自动化（Playwright/视觉回归/VNC Live View）
- ✅ 性能压测（Locust/分布式/实时大盘/告警引擎）
- ✅ APP 测试脚本管理（Appium Android/iOS）
- ✅ AI Copilot 自然语言编排
- ✅ NL2Script 脚本自动生成
- ✅ 智能错误分析与自愈
- ✅ Prompt 版本管理与 A/B 测试
- ✅ 语义去重（向量化 + 余弦相似度）
- ✅ 多租户隔离 + RBAC 权限
- ✅ 审计日志
- ✅ SSO 集成（OIDC/LDAP，Beta）
- ✅ 中英文国际化
- ✅ 暗色模式
- ✅ Docker Compose 部署
- ✅ K8s Helm Chart 部署
- ✅ GitHub Actions CI/CD 集成
- ✅ 邮件服务（SMTP/SendGrid）
- ✅ 计费系统（Free/Pro/Enterprise）
- ✅ 品牌定制（白标）

---

## 开发中 🔧

### Q3 2026（2026.07 — 2026.09）

| 功能 | 状态 | 说明 |
|------|------|------|
| 邮件通知集成 | 开发中 | 基于 P24-1 EmailService 的通知渠道 |
| 飞书/钉钉/Slack 通知 | 计划中 | Webhook + 签名验证 + 富文本卡片 |
| 自定义仪表盘 | 计划中 | 可拖拽网格布局，8 个预设组件 |
| 更多协议支持 | 计划中 | gRPC/GraphQL/WebSocket 测试 |
| cURL 导入增强 | 计划中 | 多行 cURL/变体参数/错误定位 |

---

## 计划中 📋

### Q4 2026（2026.10 — 2026.12）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 设备农场集成 | 高 | 云设备远程执行 APP 测试（BrowserStack/Sauce Labs） |
| API 响应对比 | 中 | 两次请求的 JSON Diff 对比 |
| 测试执行进度条 | 中 | 实时 N/M 进度 + 通过/失败统计 |
| 环境变量自动补全 | 中 | `{{` 触发变量列表下拉 |
| 浏览器通知 | 低 | 测试完成时原生 Notification 提醒 |
| 会话超时预警 | 低 | JWT 过期前 10 分钟弹窗提示 |
| 请求历史记录 | 低 | 最近 50 条请求自动保存 |
| 404 页面 | 低 | 友好 404 提示 + 返回首页 |
| 面包屑导航 | 低 | 根据路由自动生成 |

### Q1 2027（2027.01 — 2027.03）

| 功能 | 优先级 | 说明 |
|------|--------|------|
| AI Agent 自主测试 | 高 | 给定 URL + 目标，AI 自主遍历页面执行探索测试 |
| 设备农场深度集成 | 高 | 内置设备管理 + 实时日志 + 录屏 |
| FastAPI v2 迁移完成 | 中 | 将剩余 Flask 端点迁移到 FastAPI |
| 新手引导（Tour Guide） | 中 | 7 步交互式引导覆盖核心功能 |
| 测试分享链接 | 低 | 带时效 token 的报告分享 |

---

## 技术债务清理

| 项目 | 优先级 | 说明 |
|------|--------|------|
| 前端测试覆盖率 → 50% | 中 | 当前 36 个测试文件，目标 50+ |
| 数据库迁移规范化 | 低 | 确保所有 Model 变更均有 migration |
| API 版本化 | 低 | v1/v2 并行，逐步迁移 |

---

## 反馈

如有功能需求或建议，请通过以下方式联系我们：
- GitHub Issues: [05Huang/FullScopeTest](https://github.com/05Huang/FullScopeTest/issues)
- 邮箱: support@fullscopetest.com
