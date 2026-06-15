# Flask → FastAPI 迁移路线图

> 本文档规划 v1 Flask API (/api/v1/) 向 v2 FastAPI (/api/v2/) 的渐进式迁移策略。

---

## 1. 背景与目标

**现状**：项目同时维护两套后端框架：

| 版本 | 框架 | 路由前缀 | 模块数 |
|------|------|----------|--------|
| v1 | Flask 3.0 + Blueprints | /api/v1/ | 25 个模块 |
| v2 | FastAPI + Routers | /api/v2/ | 6 个模块（已完成） |

**目标**：逐步将 v1 模块迁移到 v2，最终移除 Flask 依赖。  
**约束**：每个模块迁移后保持 v1 路由兼容（deprecated 标记），至少保留一个版本周期（约 4 周）。

---

## 2. 迁移优先级与顺序

迁移按 **业务依赖链** 和 **用户影响面** 排序：

### 阶段 A：基础层迁移（低风险，基础设施就绪）

| 顺序 | 模块 | v1 路由 | v2 状态 | 依赖 | 预估工作量 |
|------|------|---------|---------|------|------------|
| A1 | auth | /api/v1/auth/* | ✅ 已完成 (v2/auth.py) | — | 已完成 |
| A2 | tokens | /api/v1/tokens/* | ❌ 待迁移 | auth | 0.5 天 |
| A3 | projects | /api/v1/projects/* | ❌ 待迁移 | auth | 1 天 |
| A4 | environments | /api/v1/environments/* | ❌ 待迁移 | projects | 0.5 天 |
| A5 | organizations | /api/v1/organizations/* | ❌ 待迁移 | auth | 1 天 |

### 阶段 B：核心测试模块迁移（高价值，需充分测试）

| 顺序 | 模块 | v1 路由 | v2 状态 | 依赖 | 预估工作量 |
|------|------|---------|---------|------|------------|
| B1 | api_test | /api/v1/api-test/* | ✅ 已完成 (v2/api_tests.py) | projects, environments | 已完成 |
| B2 | web_test | /api/v1/web-test/* | ✅ 已完成 (v2/ui_tests.py) | projects | 已完成 |
| B3 | perf_test | /api/v1/perf-test/* | ✅ 已完成 (v2/perf_tests.py) | projects | 已完成 |
| B4 | app_test | /api/v1/app-test/* | ❌ 待迁移 | projects | 2 天 |
| B5 | test_cases | /api/v1/test-cases/* | ✅ 已完成 (v2/test_cases.py) | — | 已完成 |

### 阶段 C：报告与分析模块

| 顺序 | 模块 | v1 路由 | v2 状态 | 依赖 | 预估工作量 |
|------|------|---------|---------|------|------------|
| C1 | reports | /api/v1/reports/* | ❌ 待迁移 | api_test, perf_test | 2 天 |
| C2 | visual | /api/v1/visual/* | ❌ 待迁移 | web_test | 1 天 |
| C3 | quality_gates | /api/v1/quality-gates/* | ❌ 待迁移 | reports | 1 天 |

### 阶段 D：AI 与辅助功能模块

| 顺序 | 模块 | v1 路由 | v2 状态 | 依赖 | 预估工作量 |
|------|------|---------|---------|------|------------|
| D1 | ai_copilot | /api/v1/ai/* | ❌ 待迁移 | auth | 1 天 |
| D2 | prompt_versions | /api/v1/prompt-versions/* | ❌ 待迁移 | auth | 0.5 天 |
| D3 | ai_stats | /api/v1/ai-stats/* | ❌ 待迁移 | auth | 0.5 天 |
| D4 | semantic_dedup | /api/v1/semantic-dedup/* | ❌ 待迁移 | ai_copilot | 0.5 天 |

### 阶段 E：自动化与集成功能模块

| 顺序 | 模块 | v1 路由 | v2 状态 | 依赖 | 预估工作量 |
|------|------|---------|---------|------|------------|
| E1 | triggers | /api/v1/triggers/* | ❌ 待迁移 | auth | 1 天 |
| E2 | alert_rules | /api/v1/perf-test/alert-rules/* | ❌ 待迁移 | perf_test | 0.5 天 |
| E3 | swagger_gen | /api/v1/swagger/* | ❌ 待迁移 | api_test | 0.5 天 |
| E4 | github_integration | /api/v1/integrations/github/* | ❌ 待迁移 | auth | 1 天 |
| E5 | github_checks | /api/v1/github-checks/* | ❌ 待迁移 | github_integration | 0.5 天 |
| E6 | docs | /api/v1/docs/* | ❌ 待迁移 | auth | 0.5 天 |

### 阶段 F：跨模块与通用功能

| 顺序 | 模块 | v1 路由 | v2 状态 | 依赖 | 预估工作量 |
|------|------|---------|---------|------|------------|
| F1 | global_search | /api/v1/search/* | ❌ 待迁移 | 全部模块 | 1 天 |
| F2 | audit_logs | 已有 Service | ❌ 待暴露 API | auth | 0.5 天 |
| F3 | webhooks/gitlab | /api/v1/webhooks/gitlab/* | ❌ 待迁移 | triggers | 0.5 天 |

---

## 3. 迁移工作模板

每个模块迁移遵循以下步骤：

### 3.1 创建 v2 Router 文件

`
backend/app/api/v2/{module}.py
`

- 使用 FastAPI APIRouter
- 定义 Pydantic 请求/响应模型（替代手动 equest.get_json()）
- 使用 Depends() 注入认证（复用 v2/auth.py 的 JWT 依赖）
- 复用现有 Service 层（pp/services/），不重写业务逻辑

### 3.2 注册路由

在 ackend/app/fastapi_app.py 的 egister_v2_routes() 中添加：

`python
from .api.v2.{module} import router as {module}_router
app.include_router({module}_router, prefix="/api/v2/{module}")
`

### 3.3 v1 路由标记 deprecated

在 v1 路由的响应头中添加 Deprecation 头：

`python
@app.after_request
def _add_deprecation_header(response):
    if request.path.startswith('/api/v1/'):
        response.headers['Deprecation'] = 'true'
        response.headers['Sunset'] = '2026-10-01'
    return response
`

### 3.4 测试

- 为 v2 Router 编写 pytest 测试（使用 TestClient）
- 确保 v1 和 v2 测试均通过
- E2E 测试覆盖关键路径

---

## 4. 关键技术决策

### 4.1 数据库访问

**当前**：Flask-SQLAlchemy (db.session, Model.query)  
**目标**：直接使用 SQLAlchemy AsyncSession（通过 database.py 共享引擎）  
**过渡方案**：FlaskContextMiddleware 保持 Flask-SQLAlchemy 模型在 FastAPI 中可用

### 4.2 认证

**当前**：Flask-JWT-Extended (@jwt_required())  
**目标**：FastAPI Depends() + PyJWT（已在 v2/auth.py 实现）  
**过渡方案**：v2 使用独立的 JWT 解析，不依赖 Flask-JWT-Extended

### 4.3 错误处理

**当前**：Flask @app.errorhandler + error_response()  
**目标**：FastAPI exception_handler + 统一 JSON 响应格式（已在 v2 实现）  
**要求**：v1 和 v2 响应格式完全一致（{code, data, message, timestamp}）

### 4.4 中间件

| 功能 | Flask 实现 | FastAPI 实现 |
|------|------------|--------------|
| CORS | lask-cors | CORSMiddleware |
| 限流 | lask-limiter + 自定义 | 需迁移为 ASGI 中间件 |
| 安全头 | security_headers.py | 需迁移为 ASGI 中间件 |
| 租户 | 	enant.py | 需迁移为 ASGI 中间件 |
| 结构化日志 | structlog | 通用，无需迁移 |
| Prometheus | prometheus-flask-instrumentator | prometheus-fastapi-instrumentator |

### 4.5 Celery 集成

Celery 任务与框架无关，无需迁移。Task 函数直接调用 Service 层。

---

## 5. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| v1/v2 行为不一致 | 用户困惑 | 统一 Service 层，仅路由层不同 |
| 数据库连接池冲突 | 连接泄漏 | 共享引擎实例（database.py） |
| 中间件执行顺序差异 | 安全/限流漏洞 | 集成测试覆盖关键路径 |
| Flask app context 依赖 | 模型查询失败 | FlaskContextMiddleware 过渡 |
| 回滚成本高 | 业务中断 | 保持 v1 路由可用，渐进切换 |

---

## 6. 时间线预估

| 阶段 | 模块数 | 预估工作量 | 目标完成 |
|------|--------|------------|----------|
| A 基础层 | 5 (2 已完成) | 3 天 | 第 1 周 |
| B 核心测试 | 5 (4 已完成) | 2 天 | 第 1-2 周 |
| C 报告分析 | 3 | 4 天 | 第 2-3 周 |
| D AI 辅助 | 4 | 2.5 天 | 第 3 周 |
| E 自动化集成 | 6 | 4 天 | 第 3-4 周 |
| F 跨模块通用 | 3 | 2 天 | 第 4 周 |
| **总计** | **25 (6 已完成)** | **~17.5 天** | **4 周** |

> 注：6 个模块已完成迁移（auth, test_cases, api_tests, ui_tests, perf_tests, openapi_docs），
> 剩余 19 个模块预估 17.5 个工作日。

---

## 7. 验收标准

每个模块迁移完成的验收标准：

- [ ] v2 Router 编写完成，包含完整的 Pydantic 模型定义
- [ ] v2 路由注册到 astapi_app.py
- [ ] v2 单元测试通过（≥5 个测试用例/模块）
- [ ] v1 路由标记 Deprecation 头
- [ ] v1 和 v2 对同一请求返回相同结构的响应
- [ ] OpenAPI 文档自动生成且描述完整
- [ ] 无回归：现有 v1 测试全部通过

---

## 附录：v2 已有模块清单

| 文件 | 模块 | 状态 |
|------|------|------|
| pi/v2/auth.py | 认证 | ✅ |
| pi/v2/test_cases.py | 测试用例 | ✅ |
| pi/v2/api_tests.py | 接口测试 | ✅ |
| pi/v2/ui_tests.py | Web 测试 | ✅ |
| pi/v2/perf_tests.py | 性能测试 | ✅ |
| pi/v2/openapi_docs.py | OpenAPI 文档 | ✅ |
