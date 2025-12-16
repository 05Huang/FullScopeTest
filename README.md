# EasyTest - 一站式自动化测试平台 🚀

<div align="center">

**专为测试工程师和开发者打造的现代化自动化测试解决方案**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.2-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Ant Design](https://img.shields.io/badge/ant--design-5.12-1890ff.svg)](https://ant.design/)

[快速开始](#-快速开始) | [功能特性](#-核心功能) | [技术架构](#-技术架构) | [部署指南](#-部署指南) | [开发文档](./document/DEVELOPMENT.md)

</div>

---

## 🎯 项目简介

EasyTest 是一个功能强大、简单易用的自动化测试平台，集成了**接口测试**、**Web自动化测试**、**性能测试**等多种测试类型。采用前后端分离架构，提供现代化的 Web 界面和完善的 RESTful API。

### 核心优势

- 🎨 **现代化 UI** - 基于 React 18 + TypeScript + Ant Design 5，界面美观易用
- 🔥 **功能全面** - 涵盖接口测试、Web UI 测试、性能测试等多种场景
- 📦 **开箱即用** - Docker 一键部署，SQLite/PostgreSQL 双数据库支持
- 🔌 **可扩展性** - 插件化架构，易于扩展新功能
- 📊 **可视化报告** - 实时监控，丰富的图表展示（ECharts）
- 🔐 **安全可靠** - JWT 双 Token 认证机制，数据加密存储

## ✨ 核心功能

### 1. 🔧 接口测试（API Testing）
- **Postman 风格工作台** - 熟悉的界面设计，零学习成本
- **环境管理** - 多环境配置（开发/测试/生产），一键切换
- **用例集合** - 组织管理用例，支持批量执行和导入导出
- **断言脚本** - JavaScript 脚本支持，灵活验证响应数据
- **前置/后置脚本** - 实现复杂的测试流程和数据准备
- **变量提取** - 支持正则、JSONPath 等多种数据提取方式
- **请求历史** - 保存历史请求记录，便于复现和调试

### 2. 🌐 Web 自动化测试（UI Testing）
- **基于 Playwright** - 支持 Chromium、Firefox、WebKit 三大浏览器内核
- **脚本管理** - Python 脚本编写和管理
- **元素管理** - 页面对象模式（POM），提高代码复用性
- **可视化执行** - 实时查看脚本执行过程和结果
- **截图/视频** - 自动截图和录制视频，便于问题定位
- **并发执行** - 支持多脚本并行执行，提高测试效率

### 3. ⚡ 性能测试（Performance Testing）
- **基于 Locust** - 分布式负载测试框架
- **场景配置** - 灵活设置并发用户数、持续时间、爬坡策略
- **实时监控** - 响应时间、吞吐量（RPS）、错误率实时展示
- **性能分析** - 详细的性能指标统计和趋势分析
- **压力测试** - 支持梯度压力、持续压力等多种测试模式

### 4. 📊 测试报告与数据分析
- **工作台看板** - 测试执行概况、通过率、趋势一目了然
- **执行历史** - 完整的测试执行记录和结果追溯
- **趋势分析** - 近7天测试通过率、执行次数趋势图
- **详细报告** - 支持导出 JSON、HTML 格式报告
- **多维度统计** - 按测试类型、时间、状态等维度统计分析

### 5. 📝 测试文档管理
- **Markdown 编辑器** - 所见即所得，实时预览（Monaco Editor）
- **文档分类** - 测试计划、测试用例、Bug报告等分类管理
- **版本控制** - 文档版本追踪和历史对比
- **模板系统** - 内置多种文档模板，快速创建标准化文档
- **导出功能** - 支持导出为 Markdown 或 HTML 格式

## 🏗️ 技术架构

### 后端技术栈
- **框架**: Flask 3.0 + Flask-RESTful
- **ORM**: SQLAlchemy
- **数据库**: SQLite（开发）/ PostgreSQL（生产）
- **认证**: Flask-JWT-Extended（双 Token 机制）
- **数据库迁移**: Flask-Migrate (Alembic)
- **性能测试**: Locust
- **Web自动化**: Playwright
- **HTTP客户端**: Requests

### 前端技术栈
- **框架**: React 18.2 + TypeScript 5.3
- **UI组件**: Ant Design 5.12
- **状态管理**: Zustand
- **路由**: React Router 6
- **HTTP客户端**: Axios
- **代码编辑器**: Monaco Editor
- **Markdown渲染**: React-Markdown
- **图表**: ECharts + echarts-for-react
- **构建工具**: Vite 5

### DevOps
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **进程管理**: Gunicorn (生产环境)

## 📦 快速开始

### 方式一：Docker 部署（推荐）

**前提条件**
- Docker 20.10+
- Docker Compose 1.29+

**启动命令**
```bash
# 克隆项目
git clone https://github.com/Asukadaisiki/AutoTestingPlatform.git
cd AutoTestingPlatform

# 开发环境
docker-compose up -d

# 生产环境
docker-compose -f docker-compose.prod.yml up -d
```

访问 http://localhost:3122（前端） 和 http://localhost:5211（后端 API）

### 方式二：本地开发部署

**前提条件**
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+（可选，默认使用 SQLite）

**1. 后端启动**
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件，配置数据库等信息

# 初始化数据库
flask db upgrade
python init_db.py  # 创建默认用户

# 启动后端服务
python wsgi.py
```
后端服务启动在 http://localhost:5211

**2. 前端启动**
```bash
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```
前端服务启动在 http://localhost:3122

**3. 默认账户**
- 用户名: `admin`
- 密码: `admin123`

## 🐳 Docker 部署详解

### 开发环境部署
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 生产环境部署
```bash
# 启动生产环境
docker-compose -f docker-compose.prod.yml up -d

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 重启服务
docker-compose -f docker-compose.prod.yml restart
```

### 服务端口说明
- **前端**: 3122 (开发) / 80,443 (生产)
- **后端 API**: 5211
- **PostgreSQL**: 5432

## 📁 项目结构

```
EasyTest-Web/
├── backend/                    # 后端 Flask 应用
│   ├── app/
│   │   ├── __init__.py        # 应用工厂
│   │   ├── config.py          # 配置文件
│   │   ├── extensions.py      # 扩展初始化
│   │   ├── api/               # API 路由
│   │   │   ├── auth.py        # 用户认证
│   │   │   ├── projects.py    # 项目管理
│   │   │   ├── api_test.py    # 接口测试
│   │   │   ├── web_test.py    # Web测试
│   │   │   ├── perf_test.py   # 性能测试
│   │   │   ├── reports.py     # 测试报告
│   │   │   ├── docs.py        # 测试文档
│   │   │   └── environments.py # 环境管理
│   │   ├── models/            # 数据模型
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── api_test_case.py
│   │   │   ├── web_test_script.py
│   │   │   ├── perf_test_scenario.py
│   │   │   ├── test_run.py
│   │   │   ├── test_document.py
│   │   │   └── environment.py
│   │   └── utils/             # 工具函数
│   │       ├── response.py    # 统一响应格式
│   │       └── validators.py  # 数据验证
│   ├── migrations/            # 数据库迁移
│   ├── instance/              # 实例文件夹（SQLite数据库）
│   ├── requirements.txt       # Python依赖
│   ├── app.py                 # 应用入口
│   ├── wsgi.py                # WSGI入口
│   ├── manage.py              # 管理命令
│   └── init_db.py             # 数据库初始化
│
├── web/                        # 前端 React 应用
│   ├── src/
│   │   ├── layouts/           # 布局组件
│   │   │   └── MainLayout.tsx
│   │   ├── pages/             # 页面组件
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx  # 工作台
│   │   │   ├── Reports.tsx    # 测试报告
│   │   │   ├── Documents.tsx  # 测试文档
│   │   │   ├── api-test/      # 接口测试
│   │   │   ├── web-test/      # Web测试
│   │   │   └── perf-test/     # 性能测试
│   │   ├── services/          # API 服务
│   │   │   ├── api.ts         # Axios配置
│   │   │   ├── authService.ts
│   │   │   ├── apiTestService.ts
│   │   │   ├── webTestService.ts
│   │   │   ├── perfTestService.ts
│   │   │   ├── reportService.ts
│   │   │   ├── documentService.ts
│   │   │   ├── environmentService.ts
│   │   │   └── projectService.ts
│   │   ├── stores/            # 状态管理
│   │   │   └── authStore.ts   # 认证状态
│   │   ├── styles/            # 样式文件
│   │   ├── App.tsx            # 应用根组件
│   │   └── main.tsx           # 入口文件
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
│
├── docker/                     # Docker 配置
│   ├── Dockerfile.backend     # 后端镜像
│   ├── Dockerfile.backend.dev # 后端开发镜像
│   ├── nginx/
│   │   ├── nginx.conf         # Nginx 配置
│   │   └── ssl/               # SSL证书
│   └── init.sql               # 数据库初始化SQL
│
├── document/                   # 项目文档
│   └── DEVELOPMENT.md         # 开发文档
│
├── docker-compose.yml         # 开发环境编排
├── docker-compose.prod.yml    # 生产环境编排
├── README.md                  # 项目说明
└── REFACTORING_PLAN.md       # 重构计划
```

## 🔧 配置说明

### 后端环境变量
创建 `backend/.env` 文件：
```bash
# Flask 配置
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True

# 数据库配置
# SQLite (开发)
DATABASE_URL=sqlite:///instance/easytest.db

# PostgreSQL (生产)
# DATABASE_URL=postgresql://user:password@localhost:5432/easytest

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# 跨域配置
CORS_ORIGINS=http://localhost:3122,http://localhost:3000

# 文件上传
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### 前端配置
编辑 `web/vite.config.ts` 修改后端 API 代理：
```typescript
server: {
  port: 3122,
  proxy: {
    '/api': {
      target: 'http://localhost:5211',  # 后端地址
      changeOrigin: true,
    },
  },
}
```

## 📖 API 文档

### RESTful API 端点

#### 认证 API
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新令牌
- `GET /api/v1/auth/me` - 获取当前用户信息

#### 接口测试 API
- `GET /api/v1/api-test/cases` - 获取用例列表
- `POST /api/v1/api-test/cases` - 创建用例
- `GET /api/v1/api-test/cases/:id` - 获取用例详情
- `PUT /api/v1/api-test/cases/:id` - 更新用例
- `DELETE /api/v1/api-test/cases/:id` - 删除用例
- `POST /api/v1/api-test/cases/:id/run` - 执行用例
- `POST /api/v1/api-test/execute` - 执行临时请求

#### Web 测试 API
- `GET /api/v1/web-test/scripts` - 获取脚本列表
- `POST /api/v1/web-test/scripts` - 创建脚本
- `POST /api/v1/web-test/scripts/:id/run` - 执行脚本

#### 性能测试 API
- `GET /api/v1/perf-test/scenarios` - 获取场景列表
- `POST /api/v1/perf-test/scenarios` - 创建场景
- `POST /api/v1/perf-test/scenarios/:id/run` - 执行场景

#### 测试报告 API
- `GET /api/v1/test-runs` - 获取执行记录
- `GET /api/v1/reports/statistics` - 获取统计数据
- `GET /api/v1/reports/dashboard` - 获取看板数据

更多API详情请查看：[API 文档](./document/API.md)

## 🛠️ 开发指南

### 后端开发
```bash
cd backend

# 创建新的数据库迁移
flask db migrate -m "描述变更内容"

# 应用迁移
flask db upgrade

# 运行测试
pytest

# 代码格式化
black app/
flake8 app/
```

### 前端开发
```bash
cd web

# 启动开发服务器
npm run dev

# 类型检查
npm run type-check

# 代码检查
npm run lint

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 开发规范
- 遵循项目的代码风格
- 添加适当的注释
- 编写单元测试
- 更新相关文档

## 📊 项目路线图

### v1.0.0 (当前版本) ✅
- [x] 基础架构搭建
- [x] 用户认证系统
- [x] 接口测试功能
- [x] Web 自动化测试
- [x] 性能测试
- [x] 测试报告
- [x] 测试文档管理

### v1.1.0 (规划中) 🚧
- [ ] 脚本录制功能
- [ ] CI/CD 集成
- [ ] 定时任务调度
- [ ] 邮件通知
- [ ] 更多测试断言类型
- [ ] 数据驱动测试

### v2.0.0 (长期规划) 📅
- [ ] 可视化测试流程编排
- [ ] 插件市场
- [ ] 多租户支持
- [ ] 移动端测试（Appium）
- [ ] AI 辅助测试
- [ ] 分布式测试执行

## 🐛 已知问题

- [ ] Playwright 浏览器下载可能较慢（建议使用国内镜像）
- [ ] 性能测试高并发时可能内存占用较高
- [ ] Markdown 编辑器在大文件时可能卡顿

## 📝 更新日志

### v1.0.0 (2024-12-24)
- 🎉 首次发布
- ✨ 完成前后端核心功能开发
- 🐳 支持 Docker 部署
- 📚 完善项目文档

详细更新日志请查看 [CHANGELOG.md](./CHANGELOG.md)

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 👥 致谢

感谢以下开源项目：
- [Flask](https://flask.palletsprojects.com/)
- [React](https://reactjs.org/)
- [Ant Design](https://ant.design/)
- [Playwright](https://playwright.dev/)
- [Locust](https://locust.io/)
- [Monaco Editor](https://microsoft.github.io/monaco-editor/)

## 📮 联系方式

- 项目仓库: https://github.com/Asukadaisiki/AutoTestingPlatform
- 问题反馈: https://github.com/Asukadaisiki/AutoTestingPlatform/issues
- 邮箱: [your-email@example.com]

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by [Asukadaisiki](https://github.com/Asukadaisiki)

</div>
