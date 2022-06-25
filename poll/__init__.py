import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

from poll import auth, main, poll
from poll.model import db, mail
from poll.models import User


load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        WTF_CSRF_SECRET_KEY='dev2',
        SECURITY_PASSWORD_SALT='random',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + app.instance_path + '/poll.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=os.environ.get("APP_MAIL_USERNAME"),
        MAIL_PASSWORD=os.environ.get("APP_MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER='badam.flask@gmail.com'
    )
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(poll.bp)

    return app
