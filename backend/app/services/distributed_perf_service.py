"""
分布式压测服务

支持多节点分布式压测，通过 Master-Worker 架构分担负载。
（预留接口，实际实现依赖外部 Worker 节点注册）
"""

from typing import Any, Dict, List, Optional
from .base import BaseService


class DistributedPerfService(BaseService):
    """分布式压测服务 — 管理 Worker 节点和任务分发"""

    def __init__(self):
        super().__init__()
        self._workers: Dict[str, dict] = {}

    def register_worker(self, worker_id: str, info: dict) -> None:
        """注册 Worker 节点"""
        self._workers[worker_id] = {
            "id": worker_id,
            "host": info.get("host", ""),
            "port": info.get("port", 0),
            "capacity": info.get("capacity", 100),  # 最大并发数
            "status": "idle",
            "current_load": 0,
        }
        self.logger.info("Worker 节点已注册", worker_id=worker_id, host=info.get("host"))

    def get_workers(self) -> List[dict]:
        """获取所有 Worker 节点"""
        return list(self._workers.values())

    def distribute_tasks(self, scenario_id: int, total_vus: int, steps: List[dict]) -> List[dict]:
        """
        将压测任务分发到各 Worker 节点

        Args:
            scenario_id: 场景 ID
            total_vus: 总虚拟用户数
            steps: 测试步骤

        Returns:
            分发计划 [{worker_id, vus_count, steps}]
        """
        workers = [w for w in self._workers.values() if w["status"] == "idle"]
        if not workers:
            self.logger.warning("无可用 Worker 节点")
            return []

        # 按容量比例分配 VU
        total_capacity = sum(w["capacity"] for w in workers)
        plan = []
        remaining_vus = total_vus

        for i, worker in enumerate(workers):
            if i == len(workers) - 1:
                assigned = remaining_vus
            else:
                assigned = max(1, int(total_vus * worker["capacity"] / total_capacity))
                assigned = min(assigned, remaining_vus)

            plan.append({
                "worker_id": worker["id"],
                "host": worker["host"],
                "vus_count": assigned,
                "steps": steps,
            })
            remaining_vus -= assigned

        self.logger.info("任务分发完成", scenario_id=scenario_id, workers=len(plan), total_vus=total_vus)
        return plan

    def collect_results(self, scenario_id: int) -> dict:
        """聚合各 Worker 的执行结果（预留接口）"""
        return {
            "scenario_id": scenario_id,
            "worker_count": len(self._workers),
            "status": "pending",
            "message": "分布式结果聚合功能待实现",
        }


# 模块级单例
_service = None


def get_distributed_perf_service() -> DistributedPerfService:
    global _service
    if _service is None:
        _service = DistributedPerfService()
    return _service
