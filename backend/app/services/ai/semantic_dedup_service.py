"""
测试用例语义去重服务

将用例描述和步骤向量化，通过余弦相似度计算语义相似性，
返回相似度超过阈值的用例对，帮助用户发现和清理重复用例。

支持两种向量化方式：
1. 优先使用 OpenAI 兼容的 Embedding API（如 text-embedding-3-small）
2. 降级到基于 scikit-learn 的 TF-IDF 向量化（无需外部 API）
"""

import json
import math
import os
from typing import Dict, Any, List, Optional, Tuple

from ...extensions import db
from ...models.api_test_case import ApiTestCase
from ...core.logging import get_logger

logger = get_logger(__name__)


# ---- 文本提取 ----


def _extract_case_text(case: ApiTestCase) -> str:
    """从 ApiTestCase 提取用于语义比较的文本"""
    parts = []
    if case.name:
        parts.append(case.name)
    if case.description:
        parts.append(case.description)
    if case.method:
        parts.append(case.method)
    if case.url:
        parts.append(case.url)
    return ' '.join(parts)


# ---- 向量化：TF-IDF（本地降级方案） ----


def _tfidf_vectorize(texts: List[str]) -> List[List[float]]:
    """
    使用 TF-IDF 将文本列表转换为向量。
    降级方案：不依赖外部 Embedding API。
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

    vectorizer = TfidfVectorizer(max_features=1000, token_pattern=r'(?u)\b\w+\b')
    tfidf_matrix = vectorizer.fit_transform(texts)

    # 转为稠密列表
    return tfidf_matrix.toarray().tolist()


# ---- 向量化：Embedding API ----


def _embedding_api_vectorize(texts: List[str], config: Optional[Dict] = None) -> List[List[float]]:
    """
    使用 OpenAI 兼容的 Embedding API 获取文本向量。

    Args:
        texts: 文本列表
        config: 可选配置，包含 AI_EMBEDDING_BASE_URL / AI_EMBEDDING_API_KEY / AI_EMBEDDING_MODEL
    """
    import requests as req

    cfg = config or {}
    base_url = (
        cfg.get('AI_EMBEDDING_BASE_URL')
        or os.environ.get('AI_EMBEDDING_BASE_URL')
        or cfg.get('AI_ASSISTANT_BASE_URL')
        or os.environ.get('AI_ASSISTANT_BASE_URL')
        or 'https://api.openai.com/v1'
    ).rstrip('/')

    api_key = (
        cfg.get('AI_EMBEDDING_API_KEY')
        or os.environ.get('AI_EMBEDDING_API_KEY')
        or cfg.get('AI_ASSISTANT_API_KEY')
        or os.environ.get('AI_ASSISTANT_API_KEY')
        or ''
    ).strip()

    model = (
        cfg.get('AI_EMBEDDING_MODEL')
        or os.environ.get('AI_EMBEDDING_MODEL')
        or 'text-embedding-3-small'
    )

    if not api_key:
        raise ValueError('No API key available for embedding')

    endpoint = f'{base_url}/embeddings'

    # 分批处理（API 通常有 batch 限制）
    all_embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        resp = req.post(
            endpoint,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json={'model': model, 'input': batch},
            timeout=60,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f'Embedding API failed: HTTP {resp.status_code} {resp.text[:300]}')

        data = resp.json()
        # 按 index 排序确保顺序正确
        sorted_data = sorted(data.get('data', []), key=lambda x: x['index'])
        all_embeddings.extend([item['embedding'] for item in sorted_data])

    return all_embeddings


# ---- 余弦相似度 ----


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """计算两个向量的余弦相似度"""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def _cosine_similarity_matrix(vectors: List[List[float]]) -> List[List[float]]:
    """计算向量列表的余弦相似度矩阵"""
    n = len(vectors)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1.0
        for j in range(i + 1, n):
            sim = _cosine_similarity(vectors[i], vectors[j])
            matrix[i][j] = sim
            matrix[j][i] = sim
    return matrix


# ---- 主服务函数 ----


def find_duplicates(
    project_id: int,
    *,
    threshold: float = 0.85,
    case_type: str = 'api',
    config: Optional[Dict] = None,
    limit: int = 500,
) -> Dict[str, Any]:
    """
    在指定项目中查找语义相似的测试用例对。

    Args:
        project_id: 项目 ID
        threshold: 相似度阈值（默认 0.85）
        case_type: 用例类型 'api' / 'web'
        config: 可选 AI 配置
        limit: 最多分析的用例数量（防止超大项目性能问题）

    Returns:
        dict: {
            'total_cases': int,
            'duplicate_pairs': [
                {
                    'case_a': {...},
                    'case_b': {...},
                    'similarity': float,
                }
            ],
            'summary': {
                'total_pairs_checked': int,
                'duplicate_count': int,
                'method': str,
            }
        }
    """
    # 1. 获取用例
    if case_type == 'api':
        cases = ApiTestCase.query.filter_by(
            project_id=project_id,
            is_enabled=True,
        ).order_by(ApiTestCase.id).limit(limit).all()
    else:
        from ...models.web_test_script import WebTestScript
        cases = WebTestScript.query.filter_by(
            project_id=project_id,
        ).order_by(WebTestScript.id).limit(limit).all()

    if len(cases) < 2:
        return {
            'total_cases': len(cases),
            'duplicate_pairs': [],
            'summary': {
                'total_pairs_checked': 0,
                'duplicate_count': 0,
                'method': 'none',
            },
        }

    # 2. 提取文本
    texts = [_extract_case_text(c) for c in cases]
    # 过滤空文本
    valid_indices = [i for i, t in enumerate(texts) if t.strip()]
    if len(valid_indices) < 2:
        return {
            'total_cases': len(cases),
            'duplicate_pairs': [],
            'summary': {
                'total_pairs_checked': 0,
                'duplicate_count': 0,
                'method': 'none',
            },
        }

    valid_texts = [texts[i] for i in valid_indices]
    valid_cases = [cases[i] for i in valid_indices]

    # 3. 向量化
    method = 'tfidf'
    try:
        vectors = _embedding_api_vectorize(valid_texts, config=config)
        method = 'embedding_api'
        logger.info('Using embedding API for dedup', count=len(valid_texts))
    except Exception as exc:
        logger.warning(
            'Embedding API unavailable, falling back to TF-IDF',
            error=str(exc),
        )
        try:
            vectors = _tfidf_vectorize(valid_texts)
            method = 'tfidf'
        except ImportError:
            logger.error('scikit-learn not installed, cannot perform dedup')
            return {
                'total_cases': len(cases),
                'duplicate_pairs': [],
                'summary': {
                    'total_pairs_checked': 0,
                    'duplicate_count': 0,
                    'method': 'unavailable',
                    'error': 'Neither embedding API nor scikit-learn is available',
                },
            }

    # 4. 计算相似度矩阵并找出重复对
    sim_matrix = _cosine_similarity_matrix(vectors)

    duplicate_pairs = []
    total_pairs = 0
    n = len(valid_cases)

    for i in range(n):
        for j in range(i + 1, n):
            total_pairs += 1
            similarity = sim_matrix[i][j]
            if similarity >= threshold:
                case_a = valid_cases[i]
                case_b = valid_cases[j]

                pair = {
                    'case_a': {
                        'id': case_a.id,
                        'name': case_a.name,
                        'description': getattr(case_a, 'description', '') or '',
                        'method': getattr(case_a, 'method', ''),
                        'url': getattr(case_a, 'url', ''),
                    },
                    'case_b': {
                        'id': case_b.id,
                        'name': case_b.name,
                        'description': getattr(case_b, 'description', '') or '',
                        'method': getattr(case_b, 'method', ''),
                        'url': getattr(case_b, 'url', ''),
                    },
                    'similarity': round(similarity, 4),
                }
                duplicate_pairs.append(pair)

    # 按相似度降序排序
    duplicate_pairs.sort(key=lambda x: x['similarity'], reverse=True)

    logger.info(
        'Dedup scan completed',
        project_id=project_id,
        total_cases=len(cases),
        pairs_checked=total_pairs,
        duplicates_found=len(duplicate_pairs),
        method=method,
    )

    return {
        'total_cases': len(cases),
        'duplicate_pairs': duplicate_pairs,
        'summary': {
            'total_pairs_checked': total_pairs,
            'duplicate_count': len(duplicate_pairs),
            'method': method,
        },
    }


# 模块级单例
semantic_dedup_service = {
    'find_duplicates': find_duplicates,
}
