import os

from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from flaskr.db import db
from flaskr.models.post import Post
from flaskr.models.user import User

bp = Blueprint('posts', __name__)


@bp.route('/posts', methods=('GET',))
@jwt_required()
def index():
    posts = Post.query.all()

    posts = [post.to_dict() for post in posts]
    return jsonify(posts)


@bp.route('/posts', methods=('POST',))
@jwt_required()
def create():
    data = request.form
    image = request.files['image']

    filename = secure_filename(image.filename.replace(' ', ''))

    post = Post(title=data['title'], body=data['body'], author_id=get_jwt_identity()["id"], image=filename)
    db.session.add(post)
    db.session.commit()

    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    return jsonify(post.to_dict())


@bp.route('/posts/<post_id>', methods=('GET',))
@jwt_required()
def show(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({}), 404

    return jsonify(post.to_dict())


@bp.route('/posts/<post_id>', methods=('DELETE',))
@jwt_required()
def delete(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({}), 404

    if get_jwt_identity()['id'] != post.author_id:
        return jsonify({'error': 'Unauthorized'}), 402

    db.session.delete(post)
    db.session.commit()
    
    return jsonify({})


@bp.route('/author/<username>', methods=('GET',))
@jwt_required()
def by_author(username):
    author = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author_id=author.id).all()

    posts = [post.to_dict() for post in posts]

    return jsonify(posts)


@bp.route('/userinfo/<username>', methods=('GET',))
@jwt_required()
def userinfo(username):
    user = User.query.filter_by(username=username).first()

    return jsonify(user.to_dict())
