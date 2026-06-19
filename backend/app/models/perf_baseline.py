"""
性能测试基线模型

存储性能测试基线数据，用于退化检测。
"""

from datetime import datetime, timezone
from ..extensions import db


class PerfBaseline(db.Model):
    """性能测试基线表"""

    __tablename__ = "perf_baselines"
    __table_args__ = (
        db.Index("idx_perf_baselines_scenario", "scenario_id"),
        db.Index("idx_perf_baselines_active", "is_active"),
    )

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, nullable=False, comment="场景 ID")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, comment="创建者")
    name = db.Column(db.String(200), nullable=False, comment="基线名称")
    is_active = db.Column(db.Boolean, default=True, comment="是否为当前活跃基线")
    metrics = db.Column(db.JSON, nullable=False, comment="基线指标 {p50, p90, p95, p99, avg, throughput, error_rate}"
    run_id = db.Column(db.Integer, comment="关联的测试运行 ID")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def to_dict(self):
        return {
            "id": self.id,
            "scenario_id": self.scenario_id,
            "name": self.name,
            "is_active": self.is_active,
            "metrics": self.metrics,
            "run_id": self.run_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

