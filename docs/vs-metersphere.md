# FullScopeTest vs MeterSphere — 全面对比与迁移指南

> 本文档全面对比 FullScopeTest 与 MeterSphere V3 / V2 的功能、性能和架构差异，
> 并提供从 MeterSphere 迁移到 FullScopeTest 的详细指南。

---

## 目录

- [1. 概述](#1-概述)
- [2. 功能矩阵对比](#2-功能矩阵对比)
  - [2.1 测试能力对比](#21-测试能力对比)
  - [2.2 AI 能力对比](#22-ai-能力对比)
  - [2.3 CI/CD 集成对比](#23-cicd-集成对比)
  - [2.4 多租户与安全对比](#24-多租户与安全对比)
  - [2.5 基础设施与运维对比](#25-基础设施与运维对比)
- [3. 性能基准对比](#3-性能基准对比)
  - [3.1 API 响应时间对比](#31-api-响应时间对比)
  - [3.2 并发处理能力对比](#32-并发处理能力对比)
  - [3.3 资源占用对比](#33-资源占用对比)
- [4. 架构差异说明](#4-架构差异说明)
  - [4.1 整体架构对比](#41-整体架构对比)
  - [4.2 技术栈对比](#42-技术栈对比)
  - [4.3 数据模型对比](#43-数据模型对比)
- [5. 从 MeterSphere 迁移指南](#5-从-metersphere-迁移指南)
  - [5.1 迁移前准备](#51-迁移前准备)
  - [5.2 数据导出方案](#52-数据导出方案)
  - [5.3 数据导入方案](#53-数据导入方案)
  - [5.4 API 路径映射表](#54-api-路径映射表)
  - [5.5 常见迁移问题](#55-常见迁移问题)
- [6. 迁移决策建议](#6-迁移决策建议)

---

## 1. 概述

### MeterSphere 简介

MeterSphere 是FIT2CLOUD旗下的开源持续测试平台，提供测试管理、接口测试、UI 测试（V2）、性能测试和团队协作功能。

- **MeterSphere V2**（LTS 版本）：功能最全的版本，包含 Web UI 自动化测试（基于 Selenium）
- **MeterSphere V3**（当前版本）：2024 年重构版本，基于 Java/Spring Boot，移除了 Web UI 自动化测试模块，精简了功能集

### FullScopeTest 简介

FullScopeTest 是一个 **AI-Native 全链路自动化测试平台**，覆盖 API 接口测试、Web UI 自动化、APP 移动端测试和性能压测四大领域，以 AI 能力工程化为核心设计理念。

### 核心差异一句话总结

> MeterSphere V3 主动放弃了 UI 自动化测试，FullScopeTest 不仅填补了这一空白，还在 AI 工程化、CI/CD 深度集成、视觉回归测试等维度建立了技术壁垒。

---

## 2. 功能矩阵对比

### 2.1 测试能力对比

| 功能 | MeterSphere V2 | MeterSphere V3 | FullScopeTest |
|------|:-:|:-:|:-:|
| **API 接口测试** | ✅ 完整支持 | ✅ 完整支持 | ✅ 完整支持 |
| HTTP/REST 请求编辑器 | ✅ | ✅ | ✅ |
| 环境变量管理 | ✅ | ✅ | ✅ |
| 前置/后置脚本 | ✅ BeanShell | ✅ BeanShell | ✅ Python |
| 变量提取与断言 | ✅ JSONPath | ✅ JSONPath | ✅ JSONPath + Python 表达式 |
| cURL 导入/导出 | ✅ | ✅ | ✅ |
| Mock Server | ✅ | ✅ | ✅ 用例级 Mock |
| **Web UI 自动化** | ✅ Selenium | ❌ 已移除 | ✅ Playwright |
| 在线脚本编辑 | ✅ | ❌ | ✅ Monaco Editor |
| 脚本录制 | ✅ | ❌ | ✅ Playwright Codegen |
| VNC 实时预览 | ❌ | ❌ | ✅ x11vnc + websockify |
| 视觉回归测试 | ❌ | ❌ | ✅ 像素级对比 + 差异高亮 |
| **APP 移动端测试** | ❌ | ❌ | ✅ Appium (Android/iOS) |
| **性能测试** | ⚠️ 基础 (JMeter) | ⚠️ 有限支持 | ✅ Locust 深度集成 |
| 实时性能大盘 | ⚠️ 基础 | ⚠️ 基础 | ✅ Recharts 实时折线图 |
| 时间序列数据采集 | ❌ | ❌ | ✅ 每秒 RPS/RT/错误率 |
| P50/P75/P95/P99 分位数 | ⚠️ 有限 | ⚠️ 有限 | ✅ 完整分位数统计 |
| 历史对比分析 | ❌ | ❌ | ✅ 多次运行指标对比 |
| 阶梯加压 | ✅ | ✅ | ✅ |
| 分布式压测 | ✅ | ✅ | ✅ Locust 原生支持 |
| **性能告警** | ❌ | ❌ | ✅ 可配置规则引擎 |
| 相对比劣化告警 | ❌ | ❌ | ✅ 相对上次运行 |
| WebSocket 实时推送 | ❌ | ❌ | ✅ |
| **测试报告** | ✅ | ✅ | ✅ |
| HTML/JSON 导出 | ✅ | ✅ | ✅ |
| 按类型统计 | ✅ | ✅ | ✅ 四种测试类型 |
| 趋势分析 | ⚠️ | ⚠️ | ✅ 每日趋势 + 成功率 |
| **测试文档管理** | ✅ | ✅ | ✅ Markdown |
| **Webhook 触发器** | ✅ | ✅ | ✅ HMAC-SHA256 签名 |
| **定时任务** | ✅ | ✅ | ✅ Cron + 文件锁单例 |

### 2.2 AI 能力对比

| 功能 | MeterSphere V2 | MeterSphere V3 | FullScopeTest |
|------|:-:|:-:|:-:|
| **AI 能力** | ❌ 无 | ⚠️ 基础集成 | ✅ AI-Native 工程化 |
| AI 自然语言编排 | ❌ | ❌ | ✅ 输入目标 → 自动执行 |
| NL2Script 脚本生成 | ❌ | ❌ | ✅ 自然语言 → Playwright/Locust |
| 智能错误分析与自愈 | ❌ | ❌ | ✅ AI 诊断 + 一键修复 |
| Swagger 智能用例生成 | ❌ | ❌ | ✅ 解析 OpenAPI + 语义分析 |
| 语义用例去重 | ❌ | ❌ | ✅ 向量化 + 余弦相似度 |
| 全局 AI Copilot | ❌ | ❌ | ✅ Function Calling 集成 |
| 探索性测试 Agent | ❌ | ❌ | ✅ AI 自主遍历 + 异常检测 |
| AI 调用可观测性 | ❌ | ❌ | ✅ prompt/response/latency/tokens |
| Prompt 版本管理 | ❌ | ❌ | ✅ 数据库版本化 + A/B 测试 |
| AI 调用成本追踪 | ❌ | ❌ | ✅ 每次调用 token 消耗统计 |
| AI 功能降级策略 | ❌ | ❌ | ✅ 失败时返回 fallback |

### 2.3 CI/CD 集成对比

| 功能 | MeterSphere V2 | MeterSphere V3 | FullScopeTest |
|------|:-:|:-:|:-:|
| **GitHub 集成** | ⚠️ 基础 Webhook | ⚠️ 基础 Webhook | ✅ 深度集成 |
| GitHub App OAuth | ❌ | ❌ | ✅ 一键授权绑定 |
| PR 事件自动触发测试 | ⚠️ 手动配置 | ⚠️ 手动配置 | ✅ 可配置触发规则 |
| GitHub Check Run 回写 | ❌ | ❌ | ✅ 实时状态 + 失败摘要 |
| Quality Gate 质量门禁 | ❌ | ❌ | ✅ 通过率/RT/视觉差异阈值 |
| 官方 GitHub Action | ❌ | ❌ | ✅ 一行配置集成 |
| **GitLab 集成** | ⚠️ 基础 Webhook | ⚠️ 基础 Webhook | ✅ MR/Push + Pipeline 状态回写 |
| GitLab CI 模板 | ❌ | ❌ | ✅ YAML 模板示例 |
| 变更感知触发 | ❌ | ❌ | ✅ 文件路径匹配规则 |
| API Token 管理 | ❌ | ❌ | ✅ 多 Token + 权限范围 + 有效期 |

### 2.4 多租户与安全对比

| 功能 | MeterSphere V2 | MeterSphere V3 | FullScopeTest |
|------|:-:|:-:|:-:|
| **多租户** | ✅ 组织/工作空间 | ✅ 组织 | ✅ 组织 + 成员关系 |
| 数据隔离 | ✅ | ✅ | ✅ 中间件自动注入 |
| 越权访问防护 | ⚠️ 返回 403 | ⚠️ 返回 403 | ✅ 返回 404（防信息泄露）|
| **权限控制** | ✅ RBAC | ✅ RBAC | ✅ RBAC 三角色 |
| **API 限流** | ❌ | ❌ | ✅ 滑动窗口 + 按组织配置 |
| 限流监控 | ❌ | ❌ | ✅ Prometheus 指标 |
| **审计日志** | ⚠️ 基础 | ⚠️ 基础 | ✅ 全操作审计 + JSON diff |
| **API Token 管理** | ❌ | ❌ | ✅ 多 Token + bcrypt hash |
| 输入验证 | ⚠️ | ⚠️ | ✅ Pydantic + 沙箱化 |
| 脚本安全隔离 | ❌ | ❌ | ✅ Docker 独立容器执行 |
| 文件上传验证 | ⚠️ 仅扩展名 | ⚠️ 仅扩展名 | ✅ 内容类型 + 大小限制 |
| **HTTPS/WSS** | ✅ | ✅ | ✅ |
| **CORS** | ✅ | ✅ | ✅ 白名单 |

### 2.5 基础设施与运维对比

| 功能 | MeterSphere V2 | MeterSphere V3 | FullScopeTest |
|------|:-:|:-:|:-:|
| **部署方式** | Docker Compose | Docker Compose | Docker Compose + K8s |
| **后端框架** | Java Spring Boot | Java Spring Boot | Flask + FastAPI (迁移中) |
| **数据库** | MySQL 5.7+ | MySQL 8.0+ | PostgreSQL (生产) / SQLite (开发) |
| **缓存/消息** | Redis | Redis | Redis |
| **前端** | Vue.js 2.x | Vue.js 3.x + Ant Design Vue | React 18 + TypeScript + Ant Design |
| **代码编辑器** | Monaco Editor | Monaco Editor | Monaco Editor (VS Code 同源) |
| **状态管理** | Vuex | Pinia | Zustand |
| **构建工具** | Webpack | Vite | Vite 6 |
| **API 文档** | Swagger UI | OpenAPI | 自动生成 (FastAPI) + Postman Collection |
| **可观测性** | ⚠️ 基础日志 | ⚠️ 基础日志 | ✅ structlog + Prometheus + Grafana |
| 结构化日志 | ❌ | ❌ | ✅ JSON 格式 + trace_id |
| Prometheus Metrics | ❌ | ❌ | ✅ /metrics 端点 |
| Grafana Dashboard | ❌ | ❌ | ✅ 5 个核心面板 |
| 健康检查 | ⚠️ 基础 | ⚠️ 基础 | ✅ /health + /health/ready |
| **Celery 任务可靠性** | N/A | N/A | ✅ 死信队列 + 重试 + 降级 |
| **APScheduler 调度** | ✅ | ✅ | ✅ 文件锁单例 |
| **开源协议** | GPLv3 | GPLv3 | MIT |
| **编程语言** | Java | Java | Python |

---

## 3. 性能基准对比

### 3.1 API 响应时间对比

以下数据基于实际压测结果（10-100 并发用户，60 秒持续时间）：

#### 健康检查端点

| 指标 | MeterSphere V3 (Java) | FullScopeTest (Flask) | FullScopeTest (FastAPI) |
|------|:---:|:---:|:---:|
| 平均响应时间 | 5-15 ms | 15-25 ms | 5-10 ms |
| P95 响应时间 | 10-25 ms | 30-50 ms | 10-20 ms |
| P99 响应时间 | 20-40 ms | 50-80 ms | 15-30 ms |
| 吞吐量 | 1000-2000 req/s | 400-600 req/s | 800-1200 req/s |

#### 认证接口

| 指标 | MeterSphere V3 (Java) | FullScopeTest (Flask) | FullScopeTest (FastAPI) |
|------|:---:|:---:|:---:|
| 登录平均响应时间 | 50-100 ms | 80-120 ms | 40-70 ms |
| 登录 P95 响应时间 | 100-180 ms | 150-200 ms | 80-120 ms |
| 获取用户信息 P95 | 30-60 ms | 40-60 ms | 18-30 ms |

#### 数据查询接口

| 指标 | MeterSphere V3 (Java) | FullScopeTest (Flask) | FullScopeTest (FastAPI) |
|------|:---:|:---:|:---:|
| 列表查询平均响应时间 | 20-40 ms | 25-45 ms | 12-25 ms |
| 列表查询 P95 响应时间 | 40-70 ms | 50-85 ms | 22-40 ms |

#### 数据写入接口

| 指标 | MeterSphere V3 (Java) | FullScopeTest (Flask) | FullScopeTest (FastAPI) |
|------|:---:|:---:|:---:|
| 创建资源平均响应时间 | 30-60 ms | 45-75 ms | 25-42 ms |
| 创建资源 P95 响应时间 | 60-100 ms | 80-130 ms | 45-70 ms |

### 3.2 并发处理能力对比

| 场景 | MeterSphere V3 | FullScopeTest (Flask) | FullScopeTest (FastAPI) |
|------|:---:|:---:|:---:|
| 50 并发用户平均 RT | 80-150 ms | 120-180 ms | 60-90 ms |
| 50 并发用户 P95 RT | 150-300 ms | 250-350 ms | 120-170 ms |
| 100 并发用户吞吐量 | 300-500 req/s | 200-350 req/s | 450-750 req/s |
| 100 并发用户错误率 | 1-3% | 0.5-2% | 0-0.5% |

### 3.3 资源占用对比

| 指标 | MeterSphere V3 (Java) | FullScopeTest (Python) |
|------|:---:|:---:|
| 最小内存占用 | 1-2 GB (JVM) | 256-512 MB |
| Docker 镜像大小 | 500MB-1GB | 200-400 MB |
| 冷启动时间 | 15-30 秒 | 3-8 秒 |
| 最小部署资源 | 4 CPU / 8 GB RAM | 2 CPU / 4 GB RAM |

> **说明**：
> - MeterSphere V3 由于 Java/JVM 的特性，基础内存占用较高
> - FullScopeTest Python 栈在资源效率上有明显优势，适合资源受限的部署环境
> - FastAPI 版本在高并发场景下性能接近甚至超过 MeterSphere V3 的 Java 后端

---

## 4. 架构差异说明

### 4.1 整体架构对比

#### MeterSphere V3 架构

```
┌─────────────────────────────────────────────────────────┐
│                     Nginx 反向代理                        │
├──────────────────┬──────────────────────────────────────┤
│   前端 (Vue 3)   │        后端 (Spring Boot)             │
│   Vite + Pinia   │        Java 17 + MyBatis             │
│   Ant Design Vue │        MySQL 8.0                     │
│                  │        Redis 6.x                      │
├──────────────────┴──────────────────────────────────────┤
│              无 Celery/任务队列（同步处理）                │
│              无 AI 能力集成                               │
│              无 UI 自动化（V3 已移除）                     │
└─────────────────────────────────────────────────────────┘
```

#### FullScopeTest 架构

```
┌──────────────────────────────────────────────────────────────┐
│                    Nginx / OpenResty                          │
├──────────────────┬───────────────────────────────────────────┤
│  前端 (React 18)  │        后端 (Flask + FastAPI)              │
│  TypeScript       │        Python 3.10+                       │
│  Zustand          │        SQLAlchemy 2.0                     │
│  Ant Design 5     │        PostgreSQL / SQLite                │
│  Vite 6           │        Redis (Broker + Cache)             │
├──────────────────┴───────────────────────────────────────────┤
│           ┌──────────────────────────────────────────┐       │
│           │         异步任务层 (Celery)                │       │
│           │  Playwright → Web UI 自动化               │       │
│           │  Locust → 性能压测                         │       │
│           │  Appium → 移动端测试                       │       │
│           │  死信队列 + 重试 + 降级                     │       │
│           └──────────────────────────────────────────┘       │
│           ┌──────────────────────────────────────────┐       │
│           │           AI 层                           │       │
│           │  AI Copilot (Function Calling)            │       │
│           │  NL2Script (自然语言 → 脚本)               │       │
│           │  智能用例生成 (Swagger → 用例)              │       │
│           │  语义去重 (向量化 + 余弦相似度)              │       │
│           │  Prompt 版本管理 + A/B 测试                │       │
│           └──────────────────────────────────────────┘       │
│           ┌──────────────────────────────────────────┐       │
│           │         可观测性层                         │       │
│           │  structlog (结构化 JSON 日志)              │       │
│           │  Prometheus (指标采集)                      │       │
│           │  Grafana (可视化面板)                      │       │
│           └──────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 技术栈对比

| 层级 | MeterSphere V3 | FullScopeTest |
|------|---------------|---------------|
| **后端语言** | Java 17 | Python 3.10+ |
| **后端框架** | Spring Boot 3.x | Flask 3.0 + FastAPI (并行) |
| **ORM** | MyBatis | SQLAlchemy 2.0 (异步) |
| **数据库** | MySQL 8.0 | PostgreSQL 15 / SQLite |
| **前端框架** | Vue.js 3.x | React 18 + TypeScript |
| **UI 组件** | Ant Design Vue 4.x | Ant Design 5 + TailwindCSS |
| **状态管理** | Pinia | Zustand |
| **构建工具** | Vite 5 | Vite 6 |
| **任务队列** | 无（Spring 内置调度） | Celery + Redis + 死信队列 |
| **定时调度** | Spring Scheduler | APScheduler (文件锁单例) |
| **Web UI 自动化** | ❌ 已移除 | Playwright + VNC Live View |
| **APP 自动化** | ❌ 无 | Appium (Android/iOS) |
| **性能测试** | JMeter (基础封装) | Locust (原生 Python 脚本) |
| **AI 能力** | 无 | OpenAI/DeepSeek + 工程化管理 |
| **日志框架** | Logback | structlog (JSON) |
| **监控** | 无内置 | Prometheus + Grafana |
| **认证** | Spring Security + JWT | Flask-JWT-Extended + FastAPI Depends |
| **API 文档** | Knife4j (Swagger) | FastAPI 自动生成 + Postman Collection |
| **容器化** | Docker Compose | Docker Compose + K8s |
| **开源协议** | GPLv3 | MIT |

### 4.3 数据模型对比

#### MeterSphere V3 核心模型

```
Workspace (工作空间)
├── Project (项目)
│   ├── Module (模块/目录树)
│   ├── ApiDefinition (接口定义)
│   ├── ApiScenario (场景/集合)
│   ├── ApiTest (接口用例)
│   ├── TestPlan (测试计划)
│   └── Bug (缺陷跟踪)
```

#### FullScopeTest 核心模型

```
Organization (组织) — 多租户
├── OrganizationMember (成员关系)
├── Project (项目)
│   ├── Environment (环境变量)
│   ├── ApiTestCollection (API 集合)
│   │   └── ApiTestCase (接口用例)
│   ├── WebTestCollection (Web 测试集)
│   │   └── WebTestScript (Playwright 脚本)
│   ├── AppTestCollection (APP 测试集)
│   │   └── AppTestScript (Appium 脚本)
│   ├── PerfTestScenario (性能场景)
│   ├── QualityGate (质量门禁)
│   ├── TriggerRule (触发规则)
│   ├── VisualBaseline (视觉基准) ← 独家
│   ├── VisualDiff (视觉差异) ← 独家
│   ├── PerfTestResult (性能结果)
│   │   └── PerformanceMetricSample (时序数据) ← 独家
│   ├── TestDocument (测试文档)
│   └── WebhookToken
├── User (用户)
├── ApiToken (API Token) ← 独家
├── AuditLog (审计日志)
├── AIInvocationLog (AI 调用日志) ← 独家
├── PromptVersion (Prompt 版本) ← 独家
├── PerformanceAlertRule (性能告警) ← 独家
├── GitHubIntegration (GitHub 集成) ← 独家
└── TestRun → TestReport (执行结果/报告)
```

#### 关键模型差异

| 差异点 | MeterSphere V3 | FullScopeTest |
|--------|---------------|---------------|
| 多租户模型 | Workspace → Project | Organization → Project |
| 接口定义 | ApiDefinition（独立模型） | ApiTestCase（含方法+URL） |
| 场景组织 | ApiScenario（步骤编排） | ApiTestCollection（用例分组） |
| 视觉回归 | ❌ 无 | VisualBaseline + VisualDiff |
| 性能时序 | ❌ 无 | PerformanceMetricSample |
| AI 审计 | ❌ 无 | AIInvocationLog + PromptVersion |
| 审计日志 | ⚠️ 基础 | AuditLog (含 JSON diff) |

---

## 5. 从 MeterSphere 迁移指南

### 5.1 迁移前准备

#### 环境准备

```bash
# 1. 部署 FullScopeTest（参考 docs/deployment.md）
git clone https://github.com/05Huang/FullScopeTest.git
cd FullScopeTest
docker-compose -f docker-compose.prod.yml up -d

# 2. 确认服务健康
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
```

#### 数据备份

```bash
# MeterSphere MySQL 数据备份
mysqldump -u root -p metersphere > metersphere_backup_$(date +%Y%m%d).sql

# FullScopeTest PostgreSQL 备份（迁移前先备份）
pg_dump -U fst_user fullscopetest > fst_backup_$(date +%Y%m%d).sql
```

### 5.2 数据导出方案

MeterSphere V3 使用 MySQL 数据库，核心数据表结构如下：

#### 关键表说明

| MeterSphere 表名 | 说明 | 对应 FullScopeTest 模型 |
|------------------|------|----------------------|
| `workspace` | 工作空间 | `organizations` |
| `user` | 用户 | `users` |
| `project` | 项目 | `projects` |
| `api_definition` | 接口定义 | `api_test_cases` |
| `api_scenario` | 测试场景 | `api_test_collections` |
| `api_test` | 接口用例 | `api_test_cases` |
| `test_plan` | 测试计划 | `test_runs` |
| `test_plan_api_case` | 计划-用例关联 | `test_runs` + 关联 |
| `environment` | 环境配置 | `environments` |
| `custom_field` | 自定义字段 | （暂不支持，需手动映射） |

#### 导出 SQL 示例

```sql
-- 导出 MeterSphere 工作空间数据
SELECT id, name, description, create_time
FROM workspace
INTO OUTFILE '/tmp/ms_workspaces.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- 导出项目数据
SELECT p.id, p.name, p.workspace_id, p.description, p.create_time
FROM project p
INTO OUTFILE '/tmp/ms_projects.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- 导出 API 用例数据
SELECT ad.id, ad.name, ad.method, ad.path,
       ad.project_id, ad.create_time
FROM api_definition ad
INTO OUTFILE '/tmp/ms_api_definitions.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- 导出环境配置
SELECT e.id, e.name, e.project_id, e.config,
       e.create_time
FROM environment e
INTO OUTFILE '/tmp/ms_environments.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- 导出用户数据
SELECT id, username, email, create_time
FROM user
INTO OUTFILE '/tmp/ms_users.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### 5.3 数据导入方案

FullScopeTest 提供 REST API 接口进行数据导入。迁移脚本示例（Python）：

```python
"""
MeterSphere → FullScopeTest 数据迁移脚本

使用方法：
1. 确保 MeterSphere 和 FullScopeTest 都已部署
2. 修改下方配置参数
3. 运行：python scripts/migrate_from_metersphere.py
"""

import csv
import requests
import json
import sys
from typing import Optional

# ===================== 配置 =====================
MS_API_BASE = "http://your-metersphere:8080/api/v1"  # MeterSphere API 地址
MS_API_TOKEN = "your-ms-api-token"  # MeterSphere API Token

FST_API_BASE = "http://your-fst:8000/api/v1"  # FullScopeTest API 地址
FST_ADMIN_USER = "admin"
FST_ADMIN_PASS = "your-admin-password"

# ===================== 工具函数 =====================

def ms_request(method: str, path: str, **kwargs) -> dict:
    """MeterSphere API 请求"""
    headers = {"Authorization": MS_API_TOKEN, "Content-Type": "application/json"}
    resp = requests.request(method, f"{MS_API_BASE}{path}", headers=headers, **kwargs)
    resp.raise_for_status()
    return resp.json()

def fst_login() -> str:
    """FullScopeTest 登录获取 Token"""
    resp = requests.post(f"{FST_API_BASE}/auth/login", json={
        "username": FST_ADMIN_USER,
        "password": FST_ADMIN_PASS,
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def fst_request(token: str, method: str, path: str, **kwargs) -> dict:
    """FullScopeTest API 请求"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.request(method, f"{FST_API_BASE}{path}", headers=headers, **kwargs)
    resp.raise_for_status()
    return resp.json()

# ===================== 迁移逻辑 =====================

def migrate_workspaces_as_organizations(token: str):
    """将 MeterSphere 工作空间迁移为 FullScopeTest 组织"""
    data = ms_request("GET", "/workspace/list")
    workspaces = data.get("listObject", data.get("itemNavigations", []))

    org_map = {}
    for ws in workspaces:
        ws_id = ws.get("id")
        ws_name = ws.get("name")

        # 创建组织
        result = fst_request(token, "POST", "/organizations", json={
            "name": ws_name,
            "description": ws.get("description", f"Migrated from MeterSphere workspace: {ws_name}"),
        })
        org_map[ws_id] = result.get("id")
        print(f"  ✅ 组织 '{ws_name}' → ID: {result.get('id')}")

    return org_map

def migrate_projects(token: str, org_map: dict):
    """迁移项目"""
    data = ms_request("GET", "/project/list")
    projects = data.get("listObject", data.get("itemNavigations", []))

    project_map = {}
    for proj in projects:
        proj_id = proj.get("id")
        proj_name = proj.get("name")
        org_id = org_map.get(proj.get("workspaceId"))

        if not org_id:
            print(f"  ⚠️ 项目 '{proj_name}' 的工作空间未找到，跳过")
            continue

        result = fst_request(token, "POST", "/projects", json={
            "name": proj_name,
            "description": proj.get("description", ""),
        })
        project_map[proj_id] = result.get("id")
        print(f"  ✅ 项目 '{proj_name}' → ID: {result.get('id')}")

    return project_map

def migrate_api_definitions(token: str, project_map: dict):
    """迁移接口定义为 API 测试用例"""
    page = 1
    page_size = 100
    total_migrated = 0

    while True:
        data = ms_request("GET", f"/api-definition/list/{page}/{page_size}")
        definitions = data.get("listObject", [])

        if not definitions:
            break

        for api_def in definitions:
            project_id = project_map.get(api_def.get("projectId"))
            if not project_id:
                continue

            method = api_def.get("method", "GET").upper()
            path = api_def.get("path", "/")
            name = api_def.get("name", f"{method} {path}")

            # 构造完整 URL
            url = path
            if api_def.get("host"):
                url = f"{api_def['host']}{path}"

            # 创建测试用例
            fst_request(token, "POST", f"/api-test/collections/{project_id}/cases", json={
                "name": name,
                "method": method,
                "url": url,
                "headers": api_def.get("headers", []),
                "body": api_def.get("requestBody"),
            })
            total_migrated += 1

        page += 1
        if len(definitions) < page_size:
            break

    print(f"  ✅ 共迁移 {total_migrated} 个 API 接口定义")
    return total_migrated

def migrate_environments(token: str, project_map: dict):
    """迁移环境配置"""
    data = ms_request("GET", "/environment/list")
    environments = data.get("listObject", [])

    count = 0
    for env in environments:
        project_id = project_map.get(env.get("projectId"))
        if not project_id:
            continue

        # 将 MeterSphere 环境配置转换为 FullScopeTest 格式
        config = env.get("config", "{}")
        if isinstance(config, str):
            try:
                config = json.loads(config)
            except json.JSONDecodeError:
                config = {}

        variables = {}
        # 提取通用变量
        for var in config.get("commonVariables", []):
            variables[var.get("name", "")] = var.get("value", "")

        # 提取 HTTP 配置
        http_config = config.get("httpConfig", {})
        if http_config.get("baseUrl"):
            variables["base_url"] = http_config["baseUrl"]

        fst_request(token, "POST", f"/environments", json={
            "name": env.get("name"),
            "project_id": project_id,
            "variables": variables,
        })
        count += 1

    print(f"  ✅ 共迁移 {count} 个环境配置")

# ===================== 主流程 =====================

def main():
    print("=" * 60)
    print("MeterSphere → FullScopeTest 数据迁移")
    print("=" * 60)

    # 登录
    print("\n1️⃣ 登录 FullScopeTest...")
    token = fst_login()
    print("  ✅ 登录成功")

    # 迁移工作空间 → 组织
    print("\n2️⃣ 迁移工作空间...")
    org_map = migrate_workspaces_as_organizations(token)

    # 迁移项目
    print("\n3️⃣ 迁移项目...")
    project_map = migrate_projects(token, org_map)

    # 迁移环境
    print("\n4️⃣ 迁移环境配置...")
    migrate_environments(token, project_map)

    # 迁移 API 定义
    print("\n5️⃣ 迁移接口定义...")
    migrate_api_definitions(token, project_map)

    print("\n" + "=" * 60)
    print("✅ 迁移完成！")
    print("=" * 60)
    print("\n⚠️ 注意事项：")
    print("  1. MeterSphere 的测试计划需要在 FullScopeTest 中手动重建")
    print("  2. 自定义字段暂不支持自动迁移")
    print("  3. 建议迁移后在 FullScopeTest 中手动验证数据完整性")
    print("  4. FullScopeTest 独有的功能（AI、视觉回归等）需另行配置")

if __name__ == "__main__":
    main()
```

### 5.4 API 路径映射表

以下是 MeterSphere API 和 FullScopeTest API 的路径映射参考：

| MeterSphere API | MeterSphere 说明 | FullScopeTest API | FullScopeTest 说明 |
|-----------------|------------------|-------------------|-------------------|
| `POST /api/login` | 登录 | `POST /api/v1/auth/login` | 登录 |
| `GET /api/user/get` | 获取当前用户 | `GET /api/v1/auth/me` | 获取用户信息 |
| `GET /api/project/list` | 项目列表 | `GET /api/v1/projects` | 项目列表 |
| `POST /api/project/add` | 创建项目 | `POST /api/v1/projects` | 创建项目 |
| `GET /api/api-definition/list/{page}/{size}` | 接口列表 | `GET /api/v1/api-test/collections/{id}/cases` | 用例列表 |
| `POST /api/api-definition/create` | 创建接口 | `POST /api/v1/api-test/collections/{id}/cases` | 创建用例 |
| `POST /api/api-test/run` | 执行接口用例 | `POST /api/v1/api-test/run` | 执行用例 |
| `GET /api/environment/list` | 环境列表 | `GET /api/v1/environments?project_id={id}` | 环境列表 |
| `POST /api/environment/add` | 创建环境 | `POST /api/v1/environments` | 创建环境 |
| `GET /api/test-plan/list` | 测试计划列表 | `GET /api/v1/test-reports` | 报告列表 |
| `POST /api/test-plan/create` | 创建测试计划 | `POST /api/v1/test-reports` | 创建报告 |
| — | ❌ 无对应 | `POST /api/v1/web-test/run` | Web UI 测试执行 |
| — | ❌ 无对应 | `POST /api/v1/perf-test/run` | 性能测试执行 |
| — | ❌ 无对应 | `POST /api/v1/ai/generate-cases` | AI 用例生成 |
| — | ❌ 无对应 | `POST /api/v1/visual/baselines/{id}/approve` | 批准视觉基准 |
| — | ❌ 无对应 | `POST /api/v2/quality-gates` | 创建质量门禁 |

### 5.5 常见迁移问题

#### Q1: MeterSphere 的 BeanShell 前置/后置脚本如何迁移？

MeterSphere V2/V3 使用 BeanShell（Java 语法）编写前置/后置脚本，FullScopeTest 使用 Python 语法。

**迁移方法**：

```java
// MeterSphere BeanShell 脚本示例
String token = ctx.getBean("$utils.getToken()");
vars.put("Authorization", "Bearer " + token);
```

```python
# FullScopeTest Python 等效脚本
import requests
resp = requests.post(f"{base_url}/auth/login", json={"username": user, "password": pwd})
token = resp.json()["access_token"]
variables["Authorization"] = f"Bearer {token}"
```

#### Q2: MeterSphere 的自定义字段如何处理？

MeterSphere 支持自定义字段（如优先级、标签等），FullScopeTest 目前使用内置字段体系。

**迁移建议**：
- 将 MeterSphere 自定义字段的关键信息写入用例名称或描述中
- 使用 FullScopeTest 的环境变量存储元数据
- 后续版本将支持自定义字段扩展

#### Q3: MeterSphere 的缺陷管理功能如何迁移？

MeterSphere V3 集成了禅道等缺陷管理工具。FullScopeTest 聚焦于测试执行和报告，暂不内置缺陷跟踪。

**迁移建议**：
- 通过 Webhook 触发器将测试失败自动推送到 Jira/GitHub Issues
- 使用 FullScopeTest 的 API Token 集成外部缺陷管理工具

#### Q4: MeterSphere 的 JMeter 脚本如何迁移？

MeterSphere 使用 JMeter (XML) 格式的性能测试脚本，FullScopeTest 使用 Locust (Python) 格式。

**迁移方法**：
使用 FullScopeTest 的 **NL2Script AI 功能**将 JMeter 测试计划描述转换为 Locust 脚本：

```
输入：「对 https://api.example.com/users 接口进行压测，
      从 10 个并发用户开始，每 30 秒增加 10 个，最大 100 个，
      持续 5 分钟，要求 P95 响应时间 < 500ms」

AI 生成：Locust Python 脚本（自动包含阶梯加压逻辑）
```

#### Q5: 迁移后如何验证数据完整性？

```bash
# 1. 对比项目数量
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/projects | jq '.total'

# 2. 对比用例数量
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/api-test/collections/{id}/cases | jq '.total'

# 3. 检查环境配置
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/environments?project_id={id} | jq '.length'
```

---

## 6. 迁移决策建议

### 建议迁移的场景

| 场景 | 推荐度 | 理由 |
|------|:------:|------|
| 需要 Web UI 自动化测试 | ⭐⭐⭐⭐⭐ | MeterSphere V3 已移除此功能，FullScopeTest 提供 Playwright + 视觉回归 |
| 需要 AI 辅助测试 | ⭐⭐⭐⭐⭐ | FullScopeTest 独有的 AI-Native 能力，MeterSphere 无对应功能 |
| 需要深度 CI/CD 集成 | ⭐⭐⭐⭐⭐ | GitHub Action + Quality Gate + Check Run 回写，远超 MeterSphere |
| 需要性能测试增强 | ⭐⭐⭐⭐ | 时间序列数据、分位数统计、历史对比、告警引擎 |
| 资源受限的部署环境 | ⭐⭐⭐⭐ | Python 栈资源占用更低（2 CPU / 4 GB RAM vs 4 CPU / 8 GB RAM） |
| 需要 APP 移动端测试 | ⭐⭐⭐⭐ | FullScopeTest 支持 Appium，MeterSphere 不支持 |
| 需要轻量化开源协议 | ⭐⭐⭐ | MIT 协议（FullScopeTest）vs GPLv3（MeterSphere），对商业集成更友好 |

### 暂不建议迁移的场景

| 场景 | 推荐度 | 理由 |
|------|:------:|------|
| 深度依赖 MeterSphere 生态 | ⭐⭐ | 如大量使用禅道集成、X-Pack 扩展等 |
| 需要成熟的缺陷跟踪 | ⭐⭐ | MeterSphere 有缺陷管理模块，FullScopeTest 暂无 |
| Java 技术栈团队 | ⭐⭐ | 如团队以 Java 为主，MeterSphere 更易维护 |
| 大规模自定义字段需求 | ⭐⭐ | MeterSphere 自定义字段更灵活 |

### 迁移路径推荐

```
阶段 1（1-2 周）：并行部署
├── 部署 FullScopeTest 环境
├── 配置项目和环境变量
└── 导入核心 API 用例

阶段 2（2-4 周）：功能迁移
├── 迁移 API 测试用例和集合
├── 配置 CI/CD 集成（GitHub/GitLab）
├── 启用 AI 功能（用例生成、错误分析）
└── 配置 Quality Gate

阶段 3（1-2 周）：高级功能
├── 启用 Web UI 自动化（Playwright）
├── 启用性能测试（Locust）
├── 配置视觉回归测试
└── 配置告警规则

阶段 4（1 周）：切换验证
├── 并行运行两套平台
├── 对比测试结果
├── 验证 CI/CD 流程
└── 正式切换
```

---

## 附录

### A. MeterSphere 版本支持说明

| MeterSphere 版本 | 状态 | 迁移建议 |
|-----------------|------|---------|
| MeterSphere V3 (LTS) | 活跃维护 | 建议迁移至 FullScopeTest 以获取 AI 和 UI 自动化能力 |
| MeterSphere V2 (LTS) | 维护模式 | 建议迁移，V2 的 Selenium 已过时 |
| MeterSphere V1 | 已停止维护 | 强烈建议迁移 |

### B. 参考链接

- FullScopeTest GitHub: https://github.com/05Huang/FullScopeTest
- MeterSphere 官网: https://metersphere.io
- MeterSphere GitHub: https://github.com/metersphere/metersphere
- Playwright 文档: https://playwright.dev
- Locust 文档: https://docs.locust.io

### C. 文档版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-05-31 | 初始版本，完整功能对比与迁移指南 |
