# EasyTest 项目启动指南

## 数据库状态

✅ 数据库已初始化完成
- 数据库文件：`backend/instance/easytest_dev.db`
- 所有表已创建
- 测试用户已创建：
  - 用户名：`admin`
  - 密码：`admin123`
  - 邮箱：`admin@example.com`

## 启动步骤

### 1. 后端启动

#### 方法一：使用批处理脚本（推荐）
```bash
cd backend
.\run_server.bat
```

#### 方法二：手动启动
```powershell
cd backend
$env:PYTHONPATH = "D:\AutoTestingLearingProject\EasyTest-Web\backend"
D:\AutoTestingLearingProject\EasyTest-Web\.venv\Scripts\python.exe app.py
```

后端将在 http://127.0.0.1:5211 运行

### 2. 前端启动

```bash
cd web
npm install
npm run dev
```

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
- 数据库未初始化
- 缺少依赖包

**解决方法**：
1. 确保后端服务器正在运行
2. 检查数据库文件是否存在
3. 运行 `pip install -r requirements.txt` 安装依赖

### 2. 无法连接数据库
**检查**：
- 数据库文件路径：`backend/instance/easytest_dev.db`
- 配置文件：`backend/app/config.py`

### 3. 模块导入错误
**解决**：
- 确保 PYTHONPATH 正确设置
- 使用提供的启动脚本

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
- SQLite (开发环境)

### 前端
- React + TypeScript
- Ant Design
- Vite

## 端口配置

- 后端：5211
- 前端：根据 Vite 配置（通常是 5173）
