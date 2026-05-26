# 贡献指南

感谢您对 FullScopeTest 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

1. 在 [GitHub Issues](https://github.com/your-username/fullscopetest/issues) 中搜索是否已有相同问题
2. 如果没有，创建一个新的 Issue
3. 使用 Bug 报告模板，提供详细的复现步骤

### 建议新功能

1. 在 [GitHub Discussions](https://github.com/your-username/fullscopetest/discussions) 中分享您的想法
2. 获得社区认可后，创建 Feature Request Issue
3. 等待维护者确认后开始开发

### 提交代码

1. Fork 项目仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发环境设置

### 前置要求

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+ (或 SQLite 用于开发)
- Redis (可选，用于 Celery)

### 本地开发

```bash
# 克隆项目
git clone https://github.com/your-username/fullscopetest.git
cd fullscopetest

# 后端设置
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-test.txt
python init_db.py

# 前端设置
cd ../web
npm install

# 启动开发服务器
npm run dev  # 前端 (http://localhost:3000)
python app.py  # 后端 (http://localhost:5211)
```

## 代码规范

### 提交信息格式

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

类型包括：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档变更
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建过程或辅助工具变动
- `ci`: CI 配置变更

### Python 代码规范

- 遵循 PEP 8
- 使用 Black 格式化代码
- 使用 isort 排序导入
- 编写文档字符串

### TypeScript/React 代码规范

- 使用 ESLint + Prettier
- 遵循 React Hooks 规则
- 使用 TypeScript 严格模式
- 组件使用函数式组件 + Hooks

## 测试

### 后端测试

```bash
cd backend
pytest -q tests
pytest --cov=app tests  # 带覆盖率
```

### 前端测试

```bash
cd web
npm run test
npm run test:coverage
```

## Pull Request 指南

1. 确保所有测试通过
2. 更新相关文档
3. 保持 PR 范围小而专注
4. 提供清晰的 PR 描述
5. 关联相关 Issue

## 行为准则

请参阅 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 问题？

如有任何问题，请在 [GitHub Discussions](https://github.com/your-username/fullscopetest/discussions) 中提问。
