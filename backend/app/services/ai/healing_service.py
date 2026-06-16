"""
AI 测试用例自愈服务

当测试用例执行失败时，AI 分析失败原因并提供修复建议。
"""

import json
from typing import Dict, Any, List, Optional
from ...extensions import db
from ...models.api_test_case import ApiTestCase
from ...models.test_case_version import TestCaseVersion
from ..ai.base import AIServiceBase
from ...core.logging import get_logger
from ...utils.exceptions import NotFoundError

logger = get_logger(__name__)

HEALING_SYSTEM_PROMPT = """你是 API 测试用例修复专家。根据测试失败信息分析原因并给出修复建议。
返回格式（严格 JSON）：
{"failure_reason": "分类", "analysis": "分析", "fixes": [{"field": "字段", "current": "当前值", "suggested": "建议值", "reason": "原因"}], "confidence": 0.8}
failure_reason 可选：path_changed/field_missing/status_changed/auth_expired/timeout/server_error/data_format/unknown
"""


class HealingService(AIServiceBase):
    """AI 用例自愈服务"""

    def heal_case(self, case_id: int, failure_info: Dict[str, Any], user_id: Optional[int] = None) -> Dict[str, Any]:
        """为单个失败用例生成修复建议"""
        case = ApiTestCase.query.get(case_id)
        if not case:
            raise NotFoundError("测试用例", case_id)

        case_text = self._case_to_text(case)
        failure_text = self._failure_to_text(failure_info)
        msg_content = "测试用例:\n" + case_text + "\n\n失败信息:\n" + failure_text + "\n\n请分析并给出修复建议。"
        messages = [{"role": "user", "content": msg_content}]

        response = self.simple_chat(messages=messages, feature="case_healing", user_id=user_id, system_prompt=HEALING_SYSTEM_PROMPT, temperature=0.2)
        content = self.get_content(response)
        suggestion = self._parse_suggestion(content, case_id)
        suggestion["original_case"] = case.to_dict()
        return suggestion

    def heal_collection(self, collection_id: int, failures: List[Dict[str, Any]], user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """批量自愈用例集中的失败用例"""
        from ...models.api_test_case import ApiTestCollection
        collection = ApiTestCollection.query.get(collection_id)
        if not collection:
            raise NotFoundError("用例集", collection_id)
        results = []
        for failure in failures:
            try:
                suggestion = self.heal_case(failure["case_id"], failure.get("failure_info", {}), user_id)
                results.append(suggestion)
            except Exception as exc:
                results.append({"case_id": failure["case_id"], "error": str(exc)})
        return results

    def apply_fix(self, case_id: int, fixes: List[Dict[str, Any]], user_id: Optional[int] = None) -> Dict[str, Any]:
        """应用修复建议到用例"""
        case = ApiTestCase.query.get(case_id)
        if not case:
            raise NotFoundError("测试用例", case_id)
        # 保存版本快照
        try:
            # 获取最新版本号
            from sqlalchemy import func
            max_ver = db.session.query(func.max(TestCaseVersion.version)).filter_by(
                case_type="api", case_id=case.id
            ).scalar() or 0
            db.session.add(TestCaseVersion(
                case_type="api", case_id=case.id, version=max_ver + 1,
                content=case.to_dict(), change_summary="AI 自愈前快照", created_by=user_id,
            ))
        except Exception:
            pass
        applied = []
        for fix in fixes:
            field = fix.get("field")
            if field and hasattr(case, field) and fix.get("suggested") is not None:
                setattr(case, field, fix["suggested"])
                applied.append(field)
        db.session.commit()
        return {"case_id": case_id, "applied_fields": applied, "updated_case": case.to_dict(), "message": f"已应用 {len(applied)} 项修复"}

    def _case_to_text(self, case: ApiTestCase) -> str:
        parts = [f"名称: {case.name}", f"方法: {case.method}", f"URL: {case.url}"]
        if case.assertions: parts.append(f"断言: {json.dumps(case.assertions, ensure_ascii=False)}")
        return "\n".join(parts)

    def _failure_to_text(self, info: Dict[str, Any]) -> str:
        parts = []
        for key, label in [("status_code", "状态码"), ("expected_status", "期望状态码"), ("response_body", "响应"), ("error_message", "错误")]:
            if key in info: parts.append(f"{label}: {str(info[key])[:500]}")
        return "\n".join(parts)

    def _parse_suggestion(self, content: str, case_id: int) -> Dict[str, Any]:
        try:
            if "```json" in content: json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content: json_str = content.split("```")[1].split("```")[0].strip()
            else: json_str = content.strip()
            result = json.loads(json_str)
            result["case_id"] = case_id
            result["can_auto_apply"] = result.get("confidence", 0) >= 0.7 and len(result.get("fixes", [])) > 0
            return result
        except (json.JSONDecodeError, IndexError):
            return {"case_id": case_id, "failure_reason": "unknown", "analysis": content[:500], "fixes": [], "confidence": 0.3, "can_auto_apply": False}
