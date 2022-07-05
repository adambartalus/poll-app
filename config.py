from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = 'default'
    WTF_CSRF_SECRET_KEY = 'def'
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    PASSWORD_RESET_SALT = environ.get('PASSWORD_RESET_SALT')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/poll.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get("APP_MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("APP_MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = environ.get("APP_MAIL_DEFAULT_SENDER")

    TESTING = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    SECRET_KEY = environ.get('PROD_SECRET_KEY')
    WTF_CSRF_SECRET_KEY = environ.get('PROD_WTF_CSRF_SECRET_KEY')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SECRET_KEY = environ.get('DEV_SECRET_KEY')
    WTF_CSRF_SECRET_KEY = environ.get('DEV_WTF_CSRF_SECRET_KEY')


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/poll_test.sqlite'
