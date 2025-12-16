"""
项目模型

存储测试项目信息
"""

from datetime import datetime
from ..extensions import db


class Project(db.Model):
    """项目表"""
    
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='项目名称')
    description = db.Column(db.Text, comment='项目描述')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='所有者 ID')
    settings = db.Column(db.JSON, default=dict, comment='项目设置')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联
    environments = db.relationship('Environment', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    api_collections = db.relationship('ApiTestCollection', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    web_scripts = db.relationship('WebTestScript', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    perf_scenarios = db.relationship('PerfTestScenario', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    test_runs = db.relationship('TestRun', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    documents = db.relationship('TestDocument', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'settings': self.settings,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # 统计信息
            'env_count': self.environments.count(),
            'api_collection_count': self.api_collections.count(),
            'web_script_count': self.web_scripts.count(),
            'perf_scenario_count': self.perf_scenarios.count()
        }
    
    def __repr__(self):
        return f'<Project {self.name}>'
