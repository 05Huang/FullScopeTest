# 开发环境搭建指南

## 快速开始（Docker 一键启动）

### 前置条件
- Docker Desktop 4.0+（含 Docker Compose v2）
- Git

### 一键启动

```bash
# 克隆项目
git clone <repo-url>
cd FullScopeTest

# 启动所有服务（Redis + Flask 后端 + Vite 前端）
docker-compose -f docker-compose.dev.yml up --build

# 或后台启动
docker-compose -f docker-compose.dev.yml up -d --build
```

启动后访问：
- **前端**: http://localhost:3001
- **后端 API**: http://localhost:5000
- **健康检查**: http://localhost:5000/health

### 使用 PostgreSQL（可选）

默认使用 SQLite，如需 PostgreSQL：

```bash
# 启用 PostgreSQL profile
docker-compose -f docker-compose.dev.yml --profile postgres up --build

# 或设置环境变量使用 PostgreSQL
export DATABASE_URL=postgresql://fullscopetest:devpassword@localhost:5432/fullscopetest_dev
```

### 清理环境

```bash
# 停止服务（保留数据）
docker-compose -f docker-compose.dev.yml down

# 停止服务并清除所有数据（包括数据库）
docker-compose -f docker-compose.dev.yml down -v
```

---

## 本地开发（不使用 Docker）

### 前置条件
- Python 3.10+
- Node.js 18+
- Redis（本地安装或 Docker）

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，至少设置：
# SECRET_KEY=your-secret-key
# JWT_SECRET_KEY=your-jwt-secret-key

# 初始化数据库
flask db upgrade

# 启动后端
flask run --host=0.0.0.0 --port=5000 --reload
```

### 前端启动

```bash
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### Redis

```bash
# 使用 Docker 启动 Redis
docker run -d --name fst_redis -p 6379:6379 redis:7-alpine
```

---

## 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Flask 密钥 | 必须设置 |
| `JWT_SECRET_KEY` | JWT 签名密钥 | 必须设置 |
| `DATABASE_URL` | 数据库连接串 | `sqlite:///fullscopetest.db` |
| `REDIS_URL` | Redis 连接串 | `redis://localhost:6379/0` |
| `FLASK_ENV` | Flask 环境 | `development` |
| `AI_ASSISTANT_API_KEY` | AI 助手 API Key | 空（AI 功能不可用） |

---

## 常见问题

### Q: 数据库迁移失败怎么办？

```bash
cd backend
# 重置数据库（开发环境）
python scripts/reset_db.py --seed --force
```

### Q: 前端无法连接后端？

检查 `web/vite.config.ts` 中的 proxy 配置，确保指向正确的后端地址。

### Q: Redis 连接失败？

```bash
# 检查 Redis 是否运行
docker ps | grep redis
# 或
redis-cli ping
```
