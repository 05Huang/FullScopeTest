"""
PR 评论服务

测试执行完成后，在 GitHub PR 中添加评论并更新 Check Run 状态。
"""

import os
import requests
from typing import Dict, Any, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

GITHUB_API = "https://api.github.com"


class PRCommentService:
    """PR 评论服务"""

    def __init__(self, token: str = None):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")

    def add_comment(self, repo: str, pr_number: int, body: str) -> bool:
        """在 PR 中添加评论"""
        if not self.token:
            logger.warning("GitHub Token 未配置，跳过 PR 评论")
            return False
        try:
            resp = requests.post(
                f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments",
                headers={"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github.v3+json"},
                json={"body": body},
                timeout=10,
            )
            if resp.status_code == 201:
                logger.info("PR 评论添加成功", repo=repo, pr=pr_number)
                return True
            logger.warning("PR 评论添加失败", status=resp.status_code)
            return False
        except Exception as exc:
            logger.error("PR 评论异常", error=str(exc))
            return False

    def create_check_run(self, repo: str, head_sha: str, name: str, status: str, conclusion: str = None,
                         output: Dict = None) -> bool:
        """创建 GitHub Check Run"""
        if not self.token: return False
        payload = {"name": name, "head_sha": head_sha, "status": status}
        if conclusion: payload["conclusion"] = conclusion
        if output: payload["output"] = output
        try:
            resp = requests.post(
                f"{GITHUB_API}/repos/{repo}/check-runs",
                headers={"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github.v3+json"},
                json=payload, timeout=10,
            )
            return resp.status_code == 201
        except Exception as exc:
            logger.error("Check Run 创建失败", error=str(exc))
            return False

    def format_test_results_comment(self, results: Dict[str, Any]) -> str:
        """格式化测试结果为 PR 评论"""
        total = results.get("total", 0)
        passed = results.get("passed", 0)
        failed = results.get("failed", 0)
        pass_rate = results.get("pass_rate", 0)
        duration = results.get("duration", 0)
        report_url = results.get("report_url", "")

        status_icon = "✅" if failed == 0 else "❌"
        lines = [
            f"## {status_icon} FullScopeTest Results",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Pass Rate | **{pass_rate}%** |",
            f"| Total Cases | {total} |",
            f"| Passed | {passed} |",
            f"| Failed | {failed} |",
            f"| Duration | {duration:.1f}s |",
        ]
        if report_url:
            lines.append(f"\n[View Full Report]({report_url})")
        return "\n".join(lines)


_instance = None


def get_pr_comment_service():
    global _instance
    if _instance is None: _instance = PRCommentService()
    return _instance
