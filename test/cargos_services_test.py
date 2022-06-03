from core.services.cargos.cargos_services import verifica_se_ha_colaboradores_com_cargo
from factories.cargos_factory import cria_cargos
from factories.colaboradores_factory import cria_colaboradores


class TestCargosServices:

    def test_verifica_se_ha_colaboradores_com_cargo(self, app):
        cria_cargos()
        cria_colaboradores()
        app.test_client()
        resposta = verifica_se_ha_colaboradores_com_cargo(1)

        assert resposta is True

    def test_verifica_se_ha_colaboradores_com_cargo_invalido(self, app):
        cria_cargos()
        cria_colaboradores()
        app.test_client()
        resposta = verifica_se_ha_colaboradores_com_cargo(42)

        assert resposta is False
