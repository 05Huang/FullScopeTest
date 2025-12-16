"""
环境模型

存储测试环境配置
"""

from datetime import datetime
from ..extensions import db


class Environment(db.Model):
    """环境配置表"""
    
    __tablename__ = 'environments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目 ID')
    name = db.Column(db.String(50), nullable=False, comment='环境名称')
    base_url = db.Column(db.String(255), nullable=False, comment='基础 URL')
    variables = db.Column(db.JSON, default=dict, comment='环境变量')
    headers = db.Column(db.JSON, default=dict, comment='默认请求头')
    is_default = db.Column(db.Boolean, default=False, comment='是否默认环境')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'base_url': self.base_url,
            'variables': self.variables,
            'headers': self.headers,
            'is_default': self.is_default,
            'is_active': self.is_default,  # 前端使用的字段名
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Environment {self.name}>'
