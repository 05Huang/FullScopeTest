"""
并行测试执行引擎

支持同一用例集内的用例并行执行，显著提升大量用例的执行效率。

特性：
- 可配置并行度（默认 5，最大 20）
- 进度实时汇总（已执行/总数/通过/失败）
- 资源限制：防止并发过高压垮被测系统
- 结果汇总：所有并行结果合并为统一报告
"""

import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Callable, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)


class ParallelExecutor:
    """并行测试执行器"""

    def __init__(self, max_workers: int = None):
        """
        初始化并行执行器

        Args:
            max_workers: 最大并行数（默认从配置读取）
        """
        if max_workers is None:
            max_workers = int(os.environ.get("PARALLEL_WORKERS", "5"))
        max_allowed = int(os.environ.get("MAX_PARALLEL_WORKERS", "20"))
        self.max_workers = min(max(max_workers, 1), max_allowed)
        logger.info("并行执行器初始化", max_workers=self.max_workers)

    def execute_parallel(
        self,
        cases: List[Any],
        execute_fn: Callable,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        并行执行测试用例

        Args:
            cases: 待执行的用例列表
            execute_fn: 执行函数 (case) -> result_dict
            progress_callback: 进度回调 (completed, total, passed, failed)

        Returns:
            Dict: {results, total, passed, failed, duration}
        """
        total = len(cases)
        if total == 0:
            return {"results": [], "total": 0, "passed": 0, "failed": 0, "duration": 0}

        results = [None] * total
        passed = 0
        failed = 0
        completed = 0
        start_time = time.time()

        logger.info("开始并行执行", total=total, workers=self.max_workers)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_index = {}
            for i, case in enumerate(cases):
                future = executor.submit(self._safe_execute, execute_fn, case, i)
                future_to_index[future] = i

            # 收集结果
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result(timeout=300)  # 5 分钟超时
                    results[index] = result
                    if result.get("passed", False):
                        passed += 1
                    else:
                        failed += 1
                except Exception as exc:
                    results[index] = {
                        "passed": False,
                        "error": str(exc),
                        "case_index": index,
                    }
                    failed += 1

                completed += 1
                if progress_callback:
                    try:
                        progress_callback(completed, total, passed, failed)
                    except Exception:
                        pass  # 回调失败不影响执行

        duration = time.time() - start_time

        logger.info(
            "并行执行完成",
            total=total, passed=passed, failed=failed,
            duration=round(duration, 2),
            parallel_speedup=f"{total * (duration / max(completed, 1) / self.max_workers):.1f}x" if completed > 0 else "N/A",
        )

        return {
            "results": [r for r in results if r is not None],
            "total": total,
            "passed": passed,
            "failed": failed,
            "duration": round(duration, 2),
            "parallel_workers": self.max_workers,
        }

    @staticmethod
    def _safe_execute(execute_fn: Callable, case: Any, index: int) -> Dict[str, Any]:
        """安全执行单个用例（捕获异常）"""
        try:
            result = execute_fn(case)
            if isinstance(result, dict):
                result["case_index"] = index
                return result
            return {"passed": bool(result), "case_index": index, "raw_result": result}
        except Exception as exc:
            logger.warning("用例执行异常", case_index=index, error=str(exc))
            return {"passed": False, "error": str(exc), "case_index": index}


    def get_config(self) -> Dict[str, Any]:
        """获取当前并行配置"""
        return {
            "max_workers": self.max_workers,
            "max_allowed": int(os.environ.get("MAX_PARALLEL_WORKERS", "20")),
            "configured": int(os.environ.get("PARALLEL_WORKERS", "5")),
        }


_instance = None


def get_parallel_executor() -> ParallelExecutor:
    """获取并行执行器单例"""
    global _instance
    if _instance is None:
        _instance = ParallelExecutor()
    return _instance