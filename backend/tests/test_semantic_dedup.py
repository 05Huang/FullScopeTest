"""
测试用例语义去重服务测试

测试 TF-IDF 向量化、余弦相似度计算、重复检测逻辑和 API 端点
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock


# ---- 辅助函数 ----


def _create_test_project(app):
    """在测试数据库中创建一个项目"""
    with app.app_context():
        from app.extensions import db
        from app.models.project import Project
        project = Project(name=f'dedup_test_{uuid.uuid4().hex[:8]}', description='test', owner_id=1)
        db.session.add(project)
        db.session.commit()
        return project.id


def _create_api_cases(app, project_id, user_id, cases_data):
    """批量创建 API 测试用例"""
    with app.app_context():
        from app.extensions import db
        from app.models.api_test_case import ApiTestCase
        created = []
        for data in cases_data:
            case = ApiTestCase(
                project_id=project_id,
                user_id=user_id,
                name=data['name'],
                description=data.get('description', ''),
                method=data.get('method', 'GET'),
                url=data.get('url', '/test'),
                is_enabled=True,
            )
            db.session.add(case)
            db.session.flush()
            created.append(case.id)
        db.session.commit()
        return created


def _auth_headers(client, app):
    """获取认证 headers"""
    import uuid as _uuid
    with app.app_context():
        from app.extensions import db
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        username = f'dedup_user_{_uuid.uuid4().hex[:8]}'
        user = User(
            username=username,
            email=f'{username}@test.com',
            password_hash=generate_password_hash('test123'),
            role='admin',
        )
        db.session.add(user)
        db.session.commit()
        uid = user.id

    resp = client.post('/api/v1/auth/login', json={'username': username, 'password': 'test123'})
    token = resp.get_json().get('data', {}).get('access_token', '')
    return {'Authorization': f'Bearer {token}'}, uid


# ---- TF-IDF 单元测试 ----


class TestTfidfVectorization:
    """TF-IDF 向量化测试"""

    def test_tfidf_basic(self):
        """测试基本 TF-IDF 向量化"""
        from app.services.ai.semantic_dedup_service import _tfidf_vectorize

        texts = [
            '获取用户列表 GET /api/users',
            '创建用户 POST /api/users',
            '获取用户列表 GET /api/users',
        ]
        vectors = _tfidf_vectorize(texts)

        assert len(vectors) == 3
        assert len(vectors[0]) > 0
        # 相同文本的向量应该相同
        assert vectors[0] == vectors[2]

    def test_tfidf_empty_text(self):
        """测试空文本处理"""
        from app.services.ai.semantic_dedup_service import _tfidf_vectorize

        texts = ['hello world', '', 'hello world']
        vectors = _tfidf_vectorize(texts)
        assert len(vectors) == 3


# ---- 余弦相似度测试 ----


class TestCosineSimilarity:
    """余弦相似度计算测试"""

    def test_identical_vectors(self):
        """测试相同向量的相似度为 1.0"""
        from app.services.ai.semantic_dedup_service import _cosine_similarity

        vec = [1.0, 2.0, 3.0]
        sim = _cosine_similarity(vec, vec)
        assert abs(sim - 1.0) < 1e-6

    def test_orthogonal_vectors(self):
        """测试正交向量的相似度为 0.0"""
        from app.services.ai.semantic_dedup_service import _cosine_similarity

        sim = _cosine_similarity([1.0, 0.0], [0.0, 1.0])
        assert abs(sim) < 1e-6

    def test_opposite_vectors(self):
        """测试反向向量的相似度为 -1.0"""
        from app.services.ai.semantic_dedup_service import _cosine_similarity

        sim = _cosine_similarity([1.0, 0.0], [-1.0, 0.0])
        assert abs(sim - (-1.0)) < 1e-6

    def test_empty_vectors(self):
        """测试空向量"""
        from app.services.ai.semantic_dedup_service import _cosine_similarity

        assert _cosine_similarity([], []) == 0.0
        assert _cosine_similarity([1.0], []) == 0.0

    def test_zero_vectors(self):
        """测试零向量"""
        from app.services.ai.semantic_dedup_service import _cosine_similarity

        assert _cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0


# ---- 文本提取测试 ----


class TestTextExtraction:
    """用例文本提取测试"""

    def test_extract_from_api_case(self):
        """测试从 ApiTestCase 提取文本"""
        from app.services.ai.semantic_dedup_service import _extract_case_text

        case = MagicMock()
        case.name = '获取用户列表'
        case.description = '获取所有用户的列表'
        case.method = 'GET'
        case.url = '/api/users'

        text = _extract_case_text(case)
        assert '获取用户列表' in text
        assert '获取所有用户的列表' in text
        assert 'GET' in text
        assert '/api/users' in text

    def test_extract_empty_case(self):
        """测试从空用例提取文本"""
        from app.services.ai.semantic_dedup_service import _extract_case_text

        case = MagicMock()
        case.name = None
        case.description = None
        case.method = None
        case.url = None

        text = _extract_case_text(case)
        assert text == ''


# ---- 去重服务集成测试 ----


class TestFindDuplicates:
    """去重服务集成测试"""

    def test_find_duplicates_few_cases(self, app, client):
        """测试用例数量不足时返回空结果"""
        from app.services.ai.semantic_dedup_service import find_duplicates

        project_id = _create_test_project(app)
        with app.app_context():
            result = find_duplicates(project_id, threshold=0.85)

            assert result['total_cases'] == 0
            assert result['duplicate_pairs'] == []
            assert result['summary']['duplicate_count'] == 0

    def test_find_duplicates_with_duplicates(self, app, client):
        """测试检测到重复用例"""
        from app.services.ai.semantic_dedup_service import find_duplicates

        project_id = _create_test_project(app)
        with app.app_context():
            from app.extensions import db
            from app.models.user import User
            user = User.query.first()
            user_id = user.id if user else 1

        _create_api_cases(app, project_id, user_id, [
            {'name': '获取用户列表', 'description': '获取所有用户', 'method': 'GET', 'url': '/api/users'},
            {'name': '获取所有用户列表', 'description': '获取用户列表', 'method': 'GET', 'url': '/api/users'},
            {'name': '创建用户', 'description': '创建一个新用户', 'method': 'POST', 'url': '/api/users'},
        ])

        with app.app_context():
            result = find_duplicates(project_id, threshold=0.5, config={'AI_ASSISTANT_API_KEY': ''})

            assert result['total_cases'] == 3
            assert result['summary']['total_pairs_checked'] == 3
            # 前两个用例应该高度相似
            if result['duplicate_pairs']:
                assert result['duplicate_pairs'][0]['similarity'] > 0.5

    def test_find_duplicates_no_duplicates(self, app, client):
        """测试没有重复用例的情况"""
        from app.services.ai.semantic_dedup_service import find_duplicates

        project_id = _create_test_project(app)
        with app.app_context():
            from app.extensions import db
            from app.models.user import User
            user = User.query.first()
            user_id = user.id if user else 1

        _create_api_cases(app, project_id, user_id, [
            {'name': '获取用户列表', 'description': '获取所有用户', 'method': 'GET', 'url': '/api/users'},
            {'name': '删除订单', 'description': '根据ID删除订单', 'method': 'DELETE', 'url': '/api/orders/{id}'},
            {'name': '上传文件', 'description': '上传图片文件到服务器', 'method': 'POST', 'url': '/api/upload'},
        ])

        with app.app_context():
            result = find_duplicates(project_id, threshold=0.95)

            assert result['total_cases'] == 3
            # 高阈值下不应有重复
            assert result['summary']['duplicate_count'] == 0

    def test_find_duplicates_custom_threshold(self, app, client):
        """测试自定义阈值"""
        from app.services.ai.semantic_dedup_service import find_duplicates

        project_id = _create_test_project(app)
        with app.app_context():
            from app.extensions import db
            from app.models.user import User
            user = User.query.first()
            user_id = user.id if user else 1

        _create_api_cases(app, project_id, user_id, [
            {'name': '获取用户', 'description': '获取用户信息', 'method': 'GET', 'url': '/api/users'},
            {'name': '查询用户', 'description': '查询用户详情', 'method': 'GET', 'url': '/api/users/{id}'},
        ])

        with app.app_context():
            # 低阈值应该找到更多
            result_low = find_duplicates(project_id, threshold=0.3, config={'AI_ASSISTANT_API_KEY': ''})
            # 高阈值应该找到更少
            result_high = find_duplicates(project_id, threshold=0.99, config={'AI_ASSISTANT_API_KEY': ''})

            assert result_low['summary']['duplicate_count'] >= result_high['summary']['duplicate_count']


# ---- API 端点测试 ----


class TestDedupApiEndpoint:
    """语义去重 API 端点测试"""

    def test_missing_project_id(self, client, app):
        """测试缺少 project_id 返回 400"""
        headers, _ = _auth_headers(client, app)
        resp = client.post('/api/v1/ai/find-duplicates', json={}, headers=headers)
        assert resp.status_code == 400

    def test_invalid_threshold(self, client, app):
        """测试无效阈值返回 400"""
        headers, _ = _auth_headers(client, app)
        resp = client.post('/api/v1/ai/find-duplicates', json={
            'project_id': 1,
            'threshold': 1.5,
        }, headers=headers)
        assert resp.status_code == 400

    def test_invalid_case_type(self, client, app):
        """测试无效 case_type 返回 400"""
        headers, _ = _auth_headers(client, app)
        resp = client.post('/api/v1/ai/find-duplicates', json={
            'project_id': 1,
            'case_type': 'invalid',
        }, headers=headers)
        assert resp.status_code == 400

    def test_successful_scan(self, client, app):
        """测试成功执行去重扫描"""
        headers, _ = _auth_headers(client, app)
        project_id = _create_test_project(app)

        resp = client.post('/api/v1/ai/find-duplicates', json={
            'project_id': project_id,
            'threshold': 0.85,
            'case_type': 'api',
        }, headers=headers)

        assert resp.status_code == 200
        data = resp.get_json()
        assert data['code'] == 200
        assert 'duplicate_pairs' in data['data']
        assert 'summary' in data['data']

    def test_scan_with_cases(self, client, app):
        """测试有测试用例时的扫描"""
        headers, uid = _auth_headers(client, app)
        project_id = _create_test_project(app)

        _create_api_cases(app, project_id, uid, [
            {'name': '获取用户列表', 'description': '获取所有用户', 'method': 'GET', 'url': '/api/users'},
            {'name': '查询所有用户', 'description': '查询用户列表', 'method': 'GET', 'url': '/api/users'},
        ])

        resp = client.post('/api/v1/ai/find-duplicates', json={
            'project_id': project_id,
            'threshold': 0.5,
            'case_type': 'api',
        }, headers=headers)

        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['total_cases'] == 2
