from db import db


class BaseModel:
    def save(self):
        db.session.add(self)
        db.session.commit()
        return db.session.refresh(self)

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def commit():
        db.session.commit()
