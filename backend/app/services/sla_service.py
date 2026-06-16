"""
SLA 追踪与告警服务

追踪测试通过率是否满足 SLA 要求。
"""

import os
from typing import Dict, Any, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# 默认 SLA 配置
DEFAULT_SLA = {
    "api_pass_rate": float(os.environ.get("SLA_API_PASS_RATE", "95.0")),
    "web_pass_rate": float(os.environ.get("SLA_WEB_PASS_RATE", "90.0")),
    "perf_p95_ms": float(os.environ.get("SLA_PERF_P95_MS", "2000")),
    "availability": float(os.environ.get("SLA_AVAILABILITY", "99.9")),
}


class SLAService:
    """SLA 追踪服务"""

    def evaluate_sla(self, metrics: Dict[str, Any], sla_config: Dict[str, float] = None) -> Dict[str, Any]:
        """
        评估 SLA 达标情况

        Args:
            metrics: 当前指标 {api_pass_rate, web_pass_rate, perf_p95_ms, availability}
            sla_config: SLA 配置（可选，默认使用 DEFAULT_SLA）

        Returns:
            Dict: SLA 评估结果
        """
        sla = sla_config or DEFAULT_SLA
        results = {}
        all_passed = True

        for key, threshold in sla.items():
            actual = metrics.get(key, 0)
            if key.endswith("_ms"):
                # 响应时间：越低越好
                passed = actual <= threshold
                status = "ok" if passed else ("warning" if actual <= threshold * 1.2 else "violation")
            else:
                # 通过率/可用性：越高越好
                passed = actual >= threshold
                status = "ok" if passed else ("warning" if actual >= threshold * 0.95 else "violation")

            if not passed:
                all_passed = False

            results[key] = {
                "threshold": threshold,
                "actual": actual,
                "passed": passed,
                "status": status,
            }

        return {
            "overall_status": "ok" if all_passed else "violation",
            "checks": results,
        }


_instance = None


def get_sla_service():
    global _instance
    if _instance is None: _instance = SLAService()
    return _instance
