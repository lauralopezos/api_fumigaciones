def test_crud_admins(client):
    r = client.post("/administradores", json={
        "nombre": "Laura", "email": "laura@empresa.com"
    })
    assert r.status_code == 201
    aid = r.get_json()["id"]

    assert client.get("/administradores").status_code == 200
    assert client.get(f"/administradores/{aid}").status_code == 200
    assert client.put(
        f"/administradores/{aid}",
        json={
            "email": "nuevo@empresa.com"}).status_code == 200
    assert client.delete(f"/administradores/{aid}").status_code == 200
    assert client.get(f"/administradores/{aid}").status_code == 404
