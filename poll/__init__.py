import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from poll.db import get_db
from poll.models import User


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        WTF_CSRF_SECRET_KEY='dev2',
        DATABASE=os.path.join(app.instance_path, 'poll.sqlite'),
    )
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_row = get_db().execute(
            'SELECT *'
            ' FROM user'
            ' WHERE id=?',
            [user_id]
        ).fetchone()
        if user_row is None:
            return None
        return User(user_row['id'], user_row['username'], user_row['password'])

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth, main, poll
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(poll.bp)

    return app
