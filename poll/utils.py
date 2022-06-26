from poll.models import Poll, PollVote


def poll_exists(id_):
    poll = Poll.query.get(id_)

    return poll is not None


def voted_on(user, poll_id):
    for vote in user.votes:
        if vote.poll_option.poll.id == poll_id:
            return True
    return False


def get_vote_count(poll_option_id):
    vote_count = PollVote.query.filter_by(poll_option_id=poll_option_id).count()

    return vote_count
