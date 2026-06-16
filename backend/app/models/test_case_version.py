"""
用例版本历史模型

每次修改用例时自动保存前一版本的快照，支持版本查看和 diff 对比。

版本快照包含用例的完整字段（content JSON），以及变更摘要。
最多保留最近 N 个版本（可通过 MAX_VERSIONS 环境变量配置，默认 50）。
"""
import os
from datetime import datetime
from ..extensions import db

# 最大版本数（可配置）
MAX_VERSIONS = int(os.environ.get('MAX_VERSIONS', '50'))


class TestCaseVersion(db.Model):
    """用例版本历史表"""

    __tablename__ = 'test_case_versions'
    __table_args__ = (
        db.Index('idx_tc_versions_case', 'case_type', 'case_id'),
        db.Index('idx_tc_versions_created', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # 用例标识（通用：支持 API/Web 等不同类型）
    case_type = db.Column(db.String(20), nullable=False, comment='用例类型: api/web')
    case_id = db.Column(db.Integer, nullable=False, comment='用例 ID')
    version = db.Column(db.Integer, nullable=False, comment='版本号（从 1 开始递增）')

    # 版本快照（用例的完整字段）
    content = db.Column(db.JSON, nullable=False, comment='用例快照（完整字段 JSON）')

    # 变更信息
    change_summary = db.Column(db.String(500), comment='变更摘要')
    changed_fields = db.Column(db.JSON, default=list, comment='变更的字段列表')

    # 操作者
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, comment='修改者 ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='版本创建时间')

    # 关联
    user = db.relationship('User', backref='case_versions')

    def to_dict(self):
        return {
            'id': self.id,
            'case_type': self.case_type,
            'case_id': self.case_id,
            'version': self.version,
            'content': self.content,
            'change_summary': self.change_summary,
            'changed_fields': self.changed_fields or [],
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<TestCaseVersion {self.case_type}:{self.case_id} v{self.version}>'


def diff_versions(old_content: dict, new_content: dict) -> dict:
    """
    对比两个版本的内容差异

    Args:
        old_content: 旧版本内容
        new_content: 新版本内容

    Returns:
        {changed_fields: [field], diffs: {field: {old, new}}}
    """
    all_keys = set(list(old_content.keys()) + list(new_content.keys()))
    # 忽略时间戳字段
    ignore_keys = {'created_at', 'updated_at', 'last_run_at'}
    changed_fields = []
    diffs = {}

    for key in sorted(all_keys):
        if key in ignore_keys:
            continue
        old_val = old_content.get(key)
        new_val = new_content.get(key)
        if old_val != new_val:
            changed_fields.append(key)
            diffs[key] = {
                'old': old_val,
                'new': new_val,
            }

    return {
        'changed_fields': changed_fields,
        'diffs': diffs,
    }