import datetime
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from . import auth, posts, api, comments
from .db import db, db_create_all
from .models import user, post, comment


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_AUTH_URL_RULE='/auth/login',
        JWT_EXPIRATION_DELTA=datetime.timedelta(seconds=86400)
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
    app.register_blueprint(comments.bp)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')

    db.app = app
    db.init_app(app)

    app.cli.add_command(db_create_all)
    Migrate(app, db)
    CORS(app)
    JWTManager(app)
    return app
