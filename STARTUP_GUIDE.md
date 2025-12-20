# EasyTest 项目启动指南

## 前置要求

### 必需组件
1. **Python 3.10+** - 后端运行环境
2. **Node.js 18+** - 前端构建工具
3. **PostgreSQL 15+** - 生产数据库（开发可用 SQLite）
4. **Redis 5.0+** - 异步任务队列（新增）

### Redis 安装

#### Windows
下载并安装 Redis for Windows：
- 方式 1：[Redis for Windows](https://github.com/tporadowski/redis/releases)
- 方式 2：[Memurai](https://www.memurai.com/) (推荐)

启动 Redis：
```powershell
# 如果下载的是便携版
D:\redis-windows\redis-server.exe

# 如果安装为服务
redis-server
```

验证 Redis：
```powershell
redis-cli ping
# 应返回: PONG
```

#### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis
```

## 数据库配置

⚠️ **重要：项目已切换到 PostgreSQL 数据库**

### 数据库设置
请查看 [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) 获取详细的 PostgreSQL 安装和配置指南。

#### 快速启动（使用 Docker）
```bash
# 启动 PostgreSQL 数据库
docker-compose up -d postgres

# 初始化数据库
cd backend
python init_db.py
python create_test_user.py
```

#### 本地安装 PostgreSQL
参考 [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) 中的详细步骤。

### 测试用户
- 用户名：`admin`
- 密码：`admin123`
- 邮箱：`admin@example.com`

## 启动步骤

### 1. 启动 Redis（新增）
```bash
# Windows（如果未作为服务运行）
D:\redis-windows\redis-server.exe

# Linux/Mac
redis-server

# 验证 Redis
redis-cli ping  # 应返回 PONG
```

### 2. 启动 Celery Worker（新增）
```bash
cd backend

# Windows
.\run_celery.bat

# Linux/Mac
celery -A app.extensions:celery worker --loglevel=info
```

Celery Worker 将处理所有异步任务（Web 测试、性能测试等）。

### 3. 构建前端
```bash
cd web
npm install
npm run build
```

### 4. 启动后端
```bash
cd backend
.\run_server.bat
```
后端运行在 http://127.0.0.1:5211

### 5. 启动 Nginx
```bash
cd nginx
.\start-nginx.bat
```

### 6. 访问应用
打开浏览器访问：**http://localhost:8080**

---

## 快速启动命令汇总

```powershell
# 终端 1：Redis（如未运行）
D:\redis-windows\redis-server.exe

# 终端 2：Celery Worker
cd D:\AutoTestingLearingProject\EasyTest-Web\backend
.\run_celery.bat

# 终端 3：后端
cd D:\AutoTestingLearingProject\EasyTest-Web\backend
.\run_server.bat

# 终端 4：构建前端（首次或修改后）
cd D:\AutoTestingLearingProject\EasyTest-Web\web
npm run build

# 终端 5：Nginx（如未启动）
cd D:\AutoTestingLearingProject\EasyTest-Web\nginx
.\start-nginx.bat

# 访问 http://localhost:8080
```

## Nginx 管理

```bash
# 启动 Nginx
cd nginx
.\start-nginx.bat

# 停止 Nginx
.\stop-nginx.bat

# 重载配置（修改 nginx.conf 后）
nginx -s reload
```

## 端口配置

| 服务 | 端口 | 说明 |
|------|------|------|
| Nginx | 8080 | 前端静态文件 + API 代理 |
| Flask 后端 | 5211 | API 服务 |
| PostgreSQL | 5432 | 数据库 |
| Redis | 6379 | 消息队列和任务结果存储 |
| Celery Worker | - | 异步任务处理器 |

## 测试 API

可以使用提供的测试脚本：
```powershell
cd backend
python test_api.py
```

## 常见问题

### 1. 获取数据失败
**原因**：
- 后端服务器未启动
- PostgreSQL 数据库未启动或未连接
- 数据库未初始化
- 缺少依赖包

**解决方法**：
1. 确保 PostgreSQL 服务正在运行
   - Docker: `docker-compose up -d postgres`
   - 本地: 检查 PostgreSQL 服务状态
2. 确保后端服务器正在运行
3. 检查数据库连接配置（`backend/.env`）
4. 运行 `pip install -r requirements.txt` 安装依赖

### 2. 无法连接数据库
**检查**：
- PostgreSQL 服务是否运行（端口 5432）
- 数据库用户和密码是否正确
- 环境变量配置：`backend/.env`
- 连接字符串：`postgresql://easytest:easytest123@localhost:5432/easytest_dev`

详细故障排查请参考 [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)

### 3. 模块导入错误
**解决**：
- 确保 PYTHONPATH 正确设置
- 使用提供的启动脚本

### 4. 前端修改后不生效
**解决**：
- 需要重新运行 `npm run build` 构建前端

## 重新初始化数据库

如果需要重新初始化数据库：
```bash
cd backend  
python init_db.py
python create_test_user.py
```

## API 测试

### 登录测试
```bash
curl -X POST http://127.0.0.1:5211/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 获取项目列表
```bash
curl http://127.0.0.1:5211/api/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 技术栈

### 后端
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.6.0
- PostgreSQL 15+ (生产数据库)
- psycopg2-binary 2.9.9 (PostgreSQL 驱动)
- Celery 5.3.4 (异步任务队列)
- Redis 5.0.1 (消息代理)

### 前端
- React + TypeScript
- Ant Design
- Vite
