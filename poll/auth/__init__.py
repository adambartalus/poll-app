from flask import Blueprint

from poll.auth import views

bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/auth/static'
)
bp.add_url_rule('/register', view_func=views.register, methods=['GET', 'POST'])
bp.add_url_rule('/login', view_func=views.login, methods=['GET', 'POST'])
bp.add_url_rule('/logout', view_func=views.logout)
bp.add_url_rule('/confirm/<token>', view_func=views.confirm_email)
bp.add_url_rule('/reset-password', view_func=views.password_reset_email, methods=['GET', 'POST'])
bp.add_url_rule('/reset-password/<token>', view_func=views.reset_password, methods=['GET', 'POST'])
