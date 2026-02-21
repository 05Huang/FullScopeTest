import os
import sys
from typing import List


SUPPORTED_POOLS = {"prefork", "threads", "gevent", "eventlet", "solo"}


def _resolve_default_pool() -> str:
    return "threads" if sys.platform.startswith("win") else "prefork"


def _parse_positive_int(raw_value: str | None, fallback: int) -> int:
    if raw_value is None:
        return fallback
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return fallback
    return value if value > 0 else fallback


def build_worker_argv(loglevel: str = "info") -> List[str]:
    default_pool = _resolve_default_pool()
    pool = os.environ.get("CELERY_WORKER_POOL", default_pool).strip().lower()
    if pool not in SUPPORTED_POOLS:
        pool = default_pool

    default_concurrency = max(2, os.cpu_count() or 2)
    if pool == "solo":
        concurrency = 1
    else:
        concurrency = _parse_positive_int(
            os.environ.get("CELERY_WORKER_CONCURRENCY"),
            default_concurrency,
        )

    prefetch_multiplier = _parse_positive_int(
        os.environ.get("CELERY_WORKER_PREFETCH_MULTIPLIER"),
        1,
    )

    argv = [
        "worker",
        f"--loglevel={loglevel}",
        f"--pool={pool}",
        f"--prefetch-multiplier={prefetch_multiplier}",
    ]

    if pool != "solo":
        argv.append(f"--concurrency={concurrency}")

    return argv
