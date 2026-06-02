"""
性能测试结果模型

存储完整的性能测试运行结果，支持时间序列数据
"""

from datetime import datetime
from ..extensions import db


class PerformanceTestResult(db.Model):
    """性能测试结果表 - 存储每次测试运行的汇总数据"""

    __tablename__ = 'performance_test_results'
    __table_args__ = (
        db.Index('idx_perf_results_scenario_id', 'scenario_id'),
        db.Index('idx_perf_results_project_id', 'project_id'),
        db.Index('idx_perf_results_created_at', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('perf_test_scenarios.id'), nullable=False, comment='关联的性能测试场景 ID')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, comment='项目 ID')

    # 测试运行配置快照
    user_count = db.Column(db.Integer, nullable=False, comment='并发用户数')
    spawn_rate = db.Column(db.Integer, nullable=False, comment='用户生成速率')
    duration = db.Column(db.Integer, nullable=False, comment='持续时间（秒）')
    target_url = db.Column(db.String(500), comment='目标 URL')

    # 运行状态
    status = db.Column(db.String(20), default='running', comment='状态: running/completed/failed/stopped')
    started_at = db.Column(db.DateTime, default=datetime.utcnow, comment='开始时间')
    finished_at = db.Column(db.DateTime, comment='结束时间')

    # 统计摘要（任务结束后计算）
    total_requests = db.Column(db.Integer, default=0, comment='总请求数')
    total_failures = db.Column(db.Integer, default=0, comment='失败请求数')
    error_rate = db.Column(db.Float, default=0.0, comment='错误率 (%)')
    rps = db.Column(db.Float, default=0.0, comment='最大 RPS')
    avg_response_time = db.Column(db.Float, comment='平均响应时间 (ms)')
    min_response_time = db.Column(db.Float, comment='最小响应时间 (ms)')
    max_response_time = db.Column(db.Float, comment='最大响应时间 (ms)')
    p50_response_time = db.Column(db.Float, comment='P50 响应时间 (ms)')
    p75_response_time = db.Column(db.Float, comment='P75 响应时间 (ms)')
    p95_response_time = db.Column(db.Float, comment='P95 响应时间 (ms)')
    p99_response_time = db.Column(db.Float, comment='P99 响应时间 (ms)')

    # 原始结果（完整 Locust 输出等）
    raw_result = db.Column(db.JSON, comment='原始结果 JSON')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    # 关联关系
    scenario = db.relationship('PerfTestScenario', backref=db.backref('test_results', cascade='all, delete-orphan'))
    project = db.relationship('Project', backref='perf_test_results')
    metric_samples = db.relationship('PerformanceMetricSample', backref='test_result', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'scenario_id': self.scenario_id,
            'project_id': self.project_id,
            'user_count': self.user_count,
            'spawn_rate': self.spawn_rate,
            'duration': self.duration,
            'target_url': self.target_url,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'total_requests': self.total_requests,
            'total_failures': self.total_failures,
            'error_rate': self.error_rate,
            'rps': self.rps,
            'avg_response_time': self.avg_response_time,
            'min_response_time': self.min_response_time,
            'max_response_time': self.max_response_time,
            'p50_response_time': self.p50_response_time,
            'p75_response_time': self.p75_response_time,
            'p95_response_time': self.p95_response_time,
            'p99_response_time': self.p99_response_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<PerformanceTestResult {self.id} scenario={self.scenario_id}>'


class PerformanceMetricSample(db.Model):
    """性能测试指标采样表 - 存储时间序列数据（每秒的 RPS、响应时间、错误率、并发用户数）"""

    __tablename__ = 'performance_metric_samples'
    __table_args__ = (
        db.Index('idx_perf_samples_result_id', 'test_result_id'),
        db.Index('idx_perf_samples_timestamp', 'timestamp'),
    )

    id = db.Column(db.Integer, primary_key=True)
    test_result_id = db.Column(db.Integer, db.ForeignKey('performance_test_results.id'), nullable=False, comment='关联的测试结果 ID')

    # 时间点
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='采样时间点')
    elapsed_seconds = db.Column(db.Integer, nullable=False, comment='自测试开始后的秒数')

    # 指标数据
    rps = db.Column(db.Float, default=0.0, comment='当前 RPS')
    active_users = db.Column(db.Integer, default=0, comment='当前活跃用户数')
    avg_response_time = db.Column(db.Float, comment='平均响应时间 (ms)')
    min_response_time = db.Column(db.Float, comment='最小响应时间 (ms)')
    max_response_time = db.Column(db.Float, comment='最大响应时间 (ms)')
    p95_response_time = db.Column(db.Float, comment='P95 响应时间 (ms)')
    p99_response_time = db.Column(db.Float, comment='P99 响应时间 (ms)')
    request_count = db.Column(db.Integer, default=0, comment='累计请求数')
    failure_count = db.Column(db.Integer, default=0, comment='累计失败数')
    error_rate = db.Column(db.Float, default=0.0, comment='当前错误率 (%)')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    def to_dict(self):
        return {
            'id': self.id,
            'test_result_id': self.test_result_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'elapsed_seconds': self.elapsed_seconds,
            'rps': self.rps,
            'active_users': self.active_users,
            'avg_response_time': self.avg_response_time,
            'min_response_time': self.min_response_time,
            'max_response_time': self.max_response_time,
            'p95_response_time': self.p95_response_time,
            'p99_response_time': self.p99_response_time,
            'request_count': self.request_count,
            'failure_count': self.failure_count,
            'error_rate': self.error_rate,
        }

    def __repr__(self):
        return f'<PerformanceMetricSample t={self.elapsed_seconds}s rps={self.rps}>'
