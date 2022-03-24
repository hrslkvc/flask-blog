from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from flaskr.db import db
from flaskr.models.comment import Comment

bp = Blueprint('comments', __name__)


@bp.route('/comments', methods=('GET',))
@jwt_required()
def index():
    comments = Comment.query.all()

    comments = [comment.to_dict() for comment in comments]
    return jsonify(comments)


@bp.route('/comments', methods=('POST',))
@jwt_required()
def create():
    data = request.json

    comment = Comment(text=data['text'], author_id=data['author_id'], post_id=data['post_id'])

    db.session.add(comment)
    db.session.commit()

    post = comment.post
    post.comment_count += 1
    db.session.add(post)
    db.session.commit()

    return jsonify(comment.to_dict())
