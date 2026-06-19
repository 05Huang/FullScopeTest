"""
评论服务

管理评论的 CRUD、@提及解析、软删除。
评论支持 Markdown 格式，编辑和删除仅限作者和管理员。
"""
import re
from datetime import datetime, timezone
from .base import BaseService
from ..extensions import db
from ..models.comment import Comment
from ..models.user import User
from ..utils.exceptions import NotFoundError, PermissionError, ValidationError
from ..core.logging import get_logger

logger = get_logger(__name__)

# @提及正则：匹配 @username 格式
MENTION_PATTERN = re.compile(r'@(\w+)')


class CommentService(BaseService):
    """评论服务"""

    def create_comment(self, user_id: int, resource_type: str, resource_id: int,
                       content: str, parent_id: int = None) -> dict:
        """
        创建评论

        Args:
            user_id: 评论者 ID
            resource_type: 资源类型
            resource_id: 资源 ID
            content: 评论内容（Markdown）
            parent_id: 父评论 ID（回复时）

        Returns:
            评论字典
        """
        if not content or not content.strip():
            raise ValidationError("评论内容不能为空")

        if resource_type not in ('test_case', 'test_run', 'test_plan'):
            raise ValidationError(f"不支持的资源类型: {resource_type}")

        # 解析 @提及
        mentions = self._extract_mentions(content)

        comment = Comment(
            resource_type=resource_type,
            resource_id=resource_id,
            content=content.strip(),
            user_id=user_id,
            mentions=mentions,
            parent_id=parent_id,
        )

        # 验证父评论存在且属于同一资源
        if parent_id:
            parent = Comment.query.get(parent_id)
            if not parent:
                raise NotFoundError("父评论", parent_id)
            if parent.resource_type != resource_type or parent.resource_id != resource_id:
                raise ValidationError("父评论不属于同一资源")

        with self.transaction():
            self.add(comment)

        logger.info("评论已创建",
                     comment_id=comment.id,
                     resource_type=resource_type,
                     resource_id=resource_id,
                     user_id=user_id,
                     mentions=mentions)
        return comment.to_dict()

    def get_comments(self, resource_type: str, resource_id: int,
                     page: int = 1, per_page: int = 50) -> dict:
        """
        获取资源的评论列表（仅顶层评论，回复内嵌）

        Args:
            resource_type: 资源类型
            resource_id: 资源 ID
            page: 页码
            per_page: 每页数量

        Returns:
            分页结果
        """
        query = Comment.query.filter_by(
            resource_type=resource_type,
            resource_id=resource_id,
            parent_id=None,  # 仅顶层评论
            is_deleted=False,
        )
        total = query.count()
        comments = query.order_by(Comment.created_at.asc()) \
            .offset((page - 1) * per_page) \
            .limit(per_page) \
            .all()

        return {
            'items': [c.to_dict(include_replies=True) for c in comments],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
        }

    def update_comment(self, comment_id: int, user_id: int, content: str,
                       is_admin: bool = False) -> dict:
        """
        编辑评论（仅作者可编辑）

        Args:
            comment_id: 评论 ID
            user_id: 操作者 ID
            content: 新内容
            is_admin: 是否为管理员

        Returns:
            更新后的评论字典
        """
        comment = Comment.query.get(comment_id)
        if not comment:
            raise NotFoundError("评论", comment_id)
        if comment.is_deleted:
            raise ValidationError("已删除的评论不可编辑")
        if comment.user_id != user_id and not is_admin:
            raise PermissionError("仅作者或管理员可编辑评论")

        if not content or not content.strip():
            raise ValidationError("评论内容不能为空")

        comment.content = content.strip()
        comment.is_edited = True
        comment.edited_at = datetime.now(timezone.utc).replace(tzinfo=None)
        comment.mentions = self._extract_mentions(content)

        with self.transaction():
            self.add(comment)

        return comment.to_dict()

    def delete_comment(self, comment_id: int, user_id: int,
                       is_admin: bool = False):
        """
        软删除评论（仅作者或管理员可删除）
        """
        comment = Comment.query.get(comment_id)
        if not comment:
            raise NotFoundError("评论", comment_id)
        if comment.is_deleted:
            return  # 已删除，幂等
        if comment.user_id != user_id and not is_admin:
            raise PermissionError("仅作者或管理员可删除评论")

        comment.is_deleted = True
        with self.transaction():
            self.add(comment)

        logger.info("评论已删除", comment_id=comment_id, user_id=user_id)

    def get_comment(self, comment_id: int) -> dict:
        """获取单条评论详情"""
        comment = Comment.query.get(comment_id)
        if not comment:
            raise NotFoundError("评论", comment_id)
        return comment.to_dict(include_replies=True)

    def _extract_mentions(self, content: str) -> list:
        """
        从评论内容中提取 @提及的用户名，转换为用户 ID

        Args:
            content: 评论内容

        Returns:
            提及的用户 ID 列表
        """
        usernames = MENTION_PATTERN.findall(content)
        if not usernames:
            return []

        user_ids = []
        for username in set(usernames):
            user = User.query.filter_by(username=username).first()
            if user:
                user_ids.append(user.id)
        return user_ids