# PostgreSQL 本地配置完成

## ✅ 迁移成功

已成功将数据库从 SQLite 迁移到 PostgreSQL！

## 📊 数据库信息

- **数据库**: `easytest_dev`
- **用户**: `easytest`
- **密码**: `easytest123`
- **端口**: `5432`
- **连接字符串**: `postgresql://easytest:easytest123@localhost:5432/easytest_dev`

## 🗂️ 已创建的表

1. users - 用户表
2. projects - 项目表
3. environments - 环境表
4. api_test_collections - API 测试集合表
5. api_test_cases - API 测试用例表
6. web_test_scripts - Web 测试脚本表
7. perf_test_scenarios - 性能测试场景表
8. test_runs - 测试运行记录表
9. test_documents - 测试文档表

## 👤 测试用户

- **用户名**: admin
- **密码**: admin123
- **邮箱**: admin@example.com

## 🚀 启动服务

### 后端服务
```bash
cd backend
D:/AutoTestingLearingProject/EasyTest-Web/.venv/Scripts/python.exe app.py
```

服务地址: http://127.0.0.1:5211

### 前端服务
```bash
cd web
npm run dev
```

## 🔧 常用命令

### 连接数据库
```bash
$env:PGPASSWORD = "easytest123"
& "D:\PostgreSQL\bin\psql.exe" -U easytest -d easytest_dev -p 5432
```

### 查看所有表
```bash
$env:PGPASSWORD = "easytest123"
& "D:\PostgreSQL\bin\psql.exe" -U easytest -d easytest_dev -p 5432 -c "\dt"
```

### 查看表结构
```bash
$env:PGPASSWORD = "easytest123"
& "D:\PostgreSQL\bin\psql.exe" -U easytest -d easytest_dev -p 5432 -c "\d users"
```

### 查询数据
```bash
$env:PGPASSWORD = "easytest123"
& "D:\PostgreSQL\bin\psql.exe" -U easytest -d easytest_dev -p 5432 -c "SELECT * FROM users;"
```

## 📝 配置文件

### backend/.env
```env
FLASK_ENV=development
FLASK_APP=wsgi.py
DATABASE_URL=postgresql://easytest:easytest123@localhost:5432/easytest_dev
SECRET_KEY=dev-secret-key-for-testing
JWT_SECRET_KEY=dev-jwt-secret-key-for-testing
REDIS_URL=redis://localhost:6379/0
```

### backend/app/config.py
```python
# 开发环境默认使用 PostgreSQL
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'postgresql://easytest:easytest123@localhost:5432/easytest_dev'
)
```

## 🎯 下一步

1. ✅ PostgreSQL 已安装并运行
2. ✅ 数据库和用户已创建
3. ✅ 数据表已初始化
4. ✅ 测试用户已创建
5. ✅ 后端服务已启动

现在可以启动前端并开始使用了！

## 💡 提示

- PostgreSQL 服务名: `postgresql-x64-18`
- 使用 `services.msc` 或 `Get-Service postgresql*` 查看服务状态
- 详细配置指南请查看: [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)
