"""
RAG 检索增强服务

基于已有用例的语义检索，为 LLM 生成提供上下文。

工作流程：
1. 用户请求生成测试用例时，先从项目中检索语义最相似的已有用例
2. 将检索到的用例作为 few-shot examples 注入 prompt
3. LLM 基于参考用例生成新用例

检索支持：
- 按项目过滤
- 按标签过滤
- 按测试类型过滤
"""

from typing import List, Dict, Any, Optional
from ...extensions import db
from ...models.api_test_case import ApiTestCase
from ...core.logging import get_logger
from .embedding_service import get_embedding_service, _cosine_similarity, _tfidf_vector

logger = get_logger(__name__)

# 默认检索数量
DEFAULT_TOP_K = 5
MAX_TOP_K = 10


class RAGService:
    """
    RAG 检索增强服务

    从项目中检索语义最相似的测试用例，
    为 AI 生成提供高质量的 few-shot 示例。
    """

    def retrieve_similar_cases(
        self,
        query: str,
        project_id: Optional[int] = None,
        top_k: int = DEFAULT_TOP_K,
        tags: Optional[List[str]] = None,
        method: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        检索与 query 语义最相似的测试用例

        Args:
            query: 查询文本（用户的需求描述或已有用例内容）
            project_id: 限定项目 ID（可选）
            top_k: 返回数量（默认 5，最大 10）
            tags: 按标签过滤（可选）
            method: 按 HTTP 方法过滤（可选）

        Returns:
            List[Dict]: 按相似度降序排列的用例列表，每项包含
                        {case_dict, similarity, matched_reason}
        """
        top_k = min(top_k, MAX_TOP_K)
        if not query or not query.strip():
            return []

        # 构建查询
        cases_query = ApiTestCase.query
        if project_id:
            cases_query = cases_query.filter_by(project_id=project_id)
        if method:
            cases_query = cases_query.filter_by(method=method.upper())
        if tags:
            # JSON 字段中的标签过滤（SQLite 兼容方式）
            for tag in tags:
                cases_query = cases_query.filter(
                    ApiTestCase.tags.like(f'%{tag}%')
                )

        cases = cases_query.order_by(ApiTestCase.created_at.desc()).limit(200).all()
        if not cases:
            return []

        # 计算查询向量
        emb_service = get_embedding_service()
        query_emb = emb_service.embed(query)
        if not query_emb:
            # 降级：使用关键词匹配
            return self._keyword_fallback(query, cases, top_k)

        # 计算所有用例的相似度
        scored_cases = []
        for case in cases:
            case_text = self._case_to_text(case)
            case_emb = emb_service.embed(case_text)
            if case_emb and len(case_emb) == len(query_emb):
                # 对于 TF-IDF 稠密向量使用余弦相似度
                similarity = sum(a * b for a, b in zip(query_emb, case_emb))
                scored_cases.append((case, similarity))

        # 排序取 top_k
        scored_cases.sort(key=lambda x: x[1], reverse=True)

        results = []
        for case, sim in scored_cases[:top_k]:
            results.append({
                "case": case.to_dict(),
                "similarity": round(sim, 4),
                "matched_reason": self._explain_match(query, case),
            })

        logger.info(
            "RAG 检索完成",
            query_length=len(query),
            candidates=len(cases),
            returned=len(results),
            top_similarity=results[0]["similarity"] if results else 0,
        )
        return results

    def build_rag_context(
        self,
        query: str,
        project_id: Optional[int] = None,
        top_k: int = DEFAULT_TOP_K,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        构建 RAG 上下文文本（可直接注入 prompt）

        Args:
            query: 查询文本
            project_id: 限定项目 ID
            top_k: 返回数量
            tags: 标签过滤

        Returns:
            str: 格式化的参考用例文本
        """
        similar_cases = self.retrieve_similar_cases(
            query=query,
            project_id=project_id,
            top_k=top_k,
            tags=tags,
        )

        if not similar_cases:
            return ""

        parts = ["以下是项目中已有的高质量测试用例，可作为参考：\n"]
        for i, item in enumerate(similar_cases, 1):
            case = item["case"]
            sim = item["similarity"]
            parts.append(
                f"--- 参考用例 {i} (相似度: {sim:.2f}) ---\n"
                f"名称: {case.get('name', '')}\n"
                f"方法: {case.get('method', '')} URL: {case.get('url', '')}\n"
                f"描述: {case.get('description', '')}\n"
                f"断言: {case.get('assertions', '')}\n"
            )

        return "\n".join(parts)

    def _case_to_text(self, case: ApiTestCase) -> str:
        """将测试用例转为可嵌入的文本"""
        parts = [
            case.name or "",
            case.description or "",
            f"{case.method} {case.url}" if case.method else "",
            str(case.headers) if case.headers else "",
            str(case.body) if case.body else "",
            str(case.assertions) if case.assertions else "",
        ]
        return " ".join(p for p in parts if p).strip()

    def _keyword_fallback(
        self, query: str, cases: List[ApiTestCase], top_k: int
    ) -> List[Dict[str, Any]]:
        """关键词匹配降级方案"""
        query_vec = _tfidf_vector(query)
        scored = []
        for case in cases:
            case_text = self._case_to_text(case)
            case_vec = _tfidf_vector(case_text)
            sim = _cosine_similarity(query_vec, case_vec)
            if sim > 0:
                scored.append((case, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for case, sim in scored[:top_k]:
            results.append({
                "case": case.to_dict(),
                "similarity": round(sim, 4),
                "matched_reason": "关键词匹配",
            })
        return results

    def _explain_match(self, query: str, case: ApiTestCase) -> str:
        """解释匹配原因"""
        reasons = []
        if case.url and any(kw in case.url.lower() for kw in query.lower().split()[:3]):
            reasons.append("URL 匹配")
        if case.name and any(kw in case.name.lower() for kw in query.lower().split()[:3]):
            reasons.append("名称匹配")
        if case.tags:
            reasons.append("标签匹配")
        return reasons[0] if reasons else "语义相似"


_service_instance = None


def get_rag_service() -> RAGService:
    """获取 RAG 服务单例"""
    global _service_instance
    if _service_instance is None:
        _service_instance = RAGService()
    return _service_instance
