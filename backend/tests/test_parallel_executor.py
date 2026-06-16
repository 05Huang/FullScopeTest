"""
并行测试执行引擎测试
"""

import pytest
import time


class TestParallelExecutor:
    """ParallelExecutor 测试"""

    def test_execute_empty_cases(self, app):
        """空用例列表应返回空结果"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=2)
            result = executor.execute_parallel([], lambda c: {"passed": True})
            assert result["total"] == 0
            assert result["passed"] == 0
            assert result["results"] == []

    def test_execute_all_pass(self, app):
        """全部通过的用例"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=2)
            cases = [{"name": f"case_{i}"} for i in range(5)]
            result = executor.execute_parallel(
                cases, lambda c: {"passed": True, "name": c["name"]}
            )
            assert result["total"] == 5
            assert result["passed"] == 5
            assert result["failed"] == 0

    def test_execute_mixed_results(self, app):
        """混合通过/失败的结果"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=2)

            def execute_fn(case):
                if case.get("should_fail"):
                    return {"passed": False, "error": "assertion failed"}
                return {"passed": True}

            cases = [
                {"name": "pass1"},
                {"name": "fail1", "should_fail": True},
                {"name": "pass2"},
            ]
            result = executor.execute_parallel(cases, execute_fn)
            assert result["total"] == 3
            assert result["passed"] == 2
            assert result["failed"] == 1

    def test_execute_with_exception(self, app):
        """执行函数抛出异常应被捕获"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=2)

            def execute_fn(case):
                raise ValueError("test error")

            cases = [{"name": "error_case"}]
            result = executor.execute_parallel(cases, execute_fn)
            assert result["total"] == 1
            assert result["failed"] == 1
            assert "error" in result["results"][0]

    def test_progress_callback(self, app):
        """进度回调应被调用"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=2)
            progress_calls = []

            def on_progress(completed, total, passed, failed):
                progress_calls.append((completed, total, passed, failed))

            cases = [{"name": f"case_{i}"} for i in range(3)]
            executor.execute_parallel(
                cases, lambda c: {"passed": True}, progress_callback=on_progress
            )
            assert len(progress_calls) == 3
            assert progress_calls[-1][0] == 3  # 最后一次 completed = 3

    def test_max_workers_limited(self, app):
        """并行度应被限制在合理范围"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=100)
            assert executor.max_workers <= 20

    def test_get_config(self, app):
        """配置信息应包含关键字段"""
        with app.app_context():
            from app.services.parallel_executor import ParallelExecutor
            executor = ParallelExecutor(max_workers=3)
            config = executor.get_config()
            assert "max_workers" in config
            assert config["max_workers"] == 3
