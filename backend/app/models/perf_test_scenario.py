"""
性能测试场景模型

存储 Locust 性能测试配置
"""

from datetime import datetime
from ..extensions import db


class PerfTestScenario(db.Model):
    """性能测试场景表"""
    
    __tablename__ = 'perf_test_scenarios'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True, comment='项目 ID')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户 ID')
    name = db.Column(db.String(255), nullable=False, comment='场景名称')
    description = db.Column(db.Text, comment='场景描述')
    
    # 请求配置
    target_url = db.Column(db.String(500), nullable=False, comment='目标 URL')
    method = db.Column(db.String(10), default='GET', comment='HTTP 方法')
    headers = db.Column(db.JSON, default=dict, comment='请求头')
    body = db.Column(db.JSON, comment='请求体')
    script_content = db.Column(db.Text, comment='Locust 脚本内容')
    
    # 负载配置
    user_count = db.Column(db.Integer, default=10, comment='并发用户数')
    spawn_rate = db.Column(db.Integer, default=1, comment='用户生成速率')
    duration = db.Column(db.Integer, default=60, comment='持续时间（秒）')
    ramp_up = db.Column(db.Integer, default=0, comment='爬坡时间（秒）')
    
    # 阶梯加压配置
    step_load_enabled = db.Column(db.Boolean, default=False, comment='是否启用阶梯加压')
    step_users = db.Column(db.Integer, default=10, comment='每步增加用户数')
    step_duration = db.Column(db.Integer, default=30, comment='每步持续时间')
    
    # 状态信息
    status = db.Column(db.String(20), default='pending', comment='当前状态: pending/running/completed/failed/stopped')
    last_run_at = db.Column(db.DateTime, comment='最后运行时间')
    last_result = db.Column(db.JSON, comment='最后执行结果')
    
    # 结果统计
    avg_response_time = db.Column(db.Float, comment='平均响应时间 (ms)')
    max_response_time = db.Column(db.Float, comment='最大响应时间 (ms)')
    min_response_time = db.Column(db.Float, comment='最小响应时间 (ms)')
    throughput = db.Column(db.Float, comment='吞吐量 (req/s)')
    error_rate = db.Column(db.Float, comment='错误率 (%)')
    
    # 其他配置
    tags = db.Column(db.JSON, default=list, comment='标签')
    is_enabled = db.Column(db.Boolean, default=True, comment='是否启用')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'target_url': self.target_url,
            'method': self.method,
            'headers': self.headers,
            'body': self.body,
            'script_content': self.script_content,
            'user_count': self.user_count,
            'spawn_rate': self.spawn_rate,
            'duration': self.duration,
            'ramp_up': self.ramp_up,
            'step_load_enabled': self.step_load_enabled,
            'step_users': self.step_users,
            'step_duration': self.step_duration,
            'status': self.status,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'last_result': self.last_result,
            'avg_response_time': self.avg_response_time,
            'max_response_time': self.max_response_time,
            'min_response_time': self.min_response_time,
            'throughput': self.throughput,
            'error_rate': self.error_rate,
            'tags': self.tags,
            'is_enabled': self.is_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<PerfTestScenario {self.name}>'
