# Locust 实时监控与修复记录

## 当前方案概览
- 执行方式：Celery 任务内以子进程运行 Locust，开启 `--csv-full-history`，避免 Celery/gevent 冲突并产出实时 CSV。
- 实时写库：后台监控线程每 2 秒读取 `_stats_history.csv`，回填场景的 `avg/min/max/throughput/error_rate`，并写入 `last_result.realtime = { timestamp: <UTC ISO Z>, stats: {...} }`。
- 对外接口：
  - `/perf-test/running`：列出运行中的场景，附 `started_at`（UTC Z）。
  - `/perf-test/scenarios/:id/status`：返回实时字段和 `last_result.realtime`。
- 前端轮询：`PerfTestMonitor` 每 2 秒调用上述接口，无需手动刷新；横轴使用实时时间戳（不再固定 5s 步长）。

## 已修复问题
- Greenlet 不执行请求：改为子进程运行 Locust，规避 Celery/greenlet 调度冲突。
- 实时曲线横轴固定步长：改用后端实时时间戳生成标签。
- 报告/状态时间戳异常：统一输出 UTC ISO `...Z`，前端按本地时区展示。
- 场景管理页顶部实时统计卡片：已移除，避免与实时面板重复且数据不更新。
- 监控进度条不动：根据 `started_at` 与 `duration` 计算 `elapsed`，进度随时间推进。

## 运行逻辑速览
1) Celery 任务启动子进程 `python -m locust ... --csv <tmp>/rt --csv-full-history --headless --run-time {run_time}s`。
2) 监控线程每 2 秒读取 `<tmp>/rt_stats_history.csv` 最新行，更新数据库实时指标。
3) `/status` 接口直接返回数据库实时字段，前端 2 秒轮询渲染曲线；无需手动刷新。
4) 任务结束解析 `<tmp>/rt_stats.csv` 汇总写入 `last_result.results`，并清理临时目录。

## 验证建议
- 重启 Celery worker 后启动性能场景，打开实时监控页，检查 Network 中 `/status` 返回的 `last_result.realtime.stats` 是否更新。
- 若实时为空：确认 `_stats_history.csv` 是否生成（临时目录），并检查 worker 是否使用最新启动参数。

## 相关文件
- 后端：`backend/app/tasks.py`（子进程执行 + CSV 轮询）、`backend/app/api/perf_test.py`（状态接口时间戳）。
- 前端：`web/src/pages/perf-test/PerfTestMonitor.tsx`（时间轴与进度）、`web/src/pages/perf-test/PerfTestScenarios.tsx`（移除顶部统计卡）。