import pytest
from werkzeug.security import generate_password_hash

from poll import create_app
from poll.extensions import db
from poll.models import User


@pytest.fixture()
def app():
    app = create_app('config.TestConfig')
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(User('test', 'test@test.com', generate_password_hash('test')))
        db.session.commit()
    yield app


@pytest.fixture()
def user(app):
    with app.app_context():
        return User.query.filter_by(username='test').first()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test', follow_redirects=False, **kwargs):
        return self._client.post(
            '/login',
            data={
                'username': username,
                'password': password,
                **kwargs
            },
            follow_redirects=follow_redirects
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
