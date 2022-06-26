from datetime import datetime

from flask_login import UserMixin

from poll.model import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmation_date = db.Column(db.DateTime, nullable=True)
    votes = db.relationship('PollVote', backref='user', lazy='dynamic')

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    multiple = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())
    options = db.relationship('PollOption', backref='poll', lazy=True)


class PollQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(64), nullable=False)


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(64), nullable=False)
    votes = db.relationship('PollVote', backref='poll_option', lazy=True)


class PollVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_option_id = db.Column(db.Integer, db.ForeignKey('poll_option.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
