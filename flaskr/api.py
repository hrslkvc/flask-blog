from flask import Blueprint, jsonify

from .services import post_service

bp = Blueprint('api', __name__, url_prefix='/api/posts')


@bp.route('/')
def get_posts():
    posts = post_service.get_many()

    posts = [dict(post) for post in posts]
    return jsonify(posts)


@bp.route('<post_id>')
def get_post(post_id):
    post = post_service.get_one(post_id, append_author=True)

    if not post:
        return jsonify({}), 404

    return dict(post)
