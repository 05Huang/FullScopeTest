# EasyTest 项目启动指南

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

### 1. 构建前端
```bash
cd web
npm install
npm run build
```

### 2. 启动后端
```bash
cd backend
.\run_server.bat
```
后端运行在 http://127.0.0.1:5211

### 3. 启动 Nginx
```bash
cd nginx
.\start-nginx.bat
```

### 4. 访问应用
打开浏览器访问：**http://localhost:8080**

---

## 快速启动命令汇总

```powershell
# 终端 1：后端
cd D:\AutoTestingLearingProject\EasyTest-Web\backend
.\run_server.bat

# 终端 2：构建前端（首次或修改后）
cd D:\AutoTestingLearingProject\EasyTest-Web\web
npm run build

# 终端 3：Nginx（如未启动）
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

### 前端
- React + TypeScript
- Ant Design
- Vite
