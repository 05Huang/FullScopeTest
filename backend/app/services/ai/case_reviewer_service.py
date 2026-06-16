"""
AI 测试用例质量审查服务

审查维度：
- 断言完整性：是否有足够的断言验证响应
- 边界覆盖：是否覆盖了正常/异常/边界值
- 命名规范：用例名称是否清晰描述测试意图
- 数据独立性：是否依赖其他用例的状态
- 安全性：是否测试了 SQL 注入、XSS 等安全场景
"""

import json
from typing import Dict, Any, List, Optional
from ..ai.base import AIServiceBase
from ...models.api_test_case import ApiTestCase, ApiTestCollection
from ...core.logging import get_logger
from ...utils.exceptions import NotFoundError

logger = get_logger(__name__)

REVIEW_PROMPT = """你是测试用例质量审查专家。审查以下测试用例并给出评分和建议。

评分维度（每项 0-20 分，总分 100）：
1. 断言完整性（0-20）：是否有足够的断言验证响应
2. 边界覆盖（0-20）：是否覆盖了正常/异常/边界值
3. 命名规范（0-20）：用例名称是否清晰描述测试意图
4. 数据独立性（0-20）：是否依赖其他用例的状态
5. 安全性（0-20）：是否测试了注入、XSS 等安全场景

返回格式（严格 JSON）：
{"score": 85, "dimensions": {"assertions": {"score": 18, "comment": "..."}, "boundary": {"score": 16, "comment": "..."}, "naming": {"score": 17, "comment": "..."}, "independence": {"score": 18, "comment": "..."}, "security": {"score": 16, "comment": "..."}}, "suggestions": ["建议1", "建议2"], "overall": "整体评价"}
"""


class CaseReviewerService(AIServiceBase):
    """AI 用例质量审查服务"""

    def review_case(self, case_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """审查单个用例"""
        case = ApiTestCase.query.get(case_id)
        if not case:
            raise NotFoundError("测试用例", case_id)
        return self._do_review(case, user_id)

    def review_collection(self, collection_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """审查整个用例集"""
        collection = ApiTestCollection.query.get(collection_id)
        if not collection:
            raise NotFoundError("用例集", collection_id)

        cases = ApiTestCase.query.filter_by(collection_id=collection_id).all()
        results = []
        for case in cases:
            try:
                result = self._do_review(case, user_id)
                results.append(result)
            except Exception as exc:
                logger.warning("用例审查失败", case_id=case.id, error=str(exc))
                results.append({"case_id": case.id, "error": str(exc)})

        # 计算平均分
        scores = [r["score"] for r in results if "score" in r]
        avg_score = round(sum(scores) / max(len(scores), 1), 1)

        return {
            "collection_id": collection_id,
            "total_cases": len(cases),
            "reviewed": len(results),
            "average_score": avg_score,
            "results": results,
        }

    def _do_review(self, case: ApiTestCase, user_id: Optional[int]) -> Dict[str, Any]:
        """执行单个用例审查"""
        case_text = self._case_to_text(case)
        messages = [{"role": "user", "content": "审查以下测试用例：\n" + case_text}]

        response = self.simple_chat(
            messages=messages, feature="case_review", user_id=user_id,
            system_prompt=REVIEW_PROMPT, temperature=0.2,
        )
        content = self.get_content(response)
        return self._parse_review(content, case)

    def _case_to_text(self, case: ApiTestCase) -> str:
        """将用例转为审查文本"""
        parts = [
            f"名称: {case.name}",
            f"方法: {case.method}",
            f"URL: {case.url}",
            f"描述: {case.description or '无'}",
        ]
        if case.headers: parts.append(f"Headers: {json.dumps(case.headers, ensure_ascii=False)}")
        if case.body: parts.append(f"Body: {json.dumps(case.body, ensure_ascii=False)}")
        if case.assertions: parts.append(f"断言: {json.dumps(case.assertions, ensure_ascii=False)}")
        else: parts.append("断言: 无")
        return "\n".join(parts)

    def _parse_review(self, content: str, case: ApiTestCase) -> Dict[str, Any]:
        """解析审查结果"""
        try:
            if "```json" in content: json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content: json_str = content.split("```")[1].split("```")[0].strip()
            else: json_str = content.strip()
            result = json.loads(json_str)
            result["case_id"] = case.id
            result["case_name"] = case.name
            return result
        except (json.JSONDecodeError, IndexError):
            return self._fallback_review(case)

    def _fallback_review(self, case: ApiTestCase) -> Dict[str, Any]:
        """降级审查（AI 不可用时）"""
        score = 50  # 基础分
        dims = {}

        # 断言完整性
        assertions = case.assertions or []
        if len(assertions) >= 3:
            dims["assertions"] = {"score": 18, "comment": "断言充分"}
            score += 8
        elif len(assertions) >= 1:
            dims["assertions"] = {"score": 12, "comment": "断言较少"}
            score += 2
        else:
            dims["assertions"] = {"score": 0, "comment": "缺少断言"}

        # 命名规范
        name = case.name or ""
        if len(name) > 10 and any(kw in name for kw in ["测试", "test", "验证"]):
            dims["naming"] = {"score": 18, "comment": "命名规范"}
            score += 8
        else:
            dims["naming"] = {"score": 10, "comment": "命名可改进"}
            score += 2

        # 安全性
        if case.body and isinstance(case.body, dict):
            body_str = json.dumps(case.body)
            if any(kw in body_str.lower() for kw in ["inject", "xss", "script", "<"]):
                dims["security"] = {"score": 16, "comment": "包含安全测试"}
                score += 6
            else:
                dims["security"] = {"score": 8, "comment": "缺少安全测试"}
        else:
            dims["security"] = {"score": 5, "comment": "无安全相关断言"}

        score = min(score, 100)
        return {
            "case_id": case.id, "case_name": case.name, "score": score,
            "dimensions": dims,
            "suggestions": ["建议添加更多断言", "建议增加边界值测试"],
            "overall": "降级评估（AI 不可用）",
        }


_instance = None


def get_case_reviewer_service() -> CaseReviewerService:
    global _instance
    if _instance is None:
        _instance = CaseReviewerService()
    return _instance