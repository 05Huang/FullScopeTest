# 贡献指南

感谢您对 FullScopeTest 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

1. 在 [GitHub Issues](https://github.com/05Huang/FullScopeTest/issues) 中搜索是否已有相同问题
2. 如果没有，创建一个新的 Issue，包含：
   - 清晰的问题描述
   - 复现步骤（环境信息、操作步骤、预期行为、实际行为）
   - 相关日志或截图

### 建议新功能

1. 在 [GitHub Issues](https://github.com/05Huang/FullScopeTest/issues) 中创建 Feature Request
2. 说明使用场景和预期效果
3. 等待维护者确认后开始开发

### 提交代码

1. Fork 项目仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改（遵循下方提交规范）
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request，关联相关 Issue

## 开发环境设置

### 前置要求

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建 |
| Redis | 5.0+ | Celery 消息队列（必需） |

> 本地开发默认使用 SQLite，无需安装 PostgreSQL。

### 本地开发

```bash
# 克隆项目
git clone https://github.com/05Huang/FullScopeTest.git
cd FullScopeTest

# === 后端 ===
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-test.txt

# 准备配置
cp .env.example .env
# 编辑 .env，至少设置 SECRET_KEY 和 JWT_SECRET_KEY

# 初始化数据库并创建管理员
python init_db.py
python create_admin.py  # 默认账号: admin / admin123

# 启动后端（需先启动 Redis）
python app.py

# === 前端（新终端） ===
cd web
npm install
npm run dev  # http://localhost:3000
```

## 提交规范

项目使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范，通过 commitlint + husky 强制校验：

```
<type>(<scope>): <subject>
```

**类型：**
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档变更
- `style`: 代码格式（不影响运行）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建/工具变动
- `ci`: CI 配置变更

**示例：**
```
feat(api-test): 添加 cURL 导入功能
fix(auth): 修复 Token 刷新失败问题
docs: 更新 API 文档
```

## 代码规范

### Python

- 遵循 PEP 8
- 使用类型注解（Type Hints）
- 函数和类需有简要文档字符串

### TypeScript / React

- 启用严格模式 TypeScript（`noUnusedLocals`, `noUnusedParameters` 等）
- 使用 ESLint 检查：`cd web && npm run lint`
- 组件使用函数式组件 + Hooks
- 状态管理使用 Zustand，按模块拆分 Store

## 测试

### 后端测试

```bash
cd backend
pytest -q tests          # 运行全部测试
pytest -q tests/test_auth.py  # 运行单个文件
```

### 前端测试

```bash
cd web
npm run test             # 运行测试
```

提交代码前请确保所有测试通过。

## Pull Request 指南

1. 确保所有测试通过
2. 更新相关文档（如有必要）
3. 保持 PR 范围小而专注
4. 提供清晰的 PR 描述，说明改动内容和原因
5. 关联相关 Issue

## 行为准则

请参阅 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 问题？

如有疑问，请在 [GitHub Issues](https://github.com/05Huang/FullScopeTest/issues) 中提问。
