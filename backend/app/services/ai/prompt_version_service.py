"""
Prompt 版本管理服务

提供 Prompt 版本的 CRUD、A/B 测试选择、统计更新等功能。
"""

import random
from typing import Optional, List, Dict, Any
from datetime import datetime

from ...extensions import db
from ...models.prompt_version import PromptVersion
from ...models.ai_invocation_log import AIInvocationLog
from ...core.logging import get_logger

logger = get_logger(__name__)


class PromptVersionService:
    """Prompt 版本管理服务"""

    # ---- 查询 ----

    @staticmethod
    def get_by_id(version_id: int) -> Optional[PromptVersion]:
        """按 ID 获取 Prompt 版本"""
        return PromptVersion.query.get(version_id)

    @staticmethod
    def get_active_versions(feature: str) -> List[PromptVersion]:
        """获取指定 feature 的所有激活版本"""
        return PromptVersion.query.filter_by(
            feature=feature,
            is_active=True,
        ).order_by(PromptVersion.version.desc()).all()

    @staticmethod
    def list_versions(
        feature: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """
        分页查询 Prompt 版本列表

        Returns:
            dict: {'items': [...], 'total': int, 'page': int, 'per_page': int, 'pages': int}
        """
        query = PromptVersion.query

        if feature:
            query = query.filter_by(feature=feature)
        if is_active is not None:
            query = query.filter_by(is_active=is_active)

        query = query.order_by(
            PromptVersion.feature.asc(),
            PromptVersion.version.desc(),
        )

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'items': [v.to_dict() for v in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
        }

    @staticmethod
    def get_latest_version(feature: str) -> Optional[PromptVersion]:
        """获取指定 feature 的最新版本号"""
        return PromptVersion.query.filter_by(feature=feature).order_by(
            PromptVersion.version.desc()
        ).first()

    # ---- 创建 ----

    @staticmethod
    def create_version(
        feature: str,
        name: str,
        system_prompt: str,
        *,
        user_prompt_template: Optional[str] = None,
        temperature: float = 0.3,
        model_name: Optional[str] = None,
        is_active: bool = False,
        traffic_weight: float = 1.0,
        change_notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> PromptVersion:
        """
        创建新的 Prompt 版本

        自动计算 version 号（feature 下递增）。
        如果 is_active=True 且同 feature 下没有其他激活版本，则自动激活。
        """
        # 获取当前最大版本号
        latest = PromptVersionService.get_latest_version(feature)
        next_version = (latest.version + 1) if latest else 1

        pv = PromptVersion(
            feature=feature,
            name=name,
            version=next_version,
            is_active=is_active,
            system_prompt=system_prompt,
            user_prompt_template=user_prompt_template,
            temperature=temperature,
            model_name=model_name,
            traffic_weight=traffic_weight,
            change_notes=change_notes,
            created_by=created_by,
        )

        db.session.add(pv)
        db.session.commit()

        logger.info(
            'Prompt version created',
            feature=feature,
            name=name,
            version=next_version,
            is_active=is_active,
        )
        return pv

    # ---- 更新 ----

    @staticmethod
    def update_version(
        version_id: int,
        *,
        name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        user_prompt_template: Optional[str] = None,
        temperature: Optional[float] = None,
        model_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        traffic_weight: Optional[float] = None,
        change_notes: Optional[str] = None,
    ) -> Optional[PromptVersion]:
        """更新 Prompt 版本"""
        pv = PromptVersion.query.get(version_id)
        if not pv:
            return None

        if name is not None:
            pv.name = name
        if system_prompt is not None:
            pv.system_prompt = system_prompt
        if user_prompt_template is not None:
            pv.user_prompt_template = user_prompt_template
        if temperature is not None:
            pv.temperature = temperature
        if model_name is not None:
            pv.model_name = model_name
        if is_active is not None:
            if is_active:
                pv.is_active = True
            else:
                pv.is_active = False
                pv.deactivated_at = datetime.utcnow()
        if traffic_weight is not None:
            pv.traffic_weight = max(0.0, min(1.0, traffic_weight))
        if change_notes is not None:
            pv.change_notes = change_notes

        pv.updated_at = datetime.utcnow()
        db.session.commit()

        logger.info('Prompt version updated', version_id=version_id)
        return pv

    # ---- 停用 ----

    @staticmethod
    def deactivate_version(version_id: int) -> bool:
        """停用（软删除）Prompt 版本"""
        pv = PromptVersion.query.get(version_id)
        if not pv:
            return False

        pv.is_active = False
        pv.deactivated_at = datetime.utcnow()
        pv.updated_at = datetime.utcnow()
        db.session.commit()

        logger.info('Prompt version deactivated', version_id=version_id)
        return True

    # ---- A/B 测试选择 ----

    @staticmethod
    def select_version_for_ab_test(feature: str) -> Optional[PromptVersion]:
        """
        基于流量权重选择一个激活的 Prompt 版本用于 A/B 测试。

        如果只有一个激活版本，直接返回。
        如果有多个激活版本，按 traffic_weight 比例随机选择。
        """
        active_versions = PromptVersionService.get_active_versions(feature)
        if not active_versions:
            return None
        if len(active_versions) == 1:
            return active_versions[0]

        # 按权重随机选择
        total_weight = sum(v.traffic_weight for v in active_versions)
        if total_weight <= 0:
            return random.choice(active_versions)

        rand = random.uniform(0, total_weight)
        cumulative = 0.0
        for v in active_versions:
            cumulative += v.traffic_weight
            if rand <= cumulative:
                return v

        return active_versions[-1]

    # ---- 统计更新 ----

    @staticmethod
    def refresh_stats(version_id: int) -> Optional[PromptVersion]:
        """
        从 AIInvocationLog 重新计算并更新指定 PromptVersion 的统计字段。
        """
        pv = PromptVersion.query.get(version_id)
        if not pv:
            return None

        stats = db.session.query(
            db.func.count(AIInvocationLog.id).label('total'),
            db.func.sum(db.case((AIInvocationLog.success == True, 1), else_=0)).label('success'),
            db.func.sum(db.case((AIInvocationLog.success == False, 1), else_=0)).label('failure'),
            db.func.avg(AIInvocationLog.latency_ms).label('avg_latency'),
            db.func.avg(AIInvocationLog.total_tokens).label('avg_tokens'),
            db.func.avg(AIInvocationLog.cost_estimate).label('avg_cost'),
        ).filter(
            AIInvocationLog.prompt_version_id == version_id
        ).first()

        pv.total_invocations = stats.total or 0
        pv.success_count = int(stats.success or 0)
        pv.failure_count = int(stats.failure or 0)
        pv.avg_latency_ms = round(float(stats.avg_latency or 0), 2)
        pv.avg_tokens = round(float(stats.avg_tokens or 0), 2)
        pv.avg_cost = round(float(stats.avg_cost or 0), 8)
        pv.updated_at = datetime.utcnow()

        db.session.commit()

        logger.info(
            'Prompt version stats refreshed',
            version_id=version_id,
            total_invocations=pv.total_invocations,
            success_count=pv.success_count,
        )
        return pv

    @staticmethod
    def refresh_all_stats(feature: Optional[str] = None) -> int:
        """批量刷新所有（或指定 feature 的）PromptVersion 统计。返回刷新数量。"""
        query = PromptVersion.query
        if feature:
            query = query.filter_by(feature=feature)

        versions = query.all()
        count = 0
        for pv in versions:
            PromptVersionService.refresh_stats(pv.id)
            count += 1

        return count


prompt_version_service = PromptVersionService()
