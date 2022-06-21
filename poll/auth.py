from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import Length, EqualTo, DataRequired

from poll.model import db
from poll.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('password')])


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # POST
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db.session.add(User(username, generate_password_hash(password)))
        db.session.commit()

        return redirect(url_for('auth.login'))
    # GET
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # GET
    if request.method == 'GET':
        return render_template('auth/login.html')
    # POST
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password_hash, password):
        # TODO: mark errors
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
