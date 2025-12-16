"""
测试执行记录模型

存储测试运行记录和结果
"""

from datetime import datetime
from ..extensions import db


class TestRun(db.Model):
    """测试执行记录表"""
    
    __tablename__ = 'test_runs'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目 ID')
    
    # 测试类型
    test_type = db.Column(db.String(20), nullable=False, comment='测试类型: api/web/performance')
    
    # 关联的测试对象 ID（根据 test_type 对应不同表）
    test_object_id = db.Column(db.Integer, comment='测试对象 ID')
    test_object_name = db.Column(db.String(255), comment='测试对象名称')
    
    # 执行状态
    status = db.Column(db.String(20), default='pending', comment='状态: pending/running/success/failed/cancelled')
    
    # 执行统计
    total_cases = db.Column(db.Integer, default=0, comment='总用例数')
    passed = db.Column(db.Integer, default=0, comment='通过数')
    failed = db.Column(db.Integer, default=0, comment='失败数')
    skipped = db.Column(db.Integer, default=0, comment='跳过数')
    error = db.Column(db.Integer, default=0, comment='错误数')
    
    # 执行时间
    duration = db.Column(db.Float, comment='执行耗时(秒)')
    started_at = db.Column(db.DateTime, comment='开始时间')
    finished_at = db.Column(db.DateTime, comment='结束时间')
    
    # 执行环境
    environment_id = db.Column(db.Integer, comment='使用的环境 ID')
    environment_name = db.Column(db.String(50), comment='环境名称')
    
    # 执行结果详情
    results = db.Column(db.JSON, default=list, comment='执行结果详情')
    
    # 报告
    report_path = db.Column(db.String(500), comment='报告文件路径')
    allure_report_path = db.Column(db.String(500), comment='Allure 报告路径')
    
    # 触发方式
    triggered_by = db.Column(db.String(50), comment='触发方式: manual/schedule/ci')
    triggered_user_id = db.Column(db.Integer, comment='触发用户 ID')
    
    # 错误信息
    error_message = db.Column(db.Text, comment='错误信息')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'test_type': self.test_type,
            'test_object_id': self.test_object_id,
            'test_object_name': self.test_object_name,
            'status': self.status,
            'total_cases': self.total_cases,
            'passed': self.passed,
            'failed': self.failed,
            'skipped': self.skipped,
            'error': self.error,
            'pass_rate': round(self.passed / self.total_cases * 100, 2) if self.total_cases > 0 else 0,
            'duration': self.duration,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'environment_id': self.environment_id,
            'environment_name': self.environment_name,
            'report_path': self.report_path,
            'allure_report_path': self.allure_report_path,
            'triggered_by': self.triggered_by,
            'triggered_user_id': self.triggered_user_id,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<TestRun {self.id} {self.test_type} {self.status}>'
