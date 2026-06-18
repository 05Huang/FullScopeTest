"""维护任务（清理、备份等）"""

from app.extensions import celery, db
from app.models.web_test_script import WebTestScript
from app.models.perf_test_scenario import PerfTestScenario
from app.core.logging import get_logger
from app.core.metrics import record_task_success, record_task_failure
from datetime import datetime

from .common import _get_flask_app

logger = get_logger(__name__)


@celery.task(
    name='tasks.cleanup_old_results',
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    autoretry_for=(IOError, OSError),
)
def cleanup_old_results_task():
    """
    清理旧的测试结果（定时任务）

    清理超过 30 天的测试结果
    """
    task_start_time = time.time()
    # 使用 Flask 应用上下文
    with _get_flask_app().app_context():
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=30)

            # 清理 Web 测试结果
            old_scripts = WebTestScript.query.filter(
                WebTestScript.last_run_at < cutoff_date
            ).all()

            for script in old_scripts:
                script.last_result = None

            # 清理性能测试结果
            old_scenarios = PerfTestScenario.query.filter(
                PerfTestScenario.last_run_at < cutoff_date
            ).all()

            for scenario in old_scenarios:
                scenario.last_result = None

            db.session.commit()

            record_task_success('cleanup_old_results', time.time() - task_start_time)
            return {
                'success': True,
                'cleaned_scripts': len(old_scripts),
                'cleaned_scenarios': len(old_scenarios)
            }

        except Exception as e:
            record_task_failure('cleanup_old_results', time.time() - task_start_time)
            return {
                'success': False,
                'error': str(e)
            }

