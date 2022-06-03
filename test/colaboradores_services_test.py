from core.services.coloboradores.colaboradores_services import *
from factories.colaboradores_factory import cria_colaboradores
from factories.cargos_factory import cria_cargos


class TestColaboradoresServices:

    def test_get_hashed_password(self):
        senha = "senha123"
        senha_hashed = get_hashed_password(senha)

        assert isinstance(senha_hashed, str)
        assert len(senha_hashed) > len(senha)

    def test_check_password(self):
        senha = "senha123"
        senha_hashed = get_hashed_password(senha)
        verifica = check_password(senha, senha_hashed)

        assert verifica is True

    def test_verifica_se_lider_enviado_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula_lider": 12345,
        }
        app.test_client()
        resposta = verifica_se_lider_enviado_existe(data)

        assert resposta is True

    def test_verifica_se_lider_enviado_existe_invalido(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula_lider": 42,
        }
        app.test_client()
        resposta = verifica_se_lider_enviado_existe(data)

        assert resposta is False

    def test_verifica_se_lider_pode_ser_lider(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula_lider": 12345,
        }
        app.test_client()
        resposta = verifica_se_lider_pode_ser_lider(data)

        assert resposta is True

    def test_verifica_se_lider_pode_ser_lider_invalido(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "matricula_lider": 23456,
        }
        app.test_client()
        resposta = verifica_se_lider_pode_ser_lider(data)

        assert resposta is False

    def test_verifica_se_cargo_enviado_existe(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 1,
        }
        app.test_client()
        resposta = verifica_se_cargo_enviado_existe(data)

        assert resposta is True

    def test_verifica_se_cargo_enviado_existe_invalido(self, app):
        cria_cargos()
        cria_colaboradores()
        data = {
            "cargo_id": 42,
        }
        app.test_client()
        resposta = verifica_se_cargo_enviado_existe(data)

        assert resposta is False
