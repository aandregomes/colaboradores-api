from factories.cargos_factory import cria_cargos
from factories.colaboradores_factory import cria_colaborador


class TestColaboradorAlterarSenha:
    def test_colaborador_alterar_senha_200(self, app):
        cria_cargos()
        cria_colaborador()
        data = {
            "senha_atual": "senha123",
            "nova_senha": "senhaMaisdificiL321"
        }
        client = app.test_client()
        response = client.patch(
            '/colaboradores/12345/alterar-senha',
            json=data
        )
        assert response.status_code == 200
        assert response.json == 'Senha alterada com sucesso!'
