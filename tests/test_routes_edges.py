def test_consumidores_edges(client):
    # crear sin nombre/email -> 400
    assert client.post("/consumidores", json={"nombre": ""}).status_code == 400

    # crear válido
    r = client.post("/consumidores", json={
        "nombre": "A", "email": "a@x.com", "direccion": ""
    })
    assert r.status_code == 201
    cid = r.get_json()["id"]

    # duplicado email -> 400
    assert client.post("/consumidores", json={
        "nombre": "B", "email": "a@x.com"
    }).status_code == 400

    # update inexistente -> 404
    assert client.put("/consumidores/999999",
                      json={"nombre": "Z"}).status_code == 404

    # update sin campos -> 400
    assert client.put(f"/consumidores/{cid}", json={}).status_code == 400

    # update email duplicado -> 400
    client.post("/consumidores", json={
        "nombre": "C", "email": "c@x.com", "direccion": ""
    })
    assert client.put(
        f"/consumidores/{cid}",
        json={
            "email": "c@x.com"}).status_code == 400

    # delete inexistente -> 404
    assert client.delete("/consumidores/999999").status_code == 404


def test_tecnicos_edges(client):
    # update inexistente -> 404
    assert client.put("/tecnicos/999999",
                      json={"nombre": "Z"}).status_code == 404
    # delete inexistente -> 404
    assert client.delete("/tecnicos/999999").status_code == 404


def test_admins_edges(client):
    # crear sin nombre/email -> 400
    assert client.post("/administradores",
                       json={"nombre": "X"}).status_code == 400

    # crear OK
    r = client.post(
        "/administradores",
        json={
            "nombre": "L",
            "email": "l@x.com"})
    assert r.status_code == 201
    aid = r.get_json()["id"]

    # duplicado email -> 400
    assert client.post(
        "/administradores",
        json={
            "nombre": "L2",
            "email": "l@x.com"}).status_code == 400

    # update inexistente -> 404
    assert client.put("/administradores/999999",
                      json={"email": "n@x.com"}).status_code == 404

    # update sin cambios -> 400
    assert client.put(f"/administradores/{aid}", json={}).status_code == 400

    # update email duplicado -> 400
    client.post("/administradores", json={"nombre": "M", "email": "m@x.com"})
    assert client.put(
        f"/administradores/{aid}",
        json={
            "email": "m@x.com"}).status_code == 400

    # delete inexistente -> 404
    assert client.delete("/administradores/999999").status_code == 404
