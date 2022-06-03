from flask import request
from flask_api import status
from flask_restx import Namespace, Resource, fields
from core.models.colaboradores import Colaboradores
from core.services.coloboradores.colaboradores_services import check_password, get_hashed_password, verifica_se_cargo_enviado_existe, verifica_se_lider_enviado_existe, verifica_se_lider_pode_ser_lider


api = Namespace(
    'colaboradores',
    description='Operações relacionadas ao colaborador'
)

colaboradores_model = api.model('Colaboradores', {
    'matricula': fields.Integer(
        required=True,
        description='Identificador do colaborador'
    ),
    'nome': fields.String(
        required=True,
        description='Nome do colaborador'
    ),
    'sobrenome': fields.String(
        required=True,
        description='Sobrenome do colaborador'
    ),
    'cargo_id': fields.Integer(
        required=True,
        description='Identificador do cargo'
    ),
    'cargo': fields.String(
        readonly=True,
        description='Nome do cargo'
    ),
    'matricula_lider': fields.Integer(
        required=False,
        description='Identificador do lider'
    ),
    'nome_lider': fields.String(
        readonly=True,
        description='Nome do lider'
    ),
    'salario': fields.Float(
        required=True,
        description='Salário do colaborador'
    ),
    'status_ativo': fields.Boolean(
        required=False,
        default=True,
        description='Se o colaborador está ativo'
    )
})

post_colaboradores_model = api.model('PostColaboradores', {
    'matricula': fields.Integer(
        required=True,
        description='Identificador do colaborador'
    ),
    'nome': fields.String(
        required=True,
        description='Nome do colaborador'
    ),
    'sobrenome': fields.String(
        required=True,
        description='Sobrenome do colaborador'
    ),
    'cargo_id': fields.Integer(
        required=True,
        description='Identificador do cargo'
    ),
    'matricula_lider': fields.Integer(
        required=False,
        description='Identificador do lider'
    ),
    'salario': fields.Float(
        required=True,
        description='Salário do colaborador'
    ),
    'senha': fields.String(
        required=True,
        description='Senha'
    ),
    'status_ativo': fields.Boolean(
        required=False,
        default=True,
        description='Se o colaborador está ativo'
    )
})

atualiza_colaboradores_model = api.model('AtualizaColaboradores', {
    'matricula': fields.Integer(
        required=False,
        description='Identificador do colaborador'
    ),
    'nome': fields.String(
        required=False,
        description='Nome do colaborador'
    ),
    'sobrenome': fields.String(
        required=False,
        description='Sobrenome do colaborador'
    ),
    'cargo_id': fields.Integer(
        required=False,
        description='Identificador do cargo'
    ),
    'matricula_lider': fields.Integer(
        required=False,
        description='Identificador do lider'
    ),
    'salario': fields.Float(
        required=False,
        description='Salário do colaborador'
    ),
    'status_ativo': fields.Boolean(
        required=False,
        default=True,
        description='Se o colaborador está ativo'
    )
})

promove_colaborador_model = api.model('PromoveColaborador', {
    'cargo_id': fields.Integer(
        required=False,
        description='Identificador do cargo'
    ),
    'matricula_lider': fields.Integer(
        required=False,
        description='Identificador do lider'
    ),
    'salario': fields.Float(
        required=False,
        description='Salário do colaborador'
    )
})


alteracao_de_senha_model = api.model('AlteraSenhaColaborador', {
    'senha_atual': fields.String(
        required=True,
        description='Senha atual'
    ),
    'nova_senha': fields.String(
        required=True,
        description='Nova senha'
    ),
})


@api.route('/')
class ColaboradoresResource(Resource):
    '''Retorna todos os cargos e cria cargos novos'''

    @api.doc('list_colaboradores')
    @ api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @ api.marshal_list_with(colaboradores_model, code=status.HTTP_200_OK)
    def get(self):
        '''Lista de todos os colaboradores'''
        lista_de_usuarios = Colaboradores.query.all()
        return lista_de_usuarios, status.HTTP_200_OK

    @ api.doc('create_colaboradores')
    @api.response(status.HTTP_400_BAD_REQUEST, 'Informações enviadas não aceitas')
    @ api.response(status.HTTP_409_CONFLICT, 'Colaborador com essa matrícula já existe')
    @ api.expect(post_colaboradores_model, validate=True)
    @ api.marshal_with(colaboradores_model, code=status.HTTP_201_CREATED)
    def post(self):
        '''Criação de um usuário'''
        data = request.json
        data.update({"senha": get_hashed_password(data["senha"])})
        if Colaboradores.query.filter_by(matricula=data.get("matricula")).first():
            api.abort(
                status.HTTP_409_CONFLICT,
                'Colaborador com essa matrícula já existe'
            )
        if not verifica_se_lider_enviado_existe(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O líder informado não existe'
            )
        if not verifica_se_lider_pode_ser_lider(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O líder informado não tem cargo de liderança'
            )
        if not verifica_se_cargo_enviado_existe(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O cargo_id informado não existe'
            )
        novo_colaborador = Colaboradores(**data)
        novo_colaborador.save()
        return novo_colaborador, status.HTTP_201_CREATED


@api.route('/<int:matricula>')
class ColaboradoresItemResource(Resource):
    '''Retorna, atualiza e exclui um colaborador específico'''

    @api.doc('get_colaborador')
    @api.response(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.marshal_with(colaboradores_model, code=status.HTTP_200_OK)
    def get(self, matricula):
        '''Busca um colaborador por matrícula'''
        colaborador = Colaboradores.query.filter_by(
            matricula=matricula).first()
        if not colaborador:
            api.abort(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
        return colaborador, status.HTTP_200_OK

    @api.doc('update_colaborador')
    @api.response(status.HTTP_400_BAD_REQUEST, 'Informações enviadas não aceitas')
    @api.response(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.expect(atualiza_colaboradores_model, validate=True, skip_none=True)
    @api.marshal_with(atualiza_colaboradores_model, code=status.HTTP_200_OK)
    def patch(self, matricula):
        '''Atualiza um colaborador por matrícula'''
        data = request.json

        query_colaborador = Colaboradores.query.filter_by(matricula=matricula)
        if not query_colaborador.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')

        if not verifica_se_lider_enviado_existe(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O líder informado não existe'
            )
        if not verifica_se_lider_pode_ser_lider(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O líder informado não tem cargo de liderança'
            )
        if not verifica_se_cargo_enviado_existe(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O cargo_id informado não existe'
            )
        query_colaborador.update(data)
        Colaboradores.commit()
        if nova_matricula := data.get("matricula", False):
            query_colaborador = Colaboradores.query.filter_by(
                matricula=nova_matricula)
        return query_colaborador.first(), status.HTTP_200_OK

    @api.doc('delete_colaborador')
    @api.response(status.HTTP_204_NO_CONTENT, 'Sucesso (Sem conteúdo)')
    @api.response(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    def delete(self, matricula):
        '''Exclusão de colaborador'''
        query_colaborador = Colaboradores.query.filter_by(matricula=matricula)
        if not query_colaborador.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
        query_colaborador.delete()
        Colaboradores.commit()
        return "", status.HTTP_204_NO_CONTENT


@api.route('/<int:matricula>/demissao')
class ColaboradorDemissaoResource(Resource):
    '''Demissão de colaboradores'''

    @api.doc('demite_colaborador')
    @api.response(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.marshal_with(colaboradores_model, code=status.HTTP_200_OK)
    def patch(self, matricula):
        '''Demite colaborador'''
        query_colaborador = Colaboradores.query.filter_by(matricula=matricula)
        if not query_colaborador.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
        query_colaborador.update({"status_ativo": False})
        Colaboradores.commit()
        return query_colaborador.first(), status.HTTP_200_OK


@api.route('/<int:matricula>/promocao')
class ColaboradorPromocaoResource(Resource):
    '''Promoção de colaborador'''

    @api.doc('promove_colaborador')
    @api.response(status.HTTP_400_BAD_REQUEST, 'Informações enviadas não aceitas')
    @api.response(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.expect(promove_colaborador_model, validate=True, skip_none=True)
    @api.marshal_with(colaboradores_model, code=status.HTTP_200_OK)
    def patch(self, matricula):
        '''Promove colaborador'''
        data = request.json

        query_colaborador = Colaboradores.query.filter_by(matricula=matricula)
        if not query_colaborador.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')

        if not verifica_se_lider_enviado_existe(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O líder informado não existe'
            )
        if not verifica_se_lider_pode_ser_lider(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O líder informado não tem cargo de liderança'
            )
        if not verifica_se_cargo_enviado_existe(data):
            api.abort(
                status.HTTP_400_BAD_REQUEST,
                'O cargo_id informado não existe'
            )
        query_colaborador.update(data)
        Colaboradores.commit()
        return query_colaborador.first(), status.HTTP_200_OK


@api.route('/<int:matricula>/alterar-senha')
class ColaboradorAlterarSenhaResource(Resource):
    '''Alteração de senha de colaborador'''

    @api.doc('promove_colaborador')
    @api.response(status.HTTP_400_BAD_REQUEST, 'Informações enviadas não aceitas')
    @api.response(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
    @api.response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal Server error')
    @api.expect(alteracao_de_senha_model, validate=True)
    def patch(self, matricula):
        '''Altera senha do colaborador'''
        data = request.json
        query_colaborador = Colaboradores.query.filter_by(matricula=matricula)
        if not query_colaborador.first():
            api.abort(status.HTTP_404_NOT_FOUND, 'Colaborador não encontrado')
        if check_password(data.get("senha_atual"), query_colaborador.first().senha):
            query_colaborador.update(
                {"senha": get_hashed_password(data.get("nova_senha"))})
            Colaboradores.commit()
            return "Senha alterada com sucesso!", status.HTTP_200_OK
        return 'Senha incorreta', status.HTTP_400_BAD_REQUEST
