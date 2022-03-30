import datetime

from flask import url_for

from flaskr.db import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post')
    comment_count = db.Column(db.Integer, nullable=False, default=0)
    likes = db.relationship('PostLike', backref='post')
    like_count = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'created': self.created_at,
            'image': self.image,
            'image_url': url_for('static', filename=self.image),
            'title': self.title,
            'body': self.body,
            'author': self.author.to_dict(),
            'comments': [comment.to_dict() for comment in self.comments],
            'comment_count': self.comment_count,
            'like_count': self.like_count
        }
