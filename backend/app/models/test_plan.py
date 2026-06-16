"""
测试计划模型

支持测试计划管理：计划 → 执行轮次 → 用例结果。
用于回归测试、迭代测试等场景的计划化管理。

TestPlan: 测试计划（包含用例列表、标签等元数据）
TestPlanRun: 执行轮次（从计划创建，记录每次执行的状态和结果）
TestPlanCaseResult: 单个用例在轮次中的执行结果
"""
from datetime import datetime
from ..extensions import db


class TestPlan(db.Model):
    """测试计划表"""

    __tablename__ = 'test_plans'
    __table_args__ = (
        db.Index('idx_test_plans_project_id', 'project_id'),
        db.Index('idx_test_plans_user_id', 'user_id'),
        db.Index('idx_test_plans_status', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目 ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='创建者 ID')
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, comment='组织 ID')

    name = db.Column(db.String(200), nullable=False, comment='计划名称')
    description = db.Column(db.Text, comment='计划描述')
    status = db.Column(db.String(20), default='draft', comment='状态: draft/active/archived')

    # 关联的用例 ID 列表
    include_cases = db.Column(db.JSON, default=list, comment='包含的用例 ID 列表 [{case_type, case_id}]')
    tags = db.Column(db.JSON, default=list, comment='标签')

    # 统计（冗余字段，通过轮次聚合更新）
    total_runs = db.Column(db.Integer, default=0, comment='总执行轮次数')
    last_run_at = db.Column(db.DateTime, comment='最后执行时间')
    last_pass_rate = db.Column(db.Float, comment='最后通过率')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    project = db.relationship('Project', backref='test_plans')
    user = db.relationship('User', backref='test_plans')
    organization = db.relationship('Organization', backref='test_plans')
    runs = db.relationship('TestPlanRun', backref='plan', lazy='dynamic', cascade='all, delete-orphan',
                           order_by='TestPlanRun.created_at.desc()')

    def to_dict(self, include_runs=False):
        result = {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'include_cases': self.include_cases or [],
            'tags': self.tags or [],
            'total_runs': self.total_runs,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'last_pass_rate': self.last_pass_rate,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_runs:
            result['runs'] = [r.to_dict() for r in self.runs.limit(20).all()]
        return result

    def __repr__(self):
        return f'<TestPlan {self.name} project={self.project_id}>'


class TestPlanRun(db.Model):
    """测试计划执行轮次表"""

    __tablename__ = 'test_plan_runs'
    __table_args__ = (
        db.Index('idx_test_plan_runs_plan_id', 'plan_id'),
        db.Index('idx_test_plan_runs_status', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('test_plans.id'), nullable=False, comment='计划 ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='执行者 ID')

    status = db.Column(db.String(20), default='pending', comment='状态: pending/running/completed/failed/cancelled')

    # 执行统计
    total_cases = db.Column(db.Integer, default=0, comment='总用例数')
    passed = db.Column(db.Integer, default=0, comment='通过数')
    failed = db.Column(db.Integer, default=0, comment='失败数')
    skipped = db.Column(db.Integer, default=0, comment='跳过数')
    error = db.Column(db.Integer, default=0, comment='错误数')
    pass_rate = db.Column(db.Float, default=0.0, comment='通过率（百分比）')

    # 时间
    started_at = db.Column(db.DateTime, comment='开始时间')
    finished_at = db.Column(db.DateTime, comment='结束时间')
    duration = db.Column(db.Float, comment='执行耗时(秒)')

    # 执行环境
    environment_id = db.Column(db.Integer, comment='执行环境 ID')
    environment_name = db.Column(db.String(100), comment='环境名称')

    # 备注
    notes = db.Column(db.Text, comment='轮次备注')

    # 触发方式
    triggered_by = db.Column(db.String(50), default='manual', comment='触发方式: manual/schedule/ci')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    user = db.relationship('User', backref='test_plan_runs')
    case_results = db.relationship('TestPlanCaseResult', backref='run', lazy='dynamic',
                                   cascade='all, delete-orphan')

    def to_dict(self, include_cases=False):
        result = {
            'id': self.id,
            'plan_id': self.plan_id,
            'user_id': self.user_id,
            'status': self.status,
            'total_cases': self.total_cases,
            'passed': self.passed,
            'failed': self.failed,
            'skipped': self.skipped,
            'error': self.error,
            'pass_rate': self.pass_rate,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'duration': self.duration,
            'environment_id': self.environment_id,
            'environment_name': self.environment_name,
            'notes': self.notes,
            'triggered_by': self.triggered_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_cases:
            result['case_results'] = [c.to_dict() for c in self.case_results.all()]
        return result

    def __repr__(self):
        return f'<TestPlanRun plan={self.plan_id} status={self.status}>'


class TestPlanCaseResult(db.Model):
    """测试计划用例执行结果表"""

    __tablename__ = 'test_plan_case_results'
    __table_args__ = (
        db.Index('idx_tp_case_results_run_id', 'run_id'),
        db.UniqueConstraint('run_id', 'case_type', 'case_id', name='uq_tp_case_result'),
    )

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('test_plan_runs.id'), nullable=False, comment='轮次 ID')

    # 用例标识（通用：支持 API/Web/Perf 等不同类型用例）
    case_type = db.Column(db.String(20), nullable=False, comment='用例类型: api/web/perf')
    case_id = db.Column(db.Integer, nullable=False, comment='用例 ID')
    case_name = db.Column(db.String(255), comment='用例名称（冗余，方便查询）')

    # 执行结果
    status = db.Column(db.String(20), default='pending', comment='状态: pending/passed/failed/skipped/error')
    duration = db.Column(db.Float, comment='执行耗时(秒)')
    error_message = db.Column(db.Text, comment='错误信息')
    result_detail = db.Column(db.JSON, comment='详细结果')

    # 关联到实际执行记录（可选）
    test_run_id = db.Column(db.Integer, comment='关联的 TestRun ID')

    executed_at = db.Column(db.DateTime, comment='执行时间')

    def to_dict(self):
        return {
            'id': self.id,
            'run_id': self.run_id,
            'case_type': self.case_type,
            'case_id': self.case_id,
            'case_name': self.case_name,
            'status': self.status,
            'duration': self.duration,
            'error_message': self.error_message,
            'result_detail': self.result_detail,
            'test_run_id': self.test_run_id,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
        }

    def __repr__(self):
        return f'<TestPlanCaseResult run={self.run_id} case={self.case_type}:{self.case_id}>'