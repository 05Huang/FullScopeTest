"""
评论与讨论系统测试

覆盖：评论 CRUD、@提及解析、软删除、权限控制、回复、分页
"""
import uuid


def _auth_headers(client, username=None):
    uid = uuid.uuid4().hex[:8]
    username = username or f"cmt_{uid}"
    password = "Passw0rd!"
    email = f"{username}@example.com"
    client.post("/api/v1/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    token = resp.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}, username


# ══════════════════════════════════════════════════════════════════════════════
# 一、评论 CRUD API 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCommentCRUD:
    """评论 CRUD 测试"""

    def test_create_comment(self, client, no_rate_limit):
        """创建评论"""
        headers, _ = _auth_headers(client)
        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
            "resource_id": 1,
            "content": "This is a **test** comment",
        })
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["content"] == "This is a **test** comment"
        assert data["resource_type"] == "test_case"
        assert data["resource_id"] == 1
        assert data["is_deleted"] is False

    def test_create_comment_empty_content(self, client, no_rate_limit):
        """空内容应返回 400"""
        headers, _ = _auth_headers(client)
        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
            "resource_id": 1,
            "content": "",
        })
        assert resp.status_code == 400

    def test_create_comment_invalid_resource_type(self, client, no_rate_limit):
        """无效资源类型应返回 400"""
        headers, _ = _auth_headers(client)
        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "invalid_type",
            "resource_id": 1,
            "content": "Test",
        })
        assert resp.status_code == 400

    def test_create_comment_missing_fields(self, client, no_rate_limit):
        """缺少必填字段应返回 400"""
        headers, _ = _auth_headers(client)
        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
        })
        assert resp.status_code == 400

    def test_list_comments(self, client, no_rate_limit):
        """获取评论列表"""
        headers, _ = _auth_headers(client)
        # 创建 2 条评论
        for i in range(2):
            client.post("/api/v1/comments", headers=headers, json={
                "resource_type": "test_run",
                "resource_id": 100,
                "content": f"Comment {i}",
            })
        resp = client.get("/api/v1/comments/test_run/100", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] >= 2

    def test_list_comments_empty(self, client, no_rate_limit):
        """没有评论时返回空列表"""
        headers, _ = _auth_headers(client)
        resp = client.get("/api/v1/comments/test_case/99999", headers=headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["total"] == 0
        assert data["items"] == []

    def test_get_comment_detail(self, client, no_rate_limit):
        """获取单条评论详情"""
        headers, _ = _auth_headers(client)
        create_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
            "resource_id": 1,
            "content": "Detail test",
        })
        comment_id = create_resp.get_json()["data"]["id"]

        resp = client.get(f"/api/v1/comments/{comment_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()["data"]["content"] == "Detail test"

    def test_get_comment_not_found(self, client, no_rate_limit):
        """获取不存在的评论应返回 404"""
        headers, _ = _auth_headers(client)
        resp = client.get("/api/v1/comments/99999", headers=headers)
        assert resp.status_code == 404

    def test_update_comment(self, client, no_rate_limit):
        """编辑评论"""
        headers, _ = _auth_headers(client)
        create_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
            "resource_id": 1,
            "content": "Original",
        })
        comment_id = create_resp.get_json()["data"]["id"]

        resp = client.put(f"/api/v1/comments/{comment_id}", headers=headers, json={
            "content": "Updated **content**",
        })
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert data["content"] == "Updated **content**"
        assert data["is_edited"] is True

    def test_update_comment_empty_content(self, client, no_rate_limit):
        """编辑为空内容应返回 400"""
        headers, _ = _auth_headers(client)
        create_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case", "resource_id": 1, "content": "Test",
        })
        comment_id = create_resp.get_json()["data"]["id"]

        resp = client.put(f"/api/v1/comments/{comment_id}", headers=headers, json={
            "content": "",
        })
        assert resp.status_code == 400

    def test_delete_comment(self, client, no_rate_limit):
        """软删除评论"""
        headers, _ = _auth_headers(client)
        create_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case", "resource_id": 1, "content": "To delete",
        })
        comment_id = create_resp.get_json()["data"]["id"]

        resp = client.delete(f"/api/v1/comments/{comment_id}", headers=headers)
        assert resp.status_code == 200

        # 获取详情应显示 [已删除]
        resp = client.get(f"/api/v1/comments/{comment_id}", headers=headers)
        assert resp.get_json()["data"]["is_deleted"] is True
        assert resp.get_json()["data"]["content"] == "[已删除]"

    def test_delete_comment_not_found(self, client, no_rate_limit):
        """删除不存在的评论应返回 404"""
        headers, _ = _auth_headers(client)
        resp = client.delete("/api/v1/comments/99999", headers=headers)
        assert resp.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 二、回复测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCommentReplies:
    """评论回复测试"""

    def test_create_reply(self, client, no_rate_limit):
        """创建回复"""
        headers, _ = _auth_headers(client)
        parent_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case", "resource_id": 2, "content": "Parent",
        })
        parent_id = parent_resp.get_json()["data"]["id"]

        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
            "resource_id": 2,
            "content": "Reply",
            "parent_id": parent_id,
        })
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["parent_id"] == parent_id

    def test_reply_to_nonexistent_parent(self, client, no_rate_limit):
        """回复不存在的父评论应返回 404"""
        headers, _ = _auth_headers(client)
        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case", "resource_id": 3,
            "content": "Reply", "parent_id": 99999,
        })
        assert resp.status_code == 404

    def test_list_comments_includes_replies(self, client, no_rate_limit):
        """评论列表应包含回复"""
        headers, _ = _auth_headers(client)
        parent_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_run", "resource_id": 200, "content": "Parent",
        })
        parent_id = parent_resp.get_json()["data"]["id"]
        client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_run", "resource_id": 200,
            "content": "Reply 1", "parent_id": parent_id,
        })

        resp = client.get("/api/v1/comments/test_run/200", headers=headers)
        data = resp.get_json()["data"]
        parent_comment = [c for c in data["items"] if c["id"] == parent_id]
        assert len(parent_comment) == 1
        assert len(parent_comment[0]["replies"]) >= 1

    def test_deleted_comment_not_in_list(self, client, no_rate_limit):
        """已删除的评论不应出现在列表中"""
        headers, _ = _auth_headers(client)
        create_resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case", "resource_id": 5, "content": "To hide",
        })
        comment_id = create_resp.get_json()["data"]["id"]
        client.delete(f"/api/v1/comments/{comment_id}", headers=headers)

        resp = client.get("/api/v1/comments/test_case/5", headers=headers)
        data = resp.get_json()["data"]
        ids = [c["id"] for c in data["items"]]
        assert comment_id not in ids


# ══════════════════════════════════════════════════════════════════════════════
# 三、@提及测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCommentMentions:
    """@提及测试"""

    def test_mention_parses_user_ids(self, client, no_rate_limit):
        """@提及应解析为用户 ID"""
        headers1, username1 = _auth_headers(client)
        headers2, username2 = _auth_headers(client)

        resp = client.post("/api/v1/comments", headers=headers1, json={
            "resource_type": "test_case",
            "resource_id": 10,
            "content": f"Hey @{username2}, please check this",
        })
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert len(data["mentions"]) >= 1

    def test_mention_nonexistent_user(self, client, no_rate_limit):
        """@提及不存在的用户应忽略"""
        headers, _ = _auth_headers(client)
        resp = client.post("/api/v1/comments", headers=headers, json={
            "resource_type": "test_case",
            "resource_id": 10,
            "content": "@nonexistent_user check this",
        })
        assert resp.status_code == 201
        data = resp.get_json()["data"]
        assert data["mentions"] == []


# ══════════════════════════════════════════════════════════════════════════════
# 四、Service 单元测试
# ══════════════════════════════════════════════════════════════════════════════

class TestCommentService:
    """CommentService 单元测试"""

    def test_extract_mentions(self, app):
        from app.services.comment_service import CommentService
        svc = CommentService()
        with app.app_context():
            mentions = svc._extract_mentions("Hello @alice and @bob")
            # alice/bob 可能不存在，所以返回空
            assert isinstance(mentions, list)

    def test_create_comment_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.comment_service import CommentService
        svc = CommentService()
        with app.app_context():
            user = User(username=f"cmt_{uuid.uuid4().hex[:6]}", email="cmt@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            comment = svc.create_comment(
                user_id=user.id,
                resource_type='test_case',
                resource_id=1,
                content='Service test comment',
            )
            assert comment['content'] == 'Service test comment'
            assert comment['user_id'] == user.id
            db.session.rollback()

    def test_soft_delete_service(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.comment_service import CommentService
        svc = CommentService()
        with app.app_context():
            user = User(username=f"cmt_{uuid.uuid4().hex[:6]}", email="cmt2@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()

            comment = svc.create_comment(
                user_id=user.id, resource_type='test_case',
                resource_id=1, content='To delete',
            )
            svc.delete_comment(comment['id'], user.id)

            detail = svc.get_comment(comment['id'])
            assert detail['is_deleted'] is True
            db.session.rollback()

    def test_update_comment_permission_check(self, app):
        from app.extensions import db
        from app.models.user import User
        from app.services.comment_service import CommentService
        from app.utils.exceptions import PermissionError
        svc = CommentService()
        with app.app_context():
            user1 = User(username=f"cmt_{uuid.uuid4().hex[:6]}", email="c1@test.com", password_hash="h")
            user2 = User(username=f"cmt_{uuid.uuid4().hex[:6]}", email="c2@test.com", password_hash="h")
            db.session.add_all([user1, user2])
            db.session.flush()

            comment = svc.create_comment(
                user_id=user1.id, resource_type='test_case',
                resource_id=1, content='Owned',
            )
            import pytest
            with pytest.raises(PermissionError):
                svc.update_comment(comment['id'], user2.id, 'Hacked')
            db.session.rollback()