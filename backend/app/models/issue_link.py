"""
缺陷关联模型

将测试执行结果与外部缺陷跟踪系统（Jira/飞书）的 Issue 关联起来。
支持手动和自动两种创建模式。
"""
from datetime import datetime
from ..extensions import db


class IssueLink(db.Model):
    """缺陷关联表"""

    __tablename__ = 'issue_links'
    __table_args__ = (
        db.Index('idx_issue_links_test_run_id', 'test_run_id'),
        db.Index('idx_issue_links_tracker', 'tracker'),
        db.Index('idx_issue_links_status', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # 关联的测试执行记录
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_runs.id'), nullable=True, comment='关联的 TestRun ID')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, comment='项目 ID')

    # 外部缺陷信息
    tracker = db.Column(db.String(20), nullable=False, comment='缺陷跟踪系统: jira/feishu')
    issue_key = db.Column(db.String(100), nullable=False, comment='外部 Issue Key（如 PROJ-123）')
    issue_url = db.Column(db.String(500), comment='外部 Issue 链接')
    issue_title = db.Column(db.String(500), comment='Issue 标题')
    status = db.Column(db.String(50), default='open', comment='缺陷状态: open/in_progress/resolved/closed')

    # 创建方式
    created_by = db.Column(db.String(20), default='manual', comment='创建方式: manual/auto')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, comment='手动创建时的操作者')

    # 附加数据
    extra = db.Column(db.JSON, default=dict, comment='附加数据')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    test_run = db.relationship('TestRun', backref='issue_links')
    project = db.relationship('Project', backref='issue_links')
    user = db.relationship('User', backref='issue_links')

    def to_dict(self):
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'project_id': self.project_id,
            'tracker': self.tracker,
            'issue_key': self.issue_key,
            'issue_url': self.issue_url,
            'issue_title': self.issue_title,
            'status': self.status,
            'created_by': self.created_by,
            'user_id': self.user_id,
            'extra': self.extra,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<IssueLink {self.tracker}:{self.issue_key} run={self.test_run_id}>'