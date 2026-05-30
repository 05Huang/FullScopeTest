"""
质量门禁模型

存储质量门禁规则配置和评估结果
"""

from datetime import datetime
from ..extensions import db


class QualityGate(db.Model):
    """质量门禁规则表"""

    __tablename__ = 'quality_gates'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目 ID')
    name = db.Column(db.String(100), nullable=False, comment='门禁名称')
    description = db.Column(db.Text, comment='门禁描述')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')

    # 通过率阈值
    min_pass_rate = db.Column(db.Float, default=100.0, comment='最小通过率 (%)')

    # P95 响应时间上限
    max_p95_response_time = db.Column(db.Float, comment='P95 响应时间上限 (ms)')

    # 视觉差异上限
    max_visual_diff_percentage = db.Column(db.Float, comment='视觉差异上限 (%)')

    # 创建者
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='创建者 ID')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    # 关联关系
    project = db.relationship('Project', backref='quality_gates')
    creator = db.relationship('User', backref='quality_gates')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'min_pass_rate': self.min_pass_rate,
            'max_p95_response_time': self.max_p95_response_time,
            'max_visual_diff_percentage': self.max_visual_diff_percentage,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<QualityGate {self.name}>'


class QualityGateEvaluation(db.Model):
    """质量门禁评估结果表"""

    __tablename__ = 'quality_gate_evaluations'

    id = db.Column(db.Integer, primary_key=True)
    quality_gate_id = db.Column(db.Integer, db.ForeignKey('quality_gates.id'), nullable=False, comment='质量门禁 ID')
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_runs.id'), nullable=False, comment='测试执行记录 ID')

    # 评估结果
    passed = db.Column(db.Boolean, nullable=False, comment='是否通过')
    evaluation_details = db.Column(db.JSON, default=dict, comment='评估详情')

    # GitHub Check Run 同步
    github_check_run_id = db.Column(db.Integer, comment='GitHub Check Run ID')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 关联关系
    quality_gate = db.relationship('QualityGate', backref='evaluations')
    test_run = db.relationship('TestRun', backref='quality_evaluations')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'quality_gate_id': self.quality_gate_id,
            'test_run_id': self.test_run_id,
            'passed': self.passed,
            'evaluation_details': self.evaluation_details,
            'github_check_run_id': self.github_check_run_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<QualityGateEvaluation gate={self.quality_gate_id} passed={self.passed}>'
