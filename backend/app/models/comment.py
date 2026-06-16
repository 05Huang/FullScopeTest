"""
评论与讨论模型

支持在用例、执行结果等资源上添加评论。
评论支持 Markdown 格式和 @提及用户。
"""
from datetime import datetime
from ..extensions import db


class Comment(db.Model):
    """评论表"""

    __tablename__ = 'comments'
    __table_args__ = (
        db.Index('idx_comments_resource', 'resource_type', 'resource_id'),
        db.Index('idx_comments_user_id', 'user_id'),
        db.Index('idx_comments_created_at', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # 关联的资源
    resource_type = db.Column(db.String(50), nullable=False, comment='资源类型: test_case/test_run/test_plan')
    resource_id = db.Column(db.Integer, nullable=False, comment='资源 ID')

    # 评论内容
    content = db.Column(db.Text, nullable=False, comment='评论内容（Markdown 格式）')

    # 操作者
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='评论者 ID')

    # @提及的用户 ID 列表
    mentions = db.Column(db.JSON, default=list, comment='@提及的用户 ID 列表')

    # 回复支持（简单实现：parent_id 引用父评论）
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True, comment='父评论 ID（回复）')

    # 编辑追踪
    is_edited = db.Column(db.Boolean, default=False, comment='是否被编辑过')
    edited_at = db.Column(db.DateTime, comment='最后编辑时间')

    # 软删除
    is_deleted = db.Column(db.Boolean, default=False, comment='是否已删除')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    user = db.relationship('User', backref='comments')
    parent = db.relationship('Comment', remote_side=[id], backref='replies')

    def to_dict(self, include_replies=False):
        result = {
            'id': self.id,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'content': self.content if not self.is_deleted else '[已删除]',
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'mentions': self.mentions or [],
            'parent_id': self.parent_id,
            'is_edited': self.is_edited,
            'edited_at': self.edited_at.isoformat() if self.edited_at else None,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_replies:
            result['replies'] = [r.to_dict() for r in self.replies if not r.is_deleted]
        return result

    def __repr__(self):
        return f'<Comment {self.resource_type}:{self.resource_id} by user {self.user_id}>'