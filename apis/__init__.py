from flask_restx import Api
from .colaboradores import api as ns_colaboradores
from .cargos import api as ns_cargos

api = Api(
    title='Aquarela Users API',
    version='1.0',
    description='Uma API simples para Criar, Ler, Atualizar e Deleter (CRUD) usuários de um Banco de Dados',
)

api.add_namespace(ns_colaboradores)
api.add_namespace(ns_cargos)
