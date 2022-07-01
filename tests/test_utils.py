from poll.extensions import db
from poll.models import Poll, PollTitle, PollOption
from poll.utils import poll_exists


def test_poll_exists(app):
    with app.app_context():
        assert not poll_exists(1)
        new_poll = Poll()
        db.session.add(new_poll)
        db.session.flush()

        db.session.add(PollTitle(poll_id=new_poll.id, text='test_title'))

        for option in ['1', '2', '3']:
            db.session.add(PollOption(poll_id=new_poll.id, text=option))
        db.session.commit()

        assert poll_exists(1)


def test_voted_on(user):
    assert not user.voted_on(1)


def test_get_voted_polls(user, app):
    with app.app_context():
        assert user.get_voted_polls() == []
