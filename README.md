# EasyTest - 简单易用的自动化测试平台

<div align="center">

![EasyTest Logo](docs/logo.png)

**专为个人开发者打造的一站式自动化测试平台**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.3-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)

</div>

## ✨ 特性

- 🚀 **简单高效** - 开箱即用，无需复杂配置
- 🔧 **接口测试** - 类似 Postman 的接口测试体验，支持环境变量、断言脚本、cURL 导出
- 🌐 **Web 自动化** - 基于 Playwright 的 Web UI 自动化测试，支持录制和元素库
- ⚡ **性能测试** - 集成 Locust，支持实时监控和结果分析
- 📊 **可视化报告** - 完整的测试报告和趋势分析
- 📝 **测试文档** - Markdown 编辑器，方便管理测试文档

## 📅 更新日志

### v1.1.0 (2025-12-24)

#### 🆕 新增功能
- **Web 测试录制器** - 支持录制浏览器操作，自动生成 Playwright 脚本
- **元素库管理** - 统一管理页面元素，支持 CSS/XPath/ID 等定位方式
- **性能测试实时监控** - 实时查看运行中测试的响应时间、吞吐量、错误率
- **性能测试结果分析** - 详细的响应时间分布、请求统计、历史对比

#### 🔧 功能完善
- **API 测试工作台**
  - 从数据库加载测试用例和集合
  - 支持复制为 cURL 命令
  - 支持保存请求为用例
  - 参数/请求头表格添加删除功能
- **用例管理**
  - 编辑用例功能
  - 复制用例功能
  - 批量删除功能
  - 搜索过滤功能
- **脚本管理**
  - 编辑脚本功能
  - 批量执行和删除
  - 搜索过滤功能
- **场景管理**
  - 编辑场景功能
  - 批量删除功能
  - 搜索过滤功能
- **报告管理**
  - 批量删除和下载
  - 搜索过滤功能
- **文档管理**
  - 搜索过滤功能

#### 🐛 Bug 修复
- 修复请求头变量命名冲突问题
- 修复编译警告（未使用变量）

## 📦 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- PostgreSQL (可选，默认使用 SQLite)

### 安装

1. **克隆项目**

```bash
git clone https://github.com/Asukadaisiki/easytest.git
cd easytest
```

2. **安装后端依赖**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **安装前端依赖**

```bash
cd ../web
npm install
```

4. **初始化数据库**

```bash
cd ../backend
flask db upgrade
```

5. **启动服务**

```bash
# 终端 1: 启动后端
cd backend
python wsgi.py

# 终端 2: 启动前端
cd web
npm run dev
```

6. **访问应用**

打开浏览器访问 http://localhost:3000

## 🏗️ 项目结构

```
easytest/
├── backend/                 # 后端 Flask 应用
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   └── utils/          # 工具函数
│   ├── requirements.txt
│   └── wsgi.py
├── web/                     # 前端 React 应用
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── services/       # API 服务
│   │   └── stores/         # 状态管理
│   └── package.json
├── document/                # 项目文档
└── docker/                  # Docker 配置
```

## 📚 功能模块

### 接口测试

- 支持 GET、POST、PUT、DELETE、PATCH 等 HTTP 方法
- 请求参数、Headers、Body 配置
- 环境变量管理
- 前置/后置脚本
- 断言验证
- 用例集合管理

### Web 自动化测试

- 基于 Playwright 的浏览器自动化
- 支持 Chromium、Firefox、WebKit
- 脚本录制功能
- 元素库管理
- 截图和视频录制

### 性能测试

- 基于 Locust 的性能测试
- 并发用户模拟
- 实时监控面板
- 性能报告生成

## 🔧 配置

### 环境变量

```bash
# backend/.env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///easytest.db
# DATABASE_URL=postgresql://user:pass@localhost/easytest

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
```

## 🐳 Docker 部署

```bash
# 开发环境
docker-compose up -d

# 生产环境
docker-compose -f docker-compose.prod.yml up -d
```

## 📖 API 文档

启动后端服务后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:5000/api/docs

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<div align="center">
Made with ❤️ by EasyTest Team
</div>
