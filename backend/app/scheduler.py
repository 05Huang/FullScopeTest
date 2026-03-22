"""
定时任务调度器

使用 Flask-APScheduler 管理定时任务
"""

import os
import sys

# Windows 平台不支持 fcntl，需要特殊处理
try:
    import fcntl
except ImportError:
    fcntl = None

from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
import logging
import atexit

scheduler = APScheduler()
logger = logging.getLogger(__name__)

# 全局文件锁句柄
_scheduler_lock = None

def init_scheduler(app):
    """初始化调度器 (带有防多进程重复启动机制)"""
    global _scheduler_lock
    
    # 使用文件锁确保在 Gunicorn 多进程下只有一个进程启动调度器
    lock_file = os.path.join(app.root_path, '..', 'scheduler.lock')
    
    try:
        if sys.platform == 'win32' or not fcntl:
            # Windows 下多进程调度问题不明显（通常不用 Gunicorn），直接启动
            scheduler.init_app(app)
            scheduler.start()
        else:
            _scheduler_lock = open(lock_file, 'w')
            # 尝试获取排他非阻塞锁
            fcntl.flock(_scheduler_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # 拿到锁，可以启动调度器
            scheduler.init_app(app)
            scheduler.start()
            logger.info("获取调度器锁成功，已启动 APScheduler")
            
            # 注册退出时释放锁
            def release_lock():
                try:
                    fcntl.flock(_scheduler_lock, fcntl.LOCK_UN)
                    _scheduler_lock.close()
                    if os.path.exists(lock_file):
                        os.remove(lock_file)
                except Exception:
                    pass
            atexit.register(release_lock)
        
        # 启动时加载数据库中所有激活的任务
        with app.app_context():
            from .models.scheduled_task import ScheduledTask
            # 检查表是否存在，防止在测试环境或初始化时报错
            from sqlalchemy import inspect
            from .extensions import db
            inspector = inspect(db.engine)
            if inspector.has_table("scheduled_tasks"):
                active_tasks = ScheduledTask.query.filter_by(is_active=True).all()
                for task in active_tasks:
                    add_or_update_job(task)
            else:
                logger.warning("scheduled_tasks 表不存在，跳过加载定时任务")
                
    except IOError:
        # 获取锁失败，说明其他进程已经启动了调度器
        logger.info("调度器已在其他进程中启动，当前进程跳过初始化")
        # 将 scheduler 对象置于静默状态，提供空实现以防调用报错
        _patch_dummy_scheduler(scheduler)

def _patch_dummy_scheduler(sched):
    """提供空实现，防止其他没有拿到锁的进程调用 scheduler.add_job 时报错"""
    sched.get_job = lambda *args, **kwargs: None
    sched.add_job = lambda *args, **kwargs: None
    sched.modify_job = lambda *args, **kwargs: None
    sched.remove_job = lambda *args, **kwargs: None

            
def get_job_id(task_id):
    return f"scheduled_task_{task_id}"

def add_or_update_job(task):
    """添加或更新任务到调度器"""
    job_id = get_job_id(task.id)
    
    # 解析 cron 表达式 (支持常见的 5 位或 6 位 cron，这里使用 5 位：分 时 日 月 周)
    # APScheduler 的 CronTrigger 可以通过 from_crontab 方便地解析
    try:
        trigger = CronTrigger.from_crontab(task.cron_expression)
        
        if scheduler.get_job(job_id):
            scheduler.modify_job(job_id, trigger=trigger)
        else:
            scheduler.add_job(
                id=job_id,
                func=execute_scheduled_task,
                args=[task.id],
                trigger=trigger,
                replace_existing=True
            )
        logger.info(f"成功加载定时任务: {job_id} - {task.name}")
    except Exception as e:
        logger.error(f"加载定时任务失败 {job_id}: {str(e)}")

def remove_job(task_id):
    """从调度器移除任务"""
    job_id = get_job_id(task_id)
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"已移除定时任务: {job_id}")

def execute_scheduled_task(task_id):
    """执行定时任务"""
    # 由于是在后台线程执行，需要应用上下文
    app = scheduler.app
    with app.app_context():
        from .models.scheduled_task import ScheduledTask
        from .tasks import run_api_collection_task, run_web_collection_task, run_perf_scenario_task
        
        task = ScheduledTask.query.get(task_id)
        if not task or not task.is_active:
            return
            
        logger.info(f"开始执行定时任务: {task.name} (ID: {task.id})")
        
        try:
            celery_task = None
            if task.target_type == 'api_collection':
                celery_task = run_api_collection_task.delay(task.target_id, None)
            elif task.target_type == 'web_collection':
                celery_task = run_web_collection_task.delay(task.target_id, None)
            elif task.target_type == 'perf_scenario':
                celery_task = run_perf_scenario_task.delay(task.target_id)
            else:
                logger.error(f"未知的任务目标类型: {task.target_type}")
                return
                
            # 发送通知
            send_notification(task, "started", celery_task.id if celery_task else None)
        except Exception as e:
            logger.error(f"定时任务执行失败: {str(e)}")
            send_notification(task, "failed", error=str(e))

def send_notification(task, status, task_id=None, error=None):
    """发送 Webhook 通知 (如钉钉/飞书)"""
    if not task.notify_webhook:
        return
        
    # 判断是否需要通知
    if task.notify_events != 'all' and status != task.notify_events:
        return
        
    try:
        # 构建通知内容
        title = f"定时任务: {task.name} 执行状态 - {status}"
        content = f"**任务名称:** {task.name}\n**目标类型:** {task.target_type}\n**目标ID:** {task.target_id}\n**状态:** {status}"
        if task_id:
            content += f"\n**任务ID:** {task_id}"
        if error:
            content += f"\n**错误信息:** {error}"
            
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(task.notify_webhook, json=payload, headers=headers, timeout=5)
        logger.info(f"通知发送结果: {response.status_code}")
    except Exception as e:
        logger.error(f"发送通知失败: {str(e)}")
