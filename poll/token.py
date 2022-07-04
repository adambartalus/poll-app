from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def generate_token(email, salt):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def confirm_token(token, salt, expiration=3600):
    """
    Extracts the string encoded in the token.

    Args:
        token:
        salt: security salt
        expiration: expiration time in seconds

    Returns:
        the email encoded in the token

    Raises:
        BadSignature: if the token is invalid
        SignatureExpired: if the token is expired
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt=salt,
        max_age=expiration
    )

    return email
