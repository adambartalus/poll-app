from flask_login import UserMixin
from model import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    # def __init__(self, id_, username, password_hash):
    #     self.id = id_
    #     self.username = username
    #     self.password_hash = password_hash
