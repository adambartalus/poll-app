from datetime import datetime

from flask_login import UserMixin

from poll.model import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    multiple = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())


class PollQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(64), nullable=False)


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(64), nullable=False)


class PollVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_option_id = db.Column(db.Integer, db.ForeignKey('poll_option.id'), nullable=False)
