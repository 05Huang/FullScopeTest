"""APP 测试异步任务（Appium）"""

from app.extensions import celery, db
from app.core.logging import get_logger
from app.core.metrics import record_task_success, record_task_failure
import subprocess
import time
import os
from datetime import datetime, timezone

from app.utils.sandbox import execute_script
from .common import _get_flask_app

logger = get_logger(__name__)


@celery.task(
    bind=True,
    name='tasks.run_app_test',
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    autoretry_for=(IOError, OSError, TimeoutError),
)
def run_app_test_task(self, script_id, user_id):
    """异步执行 APP 测试脚本（Appium）"""
    task_start_time = time.time()
    with _get_flask_app().app_context():
        from app.models.app_test_script import AppTestScript

        script = None
        try:
            script = AppTestScript.query.filter_by(id=script_id, user_id=user_id).first()
            if not script:
                record_task_failure('run_app_test', time.time() - task_start_time)
                return {'success': False, 'error': 'Script not found'}

            script.status = 'running'
            script.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
            db.session.commit()

            self.update_state(state='PROGRESS', meta={'status': 'Running Appium test...'})

            # 准备工作目录
            work_dir = os.path.join(os.path.dirname(_get_flask_app().root_path), 'data', 'app_tests', str(script_id))
            os.makedirs(work_dir, exist_ok=True)

            # 通过沙箱执行脚本（AST 检查 + 子进程隔离 + 审计日志）
            sandbox_result = execute_script(
                script_content=script.script_content,
                user_id=user_id,
                timeout=300,  # 5 分钟超时
                work_dir=work_dir,
                script_id=script_id,
                script_type="app",
            )

            duration = sandbox_result['duration']
            success = sandbox_result['success']

            # 更新脚本状态
            script.status = 'passed' if success else 'failed'
            script.last_result = {
                'success': success,
                'duration': duration,
                'stdout': sandbox_result['stdout'],
                'stderr': sandbox_result['stderr'],
                'return_code': sandbox_result.get('return_code'),
                'error': sandbox_result.get('error'),
                'script_hash': sandbox_result.get('script_hash'),
                'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            }
            db.session.commit()

            if success:
                record_task_success('run_app_test', time.time() - task_start_time)
            else:
                record_task_failure('run_app_test', time.time() - task_start_time)

            return {
                'success': success,
                'script_id': script_id,
                'duration': duration,
                'stdout': sandbox_result['stdout'],
                'stderr': sandbox_result['stderr'],
                'return_code': sandbox_result.get('return_code'),
            }

        except subprocess.TimeoutExpired:
            # 安全网：sandbox 内部已处理超时，此处为防御性代码
            if script:
                script.status = 'failed'
                script.last_result = {
                    'success': False,
                    'error': 'Execution timeout (5 minutes)',
                    'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                }
                db.session.commit()
            record_task_failure('run_app_test', time.time() - task_start_time)
            return {'success': False, 'error': 'Execution timeout'}

        except Exception as e:
            if script:
                script.status = 'failed'
                script.last_result = {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                }
                db.session.commit()
            record_task_failure('run_app_test', time.time() - task_start_time)
            return {'success': False, 'error': str(e)}
