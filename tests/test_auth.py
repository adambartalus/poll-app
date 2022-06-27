from flask_login import current_user
import pytest

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
    assert response.headers["Location"] == 'http://localhost/login'
    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None
        assert User.query.filter_by(username='b').first() is None


@pytest.mark.parametrize(('username', 'email', 'password', 'confirm_password', 'messages'), (
    ('', '', '', '', [b'Username is required.', b'Email is required.', b'Password is required.']),
    ('a', '', '', '', [b'Email is required.', b'Password is required.']),
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

    assert response.headers["Location"] == 'http://localhost/'

    with client:
        client.get('/')
        assert current_user.is_authenticated
        assert current_user.username == 'test'


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
