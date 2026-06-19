"""
数据归档与清理服务

管理测试执行产生的大量数据（执行记录、报告、截图）的生命周期。

保留策略通过环境变量配置：
- RETENTION_RAW_DAYS: 原始测试结果保留天数（默认 90）
- RETENTION_ATTACHMENTS_DAYS: 截图/附件保留天数（默认 30）
- RETENTION_SUMMARY_DAYS: 汇总统计保留天数（默认 365）

删除前记录审计日志，支持手动触发清理。
"""

import os
import glob
from datetime import datetime, timezone, timedelta

from ..core.logging import get_logger

logger = get_logger(__name__)


def _env_int(key: str, default: int) -> int:
    raw = os.environ.get(key)
    if raw is None:
        return default
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        return default


# 保留策略配置
RAW_RETENTION_DAYS = _env_int("RETENTION_RAW_DAYS", 90)
ATTACHMENT_RETENTION_DAYS = _env_int("RETENTION_ATTACHMENTS_DAYS", 30)
SUMMARY_RETENTION_DAYS = _env_int("RETENTION_SUMMARY_DAYS", 365)


def cleanup_raw_test_runs(app_context=None):
    """
    清理超过保留期的原始测试执行记录

    Returns:
        dict: 清理统计
    """
    from ..extensions import db
    from ..models.test_run import TestRun

    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=RAW_RETENTION_DAYS)
    stats = {"deleted_runs": 0, "cutoff_date": cutoff.isoformat()}

    try:
        old_runs = TestRun.query.filter(TestRun.created_at < cutoff).all()
        for run in old_runs:
            logger.info(
                "数据归档: 删除过期测试执行记录",
                run_id=run.id,
                created_at=str(run.created_at),
                project_id=run.project_id,
            )
            db.session.delete(run)
            stats["deleted_runs"] += 1

        if stats["deleted_runs"] > 0:
            db.session.commit()
            logger.info("数据归档完成", **stats)
    except Exception as exc:
        db.session.rollback()
        logger.error("数据归档失败", error=str(exc))
        stats["error"] = str(exc)

    return stats


def cleanup_old_reports(app_context=None):
    """
    清理超过保留期的测试报告

    Returns:
        dict: 清理统计
    """
    from ..extensions import db
    from ..models.test_report import TestReport

    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=RAW_RETENTION_DAYS)
    stats = {"deleted_reports": 0}

    try:
        old_reports = TestReport.query.filter(TestReport.created_at < cutoff).all()
        for report in old_reports:
            logger.info(
                "数据归档: 删除过期报告",
                report_id=report.id,
                created_at=str(report.created_at),
            )
            db.session.delete(report)
            stats["deleted_reports"] += 1

        if stats["deleted_reports"] > 0:
            db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logger.error("报告归档失败", error=str(exc))
        stats["error"] = str(exc)

    return stats


def cleanup_old_screenshots(storage_path=None):
    """
    清理超过保留期的截图文件

    Args:
        storage_path: 截图存储路径（默认从配置读取）

    Returns:
        dict: 清理统计
    """
    if storage_path is None:
        storage_path = os.environ.get(
            "SCREENSHOT_STORAGE_PATH",
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "screenshots"),
        )

    cutoff_ts = (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=ATTACHMENT_RETENTION_DAYS)).timestamp()
    stats = {"deleted_files": 0, "freed_bytes": 0}

    if not os.path.exists(storage_path):
        return stats

    try:
        for root, dirs, files in os.walk(storage_path):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    mtime = os.path.getmtime(fpath)
                    if mtime < cutoff_ts:
                        fsize = os.path.getsize(fpath)
                        os.remove(fpath)
                        stats["deleted_files"] += 1
                        stats["freed_bytes"] += fsize
                        logger.info("数据归档: 删除过期截图", path=fpath, size=fsize)
                except OSError:
                    pass

        if stats["deleted_files"] > 0:
            logger.info("截图归档完成", **stats)
    except Exception as exc:
        logger.error("截图归档失败", error=str(exc))
        stats["error"] = str(exc)

    return stats


def run_full_cleanup(storage_path=None):
    """
    执行完整的数据清理（供定时任务和手动 API 调用）

    Returns:
        dict: 汇总清理统计
    """
    logger.info("=== 开始数据归档清理 ===")
    results = {
        "raw_runs": cleanup_raw_test_runs(),
        "reports": cleanup_old_reports(),
        "screenshots": cleanup_old_screenshots(storage_path),
        "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
    }
    logger.info("=== 数据归档清理完成 ===", results=results)
    return results
