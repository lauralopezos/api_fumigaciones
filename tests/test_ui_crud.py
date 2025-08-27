def crea_consumidor_por_ui(client, nombre, email, direccion):
    r = client.post("/ui/consumidores/new", data={
        "nombre": nombre, "email": email, "direccion": direccion
    }, follow_redirects=True)
    assert r.status_code == 200  # redirecciona a lista

    # Usa la API para tomar el id del último
    j = client.get("/consumidores").get_json()
    cid = max(x["id"] for x in j)  # asumiendo autoincrement
    return cid

def test_ui_consumidores_crud(client):
    # Crear
    cid = crea_consumidor_por_ui(client, "Ana", "ana@ui.com", "Calle 1")

    # Editar (GET)
    assert client.get(f"/ui/consumidores/{cid}/edit").status_code == 200
    # Editar (POST)
    r = client.post(f"/ui/consumidores/{cid}/edit", data={
        "nombre": "Ana Mod", "email": "ana@ui.com", "direccion": "Calle 2"
    }, follow_redirects=True)
    assert r.status_code == 200

    # Eliminar
    r = client.post(f"/ui/consumidores/{cid}/delete", follow_redirects=True)
    assert r.status_code == 200

    # Ya no debe existir (vista de edición 404 y API 404)
    assert client.get(f"/ui/consumidores/{cid}/edit").status_code == 404
    assert client.get(f"/consumidores/{cid}").status_code == 404

def test_ui_tecnicos_crud(client):
    # Crear por UI
    r = client.post("/ui/tecnicos/new", data={
        "nombre": "Pedro", "telefono": "3001112222", "especialidad": "Plagas"
    }, follow_redirects=True)
    assert r.status_code == 200
    # Tomamos id por API
    tid = max(x["id"] for x in client.get("/tecnicos").get_json())

    # Editar
    assert client.get(f"/ui/tecnicos/{tid}/edit").status_code == 200
    r = client.post(f"/ui/tecnicos/{tid}/edit", data={
        "nombre": "Pedro M", "telefono": "3009998888", "especialidad": "Termitas"
    }, follow_redirects=True)
    assert r.status_code == 200

    # Eliminar
    r = client.post(f"/ui/tecnicos/{tid}/delete", follow_redirects=True)
    assert r.status_code == 200
    assert client.get(f"/tecnicos/{tid}").status_code == 404

def test_ui_admins_crud(client):
    # Crear
    r = client.post("/ui/administradores/new", data={
        "nombre": "Laura", "email": "laura@ui.com"
    }, follow_redirects=True)
    assert r.status_code == 200
    aid = max(x["id"] for x in client.get("/administradores").get_json())

    # Editar
    assert client.get(f"/ui/administradores/{aid}/edit").status_code == 200
    r = client.post(f"/ui/administradores/{aid}/edit", data={
        "nombre": "Laura M", "email": "laura@ui.com"
    }, follow_redirects=True)
    assert r.status_code == 200

    # Eliminar
    r = client.post(f"/ui/administradores/{aid}/delete", follow_redirects=True)
    assert r.status_code == 200
    assert client.get(f"/administradores/{aid}").status_code == 404
