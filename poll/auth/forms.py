from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField,  StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

MIN_PASSWORD_LENGTH = 8


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required.')])
    email = EmailField('Email', validators=[DataRequired(message='Email is required.'), Email()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=MIN_PASSWORD_LENGTH, message=f'Password must be at least {MIN_PASSWORD_LENGTH} characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class PasswordResetEmailForm(FlaskForm):
    email = EmailField('Email')
    submit = SubmitField('Send email')


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        'New password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=MIN_PASSWORD_LENGTH, message=f'Password must be at least {MIN_PASSWORD_LENGTH} characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm new password',
        validators=[
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Change password')
