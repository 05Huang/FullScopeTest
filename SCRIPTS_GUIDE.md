# EasyTest 脚本使用指南

## 快速开始

推荐使用 `START.bat` 一键启动所有服务。

---

## 脚本分类

### 启动脚本 (scripts/start/)

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| `scripts/start/start-all.bat` | 启动所有服务 | 完整启动（Redis + Celery + 后端 + Nginx） |
| `scripts/start/start-backend.bat` | 只启动后端 | 仅需后端服务时 |
| `scripts/stop/start-nginx.bat` | 启动 Nginx | 仅需 Web 服务时 |

### 重启脚本 (scripts/restart/)

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| `scripts/restart/quick-restart.bat` | 构建前端 + 重启后端 | 代码修改后快速验证（推荐） |
| `scripts/restart/restart-all.bat` | 完整重启 | 包含 Redis 和 Celery 的完整重启 |

### 停止脚本 (scripts/stop/)

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| `scripts/stop/stop-all.bat` | 停止所有服务 | 需要完全停止服务时 |
| `scripts/stop/stop-nginx.bat` | 停止 Nginx | 仅停止 Web 服务 |

### 构建脚本 (scripts/build/)

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| `scripts/build/build-frontend.bat` | 只构建前端 | 只修改了前端代码时 |

### 后端专用脚本 (scripts/backend/)

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| `scripts/backend/run-celery.bat` | 启动 Celery Worker | 异步任务处理 |
| `scripts/backend/run-dev.bat` | 开发模式启动 | 本地开发调试 |
| `scripts/backend/run-server.bat` | 启动生产服务器 | 生产环境运行 |

---

## 使用场景

### 场景1：首次启动项目
```bash
# 1. 确保已安装依赖
cd backend && pip install -r requirements.txt
cd ../web && npm install

# 2. 初始化数据库
cd ../backend && python init_db.py

# 3. 一键启动所有服务
cd ..
START.bat
```

### 场景2：日常开发
```bash
# 修改代码后快速重启
scripts/restart/quick-restart.bat
```

### 场景3：只修改前端
```bash
# 只需构建前端
scripts/build/build-frontend.bat
```

### 场景4：完整重启
```bash
# 包含 Redis 和 Celery 的完整重启
scripts/restart/restart-all.bat
```

### 场景5：停止所有服务
```bash
# 停止所有服务
scripts/stop/stop-all.bat
```

---

## 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端 | http://localhost:8080 | 通过 Nginx 访问 |
| 后端 API | http://localhost:5211/api/v1 | Flask 后端 |
| Redis | localhost:6379 | 消息队列 |

---

## 默认测试账号

- 用户名：`admin`
- 密码：`admin123`

---

## 注意事项

### Redis 需要单独安装
- Windows: 下载 [Redis for Windows](https://github.com/microsoftarchive/redis/releases)
- 或使用 Docker: `docker run -d -p 6379:6379 redis`

### Nginx 配置
- 前端通过 Nginx 提供服务：`http://localhost:8080`
- 需要修改 `scripts/stop/start-nginx.bat` 中的 `NGINX_PATH` 为你的 Nginx 安装路径

### 构建完成后
- 必须刷新浏览器（`Ctrl + Shift + R`）才能看到更新
- 建议清除浏览器缓存
