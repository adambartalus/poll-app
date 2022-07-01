from datetime import datetime

from flask import redirect, render_template, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from poll.auth.forms import RegisterForm, LoginForm
from poll.email import send_email
from poll.extensions import db
from poll.models import User
from poll.safe_redirect import is_safe_url
from poll.token import generate_confirmation_token, confirm_token


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

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url, username=username)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

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


@login_required
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.id != current_user.id:
        flash('Wrong account')
        return redirect(url_for('main.index'))
    if user.confirmed:
        flash('Account already confirmed. Please log in.', 'success')
    else:
        user.confirmed = True
        user.confirmation_date = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.index'))
