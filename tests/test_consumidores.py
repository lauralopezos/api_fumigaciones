def test_crud_consumidores(client):
    # CREATE
    r = client.post("/consumidores", json={
        "nombre": "Ana", "email": "ana@demo.com", "direccion": "Calle 1"
    })
    assert r.status_code == 201
    cid = r.get_json()["id"]

    # LIST
    r = client.get("/consumidores")
    assert r.status_code == 200
    assert any(x["id"] == cid for x in r.get_json())

    # GET ONE
    r = client.get(f"/consumidores/{cid}")
    assert r.status_code == 200
    assert r.get_json()["email"] == "ana@demo.com"

    # UPDATE
    r = client.put(f"/consumidores/{cid}", json={"direccion": "Calle 2"})
    assert r.status_code == 200

    # DELETE
    r = client.delete(f"/consumidores/{cid}")
    assert r.status_code == 200

    # 404 after delete
    r = client.get(f"/consumidores/{cid}")
    assert r.status_code == 404
