# tests/conftest.py
import os, sys, pytest
from pathlib import Path

# --- Hacer que Python encuentre src/ ---
BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# --- Forzar entorno de pruebas ---
os.environ["APP_ENV"] = "testing"


from app import app
from db import mysql
from MySQLdb import OperationalError

# --- Parchear teardown de Flask-MySQLdb para ignorar error 2006 en close() ---
_orig_teardown = mysql.teardown
def _teardown_safe(exception):
    try:
        _orig_teardown(exception)
    except OperationalError:
        # Ignora "2006, MySQL server has gone away" en cierre de conexión
        pass
# Reemplaza el método en la instancia
mysql.teardown = _teardown_safe
# Sustituye el handler ya registrado por el de arriba
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
    # 1) Limpieza de tablas dentro de un application context
    with test_app.app_context():
        conn = mysql.connection
        cur = conn.cursor()
        # Si tus tablas tuvieran FKs, respeta orden (hijo -> padre)
        cur.execute("TRUNCATE TABLE consumidores")
        cur.execute("TRUNCATE TABLE tecnicos")
        cur.execute("TRUNCATE TABLE administradores")
        conn.commit()
        cur.close()

    # 2) Cliente de pruebas
    with test_app.test_client() as c:
        yield c
