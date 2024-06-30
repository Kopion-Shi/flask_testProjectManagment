from flask_login import UserMixin
from applications.exts import sqlAlchemy_db as db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, id, username, ):
        self.id = id
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username
