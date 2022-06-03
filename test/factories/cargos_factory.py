from core.models.cargos import Cargos


mock_cargos = [
    {
        "cargo": "tech lead",
        "lider": True
    },
    {
        "cargo": "developer i",
        "lider": False
    },
    {
        "cargo": "developer ii",
        "lider": False
    },
    {
        "cargo": "developer iii",
        "lider": False
    },
    {
        "cargo": "developer specialist",
        "lider": False
    }
]


def cria_cargos():
    for mock_cargo in mock_cargos:
        cargo = Cargos(**mock_cargo)
        cargo.save()
