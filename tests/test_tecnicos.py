def test_crud_tecnicos(client):
    r = client.post("/tecnicos", json={
        "nombre": "Pedro", "telefono": "3001234567", "especialidad": "Plagas"
    })
    assert r.status_code == 201
    tid = r.get_json()["id"]

    assert client.get("/tecnicos").status_code == 200
    assert client.get(f"/tecnicos/{tid}").status_code == 200
    assert client.put(
        f"/tecnicos/{tid}",
        json={
            "telefono": "3010000000"}).status_code == 200
    assert client.delete(f"/tecnicos/{tid}").status_code == 200
    assert client.get(f"/tecnicos/{tid}").status_code == 404
