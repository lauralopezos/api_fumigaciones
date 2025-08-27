import os
import importlib


os.environ.setdefault("MYSQL_HOST", "127.0.0.1")
os.environ.setdefault("MYSQL_USER", "root")
os.environ.setdefault("MYSQL_PASSWORD", "root")
os.environ.setdefault("MYSQL_DB", "fumigaciones_db")


import config
config.DevelopmentConfig.MYSQL_HOST = os.environ["MYSQL_HOST"]
config.DevelopmentConfig.MYSQL_USER = os.environ["MYSQL_USER"]
config.DevelopmentConfig.MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
config.DevelopmentConfig.MYSQL_DB = os.environ["MYSQL_DB"]


import pytest
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
