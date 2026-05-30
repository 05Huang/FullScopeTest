"""
测试触发规则模型

定义基于 Git 事件自动触发测试的规则配置
"""

from datetime import datetime
from ..extensions import db


class TriggerRule(db.Model):
    """测试触发规则表"""
    
    __tablename__ = 'trigger_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目 ID')
    name = db.Column(db.String(100), nullable=False, comment='规则名称')
    description = db.Column(db.Text, comment='规则描述')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    
    # 触发条件
    trigger_event = db.Column(db.String(50), nullable=False, comment='触发事件: push, pull_request, tag')
    target_branches = db.Column(db.JSON, default=list, comment='目标分支列表，空列表表示匹配所有分支')
    target_tags = db.Column(db.JSON, default=list, comment='目标 tag 模式列表（支持通配符）')
    
    # 文件路径变更匹配
    include_paths = db.Column(db.JSON, default=list, comment='包含的文件路径模式（如 /api/**）')
    exclude_paths = db.Column(db.JSON, default=list, comment='排除的文件路径模式')
    
    # 测试类型过滤
    test_types = db.Column(db.JSON, default=list, comment='要运行的测试类型: api, web, perf')
    tags = db.Column(db.JSON, default=list, comment='要运行的测试标签')
    
    # 执行配置
    target_type = db.Column(db.String(50), nullable=False, comment='目标类型: api_collection, web_collection, perf_scenario')
    target_id = db.Column(db.Integer, nullable=True, comment='目标 ID（可选，为空则运行所有匹配的测试）')
    
    # 元数据
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='创建者 ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联关系
    project = db.relationship('Project', backref='trigger_rules')
    creator = db.relationship('User', backref='created_trigger_rules')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'trigger_event': self.trigger_event,
            'target_branches': self.target_branches,
            'target_tags': self.target_tags,
            'include_paths': self.include_paths,
            'exclude_paths': self.exclude_paths,
            'test_types': self.test_types,
            'tags': self.tags,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<TriggerRule {self.name} for project {self.project_id}>'
