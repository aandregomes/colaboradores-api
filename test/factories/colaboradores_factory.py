from turtle import update
from core.models.colaboradores import Colaboradores
from core.services.coloboradores.colaboradores_services import get_hashed_password


mock_colaboradores = [
    {
        "matricula": 12345,
        "nome": "Nome Lider",
        "sobrenome": "Sobrenome Lider",
        "cargo_id": 1,
        "salario": 10000.0,
        "senha": "senha123"
    },
    {
        "matricula": 23456,
        "nome": "Nome Subordinado",
        "sobrenome": "Sobrenome Subordinado",
        "cargo_id": 2,
        "matricula_lider": 12345,
        "salario": 5000.0,
        "senha": "senha123"
    },
    {
        "matricula": 34567,
        "nome": "Nome Outro Lider",
        "sobrenome": "Sobrenome Outro Lider",
        "cargo_id": 1,
        "salario": 20000.0,
        "senha": "senha123"
    },
    {
        "matricula": 45678,
        "nome": "Nome Outro Subordinado",
        "sobrenome": "Sobrenome Outro Subordinado",
        "cargo_id": 2,
        "matricula_lider": 34567,
        "salario": 3000.0,
        "senha": "senha123"
    },
]


def cria_colaboradores():
    for mock_colaborador in mock_colaboradores:
        mock_colaborador.update(
            {"senha": get_hashed_password(mock_colaborador["senha"])})
        colaborador = Colaboradores(**mock_colaborador)
        colaborador.save()


def cria_colaborador():
    col = {
        "matricula": 12345,
        "nome": "Nome Lider",
        "sobrenome": "Sobrenome Lider",
        "cargo_id": 1,
        "salario": 10000.0,
        "senha": "senha123"
    }
    col.update({"senha": get_hashed_password(col["senha"])})
    colaborador = Colaboradores(**col)
    colaborador.save()
