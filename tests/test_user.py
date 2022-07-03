import pytest
from urllib.parse import urlparse

from poll.models import Poll
from poll.utils import add_poll


@pytest.mark.parametrize('path', (
    '/user/voted-polls',
    '/user/my-polls'
))
def test_login_required(client, path):
    response = client.get(path)
    assert urlparse(response.headers["Location"]).path == "/login"


def test_no_voted_polls(client, auth):
    auth.login()
    response = client.get('/user/voted-polls')

    assert b"You haven't voted on any polls." in response.data


def test_voted_polls(client, app, auth):
    add_poll(app, 'test-title', ['1', '4', '9'], False)

    auth.login()
    client.post(
        '/poll/1',
        data={
            'choice': 1
        }
    )
    response = client.get('/user/voted-polls')
    assert b"test-title" in response.data


def test_no_my_polls(client, auth):
    auth.login()
    response = client.get('/user/my-polls')

    assert b"You haven't created any polls." in response.data


def test_my_polls(client, app, auth):
    auth.login()
    client.post(
        '/poll/create',
        data={
            'title': 'test-title',
            'answer_options-0': '1',
            'answer_options-1': '4',
            'answer_options-2': '9',
            'multiple_choices': False
        }
    )
    with app.app_context():
        poll = Poll.query.filter_by(id=1).first()
        assert poll is not None

    response = client.get('/user/my-polls')
    assert b"test-title" in response.data
