from flask import Blueprint, jsonify

from .models.post import Post
from .models.user import User

bp = Blueprint('api', __name__, url_prefix='/api/posts')


@bp.route('/')
def get_posts():
    posts = Post.query.all()

    posts = [post.to_dict() for post in posts]
    return jsonify(posts)


@bp.route('<post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({}), 404

    return jsonify(post.to_dict())


@bp.route('/author/<username>')
def get_posts_by_author(username):
    author = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author_id=author.id).all()

    posts = [post.to_dict() for post in posts]

    return jsonify(posts)
