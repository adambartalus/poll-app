from datetime import datetime
from functools import wraps

from flask_login import current_user

from poll.extensions import login_manager, db
from poll.models import Poll, PollOption, PollTitle


def poll_exists(id_):
    poll = Poll.query.get(id_)

    return poll is not None


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


def add_poll(app, title, options, multiple):
    with app.app_context():
        user_id = current_user.id if (current_user and current_user.is_authenticated) else None
        new_poll = Poll(multiple=multiple, created=datetime.now(), user_id=user_id)
        db.session.add(new_poll)
        db.session.flush()

        db.session.add(PollTitle(poll_id=new_poll.id, text=title))

        for option in options:
            db.session.add(PollOption(poll_id=new_poll.id, text=option))
        db.session.commit()
        return new_poll.id
