"""
Flaky Test 检测服务

分析测试用例在最近 N 次执行中的通过/失败模式，
自动识别不稳定（flaky）的测试用例。

评分算法：(状态切换次数 / 执行次数) * 100
- > 30: 疑似不稳定
- > 60: 不稳定
"""

from typing import Dict, Any, List, Optional
from ...extensions import db
from ...models.api_test_case import ApiTestCase
from ...core.logging import get_logger

logger = get_logger(__name__)


class FlakyDetectorService:
    """Flaky Test 检测服务"""

    def detect_flaky_tests(
        self,
        project_id: Optional[int] = None,
        recent_runs: int = 20,
        min_runs: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        检测项目中的 flaky 测试用例

        Args:
            project_id: 限定项目 ID
            recent_runs: 分析最近 N 次执行
            min_runs: 最少执行次数（低于此数不分析）

        Returns:
            List[Dict]: flaky 用例列表，按 flaky_score 降序
        """
        query = ApiTestCase.query
        if project_id:
            query = query.filter_by(project_id=project_id)

        # 只分析有过执行记录的用例
        cases = query.filter(
            ApiTestCase.last_status.isnot(None),
            ApiTestCase.last_run_at.isnot(None),
        ).all()

        results = []
        for case in cases:
            result = self._analyze_case(case)
            if result and result["run_count"] >= min_runs:
                results.append(result)

        # 按 flaky_score 降序
        results.sort(key=lambda x: x["flaky_score"], reverse=True)

        logger.info(
            "Flaky 检测完成",
            project_id=project_id,
            analyzed=len(cases),
            flaky_count=len([r for r in results if r["flaky_score"] > 30]),
        )
        return results

    def get_flaky_report(
        self,
        project_id: Optional[int] = None,
        top_n: int = 10,
    ) -> Dict[str, Any]:
        """
        生成 Flaky 测试报告

        Args:
            project_id: 限定项目 ID
            top_n: 返回 Top N

        Returns:
            Dict: 包含 flaky 用例列表和统计信息
        """
        flaky_tests = self.detect_flaky_tests(project_id=project_id)

        suspected = [t for t in flaky_tests if t["flaky_score"] > 30]
        confirmed = [t for t in flaky_tests if t["flaky_score"] > 60]

        report = {
            "total_analyzed": len(flaky_tests),
            "suspected_flaky": len(suspected),
            "confirmed_flaky": len(confirmed),
            "top_flaky": flaky_tests[:top_n],
            "categories": {
                "suspected": [t for t in suspected if t["flaky_score"] <= 60],
                "confirmed": confirmed,
            },
        }
        return report

    def _analyze_case(self, case: ApiTestCase) -> Optional[Dict[str, Any]]:
        """分析单个用例的稳定性"""
        # 使用 last_status 作为当前状态
        # 在实际场景中，这里会查询 test_runs 的 results 字段来获取历史
        # 简化实现：基于 case 的 last_status 和 last_result 进行分析
        last_status = case.last_status
        if not last_status:
            return None

        # 简化的 flaky 评分
        # 真实实现需要查询历史执行记录
        run_count = 1  # 至少执行过 1 次
        status_changes = 0

        # 从 last_result 中提取历史信息（如果可用）
        last_result = case.last_result or {}
        if isinstance(last_result, dict):
            history = last_result.get("history", [])
            if history:
                run_count = len(history)
                for i in range(1, len(history)):
                    if history[i] != history[i - 1]:
                        status_changes += 1

        flaky_score = (status_changes / max(run_count, 1)) * 100

        # 分类
        if flaky_score > 60:
            category = "unstable"
            label = "不稳定"
        elif flaky_score > 30:
            category = "suspected"
            label = "疑似不稳定"
        else:
            category = "stable"
            label = "稳定"

        return {
            "case_id": case.id,
            "case_name": case.name,
            "url": case.url,
            "method": case.method,
            "last_status": last_status,
            "run_count": run_count,
            "status_changes": status_changes,
            "flaky_score": round(flaky_score, 1),
            "category": category,
            "label": label,
        }


_instance = None


def get_flaky_detector_service() -> FlakyDetectorService:
    global _instance
    if _instance is None:
        _instance = FlakyDetectorService()
    return _instance
