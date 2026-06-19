"""
测试执行成本估算服务

基于历史平均执行时间预估总耗时。
"""

from typing import Dict, Any, List, Optional
from ..extensions import db
from ..models.api_test_case import ApiTestCase
from ..models.test_run import TestRun
from ..core.logging import get_logger
from sqlalchemy import func

logger = get_logger(__name__)


class TestCostEstimator:
    """测试执行成本估算"""

    def estimate_collection(
        self,
        collection_id: int,
        env_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        估算用例集执行成本

        Args:
            collection_id: 用例集 ID
            env_id: 环境 ID

        Returns:
            Dict: {total_cases, estimated_seconds, estimated_minutes, per_case}
        """
        cases = ApiTestCase.query.filter_by(collection_id=collection_id).all()
        if not cases:
            return {'total_cases': 0, 'estimated_seconds': 0, 'estimated_minutes': 0, 'per_case': []}

        case_ids = [c.id for c in cases]

        # 查询历史平均执行时间
        avg_times = {}
        if case_ids:
            results = db.session.query(
                TestRun.case_id,
                func.avg(TestRun.duration_ms).label('avg_time'),
            ).filter(
                TestRun.case_id.in_(case_ids),
                TestRun.duration_ms.isnot(None),
            ).group_by(TestRun.case_id).all()

            for case_id, avg_time in results:
                avg_times[case_id] = float(avg_time) if avg_time else 0

        per_case = []
        total_ms = 0
        for case in cases:
            avg_time = avg_times.get(case.id)
            if avg_time is None:
                # 无历史数据，使用默认估算
                avg_time = (case.timeout or 5) * 1000 * 0.3  # 默认取超时的 30%
            per_case.append({
                'case_id': case.id,
                'name': case.name,
                'method': case.method,
                'url': case.url,
                'estimated_ms': round(avg_time, 1),
                'has_history': case.id in avg_times,
            })
            total_ms += avg_time

        total_seconds = total_ms / 1000
        return {
            'total_cases': len(cases),
            'estimated_seconds': round(total_seconds, 1),
            'estimated_minutes': round(total_seconds / 60, 1),
            'per_case': per_case,
            'confidence': 'high' if len(avg_times) > len(cases) * 0.5 else 'low',
        }


_instance = None


def get_test_cost_estimator() -> TestCostEstimator:
    global _instance
    if _instance is None:
        _instance = TestCostEstimator()
    return _instance
