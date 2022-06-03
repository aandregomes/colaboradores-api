from flask import Flask
from flask_migrate import Migrate
from apis import api
from config import get_config
from db import db


def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    db.init_app(app)
    Migrate(app, db)
    api.init_app(app)
    return app
