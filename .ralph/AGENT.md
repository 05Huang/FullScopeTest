# AGENT.md — FullScopeTest Build & Test Commands
# Ralph 在每次循环中参考此文件执行构建和测试

## 环境检查

```bash
# 检查 Python 版本（需要 3.10+）
python3 --version

# 检查 Node 版本（需要 18+）
node --version

# 检查 Docker
docker --version
docker compose version
```

## 后端（Backend）

### 安装依赖
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果存在
```

### 运行后端测试
```bash
cd backend
pytest tests/ -x -q --tb=short
# -x: 第一个失败就停止
# -q: 简洁输出
# --tb=short: 简短的错误追踪
```

### 运行特定测试
```bash
cd backend
pytest tests/test_auth.py -v
pytest tests/ -k "test_api" -v
```

### 代码质量检查
```bash
cd backend
# 安装 ruff（如果没有）
pip install ruff --break-system-packages 2>/dev/null || pip install ruff

# 检查代码质量
ruff check app/ --select E,W,F --exit-zero

# 格式化（不强制要求，但推荐）
ruff format app/ --check
```

### 数据库迁移
```bash
cd backend
# 生成新迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

### 启动后端开发服务器
```bash
cd backend
# Flask 模式
flask run --port 5000

# 或 FastAPI 模式（迁移后）
uvicorn app.fastapi_app:app --reload --port 8000
```

## 前端（Frontend）

### 安装依赖
```bash
cd frontend
npm install
```

### 类型检查
```bash
cd frontend
npx tsc --noEmit
```

### 运行前端测试
```bash
cd frontend
npm test -- --passWithNoTests --watchAll=false
# 或
npx vitest run
```

### 构建
```bash
cd frontend
npm run build
```

### 启动开发服务器
```bash
cd frontend
npm run dev
```

## Docker

### 启动完整开发环境
```bash
docker compose up -d
docker compose logs -f
```

### 重建特定服务
```bash
docker compose build backend
docker compose up -d backend
```

### 停止并清理
```bash
docker compose down
docker compose down -v  # 同时删除 volumes
```

## Git 工作流

### 提交格式
```bash
git add -A
git commit -m "type(scope): description"
# type: feat | fix | refactor | test | docs | chore
# scope: backend | frontend | infra | ci | docs
# 示例：
# git commit -m "feat(backend): add visual regression test models"
# git commit -m "fix(frontend): correct port in docker-compose"
# git commit -m "test(backend): add scheduler lock tests"
```

### 推荐的提交类型
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 重构（不改变功能）
- `test`: 添加或修改测试
- `docs`: 文档更新
- `chore`: 构建配置、依赖更新

## 验收标准（每次提交前检查）

```bash
# 1. 后端测试必须通过
cd backend && pytest tests/ -x -q --tb=short
echo "Backend tests: $?"

# 2. 前端类型检查（如果修改了前端代码）
cd frontend && npx tsc --noEmit
echo "TypeScript check: $?"

# 3. 没有遗留的 TODO/FIXME（新增代码中）
git diff HEAD~1 | grep -E "^\+.*TODO|^\+.*FIXME|^\+.*HACK" | grep -v "test" || echo "No new TODOs"
```

## 常见问题

### 数据库连接失败
```bash
# 检查 PostgreSQL 是否运行
docker compose ps db
# 或
pg_isready -h localhost -p 5432
```

### Redis 连接失败
```bash
# 检查 Redis 是否运行
docker compose ps redis
# 或
redis-cli ping
```

### 端口占用
```bash
# 检查 5000 端口
lsof -i :5000
# 检查 3000/5173 端口（前端）
lsof -i :5173
```

### 依赖冲突
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

## 新增依赖时

```bash
# 后端
cd backend
pip install new-package
pip freeze > requirements.txt  # 更新依赖文件

# 或者手动编辑 requirements.txt 添加 new-package==x.y.z
# 然后 pip install -r requirements.txt

# 前端
cd frontend
npm install new-package
# package.json 会自动更新
```
