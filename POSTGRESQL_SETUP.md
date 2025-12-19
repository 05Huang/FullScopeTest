# PostgreSQL 数据库设置指南

## 本地开发环境设置

### 方式一：使用 Docker (推荐)

1. **启动 PostgreSQL 容器**
```bash
docker-compose up -d postgres
```

2. **验证数据库连接**
```bash
docker exec -it easytest_postgres psql -U easytest -d easytest_dev
```

3. **初始化数据库**
```bash
cd backend
python init_db.py
```

### 方式二：本地安装 PostgreSQL

#### Windows 安装步骤

1. **下载并安装 PostgreSQL**
   - 访问 https://www.postgresql.org/download/windows/
   - 下载 PostgreSQL 15+ 安装程序
   - 安装时设置密码（记住此密码）

2. **创建数据库和用户**

打开 pgAdmin 或使用 psql 命令行：

```sql
-- 创建用户
CREATE USER easytest WITH PASSWORD 'easytest123';

-- 创建数据库
CREATE DATABASE easytest_dev OWNER easytest;

-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE easytest_dev TO easytest;
```

使用 psql 命令行：
```bash
# 连接到 PostgreSQL (以管理员身份)
psql -U postgres

# 然后执行上面的 SQL 命令
```

3. **配置环境变量**

确保 `backend/.env` 文件包含：
```
DATABASE_URL=postgresql://easytest:easytest123@localhost:5432/easytest_dev
```

4. **初始化数据库表结构**

```bash
cd backend

# 初始化数据库
python init_db.py

# 或者使用迁移
flask db upgrade
```

#### Linux/Mac 安装步骤

1. **安装 PostgreSQL**

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Mac (使用 Homebrew):
```bash
brew install postgresql@15
brew services start postgresql@15
```

2. **创建数据库和用户**

```bash
# 切换到 postgres 用户
sudo -u postgres psql

# 在 psql 中执行
CREATE USER easytest WITH PASSWORD 'easytest123';
CREATE DATABASE easytest_dev OWNER easytest;
GRANT ALL PRIVILEGES ON DATABASE easytest_dev TO easytest;
\q
```

3. **初始化数据库**

```bash
cd backend
python init_db.py
```

## 数据库管理命令

### 查看数据库状态

```bash
# Docker 环境
docker exec -it easytest_postgres psql -U easytest -d easytest_dev

# 本地环境
psql -U easytest -d easytest_dev
```

### 常用 psql 命令

```sql
-- 列出所有数据库
\l

-- 连接到数据库
\c easytest_dev

-- 列出所有表
\dt

-- 查看表结构
\d table_name

-- 退出
\q
```

### 数据库迁移

```bash
# 创建新迁移
flask db migrate -m "描述变更内容"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade

# 查看迁移历史
flask db history
```

## 数据库备份与恢复

### 备份数据库

```bash
# Docker 环境
docker exec easytest_postgres pg_dump -U easytest easytest_dev > backup.sql

# 本地环境
pg_dump -U easytest easytest_dev > backup.sql
```

### 恢复数据库

```bash
# Docker 环境
docker exec -i easytest_postgres psql -U easytest easytest_dev < backup.sql

# 本地环境
psql -U easytest easytest_dev < backup.sql
```

## 常见问题

### 1. 连接被拒绝

**问题**：`could not connect to server: Connection refused`

**解决方案**：
- 确认 PostgreSQL 服务正在运行
- 检查端口 5432 是否被占用
- 验证防火墙设置

Windows:
```bash
# 检查服务状态
services.msc  # 查找 postgresql-x64-15

# 或使用命令
Get-Service postgresql*
```

Linux:
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### 2. 认证失败

**问题**：`FATAL: password authentication failed`

**解决方案**：
- 检查 `.env` 文件中的用户名和密码
- 确认数据库用户已创建
- 重置用户密码：
```sql
ALTER USER easytest WITH PASSWORD 'easytest123';
```

### 3. 数据库不存在

**问题**：`FATAL: database "easytest_dev" does not exist`

**解决方案**：
```bash
# 创建数据库
createdb -U easytest easytest_dev

# 或使用 psql
psql -U postgres -c "CREATE DATABASE easytest_dev OWNER easytest;"
```

### 4. Docker 容器问题

**问题**：无法连接到 Docker 中的 PostgreSQL

**解决方案**：
```bash
# 检查容器状态
docker ps | grep postgres

# 查看容器日志
docker logs easytest_postgres

# 重启容器
docker-compose restart postgres

# 完全重建
docker-compose down
docker-compose up -d postgres
```

## 性能优化建议

### 1. 连接池配置

在 `config.py` 中添加：
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### 2. 索引优化

为常用查询字段添加索引：
```python
# 在模型中添加索引
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)  # 添加索引
    created_at = db.Column(db.DateTime, index=True)
```

### 3. 查询优化

使用 eager loading 避免 N+1 查询：
```python
# 使用 joinedload
from sqlalchemy.orm import joinedload

projects = Project.query.options(
    joinedload(Project.api_test_cases)
).all()
```

## 从 SQLite 迁移数据

如果您之前使用 SQLite 并需要迁移数据：

1. **导出 SQLite 数据**
```bash
python export_sqlite_data.py > data.json
```

2. **导入到 PostgreSQL**
```bash
python import_to_postgresql.py data.json
```

或使用第三方工具如 `pgloader`:
```bash
pgloader sqlite://easytest_dev.db postgresql://easytest:easytest123@localhost/easytest_dev
```

## 生产环境建议

1. **使用强密码**：更改默认密码
2. **启用 SSL**：配置 PostgreSQL SSL 连接
3. **定期备份**：设置自动备份任务
4. **监控性能**：使用 pg_stat_statements
5. **限制连接数**：配置 max_connections
6. **使用连接池**：如 PgBouncer

## 参考资源

- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [Flask-SQLAlchemy 文档](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
