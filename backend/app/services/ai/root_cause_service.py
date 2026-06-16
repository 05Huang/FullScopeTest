"""
AI 失败根因分析服务

测试执行完成后，AI 分析所有失败用例并归类原因：
- 环境问题
- 数据问题
- 接口变更
- 认证失败
- 超时
- 可能的产品 Bug

输出根因报告：失败用例按原因聚合，每类给出修复建议。
"""

import json
from typing import Dict, Any, List, Optional
from ..ai.base import AIServiceBase
from ...core.logging import get_logger

logger = get_logger(__name__)

ROOT_CAUSE_PROMPT = """你是测试失败根因分析专家。分析以下失败用例列表，归类失败原因。

返回格式（严格 JSON）：
{
  "summary": {"total_failed": N, "categories": 4},
  "categories": [
    {
      "reason": "失败原因分类",
      "reason_label": "原因中文标签",
      "count": N,
      "case_names": ["用例名1", "用例名2"],
      "suggestion": "修复建议"
    }
  ]
}

失败原因分类：
- env_issue: 环境问题（服务不可用、配置错误）
- data_issue: 数据问题（测试数据缺失、格式错误）
- api_changed: 接口变更（路径/字段/状态码变更）
- auth_expired: 认证过期（Token 失效、权限变更）
- timeout: 超时
- bug: 可能的产品 Bug
- other: 其他"""


class RootCauseService(AIServiceBase):
    """AI 失败根因分析服务"""

    def analyze_failures(
        self,
        failures: List[Dict[str, Any]],
        user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        分析失败用例列表，归类根因

        Args:
            failures: 失败用例列表，每项包含
                {case_name, status_code, error_message, response_body, url, method}
            user_id: 请求用户 ID

        Returns:
            Dict: 根因分析报告
        """
        if not failures:
            return {
                "summary": {"total_failed": 0, "categories": 0},
                "categories": [],
            }

        # 构建失败摘要文本
        failure_text = self._build_failure_text(failures)
        messages = [
            {
                "role": "user",
                "content": f"以下 {len(failures)} 个测试用例执行失败，请分析根因：\n\n{failure_text}",
            }
        ]

        response = self.simple_chat(
            messages=messages,
            feature="root_cause_analysis",
            user_id=user_id,
            system_prompt=ROOT_CAUSE_PROMPT,
            temperature=0.2,
            fallback_response=None,
        )

        content = self.get_content(response)
        report = self._parse_report(content, failures)

        logger.info(
            "根因分析完成",
            total_failed=len(failures),
            categories=len(report.get("categories", [])),
        )
        return report

    def _build_failure_text(self, failures: List[Dict[str, Any]]) -> str:
        """构建失败摘要文本"""
        parts = []
        for i, f in enumerate(failures, 1):
            parts.append(
                f"{i}. {f.get('case_name', 'unknown')} "
                f"[{f.get('method', '?')} {f.get('url', '?')}] "
                f"status={f.get('status_code', '?')} "
                f"error={str(f.get('error_message', ''))[:200]}"
            )
        return "\n".join(parts)

    def _parse_report(self, content: str, failures: List[Dict]) -> Dict[str, Any]:
        """解析 AI 返回的根因报告"""
        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()
            result = json.loads(json_str)
            result.setdefault("summary", {})
            result["summary"]["total_failed"] = len(failures)
            return result
        except (json.JSONDecodeError, IndexError):
            # 降级：按状态码简单分类
            return self._fallback_classify(failures)

    def _fallback_classify(self, failures: List[Dict]) -> Dict[str, Any]:
        """降级分类（AI 不可用时）"""
        categories = {}
        for f in failures:
            status = f.get("status_code", 0)
            if status == 404:
                key = "api_changed"
            elif status in (401, 403):
                key = "auth_expired"
            elif status >= 500:
                key = "bug"
            elif "timeout" in str(f.get("error_message", "")).lower():
                key = "timeout"
            else:
                key = "other"

            if key not in categories:
                categories[key] = {"reason": key, "count": 0, "case_names": [], "suggestion": ""}
            categories[key]["count"] += 1
            categories[key]["case_names"].append(f.get("case_name", "unknown"))

        return {
            "summary": {"total_failed": len(failures), "categories": len(categories)},
            "categories": list(categories.values()),
        }


_instance = None


def get_root_cause_service() -> RootCauseService:
    global _instance
    if _instance is None:
        _instance = RootCauseService()
    return _instance
