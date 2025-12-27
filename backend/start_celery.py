"""
Celery Worker 启动脚本

直接运行此脚本启动 Celery Worker
"""
import os

# ⚠️ 必须在任何其他导入之前进行 gevent monkey-patch
# 否则会导致 greenlet 无法正常执行
import gevent.monkey
gevent.monkey.patch_all()

# 确保加载 .env 文件
from dotenv import load_dotenv
load_dotenv()

# 确保 Celery 启用
os.environ.setdefault('CELERY_ENABLE', 'true')

from app.celery_app import make_celery
import app.tasks  # 导入任务模块


def _reset_stale_running_status():
    """Worker 启动前清理数据库中遗留的 running 状态，防止前端误判为仍在运行"""
    try:
        from app import create_app
        from app.extensions import db
        from app.models.perf_test_scenario import PerfTestScenario

        app = create_app()
        with app.app_context():
            updated = PerfTestScenario.query.filter_by(status='running').update(
                {
                    'status': 'failed',
                    'last_result': {
                        'success': False,
                        'error': 'worker restarted: marking stale running task as failed',
                    }
                },
                synchronize_session=False,
            )
            if updated:
                db.session.commit()
                print(f"[celery-start] 重置遗留运行中任务数: {updated}")
            else:
                db.session.rollback()
    except Exception as e:
        print(f"[celery-start] 重置运行中任务失败: {e}")


# 创建配置好的 Celery 实例
celery = make_celery()

# 在启动 worker 前执行清理，避免重启后状态残留
_reset_stale_running_status()

# 启动 worker
if __name__ == '__main__':
    celery.start(['worker', '--loglevel=info', '--pool=solo'])
