# EasyTest 项目启动指南

详细的安装、配置和启动步骤。

---

## 📋 前置要求

### 必需组件

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建工具 |
| PostgreSQL | 15+ | 生产数据库（开发可用 SQLite） |
| Redis | 5.0+ | 异步任务队列 |

### 系统要求
- Windows 10+、Linux、macOS 或其他支持 Python 的操作系统
- 至少 2GB RAM
- 至少 1GB 硬盘空间

---

## 🔧 环境安装

### Windows

#### 1. 安装 Python

1. 访问 [python.org](https://www.python.org/downloads/)
2. 下载 Python 3.10+ 安装程序
3. 运行安装程序，**勾选 "Add Python to PATH"**
4. 完成安装

验证安装：
```powershell
python --version
pip --version
```

#### 2. 安装 Node.js

1. 访问 [nodejs.org](https://nodejs.org/)
2. 下载 LTS 版本（18+）
3. 运行安装程序，按照提示完成安装

验证安装：
```powershell
node --version
npm --version
```

#### 3. 安装 PostgreSQL

1. 访问 [postgresql.org](https://www.postgresql.org/download/windows/)
2. 下载 PostgreSQL 15+ 安装程序
3. 运行安装程序，记下密码和端口号（默认 5432）
4. 完成安装

验证安装：
```powershell
# 打开 PostgreSQL 命令行
psql -U postgres -c "SELECT version();"
```

#### 4. 安装 Redis

**方式 1：使用 Redis for Windows（推荐）**

1. 访问 [github.com/tporadowski/redis](https://github.com/tporadowski/redis/releases)
2. 下载最新版本（如 Redis-x64-5.0.14.1.zip）
3. 解压到本地目录（如 `D:\redis-windows`）
4. 启动 Redis：
   ```powershell
   D:\redis-windows\redis-server.exe
   ```

**方式 2：使用 Memurai（Windows 原生 Redis）**

1. 访问 [memurai.com](https://www.memurai.com/)
2. 下载并安装
3. 自动作为服务启动

验证 Redis：
```powershell
redis-cli ping
# 应返回: PONG
```

#### Linux/macOS

```bash
# Ubuntu/Debian
sudo apt-get install python3.10 python3-pip python3-venv
sudo apt-get install nodejs npm
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install redis-server

# macOS
brew install python@3.10 node postgresql redis

# 启动服务
sudo systemctl start postgresql redis
# 或
brew services start postgresql redis
```

---

## 📦 项目初始化

### 1. 克隆项目

```bash
git clone https://github.com/Asukadaisiki/easytest.git
cd EasyTest-Web
```

### 2. 创建 Python 虚拟环境（可选但推荐）

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `backend/.env` 文件：

```bash
# Flask 配置
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# 数据库配置
# 开发环境（SQLite）
DATABASE_URL=sqlite:///easytest_dev.db

# 生产环境（PostgreSQL）
# 根据你的 PostgreSQL 配置修改用户名、密码、主机、数据库名
# DATABASE_URL=postgresql://easytest:password@localhost:5432/easytest_db

# JWT 配置
JWT_SECRET_KEY=jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=86400
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# Celery 配置
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# 服务配置
FLASK_APP=app.py
SERVER_HOST=127.0.0.1
SERVER_PORT=5211
```

### 5. 初始化数据库

#### 使用 SQLite（开发环境推荐）

```bash
cd backend
python init_db.py
```

此命令会：
- 创建数据库文件 `easytest_dev.db`
- 创建所有表
- 插入默认数据

#### 使用 PostgreSQL（生产环境推荐）

1. **创建数据库和用户**

```sql
-- 使用 psql 连接到 PostgreSQL
psql -U postgres

-- 创建用户
CREATE USER easytest WITH PASSWORD 'password';

-- 创建数据库
CREATE DATABASE easytest_db OWNER easytest;

-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE easytest_db TO easytest;

-- 退出
\q
```

2. **修改 `.env` 中的数据库 URL**

```bash
DATABASE_URL=postgresql://easytest:password@localhost:5432/easytest_db
```

3. **初始化数据库**

```bash
cd backend
python init_db.py
```

### 6. 安装前端依赖

```bash
cd web
npm install
```

---

## 🚀 启动项目

### 步骤 1：启动 Redis

**Windows：**
```powershell
# 如果使用独立的 Redis 可执行文件
D:\redis-windows\redis-server.exe

# 或者（如果安装为服务）
redis-server

# 验证
redis-cli ping  # 应返回 PONG
```

**Linux/macOS：**
```bash
redis-server

# 验证
redis-cli ping  # 应返回 PONG
```

### 步骤 2：启动 Celery Worker（新终端）

Celery Worker 用于处理异步任务（Web 测试、性能测试等）。

**Windows：**
```powershell
cd backend
.\run_celery.bat
```

**Linux/macOS：**
```bash
cd backend
celery -A app.extensions:celery worker --loglevel=info
```

预期输出：
```
 -------------- celery@HOSTNAME v5.3.4 (emerald-rush)
--- ***** -----
-- ******* ----
- *** --- * ---
- ** ---------- [config]
- ** ---------- .
- ** ---------- [queues]
-  * ----------     - celery
-  ----------
[tasks]
...
[2025-12-28 10:00:00,000: INFO/MainProcess] Connected to redis://...
```

### 步骤 3：启动后端服务（新终端）

**Windows：**
```powershell
cd backend
.\run_server.bat
```

**Linux/macOS：**
```bash
cd backend
python app.py
```

预期输出：
```
 * Running on http://127.0.0.1:5211
 * Press CTRL+C to quit
```

访问：`http://127.0.0.1:5211`

### 步骤 4：构建前端（新终端）

```bash
cd web
npm run build
```

构建完成后会在 `web/dist` 文件夹生成静态文件。

### 步骤 5：启动 Nginx（新终端）

**Windows：**
```powershell
cd nginx
.\start-nginx.bat
```

**Linux/macOS：**
```bash
cd nginx
./start-nginx.sh  # 需要先创建此脚本或使用 docker
```

### 步骤 6：访问应用

打开浏览器访问：**http://localhost:8080**

登录信息：
- 用户名：`admin`
- 密码：`admin123`

---

## 📋 快速启动清单

### 第一次启动（完整流程）

| 步骤 | 命令 | 终端 | 说明 |
|------|------|------|------|
| 1 | `cd backend && pip install -r requirements.txt` | 1 | 安装依赖（仅需一次） |
| 2 | `python init_db.py` | 1 | 初始化数据库（仅需一次） |
| 3 | 配置 `.env` | - | 配置环境变量（仅需一次） |
| 4 | `redis-server` 或 `D:\redis\redis-server.exe` | 1 | 启动 Redis |
| 5 | `cd backend && .\run_celery.bat` | 2 | 启动 Celery Worker |
| 6 | `cd backend && .\run_server.bat` | 3 | 启动后端 |
| 7 | `cd web && npm run build` | 4 | 构建前端 |
| 8 | `cd nginx && .\start-nginx.bat` | 5 | 启动 Nginx |
| 9 | 访问 `http://localhost:8080` | 浏览器 | 使用应用 |

### 日常启动（已配置过）

| 步骤 | 命令 | 终端 | 说明 |
|------|------|------|------|
| 1 | `redis-server` 或 `D:\redis\redis-server.exe` | 1 | 启动 Redis |
| 2 | `cd backend && .\run_celery.bat` | 2 | 启动 Celery Worker |
| 3 | `cd backend && .\run_server.bat` | 3 | 启动后端 |
| 4 | `cd nginx && .\start-nginx.bat` | 4 | 启动 Nginx（如果需要） |
| 5 | 访问 `http://localhost:8080` | 浏览器 | 使用应用 |

---

## 🐳 Docker 快速启动

如果已安装 Docker 和 Docker Compose，可以一键启动所有服务：

### 开发环境

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

### 生产环境

```bash
# 启动所有服务
docker-compose -f docker-compose.prod.yml up -d

# 停止服务
docker-compose -f docker-compose.prod.yml down
```

---

## 🌐 端口和 URL

### 服务端口

| 服务 | 端口 | URL | 说明 |
|------|------|-----|------|
| Nginx | 8080 | http://localhost:8080 | 前端和 API 反向代理 |
| Flask 后端 | 5211 | http://127.0.0.1:5211 | API 服务 |
| PostgreSQL | 5432 | - | 数据库（不提供网络访问） |
| Redis | 6379 | - | 消息队列（不提供网络访问） |

### 重要 URL

| 功能 | URL | 说明 |
|------|-----|------|
| Web 应用 | http://localhost:8080 | 前端应用 |
| API 文档 | 在应用内访问 | Swagger UI |
| 登录 | http://localhost:8080/login | 用户登录 |
| 注册 | http://localhost:8080/register | 新用户注册 |

---

## ✅ 验证安装

### 验证后端

```bash
# 检查后端是否运行
curl http://127.0.0.1:5211/api/v1/auth/me -H "Authorization: Bearer <token>"

# 或使用 Postman、Insomnia 等工具
# POST http://127.0.0.1:5211/api/v1/auth/login
# Body: {"username": "admin", "password": "admin123"}
```

### 验证前端

打开浏览器访问 http://localhost:8080，应该看到登录页面。

### 验证数据库

```bash
# SQLite
sqlite3 backend/easytest_dev.db ".tables"

# PostgreSQL
psql -U easytest -d easytest_db -c "\dt"
```

### 验证 Redis

```bash
redis-cli ping
# 应返回: PONG
```

---

## ⚠️ 常见问题

### 1. 数据库连接失败

**症状：** 启动后端时报错 `无法连接数据库`

**原因：**
- PostgreSQL 服务未运行
- 数据库用户名/密码错误
- `.env` 配置错误

**解决：**
```bash
# 检查 PostgreSQL 状态
pg_isready -h localhost -p 5432

# 检查 .env 中的 DATABASE_URL 是否正确
# 尝试手动连接
psql -U easytest -d easytest_db -h localhost

# 重新初始化数据库
python init_db.py
```

### 2. Redis 连接失败

**症状：** Celery Worker 启动失败，报错 `无法连接 Redis`

**原因：**
- Redis 服务未启动
- Redis 端口被占用

**解决：**
```bash
# 启动 Redis
redis-server

# 验证连接
redis-cli ping

# 检查端口占用（Windows）
netstat -ano | findstr 6379
```

### 3. 前端无法加载

**症状：** 访问 http://localhost:8080 显示 404 或无法连接

**原因：**
- 前端未构建
- Nginx 未启动

**解决：**
```bash
# 重新构建前端
cd web
npm run build

# 启动 Nginx
cd nginx
.\start-nginx.bat

# 检查 Nginx 状态
curl http://localhost:8080
```

### 4. 模块导入错误

**症状：** 启动后端时报 `ModuleNotFoundError`

**原因：**
- 虚拟环境未激活
- 依赖未安装完整

**解决：**
```bash
# 激活虚拟环境
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 重新安装依赖
pip install -r requirements.txt
```

### 5. Nginx 端口被占用

**症状：** 启动 Nginx 失败，报错 `端口 8080 已被使用`

**原因：**
- 8080 端口已被其他程序占用
- Nginx 已有实例运行

**解决：**
```bash
# Windows：查找占用 8080 的进程
netstat -ano | findstr 8080

# Linux：查找占用 8080 的进程
lsof -i :8080

# 停止占用的进程，或更改 nginx.conf 中的端口
```

### 6. 前端修改后不生效

**症状：** 修改了前端代码但访问时仍显示旧内容

**原因：**
- 没有重新构建前端
- 浏览器缓存

**解决：**
```bash
# 重新构建前端
cd web
npm run build

# 清除浏览器缓存（Ctrl+Shift+Delete）或使用无痕窗口
```

### 7. 性能测试/Web 测试任务不执行

**症状：** 提交任务后，任务一直在 pending 状态

**原因：**
- Celery Worker 未启动
- Redis 连接失败

**解决：**
```bash
# 检查 Celery Worker 是否运行
ps aux | grep celery  # Linux
tasklist | findstr celery  # Windows

# 重启 Celery Worker
cd backend
.\run_celery.bat  # Windows
celery -A app.extensions:celery worker --loglevel=info  # Linux/Mac
```

---

## 🔄 日常使用

### 关闭应用

关闭所有终端窗口即可。如需正常关闭，使用 Ctrl+C：

```bash
# 在各自的终端按 Ctrl+C

# 或停止 Nginx
cd nginx
.\stop-nginx.bat  # Windows
```

### 重新启动

重新执行启动步骤即可。数据会保留在数据库中。

### 重置数据库

```bash
cd backend

# 删除旧数据库
rm easytest_dev.db  # Linux/Mac
del easytest_dev.db  # Windows

# 重新初始化
python init_db.py
```

---

## 📞 获取帮助

如遇到问题，请：

1. 检查本文档中的"常见问题"部分
2. 查看各服务的日志输出
3. 检查防火墙设置
4. 提交 GitHub Issue

---

## 💡 开发小贴士

### 前端开发模式

如需热重载（修改即生效）：

```bash
cd web
npm run dev
```

然后访问 http://localhost:5173（Vite 开发服务器）

但需要配置 API 代理，详见 `web/vite.config.ts`

### 后端调试

使用 Flask 调试模式：

```bash
cd backend
FLASK_DEBUG=1 python app.py
```

### 数据库迁移

修改模型后需要生成迁移：

```bash
cd backend
flask db migrate -m "描述"
flask db upgrade
```

---

<div align="center">

**👍 成功启动？开始使用 EasyTest 进行测试吧！**

参考 [API.md](API.md) 了解所有可用接口。

</div>
