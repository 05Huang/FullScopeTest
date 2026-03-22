import os
import sys
import tempfile

import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

_db_fd, _db_path = tempfile.mkstemp(prefix="fullscopetest_test_", suffix=".db")
os.close(_db_fd)

os.environ.setdefault("TEST_DATABASE_URL", f"sqlite:///{_db_path}")


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("FLASK_ENV", "testing")
    os.environ["CELERY_ENABLE"] = "false"

    from app import create_app
    from app.extensions import db

    flask_app = create_app("testing")
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_ENGINE_OPTIONS={"connect_args": {"check_same_thread": False}},
        JWT_SECRET_KEY="test-jwt-secret",
    )

    with flask_app.app_context():
        # 确保所有模型都被导入，以便 create_all 能创建它们
        import app.models
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    try:
        os.remove(_db_path)
    except FileNotFoundError:
        pass


@pytest.fixture()
def client(app):
    return app.test_client()
