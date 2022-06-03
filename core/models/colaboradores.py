import datetime
from db import db
from .abc import BaseModel


class Colaboradores(db.Model, BaseModel):
    __tablename__ = 'colaboradores'

    matricula = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False,
    )
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    cargo_id = db.Column(db.Integer, db.ForeignKey("cargos.id"))
    cargo = db.relationship("Cargos", foreign_keys=[cargo_id])
    matricula_lider = db.Column(
        db.Integer,
        db.ForeignKey('colaboradores.matricula'),
        index=True
    )
    nome_lider = db.relationship(
        lambda: Colaboradores,
        remote_side=matricula,
        backref='lider'
    )
    salario = db.Column(db.Float, nullable=False, default=0)
    status_ativo = db.Column(db.Boolean, nullable=False, default=True)
    senha = db.Column(db.String(300), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    def __repr__(self):
        return f'<Colaborador {self.nome}>'
