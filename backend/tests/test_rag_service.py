"""
RAG 检索增强服务测试

测试 EmbeddingService 和 RAGService 的核心功能。
"""

import pytest
import json
from unittest.mock import patch, MagicMock


class TestEmbeddingService:
    """EmbeddingService 测试"""

    def test_tfidf_embedding_returns_vector(self, app):
        """TF-IDF 降级方案应返回固定维度的向量"""
        with app.app_context():
            from app.services.ai.embedding_service import EmbeddingService
            svc = EmbeddingService()
            result = svc.embed("用户登录接口测试")
            assert isinstance(result, list)
            assert len(result) == 256  # 固定维度

    def test_embedding_empty_text(self, app):
        """空文本应返回空列表"""
        with app.app_context():
            from app.services.ai.embedding_service import EmbeddingService
            svc = EmbeddingService()
            assert svc.embed("") == []
            assert svc.embed("   ") == []

    def test_embedding_cached(self, app):
        """相同文本应返回缓存的向量"""
        with app.app_context():
            from app.services.ai.embedding_service import EmbeddingService
            svc = EmbeddingService()
            text = "测试缓存功能"
            result1 = svc.embed(text)
            result2 = svc.embed(text)
            assert result1 == result2

    def test_batch_embedding(self, app):
        """批量嵌入应返回与输入等长的列表"""
        with app.app_context():
            from app.services.ai.embedding_service import EmbeddingService
            svc = EmbeddingService()
            texts = ["用例1", "用例2", "用例3"]
            results = svc.embed_batch(texts)
            assert len(results) == 3
            for r in results:
                assert isinstance(r, list)
                assert len(r) == 256

    def test_cosine_similarity_identical(self):
        """相同向量的余弦相似度应为 1.0"""
        from app.services.ai.embedding_service import _cosine_similarity
        vec = {"a": 1.0, "b": 2.0, "c": 3.0}
        assert abs(_cosine_similarity(vec, vec) - 1.0) < 0.001

    def test_cosine_similarity_orthogonal(self):
        """正交向量的余弦相似度应为 0.0"""
        from app.services.ai.embedding_service import _cosine_similarity
        vec1 = {"a": 1.0}
        vec2 = {"b": 1.0}
        assert _cosine_similarity(vec1, vec2) == 0.0

    def test_tokenizer_chinese(self):
        """分词器应能处理中文"""
        from app.services.ai.embedding_service import _tokenize
        tokens = _tokenize("用户登录接口测试")
        assert len(tokens) > 0

    def test_tokenizer_english(self):
        """分词器应能处理英文"""
        from app.services.ai.embedding_service import _tokenize
        tokens = _tokenize("test user login api")
        assert "test" in tokens
        assert "user" in tokens


class TestRAGService:
    """RAGService 测试"""

    def test_retrieve_empty_query(self, app):
        """空查询应返回空结果"""
        with app.app_context():
            from app.services.ai.rag_service import RAGService
            svc = RAGService()
            result = svc.retrieve_similar_cases("")
            assert result == []

    def test_retrieve_no_cases(self, app):
        """无用例时应返回空结果"""
        with app.app_context():
            from app.services.ai.rag_service import RAGService
            svc = RAGService()
            result = svc.retrieve_similar_cases("查询不存在的用例")
            assert result == []

    def test_retrieve_with_cases(self, app, client):
        """有用例时应返回排序后的结果"""
        with app.app_context():
            from app.extensions import db
            from app.models.project import Project
            from app.models.api_test_case import ApiTestCase

            # 创建测试项目和用例
            project = Project(name="RAG 测试项目", owner_id=1)
            db.session.add(project)
            db.session.commit()

            cases = [
                ApiTestCase(
                    name="用户登录测试",
                    description="测试用户登录接口",
                    method="POST",
                    url="/api/login",
                    project_id=project.id,
                    user_id=1,
                ),
                ApiTestCase(
                    name="获取用户列表",
                    description="测试获取用户列表接口",
                    method="GET",
                    url="/api/users",
                    project_id=project.id,
                    user_id=1,
                ),
            ]
            for c in cases:
                db.session.add(c)
            db.session.commit()

            from app.services.ai.rag_service import RAGService
            svc = RAGService()
            result = svc.retrieve_similar_cases(
                "测试登录功能",
                project_id=project.id,
                top_k=2,
            )
            assert len(result) > 0
            assert "case" in result[0]
            assert "similarity" in result[0]

    def test_build_rag_context_returns_string(self, app, client):
        """构建 RAG 上下文应返回字符串"""
        with app.app_context():
            from app.services.ai.rag_service import RAGService
            svc = RAGService()
            context = svc.build_rag_context("用户登录测试查询")
            # 应返回字符串（可能有内容也可能为空）
            assert isinstance(context, str)

    def test_retrieve_top_k_limit(self, app, client):
        """top_k 应限制返回数量"""
        with app.app_context():
            from app.services.ai.rag_service import RAGService
            svc = RAGService()
            result = svc.retrieve_similar_cases("测试", top_k=3)
            assert len(result) <= 3
