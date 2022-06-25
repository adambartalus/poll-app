from flask import current_app
from flask_mail import Message

from poll.model import mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    print(msg.sender)
    mail.send(msg)