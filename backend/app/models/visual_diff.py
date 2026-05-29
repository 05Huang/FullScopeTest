"""
视觉回归测试差异记录模型

存储测试截图与基准截图的差异对比结果
"""

from datetime import datetime
from ..extensions import db


class VisualDiff(db.Model):
    """视觉回归差异记录表"""

    __tablename__ = 'visual_diffs'
    __table_args__ = (
        db.Index('idx_visual_diffs_test_run_id', 'test_run_id'),
        db.Index('idx_visual_diffs_baseline_id', 'baseline_id'),
        db.Index('idx_visual_diffs_test_case_id', 'test_case_id'),
        db.Index('idx_visual_diffs_status', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_runs.id'), nullable=False, comment='关联的测试执行记录 ID')
    baseline_id = db.Column(db.Integer, db.ForeignKey('visual_baselines.id'), nullable=True, comment='关联的基准截图 ID')
    test_case_id = db.Column(db.Integer, nullable=False, comment='关联的测试用例 ID')
    test_type = db.Column(db.String(20), nullable=False, comment='测试类型: api/web/app')

    # 截图对比信息
    step_index = db.Column(db.Integer, nullable=False, comment='测试步骤索引')
    step_name = db.Column(db.String(255), comment='测试步骤名称')
    current_image_path = db.Column(db.String(500), nullable=False, comment='当前截图存储路径')
    diff_image_path = db.Column(db.String(500), comment='差异标注图存储路径')

    # 差异分析结果
    diff_percentage = db.Column(db.Float, nullable=False, default=0.0, comment='差异百分比 (0-100)')
    diff_pixel_count = db.Column(db.Integer, default=0, comment='差异像素数量')
    total_pixel_count = db.Column(db.Integer, default=0, comment='总像素数量')
    similarity_score = db.Column(db.Float, comment='感知哈希相似度 (0-1)')

    # 截图元数据
    viewport_width = db.Column(db.Integer, comment='视口宽度')
    viewport_height = db.Column(db.Integer, comment='视口高度')

    # 对比配置
    threshold = db.Column(db.Float, default=5.0, comment='差异阈值 (%)，超过则判定为视觉失败')

    # 状态
    status = db.Column(db.String(20), default='pending', comment='状态: pending/visual_pass/visual_fail/approved/rejected')
    is_baseline_current = db.Column(db.Boolean, default=True, comment='基准截图是否为最新版本')

    # 审核信息
    reviewed_by = db.Column(db.Integer, comment='审核人用户 ID')
    reviewed_at = db.Column(db.DateTime, comment='审核时间')
    review_comment = db.Column(db.Text, comment='审核备注')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    # 关联关系
    test_run = db.relationship('TestRun', backref='visual_diffs')
    baseline = db.relationship('VisualBaseline', backref='diffs')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'test_run_id': self.test_run_id,
            'baseline_id': self.baseline_id,
            'test_case_id': self.test_case_id,
            'test_type': self.test_type,
            'step_index': self.step_index,
            'step_name': self.step_name,
            'current_image_path': self.current_image_path,
            'diff_image_path': self.diff_image_path,
            'diff_percentage': self.diff_percentage,
            'diff_pixel_count': self.diff_pixel_count,
            'total_pixel_count': self.total_pixel_count,
            'similarity_score': self.similarity_score,
            'viewport_width': self.viewport_width,
            'viewport_height': self.viewport_height,
            'threshold': self.threshold,
            'status': self.status,
            'is_baseline_current': self.is_baseline_current,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'review_comment': self.review_comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<VisualDiff {self.test_case_id} step:{self.step_index} diff:{self.diff_percentage}%>'
