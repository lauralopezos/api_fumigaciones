import os
import sys
from pathlib import Path
import pytest
from src.app import create_app

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app import app as flask_app
from db import execute

os.environ.setdefault("DATABASE_URL", os.getenv("DATABASE_URL_TEST", ""))

@pytest.fixture(scope="session")
def test_app():
    dsn_test = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL")
    os.environ["DATABASE_URL"] = dsn_test 
    return flask_app

@pytest.fixture(autouse=True)
def _clean_db(test_app):
    with test_app.app_context():
        execute("TRUNCATE administradores, tecnicos, consumidores RESTART IDENTITY CASCADE;", ())
    yield

@pytest.fixture()
def client():
    os.environ["DATABASE_URL"] = os.environ.get("DATABASE_URL_TEST", "")
    app = create_app()
    with app.test_client() as c:
        yield c
