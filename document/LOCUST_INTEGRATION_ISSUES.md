# Locust 实时监控集成问题记录

## 问题概述

在实现 Locust 性能测试的实时监控功能时，遇到了 **Locust greenlets 在 Celery Worker 环境中无法正常执行 HTTP 请求** 的核心问题。

## 当前状态

### ✅ 已解决的问题

#### 1. Gevent Monkey-Patch 问题
**文件**: `backend/start_celery.py`

**问题**: MonkeyPatchWarning 警告，greenlet 无法正常执行
```
MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported
```

**解决方案**: 在所有导入之前进行 gevent monkey-patch
```python
import gevent.monkey
gevent.monkey.patch_all()
```

#### 2. Locust 2.x API 兼容性
**文件**: `backend/app/tasks.py`

**问题 1**: `cannot import name 'Environment' from 'locust'`
```python
# 错误
from locust import Environment

# 正确
from locust.env import Environment
```

**问题 2**: `LocalRunner.__init__() got an unexpected keyword argument 'user_count'`
```python
# 错误（Locust 1.x）
runner = LocalRunner(env, user_count=user_count, spawn_rate=spawn_rate)

# 正确（Locust 2.x）
runner = LocalRunner(env)
runner.start(user_count, spawn_rate)
```

#### 3. 后台线程阻塞问题
**文件**: `backend/app/tasks.py`

**问题**: `Event.wait()` 在 gevent 环境中可能导致冲突

**解决方案**: 改用 `time.sleep()`
```python
# 错误
stop_update.wait(2)

# 正确
time.sleep(2)
```

#### 4. HttpUser 类过滤问题
**文件**: `backend/app/tasks.py`

**问题**: 扫描时包含 `HttpUser` 基类，导致 "No tasks defined on HttpUser" 错误

**解决方案**: 排除基类
```python
from locust import HttpUser as LocustHttpUser

if (isinstance(attr, type) and
    issubclass(attr, locust_module.HttpUser) and
    attr is not locust_module.HttpUser and
    attr is not LocustHttpUser):
    user_classes.append(attr)
```

### ❌ 核心问题：Greenlets 不执行 HTTP 请求

#### 现象
- 代码正常执行到 `runner.start(user_count, spawn_rate)`
- 数据库每2秒正常更新（后台线程工作）
- 但 `request_count` 始终为 0
- 没有实际 HTTP 请求发出
- 事件监听器从未被触发
- 测试会运行完整的 `run_time` 时长，但没有实际请求

#### 日志示例
```
[DEBUG] 开始导入 Locust 脚本...
[DEBUG] Locust 脚本导入成功
[DEBUG] 找到 1 个 HttpUser 类
[任务启动] 已注册事件监听器，开始执行性能测试
[DEBUG] 正在创建 Locust Environment...
[DEBUG] 正在创建 LocalRunner...
[DEBUG] 正在启动 runner，参数: user_count=2, spawn_rate=1
[DEBUG] Locust runner 已启动，开始执行测试 10 秒
# ... 10秒后 ...
[DEBUG] 测试超时，停止 runner
[DEBUG] Runner 已停止
[任务完成] 测试已执行 10 秒
# 最终统计：request_count=0, failure_count=0
```

#### 可能的原因分析

**1. `runner.greenlet.join()` 在 Celery 上下文中不工作**
   - 在 gevent-monkey-patched 的 Celery Worker 中
   - `runner.greenlet.join()` 可能无法正确让出控制权
   - Locust 的用户 greenlets 得不到执行机会

**2. Celery 任务执行模型与 Gevent 冲突**
   - Celery 使用 solo pool（单进程）
   - 与 gevent 的协程模型可能存在冲突
   - 每个任务在独立的 greenlet 中运行
   - Locust 需要创建自己的 greenlet 层级

**3. 后台更新线程干扰**
   - 使用常规 `threading.Thread` 在 gevent 环境中
   - 可能导致调度问题
   - `time.sleep(2)` 可能在 gevent 环境下无法正确让出 CPU

## 可能的出错点位置

| 文件 | 行号 | 问题 | 影响 |
|------|------|------|------|
| `start_celery.py` | 10-11 | monkey-patch 时机 | 必须在所有导入之前，否则 greenlet 无法工作 |
| `tasks.py` | 242 | `time.sleep(2)` | gevent 环境下可能无法正确让出 |
| `tasks.py` | 270 | `threading.Thread` | 与 gevent greenlet 可能冲突 |
| `tasks.py` | 334 | `runner.start()` | 在 Celery 上下文中可能无法正确启动 greenlets |
| `tasks.py` | 345 | `runner.greenlet.join()` | **核心问题点**：在 Celery 上下文中可能阻塞，不执行实际请求 |

## ✅ 最终解决方案（已实现）

### 方案 1：子进程隔离 + CSV 实时监控（已采用）

**实现日期**: 2026-01-04

**核心思路**: 通过子进程运行 Locust，利用 CSV 输出实现实时监控，完全避免 greenlet 冲突。

**实现细节**:

```python
# 1. 启动 Locust 子进程
cmd = [
    sys.executable, '-m', 'locust',
    '-f', locustfile,
    '--host', scenario.target_url,
    '--users', str(user_count),
    '--spawn-rate', str(spawn_rate),
    '--run-time', f'{run_time}s',
    '--headless',
    '--csv', csv_prefix,           # 生成 rt_stats.csv 和 rt_stats_history.csv
    '--csv-full-history',          # 关键：启用实时历史记录
]

proc = subprocess.Popen(cmd, cwd=temp_dir, ...)

# 2. 监控线程：每 2 秒读取 CSV 并更新数据库
def monitor_realtime():
    while not stop_monitor.is_set():
        time.sleep(2)
        stats = _read_latest_stats(csv_prefix)  # 读取 rt_stats_history.csv 最新行
        # 更新数据库实时指标...

# 3. 等待进程完成
proc.wait(timeout=run_time + 30)

# 4. 解析最终结果
results = _parse_locust_results(csv_prefix)
```

**关键文件修改**:
- `backend/app/tasks.py:191-388` - 重写为子进程执行 + CSV 监控
- `backend/app/api/perf_test.py` - 添加实时状态接口，时间戳统一为 UTC ISO Z
- `web/src/pages/perf-test/PerfTestMonitor.tsx` - 2秒轮询，使用实时时间戳

**已修复问题**:
- ✅ Greenlet 不执行请求 - 改为子进程运行
- ✅ 实时曲线横轴固定步长 - 改用后端实时时间戳
- ✅ 报告/状态时间戳异常 - 统一输出 UTC ISO `...Z`
- ✅ 场景管理页顶部统计卡 - 已移除避免重复
- ✅ 监控进度条不动 - 根据 `started_at` 计算进度

**运行流程**:
```
Celery 任务启动
    ↓
创建临时目录 + locustfile
    ↓
启动监控线程（每 2 秒读取 CSV）
    ↓
启动 Locust 子进程（--csv-full-history）
    ↓
实时更新数据库 ←── 监控线程读取 CSV
    ↓
子进程结束
    ↓
解析最终 CSV 结果
    ↓
更新数据库状态为 completed
    ↓
清理临时目录
```

---

## 建议的解决方案

### 方案 1：使用进程隔离（推荐）

回退到 subprocess 方式执行 Locust，通过文件或 Redis 进行实时数据通信：

```python
# 伪代码
def run_perf_test_task(scenario_id, user_count, spawn_rate, run_time):
    # 1. 创建临时结果文件
    result_file = f"/tmp/locust_results_{scenario_id}.json"

    # 2. 启动 Locust subprocess
    proc = subprocess.Popen([
        'locust',
        '-f', locustfile,
        '--host', target_url,
        '--users', str(user_count),
        '--spawn-rate', str(spawn_rate),
        '--run-time', f'{run_time}s',
        '--headless',
        '--csv', result_prefix,
        '--html', html_file
    ])

    # 3. 同时启动监控线程，定期读取 CSV 结果并更新数据库
    monitor_thread = threading.Thread(
        target=monitor_csv_results,
        args=(result_prefix, scenario_id)
    )
    monitor_thread.start()

    # 4. 等待进程完成
    proc.wait()

    # 5. 解析最终结果
    results = parse_csv_results(result_prefix)
```

**优点**：
- 完全隔离，避免 greenlet 冲突
- Locust 按设计方式运行
- 稳定可靠

**缺点**：
- 实时性稍差（通过文件轮询）
- 需要清理临时文件

### 方案 2：放弃实时监控

先完成基本的性能测试功能：

```python
def run_perf_test_task(scenario_id, user_count, spawn_rate, run_time):
    # 执行测试
    proc = subprocess.Popen([...])
    proc.wait()

    # 测试完成后一次性解析结果
    results = parse_csv_results(result_prefix)

    # 更新数据库
    scenario.status = 'completed'
    scenario.last_result = results
    db.session.commit()
```

**优点**：
- 简单可靠
- 先完成核心功能

**缺点**：
- 无法实时查看进度
- 用户体验较差

### 方案 3：深入研究 Locust 内部实现

尝试使用显式的 greenlet 调度：

```python
# 可能需要深入研究 Locust 源码
# 找到正确的方法让 greenlets 在 Celery 上下文中执行

# 可能的方向：
# 1. 使用 gevent.spawn() 显式创建 greenlet
# 2. 修改 runner 的调度方式
# 3. 使用不同的执行模型
```

**优点**：
- 如果成功，可以实现真正的实时监控

**缺点**：
- 需要深入研究 Locust 内部实现
- 可能无法解决根本冲突
- 维护成本高

## 技术栈版本信息

- Python: 3.13
- Locust: 2.42.0
- Celery: 5.6.0
- Gevent: 最新版本
- Flask: 3.0

## 相关文件

- `backend/app/tasks.py` - Celery 任务定义
- `backend/start_celery.py` - Celery Worker 启动脚本
- `backend/app/__init__.py` - Flask 应用工厂
- `web/src/pages/perf-test/PerfTestMonitor.tsx` - 前端监控页面

## 总结

**问题**: Locust greenlets 在 Celery Worker (gevent-monkey-patched) 环境中无法正常执行 HTTP 请求。这是 gevent + Celery + Locust 三者组合的固有冲突。

**已采用方案**: 子进程隔离 + CSV 实时监控

- 通过 `subprocess.Popen()` 启动独立的 Locust 进程
- 使用 `--csv-full-history` 参数生成实时 CSV 文件
- 后台监控线程每 2 秒读取 `_stats_history.csv` 最新行
- 实时更新数据库，前端通过轮询获取最新指标

**优点**:
- ✅ 完全隔离 greenlet，避免调度冲突
- ✅ Locust 按设计方式运行，稳定可靠
- ✅ 近实时监控（2秒延迟）
- ✅ 最终结果完整保留

**相关文档**: [LOCUST_MONITORING_NOTES.md](LOCUST_MONITORING_NOTES.md) - 实时监控运行逻辑速览
