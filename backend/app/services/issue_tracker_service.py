"""
缺陷跟踪集成服务

支持 Jira 和飞书项目两种缺陷跟踪系统。
通过环境变量配置集成参数。

配置项：
- JIRA_BASE_URL: Jira 实例地址（如 https://your-domain.atlassian.net）
- JIRA_USER: Jira 用户邮箱
- JIRA_API_TOKEN: Jira API Token
- JIRA_PROJECT_KEY: 默认 Jira 项目 Key
- FEISHU_PROJECT_URL: 飞书项目 API 地址
- FEISHU_ACCESS_TOKEN: 飞书访问 Token

用法：
    # 手动创建 Jira Issue
    result = create_jira_issue(summary, description, project_key)

    # 测试失败时自动创建缺陷
    auto_create_issue_on_failure(test_run_id)
"""
import os
import time
import requests
from typing import Optional
from ..extensions import db
from ..models.issue_link import IssueLink
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)

# ── 重试配置 ──────────────────────────────────────────────────────────────────

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


# ── Jira 集成 ────────────────────────────────────────────────────────────────

def create_jira_issue(
    summary: str,
    description: str,
    project_key: str = None,
    issue_type: str = 'Bug',
    priority: str = 'Medium',
    labels: list = None,
) -> dict:
    """
    在 Jira 中创建 Issue

    Args:
        summary: Issue 标题
        description: 描述（支持 Jira 格式）
        project_key: 项目 Key（默认从环境变量读取）
        issue_type: Issue 类型（Bug/Task/Story）
        priority: 优先级（Highest/High/Medium/Low/Lowest）
        labels: 标签列表

    Returns:
        {success, issue_key, issue_url, error}
    """
    base_url = os.environ.get('JIRA_BASE_URL', '').rstrip('/')
    user = os.environ.get('JIRA_USER', '')
    token = os.environ.get('JIRA_API_TOKEN', '')
    project_key = project_key or os.environ.get('JIRA_PROJECT_KEY', '')

    if not all([base_url, user, token, project_key]):
        return {'success': False, 'error': 'Jira 配置不完整，请检查环境变量'}

    url = f'{base_url}/rest/api/2/issue'
    auth = (user, token)
    headers = {'Content-Type': 'application/json'}

    payload = {
        'fields': {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
            'priority': {'name': priority},
        },
    }
    if labels:
        payload['fields']['labels'] = labels

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, json=payload, auth=auth, headers=headers, timeout=30)
            if resp.status_code in (200, 201):
                data = resp.json()
                issue_key = data.get('key', '')
                issue_url = f'{base_url}/browse/{issue_key}'
                logger.info("Jira Issue 已创建", issue_key=issue_key, summary=summary)
                return {'success': True, 'issue_key': issue_key, 'issue_url': issue_url}

            logger.warning("Jira Issue 创建失败",
                           status=resp.status_code, body=resp.text[:200], attempt=attempt + 1)
        except requests.RequestException as exc:
            logger.warning("Jira 请求异常", error=str(exc), attempt=attempt + 1)

        if attempt < MAX_RETRIES - 1:
            time.sleep(INITIAL_RETRY_DELAY * (2 ** attempt))

    return {'success': False, 'error': 'Jira Issue 创建失败（重试耗尽）'}


def get_jira_issue_status(issue_key: str) -> dict:
    """
    查询 Jira Issue 状态

    Returns:
        {success, status, summary, error}
    """
    base_url = os.environ.get('JIRA_BASE_URL', '').rstrip('/')
    user = os.environ.get('JIRA_USER', '')
    token = os.environ.get('JIRA_API_TOKEN', '')

    if not all([base_url, user, token]):
        return {'success': False, 'error': 'Jira 配置不完整'}

    url = f'{base_url}/rest/api/2/issue/{issue_key}'

    try:
        resp = requests.get(url, auth=(user, token), timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return {
                'success': True,
                'status': data.get('fields', {}).get('status', {}).get('name', 'Unknown'),
                'summary': data.get('fields', {}).get('summary', ''),
            }
        return {'success': False, 'error': f'HTTP {resp.status_code}'}
    except requests.RequestException as exc:
        return {'success': False, 'error': str(exc)}


# ── 飞书集成 ──────────────────────────────────────────────────────────────────

def create_feishu_issue(
    summary: str,
    description: str,
    project_url: str = None,
    token: str = None,
) -> dict:
    """
    在飞书项目中创建任务

    飞书项目 API 参考：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/project-v2/task/create

    Args:
        summary: 任务标题
        description: 描述
        project_url: 飞书项目 API 地址
        token: 飞书访问 Token

    Returns:
        {success, issue_key, issue_url, error}
    """
    api_url = project_url or os.environ.get('FEISHU_PROJECT_URL', '')
    access_token = token or os.environ.get('FEISHU_ACCESS_TOKEN', '')

    if not all([api_url, access_token]):
        return {'success': False, 'error': '飞书配置不完整，请检查环境变量'}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    payload = {
        'summary': summary,
        'description': description,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(api_url, json=payload, headers=headers, timeout=30)
            if resp.status_code in (200, 201):
                data = resp.json()
                task_id = data.get('data', {}).get('id', '')
                logger.info("飞书任务已创建", task_id=task_id, summary=summary)
                return {
                    'success': True,
                    'issue_key': f'feishu-{task_id}',
                    'issue_url': data.get('data', {}).get('url', ''),
                }
            logger.warning("飞书任务创建失败", status=resp.status_code, attempt=attempt + 1)
        except requests.RequestException as exc:
            logger.warning("飞书请求异常", error=str(exc), attempt=attempt + 1)

        if attempt < MAX_RETRIES - 1:
            time.sleep(INITIAL_RETRY_DELAY * (2 ** attempt))

    return {'success': False, 'error': '飞书任务创建失败（重试耗尽）'}


# ── 统一接口 ──────────────────────────────────────────────────────────────────

def create_issue(
    tracker: str,
    summary: str,
    description: str,
    test_run_id: int = None,
    project_id: int = None,
    user_id: int = None,
    created_by: str = 'manual',
    **kwargs,
) -> dict:
    """
    统一缺陷创建接口

    Args:
        tracker: 跟踪系统（jira/feishu）
        summary: Issue 标题
        description: 描述
        test_run_id: 关联的 TestRun ID
        project_id: 项目 ID
        user_id: 操作者 ID（手动创建时）
        created_by: 创建方式（manual/auto）
        **kwargs: 传递给具体 tracker 的额外参数

    Returns:
        {success, issue_link, error}
    """
    # 调用对应的 tracker 创建 Issue
    if tracker == 'jira':
        result = create_jira_issue(summary, description, **kwargs)
    elif tracker == 'feishu':
        result = create_feishu_issue(summary, description, **kwargs)
    else:
        return {'success': False, 'error': f'不支持的缺陷跟踪系统: {tracker}'}

    if not result.get('success'):
        return result

    # 创建关联记录
    link = IssueLink(
        test_run_id=test_run_id,
        project_id=project_id,
        tracker=tracker,
        issue_key=result['issue_key'],
        issue_url=result.get('issue_url', ''),
        issue_title=summary,
        status='open',
        created_by=created_by,
        user_id=user_id,
    )

    db.session.add(link)
    db.session.commit()

    logger.info("缺陷关联已创建",
                tracker=tracker, issue_key=result['issue_key'],
                test_run_id=test_run_id, created_by=created_by)

    return {'success': True, 'issue_link': link.to_dict()}


def get_issue_links(test_run_id: int = None, project_id: int = None) -> list:
    """
    查询缺陷关联列表

    Args:
        test_run_id: 按 TestRun 过滤
        project_id: 按项目过滤

    Returns:
        IssueLink 字典列表
    """
    query = IssueLink.query
    if test_run_id is not None:
        query = query.filter_by(test_run_id=test_run_id)
    if project_id is not None:
        query = query.filter_by(project_id=project_id)

    links = query.order_by(IssueLink.created_at.desc()).all()
    return [l.to_dict() for l in links]


def refresh_issue_status(link_id: int) -> dict:
    """
    刷新缺陷关联的状态（从外部系统拉取最新状态）

    Args:
        link_id: IssueLink ID

    Returns:
        更新后的 IssueLink 字典
    """
    link = IssueLink.query.get(link_id)
    if not link:
        return None

    if link.tracker == 'jira':
        result = get_jira_issue_status(link.issue_key)
        if result.get('success'):
            link.status = _map_jira_status(result['status'])
            link.issue_title = result.get('summary', link.issue_title)
            db.session.commit()
    # 飞书状态刷新暂不实现（需要飞书 API 支持）

    return link.to_dict()


def auto_create_issue_on_failure(test_run_id: int, tracker: str = None) -> Optional[dict]:
    """
    测试失败时自动创建缺陷

    仅在配置了对应的缺陷跟踪系统时生效。

    Args:
        test_run_id: TestRun ID
        tracker: 指定跟踪系统（默认从环境变量读取）

    Returns:
        创建结果或 None（未配置时）
    """
    tracker = tracker or os.environ.get('DEFAULT_ISSUE_TRACKER', '')
    if not tracker:
        return None

    run = TestRun.query.get(test_run_id)
    if not run:
        return None

    summary = f'[自动化] 测试失败: {run.test_object_name or run.test_type}'
    description = (
        f'*测试执行失败*\n\n'
        f'- **项目 ID:** {run.project_id}\n'
        f'- **测试类型:** {run.test_type}\n'
        f'- **测试名称:** {run.test_object_name}\n'
        f'- **状态:** {run.status}\n'
        f'- **失败数:** {run.failed}\n'
        f'- **错误信息:** {run.error_message or "无"}\n'
        f'- **执行时间:** {run.created_at}\n'
    )

    return create_issue(
        tracker=tracker,
        summary=summary,
        description=description,
        test_run_id=test_run_id,
        project_id=run.project_id,
        created_by='auto',
    )


def _map_jira_status(jira_status: str) -> str:
    """将 Jira 状态映射到本地状态"""
    mapping = {
        'Open': 'open',
        'To Do': 'open',
        'In Progress': 'in_progress',
        'Done': 'resolved',
        'Resolved': 'resolved',
        'Closed': 'closed',
        'Won\'t Fix': 'closed',
    }
    return mapping.get(jira_status, 'open')