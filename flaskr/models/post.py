import datetime

from flaskr.db import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    image = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User')

    def to_dict(self):
        return {
            'id': self.id,
            'created': self.created,
            'image': self.image,
            'title': self.title,
            'body': self.body,
            'author': self.author.to_dict()
        }
