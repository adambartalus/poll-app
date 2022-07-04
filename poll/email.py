from threading import Thread

from flask import current_app, url_for, render_template
from flask_mail import Message

from poll.extensions import mail
from poll.token import generate_token


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@async_
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    send_async_email(current_app._get_current_object(), msg)


def send_password_reset_email(email):
    token = generate_token(email, current_app.config['PASSWORD_RESET_SALT'])
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    html = render_template('auth/reset.html', password_reset_url=reset_url)
    subject = 'Password Reset'

    send_email(email, subject, html)
