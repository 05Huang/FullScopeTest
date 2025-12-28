# EasyTest 代码质量问题与解决方案汇总

## 主要问题概览
- 任意代码执行风险：Web 脚本直接写入临时文件后由 Celery 以同一解释器执行，无沙箱/资源隔离，超时可被用户配置，攻击面与 Celery Worker 权限共享。（backend/app/tasks.py）
- 性能/安全输入缺失：性能测试 run/quick-test 接口缺少并发/时长/目标主机上限，易触发高并发压测或对内网 SSRF。（backend/app/api/perf_test.py）
- 异常与事务处理不足：多处 DB 写入缺少 try/except+rollback，异常仅返回字符串，未记录日志，可能留脏 session。（如 backend/app/api/auth.py、perf_test.py、tasks.py）
- CORS 过于宽松：`/api/*` 全开放 origins，结合长时效 JWT，存在被第三方页面滥用风险。（backend/app/__init__.py）
- 测试缺失：后端关键路径与前端核心逻辑缺少自动化测试覆盖。

前端重点风险/改进点：
- Token 刷新并发竞争：401 时无刷新锁，可能重复刷新或状态覆盖。（web/src/services/api.ts）
- 压测监控轮询过频且串行：多场景时会堆积请求，缺少数据校验。（web/src/pages/perf-test/PerfTestMonitor.tsx）
- 表单校验不足：性能场景创建/更新缺少并发/时长上限校验，headers/body 仅做 JSON.parse。（web/src/pages/perf-test/PerfTestScenarios.tsx）

## 分阶段解决方案（循序渐进，复用现有结构）

### 阶段 1：最小侵入兜底
- 输入校验与上限：扩展现有 validators，为压测/脚本接口增加 user_count/spawn_rate/run_time/target_host 范围与白名单校验；前端表单同步校验。
- 并发/队列控制：在 Celery 调用前做 per-user/per-scenario 并发限制与队列长度检查，复用现有任务签名，不改业务层。
- 统一异常处理：通过 Flask errorhandler 统一捕获异常，记录结构化日志并 rollback DB session，保证状态一致。
- CORS/Token：将 CORS origins 配置化为白名单，缩短 Access Token 过期并保留刷新。
- 前端刷新锁：在 axios 拦截器加单例刷新 Promise，避免并发 401 多次刷新。
- 轮询优化：列表与详情分开轮询，间隔放宽（如列表 5s，详情 3-5s），使用并发限制/防抖。

### 阶段 2：执行隔离与安全加固
- 受限执行器：为 Web/性能脚本引入受限执行（容器或低权限用户），固定 CPU/内存/时长上限；对脚本做模板白名单或禁用高危模块。
- 网络白名单：性能/quick-test 目标主机启用域名白名单，防 SSRF。
- 审计日志：提交人与目标、参数、结果入库或日志，便于追踪滥用。
- 配置化：在 config 中增加脚本/压测上限，任务读取配置生效，用户参数超出即裁剪。

### 阶段 3：自动化验证与可观测
- 后端集成测试：用 pytest/Flask test client 覆盖认证、压测参数校验、超时/失败路径、队列并发限制。
- 前端单测/集成：用 Vitest/RTL 覆盖 axios 刷新锁、表单校验、轮询逻辑。
- 监控/告警：为 Celery 任务和压测提交添加基础指标/日志，配置开关控制。

## 预期承载能力（当前架构下的估算）
- 单机 4C8G，Redis/Postgres 同机，Gunicorn/Celery 默认并发约 4：适合 20–40 个同时浏览/轻量操作用户；同时发起测试任务的活跃用户建议控制在 5–10 人。
- 瓶颈：Locust/Playwright 执行与 API 同机竞争 CPU/网络，Celery 并发低、队列易堆积，数据库与 Redis 为单点。
- 提升路径：独立部署 Worker，提升 Celery 并发；性能/脚本执行迁移到专用节点或容器；Nginx+Gunicorn 增加 worker；PostgreSQL/Redis 独立实例；对性能测试设并发/时长上限和排队限流。

## 优先落地顺序建议
1. 阶段 1 全量落地：输入上限+白名单、异常处理/rollback、CORS 白名单、前端刷新锁与表单/轮询优化。
2. 阶段 2 并行推进受限执行/白名单/审计，上线后再调优限额。
3. 阶段 3 补自动化测试与监控，形成回归保障。
