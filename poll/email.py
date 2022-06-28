from threading import Thread

from flask import current_app
from flask_mail import Message

from poll.model import mail


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
