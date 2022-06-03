from core.models.colaboradores import Colaboradores


def verifica_se_ha_colaboradores_com_cargo(cargo_id):
    if Colaboradores.query.filter_by(cargo_id=cargo_id).first():
        return True
    return False
