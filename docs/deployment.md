# FullScopeTest 部署指南

本文档提供 FullScopeTest 平台的完整部署指南，包括开发环境和生产环境的部署方案。

## 系统要求

### 硬件要求

| 环境 | CPU | 内存 | 磁盘 |
|------|-----|------|------|
| 开发环境 | 2 核+ | 4GB+ | 20GB+ |
| 生产环境 | 4 核+ | 8GB+ | 100GB+ |
| 高并发生产 | 8 核+ | 16GB+ | 200GB+ |

### 软件要求

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **操作系统**: Linux (推荐 Ubuntu 20.04+)、macOS、Windows with WSL2

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/05Huang/FullScopeTest.git
cd FullScopeTest
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

### 3. 启动开发环境

```bash
docker-compose up -d
```

### 4. 访问服务

- **前端**: http://localhost:3000
- **后端 API**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001

## 开发环境部署

### 步骤 1: 配置环境变量

编辑 .env 文件，设置以下必要变量：

```env
POSTGRES_USER=fullscopetest
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=fullscopetest_dev
SECRET_KEY=your_random_secret_key_at_least_32_chars
JWT_SECRET_KEY=your_random_jwt_secret_key_at_least_32_chars
REDIS_URL=redis://redis:6379/0
```

### 步骤 2: 启动服务

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f backend
```

### 步骤 3: 初始化数据库

```bash
docker-compose exec backend bash
flask db upgrade
python create_admin.py
exit
```

### 开发环境服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| backend | 5000 | Flask 后端 API |
| postgres | 5432 | PostgreSQL 数据库 |
| redis | 6379 | Redis 缓存/消息队列 |
| prometheus | 9090 | Prometheus 监控 |
| grafana | 3001 | Grafana 可视化 |

## 生产环境部署

### 步骤 1: 配置生产环境变量

```env
POSTGRES_USER=fullscopetest
POSTGRES_PASSWORD=your_very_strong_password
POSTGRES_DB=fullscopetest_prod
DATABASE_URL=postgresql://fullscopetest:your_very_strong_password@postgres:5432/fullscopetest_prod
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_random_secret_key
JWT_SECRET_KEY=your_random_jwt_secret_key
FLASK_ENV=production
CELERY_ENABLE=true
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 步骤 2: 配置 SSL 证书

```bash
# 使用 Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

# 复制证书
mkdir -p docker/nginx/ssl
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem docker/nginx/ssl/
cp /etc/letsencrypt/live/your-domain.com/privkey.pem docker/nginx/ssl/
```

### 步骤 3: 启动生产环境

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 环境变量配置

### 必需变量

| 变量名 | 说明 |
|--------|------|
| POSTGRES_USER | PostgreSQL 用户名 |
| POSTGRES_PASSWORD | PostgreSQL 密码 |
| POSTGRES_DB | PostgreSQL 数据库名 |
| SECRET_KEY | Flask 应用密钥 |
| JWT_SECRET_KEY | JWT 签名密钥 |

### 可选变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DATABASE_URL | 完整数据库连接 URL | 自动生成 |
| REDIS_URL | Redis 连接 URL | redis://redis:6379/0 |
| FLASK_ENV | Flask 环境 | development |
| CELERY_ENABLE | 启用 Celery | false |

## 常见问题排查

### 1. 数据库连接失败

```bash
docker-compose ps postgres
docker-compose logs postgres
docker-compose restart postgres backend
```

### 2. Redis 连接失败

```bash
docker-compose ps redis
docker-compose exec redis redis-cli ping
```

### 3. 端口冲突

```bash
netstat -tulpn | grep :5000
# 修改 docker-compose.yml 中的端口映射
```

### 4. 日志查看

```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs --tail 100 backend
```

### 5. 健康检查

```bash
curl http://localhost:5000/health
docker-compose exec postgres pg_isready -U fullscopetest
docker-compose exec redis redis-cli ping
```

## 更新部署

```bash
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose exec backend flask db upgrade
```
