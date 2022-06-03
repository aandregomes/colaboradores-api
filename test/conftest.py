import pytest
from app import create_app
from db import db


@pytest.fixture(scope='function')
def app():
    app = create_app("test")
    db.app = app
    db.create_all()
    yield app

    db.session.remove()
    db.drop_all()
