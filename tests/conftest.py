import os, sys, pytest
from pathlib import Path

# src
BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

os.environ["APP_ENV"] = "testing"


from app import app
from db import mysql
from MySQLdb import OperationalError

# error 2006
_orig_teardown = mysql.teardown
def _teardown_safe(exception):
    try:
        _orig_teardown(exception)
    except OperationalError:
        pass
mysql.teardown = _teardown_safe
if hasattr(app, "teardown_appcontext_funcs"):
    for i, f in enumerate(app.teardown_appcontext_funcs):
        if getattr(f, "__qualname__", "").endswith("MySQL.teardown"):
            app.teardown_appcontext_funcs[i] = _teardown_safe
            break

@pytest.fixture(scope="session")
def test_app():
    return app

@pytest.fixture()
def client(test_app):
    with test_app.app_context():
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE consumidores")
        cur.execute("TRUNCATE TABLE tecnicos")
        cur.execute("TRUNCATE TABLE administradores")
        conn.commit()
        cur.close()

    with test_app.test_client() as c:
        yield c
