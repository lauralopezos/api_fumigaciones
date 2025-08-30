from __future__ import annotations

from flask import (
    Blueprint,
    render_template_string,
    request,
    redirect,
    url_for,
    abort,
)

from .db import (
    fetch_all as db_fetch_all,
    fetch_one as db_fetch_one,
    execute as db_execute,
)

bp = Blueprint("ui", __name__, url_prefix="/ui")


def _html_layout(title: str, body: str) -> str:
    """Layout mínimo inline para no depender de templates en disco."""
    return f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <title>{title}</title>
      <style>
        body {{
          font-family: system-ui, Arial, sans-serif;
          margin: 24px;
        }}
        table {{
          border-collapse: collapse;
          width: 100%;
          max-width: 900px;
        }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background: #f3f3f3; text-align: left; }}
        .actions a {{ margin-right: 8px; }}
        form div {{ margin: 8px 0; }}
        input[type="text"], input[type="email"] {{
          width: 100%;
          max-width: 420px;
          padding: 6px 8px;
          border: 1px solid #ccc;
          border-radius: 4px;
        }}
        .btn {{
          display: inline-block;
          padding: 6px 10px;
          border: 1px solid #444;
          border-radius: 4px;
          background: #fff;
          text-decoration: none;
          color: #222;
        }}
        .btn-primary {{
          background: #222;
          color: #fff;
          border-color: #222;
        }}
        .mt-16 {{ margin-top: 16px; }}
        .mb-16 {{ margin-bottom: 16px; }}
      </style>
    </head>
    <body>
      <nav class="mb-16">
        <a class="btn" href="{url_for('ui.index')}">Inicio UI</a>
        <a class="btn" href="{url_for('ui.lista_consumidores')}">Consumidores</a>
        <a class="btn" href="{url_for('ui.lista_tecnicos')}">Técnicos</a>
        <a class="btn" href="{url_for('ui.lista_admins')}">Administradores</a>
      </nav>
      {body}
    </body>
    </html>
    """


def _render(template: str, **ctx):
    return render_template_string(template, **ctx)


# Home

@bp.get("/")
def index():
    body = """
    <h1>UI - Fumigaciones</h1>
    <p>Selecciona una sección:</p>
    <ul>
      <li><a href="{{ url_for('ui.lista_consumidores') }}">Consumidores</a></li>
      <li><a href="{{ url_for('ui.lista_tecnicos') }}">Técnicos</a></li>
      <li><a href="{{ url_for('ui.lista_admins') }}">Administradores</a></li>
    </ul>
    """
    return _render(_html_layout("Inicio UI", body))


# Consumidores 

@bp.get("/consumidores")
def lista_consumidores():
    rows = db_fetch_all(
        "SELECT id, nombre, email, direccion FROM consumidores ORDER BY id", ()
    )
    body = """
    <h2>Consumidores</h2>
    <p>
      <a class="btn btn-primary" href="{{ url_for('ui.nuevo_consumidor') }}">+ Nuevo</a>
    </p>
    <table>
      <thead>
        <tr>
          <th>ID</th><th>Nombre</th><th>Email</th><th>Dirección</th><th></th>
        </tr>
      </thead>
      <tbody>
      {% for r in rows %}
        <tr>
          <td>{{ r.id }}</td>
          <td>{{ r.nombre }}</td>
          <td>{{ r.email }}</td>
          <td>{{ r.direccion or '' }}</td>
          <td class="actions">
            <a href="{{ url_for('ui.editar_consumidor', cid=r.id) }}">Editar</a>
            <a href="{{ url_for('ui.eliminar_consumidor', cid=r.id) }}">Eliminar</a>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    """
    return _render(_html_layout("Consumidores", body), rows=rows)

@bp.get("/consumidores/nuevo")
@bp.get("/consumidores/new")
def nuevo_consumidor():
    body = """
    <h2>Nuevo consumidor</h2>
    <form method="post" action="{{ url_for('ui.crear_consumidor') }}">
      <div>
        <label>Nombre</label>
        <input type="text" name="nombre" required>
      </div>
      <div>
        <label>Email</label>
        <input type="email" name="email" required>
      </div>
      <div>
        <label>Dirección</label>
        <input type="text" name="direccion">
      </div>
      <div class="mt-16">
        <button class="btn btn-primary" type="submit">Crear</button>
        <a class="btn" href="{{ url_for('ui.lista_consumidores') }}">Cancelar</a>
      </div>
    </form>
    """
    return _render(_html_layout("Nuevo consumidor", body))

@bp.post("/consumidores/nuevo")
@bp.post("/consumidores/new")
def crear_consumidor():
    nombre = request.form.get("nombre") or ""
    email = request.form.get("email") or ""
    direccion = request.form.get("direccion") or None
    if not nombre or not email:
        abort(400)

    exists = db_fetch_one("SELECT id FROM consumidores WHERE email=%s", (email,))
    if exists:
        abort(400)

    db_execute(
        "INSERT INTO consumidores (nombre, email, direccion) VALUES (%s, %s, %s)",
        (nombre, email, direccion),
    )
    return redirect(url_for("ui.lista_consumidores"))

@bp.get("/consumidores/<int:cid>/editar")
@bp.get("/consumidores/<int:cid>/edit")
def editar_consumidor(cid: int):
    row = db_fetch_one(
        "SELECT id, nombre, email, direccion FROM consumidores WHERE id=%s",
        (cid,),
    )
    if not row:
        abort(404)

    body = """
    <h2>Editar consumidor #{{ r.id }}</h2>
    <form method="post" action="{{ url_for('ui.actualizar_consumidor', cid=r.id) }}">
      <div>
        <label>Nombre</label>
        <input type="text" name="nombre" value="{{ r.nombre }}">
      </div>
      <div>
        <label>Email</label>
        <input type="email" name="email" value="{{ r.email }}">
      </div>
      <div>
        <label>Dirección</label>
        <input type="text" name="direccion" value="{{ r.direccion or '' }}">
      </div>
      <div class="mt-16">
        <button class="btn btn-primary" type="submit">Guardar</button>
        <a class="btn" href="{{ url_for('ui.lista_consumidores') }}">Cancelar</a>
      </div>
    </form>
    """
    return _render(_html_layout("Editar consumidor", body), r=row)

@bp.post("/consumidores/<int:cid>/editar")
@bp.post("/consumidores/<int:cid>/edit")
def actualizar_consumidor(cid: int):
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    direccion = request.form.get("direccion")

    exists = db_fetch_one("SELECT id FROM consumidores WHERE id=%s", (cid,))
    if not exists:
        abort(404)

    campos = []
    vals: list[object] = []
    if nombre is not None:
        campos.append("nombre=%s"); vals.append(nombre)
    if email is not None:
        dup = db_fetch_one(
            "SELECT id FROM consumidores WHERE email=%s AND id<>%s",
            (email, cid),
        )
        if dup:
            abort(400)
        campos.append("email=%s"); vals.append(email)
    if direccion is not None:
        campos.append("direccion=%s"); vals.append(direccion)

    if campos:
        vals.append(cid)
        q = f"UPDATE consumidores SET {', '.join(campos)} WHERE id=%s"
        db_execute(q, tuple(vals))

    return redirect(url_for("ui.lista_consumidores"))

@bp.get("/consumidores/<int:cid>/eliminar")
def eliminar_consumidor(cid: int):
    db_execute("DELETE FROM consumidores WHERE id=%s", (cid,))
    return redirect(url_for("ui.lista_consumidores"))

@bp.post("/consumidores/<int:cid>/delete")
def eliminar_consumidor_post(cid: int):
    db_execute("DELETE FROM consumidores WHERE id=%s", (cid,))
    return redirect(url_for("ui.lista_consumidores"))



#  Técnicos 

@bp.get("/tecnicos")
def lista_tecnicos():
    rows = db_fetch_all(
        "SELECT id, nombre, telefono, especialidad FROM tecnicos ORDER BY id", ()
    )
    body = """
    <h2>Técnicos</h2>
    <p>
      <a class="btn btn-primary" href="{{ url_for('ui.nuevo_tecnico') }}">+ Nuevo</a>
    </p>
    <table>
      <thead>
        <tr>
          <th>ID</th><th>Nombre</th><th>Teléfono</th><th>Especialidad</th><th></th>
        </tr>
      </thead>
      <tbody>
      {% for r in rows %}
        <tr>
          <td>{{ r.id }}</td>
          <td>{{ r.nombre }}</td>
          <td>{{ r.telefono or '' }}</td>
          <td>{{ r.especialidad or '' }}</td>
          <td class="actions">
            <a href="{{ url_for('ui.editar_tecnico', tid=r.id) }}">Editar</a>
            <a href="{{ url_for('ui.eliminar_tecnico', tid=r.id) }}">Eliminar</a>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    """
    return _render(_html_layout("Técnicos", body), rows=rows)

@bp.get("/tecnicos/nuevo")
@bp.get("/tecnicos/new")
def nuevo_tecnico():
    body = """
    <h2>Nuevo técnico</h2>
    <form method="post" action="{{ url_for('ui.crear_tecnico') }}">
      <div>
        <label>Nombre</label>
        <input type="text" name="nombre" required>
      </div>
      <div>
        <label>Teléfono</label>
        <input type="text" name="telefono">
      </div>
      <div>
        <label>Especialidad</label>
        <input type="text" name="especialidad">
      </div>
      <div class="mt-16">
        <button class="btn btn-primary" type="submit">Crear</button>
        <a class="btn" href="{{ url_for('ui.lista_tecnicos') }}">Cancelar</a>
      </div>
    </form>
    """
    return _render(_html_layout("Nuevo técnico", body))

@bp.post("/tecnicos/nuevo")
@bp.post("/tecnicos/new")
def crear_tecnico():
    nombre = request.form.get("nombre") or ""
    telefono = request.form.get("telefono") or None
    especialidad = request.form.get("especialidad") or None
    if not nombre:
        abort(400)

    db_execute(
        "INSERT INTO tecnicos (nombre, telefono, especialidad) VALUES (%s, %s, %s)",
        (nombre, telefono, especialidad),
    )
    return redirect(url_for("ui.lista_tecnicos"))

@bp.get("/tecnicos/<int:tid>/editar")
@bp.get("/tecnicos/<int:tid>/edit")
def editar_tecnico(tid: int):
    row = db_fetch_one(
        "SELECT id, nombre, telefono, especialidad FROM tecnicos WHERE id=%s",
        (tid,),
    )
    if not row:
        abort(404)

    body = """
    <h2>Editar técnico #{{ r.id }}</h2>
    <form method="post" action="{{ url_for('ui.actualizar_tecnico', tid=r.id) }}">
      <div>
        <label>Nombre</label>
        <input type="text" name="nombre" value="{{ r.nombre }}">
      </div>
      <div>
        <label>Teléfono</label>
        <input type="text" name="telefono" value="{{ r.telefono or '' }}">
      </div>
      <div>
        <label>Especialidad</label>
        <input type="text" name="especialidad" value="{{ r.especialidad or '' }}">
      </div>
      <div class="mt-16">
        <button class="btn btn-primary" type="submit">Guardar</button>
        <a class="btn" href="{{ url_for('ui.lista_tecnicos') }}">Cancelar</a>
      </div>
    </form>
    """
    return _render(_html_layout("Editar técnico", body), r=row)


@bp.post("/tecnicos/<int:tid>/editar")
@bp.post("/tecnicos/<int:tid>/edit")
def actualizar_tecnico(tid: int):
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")
    especialidad = request.form.get("especialidad")

    exists = db_fetch_one("SELECT id FROM tecnicos WHERE id=%s", (tid,))
    if not exists:
        abort(404)

    campos = []
    vals: list[object] = []
    if nombre is not None:
        campos.append("nombre=%s"); vals.append(nombre)
    if telefono is not None:
        campos.append("telefono=%s"); vals.append(telefono)
    if especialidad is not None:
        campos.append("especialidad=%s"); vals.append(especialidad)

    if campos:
        vals.append(tid)
        q = f"UPDATE tecnicos SET {', '.join(campos)} WHERE id=%s"
        db_execute(q, tuple(vals))

    return redirect(url_for("ui.lista_tecnicos"))

@bp.get("/tecnicos/<int:tid>/eliminar")
def eliminar_tecnico(tid: int):
    db_execute("DELETE FROM tecnicos WHERE id=%s", (tid,))
    return redirect(url_for("ui.lista_tecnicos"))

@bp.post("/tecnicos/<int:tid>/delete")
def eliminar_tecnico_post(tid: int):
    db_execute("DELETE FROM tecnicos WHERE id=%s", (tid,))
    return redirect(url_for("ui.lista_tecnicos"))



# Administradores 

@bp.get("/administradores")
def lista_admins():
    rows = db_fetch_all("SELECT id, nombre, email FROM administradores ORDER BY id", ())
    body = """
    <h2>Administradores</h2>
    <p>
      <a class="btn btn-primary" href="{{ url_for('ui.nuevo_admin') }}">+ Nuevo</a>
    </p>
    <table>
      <thead>
        <tr><th>ID</th><th>Nombre</th><th>Email</th><th></th></tr>
      </thead>
      <tbody>
      {% for r in rows %}
        <tr>
          <td>{{ r.id }}</td>
          <td>{{ r.nombre }}</td>
          <td>{{ r.email }}</td>
          <td class="actions">
            <a href="{{ url_for('ui.editar_admin', aid=r.id) }}">Editar</a>
            <a href="{{ url_for('ui.eliminar_admin', aid=r.id) }}">Eliminar</a>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    """
    return _render(_html_layout("Administradores", body), rows=rows)

@bp.get("/administradores/nuevo")
@bp.get("/administradores/new")
def nuevo_admin():
    body = """
    <h2>Nuevo administrador</h2>
    <form method="post" action="{{ url_for('ui.crear_admin') }}">
      <div>
        <label>Nombre</label>
        <input type="text" name="nombre" required>
      </div>
      <div>
        <label>Email</label>
        <input type="email" name="email" required>
      </div>
      <div class="mt-16">
        <button class="btn btn-primary" type="submit">Crear</button>
        <a class="btn" href="{{ url_for('ui.lista_admins') }}">Cancelar</a>
      </div>
    </form>
    """
    return _render(_html_layout("Nuevo administrador", body))

@bp.post("/administradores/nuevo")
@bp.post("/administradores/new")
def crear_admin():
    nombre = request.form.get("nombre") or ""
    email = request.form.get("email") or ""
    if not nombre or not email:
        abort(400)

    dup = db_fetch_one("SELECT id FROM administradores WHERE email=%s", (email,))
    if dup:
        abort(400)

    db_execute(
        "INSERT INTO administradores (nombre, email) VALUES (%s, %s)",
        (nombre, email),
    )
    return redirect(url_for("ui.lista_admins"))

@bp.get("/administradores/<int:aid>/editar")
@bp.get("/administradores/<int:aid>/edit")
def editar_admin(aid: int):
    row = db_fetch_one(
        "SELECT id, nombre, email FROM administradores WHERE id=%s",
        (aid,),
    )
    if not row:
        abort(404)

    body = """
    <h2>Editar administrador #{{ r.id }}</h2>
    <form method="post" action="{{ url_for('ui.actualizar_admin', aid=r.id) }}">
      <div>
        <label>Nombre</label>
        <input type="text" name="nombre" value="{{ r.nombre }}">
      </div>
      <div>
        <label>Email</label>
        <input type="email" name="email" value="{{ r.email }}">
      </div>
      <div class="mt-16">
        <button class="btn btn-primary" type="submit">Guardar</button>
        <a class="btn" href="{{ url_for('ui.lista_admins') }}">Cancelar</a>
      </div>
    </form>
    """
    return _render(_html_layout("Editar administrador", body), r=row)

@bp.post("/administradores/<int:aid>/editar")
@bp.post("/administradores/<int:aid>/edit")
def actualizar_admin(aid: int):
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    exists = db_fetch_one("SELECT id FROM administradores WHERE id=%s", (aid,))
    if not exists:
        abort(404)

    if email is not None:
        dup = db_fetch_one(
            "SELECT id FROM administradores WHERE email=%s AND id<>%s",
            (email, aid),
        )
        if dup:
            abort(400)

    campos = []
    vals: list[object] = []
    if nombre is not None:
        campos.append("nombre=%s"); vals.append(nombre)
    if email is not None:
        campos.append("email=%s"); vals.append(email)

    if campos:
        vals.append(aid)
        q = f"UPDATE administradores SET {', '.join(campos)} WHERE id=%s"
        db_execute(q, tuple(vals))

    return redirect(url_for("ui.lista_admins"))

@bp.get("/administradores/<int:aid>/eliminar")
def eliminar_admin(aid: int):
    db_execute("DELETE FROM administradores WHERE id=%s", (aid,))
    return redirect(url_for("ui.lista_admins"))

@bp.post("/administradores/<int:aid>/delete")
def eliminar_admin_post(aid: int):
    db_execute("DELETE FROM administradores WHERE id=%s", (aid,))
    return redirect(url_for("ui.lista_admins"))

