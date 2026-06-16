"""
测试用例标签与优先级管理服务

提供标签的统计、过滤和管理能力。
"""

from typing import Dict, Any, List, Optional
from ..extensions import db
from ..models.api_test_case import ApiTestCase
from ..core.logging import get_logger

logger = get_logger(__name__)

# 优先级映射
PRIORITY_MAP = {
    1: {"name": "P0", "label": "阻塞", "color": "#C75450"},
    2: {"name": "P1", "label": "严重", "color": "#D4B483"},
    3: {"name": "P2", "label": "一般", "color": "#5B8FB9"},
    4: {"name": "P3", "label": "低优先级", "color": "#629B95"},
}


class TagManagerService:
    """标签与优先级管理服务"""

    def get_tag_stats(self, project_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取标签统计

        Args:
            project_id: 限定项目

        Returns:
            List[Dict]: [{tag, count, percentage}]
        """
        query = ApiTestCase.query
        if project_id:
            query = query.filter_by(project_id=project_id)

        cases = query.all()
        total = len(cases)
        tag_counts = {}

        for case in cases:
            tags = case.tags or []
            if isinstance(tags, list):
                for tag in tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        stats = []
        for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
            stats.append({
                "tag": tag,
                "count": count,
                "percentage": round(count / max(total, 1) * 100, 1),
            })

        return stats

    def get_priority_stats(self, project_id: Optional[int] = None) -> Dict[str, Any]:
        """
        获取优先级统计

        Returns:
            Dict: {total, by_priority: {1: count, 2: count, ...}}
        """
        query = ApiTestCase.query
        if project_id:
            query = query.filter_by(project_id=project_id)

        cases = query.all()
        by_priority = {}
        for case in cases:
            p = case.priority or 2
            by_priority[p] = by_priority.get(p, 0) + 1

        return {
            "total": len(cases),
            "by_priority": {
                str(k): {"count": v, "info": PRIORITY_MAP.get(k, {})}
                for k, v in sorted(by_priority.items())
            },
        }

    def filter_by_tags(
        self,
        tags: List[str],
        project_id: Optional[int] = None,
        match_all: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        按标签过滤用例

        Args:
            tags: 标签列表
            project_id: 限定项目
            match_all: True=全部匹配，False=任一匹配

        Returns:
            List[Dict]: 匹配的用例列表
        """
        query = ApiTestCase.query
        if project_id:
            query = query.filter_by(project_id=project_id)

        cases = query.all()
        matched = []

        for case in cases:
            case_tags = set(case.tags or [])
            if match_all:
                if set(tags).issubset(case_tags):
                    matched.append(case.to_dict())
            else:
                if set(tags) & case_tags:
                    matched.append(case.to_dict())

        return matched

    def filter_by_priority(
        self,
        priorities: List[int],
        project_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        按优先级过滤用例

        Args:
            priorities: 优先级列表（1-4）
            project_id: 限定项目

        Returns:
            List[Dict]: 匹配的用例列表
        """
        query = ApiTestCase.query
        if project_id:
            query = query.filter_by(project_id=project_id)

        query = query.filter(ApiTestCase.priority.in_(priorities))
        return [c.to_dict() for c in query.all()]


_instance = None


def get_tag_manager_service() -> TagManagerService:
    global _instance
    if _instance is None:
        _instance = TagManagerService()
    return _instance