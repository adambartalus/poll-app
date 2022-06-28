import pytest
from werkzeug.security import generate_password_hash

from poll import create_app
from poll.model import db
from poll.models import User

def app1():
    app = create_app('config.TestConfig')
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(User('test', '', generate_password_hash('test')))
        db.session.commit()
    yield app
@pytest.fixture()
def app():
    app = create_app('config.TestConfig')
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(User('test', '', generate_password_hash('test')))
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
