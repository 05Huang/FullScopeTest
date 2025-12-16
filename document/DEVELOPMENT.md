# EasyTest 开发文档

## 目录

1. [项目架构](#项目架构)
2. [技术栈](#技术栈)
3. [API 设计](#api-设计)
4. [数据库设计](#数据库设计)
5. [前端开发指南](#前端开发指南)
6. [后端开发指南](#后端开发指南)
7. [部署指南](#部署指南)

## 项目架构

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户浏览器                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     Nginx 反向代理                           │
│                  (静态资源 + API 转发)                        │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
┌────────────▼────────────┐    ┌──────────────▼───────────────┐
│   前端 (React + Vite)    │    │   后端 (Flask + Gunicorn)    │
│                          │    │                              │
│  • React 18              │    │  • Flask 3.0                 │
│  • TypeScript            │    │  • Flask-SQLAlchemy          │
│  • Ant Design 5          │    │  • Flask-JWT-Extended        │
│  • Zustand               │    │  • Flask-Migrate             │
│  • React Router 6        │    │                              │
└──────────────────────────┘    └──────────────┬───────────────┘
                                               │
                                ┌──────────────▼───────────────┐
                                │         数据库层              │
                                │                              │
                                │  • PostgreSQL (生产)         │
                                │  • SQLite (开发)             │
                                │  • Redis (缓存/会话)         │
                                └──────────────────────────────┘
```

### 模块架构

```
EasyTest
├── 用户认证模块
│   ├── 注册/登录
│   ├── JWT Token 管理
│   └── 权限控制
│
├── 接口测试模块
│   ├── 请求构造器
│   ├── 环境变量管理
│   ├── 用例集合管理
│   ├── 前置/后置脚本
│   └── 断言引擎
│
├── Web 自动化模块
│   ├── Playwright 集成
│   ├── 脚本管理
│   ├── 元素库管理
│   └── 录制器
│
├── 性能测试模块
│   ├── Locust 集成
│   ├── 场景管理
│   ├── 实时监控
│   └── 结果分析
│
└── 报告中心
    ├── Allure 报告
    ├── 趋势分析
    └── 导出功能
```

## 技术栈

### 前端

| 技术 | 版本 | 说明 |
|------|------|------|
| React | 18.3 | UI 框架 |
| TypeScript | 5.6 | 类型系统 |
| Vite | 5.4 | 构建工具 |
| Ant Design | 5.x | UI 组件库 |
| Zustand | 5.x | 状态管理 |
| React Router | 6.x | 路由管理 |
| Axios | 1.x | HTTP 客户端 |
| Monaco Editor | 4.x | 代码编辑器 |
| ECharts | 5.x | 图表库 |

### 后端

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 运行时 |
| Flask | 3.0 | Web 框架 |
| SQLAlchemy | 2.x | ORM |
| Flask-JWT-Extended | 4.x | JWT 认证 |
| Flask-Migrate | 4.x | 数据库迁移 |
| Playwright | 1.x | 浏览器自动化 |
| Locust | 2.x | 性能测试 |
| Allure | 2.x | 测试报告 |

### 数据库

| 类型 | 用途 |
|------|------|
| PostgreSQL | 主数据库（生产环境） |
| SQLite | 主数据库（开发环境） |
| Redis | 缓存、会话存储 |

## API 设计

### RESTful 规范

- 使用标准 HTTP 方法
- 统一响应格式
- JWT Bearer Token 认证

### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

### API 端点

#### 认证

```
POST /api/auth/register    # 用户注册
POST /api/auth/login       # 用户登录
POST /api/auth/refresh     # 刷新令牌
GET  /api/auth/me          # 获取当前用户
PUT  /api/auth/password    # 修改密码
```

#### 项目

```
GET    /api/projects       # 获取项目列表
POST   /api/projects       # 创建项目
GET    /api/projects/:id   # 获取项目详情
PUT    /api/projects/:id   # 更新项目
DELETE /api/projects/:id   # 删除项目
```

#### 接口测试

```
GET    /api/api-test/collections       # 获取用例集合
POST   /api/api-test/collections       # 创建用例集合
GET    /api/api-test/cases             # 获取测试用例
POST   /api/api-test/cases             # 创建测试用例
POST   /api/api-test/execute           # 执行测试
```

## 数据库设计

### ER 图

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │   Project    │       │ Environment  │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id           │───────│ id           │───────│ id           │
│ username     │       │ name         │       │ name         │
│ email        │       │ description  │       │ base_url     │
│ password     │       │ user_id      │       │ project_id   │
│ created_at   │       │ created_at   │       │ variables    │
└──────────────┘       └──────────────┘       └──────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ ApiTestCase  │   │WebTestScript │   │PerfScenario  │
├──────────────┤   ├──────────────┤   ├──────────────┤
│ id           │   │ id           │   │ id           │
│ name         │   │ name         │   │ name         │
│ method       │   │ browser      │   │ users        │
│ url          │   │ script       │   │ duration     │
│ headers      │   │ project_id   │   │ project_id   │
│ body         │   │ created_at   │   │ created_at   │
│ project_id   │   └──────────────┘   └──────────────┘
└──────────────┘
```

## 前端开发指南

### 目录结构

```
src/
├── components/          # 通用组件
├── layouts/             # 布局组件
├── pages/               # 页面组件
│   ├── api-test/       # 接口测试
│   ├── web-test/       # Web 测试
│   └── perf-test/      # 性能测试
├── services/            # API 服务
├── stores/              # 状态管理
├── styles/              # 样式文件
└── utils/               # 工具函数
```

### 开发规范

1. 组件使用函数式组件 + Hooks
2. 状态管理使用 Zustand
3. 样式使用 Tailwind CSS + Ant Design
4. 代码格式化使用 Prettier
5. 代码检查使用 ESLint

## 后端开发指南

### 目录结构

```
app/
├── api/                 # API 路由
├── models/              # 数据模型
├── services/            # 业务逻辑
├── utils/               # 工具函数
├── config.py            # 配置文件
└── extensions.py        # Flask 扩展
```

### 开发规范

1. 遵循 PEP 8 代码规范
2. 使用类型注解
3. 统一异常处理
4. 统一响应格式

## 部署指南

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 手动部署

1. 安装 Nginx
2. 配置反向代理
3. 使用 Gunicorn 运行 Flask
4. 使用 PM2 或 systemd 管理进程
