import os
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app import create_app
from src.db import execute

@pytest.fixture(scope="session")
def test_app():
    dsn_test = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL", "")
    os.environ["DATABASE_URL"] = dsn_test 
    app = create_app()
    return app

@pytest.fixture(autouse=True)
def _clean_db(test_app):
    with test_app.app_context():
        execute(
            "TRUNCATE administradores, tecnicos, consumidores RESTART IDENTITY CASCADE;",
            ()
        )
    yield

@pytest.fixture()
def client(test_app):
    with test_app.test_client() as c:
        yield c
