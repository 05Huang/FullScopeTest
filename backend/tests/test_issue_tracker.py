"""
缺陷跟踪集成测试

覆盖：Jira/飞书 Issue 创建、统一接口、关联查询、状态刷新、
     自动创建、错误处理、重试机制
"""
import uuid
from unittest.mock import patch, MagicMock


# ══════════════════════════════════════════════════════════════════════════════
# 一、Jira 集成测试
# ══════════════════════════════════════════════════════════════════════════════

class TestJiraIntegration:
    """Jira Issue 创建测试"""

    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_USER': 'test@example.com',
        'JIRA_API_TOKEN': 'token123',
        'JIRA_PROJECT_KEY': 'TEST',
    })
    @patch('app.services.issue_tracker_service.requests.post')
    def test_create_jira_issue_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {'key': 'TEST-123'}
        mock_post.return_value = mock_resp

        from app.services.issue_tracker_service import create_jira_issue
        result = create_jira_issue('Bug Title', 'Bug Description')
        assert result['success'] is True
        assert result['issue_key'] == 'TEST-123'
        assert 'TEST-123' in result['issue_url']

    @patch.dict('os.environ', {}, clear=True)
    def test_create_jira_issue_missing_config(self):
        from app.services.issue_tracker_service import create_jira_issue
        # 清除 Jira 相关环境变量
        import os
        for key in ['JIRA_BASE_URL', 'JIRA_USER', 'JIRA_API_TOKEN', 'JIRA_PROJECT_KEY']:
            os.environ.pop(key, None)
        result = create_jira_issue('Title', 'Desc')
        assert result['success'] is False
        assert '配置不完整' in result['error']

    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_USER': 'test@example.com',
        'JIRA_API_TOKEN': 'token123',
        'JIRA_PROJECT_KEY': 'TEST',
    })
    @patch('app.services.issue_tracker_service.requests.post')
    def test_create_jira_issue_retry_on_failure(self, mock_post):
        import requests as req_lib
        fail_resp = MagicMock()
        fail_resp.status_code = 500
        fail_resp.text = 'Internal Server Error'
        ok_resp = MagicMock()
        ok_resp.status_code = 201
        ok_resp.json.return_value = {'key': 'TEST-456'}
        mock_post.side_effect = [fail_resp, ok_resp]

        from app.services.issue_tracker_service import create_jira_issue
        with patch('app.services.issue_tracker_service.time.sleep'):
            result = create_jira_issue('Retry Title', 'Desc')
        assert result['success'] is True
        assert result['issue_key'] == 'TEST-456'

    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_USER': 'test@example.com',
        'JIRA_API_TOKEN': 'token123',
        'JIRA_PROJECT_KEY': 'TEST',
    })
    @patch('app.services.issue_tracker_service.requests.get')
    def test_get_jira_issue_status(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'fields': {
                'status': {'name': 'In Progress'},
                'summary': 'Test Bug',
            },
        }
        mock_get.return_value = mock_resp

        from app.services.issue_tracker_service import get_jira_issue_status
        result = get_jira_issue_status('TEST-123')
        assert result['success'] is True
        assert result['status'] == 'In Progress'
        assert result['summary'] == 'Test Bug'


# ══════════════════════════════════════════════════════════════════════════════
# 二、飞书集成测试
# ══════════════════════════════════════════════════════════════════════════════

class TestFeishuIntegration:
    """飞书任务创建测试"""

    @patch.dict('os.environ', {
        'FEISHU_PROJECT_URL': 'https://open.feishu.cn/api/task',
        'FEISHU_ACCESS_TOKEN': 'token123',
    })
    @patch('app.services.issue_tracker_service.requests.post')
    def test_create_feishu_issue_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {
            'data': {'id': 'task_001', 'url': 'https://feishu.cn/task/001'},
        }
        mock_post.return_value = mock_resp

        from app.services.issue_tracker_service import create_feishu_issue
        result = create_feishu_issue('Task Title', 'Description')
        assert result['success'] is True
        assert 'feishu-task_001' in result['issue_key']

    @patch.dict('os.environ', {}, clear=True)
    def test_create_feishu_issue_missing_config(self):
        from app.services.issue_tracker_service import create_feishu_issue
        import os
        for key in ['FEISHU_PROJECT_URL', 'FEISHU_ACCESS_TOKEN']:
            os.environ.pop(key, None)
        result = create_feishu_issue('Title', 'Desc')
        assert result['success'] is False
        assert '配置不完整' in result['error']


# ══════════════════════════════════════════════════════════════════════════════
# 三、统一接口测试（需要数据库）
# ══════════════════════════════════════════════════════════════════════════════

class TestCreateIssueUnified:
    """统一 create_issue 接口测试"""

    @patch('app.services.issue_tracker_service.create_jira_issue')
    def test_create_issue_jira(self, mock_jira, app):
        mock_jira.return_value = {
            'success': True, 'issue_key': 'TEST-100', 'issue_url': 'https://jira/TEST-100',
        }
        from app.extensions import db
        from app.services.issue_tracker_service import create_issue
        with app.app_context():
            result = create_issue(
                tracker='jira',
                summary='Test Bug',
                description='Desc',
                created_by='manual',
            )
            assert result['success'] is True
            assert result['issue_link']['tracker'] == 'jira'
            assert result['issue_link']['issue_key'] == 'TEST-100'

            # 清理
            from app.models.issue_link import IssueLink
            IssueLink.query.filter_by(issue_key='TEST-100').delete()
            db.session.commit()

    def test_create_issue_unsupported_tracker(self, app):
        from app.services.issue_tracker_service import create_issue
        with app.app_context():
            result = create_issue(tracker='unknown', summary='T', description='D')
            assert result['success'] is False
            assert '不支持' in result['error']


class TestGetIssueLinks:
    """缺陷关联查询测试"""

    def test_get_issue_links_empty(self, app):
        from app.services.issue_tracker_service import get_issue_links
        with app.app_context():
            links = get_issue_links(test_run_id=99999)
            assert links == []

    def test_get_issue_links_with_data(self, app):
        from app.extensions import db
        from app.models.issue_link import IssueLink
        from app.services.issue_tracker_service import get_issue_links
        with app.app_context():
            link = IssueLink(
                tracker='jira', issue_key='TEST-200',
                issue_title='Test', test_run_id=99999,
            )
            db.session.add(link)
            db.session.commit()

            links = get_issue_links(test_run_id=99999)
            assert len(links) >= 1
            assert links[0]['issue_key'] == 'TEST-200'

            db.session.delete(link)
            db.session.commit()


# ══════════════════════════════════════════════════════════════════════════════
# 四、自动创建测试
# ══════════════════════════════════════════════════════════════════════════════

class TestAutoCreateIssue:
    """测试失败自动创建缺陷测试"""

    @patch.dict('os.environ', {
        'DEFAULT_ISSUE_TRACKER': '',
    })
    def test_auto_create_no_tracker_configured(self, app):
        from app.services.issue_tracker_service import auto_create_issue_on_failure
        with app.app_context():
            result = auto_create_issue_on_failure(1)
            assert result is None

    @patch('app.services.issue_tracker_service.create_jira_issue')
    def test_auto_create_on_failure(self, mock_jira, app):
        from app.extensions import db
        from app.models.user import User
        from app.models.project import Project
        from app.models.test_run import TestRun
        from app.services.issue_tracker_service import auto_create_issue_on_failure

        mock_jira.return_value = {
            'success': True, 'issue_key': 'AUTO-1', 'issue_url': 'https://jira/AUTO-1',
        }

        with app.app_context():
            user = User(username=f"it_{uuid.uuid4().hex[:6]}", email="it@test.com", password_hash="h")
            db.session.add(user)
            db.session.flush()
            proj = Project(name="ITProj", owner_id=user.id)
            db.session.add(proj)
            db.session.flush()
            run = TestRun(
                project_id=proj.id, test_type='api',
                test_object_name='Login Test', status='failed',
                failed=3, error_message='AssertionError',
            )
            db.session.add(run)
            db.session.flush()

            result = auto_create_issue_on_failure(run.id, tracker='jira')
            assert result is not None
            assert result['success'] is True
            assert result['issue_link']['created_by'] == 'auto'

            # 清理
            from app.models.issue_link import IssueLink
            IssueLink.query.filter_by(test_run_id=run.id).delete()
            db.session.delete(run)
            db.session.delete(proj)
            db.session.delete(user)
            db.session.commit()


# ══════════════════════════════════════════════════════════════════════════════
# 五、IssueLink Model 测试
# ══════════════════════════════════════════════════════════════════════════════

class TestIssueLinkModel:
    """IssueLink 模型测试"""

    def test_to_dict(self):
        from app.models.issue_link import IssueLink
        link = IssueLink(
            tracker='jira', issue_key='TEST-1',
            issue_url='https://jira/TEST-1', issue_title='Bug',
            status='open', created_by='manual',
        )
        d = link.to_dict()
        assert d['tracker'] == 'jira'
        assert d['issue_key'] == 'TEST-1'
        assert d['status'] == 'open'
        assert d['created_by'] == 'manual'

    def test_repr(self):
        from app.models.issue_link import IssueLink
        link = IssueLink(tracker='jira', issue_key='TEST-1', test_run_id=5)
        assert 'jira' in repr(link)
        assert 'TEST-1' in repr(link)


# ══════════════════════════════════════════════════════════════════════════════
# 六、状态映射测试
# ══════════════════════════════════════════════════════════════════════════════

class TestStatusMapping:
    """Jira 状态映射测试"""

    def test_map_jira_open(self):
        from app.services.issue_tracker_service import _map_jira_status
        assert _map_jira_status('Open') == 'open'
        assert _map_jira_status('To Do') == 'open'

    def test_map_jira_in_progress(self):
        from app.services.issue_tracker_service import _map_jira_status
        assert _map_jira_status('In Progress') == 'in_progress'

    def test_map_jira_resolved(self):
        from app.services.issue_tracker_service import _map_jira_status
        assert _map_jira_status('Done') == 'resolved'
        assert _map_jira_status('Resolved') == 'resolved'

    def test_map_jira_closed(self):
        from app.services.issue_tracker_service import _map_jira_status
        assert _map_jira_status('Closed') == 'closed'

    def test_map_jira_unknown(self):
        from app.services.issue_tracker_service import _map_jira_status
        assert _map_jira_status('UnknownStatus') == 'open'