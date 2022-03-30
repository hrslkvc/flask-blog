from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from flaskr.db import db
from flaskr.models.post import Post
from flaskr.models.post_like import PostLike

bp = Blueprint('post_likes', __name__)


@bp.route('/likes/<post_id>', methods=('GET',))
@jwt_required()
def get_post_likes(post_id):
    post = Post.query.get(post_id)

    likes = [{'id': like.id, 'user_id': like.user.id, 'user_name': like.user.username} for
             like in post.likes]
    return jsonify(likes)


@bp.route('/users/likes/<user_id>', methods=('GET',))
@jwt_required()
def get_user_likes(user_id):
    post_likes = PostLike.query.filter_by(user_id=user_id).all()

    likes = [
        {'post_id': like.post.id, 'title': like.post.title, 'user_id': like.user.id, 'user_name': like.user.username}
        for
        like in post_likes]

    return jsonify(likes)


@bp.route('/likes/<post_id>', methods=('POST',))
@jwt_required()
def like(post_id):
    liked = PostLike.query.filter_by(user_id=get_jwt_identity()["id"], post_id=post_id).all()

    if liked:
        return jsonify({'error': 'You already liked this post'})

    post = Post.query.get(post_id)
    post.like_count += 1
    post_like = PostLike(user_id=get_jwt_identity()["id"], post_id=post_id)

    db.session.add(post)
    db.session.add(post_like)
    db.session.commit()
    return jsonify({})
