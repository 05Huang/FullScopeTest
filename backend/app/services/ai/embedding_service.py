"""
向量化服务

提供文本嵌入（embedding）能力，用于 RAG 检索增强测试生成。

支持两种模式：
1. 外部 Embedding API（如 DeepSeek、OpenAI） — 高精度
2. 本地 TF-IDF 降级方案 — 零依赖，精度较低但可用

通过环境变量配置：
- EMBEDDING_API_URL：嵌入 API 地址
- EMBEDDING_API_KEY：API 密钥（默认复用 AI_ASSISTANT_API_KEY）
- EMBEDDING_MODEL：模型名称（默认 text-embedding-3-small）
"""

import os
import json
import hashlib
import math
import re
from typing import List, Optional
from collections import Counter

from ...extensions import db
from ...models.embedding_cache import EmbeddingCache
from ...core.logging import get_logger

logger = get_logger(__name__)


def _text_hash(text: str) -> str:
    """计算文本的 SHA256 哈希"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _tokenize(text: str) -> List[str]:
    """简单分词：中英文混合分词"""
    text = re.sub(r"[^\w一-鿿]", " ", text.lower())
    tokens = []
    for word in text.split():
        if word.isascii() and len(word) > 1:
            tokens.append(word)
        else:
            for i in range(len(word) - 1):
                tokens.append(word[i:i+2])
            if len(word) > 0:
                tokens.append(word)
    return tokens


def _tfidf_vector(text: str, idf_map: dict = None) -> dict:
    """计算 TF-IDF 向量（稀疏表示）"""
    tokens = _tokenize(text)
    if not tokens:
        return {}
    tf = Counter(tokens)
    total = len(tokens)
    vector = {}
    for token, count in tf.items():
        tfidf = count / total
        if idf_map and token in idf_map:
            tfidf *= idf_map[token]
        vector[token] = tfidf
    return vector


def _cosine_similarity(vec1: dict, vec2: dict) -> float:
    """计算两个稀疏向量的余弦相似度"""
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    dot = sum(vec1[k] * vec2[k] for k in common)
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class EmbeddingService:
    """
    向量化服务

    提供文本嵌入能力，支持外部 Embedding API 和本地 TF-IDF 降级。
    结果自动缓存到 EmbeddingCache 模型。
    """

    def __init__(self):
        self.api_url = os.environ.get("EMBEDDING_API_URL", "").strip()
        self.api_key = (
            os.environ.get("EMBEDDING_API_KEY", "")
            or os.environ.get("AI_ASSISTANT_API_KEY", "")
        ).strip()
        self.model = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small").strip()
        self.use_api = bool(self.api_url and self.api_key)
        if not self.use_api:
            logger.info("未配置 Embedding API，使用本地 TF-IDF 降级方案")

    def embed(self, text: str) -> List[float]:
        """获取文本的向量表示（带缓存）"""
        if not text or not text.strip():
            return []
        content_hash = _text_hash(text)
        cached = EmbeddingCache.query.filter_by(content_hash=content_hash).first()
        if cached:
            return json.loads(cached.embedding)

        if self.use_api:
            embedding = self._embed_via_api(text)
        else:
            embedding = self._embed_via_tfidf(text)

        if embedding:
            try:
                cache_entry = EmbeddingCache(
                    content_hash=content_hash,
                    feature="test_case",
                    model_name=self.model if self.use_api else "tfidf-local",
                    embedding=json.dumps(embedding),
                    content_preview=text[:200],
                )
                db.session.add(cache_entry)
                db.session.commit()
            except Exception as exc:
                db.session.rollback()
                logger.warning("嵌入缓存写入失败", error=str(exc))
        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量获取文本向量（带缓存）"""
        results = [None] * len(texts)
        hashes = [_text_hash(t) for t in texts]
        cached_entries = {
            e.content_hash: e
            for e in EmbeddingCache.query.filter(
                EmbeddingCache.content_hash.in_(hashes)
            ).all()
        }
        uncached_indices = []
        for i, (text, h) in enumerate(zip(texts, hashes)):
            if h in cached_entries:
                results[i] = json.loads(cached_entries[h].embedding)
            else:
                uncached_indices.append(i)

        if uncached_indices:
            uncached_texts = [texts[i] for i in uncached_indices]
            if self.use_api:
                new_embs = [self._embed_via_api(t) for t in uncached_texts]
            else:
                new_embs = [self._embed_via_tfidf(t) for t in uncached_texts]

            for idx, text, emb in zip(uncached_indices, uncached_texts, new_embs):
                results[idx] = emb
                if emb:
                    try:
                        h = _text_hash(text)
                        db.session.add(EmbeddingCache(
                            content_hash=h, feature="test_case",
                            model_name=self.model if self.use_api else "tfidf-local",
                            embedding=json.dumps(emb), content_preview=text[:200],
                        ))
                    except Exception:
                        pass
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
        return results

    def _embed_via_api(self, text: str) -> List[float]:
        """通过外部 API 获取嵌入向量"""
        import requests
        try:
            resp = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={"model": self.model, "input": text[:8000]},
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", [{}])[0].get("embedding", [])
            else:
                logger.warning("Embedding API 调用失败", status=resp.status_code)
                return self._embed_via_tfidf(text)
        except Exception as exc:
            logger.warning("Embedding API 异常，降级到 TF-IDF", error=str(exc))
            return self._embed_via_tfidf(text)

    def _embed_via_tfidf(self, text: str) -> List[float]:
        """本地 TF-IDF 嵌入（降级方案），维度 256"""
        dimension = 256
        vector = _tfidf_vector(text)
        dense = [0.0] * dimension
        for token, score in vector.items():
            h = int(hashlib.md5(token.encode()).hexdigest(), 16)
            idx = h % dimension
            sign = 1 if (h // dimension) % 2 == 0 else -1
            dense[idx] += sign * score
        norm = math.sqrt(sum(x * x for x in dense))
        if norm > 0:
            dense = [x / norm for x in dense]
        return dense


_service_instance = None


def get_embedding_service() -> EmbeddingService:
    """获取嵌入服务单例"""
    global _service_instance
    if _service_instance is None:
        _service_instance = EmbeddingService()
    return _service_instance
