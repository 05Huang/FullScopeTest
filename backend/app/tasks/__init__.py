"""Celery 异步任务包"""

from .web_test import run_web_test_task, _process_visual_diffs
from .perf_test import run_perf_test_task, _parse_locust_results
from .app_test import run_app_test_task
from .maintenance import cleanup_old_results_task
from .common import _build_locust_command, _build_step_stages, _inject_step_load_shape

__all__ = [
    'run_web_test_task',
    'run_perf_test_task',
    'run_app_test_task',
    'cleanup_old_results_task',
    '_build_locust_command',
    '_build_step_stages',
    '_inject_step_load_shape',
    '_parse_locust_results',
    '_process_visual_diffs',
]
