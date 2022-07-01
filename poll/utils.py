from functools import wraps

from poll.extensions import login_manager
from poll.models import Poll, PollVote


def poll_exists(id_):
    poll = Poll.query.get(id_)

    return poll is not None


def get_vote_count(poll_option_id):
    vote_count = PollVote.query.filter_by(poll_option_id=poll_option_id).count()

    return vote_count


def custom_login_message(message=None, category=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            basic_message = login_manager.login_message
            basic_message_category = login_manager.login_message_category
            login_manager.login_message = message or basic_message
            login_manager.login_message_category = category or basic_message_category
            to_return = func(*args, **kwargs)
            login_manager.login_message = basic_message
            login_manager.login_message_category = basic_message_category
            return to_return

        return inner

    return wrapper
