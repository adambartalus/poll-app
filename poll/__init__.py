import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from poll import auth, main, poll
from poll.model import db
from poll.models import User


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        WTF_CSRF_SECRET_KEY='dev2',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + app.instance_path + '/poll.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        if user is None:
            return None
        return user

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(poll.bp)

    return app
