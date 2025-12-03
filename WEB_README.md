# 🚀 接口测试平台 - Web 版

一个现代化的、基于 Web 的接口测试平台，参考 Postman 设计，完整集成 Pytest 框架。

> **📚 完整文档和设计方案已交付！** 查看 [PLATFORM_OVERVIEW.md](./PLATFORM_OVERVIEW.md) 了解全部内容。

## ✨ 核心特性

- 🎨 **现代化 Web 界面** - 参考 Postman，专业美观
- ⚡ **即时请求测试** - 实时发送和查看响应
- 🌍 **多环境支持** - 轻松切换 Dev/Test/Prod
- 🐍 **Python 原生** - 与 Pytest 无缝集成
- 📊 **Allure 报告** - 自动生成美观的测试报告
- 📦 **Docker 部署** - 一键容器化部署
- 🔄 **Postman 兼容** - 支持导入导出
- 💾 **数据持久化** - SQLite 本地存储
- 📱 **响应式设计** - 支持各种屏幕

## 🎯 五分钟快速开始

### Windows (PowerShell)
```powershell
cd web
.\run.bat
```

### Windows (CMD)
```cmd
cd web
run.bat
```

### Linux / Mac
```bash
cd web
chmod +x run.sh
./run.sh
```

然后访问：**http://localhost:5000**

## 📦 项目包含

```
web/                           # Web 应用
├── app.py                    # Flask 后端 (550+ 行)
├── static/
│   ├── index.html           # 前端 HTML (400+ 行)
│   ├── app.js               # Vue.js 逻辑 (600+ 行)
│   └── style.css            # 样式表 (800+ 行)
├── requirements.txt          # Python 依赖
├── Dockerfile               # Docker 配置
├── docker-compose.yml       # Compose 配置
├── run.bat / run.sh         # 启动脚本
└── 📚 文档/
    ├── PLATFORM_OVERVIEW.md           # 📖 功能详解析
    ├── DELIVERY.md          # 📦 交付说明
    └── INDEX.md             # 📚 文档索引

PLATFORM_OVERVIEW.md         # 项目总体说明（本项目根目录）
PROJECT_SUMMARY.md           # 项目结构分析（本项目根目录）
```

## 🎯 核心功能

### 1. 集合管理
- 创建、编辑、删除测试集合
- 卡片式展示，一键打开编辑器
- 查看集合统计信息

### 2. 请求编辑器
- Postman 风格的请求编辑器
- Headers、Body、Params 管理
- 实时预览和发送

### 3. 环境管理
- 多环境配置（Dev/Test/Prod）
- 环境变量自动注入
- 快速切换环境

### 4. 响应查看
- 自动格式化 JSON 显示
- 状态码和响应时间显示
- Headers 详情展示

### 5. 测试运行
- 集成 Pytest 框架
- 一键运行整个集合
- 自动生成 Allure 报告

### 6. 导入导出
- 导入 Postman JSON 集合
- 导出为 Postman 格式
- 支持自动转换

## 📊 技术栈

### 后端
- **Flask 2.3.2** - Web 框架
- **SQLAlchemy 3.0.5** - ORM
- **SQLite/PostgreSQL** - 数据库
- **Pytest 7.4.0** - 测试框架
- **Allure 2.13.2** - 报告工具

### 前端
- **Vue.js 3.3.4** - JavaScript 框架
- **原生 CSS 3** - 样式
- **Fetch API** - HTTP 请求
- **Font Awesome 6.4** - 图标库

### 部署
- **Docker** - 容器化
- **Docker Compose** - 容器编排
- **Gunicorn** - WSGI 服务器（可选）

## 📈 代码统计

| 组件 | 行数 |
|------|------|
| Flask 后端 | 550+ |
| HTML 前端 | 400+ |
| JavaScript | 600+ |
| CSS | 800+ |
| **代码总计** | **2350+** |
| 文档 | **2500+** |
| **项目总计** | **4850+** |

## 🚀 部署方式

### 本地开发
```bash
cd web
run.bat  # Windows
# 或
./run.sh  # Linux/Mac
```

### Docker 容器
```bash
cd web
docker-compose up -d
```

### 生产部署
```bash
# 使用 Gunicorn + Nginx
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📚 文档

### 快速入门
- **[QUICK_START.md](./web/QUICK_START.md)** - 5 分钟快速开始

### 详细功能
- **[README.md](./web/README.md)** - 功能详细说明
- **[DESIGN_GUIDE.md](./web/DESIGN_GUIDE.md)** - 架构设计方案
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - 项目结构分析

### 对标分析
- **[COMPARISON_WITH_POSTMAN.md](./web/COMPARISON_WITH_POSTMAN.md)** - Postman 功能对比

### 导航索引
- **[INDEX.md](./web/INDEX.md)** - 完整文档导航
- **[PLATFORM_OVERVIEW.md](./PLATFORM_OVERVIEW.md)** - 项目总体说明

## 💡 建议补充的功能

### 短期（1-3 个月）
- [ ] 脚本测试支持（Python 脚本）
- [ ] 高级断言管理
- [ ] 请求历史记录
- [ ] 性能分析工具

### 中期（3-6 个月）
- [ ] 用户认证和权限
- [ ] 团队协作功能
- [ ] 高级搜索过滤
- [ ] 导出代码生成

### 长期（6+ 个月）
- [ ] Mock 服务器
- [ ] CI/CD 集成
- [ ] 监控告警
- [ ] 可视化看板

## 🎓 学习资源

### 推荐阅读顺序
1. 本 README (5 分钟)
2. [QUICK_START.md](./web/QUICK_START.md) (5-10 分钟)
3. [README.md](./web/README.md) (20-30 分钟)
4. [DESIGN_GUIDE.md](./web/DESIGN_GUIDE.md) (30-40 分钟)
5. 查看源代码实现

### 按角色推荐
- **测试人员** → QUICK_START.md
- **开发者** → DESIGN_GUIDE.md
- **架构师** → PROJECT_SUMMARY.md
- **决策者** → COMPARISON_WITH_POSTMAN.md

## 🔧 常见问题

### Q: 如何快速开始？
A: 执行 `run.bat` (Windows) 或 `run.sh` (Linux/Mac)，然后访问 http://localhost:5000

### Q: 如何配置环境变量？
A: 在环境配置页面添加环境，设置 Base URL 和 Headers

### Q: 如何运行 Pytest 测试？
A: 在集合卡片点击"运行测试"按钮

### Q: 支持 Postman 导入吗？
A: 支持，在导入功能粘贴 Postman 导出的 JSON

### Q: 数据存储在哪里？
A: 本地 SQLite 数据库 (`test_cases.db`)

查看完整 FAQ：[QUICK_START.md - 常见问题](./web/QUICK_START.md#常见问题)

## 📞 获取帮助

- 📖 查看完整文档：[INDEX.md](./web/INDEX.md)
- 🚀 快速开始指南：[QUICK_START.md](./web/QUICK_START.md)
- 🏗️ 架构设计文档：[DESIGN_GUIDE.md](./web/DESIGN_GUIDE.md)
- 💬 常见问题解答：[QUICK_START.md - FAQ](./web/QUICK_START.md#常见问题)

## 🎯 Postman 对标

| 功能 | 本平台 | Postman |
|------|--------|---------|
| 请求编辑 | ✅ | ✅ |
| 集合管理 | ✅ | ✅ |
| 环境配置 | ✅ | ✅ |
| 自动化测试 | ✅ Pytest | ⚠️ 基础 |
| 本地部署 | ✅ | ❌ |
| 成本 | 💰 免费 | 💰💰💰 付费 |

**完整对比**：[COMPARISON_WITH_POSTMAN.md](./web/COMPARISON_WITH_POSTMAN.md)

## 🎉 项目亮点

✨ **设计亮点**
- 现代化的 UI/UX
- 参考 Postman 的成熟设计
- 清晰的信息架构
- 完整的交互反馈

🔧 **技术亮点**
- 前后端分离架构
- RESTful API 设计
- 规范的数据库设计
- 生产级的代码质量

📚 **文档亮点**
- 详细的架构文档
- 全面的功能说明
- 完整的使用指南
- 清晰的代码注释

🚀 **部署亮点**
- 一键启动脚本
- Docker 开箱即用
- 生产环境最佳实践
- 可扩展的系统设计

## 📈 版本信息

- **当前版本**：v1.0 (完整功能版)
- **发布日期**：2024-01-01
- **许可证**：MIT（开源）
- **Python 版本**：3.7+
- **浏览器支持**：Chrome, Firefox, Safari, Edge

## 🤝 贡献指南

欢迎贡献代码、文档或建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0 (2024-01-01)
✅ 初始版本发布
✅ 核心功能完成
✅ 完整文档交付
✅ 4000+ 行代码
✅ 7 份详细文档

## 🙏 致谢

感谢使用本接口测试平台！

**立即开始**：

```bash
cd web
run.bat  # Windows
# 或
./run.sh  # Linux/Mac
```

访问：http://localhost:5000 🚀

---

**记住这三个资源：**
1. 📚 [INDEX.md](./web/INDEX.md) - 文档导航
2. 🚀 [QUICK_START.md](./web/QUICK_START.md) - 快速开始
3. 🏗️ [PLATFORM_OVERVIEW.md](./PLATFORM_OVERVIEW.md) - 项目概览

**祝你使用愉快！** ✨
