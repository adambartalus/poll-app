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

    def get_voted_polls(self):
        """

        Returns: the polls that the user has voted on

        """
        voted_poll_ids = [vote.poll_option.poll_id for vote in self.votes]
        return Poll.query.filter(Poll.id.in_(voted_poll_ids)).all()

    def voted_on(self, poll_id):
        """

        Args:
            poll_id: the id of the poll

        Returns: whether the user has voted on the poll with the id poll_id

        """
        for vote in self.votes:
            if vote.poll_option.poll.id == poll_id:
                return True
        return False


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    multiple = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now())
    options = db.relationship('PollOption', backref='poll', lazy=True)
    title = db.relationship('PollTitle', backref='poll', uselist=False)

    @staticmethod
    def get_most_popular(n):
        polls = Poll.query.all()
        polls.sort(reverse=True, key=Poll.get_vote_count)
        return polls[:n]

    @staticmethod
    def get_most_recent(n):
        polls = Poll.query.all()
        polls.sort(reverse=True, key=lambda x: x.created)
        return polls[:n]

    def get_vote_count(self):
        return sum(map(lambda x: x.get_vote_count(), self.options))


class PollTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(64), nullable=False)


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(64), nullable=False)
    votes = db.relationship('PollVote', backref='poll_option', lazy=True)

    def get_vote_count(self):
        return len(self.votes)


class PollVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_option_id = db.Column(db.Integer, db.ForeignKey('poll_option.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
