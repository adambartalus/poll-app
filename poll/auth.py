
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from poll.db import get_db
from poll.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, EqualTo, DataRequired

bp = Blueprint('auth', __name__)


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('password')])


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # POST
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')

        get_db().execute(
            'INSERT INTO user (username, password)'
            ' VALUES (?, ?)',
            [username, generate_password_hash(password)]
        )
        get_db().commit()

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

    user_row = get_db().execute(
        'SELECT *'
        ' FROM user'
        ' WHERE username=?',
        [username]
    ).fetchone()
    if user_row is None or not check_password_hash(user_row['password'], password):
        return redirect(url_for('auth.login'))

    login_user(User(user_row['id'], user_row['username'], user_row['password']))
    return redirect(url_for('main.index'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
