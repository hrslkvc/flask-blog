from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.models.user import User
from .db import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST',))
def register():
    data = request.json
    username = data['username']
    password = data['password']

    error = None

    if not username:
        error = 'Username is required'
    if not password:
        error = 'Password is required'

    if not error:
        try:
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            error = f"Username '{username}' is already taken"
        else:
            return jsonify({})

    if error:
        return {'error': error}, 400


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
