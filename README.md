# FullScopeTest —— AI一站式自动化测试平台

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69bfd011e4b01ee6a7b76b33.png" alt="FullScopeTest Banner" width="100%" />


  <br />

  **AI 驱动的下一代全链路自动化测试平台**
  <br />
  AI 自动编排 · API 接口测试 · Web 自动化 · 性能测试 · 报告中心

  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
  [![React](https://img.shields.io/badge/react-18.3-blue.svg)](https://reactjs.org/)
  [![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
  [![Playwright](https://img.shields.io/badge/playwright-ready-2EAD33?style=flat&logo=playwright)](https://playwright.dev/)
  [![Locust](https://img.shields.io/badge/locust-ready-43B02A?style=flat)](https://locust.io/)

  <h2>🔥 在线演示地址: <a href="http://test.huangxuan.chat">test.huangxuan.chat</a> 🔥</h2>
</div>

## 📖 项目简介

**FullScopeTest** 是一款面向个人开发者与小团队的现代化自动化测试平台，覆盖了接口测试、Web 自动化、性能测试与报告中心。我们致力于通过**AI 赋能**，让测试工作变得更智能、更高效，为您提供可落地执行的 AI 自动编排能力。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c01107e4b01ee6a7b76b3a.png" alt="Dashboard 预览" width="80%" />
  <p><em>平台总览控制台</em></p>
</div>


---

## ✨ 核心特性与 AI 赋能

###  纯正的 AI 驱动能力 (AI-Native Features)

#### 1. 🤖 AI 自动编排 (AI Auto-Orchestration)
自然语言即代码！只需输入测试目标，AI 将自动为您生成结构化操作步骤（Plan），并**复用既有平台 API 自动落地执行**。
- **自然语言生成计划**：输入目标后，AI 理解意图并规划执行路径。
- **自动落地执行**：按计划调用平台 API 自动创建/更新环境、集合、用例并直接运行。
- **运行时模型配置**：前端面板支持动态设置 `base_url` / `model` / `api_key`，无缝对接各类大语言模型。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c01159e4b01ee6a7b76b3b.png" alt="AI 自动编排输入" width="45%" />
  <img src="https://res.huangxuan.chat/thrivex/album/69c01159e4b01ee6a7b76b3c.png" alt="" width="45%" />
  <p><em>AI 自动生成测试计划并自动执行</em></p>
</div>

#### 2. 🪄 AI 测试脚本自动生成 (NL2Script)
- **场景**：编写 Web UI 测试（如 Playwright/Selenium）或性能测试（如 k6/Locust）脚本往往需要一定的代码门槛，编写过程繁琐。
- **功能**：用户只需输入自然语言，例如：“登录系统，进入控制台，点击新增用户，填写随机生成的用户名，验证是否出现成功提示”。 AI Agent 会自动将其转换为完整的、可执行的 Web 测试脚本或性能测试脚本。
- **落地方式**：结合现有的 `WebTestScripts` 和 `PerfTestScenarios`，在前端增加“AI 辅助生成脚本”按钮，后端调用大模型生成代码，并在前端代码编辑器中高亮显示供用户审查和调整。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ae4b01ee6a7b76b41.png" alt="AI 生成测试脚本" width="80%" />
</div>


#### 3. 🕵️‍♂️ 智能错误分析与自愈 (Self-Healing Tests)
- **场景**：自动化测试最大的痛点是维护成本高。前端稍微改了 UI，或者 API 字段变了，测试用例就会大面积失败，排查原因很耗时。
- **功能**：当测试任务失败时，触发 AI 诊断 Agent。它会自动分析错误日志、API 响应体或报错时的 Web DOM 结构，用大白话解释失败原因（例如：“登录按钮的 selector 从 `#btn-login` 变成了 `.login-submit`，导致元素找不到”）。
- **进阶（测试自愈）**：AI 可以直接提供一个“一键修复”按钮，自动修改测试脚本中的断言或选择器，保存并重新运行。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ae4b01ee6a7b76b42.png" alt="" width="45%" />
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144be4b01ee6a7b76b43.png" alt="" width="45%" />
  <p><em>AI 智能错误分析与自愈</em></p>
</div>


#### 4. 🎲 智能测试数据生成与用例裂变 (AI Data Synthesizer)
- **场景**：API 测试往往需要构造大量边界情况或符合业务逻辑的复杂 JSON 报文。
- **功能**：基于 API 的定义或已有的基本用例，AI Agent 自动推断字段含义，并生成一套完整的测试数据集。
- **落地方式**：可以在 `ApiTestWorkspace` 中加入“AI 扩充用例”功能，用户给出一个正常的 API 请求，AI 自动裂变出包含“边界值、非法注入、空值”等数十个异常测试用例，极大提升测试覆盖率。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144be4b01ee6a7b76b44.png" alt="" width="45%" />
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144be4b01ee6a7b76b45.png" alt="" width="45%" />
  <p><em>AI 智能测试数据生成与用例裂变 </em></p>
</div>


#### 5. 🕷️ 探索性测试 Agent (Autonomous Web Explorer)
- **场景**：传统的测试需要人去预先定义每一步的断言，有没有可能让 AI 自己去探索系统并发现问题？
- **功能**：给 AI Agent 提供一个起始 URL 和简单的系统目标（比如“尽可能多地点击不同页面并寻找报错”）。Agent 利用 DOM 解析甚至视觉模型（Vision），自主决定点击哪些按钮、填写什么表单，像真实的“猴子测试（Monkey Test）”一样在网站里探索。
- **落地方式**：最终生成一份《AI 探索测试报告》，列出它发现的 JS 报错、404 死链或潜在的安全问题。这是一个非常纯粹的 Agent 行为。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ce4b01ee6a7b76b46.png" alt="探索性测试 Agent" width="80%" />
</div>


#### 6. 💬 平台级全局 Copilot (AI 助手面板)
- **场景**：将现有的离散 AI 功能整合为一个统一的对话入口。
- **功能**：在前端 React 界面（如 `MainLayout`）右下角增加一个悬浮的 AI Copilot 聊天窗口。
- **落地方式**：用户可以直接通过对话下发指令：“帮我建一个名为 '电商下单' 的性能测试场景，并发 100，持续 5 分钟”、“查一下昨天失败的 Web 测试有哪些？” 后端 Agent 通过 Function Calling (工具调用) 解析意图并直接操作数据库或调度执行任务。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c0144ce4b01ee6a7b76b47.png" alt="平台级全局 Copilot" width="80%" />
</div>


---

### �️ 强大的基础测试工作台 (Core Testing Workspace)

#### 1. 🔌 API 接口测试工作台
媲美 Postman 的丝滑体验，支持完整的 HTTP/REST API 测试生命周期。
- **环境变量与请求头**：支持 `{variable}` 变量替换与默认全局/局部请求头。
- **前置/后置脚本**：强大的脚本引擎，支持变量提取与复杂断言。
- **一键 cURL 导入导出**：方便与其他系统无缝集成。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c011b3e4b01ee6a7b76b3d.png" alt="API 测试工作台" width="80%" />
</div>

#### 2. 🌐 Web 自动化测试 (Playwright)
内置强大的 Playwright 引擎，轻松搞定 UI 自动化测试。
- **脚本管理与编辑器**：支持在线创建、编辑、保存 Playwright Python 脚本。
- **本地化录制支持**：一键唤起 `playwright codegen` 自动录制脚本（需本机环境支持）。
- **异步后台执行**：通过 Celery 队列在后台静默运行，支持实时状态跟踪与错误定位。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69c011e4e4b01ee6a7b76b3e.png" alt="Web 自动化" width="80%" />
</div>

#### 3. ⚡ 性能测试 (Locust)
基于 Locust 的分布式压测能力，直观掌握系统性能瓶颈。
- **并发模拟**：灵活配置并发用户数与阶梯加压模式（Step load）。
- **实时监控与报告**：动态绘制响应时间、吞吐量 (RPS)、错误率等核心性能指标。

<div align="center">
  <img src="https://res.huangxuan.chat/thrivex/album/69bfd012e4b01ee6a7b76b35.png" alt="性能测试看板" width="80%" />
</div>

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

### 前置要求

| 组件 | 版本建议 | 说明 |
|------|---------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建/开发服务器 |
| PostgreSQL | 15+ | 推荐数据库（默认配置更贴近 PostgreSQL） |
| Redis | 5.0+ | 异步任务（Celery）所需，未用异步可不启 |

### 1) 启动后端

```bash
cd backend
python -m venv venv

# Windows 激活虚拟环境
.\venv\Scripts\activate

# Linux/macOS 激活虚拟环境
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 可选：安装 Playwright 浏览器（启用 Web 录制/执行时强烈建议）
python -m playwright install chromium

# 准备 backend/.env（最少需要 DATABASE_URL / SECRET_KEY / JWT_SECRET_KEY）
# 示例（SQLite 快速启动）：
#   DATABASE_URL=sqlite:///fullscopetest_dev.db
#   SECRET_KEY=dev-secret
#   JWT_SECRET_KEY=dev-jwt-secret

# 初始化数据库（会 drop & create，请谨慎操作生产库）
python init_db.py

# 创建管理员账号（可选）
python create_admin.py
# 默认账号：admin / admin123

# 启动后端 API 服务
python app.py
```

> 后端默认运行地址：`http://127.0.0.1:5211/api/v1`

**可选：启动 Celery Worker（建议在新的终端窗口运行）**
```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
celery -A app.extensions:celery worker --loglevel=info
```

### 2) 启动前端（开发模式）

```bash
cd web
npm install
npm run dev
```

> 前端开发服务器默认运行在：`http://localhost:3000`（已配置代理，将 `/api/*` 转发到 `http://localhost:5211`）

---

## 🛠 构建与部署（生产/预发布环境）

```bash
cd web
npm install
npm run build
```

前端构建产物位于 `web/dist`，可由 Nginx/OpenResty 托管，并反向代理后端到 `http://127.0.0.1:5211`。配置示例可参考 `nginx/` 目录与 `deploy.sh`。

### 关键配置项 (`backend/.env`)

```bash
# ================= 数据库配置 (二选一) =================
# PostgreSQL (生产推荐)
DATABASE_URL=postgresql://user:password@localhost:5432/fullscopetest_dev
# SQLite (本地快速启动)
# DATABASE_URL=sqlite:///fullscopetest_dev.db

# ================= 异步任务配置 =================
REDIS_URL=redis://localhost:6379/0
CELERY_ENABLE=true

# ================= 安全配置 (生产务必修改) =================
SECRET_KEY=change-me
JWT_SECRET_KEY=change-me

# ================= AI 助手配置 =================
# (也可由前端界面按请求动态覆盖)
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=your_api_key_here
```

> **注意：**
> - Web 录制功能通过启动本机 `playwright codegen` 实现，远程服务器环境通常无法使用本地录制器。
> - 后端入口 `backend/app.py` 会强制启用 Celery，建议同时启动 Redis + Celery Worker 以保证功能完整。

---

## 🏗 项目架构

```text
FullScopeTest/
├── backend/              # Flask 后端核心服务
│   ├── app/              # API / Models / Tasks / Utils
│   ├── migrations/       # 数据库迁移脚本
│   ├── tests/            # 自动化测试用例 (Pytest)
│   ├── app.py            # 后端启动入口文件
│   ├── init_db.py        # 开发环境快速初始化脚本
│   └── create_admin.py   # 创建管理员账号脚本
├── web/                  # React + TS 前端源码
├── document/             # 项目文档与规范
├── nginx/                # Nginx 部署配置示例
├── docker/               # Dockerfile 及容器编排配置
└── scripts/              # 辅助运维/构建脚本
```

---

## ❓ 常见问题 (FAQ)

<details>
<summary><strong>Redis 连接失败报错？</strong></summary>
请确保您的 Redis 服务已正确启动，可以通过以下命令测试：

```bash
redis-cli ping  # 若正常应返回 PONG
```
</details>

<details>
<summary><strong>Web 自动化录制器启动失败？</strong></summary>
Web 录制依赖于 Playwright 本机环境，请确认您已执行过以下安装命令：

```bash
pip install playwright
playwright install chromium
```
</details>

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
