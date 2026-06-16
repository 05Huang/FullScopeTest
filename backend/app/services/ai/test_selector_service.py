"""
智能测试选择服务

基于代码变更分析，智能推荐需要执行的测试子集。
"""

import re
from typing import Dict, Any, List, Optional, Set
from ...extensions import db
from ...models.api_test_case import ApiTestCase
from ...core.logging import get_logger

logger = get_logger(__name__)

PATH_MAPPING_RULES = [
    (r"app/api/(\w+)\.py", r"/api/v1/\1"),
    (r"app/services/(\w+)_service\.py", r"/api/v1/\1"),
    (r"app/models/(\w+)\.py", None),  # model changes affect all
]


class TestSelectorService:
    """智能测试选择服务"""

    def select_tests(
        self,
        changed_files: List[str],
        project_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
        max_cases: int = 50,
    ) -> Dict[str, Any]:
        """
        根据代码变更智能选择测试用例

        Args:
            changed_files: 变更的文件路径列表
            project_id: 限定项目 ID
            tags: 按标签过滤
            max_cases: 最大返回用例数

        Returns:
            Dict: {cases, reasoning, total_estimated_time, affected_paths}
        """
        if not changed_files:
            return {"cases": [], "reasoning": "无变更文件", "total_estimated_time": 0}

        affected_paths = self._map_files_to_paths(changed_files)
        matched_cases = self._find_cases(affected_paths, project_id, tags)
        scored_cases = self._apply_scores(matched_cases)
        scored_cases.sort(key=lambda x: x["score"], reverse=True)
        selected = scored_cases[:max_cases]
        total_time = sum(c.get("estimated_time", 5) for c in selected)

        logger.info(
            "智能选测完成",
            changed_files=len(changed_files),
            affected_paths=len(affected_paths),
            selected=len(selected),
        )
        return {
            "cases": selected,
            "reasoning": self._build_reasoning(changed_files, affected_paths, selected),
            "total_estimated_time": total_time,
            "affected_paths": list(affected_paths),
        }

    def _map_files_to_paths(self, files: List[str]) -> Set[str]:
        """将文件路径映射到 API 路径"""
        paths: Set[str] = set()
        model_changes = False

        for filepath in files:
            filepath = filepath.replace("\\", "/")
            matched = False
            for pattern, api_prefix in PATH_MAPPING_RULES:
                m = re.search(pattern, filepath)
                if m:
                    if api_prefix is None:
                        model_changes = True
                    else:
                        paths.add(re.sub(pattern, api_prefix, filepath))
                    matched = True
                    break
            if not matched:
                # 从文件名提取关键词
                parts = filepath.split("/")
                for part in parts:
                    if part.endswith((".py", ".ts", ".tsx")):
                        keyword = part.rsplit(".", 1)[0]
                        if len(keyword) > 2:
                            paths.add(keyword)

        if model_changes:
            paths.add("__all__")
        return paths

    def _find_cases(
        self,
        affected_paths: Set[str],
        project_id: Optional[int],
        tags: Optional[List[str]],
    ) -> List[Dict[str, Any]]:
        """查找匹配的测试用例"""
        query = ApiTestCase.query
        if project_id:
            query = query.filter_by(project_id=project_id)
        if tags:
            for tag in tags:
                query = query.filter(ApiTestCase.tags.like(f"%{tag}%"))

        all_cases = query.order_by(ApiTestCase.created_at.desc()).limit(500).all()
        matched = []
        match_all = "__all__" in affected_paths

        for case in all_cases:
            match_reason = None
            if match_all:
                match_reason = "模型变更影响"
            else:
                case_url = (case.url or "").lower()
                for ap in affected_paths:
                    if ap.lower() in case_url or case_url in ap.lower():
                        match_reason = f"URL 匹配: {ap}"
                        break
                    if len(ap) > 2 and ap.lower() in (case.name or "").lower():
                        match_reason = f"名称匹配: {ap}"
                        break

            if match_reason:
                estimated_time = min(case.timeout or 5, 60)
                matched.append({
                    "case": case.to_dict(),
                    "match_reason": match_reason,
                    "estimated_time": estimated_time,
                    "score": 1.0,
                })
        return matched

    def _apply_scores(self, cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """根据历史数据和优先级加分"""
        for item in cases:
            case = item["case"]
            score = item["score"]
            if case.get("last_status") == "failed":
                score += 2.0
                item["history_bonus"] = "最近失败，优先执行"
            elif case.get("last_status") == "passed":
                score += 0.5
            priority = (case.get("priority") or "").lower()
            if priority in ("p0", "critical"):
                score += 1.5
            elif priority in ("p1", "high"):
                score += 1.0
            item["score"] = score
        return cases

    def _build_reasoning(self, files, paths, selected) -> str:
        """构建选测理由"""
        parts = [f"检测到 {len(files)} 个文件变更"]
        if "__all__" in paths:
            parts.append("包含模型变更，扩大测试范围")
        else:
            parts.append(f"映射到 {len(paths)} 个 API 路径")
        parts.append(f"推荐执行 {len(selected)} 个用例")
        return "；".join(parts)


_instance = None


def get_test_selector_service() -> TestSelectorService:
    global _instance
    if _instance is None:
        _instance = TestSelectorService()
    return _instance
