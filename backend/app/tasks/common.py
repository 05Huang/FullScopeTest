"""共享工具函数"""

import subprocess
import tempfile
import sys
import time
import os
import json
import threading
import queue
from datetime import datetime
from typing import Optional, Dict, Any, List


_flask_app_cache = None


def _get_flask_app():
    """延迟获取 Flask 应用实例，避免循环导入（缓存复用）"""
    global _flask_app_cache
    if _flask_app_cache is None:
        from app import create_app
        _flask_app_cache = create_app()
    return _flask_app_cache


class RealtimeStatsCollector:
    """实时统计数据收集器"""

    def __init__(self):
        self.request_count = 0
        self.failure_count = 0
        self.response_times = []
        self.lock = threading.Lock()
        self.last_update = time.time()

    def record_request(self, response_time, success=True):
        """记录请求数据"""
        with self.lock:
            self.request_count += 1
            if not success:
                self.failure_count += 1
            self.response_times.append(response_time)
            self.last_update = time.time()

    def get_stats(self):
        """获取当前统计数据"""
        with self.lock:
            if self.request_count == 0:
                return {
                    'request_count': 0,
                    'failure_count': 0,
                    'error_rate': 0,
                    'avg_response_time': 0,
                    'min_response_time': 0,
                    'max_response_time': 0,
                    'throughput': 0
                }

            avg_response_time = sum(self.response_times) / len(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
            error_rate = (self.failure_count / self.request_count) * 100

            # 计算吞吐量（请求/秒）
            elapsed = time.time() - self.last_update
            throughput = self.request_count / elapsed if elapsed > 0 else 0

            return {
                'request_count': self.request_count,
                'failure_count': self.failure_count,
                'error_rate': error_rate,
                'avg_response_time': avg_response_time,
                'min_response_time': min_response_time,
                'max_response_time': max_response_time,
                'throughput': throughput
            }


def _build_step_stages(user_count, step_users, step_duration, run_time):
    """Build staged load plan where step_users means incremental users per step."""
    if user_count <= 0 or step_users <= 0 or step_duration <= 0 or run_time <= 0:
        return []

    stages = []
    step_spawn_rate = max(1, (step_users + step_duration - 1) // step_duration)
    current_users = 0
    stage_start = 0

    while stage_start < run_time:
        if current_users < user_count:
            current_users = min(current_users + step_users, user_count)
        stage_end = min(stage_start + step_duration, run_time)
        stages.append({
            'start': int(stage_start),
            'end': int(stage_end),
            'users': int(current_users),
            'spawn_rate': int(step_spawn_rate),
        })
        stage_start += step_duration

    return stages


def _inject_step_load_shape(script_content, stages):
    if not stages:
        return script_content

    shape_script = f'''

from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    stages = {json.dumps(stages)}

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["end"]:
                return (stage["users"], stage["spawn_rate"])
        return None
'''
    return script_content.rstrip() + shape_script + '\n'


def _build_locust_command(locustfile, base_host, csv_prefix, run_time, user_count, spawn_rate, step_load_enabled):
    cmd = [
        sys.executable, '-m', 'locust',
        '-f', locustfile,
        '--host', base_host,
        '--run-time', f'{run_time}s',
        '--headless',
        '--csv', csv_prefix,
        '--loglevel', 'WARNING',
        '--only-summary',
        '--csv-full-history'
    ]

    if not step_load_enabled:
        cmd.extend([
            '--users', str(user_count),
            '--spawn-rate', str(spawn_rate),
        ])

    return cmd

