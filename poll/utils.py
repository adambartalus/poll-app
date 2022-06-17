from poll.model import db
from poll.models import Poll, PollVote


def poll_exists(id_):
    poll = Poll.query.get(id_)

    return poll is not None


def get_vote_count(poll_option_id):
    votes = PollVote.query.filter_by(poll_option_id=poll_option_id).all()
    c = len(votes)

    return c
