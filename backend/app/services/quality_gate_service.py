"""
质量门禁服务

实现质量门禁规则的评估逻辑
"""

from typing import Dict, Any, Optional, List
from ..extensions import db
from ..models.quality_gate import QualityGate
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)


class QualityGateService:
    """质量门禁服务"""

    def evaluate(self, gate: QualityGate, test_run: TestRun) -> Dict[str, Any]:
        """
        评估质量门禁

        Args:
            gate: 质量门禁规则
            test_run: 测试运行记录

        Returns:
            评估结果
        """
        violations = []
        passed = True

        # 检查通过率阈值
        if gate.min_pass_rate is not None and test_run.total_cases > 0:
            pass_rate = round(test_run.passed / test_run.total_cases * 100, 2)
            if pass_rate < gate.min_pass_rate:
                violations.append({
                    'metric': 'pass_rate',
                    'threshold': gate.min_pass_rate,
                    'actual': pass_rate,
                    'message': f'通过率 {pass_rate}% 低于阈值 {gate.min_pass_rate}%',
                })
                passed = False

        # 检查 P95 响应时间阈值
        if gate.max_p95_response_time is not None:
            p95_time = self._get_p95_response_time(test_run)
            if p95_time is not None and p95_time > gate.max_p95_response_time:
                violations.append({
                    'metric': 'p95_response_time',
                    'threshold': gate.max_p95_response_time,
                    'actual': p95_time,
                    'message': f'P95 响应时间 {p95_time}ms 超过阈值 {gate.max_p95_response_time}ms',
                })
                passed = False

        # 检查视觉差异阈值
        if gate.max_visual_diff_percentage is not None:
            visual_diff = self._get_max_visual_diff(test_run)
            if visual_diff is not None and visual_diff > gate.max_visual_diff_percentage:
                violations.append({
                    'metric': 'visual_diff',
                    'threshold': gate.max_visual_diff_percentage,
                    'actual': visual_diff,
                    'message': f'视觉差异 {visual_diff}% 超过阈值 {gate.max_visual_diff_percentage}%',
                })
                passed = False

        result = {
            'passed': passed,
            'gate_id': gate.id,
            'gate_name': gate.name,
            'test_run_id': test_run.id,
            'violations': violations,
            'evaluated_at': None,
        }

        logger.info(
            'Quality gate evaluated',
            gate_id=gate.id,
            test_run_id=test_run.id,
            passed=passed,
            violations_count=len(violations),
        )

        return result

    def _get_p95_response_time(self, test_run: TestRun) -> Optional[float]:
        """获取 P95 响应时间"""
        if test_run.results and isinstance(test_run.results, dict):
            return test_run.results.get('p95_response_time')
        return None

    def _get_max_visual_diff(self, test_run: TestRun) -> Optional[float]:
        """获取最大视觉差异百分比"""
        if test_run.results and isinstance(test_run.results, dict):
            return test_run.results.get('max_visual_diff_percentage')
        return None


quality_gate_service = QualityGateService()
