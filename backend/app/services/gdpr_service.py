"""
GDPR 数据合规服务

提供数据导出和删除能力，满足 GDPR 合规要求。
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from ..extensions import db
from ..models.user import User
from ..models.api_test_case import ApiTestCase
from ..models.test_run import TestRun
from ..models.comment import Comment
from ..core.logging import get_logger

logger = get_logger(__name__)


class GDPRService:
    """GDPR 数据合规服务"""

    def export_user_data(self, user_id: int) -> Dict[str, Any]:
        """
        导出用户所有个人数据（JSON 格式）

        Args:
            user_id: 用户 ID

        Returns:
            Dict: 包含用户所有数据的字典
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"用户 {user_id} 不存在")

        # 收集用户数据
        data = {
            "export_metadata": {
                "exported_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                "user_id": user_id,
                "format": "GDPR_DATA_EXPORT",
            },
            "profile": {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
            },
            "test_cases": [],
            "test_runs": [],
            "comments": [],
        }

        # 测试用例
        cases = ApiTestCase.query.filter_by(user_id=user_id).all()
        for c in cases:
            data["test_cases"].append({
                "id": c.id, "name": c.name, "method": c.method, "url": c.url,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            })

        # 测试执行记录
        runs = TestRun.query.filter_by(triggered_user_id=user_id).all()
        for r in runs:
            data["test_runs"].append({
                "id": r.id, "test_type": r.test_type, "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            })

        # 评论
        comments = Comment.query.filter_by(user_id=user_id).all()
        for cm in comments:
            data["comments"].append({
                "id": cm.id, "content": cm.content,
                "resource_type": cm.resource_type, "resource_id": cm.resource_id,
                "created_at": cm.created_at.isoformat() if cm.created_at else None,
            })

        logger.info("用户数据导出完成", user_id=user_id, cases=len(data["test_cases"]), runs=len(data["test_runs"]))
        return data

    def export_organization_data(self, org_id: int) -> Dict[str, Any]:
        """导出组织所有数据（管理员审计）"""
        from ..models.organization import Organization, OrganizationMember
        org = Organization.query.get(org_id)
        if not org:
            raise ValueError(f"组织 {org_id} 不存在")

        members = OrganizationMember.query.filter_by(organization_id=org_id).all()
        member_ids = [m.user_id for m in members]

        data = {"organization": org.to_dict() if hasattr(org, "to_dict") else {"id": org.id}, "members": len(members), "user_data": {}}
        for mid in member_ids:
            try:
                data["user_data"][mid] = self.export_user_data(mid)
            except Exception as exc:
                data["user_data"][mid] = {"error": str(exc)}
        return data

    def request_account_deletion(self, user_id: int) -> Dict[str, Any]:
        """
        请求删除账户（30 天冷静期）

        Args:
            user_id: 用户 ID

        Returns:
            Dict: 删除请求信息
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"用户 {user_id} 不存在")

        # 标记为待删除（30 天后执行）
        if hasattr(user, "settings") and isinstance(user.settings, dict):
            user.settings["deletion_requested_at"] = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
            db.session.commit()

        logger.info("账户删除请求已记录", user_id=user_id)
        return {
            "user_id": user_id,
            "status": "pending",
            "cooling_period_days": 30,
            "message": "账户删除请求已记录，30 天后将执行删除。在此期间您可以取消请求。",
        }

    def cancel_account_deletion(self, user_id: int) -> Dict[str, Any]:
        """取消账户删除请求"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"用户 {user_id} 不存在")
        if hasattr(user, "settings") and isinstance(user.settings, dict):
            user.settings.pop("deletion_requested_at", None)
            db.session.commit()
        return {"user_id": user_id, "status": "cancelled", "message": "账户删除请求已取消"}


_instance = None


def get_gdpr_service():
    global _instance
    if _instance is None: _instance = GDPRService()
    return _instance
