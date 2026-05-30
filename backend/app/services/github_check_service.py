"""
GitHub Check Run 回写服务

测试开始时创建 Check Run（状态 in_progress）；
实时更新进度（通过 Check Run 的 output.summary）；
测试结束时更新最终状态（success/failure）；
附上测试报告链接和失败用例摘要
"""

import os
import time
from datetime import datetime
from typing import Dict, Any, Optional

import requests

from ..extensions import db
from ..models.github_integration import GitHubIntegration
from ..models.test_run import TestRun
from ..core.logging import get_logger

logger = get_logger(__name__)

# GitHub API 配置
GITHUB_API_BASE_URL = 'https://api.github.com'


class GitHubCheckService:
    """GitHub Check Run 回写服务"""

    def __init__(self, integration: GitHubIntegration):
        """
        初始化服务

        Args:
            integration: GitHub 集成信息（包含 access token）
        """
        self.integration = integration
        self._access_token = None

    def _get_access_token(self) -> Optional[str]:
        """获取解密后的 access token"""
        if self._access_token:
            return self._access_token

        if not self.integration or not self.integration.access_token_encrypted:
            return None

        try:
            from .github_oauth_service import decrypt_token
            self._access_token = decrypt_token(self.integration.access_token_encrypted)
            return self._access_token
        except Exception as exc:
            logger.error('Failed to decrypt GitHub token', error=str(exc))
            return None

    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        timeout: int = 30,
    ) -> Optional[Dict]:
        """
        发送 GitHub API 请求

        Args:
            method: HTTP 方法
            url: API URL
            data: 请求体
            timeout: 超时时间（秒）

        Returns:
            响应数据，失败返回 None
        """
        token = self._get_access_token()
        if not token:
            logger.error('No GitHub access token available')
            return None

        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        try:
            resp = requests.request(
                method,
                url,
                headers=headers,
                json=data,
                timeout=timeout,
            )

            if resp.status_code >= 200 and resp.status_code < 300:
                return resp.json() if resp.content else {}

            logger.error(
                'GitHub API request failed',
                status_code=resp.status_code,
                url=url,
                response=resp.text[:500],
            )
            return None

        except requests.exceptions.Timeout:
            logger.error('GitHub API request timed out', url=url)
            return None
        except requests.exceptions.RequestException as exc:
            logger.error('GitHub API request failed', error=str(exc), url=url)
            return None

    def create_check_run(
        self,
        repo_full_name: str,
        name: str,
        head_sha: str,
        status: str = 'in_progress',
        output_title: Optional[str] = None,
        output_summary: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        创建 GitHub Check Run

        Args:
            repo_full_name: 仓库全名（owner/repo）
            name: Check Run 名称
            head_sha: 提交 SHA
            status: 状态（queued/in_progress/completed）
            output_title: 输出标题
            output_summary: 输出摘要

        Returns:
            Check Run 数据，失败返回 None
        """
        url = f'{GITHUB_API_BASE_URL}/repos/{repo_full_name}/check-runs'

        data = {
            'name': name,
            'head_sha': head_sha,
            'status': status,
        }

        if output_title or output_summary:
            data['output'] = {}
            if output_title:
                data['output']['title'] = output_title
            if output_summary:
                data['output']['summary'] = output_summary

        logger.info(
            'Creating GitHub Check Run',
            repo=repo_full_name,
            name=name,
            head_sha=head_sha[:8],
        )

        result = self._make_request('POST', url, data)
        if result:
            logger.info(
                'GitHub Check Run created',
                check_run_id=result.get('id'),
                repo=repo_full_name,
            )

        return result

    def update_check_run(
        self,
        repo_full_name: str,
        check_run_id: int,
        status: Optional[str] = None,
        output_title: Optional[str] = None,
        output_summary: Optional[str] = None,
        output_text: Optional[str] = None,
        conclusion: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        更新 GitHub Check Run

        Args:
            repo_full_name: 仓库全名（owner/repo）
            check_run_id: Check Run ID
            status: 状态（queued/in_progress/completed）
            output_title: 输出标题
            output_summary: 输出摘要
            output_text: 输出详细文本
            conclusion: 最终结论（当 status=completed 时必填）
                可选值: action_required/cancelled/failure/neutral/success/skipped/stale/timed_out

        Returns:
            更新后的 Check Run 数据，失败返回 None
        """
        url = f'{GITHUB_API_BASE_URL}/repos/{repo_full_name}/check-runs/{check_run_id}'

        data = {}

        if status:
            data['status'] = status

        if conclusion and status == 'completed':
            data['conclusion'] = conclusion

        has_output = output_title or output_summary or output_text
        if has_output:
            data['output'] = {}
            if output_title:
                data['output']['title'] = output_title
            if output_summary:
                data['output']['summary'] = output_summary
            if output_text:
                data['output']['text'] = output_text

        logger.info(
            'Updating GitHub Check Run',
            repo=repo_full_name,
            check_run_id=check_run_id,
            status=status,
            conclusion=conclusion,
        )

        return self._make_request('PATCH', url, data)

    def start_test_check_run(
        self,
        test_run: TestRun,
        repo_full_name: str,
        head_sha: str,
    ) -> Optional[Dict]:
        """
        测试开始时创建 Check Run

        Args:
            test_run: 测试运行记录
            repo_full_name: 仓库全名
            head_sha: 提交 SHA

        Returns:
            Check Run 数据
        """
        name = f'FullScopeTest - {test_run.test_type.upper()} Test'
        title = f'Running {test_run.test_type} tests'
        summary = f'Starting test run #{test_run.id} for project {test_run.project_id}'

        return self.create_check_run(
            repo_full_name=repo_full_name,
            name=name,
            head_sha=head_sha,
            status='in_progress',
            output_title=title,
            output_summary=summary,
        )

    def update_test_progress(
        self,
        repo_full_name: str,
        check_run_id: int,
        test_run: TestRun,
        current_step: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        实时更新测试进度

        Args:
            repo_full_name: 仓库全名
            check_run_id: Check Run ID
            test_run: 测试运行记录
            current_step: 当前步骤描述

        Returns:
            更新后的 Check Run 数据
        """
        title = f'Running {test_run.test_type} tests'

        summary_parts = [
            f'**Test Run #{test_run.id}**',
            f'',
            f'| Metric | Value |',
            f'|--------|-------|',
            f'| Status | {test_run.status} |',
            f'| Total Cases | {test_run.total_cases} |',
            f'| Passed | {test_run.passed} |',
            f'| Failed | {test_run.failed} |',
            f'| Skipped | {test_run.skipped} |',
            f'| Error | {test_run.error} |',
        ]

        if test_run.total_cases > 0:
            pass_rate = round(test_run.passed / test_run.total_cases * 100, 1)
            summary_parts.append(f'| Pass Rate | {pass_rate}% |')

        if current_step:
            summary_parts.append(f'')
            summary_parts.append(f'**Current Step:** {current_step}')

        summary = '\n'.join(summary_parts)

        return self.update_check_run(
            repo_full_name=repo_full_name,
            check_run_id=check_run_id,
            status='in_progress',
            output_title=title,
            output_summary=summary,
        )

    def complete_test_check_run(
        self,
        repo_full_name: str,
        check_run_id: int,
        test_run: TestRun,
        report_url: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        测试结束时更新 Check Run 最终状态

        Args:
            repo_full_name: 仓库全名
            check_run_id: Check Run ID
            test_run: 测试运行记录
            report_url: 测试报告链接

        Returns:
            更新后的 Check Run 数据
        """
        # 确定结论
        conclusion_map = {'success': 'success', 'failed': 'failure', 'cancelled': 'cancelled'}
        conclusion = conclusion_map.get(test_run.status, 'neutral')

        # 构建标题
        title = f'{test_run.test_type.upper()} tests {conclusion}'

        # 构建摘要
        summary_parts = [
            f'**Test Run #{test_run.id} - {conclusion.upper()}**',
            f'',
            f'| Metric | Value |',
            f'|--------|-------|',
            f'| Total Cases | {test_run.total_cases} |',
            f'| Passed | {test_run.passed} |',
            f'| Failed | {test_run.failed} |',
            f'| Skipped | {test_run.skipped} |',
            f'| Error | {test_run.error} |',
        ]

        if test_run.total_cases > 0:
            pass_rate = round(test_run.passed / test_run.total_cases * 100, 1)
            summary_parts.append(f'| Pass Rate | {pass_rate}% |')

        if test_run.duration:
            summary_parts.append(f'| Duration | {test_run.duration:.1f}s |')

        if test_run.environment_name:
            summary_parts.append(f'| Environment | {test_run.environment_name} |')

        summary = '\n'.join(summary_parts)

        # 构建详细文本（包含失败用例摘要）
        text_parts = []

        if test_run.results and isinstance(test_run.results, list):
            failed_cases = [
                r for r in test_run.results
                if isinstance(r, dict) and r.get('status') == 'failed'
            ]

            if failed_cases:
                text_parts.append(f'**Failed Test Cases ({len(failed_cases)}):**')
                text_parts.append('')

                for i, case in enumerate(failed_cases[:10], 1):  # 最多显示 10 个
                    case_name = case.get('name', f'Case {i}')
                    error_msg = case.get('error', case.get('error_message', 'No error message'))
                    text_parts.append(f'{i}. **{case_name}**')
                    text_parts.append(f'   Error: {error_msg}')
                    text_parts.append('')

                if len(failed_cases) > 10:
                    text_parts.append(f'... and {len(failed_cases) - 10} more failed cases')

        if report_url:
            text_parts.append(f'')
            text_parts.append(f'**[View Full Report]({report_url})**')

        text = '\n'.join(text_parts) if text_parts else None

        return self.update_check_run(
            repo_full_name=repo_full_name,
            check_run_id=check_run_id,
            status='completed',
            conclusion=conclusion,
            output_title=title,
            output_summary=summary,
            output_text=text,
        )


# 模块级便捷函数
def create_check_service(integration: GitHubIntegration) -> GitHubCheckService:
    """创建 Check Run 服务实例"""
    return GitHubCheckService(integration)
