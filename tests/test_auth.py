from datetime import datetime
from time import sleep

from flask import current_app
from flask_login import current_user
import pytest
from urllib.parse import urlparse

from werkzeug.security import check_password_hash

from poll.token import generate_token, confirm_token
from poll.models import User


def test_register(client, app):
    assert client.get('/register').status_code == 200
    response = client.post(
        '/register',
        data={
            'username': 'a',
            'email': 'test@test.com',
            'password': '12345678',
            'confirm_password': '12345678'
        }
    )
    assert response.status_code == 302
    assert urlparse(response.headers["Location"]).path == '/login'
    with app.app_context():
        user = User.query.filter_by(username='a').first()
        assert user.username == 'a'
        assert user.email == 'test@test.com'
        assert not user.confirmed
        assert not user.confirmation_date
        assert (datetime.now() - user.registration_date).total_seconds() < 10
        assert len(list(user.votes)) == 0
        assert len(list(user.polls)) == 0
        assert check_password_hash(user.password_hash, '12345678')

        assert User.query.filter_by(username='b').first() is None


@pytest.mark.parametrize(('username', 'email', 'password', 'confirm_password', 'messages'), (
    ('', '', '', '', [b'Username is required.', b'Email is required.', b'Password is required.']),
    ('', '', '12345678', '', [b'Username is required.', b'Email is required.', b'Passwords must match.']),
    ('', '', '12345678', '12345678', [b'Username is required.', b'Email is required.']),
    ('a', '', '', '', [b'Email is required.', b'Password is required.']),
    ('a', '', '12345678', '', [b'Email is required.', b'Passwords must match.']),
    ('a', '', '1234567', '1234567', [b'Email is required.', b'Password must be at least 8 characters long.']),
    ('a', 'vmi', '', '', [b'Invalid email address.', b'Password is required.']),
    ('a', 'test@test.com', '23', '', [b'Password must be at least 8 characters long.', b'Passwords must match.']),
))
def test_register_validate_input(client, username, email, password, confirm_password, messages):
    response = client.post(
        '/register',
        data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
    )
    for message in messages:
        assert message in response.data


def test_login(client, auth):
    assert client.get('/login').status_code == 200
    response = auth.login()

    assert response.status_code == 302
    assert urlparse(response.headers["Location"]).path == '/'

    with client:
        client.get('/')
        assert current_user.is_authenticated
        assert current_user.username == 'test'


@pytest.mark.parametrize('next_', (
    '/user/voted-polls',
    '/poll/1',
    '/polls'
))
def test_login_with_next(client, next_):
    response = client.get(f'/login?next={next_}')
    b = f'<input type="hidden" name="next" value="{next_}">'.encode('utf-8')

    assert response.status_code == 200
    assert b in response.data


@pytest.mark.parametrize('next_', (
    '/user/voted-polls',
    '/poll/1',
    '/polls'
))
def test_login_safe_redirect(auth, next_):
    response = auth.login(next=next_)

    assert response.status_code == 302
    assert urlparse(response.headers['Location']).path == next_


@pytest.mark.parametrize('next_', (
    'https://www.facebook.com/',
    'https://www.youtube.com/',
    'https://www.vmi.com/3'
))
def test_login_not_safe_redirect(auth, next_):
    response = auth.login(next=next_)

    assert response.status_code == 400


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Invalid username or password.'),
    ('test', 'a', b'Invalid username or password.'),
))
def test_login_validate_input(auth, client, username, password, message):
    response = auth.login('a', 'b')

    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert not current_user.is_authenticated


def test_confirm_token(auth, client, app):
    auth.login()
    response = client.get(
        '/confirm/3',
        follow_redirects=True
    )
    auth.logout()
    assert b'The confirmation link is invalid or has expired.' in response.data

    test_email = 'test1@test1.com'
    response = client.post(
        '/register',
        data={
            'username': 'b',
            'email': test_email,
            'password': '12345678',
            'confirm_password': '12345678'
        }
    )
    assert response.status_code == 302
    assert urlparse(response.headers["Location"]).path == '/login'
    with app.app_context():
        user = User.query.filter_by(username='b').first()
        assert not user.confirmed
        token = generate_token(test_email, current_app.config['SECURITY_PASSWORD_SALT'])
    response = client.get(
        f'/confirm/{token}'
    )
    assert urlparse(response.headers['Location']).path == '/login'
    with app.app_context():
        user = User.query.filter_by(email=test_email).first()
        assert not user.confirmed

    auth.login()
    response = client.get(
        f'/confirm/{token}',
        follow_redirects=True
    )
    assert b'Wrong account' in response.data
    with app.app_context():
        user = User.query.filter_by(email=test_email).first()
        assert not user.confirmed

    auth.logout()

    auth.login(username='b', password='12345678')
    response = client.get(
        f'/confirm/{token}',
        follow_redirects=True
    )
    assert b'You have confirmed your account. Thanks!' in response.data
    with app.app_context():
        user = User.query.filter_by(email=test_email).first()
        assert user.confirmed

    response = client.get(
        f'/confirm/{token}',
        follow_redirects=True
    )
    assert b'Account already confirmed. Please log in.' in response.data
    with app.app_context():
        user = User.query.filter_by(email=test_email).first()
        assert user.confirmed


def test_confirm_token_expired(auth, client, app):
    test_email = 'test1@test1.com'
    client.post(
        '/register',
        data={
            'username': 'b',
            'email': test_email,
            'password': '12345678',
            'confirm_password': '12345678'
        }
    )
    with app.app_context():
        user = User.query.filter_by(username='b').first()
        assert not user.confirmed
        token = generate_token(test_email, '')

        sleep(5)
        assert not confirm_token(token, '', 4)
