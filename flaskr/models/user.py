import datetime

from flaskr.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='author')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    liked_posts = db.relationship('PostLike', backref='user')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at,
            'post_count': len(self.posts),
            'comment_count': len(self.comments),
            'like_count': len(self.liked_posts)
        }
