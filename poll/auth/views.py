from datetime import datetime

from flask import redirect, render_template, url_for, flash, request, abort, current_app
from flask_login import login_required, login_user, logout_user, current_user
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from poll.auth.forms import RegisterForm, LoginForm, PasswordResetEmailForm, PasswordResetForm
from poll.email import send_password_reset_email, send_confirmation_email
from poll.extensions import db
from poll.models import User
from poll.safe_redirect import is_safe_url
from poll.token import confirm_token
from poll.utils import custom_login_message


def register():
    form = RegisterForm()
    # POST
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username, email, generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        send_confirmation_email(user.email, user.username)

        return redirect(url_for('auth.login'))
    # GET
    return render_template('auth/register.html', form=form)


def login():
    next_ = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        next_url = request.form.get('next')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            if not is_safe_url(next_url):
                abort(400)

            return redirect(next_url or url_for('main.index'))

        flash('Invalid username or password.', 'error')

    return render_template('auth/login.html', form=form, next=next_)


@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@custom_login_message(message='Log in to finish email verification', category='info')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token, current_app.config['SECURITY_PASSWORD_SALT'])
    except (BadSignature, SignatureExpired):
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('main.index'))

    try:
        user = User.query.filter_by(email=email).first_or_404()
    except NotFound:
        flash(f'There is no account with the email {email}', 'error')
        return redirect(url_for('main.index'))

    if user.id != current_user.id:
        flash('Wrong account', 'error')
        return redirect(url_for('main.index'))
    if user.confirmed:
        flash('Account already confirmed. Please log in.', 'success')
    else:
        user.confirmed = True
        user.confirmation_date = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))


def reset_password(token):
    try:
        email = confirm_token(token, current_app.config['PASSWORD_RESET_SALT'], 600)
    except (BadSignature, SignatureExpired):
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.login'))

    try:
        user = User.query.filter_by(email=email).first_or_404()
    except NotFound:
        flash('Invalid email address!', 'error')
        return redirect(url_for('auth.login'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your password has been changed!', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form, token=token)


def password_reset_email():
    form = PasswordResetEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        try:
            User.query.filter_by(email=email).first_or_404()
            send_password_reset_email(email)
            flash('A password reset link has been sent to your email', 'success')
            return redirect(url_for('auth.login'))
        except NotFound:
            flash('There is no account with this email', 'warning')

    return render_template('auth/password_reset_email.html', form=form)
