import pytest
from urllib.parse import urlparse

from poll.models import Poll, PollTitle
from poll.utils import add_poll


def test_index(client, auth):
    response = client.get('/')
    assert b"Log in" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log out' in response.data


@pytest.mark.parametrize('path', (
    '/poll/1',
))
def test_login_required(client, path):
    response = client.post(path)
    assert urlparse(response.headers["Location"]).path == "/login"


def test_poll_redirect(client):
    response = client.get('/poll')
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/poll/create'


def test_create_poll(client, app):
    assert client.get('/poll/create').status_code == 200
    response = client.post(
        '/poll/create',
        data={
            'title': 'test',
            'answer_options-0': '1',
            'answer_options-1': '4',
            'answer_options-2': '9',
        }
    )
    assert urlparse(response.headers["Location"]).path == '/poll/1'
    with app.app_context():
        poll_q = PollTitle.query.filter_by(text='test').first()
        assert poll_q is not None
        poll = Poll.query.filter_by(id=poll_q.poll_id).first()
        assert poll is not None
        assert not poll.multiple
        poll_options = list(map(lambda x: x.text, poll.options))
        assert poll_options == ['1', '4', '9']


@pytest.mark.parametrize(('title', 'answer_options', 'multiple', 'messages'), (
    ('', ['', ''], False, [b'Title is required.', b'There should be at least 2 valid options.']),
    ('  ', ['test', ''], False, [b'Title is required.', b'There should be at least 2 valid options.']),
    ('test', ['test', ''], False, [b'There should be at least 2 valid options.']),
    ('', ['1', '7'], False, [b'Title is required.'])
))
def test_create_poll_validate_input(client, title, answer_options, multiple, messages):
    options = {f'answer_options-{i}': e for i, e in enumerate(answer_options)}
    response = client.post(
        '/poll/create',
        data={
            'title': title,
            'multiple_choices': multiple,
            **options
        }
    )
    for message in messages:
        assert message in response.data


def test_vote_poll(auth, client, app):
    client.post(
        '/poll/create',
        data={
            'title': 'test-title',
            'answer_options-0': '1',
            'answer_options-1': '4',
            'answer_options-2': '9',
        }
    )
    response = client.post(
        '/poll/1',
        data={
            'choice': '1'
        },
        follow_redirects=True
    )
    assert b'You have to log in to vote' in response.data
    auth.login()
    response = client.post(
        '/poll/1',
        data={
            'choice': ['1', '2']
        },
        follow_redirects=True
    )
    assert b'Multiple choices are not allowed on this poll' in response.data
    response = client.post(
        '/poll/1',
        data={
            'choice': '2'
        },
        follow_redirects=True
    )
    assert b'You have successfully voted on this poll' in response.data
    response = client.post(
        '/poll/1',
        data={
            'choice': '1'
        }
    )
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/poll/1'
    response = client.get('/poll/1')
    assert b'You have already voted on this poll' in response.data


def test_vote_no_selected_option(auth, client, app):
    add_poll(app, 'test-title', ['1', '4', '9'], False)
    auth.login()
    response = client.post(
        '/poll/1',
        data={}
    )
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/poll/1'
    response = client.get('/poll/1')
    assert b'You have to select at least one option' in response.data


def test_poll_not_exists(client):
    response = client.get('/poll/1')
    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == '/'
