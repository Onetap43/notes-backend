import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

test_directory = tempfile.TemporaryDirectory()
database_path = Path(test_directory.name) / "test_notes.db"

os.environ["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
os.environ["SECRET_KEY"] = "test-secret-not-used-in-production"
os.environ["ALGORITHM"] = "HS256"

from app.database import DatabaseBase, database_engine
from app.main import app
from app.limiter import limiter

limiter.enabled = False


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database():
    yield
    database_engine.dispose()
    test_directory.cleanup()


@pytest.fixture(autouse=True)
def reset_test_database():
    assert database_engine.url.get_backend_name() == "sqlite"

    DatabaseBase.metadata.drop_all(bind=database_engine)
    DatabaseBase.metadata.create_all(bind=database_engine)

    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
