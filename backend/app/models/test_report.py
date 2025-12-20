"""
测试报告模型

存储测试报告数据和生成信息
"""

from datetime import datetime
from ..extensions import db


class TestReport(db.Model):
    """测试报告表"""
    
    __tablename__ = 'test_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_runs.id'), nullable=False, comment='测试执行记录ID')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目ID')
    
    # 报告类型和标题
    test_type = db.Column(db.String(20), nullable=False, comment='测试类型: api/web/performance')
    title = db.Column(db.String(255), nullable=False, comment='报告标题')
    
    # 报告摘要
    summary = db.Column(db.JSON, default=dict, comment='报告摘要')
    
    # 报告详细数据
    report_data = db.Column(db.JSON, default=dict, comment='详细报告数据')
    
    # HTML 报告内容
    report_html = db.Column(db.Text, comment='HTML报告内容')
    
    # 状态
    status = db.Column(db.String(20), default='generated', comment='报告状态: generating/generated/failed')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联关系
    test_run = db.relationship('TestRun', backref='report', foreign_keys=[test_run_id])
    project = db.relationship('Project', backref='test_reports')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'project_id': self.project_id,
            'test_type': self.test_type,
            'title': self.title,
            'summary': self.summary,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_detail_dict(self):
        """转换为详细字典（包含报告数据）"""
        result = self.to_dict()
        result['report_data'] = self.report_data
        return result
    
    def __repr__(self):
        return f'<TestReport {self.title}>'
