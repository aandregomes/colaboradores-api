import bcrypt
from core.models.cargos import Cargos
from core.models.colaboradores import Colaboradores


def get_hashed_password(senha):
    """
    Faz o hash da senha pela primeira vez e o salt é salvo no hash
    """
    return bcrypt.hashpw(senha, bcrypt.gensalt())


def check_password(senha, senha_hashed):
    """
    Verifica uma senha hashed com o salt já salvo
    """
    return bcrypt.checkpw(senha, senha_hashed)


def verifica_se_lider_enviado_existe(data):
    if matricula_lider := data.get("matricula_lider", False):
        if not Colaboradores.query.filter_by(matricula=matricula_lider).first():
            return False
    """
    No caso de a matrícula de líder não ter sida enviada no payload.
    ! Só poderá acontecer se o colaborador for líder
    """
    return True


def verifica_se_lider_pode_ser_lider(data):
    if matricula_lider := data.get("matricula_lider", False):
        cargo_lider = Colaboradores.query.filter_by(
            matricula=matricula_lider).first().cargo
        if cargo_lider.lider is True:
            return True
        return False
    """
    No caso de a matrícula de líder não ter sida enviada no payload.
    ! Só poderá acontecer se o colaborador for líder
    """
    return True


def verifica_se_cargo_enviado_existe(data):
    if cargo_id := data.get("cargo_id", False):
        if not Cargos.query.filter_by(id=cargo_id).first():
            return False
    """
    No caso de o cargo não ter sido enviado no payload.
    ! Só poderá acontecer no cado de PUT/PATCH
    """
    return True
