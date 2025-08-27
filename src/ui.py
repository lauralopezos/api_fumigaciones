# ui.py
import os
from flask import Blueprint, render_template, request, redirect, url_for
from db import mysql
import MySQLdb.cursors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR  = os.path.join(BASE_DIR, "templates")

ui = Blueprint("ui", __name__, url_prefix="/ui", template_folder=TPL_DIR)

def q(sql, params=(), one=False):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, params)
    if sql.strip().upper().startswith("SELECT"):
        data = cur.fetchone() if one else cur.fetchall()
    else:
        mysql.connection.commit()
        data = cur.lastrowid
    cur.close()
    return data

@ui.get("/ping")
def ui_ping():
    return "UI OK", 200

# -------- CONSUMIDORES (CRUD UI) --------
@ui.get("/consumidores")
def ui_list_consumidores():
    rows = q("SELECT id, nombre, email, direccion FROM consumidores")
    return render_template("consumidores_list.html", rows=rows)

@ui.get("/consumidores/new")
def ui_new_consumidor():
    return render_template("consumidores_form.html", item=None, mode="create")

@ui.post("/consumidores/new")
def ui_create_consumidor():
    nombre = request.form.get("nombre", "").strip()
    email  = request.form.get("email", "").strip()
    dire   = request.form.get("direccion", "").strip()
    if not nombre or not email:
        return redirect(url_for("ui.ui_new_consumidor"))
    if q("SELECT id FROM consumidores WHERE email=%s", (email,), one=True):
        return redirect(url_for("ui.ui_new_consumidor"))
    q("INSERT INTO consumidores (nombre, email, direccion) VALUES (%s,%s,%s)", (nombre, email, dire))
    return redirect(url_for("ui.ui_list_consumidores"))

@ui.get("/consumidores/<int:cid>/edit")
def ui_edit_consumidor(cid):
    item = q("SELECT id, nombre, email, direccion FROM consumidores WHERE id=%s", (cid,), one=True)
    if not item: return "No encontrado", 404
    return render_template("consumidores_form.html", item=item, mode="edit")

@ui.post("/consumidores/<int:cid>/edit")
def ui_update_consumidor(cid):
    nombre = request.form.get("nombre", "").strip()
    email  = request.form.get("email", "").strip()
    dire   = request.form.get("direccion", "").strip()
    if not q("SELECT id FROM consumidores WHERE id=%s", (cid,), one=True):
        return "No encontrado", 404
    if not nombre or not email:
        return redirect(url_for("ui.ui_edit_consumidor", cid=cid))
    if q("SELECT id FROM consumidores WHERE email=%s AND id<>%s", (email, cid), one=True):
        return redirect(url_for("ui.ui_edit_consumidor", cid=cid))
    q("UPDATE consumidores SET nombre=%s, email=%s, direccion=%s WHERE id=%s",
      (nombre, email, dire, cid))
    return redirect(url_for("ui.ui_list_consumidores"))

@ui.post("/consumidores/<int:cid>/delete")
def ui_delete_consumidor(cid):
    q("DELETE FROM consumidores WHERE id=%s", (cid,))
    return redirect(url_for("ui.ui_list_consumidores"))

# -------- TÉCNICOS (CRUD UI) --------
@ui.get("/tecnicos")
def ui_list_tecnicos():
    rows = q("SELECT id, nombre, telefono, especialidad FROM tecnicos")
    return render_template("tecnicos_list.html", rows=rows)

@ui.get("/tecnicos/new")
def ui_new_tecnico():
    return render_template("tecnicos_form.html", item=None, mode="create")

@ui.post("/tecnicos/new")
def ui_create_tecnico():
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()
    especialidad = request.form.get("especialidad", "").strip()
    if not nombre:
        return redirect(url_for("ui.ui_new_tecnico"))
    q("INSERT INTO tecnicos (nombre, telefono, especialidad) VALUES (%s,%s,%s)",
      (nombre, telefono, especialidad))
    return redirect(url_for("ui.ui_list_tecnicos"))

@ui.get("/tecnicos/<int:tid>/edit")
def ui_edit_tecnico(tid):
    item = q("SELECT id, nombre, telefono, especialidad FROM tecnicos WHERE id=%s", (tid,), one=True)
    if not item: return "No encontrado", 404
    return render_template("tecnicos_form.html", item=item, mode="edit")

@ui.post("/tecnicos/<int:tid>/edit")
def ui_update_tecnico(tid):
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()
    especialidad = request.form.get("especialidad", "").strip()
    if not q("SELECT id FROM tecnicos WHERE id=%s", (tid,), one=True):
        return "No encontrado", 404
    campos, params = [], []
    campos.append("nombre=%s");       params.append(nombre)
    campos.append("telefono=%s");     params.append(telefono)
    campos.append("especialidad=%s"); params.append(especialidad)
    params.append(tid)
    q(f"UPDATE tecnicos SET {', '.join(campos)} WHERE id=%s", tuple(params))
    return redirect(url_for("ui.ui_list_tecnicos"))

@ui.post("/tecnicos/<int:tid>/delete")
def ui_delete_tecnico(tid):
    q("DELETE FROM tecnicos WHERE id=%s", (tid,))
    return redirect(url_for("ui.ui_list_tecnicos"))

# -------- ADMINISTRADORES (CRUD UI) --------
@ui.get("/administradores")
def ui_list_admins():
    rows = q("SELECT id, nombre, email FROM administradores")
    return render_template("administradores_list.html", rows=rows)

@ui.get("/administradores/new")
def ui_new_admin():
    return render_template("administradores_form.html", item=None, mode="create")

@ui.post("/administradores/new")
def ui_create_admin():
    nombre = request.form.get("nombre", "").strip()
    email  = request.form.get("email", "").strip()
    if not nombre or not email:
        return redirect(url_for("ui.ui_new_admin"))
    if q("SELECT id FROM administradores WHERE email=%s", (email,), one=True):
        return redirect(url_for("ui.ui_new_admin"))
    q("INSERT INTO administradores (nombre, email) VALUES (%s,%s)", (nombre, email))
    return redirect(url_for("ui.ui_list_admins"))

@ui.get("/administradores/<int:aid>/edit")
def ui_edit_admin(aid):
    item = q("SELECT id, nombre, email FROM administradores WHERE id=%s", (aid,), one=True)
    if not item: return "No encontrado", 404
    return render_template("administradores_form.html", item=item, mode="edit")

@ui.post("/administradores/<int:aid>/edit")
def ui_update_admin(aid):
    nombre = request.form.get("nombre", "").strip()
    email  = request.form.get("email", "").strip()
    if not q("SELECT id FROM administradores WHERE id=%s", (aid,), one=True):
        return "No encontrado", 404
    if not nombre or not email:
        return redirect(url_for("ui.ui_edit_admin", aid=aid))
    if q("SELECT id FROM administradores WHERE email=%s AND id<>%s", (email, aid), one=True):
        return redirect(url_for("ui.ui_edit_admin", aid=aid))
    q("UPDATE administradores SET nombre=%s, email=%s WHERE id=%s", (nombre, email, aid))
    return redirect(url_for("ui.ui_list_admins"))

@ui.post("/administradores/<int:aid>/delete")
def ui_delete_admin(aid):
    q("DELETE FROM administradores WHERE id=%s", (aid,))
    return redirect(url_for("ui.ui_list_admins"))
