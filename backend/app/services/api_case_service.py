"""
API 测试用例 Service

处理测试用例的 CRUD 操作。
每次修改用例时自动保存前一版本的快照，支持版本历史查看和 diff 对比。
"""

import os
from sqlalchemy import func as sa_func
from .base import BaseService
from ..extensions import db
from ..models.api_test_case import ApiTestCase
from ..models.test_case_version import TestCaseVersion, diff_versions, MAX_VERSIONS
from ..utils.exceptions import NotFoundError, ValidationError
from ..core.logging import get_logger

logger = get_logger(__name__)


class ApiCaseService(BaseService):

    def get_cases(self, user_id: int, collection_id: int = None, project_id: int = None):
        """获取测试用例列表"""
        query = ApiTestCase.query.filter_by(user_id=user_id)
        if collection_id:
            query = query.filter_by(collection_id=collection_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        cases = query.order_by(ApiTestCase.created_at.desc()).all()
        return [c.to_dict() for c in cases]

    def get_case(self, case_id: int, user_id: int):
        """获取用例详情"""
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError("用例", case_id)
        return case.to_dict()

    def create_case(self, user_id: int, data: dict):
        """创建测试用例"""
        if not data.get('name'):
            raise ValidationError("name is required")
        if not data.get('method'):
            raise ValidationError("method is required")
        if not data.get('url'):
            raise ValidationError("url is required")

        case = ApiTestCase(
            name=data['name'],
            description=data.get('description', ''),
            method=data['method'].upper(),
            url=data['url'],
            headers=data.get('headers', {}),
            params=data.get('params', {}),
            body=data.get('body'),
            body_type=data.get('body_type', 'json'),
            pre_script=data.get('pre_script'),
            post_script=data.get('post_script'),
            assertions=data.get('assertions', []),
            collection_id=data.get('collection_id'),
            project_id=data.get('project_id'),
            environment_id=data.get('environment_id'),
            user_id=user_id,
            mock_enabled=data.get('mock_enabled', False),
            mock_response_code=data.get('mock_response_code', 200),
            mock_response_body=data.get('mock_response_body', ''),
            mock_response_headers=data.get('mock_response_headers', {}),
            mock_delay_ms=data.get('mock_delay_ms', 0)
        )

        with self.transaction():
            self.add(case)
            self.flush()
            result = case.to_dict()
        return result

    def update_case(self, case_id: int, user_id: int, data: dict):
        """
        更新测试用例

        自动保存前一版本的快照到版本历史。
        """
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError("用例", case_id)

        # 保存更新前的快照
        old_snapshot = case.to_dict()

        updatable_fields = [
            'name', 'description', 'method', 'url', 'headers', 'params',
            'body', 'body_type', 'pre_script', 'post_script', 'assertions',
            'collection_id', 'environment_id', 'mock_enabled',
            'mock_response_code', 'mock_response_body',
            'mock_response_headers', 'mock_delay_ms'
        ]
        for field in updatable_fields:
            if field in data:
                setattr(case, field, data[field])

        # 生成新快照并计算 diff
        new_snapshot = case.to_dict()
        version_diff = diff_versions(old_snapshot, new_snapshot)

        with self.transaction():
            # 仅在有实际变更时保存版本
            if version_diff['changed_fields']:
                self._save_version_snapshot(
                    case_type='api',
                    case_id=case_id,
                    content=old_snapshot,
                    changed_fields=version_diff['changed_fields'],
                    change_summary=self._build_change_summary(version_diff),
                    created_by=user_id,
                )
            result = case.to_dict()
        return result

    def delete_case(self, case_id: int, user_id: int):
        """删除测试用例"""
        case = ApiTestCase.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            raise NotFoundError("用例", case_id)

        with self.transaction():
            self.delete(case)

    # ── 版本历史 ─────────────────────────────────────────────────────────────

    def get_versions(self, case_id: int, page: int = 1, per_page: int = 20) -> dict:
        """
        获取用例的版本历史列表

        Args:
            case_id: 用例 ID
            page: 页码
            per_page: 每页数量

        Returns:
            分页结果
        """
        query = TestCaseVersion.query.filter_by(
            case_type='api', case_id=case_id,
        )
        total = query.count()
        versions = query.order_by(TestCaseVersion.version.desc()) \
            .offset((page - 1) * per_page) \
            .limit(per_page) \
            .all()

        return {
            'items': [v.to_dict() for v in versions],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
        }

    def get_version(self, version_id: int) -> dict:
        """获取指定版本详情"""
        version = TestCaseVersion.query.get(version_id)
        if not version:
            raise NotFoundError("版本", version_id)
        return version.to_dict()

    def diff_two_versions(self, version_id_1: int, version_id_2: int) -> dict:
        """
        对比两个版本的差异

        Args:
            version_id_1: 旧版本 ID
            version_id_2: 新版本 ID

        Returns:
            {version_1, version_2, diff}
        """
        v1 = TestCaseVersion.query.get(version_id_1)
        v2 = TestCaseVersion.query.get(version_id_2)
        if not v1:
            raise NotFoundError("版本", version_id_1)
        if not v2:
            raise NotFoundError("版本", version_id_2)

        diff = diff_versions(v1.content or {}, v2.content or {})
        return {
            'version_1': v1.to_dict(),
            'version_2': v2.to_dict(),
            'diff': diff,
        }

    # ── 内部工具 ─────────────────────────────────────────────────────────────

    def _save_version_snapshot(self, case_type: str, case_id: int, content: dict,
                               changed_fields: list, change_summary: str,
                               created_by: int = None):
        """
        保存版本快照

        自动递增版本号，并清理超出最大版本数的旧记录。
        """
        # 获取当前最大版本号
        max_version = db.session.query(
            sa_func.max(TestCaseVersion.version)
        ).filter_by(case_type=case_type, case_id=case_id).scalar() or 0

        version = TestCaseVersion(
            case_type=case_type,
            case_id=case_id,
            version=max_version + 1,
            content=content,
            change_summary=change_summary,
            changed_fields=changed_fields,
            created_by=created_by,
        )
        self.add(version)

        # 清理超出最大版本数的旧记录
        total_versions = TestCaseVersion.query.filter_by(
            case_type=case_type, case_id=case_id,
        ).count()
        if total_versions >= MAX_VERSIONS:
            old_versions = TestCaseVersion.query.filter_by(
                case_type=case_type, case_id=case_id,
            ).order_by(TestCaseVersion.version.asc()) \
                .limit(total_versions - MAX_VERSIONS + 1) \
                .all()
            for old in old_versions:
                self.delete(old)

        logger.info("版本快照已保存",
                     case_type=case_type, case_id=case_id,
                     version=max_version + 1,
                     changed_fields=changed_fields)

    def _build_change_summary(self, version_diff: dict) -> str:
        """构建变更摘要"""
        fields = version_diff.get('changed_fields', [])
        if not fields:
            return ''
        if len(fields) <= 3:
            return f'修改了 {", ".join(fields)}'
        return f'修改了 {", ".join(fields[:3])} 等 {len(fields)} 个字段'
