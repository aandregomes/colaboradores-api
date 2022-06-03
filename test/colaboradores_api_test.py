from factories.cargos_factory import cria_cargos
from factories.colaboradores_factory import cria_colaboradores


class TestColaboradoresApi:

    def test_get_colaboradores_200(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.get('/colaboradores/')

        assert response.status_code == 200
        assert len(response.json) > 0

    def test_post_colaborador_201(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula": 99999,
            "nome": "Novo colaborador",
            "sobrenome": "Novo colaborador",
            "cargo_id": 3,
            "matricula_lider": 12345,
            "salario": 7500.0,
            "senha": "senha123"
        }
        client = app.test_client()
        response = client.post('/colaboradores/', json=data)

        assert response.status_code == 201

    def test_post_colaborador_400_lider_nao_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula": 99999,
            "nome": "Novo colaborador",
            "sobrenome": "Novo colaborador",
            "cargo_id": 3,
            "matricula_lider": 42,
            "salario": 7500.0,
            "senha": "senha123"
        }
        client = app.test_client()
        response = client.post('/colaboradores/', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O líder informado não existe'

    def test_post_colaborador_400_lider_nao_lider(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula": 99999,
            "nome": "Novo colaborador",
            "sobrenome": "Novo colaborador",
            "cargo_id": 3,
            "matricula_lider": 23456,
            "salario": 7500.0,
            "senha": "senha123"
        }
        client = app.test_client()
        response = client.post('/colaboradores/', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O líder informado não tem cargo de liderança'

    def test_post_colaborador_400_cargo_nao_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula": 99999,
            "nome": "Novo colaborador",
            "sobrenome": "Novo colaborador",
            "cargo_id": 42,
            "matricula_lider": 12345,
            "salario": 7500.0,
            "senha": "senha123"
        }
        client = app.test_client()
        response = client.post('/colaboradores/', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O cargo_id informado não existe'

    def test_post_colaborador_409(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula": 23456,
            "nome": "Novo colaborador",
            "sobrenome": "Novo colaborador",
            "cargo_id": 3,
            "matricula_lider": 12345,
            "salario": 7500.0,
            "senha": "senha123"
        }
        client = app.test_client()
        response = client.post('/colaboradores/', json=data)

        assert response.status_code == 409
        assert response.json["message"] == 'Colaborador com essa matrícula já existe'

    def test_get_colaborador_por_matricula_200(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.get('/colaboradores/12345')

        assert response.status_code == 200
        assert len(response.json) > 0

    def test_get_colaborador_por_matricula_404(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.get('/colaboradores/42')

        assert response.status_code == 404
        assert 'Colaborador não encontrado' in response.json["message"]

    def test_patch_colaborador_por_matricula_200(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "nome": "Novo nome",
            "sobrenome": "Novo sobrenome",
        }
        client = app.test_client()
        response = client.patch('/colaboradores/12345', json=data)

        assert response.status_code == 200
        assert response.json["nome"] == "Novo nome"
        assert response.json["sobrenome"] == "Novo sobrenome"

    def test_patch_colaborador_por_matricula_400_lider_nao_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "nome": "Novo nome",
            "sobrenome": "Novo sobrenome",
            "matricula_lider": 42,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/12345', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O líder informado não existe'

    def test_patch_colaborador_por_matricula_400_lider_nao_lider(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "nome": "Novo nome",
            "sobrenome": "Novo sobrenome",
            "matricula_lider": 23456,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/12345', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O líder informado não tem cargo de liderança'

    def test_patch_colaborador_por_matricula_400_cargo_nao_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "nome": "Novo nome",
            "sobrenome": "Novo sobrenome",
            "cargo_id": 42,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/12345', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O cargo_id informado não existe'

    def test_patch_colaborador_por_matricula_404(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "nome": "Novo nome",
            "sobrenome": "Novo sobrenome",
        }
        client = app.test_client()
        response = client.patch('/colaboradores/42', json=data)

        assert response.status_code == 404
        assert 'Colaborador não encontrado' in response.json["message"]

    def test_delete_colaborador_por_matricula_204(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.delete('/colaboradores/23456')

        assert response.status_code == 204

    def test_delete_colaborador_por_matricula_204(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.delete('/colaboradores/42')

        assert response.status_code == 404
        assert 'Colaborador não encontrado' in response.json["message"]

    def test_colaborador_demissao_200(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.patch('/colaboradores/23456/demissao')

        assert response.status_code == 200
        assert response.json["status_ativo"] is False

    def test_colaborador_demissao_404(self, app):
        cria_cargos()
        cria_colaboradores()
        client = app.test_client()
        response = client.patch('/colaboradores/42/demissao')

        assert response.status_code == 404
        assert 'Colaborador não encontrado' in response.json["message"]

    def test_colaborador_promocao_200(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 3,
            "matricula_lider": 34567,
            "salario": 7500.0,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/23456/promocao', json=data)

        assert response.status_code == 200
        assert response.json["cargo_id"] == 3
        assert response.json["matricula_lider"] == 34567
        assert response.json["salario"] == 7500.0

    def test_colaborador_promocao_400_lider_nao_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 3,
            "matricula_lider": 42,
            "salario": 7500.0,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/23456/promocao', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O líder informado não existe'

    def test_colaborador_promocao_400_lider_nao_lider(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 3,
            "matricula_lider": 45678,
            "salario": 7500.0,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/23456/promocao', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O líder informado não tem cargo de liderança'

    def test_colaborador_promocao_400_lider_nao_lider(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 42,
            "matricula_lider": 34567,
            "salario": 7500.0,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/23456/promocao', json=data)

        assert response.status_code == 400
        assert response.json["message"] == 'O cargo_id informado não existe'

    def test_colaborador_promocao_400_lider_nao_lider(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 3,
            "matricula_lider": 34567,
            "salario": 7500.0,
        }
        client = app.test_client()
        response = client.patch('/colaboradores/42/promocao', json=data)

        assert response.status_code == 404
        assert 'Colaborador não encontrado' in response.json["message"]
