from flask import request
from flask_api import status
from flask_restx import Namespace, Resource, fields
from core.models.cargos import Cargos
from core.services.cargos.cargos_services import verifica_se_ha_colaboradores_com_cargo


api = Namespace('cargos', description='Operações relacionadas aos cargos')


cargos_model = api.model('Cargos', {
    'id': fields.Integer(
        readonly=True,
        description='Identificador do cargo'
    ),
    'cargo': fields.String(
        required=True,
        description='Nome do cargo'
    ),
    'lider': fields.Boolean(
        required=False,
        default=False,
        description='Se o cargo é de liderança'
    )
})

atualiza_cargos_model = api.model('Cargos', {
    'id': fields.Integer(
        readonly=True,
        description='Identificador do cargo'
    ),
    'cargo': fields.String(
        required=False,
        description='Nome do cargo'
    ),
    'lider': fields.Boolean(
        required=False,
        default=False,
        description='Se o cargo é de liderança'
    )
})


@api.route('')
class CargosResource(Resource):
    '''Retorna todos os cargos e cria cargos novos'''

    @api.doc('list_cargos')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.marshal_list_with(cargos_model, code=status.HTTP_200_OK)
    def get(self):
        '''Lista de todos os cargos'''
        lista_de_cargos = Cargos.query.all()
        return lista_de_cargos, status.HTTP_200_OK

    @api.doc('create_cargo')
    @api.response(status.HTTP_409_CONFLICT, 'Cargo com este nome já existe.')
    @api.expect(cargos_model, validate=True)
    @api.marshal_with(cargos_model, code=status.HTTP_201_CREATED)
    def post(self):
        '''Criação de um cargos'''
        data = request.json
        if Cargos.query.filter_by(cargo=data.get('cargo').lower()).first():
            api.abort(
                status.HTTP_409_CONFLICT,
                'Cargo com este nome já existe.'
            )
        novo_cargo = Cargos(**data)
        novo_cargo.save()
        return novo_cargo, status.HTTP_201_CREATED


@api.route('/<int:cargo_id>')
class CargosItemResource(Resource):
    '''Retorna, atualiza e exclui um cargo específico'''

    @api.doc('get_cargo')
    @api.response(status.HTTP_404_NOT_FOUND, 'Cargo não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.marshal_with(cargos_model, code=status.HTTP_200_OK)
    def get(self, cargo_id):
        '''Retorna informações do cargo'''
        cargo = Cargos.query.filter_by(id=cargo_id).first()

        if not cargo:
            api.abort(status.HTTP_404_NOT_FOUND, 'Cargo não encontrado')

        return cargo, status.HTTP_200_OK

    @api.doc('update_cargo')
    @api.response(status.HTTP_409_CONFLICT, 'Cargo com este nome já existe.')
    @api.response(status.HTTP_404_NOT_FOUND, 'Cargo não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.expect(atualiza_cargos_model, validate=True, skip_none=True)
    @api.marshal_with(atualiza_cargos_model, code=status.HTTP_200_OK)
    def patch(self, cargo_id):
        '''Atualiza nome do cargo e/ou se é de liderança'''
        data = request.json

        query_cargo = Cargos.query.filter_by(id=cargo_id)
        if not query_cargo.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Cargo não encontrado')

        if Cargos.query.filter_by(
            cargo=(data['cargo'].lower() if data.get('cargo', False) else "")
        ).first():
            """
            Verifica se o nome do cargo já existe:
            antes de buscar faz o lower() do nome do cargo enviado caso seja enviado
            """
            api.abort(
                status.HTTP_409_CONFLICT,
                'Cargo com este nome já existe.'
            )

        query_cargo.update(data)
        Cargos.commit()
        return query_cargo.first(), status.HTTP_200_OK

    @api.doc('delete_cargo')
    @api.response(status.HTTP_204_NO_CONTENT, 'Sucesso (Sem conteúdo)')
    @api.response(status.HTTP_409_CONFLICT, 'Há colaboradores com esse cargo')
    @api.response(status.HTTP_404_NOT_FOUND, 'Cargo não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    def delete(self, cargo_id):
        '''Exclusão de cargo'''
        query_cargo = Cargos.query.filter_by(id=cargo_id)
        if not query_cargo.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Cargo não encontrado')
        if verifica_se_ha_colaboradores_com_cargo(cargo_id):
            api.abort(status.HTTP_409_CONFLICT,
                      'Há colaboradores com esse cargo')
        query_cargo.delete()
        Cargos.commit()
        return "", status.HTTP_204_NO_CONTENT
