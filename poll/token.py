from flask import current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature


def generate_token(email, salt):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except BadSignature:
        return False
    return email
