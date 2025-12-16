# EasyTest 后端

## 技术栈

- **框架**: Flask 3.0
- **数据库**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (Flask-JWT-Extended)
- **测试框架**: Pytest + Allure
- **Web 自动化**: Playwright
- **性能测试**: Locust
- **任务队列**: Celery + Redis

## 项目结构

```
backend/
├── app/                    # 应用核心
│   ├── api/                # API 接口
│   ├── models/             # 数据模型
│   ├── services/           # 业务逻辑
│   ├── tasks/              # 异步任务
│   ├── utils/              # 工具函数
│   ├── __init__.py         # 应用工厂
│   ├── config.py           # 配置管理
│   └── extensions.py       # Flask 扩展
├── migrations/             # 数据库迁移
├── tests/                  # 单元测试
├── manage.py               # CLI 管理命令
├── wsgi.py                 # WSGI 入口
└── requirements.txt        # Python 依赖
```

## 快速开始

### 1. 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
copy .env.example .env
# 编辑 .env 文件，修改数据库连接等配置
```

### 4. 初始化数据库

```bash
# 确保 PostgreSQL 已启动，并创建数据库
# 创建数据库: CREATE DATABASE easytest_dev;

# 初始化数据库表
python manage.py init_db

# 创建管理员账号
python manage.py create_admin
```

### 5. 启动开发服务器

```bash
flask run --port=5000
# 或
python wsgi.py
```

## API 文档

启动服务后访问: http://localhost:5000/api/v1/

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| GET | /api/v1/auth/me | 获取当前用户 |
| POST | /api/v1/auth/refresh | 刷新 Token |

### 项目接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/projects | 获取项目列表 |
| POST | /api/v1/projects | 创建项目 |
| GET | /api/v1/projects/:id | 获取项目详情 |
| PUT | /api/v1/projects/:id | 更新项目 |
| DELETE | /api/v1/projects/:id | 删除项目 |

### 环境接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/projects/:id/environments | 获取环境列表 |
| POST | /api/v1/projects/:id/environments | 创建环境 |
| PUT | /api/v1/environments/:id | 更新环境 |
| DELETE | /api/v1/environments/:id | 删除环境 |

## 数据库迁移

```bash
# 生成迁移文件
flask db migrate -m "描述"

# 执行迁移
flask db upgrade

# 回滚
flask db downgrade
```
