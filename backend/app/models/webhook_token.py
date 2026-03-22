"""
Webhook 触发器模型
"""
import uuid
from datetime import datetime
from ..extensions import db

class WebhookToken(db.Model):
    """Webhook 触发器表"""
    
    __tablename__ = 'webhook_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目 ID')
    name = db.Column(db.String(100), nullable=False, comment='触发器名称')
    token = db.Column(db.String(100), unique=True, nullable=False, default=lambda: uuid.uuid4().hex, comment='唯一触发Token')
    target_type = db.Column(db.String(50), nullable=False, comment='目标类型: api_collection, web_collection, perf_scenario')
    target_id = db.Column(db.Integer, nullable=False, comment='目标 ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'token': self.token,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
