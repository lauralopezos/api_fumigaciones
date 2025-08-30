import os
import psycopg2
import psycopg2.extras
from psycopg2.pool import SimpleConnectionPool
from flask import g

_pool = None

def init_app(app):
    global _pool
    dsn = app.config.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL no está configurado")

    _pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=dsn)

    @app.teardown_appcontext
    def _close_db(_exc):
        conn = g.pop("_db_conn", None)
        if conn is not None and _pool:
            _pool.putconn(conn)

def _get_conn():
    if "_db_conn" not in g:
        if _pool is None:
            raise RuntimeError("La pool de conexiones no está inicializada. Llama init_app")
        g._db_conn = _pool.getconn()
    return g._db_conn

def fetch_all(query, params=()):
    conn = _get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()

def fetch_one(query, params=()):
    conn = _get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()

def execute(query, params=()):
    """ Ejecuta INSERT/UPDATE/DELETE.
    Si el query incluye 'RETURNING id', devuelve ese id como second value. """
    conn = _get_conn()
    with conn.cursor() as cur:
        cur.execute(query, params)
        last_id = None
        if "RETURNING id" in query.upper():
            row = cur.fetchone()
            last_id = row[0] if row else None
        conn.commit()
        return cur.rowcount, last_id
