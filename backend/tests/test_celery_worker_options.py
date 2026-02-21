from app.utils.celery_worker_options import build_worker_argv


def _to_kv(argv):
    result = {}
    for item in argv:
        if item.startswith("--") and "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
    return result


def test_build_worker_argv_defaults_to_supported_pool(monkeypatch):
    monkeypatch.delenv("CELERY_WORKER_POOL", raising=False)
    monkeypatch.delenv("CELERY_WORKER_CONCURRENCY", raising=False)
    monkeypatch.delenv("CELERY_WORKER_PREFETCH_MULTIPLIER", raising=False)

    argv = build_worker_argv("warning")
    kv = _to_kv(argv)

    assert argv[0] == "worker"
    assert kv["--loglevel"] == "warning"
    assert kv["--pool"] in {"prefork", "threads"}
    assert int(kv["--prefetch-multiplier"]) >= 1

    if kv["--pool"] == "solo":
        assert "--concurrency" not in kv
    else:
        assert int(kv["--concurrency"]) >= 1


def test_build_worker_argv_ignores_concurrency_for_solo(monkeypatch):
    monkeypatch.setenv("CELERY_WORKER_POOL", "solo")
    monkeypatch.setenv("CELERY_WORKER_CONCURRENCY", "16")

    argv = build_worker_argv()
    kv = _to_kv(argv)

    assert kv["--pool"] == "solo"
    assert "--concurrency" not in kv


def test_build_worker_argv_falls_back_when_pool_invalid(monkeypatch):
    monkeypatch.setenv("CELERY_WORKER_POOL", "invalid")
    monkeypatch.delenv("CELERY_WORKER_CONCURRENCY", raising=False)

    argv = build_worker_argv()
    kv = _to_kv(argv)

    assert kv["--pool"] in {"prefork", "threads"}
