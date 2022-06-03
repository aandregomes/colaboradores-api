from factories.cargos_factory import cria_cargos
from factories.colaboradores_factory import cria_colaboradores


class TestCargosApi:

    def test_get_cargos_200(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.get('/cargos')

        assert response.status_code == 200
        assert len(response.json) > 0

    def test_post_cargo_201(self, app):
        client = app.test_client()
        response = client.post('/cargos', json={
            "cargo": "Developer",
            "lider": False
        })

        assert response.status_code == 201
        assert response.json["cargo"] == "developer"

    def test_post_cargo_400(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.post('/cargos', json={"cargo": "developer i"})

        assert response.status_code == 409
        assert response.json["message"] == 'Cargo com este nome já existe.'

    def test_get_cargo_por_id_200(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.get('/cargos/1')

        assert response.status_code == 200
        assert response.json["id"] == 1

    def test_get_cargo_por_id_404(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.get('/cargos/42')

        assert response.status_code == 404
        assert 'Cargo não encontrado' in response.json["message"]

    def test_patch_cargo_por_id_200(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.patch('/cargos/1', json={"cargo": "novo cargo"})

        assert response.status_code == 200
        assert response.json["cargo"] == "novo cargo"

    def test_patch_cargo_por_id_404(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.patch('/cargos/42', json={"cargo": "novo cargo"})

        assert response.status_code == 404
        assert 'Cargo não encontrado' in response.json["message"]

    def test_patch_cargo_por_id_409(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.patch('/cargos/2', json={"cargo": "tech lead"})

        assert response.status_code == 409
        assert response.json["message"] == 'Cargo com este nome já existe.'

    def test_delete_cargo_por_id_204(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.delete('/cargos/1')

        assert response.status_code == 204

    def test_delete_cargo_por_id_404(self, app):
        cria_cargos()
        client = app.test_client()
        response = client.delete('/cargos/42')

        assert response.status_code == 404
        assert 'Cargo não encontrado' in response.json["message"]

    def test_delete_cargo_por_id_409(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.delete('/cargos/1')

        assert response.status_code == 409
        assert response.json["message"] == 'Há colaboradores com esse cargo'
