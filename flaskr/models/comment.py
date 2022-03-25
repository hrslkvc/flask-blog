import datetime

from flaskr.db import db


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # parent_id = db.Column(db.Integer, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "text": self.text,
            "post_id": self.post_id,
            "author_id": self.author_id
        }
