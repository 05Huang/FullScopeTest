# Celery 异步任务集成指南

## 概述

已将项目的异步任务从 Python Threading 迁移到 Celery + Redis，实现更加健壮和可扩展的异步任务处理。

## 架构变更

### 之前（Threading）
- ✗ 使用 `threading.Thread` 执行后台任务
- ✗ 进程重启后丢失任务状态
- ✗ 无法分布式部署
- ✗ 缺少任务监控和重试机制

### 现在（Celery）
- ✓ 使用 Celery 分布式任务队列
- ✓ Redis 作为消息代理和结果存储
- ✓ 任务持久化，进程重启不丢失
- ✓ 支持分布式 Worker
- ✓ 内置任务监控、重试和超时控制

## 新增文件

### 1. 配置文件
- `app/celery_app.py` - Celery 应用初始化和配置
- `app/tasks.py` - 异步任务定义

### 2. 启动脚本
- `celery_worker.py` - Celery Worker 启动脚本
- `run_celery.bat` - Windows 启动脚本

## 配置说明

### Redis 配置
在 `app/config.py` 中配置 Redis 连接：

```python
# Celery 配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

环境变量配置（可选）：
```bash
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## 使用方法

### 1. 启动 Redis
```bash
# Windows
# 下载并启动 Redis for Windows

# Linux/Mac
redis-server
```

### 2. 启动 Celery Worker

**Windows:**
```bash
cd backend
run_celery.bat
```

**Linux/Mac:**
```bash
cd backend
celery -A app.extensions:celery worker --loglevel=info
```

### 3. 启动 Flask 应用
```bash
cd backend
python app.py
```

## 任务说明

### Web 测试任务
```python
@celery.task(name='tasks.run_web_test')
def run_web_test_task(script_id, user_id):
    """异步执行 Web 测试脚本"""
```

**API 变化：**
- 提交任务：`POST /api/v1/web-test/scripts/{id}/run`
- 查询状态：`GET /api/v1/web-test/scripts/{id}/status`
- 停止任务：`POST /api/v1/web-test/scripts/{id}/stop`

### 性能测试任务
```python
@celery.task(name='tasks.run_perf_test')
def run_perf_test_task(scenario_id, user_count, spawn_rate, run_time):
    """异步执行性能测试"""
```

**API 变化：**
- 提交任务：`POST /api/v1/perf-test/scenarios/{id}/run`
- 查询状态：`GET /api/v1/perf-test/scenarios/{id}/status`
- 停止任务：`POST /api/v1/perf-test/scenarios/{id}/stop`

### 清理任务（定时任务）
```python
@celery.task(name='tasks.cleanup_old_results')
def cleanup_old_results_task():
    """清理 30 天前的测试结果"""
```

## 监控和管理

### Flower - Celery 监控工具
安装：
```bash
pip install flower
```

启动：
```bash
celery -A app.extensions:celery flower --port=5555
```

访问：http://localhost:5555

### 常用命令

查看活动任务：
```bash
celery -A app.extensions:celery inspect active
```

查看已注册任务：
```bash
celery -A app.extensions:celery inspect registered
```

撤销任务：
```bash
celery -A app.extensions:celery control revoke <task_id> --terminate
```

## 定时任务配置

使用 Celery Beat 实现定时任务：

```python
# app/celery_app.py
celery.conf.beat_schedule = {
    'cleanup-old-results': {
        'task': 'tasks.cleanup_old_results',
        'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点
    },
}
```

启动 Beat：
```bash
celery -A app.extensions:celery beat --loglevel=info
```

## 故障排查

### 1. Redis 连接失败
**错误：** `redis.exceptions.ConnectionError: Error connecting to Redis`

**解决：**
- 确认 Redis 已启动
- 检查 Redis 连接配置
- 测试连接：`redis-cli ping`

### 2. 任务未执行
**检查：**
- Celery Worker 是否运行
- 任务是否正确注册
- 查看 Worker 日志

### 3. Windows 兼容性
**注意：** Windows 下必须使用 `--pool=solo` 参数
```bash
celery -A app.extensions:celery worker --pool=solo
```

## 性能优化

### Worker 并发
```bash
# 多进程模式（Linux/Mac）
celery -A app.extensions:celery worker --concurrency=4

# 协程模式
celery -A app.extensions:celery worker --pool=gevent --concurrency=100
```

### 任务优先级
```python
task.apply_async(args=[...], priority=10)  # 0-9，数字越大优先级越高
```

### 任务重试
```python
@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def my_task(self):
    try:
        # 任务逻辑
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
```

## 部署建议

### 生产环境
1. 使用 supervisord 或 systemd 管理 Worker 进程
2. 配置多个 Worker 实现负载均衡
3. 使用 Redis Sentinel 或 Cluster 提高可用性
4. 启用 Flower 监控任务执行
5. 定期清理过期结果

### Docker 部署
参考 `docker-compose.yml` 配置 Redis 和 Celery Worker 服务。

## 相关资源

- [Celery 官方文档](https://docs.celeryq.dev/)
- [Redis 官方文档](https://redis.io/docs/)
- [Flower 文档](https://flower.readthedocs.io/)
