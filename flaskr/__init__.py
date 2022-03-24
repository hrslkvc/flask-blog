import os

from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT

from flaskr.models.user import User
from . import auth, posts, api
from .db import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_AUTH_URL_RULE='/auth/login'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(api.bp)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')
    db.app = app
    db.init_app(app)
    CORS(app)
    jwt = JWT(app, auth.authenticate, auth.identity)
    return app
