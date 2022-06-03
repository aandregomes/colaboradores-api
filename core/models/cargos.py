import datetime
from sqlalchemy.orm import validates
from db import db
from .abc import BaseModel


class Cargos(db.Model, BaseModel):
    __tablename__ = "cargos"

    id = db.Column(
        db.Integer,
        db.Identity(start=1, cycle=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    cargo = db.Column(db.String(50), unique=True, nullable=False)
    lider = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    @validates('cargo')
    def converter_para_lowercase(self, key, value):
        return value.lower()

    def __repr__(self):
        return f'<Cargo {self.cargo}>'
