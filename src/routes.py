from flask import Blueprint, request, jsonify
from db import mysql
import MySQLdb.cursors

consumidores_bp   = Blueprint("consumidores",   __name__, url_prefix="/consumidores")
tecnicos_bp       = Blueprint("tecnicos",       __name__, url_prefix="/tecnicos")
administradores_bp= Blueprint("administradores",__name__, url_prefix="/administradores")

def fetch_all(query, params=()):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    return rows

def fetch_one(query, params=()):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    return row

def execute(query, params=()):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    rowcount = cur.rowcount
    last_id = cur.lastrowid
    cur.close()
    return rowcount, last_id

# Consumidores
@consumidores_bp.post("")
def crear_consumidor():
    data = request.get_json() or {}
    nombre = data.get("nombre"); email = data.get("email"); direccion = data.get("direccion")
    if not nombre or not email:
        return jsonify({"detail": "nombre y email son requeridos"}), 400
    if fetch_one("SELECT id FROM consumidores WHERE email=%s", (email,)):
        return jsonify({"detail": "El email ya existe"}), 400
    _, new_id = execute("INSERT INTO consumidores (nombre, email, direccion) VALUES (%s,%s,%s)",
                        (nombre, email, direccion))
    return jsonify({"id": new_id, "nombre": nombre, "email": email, "direccion": direccion}), 201

@consumidores_bp.get("")
def listar_consumidores():
    return jsonify(fetch_all("SELECT id, nombre, email, direccion FROM consumidores")), 200

@consumidores_bp.get("/<int:cid>")
def obtener_consumidor(cid):
    row = fetch_one("SELECT id, nombre, email, direccion FROM consumidores WHERE id=%s", (cid,))
    if not row: return jsonify({"detail": "Consumidor no encontrado"}), 404
    return jsonify(row), 200

@consumidores_bp.put("/<int:cid>")
def actualizar_consumidor(cid):
    data = request.get_json() or {}
    nombre = data.get("nombre"); email = data.get("email"); direccion = data.get("direccion")
    if not fetch_one("SELECT id FROM consumidores WHERE id=%s", (cid,)):
        return jsonify({"detail": "Consumidor no encontrado"}), 404
    if email and fetch_one("SELECT id FROM consumidores WHERE email=%s AND id<>%s", (email, cid)):
        return jsonify({"detail": "El email ya está en uso"}), 400
    campos, vals = [], []
    if nombre is not None:    campos.append("nombre=%s");    vals.append(nombre)
    if email is not None:     campos.append("email=%s");     vals.append(email)
    if direccion is not None: campos.append("direccion=%s"); vals.append(direccion)
    if not campos: return jsonify({"detail": "Nada para actualizar"}), 400
    vals.append(cid)
    execute(f"UPDATE consumidores SET {', '.join(campos)} WHERE id=%s", tuple(vals))
    return jsonify({"detail": "Consumidor actualizado"}), 200

@consumidores_bp.delete("/<int:cid>")
def eliminar_consumidor(cid):
    filas, _ = execute("DELETE FROM consumidores WHERE id=%s", (cid,))
    if filas == 0: return jsonify({"detail": "Consumidor no encontrado"}), 404
    return jsonify({"detail": "Consumidor eliminado"}), 200

# Técnicos
@tecnicos_bp.post("")
def crear_tecnico():
    data = request.get_json() or {}
    nombre = data.get("nombre"); telefono = data.get("telefono"); especialidad = data.get("especialidad")
    if not nombre: return jsonify({"detail": "nombre es requerido"}), 400
    _, new_id = execute("INSERT INTO tecnicos (nombre, telefono, especialidad) VALUES (%s,%s,%s)",
                        (nombre, telefono, especialidad))
    return jsonify({"id": new_id, "nombre": nombre, "telefono": telefono, "especialidad": especialidad}), 201

@tecnicos_bp.get("")
def listar_tecnicos():
    return jsonify(fetch_all("SELECT id, nombre, telefono, especialidad FROM tecnicos")), 200

@tecnicos_bp.get("/<int:tid>")
def obtener_tecnico(tid):
    row = fetch_one("SELECT id, nombre, telefono, especialidad FROM tecnicos WHERE id=%s", (tid,))
    if not row: return jsonify({"detail": "Técnico no encontrado"}), 404
    return jsonify(row), 200

@tecnicos_bp.put("/<int:tid>")
def actualizar_tecnico(tid):
    data = request.get_json() or {}
    nombre = data.get("nombre"); telefono = data.get("telefono"); especialidad = data.get("especialidad")
    if not fetch_one("SELECT id FROM tecnicos WHERE id=%s", (tid,)):
        return jsonify({"detail": "Técnico no encontrado"}), 404
    campos, vals = [], []
    if nombre is not None:       campos.append("nombre=%s");       vals.append(nombre)
    if telefono is not None:     campos.append("telefono=%s");     vals.append(telefono)
    if especialidad is not None: campos.append("especialidad=%s"); vals.append(especialidad)
    if not campos: return jsonify({"detail": "Nada para actualizar"}), 400
    vals.append(tid)
    execute(f"UPDATE tecnicos SET {', '.join(campos)} WHERE id=%s", tuple(vals))
    return jsonify({"detail": "Técnico actualizado"}), 200

@tecnicos_bp.delete("/<int:tid>")
def eliminar_tecnico(tid):
    filas, _ = execute("DELETE FROM tecnicos WHERE id=%s", (tid,))
    if filas == 0: return jsonify({"detail": "Técnico no encontrado"}), 404
    return jsonify({"detail": "Técnico eliminado"}), 200

# Administradores
@administradores_bp.post("")
def crear_admin():
    data = request.get_json() or {}
    nombre = data.get("nombre"); email = data.get("email")
    if not nombre or not email:
        return jsonify({"detail": "nombre y email son requeridos"}), 400
    if fetch_one("SELECT id FROM administradores WHERE email=%s", (email,)):
        return jsonify({"detail": "El email ya existe"}), 400
    _, new_id = execute("INSERT INTO administradores (nombre, email) VALUES (%s,%s)", (nombre, email))
    return jsonify({"id": new_id, "nombre": nombre, "email": email}), 201

@administradores_bp.get("")
def listar_admins():
    return jsonify(fetch_all("SELECT id, nombre, email FROM administradores")), 200

@administradores_bp.get("/<int:aid>")
def obtener_admin(aid):
    row = fetch_one("SELECT id, nombre, email FROM administradores WHERE id=%s", (aid,))
    if not row: return jsonify({"detail": "Administrador no encontrado"}), 404
    return jsonify(row), 200

@administradores_bp.put("/<int:aid>")
def actualizar_admin(aid):
    data = request.get_json() or {}
    nombre = data.get("nombre"); email = data.get("email")
    if not fetch_one("SELECT id FROM administradores WHERE id=%s", (aid,)):
        return jsonify({"detail": "Administrador no encontrado"}), 404
    if email and fetch_one("SELECT id FROM administradores WHERE email=%s AND id<>%s", (email, aid)):
        return jsonify({"detail": "El email ya está en uso"}), 400
    campos, vals = [], []
    if nombre is not None: campos.append("nombre=%s"); vals.append(nombre)
    if email  is not None: campos.append("email=%s");  vals.append(email)
    if not campos: return jsonify({"detail": "Nada para actualizar"}), 400
    vals.append(aid)
    execute(f"UPDATE administradores SET {', '.join(campos)} WHERE id=%s", tuple(vals))
    return jsonify({"detail": "Administrador actualizado"}), 200

@administradores_bp.delete("/<int:aid>")
def eliminar_admin(aid):
    filas, _ = execute("DELETE FROM administradores WHERE id=%s", (aid,))
    if filas == 0: return jsonify({"detail": "Administrador no encontrado"}), 404
    return jsonify({"detail": "Administrador eliminado"}), 200