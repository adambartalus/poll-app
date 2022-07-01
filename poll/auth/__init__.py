from flask import Blueprint

from . import views

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
