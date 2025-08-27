def test_ui_listas(client):
    assert client.get("/ui/consumidores").status_code == 200
    assert client.get("/ui/tecnicos").status_code == 200
    assert client.get("/ui/administradores").status_code == 200

def test_ui_nuevos_forms(client):
    assert client.get("/ui/consumidores/new").status_code == 200
    assert client.get("/ui/tecnicos/new").status_code == 200
    assert client.get("/ui/administradores/new").status_code == 200
