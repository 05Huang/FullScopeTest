import os
import sys
import tempfile

import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("FLASK_ENV", "testing")
    os.environ["CELERY_ENABLE"] = "false"

    db_fd, db_path = tempfile.mkstemp(prefix="easytest_test_", suffix=".db")
    os.close(db_fd)

    os.environ["TEST_DATABASE_URL"] = f"sqlite:///{db_path}"
    app = create_app("testing")
    app.config.update(
        TESTING=True,
        SQLALCHEMY_ENGINE_OPTIONS={"connect_args": {"check_same_thread": False}},
        JWT_SECRET_KEY="test-jwt-secret",
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass


@pytest.fixture()
def client(app):
    return app.test_client()
