import pytest
from urllib.parse import urlparse

from poll.models import Poll


@pytest.mark.parametrize('path', (
    '/user/voted-polls',
))
def test_login_required(client, path):
    response = client.get(path)
    assert urlparse(response.headers["Location"]).path == "/login"


def test_no_voted_polls(client, auth):
    auth.login()
    response = client.get('/user/voted-polls')

    assert b"You haven't voted on any polls." in response.data


def test_voted_polls(client, app, auth):
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
        print(list(map(lambda x: x.id, poll.options)))
    auth.login()
    client.post(
        '/poll/1/vote',
        data={
            'choice': 1
        }
    )
    response = client.get('/user/voted-polls')
    print(response.data)
    assert b"test-title" in response.data
