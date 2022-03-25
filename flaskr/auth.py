from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
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


@bp.route('/login', methods=('POST',))
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 401

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Username doesnt exist"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(user.to_dict())
    return jsonify({"access_token": access_token, "user": user.to_dict()})


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
