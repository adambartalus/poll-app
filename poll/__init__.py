import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from poll import auth, main, poll, user
from poll.extensions import db, login_manager, migrate, mail
from poll.models import User


def create_app(config='config.DevConfig'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
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
    app.register_blueprint(user.bp)

    return app
