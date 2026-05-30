"""
触发规则服务

实现测试触发规则引擎：
- 配置规则「当 PR 目标分支为 main 时，运行标签为 regression 的测试套件」
- 支持「文件路径变更匹配」（如 /api/** 变更时只运行接口测试）
- 规则配置 CRUD API
"""

import fnmatch
from typing import Dict, Any, List, Optional
from ..extensions import db
from ..models.trigger_rule import TriggerRule
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)


def evaluate_push_event(
    ref: str,
    changed_files: List[str],
    commit_message: str,
    repository: str,
    project_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    评估 push 事件是否应该触发测试

    Args:
        ref: Git ref（如 refs/heads/main）
        changed_files: 变更的文件列表
        commit_message: 提交信息
        repository: 仓库全名
        project_id: 可选的项目 ID，用于过滤规则

    Returns:
        dict: 包含 should_trigger, test_type, target_id, matched_rules 等信息
    """
    # 从 ref 提取分支名
    branch = ref.replace('refs/heads/', '') if ref.startswith('refs/heads/') else ref

    # 获取所有激活的 push 规则
    query = TriggerRule.query.filter_by(
        trigger_event='push',
        is_active=True,
    )
    if project_id:
        query = query.filter_by(project_id=project_id)

    rules = query.all()

    matched_rules = []

    for rule in rules:
        if _matches_push_rule(rule, branch, changed_files, commit_message):
            matched_rules.append(rule)

    if not matched_rules:
        return {
            'should_trigger': False,
            'reason': 'No matching rules found for push event',
        }

    # 合并所有匹配规则的测试配置
    all_test_types = set()
    all_target_ids = set()

    for rule in matched_rules:
        if rule.test_types:
            all_test_types.update(rule.test_types)
        if rule.target_id:
            all_target_ids.add(rule.target_id)

    return {
        'should_trigger': True,
        'test_type': list(all_test_types)[0] if len(all_test_types) == 1 else 'api',
        'target_id': list(all_target_ids)[0] if len(all_target_ids) == 1 else None,
        'matched_rules': [r.to_dict() for r in matched_rules],
        'test_types': list(all_test_types),
        'target_ids': list(all_target_ids),
    }


def evaluate_pr_event(
    action: str,
    head_branch: str,
    base_branch: str,
    pr_number: int,
    pr_title: str,
    repository: str,
    changed_files: List[str],
) -> Dict[str, Any]:
    """
    评估 pull_request 事件是否应该触发测试

    Args:
        action: PR 动作（opened, synchronize, closed）
        head_branch: 源分支
        base_branch: 目标分支
        pr_number: PR 编号
        pr_title: PR 标题
        repository: 仓库全名
        changed_files: 变更的文件列表

    Returns:
        dict: 包含 should_trigger, test_type, target_id, matched_rules 等信息
    """
    # 获取所有激活的 pull_request 规则
    rules = TriggerRule.query.filter_by(
        trigger_event='pull_request',
        is_active=True,
    ).all()

    matched_rules = []

    for rule in rules:
        if _matches_pr_rule(rule, action, head_branch, base_branch, pr_title, changed_files):
            matched_rules.append(rule)

    if not matched_rules:
        return {
            'should_trigger': False,
            'reason': 'No matching rules found for pull_request event',
        }

    # 合并所有匹配规则的测试配置
    all_test_types = set()
    all_target_ids = set()

    for rule in matched_rules:
        if rule.test_types:
            all_test_types.update(rule.test_types)
        if rule.target_id:
            all_target_ids.add(rule.target_id)

    return {
        'should_trigger': True,
        'test_type': list(all_test_types)[0] if len(all_test_types) == 1 else 'api',
        'target_id': list(all_target_ids)[0] if len(all_target_ids) == 1 else None,
        'matched_rules': [r.to_dict() for r in matched_rules],
        'test_types': list(all_test_types),
        'target_ids': list(all_target_ids),
    }


def _matches_push_rule(
    rule: TriggerRule,
    branch: str,
    changed_files: List[str],
    commit_message: str,
) -> bool:
    """
    检查 push 事件是否匹配给定规则

    Args:
        rule: 触发规则
        branch: 目标分支
        changed_files: 变更的文件列表
        commit_message: 提交信息

    Returns:
        bool: 是否匹配
    """
    # 检查分支匹配
    if rule.target_branches:
        branch_matched = False
        for pattern in rule.target_branches:
            if fnmatch.fnmatch(branch, pattern):
                branch_matched = True
                break
        if not branch_matched:
            return False

    # 检查文件路径匹配
    if rule.include_paths:
        file_matched = False
        for file_path in changed_files:
            for pattern in rule.include_paths:
                if fnmatch.fnmatch(file_path, pattern):
                    file_matched = True
                    break
            if file_matched:
                break
        if not file_matched:
            return False

    # 检查排除路径
    if rule.exclude_paths:
        for file_path in changed_files:
            for pattern in rule.exclude_paths:
                if fnmatch.fnmatch(file_path, pattern):
                    return False

    return True


def _matches_pr_rule(
    rule: TriggerRule,
    action: str,
    head_branch: str,
    base_branch: str,
    pr_title: str,
    changed_files: List[str],
) -> bool:
    """
    检查 pull_request 事件是否匹配给定规则

    Args:
        rule: 触发规则
        action: PR 动作
        head_branch: 源分支
        base_branch: 目标分支
        pr_title: PR 标题
        changed_files: 变更的文件列表

    Returns:
        bool: 是否匹配
    """
    # 检查目标分支匹配
    if rule.target_branches:
        branch_matched = False
        for pattern in rule.target_branches:
            if fnmatch.fnmatch(base_branch, pattern):
                branch_matched = True
                break
        if not branch_matched:
            return False

    # 检查文件路径匹配
    if rule.include_paths:
        file_matched = False
        for file_path in changed_files:
            for pattern in rule.include_paths:
                if fnmatch.fnmatch(file_path, pattern):
                    file_matched = True
                    break
            if file_matched:
                break
        if not file_matched:
            return False

    # 检查排除路径
    if rule.exclude_paths:
        for file_path in changed_files:
            for pattern in rule.exclude_paths:
                if fnmatch.fnmatch(file_path, pattern):
                    return False

    return True


# ==================== CRUD 操作 ====================

def create_rule(
    project_id: int,
    name: str,
    trigger_event: str,
    target_type: str,
    description: Optional[str] = None,
    target_branches: Optional[List[str]] = None,
    target_tags: Optional[List[str]] = None,
    include_paths: Optional[List[str]] = None,
    exclude_paths: Optional[List[str]] = None,
    test_types: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    target_id: Optional[int] = None,
    created_by: Optional[int] = None,
) -> TriggerRule:
    """
    创建触发规则

    Args:
        project_id: 项目 ID
        name: 规则名称
        trigger_event: 触发事件类型
        target_type: 目标类型
        description: 规则描述
        target_branches: 目标分支列表
        target_tags: 目标 tag 列表
        include_paths: 包含的文件路径模式
        exclude_paths: 排除的文件路径模式
        test_types: 测试类型列表
        tags: 测试标签列表
        target_id: 目标 ID
        created_by: 创建者 ID

    Returns:
        TriggerRule: 创建的规则
    """
    rule = TriggerRule(
        project_id=project_id,
        name=name,
        description=description,
        trigger_event=trigger_event,
        target_branches=target_branches or [],
        target_tags=target_tags or [],
        include_paths=include_paths or [],
        exclude_paths=exclude_paths or [],
        test_types=test_types or [],
        tags=tags or [],
        target_type=target_type,
        target_id=target_id,
        created_by=created_by,
    )

    db.session.add(rule)
    db.session.commit()

    logger.info('Trigger rule created', rule_id=rule.id, name=name, trigger_event=trigger_event)
    return rule


def update_rule(
    rule_id: int,
    **kwargs,
) -> Optional[TriggerRule]:
    """
    更新触发规则

    Args:
        rule_id: 规则 ID
        **kwargs: 要更新的字段

    Returns:
        TriggerRule: 更新后的规则，如果不存在则返回 None
    """
    rule = TriggerRule.query.get(rule_id)
    if not rule:
        return None

    for key, value in kwargs.items():
        if hasattr(rule, key):
            setattr(rule, key, value)

    db.session.commit()
    logger.info('Trigger rule updated', rule_id=rule_id)
    return rule


def delete_rule(rule_id: int) -> bool:
    """
    删除触发规则

    Args:
        rule_id: 规则 ID

    Returns:
        bool: 是否成功删除
    """
    rule = TriggerRule.query.get(rule_id)
    if not rule:
        return False

    db.session.delete(rule)
    db.session.commit()
    logger.info('Trigger rule deleted', rule_id=rule_id)
    return True


def get_rules_by_project(project_id: int) -> List[TriggerRule]:
    """
    获取项目的所有触发规则

    Args:
        project_id: 项目 ID

    Returns:
        List[TriggerRule]: 规则列表
    """
    return TriggerRule.query.filter_by(project_id=project_id).order_by(
        TriggerRule.created_at.desc()
    ).all()


def get_active_rules_by_project(project_id: int) -> List[TriggerRule]:
    """
    获取项目的所有激活的触发规则

    Args:
        project_id: 项目 ID

    Returns:
        List[TriggerRule]: 规则列表
    """
    return TriggerRule.query.filter_by(
        project_id=project_id,
        is_active=True,
    ).order_by(TriggerRule.created_at.desc()).all()