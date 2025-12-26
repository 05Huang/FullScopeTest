"""
接口测试用例模型

存储 API 测试集合和用例
"""

from datetime import datetime
from ..extensions import db


class ApiTestCollection(db.Model):
    """接口测试集合表"""
    
    __tablename__ = 'api_test_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, comment='项目 ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户 ID')
    parent_id = db.Column(db.Integer, db.ForeignKey('api_test_collections.id'), comment='父集合 ID')
    name = db.Column(db.String(100), nullable=False, comment='集合名称')
    description = db.Column(db.Text, comment='集合描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序顺序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 自引用关联（子集合）
    children = db.relationship('ApiTestCollection', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    # 测试用例关联
    test_cases = db.relationship('ApiTestCase', backref='collection', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_children=False, include_cases=False):
        """转换为字典"""
        result = {
            'id': self.id,
            'project_id': self.project_id,
            'parent_id': self.parent_id,
            'name': self.name,
            'description': self.description,
            'sort_order': self.sort_order,
            'case_count': self.test_cases.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_children:
            result['children'] = [c.to_dict() for c in self.children.all()]
        
        if include_cases:
            result['cases'] = [c.to_dict() for c in self.test_cases.all()]
        
        return result
    
    def __repr__(self):
        return f'<ApiTestCollection {self.name}>'


class ApiTestCase(db.Model):
    """接口测试用例表"""
    
    __tablename__ = 'api_test_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('api_test_collections.id'), nullable=True, comment='集合 ID')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, comment='项目 ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户 ID')
    environment_id = db.Column(db.Integer, db.ForeignKey('environments.id'), nullable=True, comment='关联环境 ID')
    name = db.Column(db.String(255), nullable=False, comment='用例名称')
    description = db.Column(db.Text, comment='用例描述')
    
    # HTTP 请求配置
    method = db.Column(db.String(10), nullable=False, default='GET', comment='HTTP 方法')
    url = db.Column(db.String(500), nullable=False, comment='请求 URL')
    headers = db.Column(db.JSON, default=dict, comment='请求头')
    params = db.Column(db.JSON, default=dict, comment='URL 查询参数')
    body = db.Column(db.JSON, comment='请求体')
    body_type = db.Column(db.String(20), default='json', comment='请求体类型: json/form/raw/binary')
    
    # 断言配置
    assertions = db.Column(db.JSON, default=list, comment='断言规则列表')
    
    # 脚本配置
    pre_script = db.Column(db.Text, comment='前置脚本')
    post_script = db.Column(db.Text, comment='后置脚本')
    
    # 变量配置
    variables = db.Column(db.JSON, default=dict, comment='用例级变量')
    extract_variables = db.Column(db.JSON, default=list, comment='响应提取变量')
    
    # 其他配置
    timeout = db.Column(db.Integer, default=30, comment='超时时间(秒)')
    retry_count = db.Column(db.Integer, default=0, comment='重试次数')
    tags = db.Column(db.JSON, default=list, comment='标签')
    priority = db.Column(db.Integer, default=2, comment='优先级: 1-高 2-中 3-低')
    is_enabled = db.Column(db.Boolean, default=True, comment='是否启用')
    sort_order = db.Column(db.Integer, default=0, comment='排序顺序')
    
    # 执行状态
    last_run_at = db.Column(db.DateTime, comment='最后执行时间')
    last_status = db.Column(db.String(20), comment='最后执行状态: passed/failed/pending')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'environment_id': self.environment_id,
            'name': self.name,
            'description': self.description,
            'method': self.method,
            'url': self.url,
            'headers': self.headers,
            'params': self.params,
            'body': self.body,
            'body_type': self.body_type,
            'assertions': self.assertions,
            'pre_script': self.pre_script,
            'post_script': self.post_script,
            'variables': self.variables,
            'extract_variables': self.extract_variables,
            'timeout': self.timeout,
            'retry_count': self.retry_count,
            'tags': self.tags,
            'priority': self.priority,
            'is_enabled': self.is_enabled,
            'sort_order': self.sort_order,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'last_status': self.last_status or 'pending',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ApiTestCase {self.method} {self.name}>'
